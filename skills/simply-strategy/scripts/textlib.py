"""textlib - the primitives the linters and the checkers share.

One word counter, one sentence splitter, one set of budgets, one set of shapes
(a figure, a pointer, a TO FILL marker), and the finding/report types both
linters build on. Defined once so that a sentence cannot pass the markdown check
and fail the rendered page, or the reverse.

It sits in the same scripts/ folder as every consumer, which reaches it with a
sys.path insert relative to its own __file__.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# ------------------------------------------------------------------ budgets
# The length budget is owned by references/flatten/output.md. These are
# the numbers from that file, and the only copy the scripts read.

L1_MAX_SENTENCE = 15     # words per sentence at flatten level L1
MAX_PAGE_WORDS = 1200    # the whole artifact
MAX_CAPTION_WORDS = 40   # the evidence line under a must-solve
WPM = 200                # reading speed the page budget assumes

# ------------------------------------------------------------------- shapes

# A figure worth tracing: a quantity, a percentage, a money amount, a year.
FIGURE = re.compile(r"\b\d[\d.,]*\s?(?:percent|%|m|k|bn|million|billion)?\b", re.I)

# The honest form of a missing figure. Group 1 is what is needed.
TOFILL = re.compile(r"\[TO FILL:([^\]]*)\]")

# A source pointer as the markdown writes it: [plan-2026.md p. 6] or [slide 6].
# The renderer writes the same thing in parentheses. Owned by house-rules.md.
POINTER = re.compile(r"[\[(][^\])]*?\b(?:slides?|pp?\.?|pages?)\s?\d+[^\])]*[\])]", re.I)

INLINE_CODE = re.compile(r"`[^`]+`")

ABBREV = re.compile(r"\b(bijv|bijz|resp|enz|etc|nr|z\.o\.z|i\.v\.m|d\.w\.z|"
                    r"o\.a|m\.b\.t|t\.o\.v|a\.u\.b|e\.g|i\.e|vs|approx|fig)\.$",
                    re.I)

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Þ\"'(\[])")

FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---[ \t]*\r?\n", re.S)

CODE_BLOCK = re.compile(r"```.*?```", re.S)

IGNORE_BLOCK = re.compile(
    # Either linter's markers. A file that discusses the words one of them flags
    # usually discusses the other's too, and two marker names meant two ways to
    # get it wrong.
    r"<!--\s*(?:plainlint|stratlint)-ignore-start\s*-->.*?"
    r"<!--\s*(?:plainlint|stratlint)-ignore-end\s*-->",
    re.S,
)
URL = re.compile(r"https?://\S+")

def count_words(sentence: str) -> int:
    """Count words the way ASD-STE100 does (rules 8.5 to 8.7).

    Text in brackets counts as one word. So do a number with its unit, an
    abbreviation, and a hyphenated word.
    """
    # A quoted span is one word, per 8.7. Otherwise a sentence carrying a direct
    # quote is penalised for the source's verbosity, and the one thing a flattener
    # must not do to fix that is paraphrase the quote.
    s = re.sub(r"[\"\u201c\u2018][^\"\u201c\u201d\u2018\u2019]{2,}[\"\u201d\u2019]", " Q ", sentence)
    # Round or square: a source pointer is written [file.md p. 6] in markdown and
    # (file.md p. 6) on the page, and has to weigh the same in both.
    s = re.sub(r"\([^)]*\)|\[[^\]]*\]", " X ", s)
    s = re.sub(r"\b(\d[\d.,]*)\s*([A-Za-z°%]{1,4})\b", r"\1\2", s)
    tokens = re.findall(r"[A-Za-zÀ-ÿ0-9][\wÀ-ÿ'’\-/°%]*", s)
    return len(tokens)

def split_sentences(block: str) -> list[str]:
    parts = SENTENCE_SPLIT.split(block)
    merged: list[str] = []
    for part in parts:
        if merged and ABBREV.search(merged[-1]):
            merged[-1] = merged[-1] + " " + part
        else:
            merged.append(part)
    return [p.strip() for p in merged if p.strip()]

def blank_out(match: re.Match) -> str:
    """Replace a block with as many blank lines, so line numbers stay correct."""
    return "\n" * match.group(0).count("\n")

def strip_noise(text: str) -> str:
    """Strip frontmatter, code, links and ignored blocks.

    None of it counts as prose. Line numbers stay correct because removed blocks
    are replaced by the same number of blank lines.

    If a text discusses the very words a linter flags, wrap that part between
    `<!-- plainlint-ignore-start -->` and `<!-- plainlint-ignore-end -->`. The
    linter cannot tell mention from use.
    """
    text = FRONTMATTER.sub(blank_out, text)
    text = IGNORE_BLOCK.sub(blank_out, text)
    text = CODE_BLOCK.sub(blank_out, text)
    text = INLINE_CODE.sub(" CODE ", text)
    text = URL.sub(" URL ", text)
    return text

def excerpt(text: str, span: tuple[int, int], width: int = 60) -> str:
    start = max(0, span[0] - 15)
    end = min(len(text), span[1] + 25)
    frag = " ".join(text[start:end].split())
    return (("…" if start else "") + frag + ("…" if end < len(text) else ""))[:width + 10]


# --------------------------------------------------------- findings, reports
# Both linters count findings per hundred words and never count the same one
# twice. They differ only in what they look for, so the accounting lives here.


@dataclass
class Finding:
    rule: str
    detail: str
    line: int
    excerpt: str
    weight: float = 1.0


@dataclass
class Report:
    name: str
    words: int = 0
    findings: list = field(default_factory=list)
    weights: dict = field(default_factory=dict, repr=False)
    _seen: set = field(default_factory=set, repr=False)

    def add(self, finding: Finding) -> None:
        """Add a finding, but never the same one twice in the same place.

        Several patterns can match the same piece of text. Counting it twice
        makes the score unreliable.
        """
        key = (finding.rule, finding.line, finding.excerpt.strip().lower())
        if key in self._seen:
            return
        self._seen.add(key)
        finding.weight = self.weights.get(finding.rule, 1.0)
        self.findings.append(finding)

    @property
    def weighted(self) -> float:
        return sum(f.weight for f in self.findings)

    @property
    def score(self) -> float:
        """Weighted findings per hundred words. Zero when there are no words."""
        return self.weighted * 100 / self.words if self.words else 0.0


def scan_phrases(report: Report, lines, terms, rule: str, label: str) -> None:
    """Flag every occurrence of a literal phrase, longest first, whole words only."""
    if not terms:
        return
    pattern = re.compile(
        r"(?<!\w)(" + "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True))
        + r")(?!\w)", re.I)
    for lineno, line in lines:
        for m in pattern.finditer(line):
            report.add(Finding(rule, f"{label}: \u201c{m.group(1)}\u201d", lineno,
                               excerpt(line, m.span())))


def scan_regexes(report: Report, lines, patterns, rule: str, label: str) -> None:
    """Flag every match of each regex, in line order."""
    pats = [re.compile(p, re.I) for p in patterns]
    for lineno, line in lines:
        for pat in pats:
            for m in pat.finditer(line):
                report.add(Finding(rule, f"{label}: \u201c{' '.join(m.group(0).split())}\u201d",
                                   lineno, excerpt(line, m.span())))
