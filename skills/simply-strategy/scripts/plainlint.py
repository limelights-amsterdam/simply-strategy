#!/usr/bin/env python3
"""plainlint - count the mechanical markers of vague text.

English text. Returns a score in weighted findings per 100 words. Lower is
better. Under 1.5 is clean, over 8 is a lot of noise.

The linter is deliberately dumb. It counts patterns you can point at and replace.
That is where the gain is: something the text can pass through, rather than a
list of banned words.

Usage:
    python3 plainlint.py text.md
    python3 plainlint.py text.md --mode strict
    python3 plainlint.py text.md --max-sentence 15     # the L1 limit
    python3 plainlint.py README.md docs/*.md
    echo "your text" | python3 plainlint.py -
    python3 plainlint.py text.md --fail-over 2.0       # exit 1 above that score

The linter judges form, not content. An empty paragraph that scores zero is
still empty.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

# The primitives live next to this file, in the same scripts/ folder.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from textlib import (  # noqa: E402
    Finding, Report as BaseReport, count_words, excerpt, scan_phrases, scan_regexes,
    split_sentences, strip_noise,
)

# ------------------------------------------------------------------- word lists

MARKETING = [
        "seamless", "seamlessly", "frictionless", "powerful", "cutting-edge",
        "cutting edge", "next-generation", "next generation", "state-of-the-art",
        "game-changing", "game changer", "revolutionary", "disruptive",
        "robust", "battle-tested", "best-in-class", "world-class",
        "industry-leading", "effortless", "effortlessly", "blazing fast",
        "lightning fast", "blazingly", "intuitive", "user-friendly",
        "delightful", "elegant solution", "unlock", "supercharge", "empower",
        "leverage", "harness the power", "holistic", "turnkey", "end-to-end",
        "comprehensive suite", "unparalleled", "unmatched", "seamless integration",
]

OFFICE_VERBS = [
        "reach out", "reached out", "dive into", "deep dive", "diving into",
        "spin up", "spun up", "kick off", "kicked off", "circle back",
        "touch base", "drill down", "unpack", "tee up", "roll out",
        "take a look at", "go ahead and", "leverage", "utilize", "ideate",
        "operationalize", "socialize the", "align on", "double down",
        "move the needle", "low-hanging fruit", "at the end of the day",
        "when it comes to",
]

HEDGES = [
        "it is important to note", "it's important to note", "it should be noted",
        "it is worth noting", "it's worth mentioning", "may potentially",
        "could potentially", "might possibly", "generally speaking",
        "in many cases", "tends to", "to some extent", "in a sense",
        "arguably", "more or less", "one could argue", "it is often the case",
]

FILLER = [
        "in this section", "as mentioned earlier", "in today's fast-paced",
        "let's dive into", "there are a number of factors", "in conclusion",
        "as we all know", "in the world of", "when it comes down to it",
]

NOMINALIZATION = [
        r"\b(?:perform|conduct|carry\s+out|undertake|provide|make|do|give)\s+(?:a|an|the)?\s*\w+(?:tion|sion|ment|ance|ence|sis|ing)\b",
        r"\bhas\s+the\s+ability\s+to\b",
        r"\bis\s+responsible\s+for\s+the\s+\w+ing\b",
        r"\bgive\s+consideration\s+to\b",
        r"\bin\s+the\s+event\s+that\b",
]

PASSIVE = [
        r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(?:\w+ed|written|done|made|taken|given|shown|known|found|built|held|kept|sent|set|put|chosen|driven)\b(?!\s+(?:to|by\s+you))",
        r"\bit\s+(?:was|is|has\s+been)\s+(?:decided|determined|found|observed|noted)\b",
]

PARALLELISM = [
        r"\bit'?s\s+not\s+(?:just\s+)?\w+[,;]\s*it'?s\b",
        r"\bnot\s+only\b[^.!?]{0,60}\bbut\s+also\b",
        r"\bthis\s+isn'?t\s+(?:just\s+)?\w+[,;]\s*(?:it'?s|this\s+is)\b",
]

SYNONYM_CLUSTERS = [
        ["user", "customer", "client", "visitor"],
        ["application", "tool", "platform", "solution", "system"],
        ["issue", "problem", "bug", "defect", "fault"],
        ["way", "approach", "method", "technique"],
        ["start", "begin", "commence", "initiate"],
        ["remove", "delete", "erase", "clear"],
        ["change", "modify", "update", "alter"],
        ["show", "display", "present", "render"],
        ["create", "build", "generate", "produce"],
        ["check", "verify", "validate", "confirm"],
]

FORMAL = ["utilize", "commence", "terminate", "prior to", "subsequent to",
           "pursuant to", "ascertain", "endeavor", "in order to",
           "at this point in time", "aforementioned"]

# ------------------------------------------------------------------- report


# Not every finding weighs the same. A semicolon or a marketing word is
# always wrong. Passive, a formal word or an em dash is sometimes the right
# call, so those count half.
WEIGHTS = {
    "long sentence": 1.0,
    "long paragraph": 1.0,
    "semicolon": 1.0,
    "marketing word": 1.0,
    "office speak": 1.0,
    "hedge": 1.0,
    "filler": 1.0,
    "frozen verb": 1.0,
    "inversion": 1.0,
    "em dash": 0.5,
    "formal word": 0.5,
    "passive": 0.5,
    "synonym rotation": 0.5,
}


@dataclass
class Report(BaseReport):
    """Adds the sentence count, because this linter reports an average length."""
    sentences: int = 0

    @property
    def avg_sentence(self) -> float:
        return self.words / self.sentences if self.sentences else 0.0


# ------------------------------------------------------------------ helpers

MD_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
MD_HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
def prose_lines(text: str) -> list[tuple[int, str]]:
    """Return numbered lines, without headings and table rows."""
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        if MD_TABLE_ROW.match(line) or MD_HEADING.match(line):
            continue
        out.append((i, line))
    return out


def scan_punctuation(report: Report, lines) -> None:
    for lineno, line in lines:
        for m in re.finditer(r";", line):
            report.add(
                Finding("semicolon", "a semicolon splits what should have been two sentences",
                        lineno, excerpt(line, m.span()))
            )
        for m in re.finditer(r"—|(?<=\w) - (?=\w)", line):
            # A dash after a short label ("**Status**" then a dash) is formatting,
            # not a run-on thought. Only from five words before does it
            # really become two sentences fused into one.
            if len(re.findall(r"\w+", line[:m.start()])) < 5:
                continue
            report.add(
                Finding("em dash", "an em dash glues two ideas together",
                        lineno, excerpt(line, m.span()))
            )


def scan_sentences(report: Report, lines, mode: str, max_sentence: int = 0) -> None:
    cap = max_sentence if max_sentence else (20 if mode == "strict" else 25)
    para: list[str] = []
    para_start = 1

    def flush() -> None:
        if not para:
            return
        block = " ".join(para)
        sents = split_sentences(block)
        report.sentences += len(sents)
        report.words += sum(count_words(s) for s in sents)
        for s in sents:
            n = count_words(s)
            if n > cap:
                report.add(
                    Finding("long sentence", f"{n} words (limit {cap})", para_start,
                            " ".join(s.split())[:70] + "…")
                )
        if len(sents) > 6:
            report.add(
                Finding("long paragraph", f"{len(sents)} sentences (limit 6)", para_start, "")
            )
        para.clear()

    for lineno, line in lines:
        if not line.strip() or line.lstrip().startswith(("- ", "* ", ">")) or re.match(r"^\s*\d+\.\s", line):
            flush()
            # list items count toward words, not toward paragraph length
            if line.strip():
                text = re.sub(r"^\s*(?:[-*>]|\d+\.)\s*", "", line)
                for s in split_sentences(text):
                    n = count_words(s)
                    report.sentences += 1
                    report.words += n
                    if n > cap:
                        report.add(
                            Finding("long sentence", f"{n} words (limit {cap})", lineno,
                                    " ".join(s.split())[:70] + "…")
                        )
            continue
        if not para:
            para_start = lineno
        para.append(line.strip())
    flush()


def _inflections(word: str) -> set[str]:
    """Inflected forms that are still the same word.

    Wide enough to catch plurals and conjugations, narrow enough that 'clear'
    does not fire on 'clearly'.
    """
    base = word[:-2] if word.endswith("en") and len(word) > 4 else word
    return {word, base, base + "s", base + "en", base + "t", base + "e",
            base + "ed", base + "es", base + "ing", base + "d"}


def scan_synonyms(report: Report, text: str) -> None:
    """Report clusters with two or more members in the same paragraph.

    One finding per cluster per document. Giving one thing three names
    does it throughout, so one finding is enough to fix it.
    """
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    reported: set[int] = set()
    lineno = 1
    for para in paragraphs:
        start = lineno
        lineno += para.count("\n") + 2
        words = set(re.findall(r"[a-zà-ÿ]+", para.lower()))
        if len(re.findall(r"[a-zà-ÿ0-9]+", para)) < 25:
            continue  # too short to say anything meaningful about rotation
        for idx, cluster in enumerate(SYNONYM_CLUSTERS):
            if idx in reported:
                continue
            used = [w for w in cluster if _inflections(w) & words]
            if len(used) > 1:
                reported.add(idx)
                report.add(
                    Finding("synonym rotation",
                            "same thing, several names: " + ", ".join(used),
                            start, "")
                )


def analyze(name: str, text: str, mode: str, max_sentence: int = 0) -> Report:
    clean = strip_noise(text)
    report = Report(name=name, weights=WEIGHTS)
    lines = prose_lines(clean)

    scan_sentences(report, lines, mode, max_sentence)
    scan_punctuation(report, lines)
    scan_phrases(report, lines, MARKETING, "marketing word", "claims quality without evidence")
    scan_phrases(report, lines, OFFICE_VERBS, "office speak", "points at no action")
    scan_phrases(report, lines, HEDGES, "hedge", "vague uncertainty")
    scan_phrases(report, lines, FILLER, "filler", "says nothing")
    scan_phrases(report, lines, FORMAL, "formal word", "an ordinary alternative exists")
    scan_regexes(report, lines, NOMINALIZATION, "frozen verb", "the action sits in the noun")
    scan_regexes(report, lines, PASSIVE, "passive", "the actor is invisible")
    scan_regexes(report, lines, PARALLELISM, "inversion", "rhetorical contrast")
    scan_synonyms(report, clean)
    return report


# ------------------------------------------------------------------- output


BANDS = [
    (1.5, "✅ clean"),
    (3.0, "✅ good"),
    (5.0, "⚠️ could be tighter"),
    (8.0, "⚠️ woolly"),
]


def verdict(score: float) -> str:
    for limit, label in BANDS:
        if score < limit:
            return label
    return "❌ a lot of noise"


def render(reports: list[Report], show: int) -> str:
    out: list[str] = []
    out.append("## Plainlint\n")
    out.append("| File | Prose words | Avg sentence | Findings | Score /100pw | Verdict |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for r in reports:
        out.append(
            f"| {r.name} | {r.words} | {r.avg_sentence:.1f} | "
            f"{len(r.findings)} | {r.score:.2f} | {verdict(r.score)} |"
        )
    out.append("")
    out.append("Score = weighted findings per 100 words of prose. Clean < 1.5 · good < 3.0 · "
               "could be tighter < 5.0 · woolly < 8.0 · above that a lot of noise.")
    out.append("Soft patterns (passive, formal word, em dash, synonym rotation) "
               "count half, because they are sometimes the right call.\n")
    out.append("Prose words is what this linter reads: paragraphs and list items. Headings, tables "
               "and code are not scanned, so they are not in the denominator either. Stratlint "
               "counts the whole document, so the two scores are not comparable.\n")

    for r in reports:
        if not r.findings:
            out.append(f"### {r.name}\n\nNothing found.\n")
            continue
        counts = Counter(f.rule for f in r.findings)
        out.append(f"### {r.name}\n")
        out.append("| Pattern | Count |")
        out.append("| --- | --- |")
        for rule, n in counts.most_common():
            out.append(f"| {rule} | {n} |")
        out.append("")
        out.append("| Line | Pattern | What it says |")
        out.append("| --- | --- | --- |")
        for f in r.findings[:show]:
            detail = f.detail.replace("|", "\\|")
            ex = (f.excerpt or "").replace("|", "\\|")
            out.append(f"| {f.line} | {f.rule}: {detail} | {ex} |")
        if len(r.findings) > show:
            out.append(f"| … | {len(r.findings) - show} more | use `--show 0` for all |")
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Count the mechanical markers of vague text.")
    ap.add_argument("files", nargs="+", help="files, or - for stdin")
    ap.add_argument("--mode", choices=["normal", "strict"], default="normal",
                    help="strict uses 20 words per sentence instead of 25")
    ap.add_argument("--max-sentence", type=int, default=0, metavar="N",
                    help="hard word limit per sentence, overrides the mode. "
                         "Use 15 for child-level text")
    ap.add_argument("--show", type=int, default=25,
                    help="findings shown per file (0 = all)")
    ap.add_argument("--fail-over", type=float, default=None,
                    help="exit code 1 when the score goes above this")
    args = ap.parse_args()

    reports: list[Report] = []
    for path in args.files:
        if path == "-":
            reports.append(analyze("stdin", sys.stdin.read(), args.mode, args.max_sentence))
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                reports.append(analyze(path, fh.read(), args.mode, args.max_sentence))
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2

    show = 10**9 if args.show == 0 else args.show
    print(render(reports, show))

    if args.fail_over is not None:
        worst = max((r.score for r in reports), default=0.0)
        if worst > args.fail_over:
            print(f"\nScore {worst:.2f} is above the limit {args.fail_over:.2f}.",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
