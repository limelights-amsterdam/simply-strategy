#!/usr/bin/env python3
"""stratlint - check whether a strategy document contains a decision.

English text. It does two things:

1. Per line: jargon that imitates a decision, claims that fail the opposite
   test, false sacrifices, vague owners and vague deadlines.
2. Per document: is there a sacrifice, a number, a date, an owner and a stop
   threshold anywhere. That places the piece as a strategy, a plan, a
   direction or a wish.

Usage:
    python3 stratlint.py strategy.md
    python3 stratlint.py docs/*.md --fail-over 3.0
    cat memo.md | python3 stratlint.py -

The linter sees that a choice was made, not whether it pointed the right way.
That judgement stays with the reader.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# Word counting, sentence splitting and noise stripping are shared with plainlint and
# check_artifact, so the three tools measure with one ruler. The module sits next to
# this file, so the path holds in a clone and installed alike.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from textlib import (  # noqa: E402
    Finding, Report as BaseReport, count_words, scan_phrases, scan_regexes, strip_noise,
)

# ------------------------------------------------------------------ patterns

JARGON = [
        "synergies", "synergy", "core competencies", "strategic alignment",
        "value creation", "holistic approach", "north star", "double down",
        "unlock value", "operating model", "transformation journey",
        "best-in-class", "world-class", "thought leadership",
        "paradigm shift", "at scale", "low-hanging fruit", "quick wins",
        "table stakes", "boil the ocean", "move the needle", "win-win",
        "going forward", "moving forward", "strategic priority",
        "customer-centric", "data-driven", "enable the business",
        "drive growth", "build capabilities", "flywheel", "step change",
        "best practice", "leverage our", "strategic imperative",
]

# Claims whose opposite nobody would defend.
EMPTY_CLAIM = [
        r"\bwe\s+(?:are|remain|will\s+be)\s+(?:innovative|customer-centric|transparent|agile|reliable|ambitious|data-driven|sustainable|people-first)\b",
        r"\bwe\s+put\s+(?:the\s+)?(?:customer|client|people)s?\s+(?:first|at\s+the\s+cent)\b",
        r"\bwe\s+(?:invest|believe)\s+in\s+(?:quality|our\s+people|people|innovation|the\s+future)\b",
        r"\bwe\s+strive\s+for\s+(?:excellence|quality|growth|the\s+best)\b",
        r"\bwe\s+(?:strengthen|improve|grow|maintain)\s+our\s+(?:market\s+)?position\b",
        r"\bwe\s+deliver\s+(?:high[- ]quality|the\s+best|quality|excellence)\b",
        r"\bwe\s+listen\s+to\s+(?:our\s+)?(?:customers|clients)\b",
        r"\bwe\s+(?:continue|will\s+continue)\s+to\s+invest\s+in\b",
        r"\bwe\s+(?:want|aim)\s+to\s+(?:grow|be\s+the\s+best|lead)\b",
        r"\bcommitted\s+to\s+(?:excellence|quality|our\s+customers)\b",
]

FALSE_SACRIFICE = [
        r"\bwe\s+say\s+no\s+to\s+what\s+(?:doesn'?t|does\s+not)\s+fit\b",
        r"\bwe\s+focus\s+(?:more\s+)?(?:sharply|harder|better)\b",
        r"\bwe\s+prioriti[sz]e\s+(?:ruthlessly|better|harder)\b",
        r"\bwe\s+make\s+(?:hard|tough)\s+choices\b",
        r"\bwe\s+do\s+less,?\s+but\s+better\b",
        r"\bwe\s+rationali[sz]e\s+(?:the\s+)?portfolio\b",
]

VAGUE_OWNER = [
        r"\b(?:the\s+team|the\s+organi[sz]ation|everyone|all\s+of\s+us|stakeholders)\s+(?:will|should|must|needs?\s+to)\b",
        r"\bto\s+be\s+(?:determined|confirmed|assigned)\b",
        r"\bwe\s+will\s+(?:look\s+into|explore|investigate)\b",
]

VAGUE_DEADLINE = [
        "in due course", "in the near future", "as soon as possible", "asap",
        "over time", "on an ongoing basis", "continuously", "in the long run",
        "at a later stage",
]

# --------------------------------------------------- structure recognition

REAL_SACRIFICE = [
        r"\bwe\s+(?:will\s+)?stop\s+\w+",
        r"\bwe\s+(?:will\s+)?(?:close|shut\s+down|discontinue|sunset|wind\s+down)\b",
        r"\bwe\s+(?:do|will)\s+not\s+(?:build|sell|serve|support|take)\b",
        r"\bwe\s+decline\b",
        r"\bno\s+longer\s+(?:sell|support|serve|maintain)\b",
        r"\breceives?\s+no\s+(?:further\s+)?(?:investment|budget|funding)\b",
]

TARGET_NUMBER = re.compile(
    r"(?:€\s?\d|[$£]\s?\d|\d[\d.,]*\s*(?:%|procent|percent|mln|miljoen|k\b|"
    r"miljard|bn|m\b|uur|uren|dagen|weken|maanden|days|weeks|months|hours))",
    re.I)

DATE_PATTERN = re.compile(
    r"\b(?:\d{1,2}\s+(?:jan|feb|mrt|maart|apr|mei|jun|jul|aug|sep|okt|oct|nov|dec)[a-z]*"
    r"(?:\s+20\d{2})?"
    r"|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s+20\d{2}"
    r"|\d{1,2}[-/]\d{1,2}[-/]20\d{2}"
    r"|\b1\s+(?:januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december)"
    r"|\bQ[1-4]\s*20\d{2}"
    r"|\bper\s+1\s+\w+)\b",
    re.I)

OWNER_COLUMN = re.compile(
    r"\|\s*(?:owner|responsible|accountable|dri)\s*\|", re.I)
OWNER_INLINE = re.compile(
    r"\b[A-Z][a-zà-ÿ]{2,}\s+(?:levert|doet|maakt|belt|schrijft|bouwt|test|"
    r"analyseert|owns|delivers|ships|runs|leads)\b")

STOP_CRITERION = [r"\bif\s+.{0,40}?\bwe\s+(?:stop|exit|pull)\b", r"\bkill\s+criteri",
                  r"\bstop\s+threshold\b", r"\bbelow\s+.{0,30}?\bwe\s+(?:stop|exit)\b",
                  r"\bwe\s+(?:stop|exit)\s+(?:if|when|below)\b"]

WEIGHTS = {
    "empty claim": 2.0,
    "false sacrifice": 2.0,
    "jargon": 1.0,
    "vague owner": 1.0,
    "vague deadline": 1.0,
}

# --------------------------------------------------------------- data model


@dataclass
class Report(BaseReport):
    """Adds the five structure answers, which decide the verdict."""
    structure: dict = field(default_factory=dict)

    @property
    def verdict(self) -> str:
        """Place the document. See references/tests.md for the reasoning."""
        s = self.structure
        decided = s.get("sacrifice") and (s.get("number") or s.get("stop"))
        executable = s.get("owner") and s.get("date")
        if decided and executable:
            return "**Strategy**: a choice, with a sacrifice and a point of reckoning"
        if decided:
            return "**Strategy without execution**: the choice is there, the actions are not"
        if executable:
            return "**Plan**: actions with owners, but no choice underneath"
        if s.get("sacrifice") or s.get("number"):
            return "**Direction**: an ambition, not yet a decision"
        return "**Wish**: no sacrifice, no number, no owner"


# ------------------------------------------------------------------- helpers

def check_structure(report: Report, text: str) -> None:
    """Five yes/no questions that decide what kind of document this is."""
    def any_match(patterns) -> bool:
        return any(re.search(p, text, re.I) for p in patterns)

    report.structure = {
        "sacrifice": any_match(REAL_SACRIFICE),
        "number": bool(TARGET_NUMBER.search(text)),
        "date": bool(DATE_PATTERN.search(text)),
        "owner": bool(OWNER_COLUMN.search(text) or OWNER_INLINE.search(text)),
        "stop": any_match(STOP_CRITERION),
    }


STRUCTURE_HELP = {
    "sacrifice": ("What we will not do",
                  "Name one concrete customer, market or product that falls away"),
    "number": ("A number to steer by", "Add a quantity with a value"),
    "date": ("A date", "A quarter is not a date, name the day"),
    "owner": ("A name per action", "“The team” is not an owner"),
    "stop": ("When we stop", "Below which number do we pull the plug"),
}


def analyze(name: str, raw: str) -> Report:
    text = strip_noise(raw)
    report = Report(name=name, weights=WEIGHTS)
    report.words = sum(count_words(line) for line in text.splitlines())
    lines = [(i, l) for i, l in enumerate(text.splitlines(), 1)
             if not re.match(r"^\s{0,3}#{1,6}\s", l)]

    scan_regexes(report, lines, EMPTY_CLAIM, "empty claim", "fails the opposite test")
    scan_regexes(report, lines, FALSE_SACRIFICE, "false sacrifice", "sounds like a choice")
    scan_regexes(report, lines, VAGUE_OWNER, "vague owner", "nobody is accountable")
    scan_phrases(report, lines, JARGON, "jargon", "imitates a decision")
    scan_phrases(report, lines, VAGUE_DEADLINE, "vague deadline", "no date")
    check_structure(report, text)
    return report


# --------------------------------------------------------------------- output

BANDS = [(1.0, "✅ clean"), (2.5, "✅ acceptable"), (5.0, "⚠️ heavy jargon")]


def band(score: float) -> str:
    for limit, label in BANDS:
        if score < limit:
            return label
    return "❌ mostly air"


def render(reports: list[Report], show: int) -> str:
    out = ["## Stratlint\n"]
    out.append("| File | Words | Findings | Score /100w | Band |")
    out.append("| --- | --- | --- | --- | --- |")
    for r in reports:
        out.append(f"| {r.name} | {r.words} | {len(r.findings)} | "
                   f"{r.score:.2f} | {band(r.score)} |")
    out.append("")
    out.append("Words is the whole document: headings, tables and pointers included, because jargon "
               "and false sacrifices live in tables. Plainlint counts prose only, so the two scores "
               "are not comparable. Clean here is under 1.0.\n")

    for r in reports:
        out.append(f"### {r.name}\n")
        out.append("**Is it in there?**\n")
        out.append("| What | Found | If not |")
        out.append("| --- | --- | --- |")
        for key, (label, hint) in STRUCTURE_HELP.items():
            found = r.structure.get(key)
            out.append(f"| {label} | {'✅' if found else '❌'} | {'' if found else hint} |")
        out.append("")
        out.append(f"**Verdict:** {r.verdict}\n")

        if not r.findings:
            out.append("No jargon or empty claims found.\n")
            continue
        counts = Counter(f.rule for f in r.findings)
        out.append("| Pattern | Count |")
        out.append("| --- | --- |")
        for rule, n in counts.most_common():
            out.append(f"| {rule} | {n} |")
        out.append("")
        out.append("| Line | Finding | Text |")
        out.append("| --- | --- | --- |")
        order = {"empty claim": 0, "false sacrifice": 1, "vague owner": 2,
                 "vague deadline": 3, "jargon": 4}
        for f in sorted(r.findings, key=lambda f: (order.get(f.rule, 9), f.line))[:show]:
            out.append(f"| {f.line} | {f.rule}: {f.detail.replace('|', chr(92) + '|')} "
                       f"| {f.excerpt.replace('|', chr(92) + '|')} |")
        if len(r.findings) > show:
            out.append(f"| … | {len(r.findings) - show} more | `--show 0` shows all |")
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Check whether a strategy document contains a decision.")
    ap.add_argument("files", nargs="+", help="files, or - for stdin")
    ap.add_argument("--show", type=int, default=25, help="findings per file (0 = all)")
    ap.add_argument("--fail-over", type=float, default=None,
                    help="exit code 1 when the score exceeds this")
    args = ap.parse_args()

    reports = []
    for path in args.files:
        if path == "-":
            reports.append(analyze("stdin", sys.stdin.read()))
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                reports.append(analyze(path, fh.read()))
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2

    print(render(reports, 10**9 if args.show == 0 else args.show))

    if args.fail_over is not None:
        worst = max((r.score for r in reports), default=0.0)
        if worst > args.fail_over:
            print(f"\nScore {worst:.2f} exceeds the limit {args.fail_over:.2f}.",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
