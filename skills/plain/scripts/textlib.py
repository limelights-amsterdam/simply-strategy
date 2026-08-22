"""textlib - the text primitives the linters and the artifact checker share.

Counting words and splitting sentences decide whether the product's central claim
is true, so they are defined once. Before this file there were four word counters
that disagreed: the same sentence measured 19 in plainlint and 21 in
check_artifact, because one merged a number with its unit per ASD-STE100 8.6 and
the other did not. A page could pass the markdown check and fail the rendered one.

This lives next to plainlint rather than in scripts/ so that skills/plain/ still
works when it is copied out on its own. Consumers reach it with a sys.path insert
relative to their own __file__.
"""

from __future__ import annotations

import re

INLINE_CODE = re.compile(r"`[^`]+`")

ABBREV = re.compile(r"\b(bijv|bijz|resp|enz|etc|nr|z\.o\.z|i\.v\.m|d\.w\.z|"
                    r"o\.a|m\.b\.t|t\.o\.v|a\.u\.b|e\.g|i\.e|vs|approx|fig)\.$",
                    re.I)

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Þ\"'(\[])")

FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---[ \t]*\r?\n", re.S)

CODE_BLOCK = re.compile(r"```.*?```", re.S)

IGNORE_BLOCK = re.compile(
    r"<!--\s*plainlint-ignore-start\s*-->.*?<!--\s*plainlint-ignore-end\s*-->", re.S)

URL = re.compile(r"https?://\S+")

def count_words(sentence: str) -> int:
    """Count words the way ASD-STE100 does (rules 8.5 to 8.7).

    Text in brackets counts as one word. So do a number with its unit, an
    abbreviation, and a hyphenated word.
    """
    s = re.sub(r"\([^)]*\)", " X ", sentence)
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

def excerpt(text: str, span: tuple[int, int], width: int = 60) -> str:
    start = max(0, span[0] - 15)
    end = min(len(text), span[1] + 25)
    frag = " ".join(text[start:end].split())
    return (("…" if start else "") + frag + ("…" if end < len(text) else ""))[:width + 10]


# ---------------------------------------------------------------- controles
