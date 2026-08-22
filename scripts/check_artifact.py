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

NETWORK = re.compile(r"<img\b|<script\b|https?://|//cdn\.|@import|fonts\.googleapis", re.I)
UNFILLED = re.compile(r"\{\{[A-Z_]+\}\}")
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


def text_of(fragment: str) -> str:
    """Visible text: drop tags, comments, style and script blocks."""
    f = re.sub(r"<!--.*?-->", " ", fragment, flags=re.S)
    f = re.sub(r"<(style|script)\b.*?</\1>", " ", f, flags=re.S | re.I)
    f = re.sub(r"<[^>]+>", " ", f)
    return re.sub(r"\s+", " ", html.unescape(f)).strip()


def section(doc: str, sid: str) -> str:
    m = re.search(rf'<section[^>]*id="{re.escape(sid)}".*?</section>', doc, re.S | re.I)
    return m.group(0) if m else ""


def sentences(t: str):
    """Split on sentence enders. A source pointer in brackets is not a sentence."""
    t = POINTER.sub(" ", t)
    t = TOFILL.sub(" TOFILL ", t)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]


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

    empty = [SECTION_NAMES[s] for s in SECTIONS
             if section(doc, s) and len(text_of(re.sub(r'<span class="kicker">.*?</span>', " ",
                                                       section(doc, s), flags=re.S))) < 15]
    r.add("No section is silently empty", not empty, ", ".join(empty) if empty else "none")

    vague = [t.strip() for t in TOFILL.findall(doc) if len(t.strip()) < 4]
    r.add("Every TO FILL says what is needed", not vague,
          f"{len(vague)} bare marker(s)" if vague else f"{len(TOFILL.findall(doc))} marker(s), all described")

    body_only = re.sub(r"<(style|script)\b.*?</\1>", " ", doc, flags=re.S | re.I)
    dashes = EM_DASH.findall(text_of(body_only))
    r.add("No em dashes in the copy", not dashes, f"{len(dashes)} found" if dashes else "none")


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
    ap = argparse.ArgumentParser(description="Verify a rendered Simply Strategy artifact.")
    ap.add_argument("target", help="a run directory, or the artifact html itself")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
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
    check_artifact(artifact, r)
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
