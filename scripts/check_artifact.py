#!/usr/bin/env python3
"""check_artifact - verify a rendered Simply Strategy artifact.

Every claim this product makes is checkable, so it gets checked by a script
rather than by an agent's opinion. Three of the reviewer's questions become
deterministic here: is every sentence under 15 words, does every claim carry a
source pointer, and did the renderer drop a section.

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

MAX_WORDS = 15
MAX_PAGE_WORDS = 1200          # about six minutes at 200 words a minute
WPM = 200
MAX_SUPPORT_WORDS = 40         # the line under a must-solve is a caption, not an essay
SECTIONS = ["one", "must-solve", "stop", "bet", "conflicts", "gaps"]
SECTION_NAMES = {
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
TOFILL = re.compile(r"\[TO FILL:([^\]]*)\]")
POINTER = re.compile(r"\([^()]*\.(?:md|pdf|txt|docx|pptx|csv|xlsx)[^()]*\bp\.?\s?\d+[^()]*\)", re.I)
EM_DASH = re.compile(r"[—–]")


@dataclass
class Result:
    checks: list = field(default_factory=list)

    def add(self, name, ok, detail="", hard=True):
        self.checks.append({"check": name, "ok": bool(ok), "detail": detail, "hard": hard})

    @property
    def failed_hard(self):
        return [c for c in self.checks if c["hard"] and not c["ok"]]

    @property
    def warned(self):
        return [c for c in self.checks if not c["hard"] and not c["ok"]]


BLOCK = ("p", "div", "li", "td", "th", "tr", "h1", "h2", "h3", "h4", "section",
         "ul", "ol", "table", "br", "hr", "figcaption", "blockquote")


def text_of(fragment: str) -> str:
    """Visible text: drop tags, comments, style and script blocks.

    A closing block tag ends a sentence. Without this, three table cells or three
    list items run together into one very long "sentence" and the length check
    reports a failure that is not there.
    """
    f = re.sub(r"<!--.*?-->", " ", fragment, flags=re.S)
    f = re.sub(r"<(style|script)\b.*?</\1>", " ", f, flags=re.S | re.I)
    f = re.sub(rf"</?(?:{'|'.join(BLOCK)})\b[^>]*>", " \u2028 ", f, flags=re.I)
    f = re.sub(r"<[^>]+>", " ", f)
    f = html.unescape(f)
    f = re.sub(r"[ \t]+", " ", f)
    return re.sub(r"(?:\s*\u2028\s*)+", "\u2028", f).strip(" \u2028")


def section(doc: str, sid: str) -> str:
    m = re.search(rf'<section[^>]*id="{re.escape(sid)}".*?</section>', doc, re.S | re.I)
    return m.group(0) if m else ""


def sentences(t: str):
    """Split on sentence enders. A source pointer in brackets is not a sentence."""
    t = POINTER.sub(" ", t)
    t = TOFILL.sub(" TOFILL ", t)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\u2028", t) if s.strip()]


def count_words(s: str) -> int:
    """Count the way ASD-STE100 does: a bracketed aside or a hyphenated word is one word."""
    s = re.sub(r"\([^)]*\)", " X ", s)
    return len([w for w in re.split(r"[\s ]+", s.strip()) if re.search(r"[A-Za-z0-9]", w)])


def check_artifact(path: str, r: Result) -> None:
    doc = open(path, encoding="utf-8").read()

    missing = [s for s in SECTIONS if not section(doc, s)]
    r.add("All six sections present", not missing,
          "missing: " + ", ".join(SECTION_NAMES[s] for s in missing) if missing else "6 of 6")

    unfilled = sorted(set(UNFILLED.findall(doc)))
    r.add("No unfilled template slots", not unfilled,
          ", ".join(unfilled[:6]) if unfilled else "none")

    net = sorted(set(m.group(0) for m in NETWORK.finditer(doc)))
    r.add("Self-contained, nothing loads", not net,
          ", ".join(net[:5]) if net else "no img, script, CDN or remote font")

    musts = re.findall(r'<div class="must">.*?</div>\s*</div>|<div class="must">.*?(?=<div class="must">|</section>)',
                       section(doc, "must-solve"), re.S)
    r.add("Exactly three must-solve items", len(musts) == 3, f"found {len(musts)}")

    unsourced = [re.sub(r"^\d+\s*", "", text_of(m))[:60] for m in musts if not POINTER.search(m)]
    unsourced = [u.replace("\u2028", " ") for u in unsourced]
    r.add("Every must-solve carries a source pointer", not unsourced,
          "; ".join(unsourced) if unsourced else f"{len(musts)} of {len(musts)}")

    long_sentences = []
    for sid in SECTIONS:
        body = section(doc, sid)
        if not body:
            continue
        # the kicker is a label, not a sentence
        body = re.sub(r'<span class="kicker">.*?</span>', " ", body, flags=re.S | re.I)
        for s in sentences(text_of(body)):
            n = count_words(s)
            if n > MAX_WORDS:
                long_sentences.append((SECTION_NAMES[sid], n, re.sub(r"^\d+\s*", "", s)[:70]))
    r.add(f"Every sentence under {MAX_WORDS} words", not long_sentences,
          "; ".join(f"{sec}: {n}w — {s}" for sec, n, s in long_sentences[:4])
          if long_sentences else "longest is within the limit")

    # A section the material cannot answer says so in a sentence. It is never left
    # thin and never dropped, because a short section reads as a complete answer
    # and the reader cannot tell "nothing to report" from "not checked".
    thin, unsaid = [], []
    for sid in SECTIONS:
        body = section(doc, sid)
        if not body:
            continue
        content = text_of(re.sub(r'<span class="kicker">.*?</span>', " ", body, flags=re.S))
        if len(content) >= 120:
            continue
        if sid in MAY_BE_UNANSWERED and UNANSWERED.search(content):
            continue                      # short on purpose, and it says so
        (unsaid if sid in MAY_BE_UNANSWERED else thin).append(SECTION_NAMES[sid])
    r.add("No section is silently empty", not thin,
          ", ".join(thin) if thin else "none")
    r.add("A short optional section says it is unanswered", not unsaid,
          ", ".join(f"{n} is thin and does not say why" for n in unsaid) if unsaid
          else "none short, or each says so")

    vague = [t.strip() for t in TOFILL.findall(doc) if len(t.strip()) < 4]
    r.add("Every TO FILL says what is needed", not vague,
          f"{len(vague)} bare marker(s)" if vague else f"{len(TOFILL.findall(doc))} marker(s), all described")

    body_only = re.sub(r"<(style|script)\b.*?</\1>", " ", doc, flags=re.S | re.I)
    dashes = EM_DASH.findall(text_of(body_only))
    r.add("No em dashes in the copy", not dashes, f"{len(dashes)} found" if dashes else "none")

    # The page promises a reading time. Nothing enforced it, and the first real run
    # came out at 2547 words against a four-minute promise. Correct is not the same
    # as short enough.
    total = count_words(text_of(body_only).replace("\u2028", " "))
    minutes = total / WPM
    r.add(f"Fits its reading time, {MAX_PAGE_WORDS} words", total <= MAX_PAGE_WORDS,
          f"{total} words, about {minutes:.1f} minutes at {WPM} a minute"
          f"{'' if total <= MAX_PAGE_WORDS else f'. Over by {total - MAX_PAGE_WORDS}'}")

    # The line under a must-solve is set in caption type. An essay in caption type
    # puts the evidence a CFO wants in the smallest text on the page.
    long_support = []
    for i, m in enumerate(musts, 1):
        for cap in re.findall(r'class="caption"[^>]*>(.*?)</p>', m, re.S):
            n = count_words(text_of(cap).replace("\u2028", " "))
            if n > MAX_SUPPORT_WORDS:
                long_support.append(f"{i}: {n}w")
    r.add(f"Supporting line stays a caption, {MAX_SUPPORT_WORDS} words",
          not long_support, ", ".join(long_support) if long_support else "all within")


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
    for sid, label in [("cut", "What it threw away"), ("unsure", "Where it is unsure")]:
        body = section(doc, sid)
        content = text_of(re.sub(r'<span class="kicker">.*?</span>|<th\b.*?</th>', " ",
                                 body, flags=re.S | re.I))
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
        mark = "✅ pass" if c["ok"] else ("❌ fail" if c["hard"] else "⚠️ watch")
        out.append(f"| {c['check']} | {mark} | {c['detail']} |")
    out.append("")
    hard, warn = len(r.failed_hard), len(r.warned)
    if hard:
        out.append(f"**{hard} hard check(s) failed.** The artifact does not ship until these pass.")
    elif warn:
        out.append(f"All hard checks pass. {warn} thing(s) to look at.")
    else:
        out.append("All checks pass.")
    out.append("")
    out.append("Checked: " + ", ".join(files))
    return "\n".join(out)


def main() -> int:
    global MAX_PAGE_WORDS

    ap = argparse.ArgumentParser(description="Verify a rendered Simply Strategy artifact.")
    ap.add_argument("target", help="a run directory, or the artifact html itself")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--material", help="material folder, to check that pointers name real files")
    ap.add_argument("--max-words", type=int, default=MAX_PAGE_WORDS,
                    help=f"word budget for the page (default {MAX_PAGE_WORDS})")
    a = ap.parse_args()
    MAX_PAGE_WORDS = a.max_words

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
    check_artifact(artifact, r)
    if a.material:
        check_pointers(artifact, a.material, r)
    if os.path.exists(reasoning):
        check_reasoning(reasoning, r)
        files.append(reasoning)
    else:
        r.add("reasoning.html exists", False, "a run without a reasoning log is not finished")

    if a.json:
        print(json.dumps({"checks": r.checks,
                          "failed": len(r.failed_hard),
                          "warned": len(r.warned)}, indent=2))
    else:
        print(render(r, files))
    return 1 if r.failed_hard else 0


if __name__ == "__main__":
    sys.exit(main())
