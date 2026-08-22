#!/usr/bin/env python3
"""stratlint - check whether a strategy document contains a decision.

Analyses English and Dutch, detected automatically. It does two things:

1. Per line: jargon that imitates a decision, claims that fail the opposite
   test, false sacrifices, vague owners and vague deadlines.
2. Per document: is there a sacrifice, a number, a date, an owner and a stop
   threshold anywhere. That places the piece as a strategy, a plan, a
   direction or a wish.

Usage:
    python3 stratlint.py strategy.md
    python3 stratlint.py strategy.md --lang nl
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

# ------------------------------------------------------------------ patterns

JARGON = {
    "nl": [
        "synergie", "synergieën", "integrale aanpak", "stip op de horizon",
        "handelingsperspectief", "randvoorwaardelijk", "kaderstellend",
        "toekomstbestendig", "strategische verankering", "ontzorgen",
        "olievlekwerking", "laaghangend fruit", "quick wins", "in de keten",
        "opschalen", "borgen", "draagvlak creëren", "draagvlak",
        "meerwaarde", "toegevoegde waarde", "klantreis", "datagedreven",
        "innovatiekracht", "schaalbaar model", "next level",
        "stakeholders meenemen", "kritisch kijken naar", "heroverwegen",
        "de juiste dingen doen", "wendbaar", "ecosysteem", "transitie",
        "transformatie", "versnellen", "verbinden", "verankeren",
        "strategische prioriteit", "toekomstvisie", "koersvast",
        "proactief", "holistisch", "synergievoordelen", "ketenregie",
    ],
    "en": [
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
    ],
}

# Claims whose opposite nobody would defend.
EMPTY_CLAIM = {
    "nl": [
        r"\b(?:de|onze)\s+klant\s+staat\s+(?:altijd\s+)?centraal\b",
        r"\bwij?\s+(?:stellen|zetten)\s+(?:de\s+)?\w+\s+(?:centraal|voorop)\b",
        r"\bwij?\s+(?:zijn|blijven)\s+(?:een\s+)?(?:innovatief|innovatieve|betrouwbaar|betrouwbare|transparant|transparante|wendbaar|wendbare|toonaangevend|toonaangevende|ambitieus|ambitieuze|duurzaam|duurzame|klantgericht|klantgerichte)\b",
        r"\bwij?\s+(?:investeren|geloven)\s+in\s+(?:kwaliteit|onze\s+mensen|mensen|innovatie|de\s+toekomst)\b",
        r"\bwij?\s+streven\s+naar\s+(?:excellentie|kwaliteit|groei|het\s+beste|de\s+beste)\b",
        r"\bwij?\s+(?:versterken|verbeteren|vergroten|behouden)\s+(?:onze|de)\s+(?:positie|marktpositie)\b",
        r"\bwij?\s+(?:leveren|bieden)\s+(?:hoge\s+|de\s+beste\s+|topkwaliteit|kwaliteit)\b",
        r"\bwij?\s+luisteren\s+naar\s+(?:onze\s+)?klanten\b",
        r"\bwij?\s+blijven\s+(?:investeren|inzetten)\s+in\b",
        r"\bwij?\s+willen\s+(?:groeien|de\s+beste\s+zijn)\b",
        r"\boog\s+(?:hebben\s+)?voor\s+de\s+klant\b",
        r"\bwij?\s+werken\s+samen\s+(?:met|aan)\s+(?:onze\s+)?(?:partners|de\s+toekomst)\b",
    ],
    "en": [
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
    ],
}

FALSE_SACRIFICE = {
    "nl": [
        r"\b(?:wij?\s+)?zegg?en?\s+nee\s+tegen\s+wat\s+niet\s+past\b",
        r"\b(?:wij?\s+)?focus+en\s+(?:scherper|beter|meer)\b",
        r"\b(?:wij?\s+)?prioriteren\s+(?:beter|scherper|ruthless)\b",
        r"\b(?:wij?\s+)?(?:maken|durven)\s+(?:harde\s+)?keuzes?\b",
        r"\b(?:wij?\s+)?durven\s+te\s+kiezen\b",
        r"\b(?:wij?\s+)?doen\s+minder,?\s+maar\s+beter\b",
        r"\b(?:wij?\s+)?herijken\s+(?:de\s+)?portfolio\b",
        r"\b(?:wij?\s+)?snijden\s+in\s+de\s+kosten\b",
        r"\bscherpere?\s+keuzes\s+maken\b",
    ],
    "en": [
        r"\bwe\s+say\s+no\s+to\s+what\s+(?:doesn'?t|does\s+not)\s+fit\b",
        r"\bwe\s+focus\s+(?:more\s+)?(?:sharply|harder|better)\b",
        r"\bwe\s+prioriti[sz]e\s+(?:ruthlessly|better|harder)\b",
        r"\bwe\s+make\s+(?:hard|tough)\s+choices\b",
        r"\bwe\s+do\s+less,?\s+but\s+better\b",
        r"\bwe\s+rationali[sz]e\s+(?:the\s+)?portfolio\b",
    ],
}

VAGUE_OWNER = {
    "nl": [
        r"\b(?:het\s+team|de\s+organisatie|de\s+afdeling|betrokkenen|men|iedereen|wij\s+allen)\s+(?:gaat|gaan|zal|zullen|moet|moeten|pakt|pakken)\b",
        r"\bwordt\s+(?:opgepakt|belegd|uitgezet)\s+(?:door\s+(?:het\s+team|de\s+organisatie))?\b",
        r"\bwij?\s+gaan\s+(?:kijken|onderzoeken|verkennen)\s+(?:naar|of)\b",
        r"\bnader\s+te\s+bepalen\b",
    ],
    "en": [
        r"\b(?:the\s+team|the\s+organi[sz]ation|everyone|all\s+of\s+us|stakeholders)\s+(?:will|should|must|needs?\s+to)\b",
        r"\bto\s+be\s+(?:determined|confirmed|assigned)\b",
        r"\bwe\s+will\s+(?:look\s+into|explore|investigate)\b",
    ],
}

VAGUE_DEADLINE = {
    "nl": [
        "op termijn", "te zijner tijd", "zo snel mogelijk", "op korte termijn",
        "op middellange termijn", "op lange termijn", "in de toekomst",
        "binnenkort", "doorlopend", "structureel", "continu proces",
    ],
    "en": [
        "in due course", "in the near future", "as soon as possible", "asap",
        "over time", "on an ongoing basis", "continuously", "in the long run",
        "at a later stage",
    ],
}

# --------------------------------------------------- structure recognition

REAL_SACRIFICE = {
    "nl": [
        r"\bstopp?en?\s+(?:wij?\s+)?met\s+\w+",
        r"\bnemen\s+wij?\s+niet\s+(?:meer\s+)?aan\b",
        r"\bgeen\s+\w+(?:\s+\w+){0,3}\s+meer\b",
        r"\b(?:bouwen|doen|leveren|maken|verkopen)\s+wij?\s+niet\b",
        r"\b(?:sluiten|schrappen|beëindigen|afbouwen|stopzetten)\s+wij?\b",
        r"\bvalt?\s+(?:hierdoor\s+)?af\b",
        r"\bkrijgt\s+geen\s+(?:nieuwe\s+)?(?:investering|budget|onderhoud)\b",
        r"\bnemen\s+geen\s+opdrachten\b",
    ],
    "en": [
        r"\bwe\s+(?:will\s+)?stop\s+\w+",
        r"\bwe\s+(?:will\s+)?(?:close|shut\s+down|discontinue|sunset|wind\s+down)\b",
        r"\bwe\s+(?:do|will)\s+not\s+(?:build|sell|serve|support|take)\b",
        r"\bwe\s+decline\b",
        r"\bno\s+longer\s+(?:sell|support|serve|maintain)\b",
        r"\breceives?\s+no\s+(?:further\s+)?(?:investment|budget|funding)\b",
    ],
}

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
    r"\|\s*(?:eigenaar|owner|wie|verantwoordelijk|responsible|dri)\s*\|", re.I)
OWNER_INLINE = re.compile(
    r"\b[A-Z][a-zà-ÿ]{2,}\s+(?:levert|doet|maakt|belt|schrijft|bouwt|test|"
    r"analyseert|owns|delivers|ships|runs|leads)\b")

STOP_CRITERION = {
    "nl": [r"\b(?:onder|boven|beneden)\s+.{0,30}?\bstopp?en\b", r"\bstopgrens\b",
           r"\bdan\s+stopp?en\s+wij?\b", r"\bkill[-\s]?criteri",
           r"\bhalen\s+wij?\s+dat\s+niet\b", r"\btrekken\s+wij?\s+de\s+stekker\b",
           r"\bals\s+.{0,40}?\bstopp?en\s+wij?\b"],
    "en": [r"\bif\s+.{0,40}?\bwe\s+(?:stop|exit|pull)\b", r"\bkill\s+criteri",
           r"\bstop\s+threshold\b", r"\bbelow\s+.{0,30}?\bwe\s+(?:stop|exit)\b",
           r"\bwe\s+(?:stop|exit)\s+(?:if|when|below)\b"],
}

NL_STOPWORDS = {"de", "het", "een", "en", "van", "is", "dat", "niet", "voor",
                "op", "met", "zijn", "wij", "te", "aan", "die", "er", "ook"}
EN_STOPWORDS = {"the", "and", "of", "to", "is", "in", "that", "for", "with",
                "not", "we", "are", "it", "on", "as", "this", "be", "at"}

WEIGHTS = {
    "empty claim": 2.0,
    "false sacrifice": 2.0,
    "jargon": 1.0,
    "vague owner": 1.0,
    "vague deadline": 1.0,
}

# --------------------------------------------------------------- data model


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
    lang: str = "nl"
    words: int = 0
    findings: list[Finding] = field(default_factory=list)
    structure: dict = field(default_factory=dict)
    _seen: set = field(default_factory=set, repr=False)

    def add(self, finding: Finding) -> None:
        key = (finding.rule, finding.line, finding.excerpt.strip().lower())
        if key in self._seen:
            return
        self._seen.add(key)
        self.findings.append(finding)

    @property
    def score(self) -> float:
        if not self.words:
            return 0.0
        return sum(f.weight for f in self.findings) * 100 / self.words

    @property
    def verdict(self) -> str:
        """Place the document. See references/tests.md for the reasoning."""
        s = self.structure
        decided = s.get("sacrifice") and (s.get("number") or s.get("stop"))
        executable = s.get("owner") and s.get("date")
        if decided and executable:
            return "**Strategy** — a choice, with a sacrifice and a point of reckoning"
        if decided:
            return "**Strategy without execution** — the choice is there, the actions are not"
        if executable:
            return "**Plan** — actions with owners, but no choice underneath"
        if s.get("sacrifice") or s.get("number"):
            return "**Direction** — an ambition, not yet a decision"
        return "**Wish** — no sacrifice, no number, no owner"


# ------------------------------------------------------------------- helpers

FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---[ \t]*\r?\n", re.S)
IGNORE_BLOCK = re.compile(
    r"<!--\s*(?:plainlint|stratlint)-ignore-start\s*-->.*?"
    r"<!--\s*(?:plainlint|stratlint)-ignore-end\s*-->", re.S)
CODE_BLOCK = re.compile(r"```.*?```", re.S)
URL = re.compile(r"https?://\S+")


def blank_out(match: re.Match) -> str:
    return "\n" * match.group(0).count("\n")


def strip_noise(text: str) -> str:
    """Strip frontmatter, code, links and ignored blocks.

    Line numbers stay correct because removed blocks are replaced by the same
    number of blank lines. If a text discusses these very words, wrap that part
    in `<!-- stratlint-ignore-start -->` and `<!-- stratlint-ignore-end -->`.
    """
    text = FRONTMATTER.sub(blank_out, text)
    text = IGNORE_BLOCK.sub(blank_out, text)
    text = CODE_BLOCK.sub(blank_out, text)
    text = URL.sub(" URL ", text)
    return text


def detect_lang(text: str) -> str:
    words = re.findall(r"[a-zà-ÿ]+", text.lower())
    nl = sum(1 for w in words if w in NL_STOPWORDS)
    en = sum(1 for w in words if w in EN_STOPWORDS)
    return "en" if en > nl else "nl"


def excerpt(line: str, span: tuple[int, int], width: int = 62) -> str:
    start, end = max(0, span[0] - 12), min(len(line), span[1] + 22)
    frag = " ".join(line[start:end].split())
    return (("…" if start else "") + frag + ("…" if end < len(line) else ""))[:width]


def scan_phrases(report, lines, table, rule, label) -> None:
    terms = table.get(report.lang, [])
    if not terms:
        return
    pattern = re.compile(
        r"(?<!\w)(" + "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True))
        + r")(?!\w)", re.I)
    for lineno, line in lines:
        for m in pattern.finditer(line):
            report.add(Finding(rule, f"{label}: “{m.group(1)}”", lineno,
                               excerpt(line, m.span())))


def scan_regexes(report, lines, table, rule, label) -> None:
    for pat in (re.compile(p, re.I) for p in table.get(report.lang, [])):
        for lineno, line in lines:
            for m in pat.finditer(line):
                report.add(Finding(rule, f"{label}: “{' '.join(m.group(0).split())}”",
                                   lineno, excerpt(line, m.span())))


def check_structure(report: Report, text: str) -> None:
    """Five yes/no questions that decide what kind of document this is."""
    def any_match(patterns) -> bool:
        return any(re.search(p, text, re.I) for p in patterns)

    report.structure = {
        "sacrifice": any_match(REAL_SACRIFICE.get(report.lang, [])),
        "number": bool(TARGET_NUMBER.search(text)),
        "date": bool(DATE_PATTERN.search(text)),
        "owner": bool(OWNER_COLUMN.search(text) or OWNER_INLINE.search(text)),
        "stop": any_match(STOP_CRITERION.get(report.lang, [])),
    }


STRUCTURE_HELP = {
    "sacrifice": ("What we will not do",
                  "Name one concrete customer, market or product that falls away"),
    "number": ("A number to steer by", "Add a quantity with a value"),
    "date": ("A date", "A quarter is not a date, name the day"),
    "owner": ("A name per action", "“The team” is not an owner"),
    "stop": ("When we stop", "Below which number do we pull the plug"),
}


def analyze(name: str, raw: str, lang: str) -> Report:
    text = strip_noise(raw)
    report = Report(name=name, lang=lang if lang != "auto" else detect_lang(text))
    report.words = len(re.findall(r"[A-Za-zÀ-ÿ0-9][\wÀ-ÿ'’\-]*", text))
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
    out.append("| File | Lang | Words | Findings | Score /100w | Language |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for r in reports:
        out.append(f"| {r.name} | {r.lang} | {r.words} | {len(r.findings)} | "
                   f"{r.score:.2f} | {band(r.score)} |")
    out.append("")

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
            out.append(f"| {f.line} | {f.rule} — {f.detail.replace('|', chr(92) + '|')} "
                       f"| {f.excerpt.replace('|', chr(92) + '|')} |")
        if len(r.findings) > show:
            out.append(f"| … | {len(r.findings) - show} more | `--show 0` shows all |")
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Check whether a strategy document contains a decision (EN/NL).")
    ap.add_argument("files", nargs="+", help="files, or - for stdin")
    ap.add_argument("--lang", choices=["auto", "nl", "en"], default="auto")
    ap.add_argument("--show", type=int, default=25, help="findings per file (0 = all)")
    ap.add_argument("--fail-over", type=float, default=None,
                    help="exit code 1 when the score exceeds this")
    args = ap.parse_args()

    reports = []
    for path in args.files:
        if path == "-":
            reports.append(analyze("stdin", sys.stdin.read(), args.lang))
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                reports.append(analyze(path, fh.read(), args.lang))
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
