#!/usr/bin/env python3
"""check_artifact - verify a rendered Simply Strategy artifact.

Every claim this product makes is checkable, so it gets checked by a script
rather than by a judgement: is every sentence under the limit, does every claim
carry a source pointer, did the renderer drop a section, does the page fit its
reading time.

    python3 scripts/check_artifact.py runs/<slug>/
    python3 scripts/check_artifact.py runs/<slug>/simple-strategy-artifact.html
    python3 scripts/check_artifact.py runs/<slug>/ --json

Exit code 1 when a hard check fails, so a run can gate on it.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# One ruler and one set of budgets, shared with plainlint on 04-plain.md, so a
# sentence cannot pass the markdown and fail the page, or the reverse. The module
# lives next to plainlint; the path is relative to this file, so it holds in a
# clone and installed under the plugin root alike.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "plain" / "scripts"))
from textlib import (  # noqa: E402
    L1_MAX_SENTENCE as MAX_WORDS, MAX_CAPTION_WORDS, MAX_PAGE_WORDS, TOFILL, WPM,
    count_words, split_sentences,
)

# The six sections, in order, with the name each is reported under. The
# definition is skills/flatten/references/output.md; these are its ids.
SECTIONS = {
    "one": "The one sentence",
    "must-solve": "Three things must be solved",
    "stop": "What we stop doing",
    "bet": "What has to be true",
    "conflicts": "What the documents disagree about",
    "gaps": "What we do not know",
}
# Sections 3 to 6 may report that the plan does not answer them. They may never
# be absent, because a missing section reads as a complete answer.
MAY_BE_UNANSWERED = {"stop", "bet", "conflicts"}

# How much content a section needs before it counts as answered. Section 1 is one
# sentence by design and section 6 can legitimately hold a single gap, so a flat
# threshold would fail exactly the pages that got it right.
MIN_CONTENT = {"one": 30, "must-solve": 120, "stop": 120,
               "bet": 120, "conflicts": 120, "gaps": 30}

# What matters is whether the page fetches anything, not whether a URL appears in
# it. An inline SVG declares xmlns="http://www.w3.org/2000/svg" and fetches
# nothing, so a bare https?:// match rejected exactly the output DESIGN.md asks
# for. Match the loading constructs instead.
NETWORK = re.compile(
    r"""<img\b                          # an image element
      | <script\b                       # a script element
      | <(?:iframe|object|embed|video|audio|source|track)\b
      | @import\b                       # a css import
      | \b(?:src|href|data|poster)\s*=\s*["']?\s*(?:https?:)?//   # a remote reference
      | url\(\s*["']?\s*(?:https?:)?//  # a remote css url()
    """,
    re.I | re.X,
)
UNFILLED = re.compile(r"\{\{[A-Z_]+\}\}")
UNANSWERED = re.compile(r"does not (?:say|answer|name|state)|is not (?:answered|named|stated)"
                        r"|no .{0,30}(?:is named|was named|were found)", re.I)
SUPREF = re.compile(r"<sup>\s*[\d,\s]+\s*</sup>", re.I)
POINTER = re.compile(r"\([^()]*\.(?:md|pdf|txt|docx|pptx|csv|xlsx)[^()]*\bp\.?\s?\d+[^()]*\)", re.I)
EM_DASH = re.compile(r"[\u2014\u2013]")
KICKER = re.compile(r'<span class="kicker">.*?</span>', re.S | re.I)
MUST = re.compile(r'<div class="must">.*?(?=<div class="must">|</section>)', re.S)


@dataclass
class Result:
    checks: list = field(default_factory=list)

    def add(self, name, ok, detail="", hard=True):
        """ok=True passed, ok=False failed, ok=None could not run.

        A check that scanned nothing has not passed. A false pass is more
        expensive than a false fail, so "not run" is its own outcome and it
        blocks shipping the same way a failure does.
        """
        self.checks.append({"check": name, "ok": ok, "detail": detail, "hard": hard})

    @property
    def failed_hard(self):
        return [c for c in self.checks if c["hard"] and c["ok"] is False]

    @property
    def not_run(self):
        return [c for c in self.checks if c["ok"] is None]

    @property
    def warned(self):
        return [c for c in self.checks if not c["hard"] and not c["ok"]]


BLOCK = ("p", "div", "li", "td", "th", "tr", "h1", "h2", "h3", "h4", "section",
         "ul", "ol", "table", "br", "hr", "figcaption", "blockquote")


SVG = re.compile(r"<svg\b.*?</svg>", re.S | re.I)


def text_of(fragment: str) -> str:
    """Visible text: drop tags, comments, style and script blocks.

    A closing block tag ends a sentence. Without this, three table cells or three
    list items run together into one very long "sentence" and the length check
    reports a failure that is not there.
    """
    # A superscript reference marker is punctuation, not a word, and leaving it in
    # split one sentence into two and merged the halves of the next.
    f = SUPREF.sub("", fragment)
    # Text inside a figure is a label. A reader reads it, but it is not prose and
    # holding a drawing to a sentence limit measures the wrong thing.
    f = SVG.sub(" ", f)
    f = re.sub(r"<!--.*?-->", " ", f, flags=re.S)
    f = re.sub(r"<(style|script)\b.*?</\1>", " ", f, flags=re.S | re.I)
    f = re.sub(rf"</?(?:{'|'.join(BLOCK)})\b[^>]*>", " \u2028 ", f, flags=re.I)
    f = re.sub(r"<[^>]+>", " ", f)
    f = html.unescape(f)
    f = re.sub(r"[ \t]+", " ", f)
    return re.sub(r"(?:\s*\u2028\s*)+", "\u2028", f).strip(" \u2028")


DETAILS = re.compile(r"<details\b.*?</details>", re.S | re.I)


def drop_provenance(fragment: str) -> str:
    """Remove the collapsed <details> blocks before measuring.

    They are the log living on the page: the chain that supports a claim, not the
    claim. Holding provenance to fifteen words would make it useless, and counting
    it against the page budget would punish a page for showing its working. Same
    reasoning as reasoning.html, which has no budget either.
    """
    return DETAILS.sub(" ", fragment)


def section(doc: str, sid: str) -> str:
    m = re.search(rf'<section[^>]*id="{re.escape(sid)}".*?</section>', doc, re.S | re.I)
    return m.group(0) if m else ""


def sentences(t: str):
    """Split on sentence enders, the way plainlint does. A source pointer in brackets
    is not a sentence, and a closing block tag (U+2028 from text_of) always ends one."""
    t = POINTER.sub(" ", t)
    t = TOFILL.sub(" TOFILL ", t)
    return [s for block in t.split("\u2028") for s in split_sentences(block)]


def check_artifact(path: str, r: Result, max_page_words: int = MAX_PAGE_WORDS) -> None:
    doc = open(path, encoding="utf-8").read()
    secs = {sid: section(doc, sid) for sid in SECTIONS}

    missing = [s for s in SECTIONS if not secs[s]]
    r.add("All six sections present", not missing,
          "missing: " + ", ".join(SECTIONS[s] for s in missing) if missing else "6 of 6")

    unfilled = sorted(set(UNFILLED.findall(doc)))
    r.add("No unfilled template slots", not unfilled,
          ", ".join(unfilled[:6]) if unfilled else "none")

    net = sorted(set(m.group(0) for m in NETWORK.finditer(doc)))
    r.add("Self-contained, nothing loads", not net,
          ", ".join(net[:5]) if net else "no img, script, CDN or remote font")

    scanned = [s for s in SECTIONS if secs[s]]
    musts = MUST.findall(secs["must-solve"])
    r.add("Exactly three must-solve items",
          None if not secs["must-solve"] else len(musts) == 3,
          "the must-solve section was not found" if not secs["must-solve"]
          else f"found {len(musts)}")

    # Either form counts: an inline (file.md p. 6) or a superscript numeral that
    # resolves against the reference list at the foot of the page. The second is
    # the better one to read, so refusing it would push the page back to clutter.
    unsourced = [re.sub(r"^\d+\s*", "", text_of(m))[:60]
                 for m in musts if not (POINTER.search(m) or SUPREF.search(m))]
    unsourced = [u.replace("\u2028", " ") for u in unsourced]
    r.add("Every must-solve carries a source pointer",
          None if not musts else not unsourced,
          "no must-solve items to check" if not musts
          else "; ".join(unsourced) if unsourced else f"{len(musts)} of {len(musts)}")

    long_sentences = []
    for sid, body in secs.items():
        if not body:
            continue
        # the kicker is a label, not a sentence
        body = KICKER.sub(" ", drop_provenance(body))
        for s in sentences(text_of(body)):
            n = count_words(s)
            if n > MAX_WORDS:
                long_sentences.append((SECTIONS[sid], n, re.sub(r"^\d+\s*", "", s)[:70]))
    r.add(f"Every sentence under {MAX_WORDS} words",
          None if not scanned else not long_sentences,
          "no sections to scan" if not scanned
          else "; ".join(f"{sec}: {n}w: {s}" for sec, n, s in long_sentences[:4])
          if long_sentences else f"longest is within the limit, {len(scanned)} section(s) scanned")

    # A section the material cannot answer says so in a sentence. It is never left
    # thin and never dropped, because a short section reads as a complete answer
    # and the reader cannot tell "nothing to report" from "not checked".
    thin, unsaid = [], []
    for sid, body in secs.items():
        if not body:
            continue
        content = text_of(KICKER.sub(" ", body))
        if len(content) >= MIN_CONTENT[sid]:
            continue
        if sid in MAY_BE_UNANSWERED and UNANSWERED.search(content):
            continue                      # short on purpose, and it says so
        (unsaid if sid in MAY_BE_UNANSWERED else thin).append(SECTIONS[sid])
    r.add("No section is silently empty", None if not scanned else not thin,
          "no sections to scan" if not scanned else ", ".join(thin) if thin else "none")
    r.add("A short optional section says it is unanswered", None if not scanned else not unsaid,
          "no sections to scan" if not scanned
          else ", ".join(f"{n} is thin and does not say why" for n in unsaid) if unsaid
          else "none short, or each says so")

    vague = [t.strip() for t in TOFILL.findall(doc) if len(t.strip()) < 4]
    r.add("Every TO FILL says what is needed", not vague,
          f"{len(vague)} bare marker(s)" if vague else f"{len(TOFILL.findall(doc))} marker(s), all described")

    body_only = re.sub(r"<(style|script)\b.*?</\1>", " ", doc, flags=re.S | re.I)
    dashes = EM_DASH.findall(text_of(body_only))
    r.add("No em dashes in the copy", not dashes, f"{len(dashes)} found" if dashes else "none")

    # The page promises a reading time. Correct is not the same as short enough.
    total = count_words(text_of(drop_provenance(body_only)).replace("\u2028", " "))
    minutes = total / WPM
    r.add(f"Fits its reading time, {max_page_words} words", total <= max_page_words,
          f"{total} words, about {minutes:.1f} minutes at {WPM} a minute"
          f"{'' if total <= max_page_words else f'. Over by {total - max_page_words}'}")

    # The line under a must-solve is set in caption type. An essay in caption type
    # puts the evidence a CFO wants in the smallest text on the page.
    long_support = []
    for i, m in enumerate(musts, 1):
        for cap in re.findall(r'class="caption"[^>]*>(.*?)</p>', m, re.S):
            n = count_words(text_of(cap).replace("\u2028", " "))
            if n > MAX_CAPTION_WORDS:
                long_support.append(f"{i}: {n}w")
    r.add(f"Supporting line stays a caption, {MAX_CAPTION_WORDS} words",
          None if not musts else not long_support,
          "no must-solve items to check" if not musts
          else ", ".join(long_support) if long_support else "all within")


def check_pointers(doc_path: str, material: str, r: Result) -> None:
    """Every pointer must name a file that exists in the material folder.

    Checking the shape of a pointer only proves it looks like one. A confident
    citation of a document nobody has is the exact failure this tool exists to
    catch, so the filenames get checked against the folder they claim to come from.
    """
    doc = open(doc_path, encoding="utf-8").read()
    have = {n.lower() for _, _, fs in os.walk(material) for n in fs}
    if not have:
        r.add("Pointers name real files", False, f"no files found under {material}")
        return
    named, unknown = set(), set()
    for p in POINTER.findall(doc):
        for f in re.findall(r"[\w.\-]+\.(?:md|pdf|txt|docx|pptx|csv|xlsx)", p, re.I):
            named.add(f.lower())
            if f.lower() not in have:
                unknown.add(f)
    r.add("Pointers name real files", not unknown,
          "not in the material folder: " + ", ".join(sorted(unknown)[:5]) if unknown
          else f"{len(named)} distinct file(s), all present")


def check_reasoning(path: str, r: Result) -> None:
    doc = open(path, encoding="utf-8").read()

    # An unfilled {{SLOT}} is not content. Without this, a bare template passes the
    # "not empty" checks on its own placeholders, which is the same false pass the
    # missing section ids produced, one level down.
    unfilled = sorted(set(UNFILLED.findall(doc)))
    r.add("reasoning.html has no unfilled slots", not unfilled,
          ", ".join(unfilled[:6]) if unfilled else "none")
    doc = UNFILLED.sub(" ", doc)
    for sid, label in [("cut", "What it threw away"), ("unsure", "Where it is unsure")]:
        body = section(doc, sid)
        content = text_of(re.sub(r"<th\b.*?</th>", " ", KICKER.sub(" ", body), flags=re.S | re.I))
        r.add(f'reasoning.html: "{label}" is not empty', len(content) > 25,
              f"{len(content)} characters of content")
    net = sorted(set(m.group(0) for m in NETWORK.finditer(doc)))
    r.add("reasoning.html self-contained", not net, ", ".join(net[:4]) if net else "nothing loads")
    r.add("reasoning.html names the input flatten level",
          bool(re.search(r"\bL[1-5]\b", text_of(section(doc, "unsure")))),
          "", hard=False)


def render(r: Result, files) -> str:
    out = ["## Artifact check", ""]
    out.append("| Check | Status | Detail |")
    out.append("| --- | --- | --- |")
    for c in r.checks:
        mark = ("⏭️ not run" if c["ok"] is None
                else "✅ pass" if c["ok"]
                else "❌ fail" if c["hard"] else "⚠️ watch")
        out.append(f"| {c['check']} | {mark} | {c['detail']} |")
    out.append("")
    hard, warn, skipped = len(r.failed_hard), len(r.warned), len(r.not_run)
    if skipped:
        out.append(f"**{skipped} check(s) could not run.** A check that scanned nothing is not a "
                   "check that passed. Fix the markup first, then read the rest of this table.")
        out.append("")
    if hard:
        out.append(f"**{hard} hard check(s) failed.** The artifact does not ship until these pass.")
    elif not skipped:
        out.append(f"All hard checks pass. {warn} thing(s) to look at." if warn
                   else "All checks pass.")
    out.append("")
    out.append("Checked: " + ", ".join(files))
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify a rendered Simply Strategy artifact.")
    ap.add_argument("target", help="a run directory, or the artifact html itself")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--material", help="material folder, to check that pointers name real files")
    ap.add_argument("--max-words", type=int, default=MAX_PAGE_WORDS,
                    help=f"word budget for the page (default {MAX_PAGE_WORDS})")
    a = ap.parse_args()

    if os.path.isdir(a.target):
        artifact = os.path.join(a.target, "simple-strategy-artifact.html")
        reasoning = os.path.join(a.target, "reasoning.html")
    else:
        artifact = a.target
        reasoning = os.path.join(os.path.dirname(artifact) or ".", "reasoning.html")

    if not os.path.exists(artifact):
        print(f"cannot find the artifact at {artifact}", file=sys.stderr)
        return 2

    r, files = Result(), [artifact]
    check_artifact(artifact, r, a.max_words)
    if a.material:
        check_pointers(artifact, a.material, r)
    else:
        # Silence here was the same failure this tool exists to catch: the table would
        # read 'all checks pass' on a page whose pointers were never validated.
        r.add("Pointers name real files", None,
              "not run, no --material given. Pointer shape was checked, existence was not")
    if os.path.exists(reasoning):
        check_reasoning(reasoning, r)
        files.append(reasoning)
    else:
        r.add("reasoning.html exists", False, "a run without a reasoning log is not finished")

    if a.json:
        print(json.dumps({"checks": r.checks,
                          "failed": len(r.failed_hard),
                          "not_run": len(r.not_run),
                          "warned": len(r.warned)}, indent=2))
    else:
        print(render(r, files))
    # not-run blocks shipping too. A page nobody could check is not a page that passed.
    return 1 if (r.failed_hard or r.not_run) else 0


if __name__ == "__main__":
    sys.exit(main())
