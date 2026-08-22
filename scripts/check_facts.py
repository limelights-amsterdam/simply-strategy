#!/usr/bin/env python3
"""check_facts - every figure on the page has to exist in the material.

The deterministic half of "was a number invented": it does not judge whether a
claim is fair, it asks whether each figure can be found in the source at all. It
also counts the source pointers, because a page that reads well and cannot be
checked is the failure mode of writing alone.

    python3 scripts/check_facts.py runs/<slug>/<stamp>/04-plain.md --material material/<slug>/

What it does not flag, deliberately:

  - anything inside [TO FILL: ...], which is the honest form of a missing figure
  - a figure on a line that labels itself as the run's own arithmetic
  - section numbers, slide numbers and reference markers

Exit 1 when a figure cannot be found, or when the page carries fewer pointers
than --min-pointers per hundred words.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skills" / "plain" / "scripts"))
from textlib import FIGURE, POINTER, TOFILL, count_words, strip_noise  # noqa: E402

MIN_POINTERS = 2.0     # per hundred words, the gate step 5 sends the page back on

OWN_WORK = re.compile(
    r"\b(our|the panel's|the run's|my) (?:arithmetic|sums?|reading|calculation)|"
    r"\bnot a figure (?:they|the \w+) states?\b|\bour reading\b", re.I)
SKIP_CONTEXT = re.compile(r"(slide|section|item|p\.|page|step|figure|note|block)\s*$", re.I)
# A reference to one of the run's own files, not a claim about the world.
RUNFILE = re.compile(r"\b0\d-[a-z]+(?:\.md)?\b|^#{1,6}\s*0\d\b|\[0\d-", re.I)
# A line that shows its working. If two operands are traceable and the line says
# what was done to them, the result is derived in the open rather than invented.
ARITHMETIC = re.compile(r"\b(minus|plus|times|divided|leaves|of every|out of|is|are|makes)\b", re.I)


def normalise(tok: str) -> set[str]:
    """A figure written several ways is still the same figure."""
    t = tok.lower().strip().rstrip(".,;:")
    forms = {t}
    bare = re.sub(r"[^\d.]", "", t)
    if bare:
        forms.add(bare)
        forms.add(bare.rstrip("0").rstrip(".") if "." in bare else bare)
        if "," in t:
            forms.add(t.replace(",", ""))
        forms.add(bare.replace(".", ","))
    return {f for f in forms if f}


def source_text(material: str) -> str:
    out = []
    for p in pathlib.Path(material).rglob("*"):
        if p.is_file() and p.suffix.lower() in (".md", ".txt", ".csv"):
            out.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(out).lower()


def main() -> int:
    ap = argparse.ArgumentParser(description="Check every figure against the material.")
    ap.add_argument("page")
    ap.add_argument("--material", required=True)
    ap.add_argument("--show", type=int, default=12)
    ap.add_argument("--min-pointers", type=float, default=MIN_POINTERS, metavar="N",
                    help=f"pointers per hundred words the page must carry (default {MIN_POINTERS}, 0 to skip)")
    a = ap.parse_args()

    src = source_text(a.material)
    if not src.strip():
        print(f"no readable material under {a.material}", file=sys.stderr)
        return 2

    page = pathlib.Path(a.page)
    if not page.is_file():
        print(f"No such file: {a.page}", file=sys.stderr)
        return 2
    doc = strip_noise(page.read_text())
    missing, checked, excused = [], 0, 0

    for lineno, line in enumerate(doc.split("\n"), 1):
        line = RUNFILE.sub(" ", line)
        stripped = TOFILL.sub(" ", line)
        own = bool(OWN_WORK.search(line))
        if not own and ARITHMETIC.search(line):
            traceable = sum(1 for t in FIGURE.findall(stripped)
                            if len(re.sub(r"\D", "", t)) >= 2
                            and any(f in src for f in normalise(t)))
            own = traceable >= 2      # the working is on the line, in the source's own numbers
        for m in FIGURE.finditer(stripped):
            tok = m.group(0)
            before = stripped[max(0, m.start() - 12):m.start()]
            if SKIP_CONTEXT.search(before):
                continue
            if len(re.sub(r"\D", "", tok)) < 2:      # single digits are prose, not data
                continue
            checked += 1
            if own:
                excused += 1
                continue
            if not any(f in src for f in normalise(tok)):
                missing.append((lineno, tok, line.strip()[:78]))

    words = sum(count_words(line) for line in doc.split("\n"))
    pointers = len(POINTER.findall(doc))
    density = pointers * 100 / words if words else 0.0
    thin = a.min_pointers > 0 and density < a.min_pointers

    print("## Fact check\n")
    print(f"| Figures traced | {checked} |")
    print("| --- | --- |")
    print(f"| Found in the material | {checked - len(missing) - excused} |")
    print(f"| Derived in the open, or labelled as ours | {excused} |")
    print(f"| **Not found** | **{len(missing)}** |")
    print(f"| Pointers per hundred words | {density:.1f} ({pointers} in {words} words)"
          f"{', **under ' + str(a.min_pointers) + '**' if thin else ''} |")
    print()
    if missing:
        print("| Line | Figure | Where |")
        print("| --- | --- | --- |")
        for lineno, tok, ctx in missing[: a.show]:
            print(f"| {lineno} | `{tok}` | {ctx} |")
        if len(missing) > a.show:
            print(f"| … | {len(missing) - a.show} more | |")
        print()
        print("**A figure that cannot be traced is the failure this tool exists to prevent.** "
              "Either it is in the material under another form, or it should be `[TO FILL: …]`, "
              "or it is the run's own arithmetic and must say so on the line.")
        return 1
    if thin:
        print(f"**Too few pointers.** Under {a.min_pointers} per hundred words the page reads well "
              "and cannot be checked. Go back to the flatten step rather than forward.")
        return 1
    print("Every figure on the page appears in the material, or says whose arithmetic it is.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
