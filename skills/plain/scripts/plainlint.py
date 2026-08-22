#!/usr/bin/env python3
"""plainlint - count the mechanical markers of vague text.

Works on English and Dutch input. Returns a score in weighted findings per 100
words. Lower is better. Under 1.5 is clean, over 8 is a lot of noise.

De linter is bewust dom. Hij telt patronen die je kunt aanwijzen en vervangen.
Daar zit ook de winst: je hebt een systeem waar de tekst langs kan, in plaats
than a list of banned words.

Gebruik:
    python3 plainlint.py tekst.md
    python3 plainlint.py tekst.md --mode strict
    python3 plainlint.py README.md docs/*.md --lang en
    echo "je tekst" | python3 plainlint.py -
    python3 plainlint.py tekst.md --fail-over 2.0     # exit 1 bij een hogere score

The linter judges form, not content. An empty paragraph that scores zero is still
steeds leeg.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field

# ------------------------------------------------------------------- word lists

MARKETING = {
    "en": [
        "seamless", "seamlessly", "frictionless", "powerful", "cutting-edge",
        "cutting edge", "next-generation", "next generation", "state-of-the-art",
        "game-changing", "game changer", "revolutionary", "disruptive",
        "robust", "battle-tested", "best-in-class", "world-class",
        "industry-leading", "effortless", "effortlessly", "blazing fast",
        "lightning fast", "blazingly", "intuitive", "user-friendly",
        "delightful", "elegant solution", "unlock", "supercharge", "empower",
        "leverage", "harness the power", "holistic", "turnkey", "end-to-end",
        "comprehensive suite", "unparalleled", "unmatched", "seamless integration",
    ],
}

OFFICE_VERBS = {
    "en": [
        "reach out", "reached out", "dive into", "deep dive", "diving into",
        "spin up", "spun up", "kick off", "kicked off", "circle back",
        "touch base", "drill down", "unpack", "tee up", "roll out",
        "take a look at", "go ahead and", "leverage", "utilize", "ideate",
        "operationalize", "socialize the", "align on", "double down",
        "move the needle", "low-hanging fruit", "at the end of the day",
        "when it comes to",
    ],
}

HEDGES = {
    "en": [
        "it is important to note", "it's important to note", "it should be noted",
        "it is worth noting", "it's worth mentioning", "may potentially",
        "could potentially", "might possibly", "generally speaking",
        "in many cases", "tends to", "to some extent", "in a sense",
        "arguably", "more or less", "one could argue", "it is often the case",
    ],
}

FILLER = {
    "en": [
        "in this section", "as mentioned earlier", "in today's fast-paced",
        "let's dive into", "there are a number of factors", "in conclusion",
        "as we all know", "in the world of", "when it comes down to it",
    ],
}

NOMINALIZATION = {
    "en": [
        r"\b(?:perform|conduct|carry\s+out|undertake|provide|make|do|give)\s+(?:a|an|the)?\s*\w+(?:tion|sion|ment|ance|ence|sis|ing)\b",
        r"\bhas\s+the\s+ability\s+to\b",
        r"\bis\s+responsible\s+for\s+the\s+\w+ing\b",
        r"\bgive\s+consideration\s+to\b",
        r"\bin\s+the\s+event\s+that\b",
    ],
}

PASSIVE = {
    "en": [
        r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(?:\w+ed|written|done|made|taken|given|shown|known|found|built|held|kept|sent|set|put|chosen|driven)\b(?!\s+(?:to|by\s+you))",
        r"\bit\s+(?:was|is|has\s+been)\s+(?:decided|determined|found|observed|noted)\b",
    ],
}

PARALLELISM = {
    "en": [
        r"\bit'?s\s+not\s+(?:just\s+)?\w+[,;]\s*it'?s\b",
        r"\bnot\s+only\b[^.!?]{0,60}\bbut\s+also\b",
        r"\bthis\s+isn'?t\s+(?:just\s+)?\w+[,;]\s*(?:it'?s|this\s+is)\b",
    ],
}

SYNONYM_CLUSTERS = {
    "en": [
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
    ],
}

FORMAL = {
    "en": ["utilize", "commence", "terminate", "prior to", "subsequent to",
           "pursuant to", "ascertain", "endeavor", "in order to",
           "at this point in time", "aforementioned"],
}

EN_STOPWORDS = {"the", "and", "of", "to", "is", "in", "that", "for", "with",
                "not", "you", "are", "it", "on", "as", "this", "be", "at", "or"}

# ---------------------------------------------------------------- datastructuren


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
    "synoniemenrotatie": 0.5,
}


@dataclass
class Finding:
    rule: str
    detail: str
    line: int
    excerpt: str

    @property
    def weight(self) -> float:
        return WEIGHTS.get(self.rule, 1.0)


@dataclass
class Report:
    name: str
    words: int = 0
    sentences: int = 0
    findings: list[Finding] = field(default_factory=list)
    lang: str = "nl"

    def add(self, finding: Finding) -> None:
        """Add a finding, but never the same one twice in the same place.

        Meerdere patronen kunnen op hetzelfde stuk tekst aanslaan. Dubbel tellen
        maakt de score onbetrouwbaar.
        """
        key = (finding.rule, finding.line, finding.excerpt.strip().lower())
        if key in self._seen:
            return
        self._seen.add(key)
        self.findings.append(finding)

    _seen: set = field(default_factory=set, repr=False)

    @property
    def weighted(self) -> float:
        return sum(f.weight for f in self.findings)

    @property
    def score(self) -> float:
        if not self.words:
            return 0.0
        return self.weighted * 100 / self.words

    @property
    def avg_sentence(self) -> float:
        return self.words / self.sentences if self.sentences else 0.0


# ---------------------------------------------------------------- hulpfuncties

FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---[ \t]*\r?\n", re.S)
IGNORE_BLOCK = re.compile(
    r"<!--\s*plainlint-ignore-start\s*-->.*?<!--\s*plainlint-ignore-end\s*-->", re.S)
CODE_BLOCK = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`]+`")
URL = re.compile(r"https?://\S+")
MD_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
MD_HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Þ\"'(\[])")
ABBREV = re.compile(r"\b(bijv|bijz|resp|enz|etc|nr|z\.o\.z|i\.v\.m|d\.w\.z|"
                    r"o\.a|m\.b\.t|t\.o\.v|a\.u\.b|e\.g|i\.e|vs|approx|fig)\.$",
                    re.I)


def blank_out(match: re.Match) -> str:
    """Replace a block with as many blank lines, so line numbers stay correct."""
    return "\n" * match.group(0).count("\n")


def strip_noise(text: str) -> str:
    """Haal frontmatter, code, links en genegeerde blokken weg.

    Die tellen niet mee als proza. Regelnummers blijven kloppen doordat
    removed blocks are replaced by the same number of blank lines.

    If a text discusses the very words this linter flags, wrap that part in
    stuk dan tussen `<!-- plainlint-ignore-start -->` en
    `<!-- plainlint-ignore-end -->`. The linter cannot tell mention from use.
    onderscheiden.
    """
    text = FRONTMATTER.sub(blank_out, text)
    text = IGNORE_BLOCK.sub(blank_out, text)
    text = CODE_BLOCK.sub(blank_out, text)
    text = INLINE_CODE.sub(" CODE ", text)
    text = URL.sub(" URL ", text)
    return text


def prose_lines(text: str) -> list[tuple[int, str]]:
    """Return numbered lines, without headings and table rows."""
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        if MD_TABLE_ROW.match(line) or MD_HEADING.match(line):
            continue
        out.append((i, line))
    return out


def split_sentences(block: str) -> list[str]:
    parts = SENTENCE_SPLIT.split(block)
    merged: list[str] = []
    for part in parts:
        if merged and ABBREV.search(merged[-1]):
            merged[-1] = merged[-1] + " " + part
        else:
            merged.append(part)
    return [p.strip() for p in merged if p.strip()]


def count_words(sentence: str) -> int:
    """Count words the way ASD-STE100 does (rules 8.5 to 8.7).

    Tekst tussen haakjes telt als een woord. Getallen met eenheid, afkortingen
    and hyphenated words each count as one word.
    """
    s = re.sub(r"\([^)]*\)", " X ", sentence)
    s = re.sub(r"\b(\d[\d.,]*)\s*([A-Za-z°%]{1,4})\b", r"\1\2", s)
    tokens = re.findall(r"[A-Za-zÀ-ÿ0-9][\wÀ-ÿ'’\-/°%]*", s)
    return len(tokens)


def detect_lang(text: str) -> str:
    """English only. The pipeline writes English, so there is nothing to detect."""
    return "en"


def excerpt(text: str, span: tuple[int, int], width: int = 60) -> str:
    start = max(0, span[0] - 15)
    end = min(len(text), span[1] + 25)
    frag = " ".join(text[start:end].split())
    return (("…" if start else "") + frag + ("…" if end < len(text) else ""))[:width + 10]


# ---------------------------------------------------------------- controles


def scan_phrases(report: Report, lines, table, rule: str, label: str) -> None:
    terms = table.get(report.lang, [])
    if not terms:
        return
    pattern = re.compile(
        r"(?<!\w)(" + "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True)) + r")(?!\w)",
        re.I,
    )
    for lineno, line in lines:
        for m in pattern.finditer(line):
            report.add(
                Finding(rule, f"{label}: “{m.group(1)}”", lineno, excerpt(line, m.span()))
            )


def scan_regexes(report: Report, lines, table, rule: str, label: str) -> None:
    pats = [re.compile(p, re.I) for p in table.get(report.lang, [])]
    for lineno, line in lines:
        for pat in pats:
            for m in pat.finditer(line):
                report.add(
                    Finding(rule, f"{label}: “{' '.join(m.group(0).split())}”",
                            lineno, excerpt(line, m.span()))
                )


def scan_punctuation(report: Report, lines, mode: str) -> None:
    for lineno, line in lines:
        for m in re.finditer(r";", line):
            report.add(
                Finding("semicolon", "a semicolon splits what should have been two sentences",
                        lineno, excerpt(line, m.span()))
            )
        for m in re.finditer(r"—|(?<=\w) - (?=\w)", line):
            # A dash after a short label ("**Status — ...**") is formatting,
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

    def flush(end_line: int) -> None:
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
            flush(lineno)
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
    flush(0)


def _inflections(word: str) -> set[str]:
    """Inflected forms that are still the same word.

    Ruim genoeg om meervoud en vervoeging te vangen, krap genoeg om
    'clear' niet op 'clearly' te laten aanslaan.
    """
    base = word[:-2] if word.endswith("en") and len(word) > 4 else word
    return {word, base, base + "s", base + "en", base + "t", base + "e",
            base + "ed", base + "es", base + "ing", base + "d"}


def scan_synonyms(report: Report, text: str) -> None:
    """Report clusters with two or more members in the same paragraph.

    Eén melding per cluster per document. Wie hetzelfde ding drie namen geeft
    doet dat overal, en dan is één melding genoeg om het op te lossen.
    """
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    reported: set[int] = set()
    lineno = 1
    for para in paragraphs:
        start = lineno
        lineno += para.count("\n") + 2
        words = set(re.findall(r"[a-zà-ÿ]+", para.lower()))
        if len(re.findall(r"[a-zà-ÿ0-9]+", para)) < 25:
            continue  # te kort om iets zinnigs over rotatie te zeggen
        for idx, cluster in enumerate(SYNONYM_CLUSTERS.get(report.lang, [])):
            if idx in reported:
                continue
            used = [w for w in cluster if _inflections(w) & words]
            if len(used) > 1:
                reported.add(idx)
                report.add(
                    Finding("synoniemenrotatie",
                            "zelfde ding, meerdere namen: " + ", ".join(used),
                            start, "")
                )


def analyze(name: str, text: str, lang: str, mode: str, max_sentence: int = 0) -> Report:
    clean = strip_noise(text)
    report = Report(name=name, lang=lang if lang != "auto" else detect_lang(clean))
    lines = prose_lines(clean)

    scan_sentences(report, lines, mode, max_sentence)
    scan_punctuation(report, lines, mode)
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


# ---------------------------------------------------------------- uitvoer


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
    out.append("| File | Lang | Words | Avg sentence | Findings | Score /100w | Verdict |")
    out.append("| --- | --- | --- | --- | --- | --- | --- |")
    for r in reports:
        out.append(
            f"| {r.name} | {r.lang} | {r.words} | {r.avg_sentence:.1f} | "
            f"{len(r.findings)} | {r.score:.2f} | {verdict(r.score)} |"
        )
    out.append("")
    out.append("Score = weighted findings per 100 words. Clean < 1.5 · good < 3.0 · "
               "could be tighter < 5.0 · woolly < 8.0 · above that a lot of noise.")
    out.append("Soft patterns (passive, formal word, em dash, synonym rotation) "
               "count half, because they are sometimes the right call.\n")

    for r in reports:
        if not r.findings:
            out.append(f"### {r.name}\n\nNiets gevonden.\n")
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
            out.append(f"| {f.line} | {f.rule} — {detail} | {ex} |")
        if len(r.findings) > show:
            out.append(f"| … | {len(r.findings) - show} more | use `--show 0` for all |")
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Count the mechanical markers of vague text.")
    ap.add_argument("files", nargs="+", help="files, or - for stdin")
    ap.add_argument("--lang", choices=["auto", "en"], default="auto")
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
            reports.append(analyze("stdin", sys.stdin.read(), args.lang, args.mode, args.max_sentence))
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                reports.append(analyze(path, fh.read(), args.lang, args.mode, args.max_sentence))
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
