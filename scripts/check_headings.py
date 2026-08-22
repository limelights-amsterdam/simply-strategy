#!/usr/bin/env python3
"""check_headings - the titles have to read as a story on their own.

Someone scanning a strategy page reads the headings and nothing else. If those
headings count what the page contains ("Nine pairs cannot both be true") rather
than saying what the material does, the scan returns a table of contents instead
of an argument.

Two things are checkable and one is not.

Checkable: a heading makes a claim about the material rather than about the page,
and a number or a name in it appears in the section beneath it. The second is the
guarantee against a heading that reads well and is not supported.

Not checkable: whether the sequence is any good. That is judgement, and it belongs
to step 5 of the run.

    python3 scripts/check_headings.py runs/<slug>/<stamp>/simple-strategy-artifact.html
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys

# The word counter, the sentence limit and the figure shape are the ones the rest
# of the run measures with. The section names come from the artifact checker.
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "skills" / "plain" / "scripts"))
sys.path.insert(0, str(HERE))
from textlib import FIGURE, L1_MAX_SENTENCE as MAX_WORDS, count_words  # noqa: E402
from check_artifact import SECTIONS, drop_provenance  # noqa: E402

# A heading whose subject is a count of what the page holds.
COUNTING = re.compile(
    r"^\s*(?:all\s+)?(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|\d+)\s+"
    r"(?:things?|pairs?|unknowns?|bets?|gaps?|items?|findings?|reasons?|points?)\b",
    re.I,
)
STOP = set("""a an the and or but of to in on at for with from by as is are was were be been
being it its this that these those has have had not no nor so than then there here which who
whom whose what when where why how all any both each few more most other some such only own
same too very can will just do does did done into out up down over under again further once
you your they their we our us them he she his her""".split())



def text_of(fragment: str) -> str:
    """Visible text. Provenance blocks are the log on the page, not the section,
    so a name that only appears there does not ground a heading."""
    f = re.sub(r"<[^>]+>", " ", drop_provenance(fragment))
    return re.sub(r"\s+", " ", html.unescape(f)).strip()


def content_words(s: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z'-]+", s.lower())
    return [w for w in words if w not in STOP and len(w) > 2]


# A heading that merely repeats a section name is a label, and a page of labels
# is a table of contents. Compared on content words, so "The three things that
# must be solved" and "Three things must be solved" are the same label.
LABELS = {frozenset(content_words(name)) for name in SECTIONS.values()}


def sections(doc: str):
    """Each heading with the text that follows it, up to the next heading."""
    parts = list(re.finditer(r"<(h1|h2|h3)>(.*?)</\1>", doc, re.S))
    for i, m in enumerate(parts):
        end = parts[i + 1].start() if i + 1 < len(parts) else len(doc)
        yield text_of(m.group(2)), text_of(doc[m.end():end])


def main() -> int:
    ap = argparse.ArgumentParser(description="Check that the headings read as a story.")
    ap.add_argument("artifact")
    ap.add_argument("--max-words", type=int, default=MAX_WORDS)
    ap.add_argument("--json", action="store_true",
                    help="machine-readable, for tests/run_fixtures.py")
    a = ap.parse_args()

    path = pathlib.Path(a.artifact)
    if not path.is_file():
        print(f"No such file: {a.artifact}", file=sys.stderr)
        return 2
    doc = path.read_text(encoding="utf-8")
    rows, failed = [], 0
    prev_subject = set()

    for i, (head, body) in enumerate(sections(doc), 1):
        problems = []
        if frozenset(content_words(head)) in LABELS:
            problems.append("names the section instead of claiming anything")
        elif COUNTING.match(head):
            problems.append("counts the page, does not claim anything about the material")
        n = count_words(head)
        if n > a.max_words:
            problems.append(f"{n} words")
        # Only numbers and proper names. A heading is a compression and is
        # entitled to different words from its section; what gets invented is a
        # figure or a name, so that is what this checks. A capital after a full
        # stop is a sentence opening, not a name.
        scan = re.sub(r"(^|[.!?]\s+)([A-Z])", lambda m: m.group(1) + m.group(2).lower(), head)
        facts = FIGURE.findall(scan) + re.findall(r"\b[A-Z][A-Za-z0-9]{2,}\b", scan)
        below = body.lower()
        ungrounded = [f for f in facts
                      if f.lower().strip() not in below and f.split()[0].lower() not in below]
        if ungrounded:
            problems.append("a number or name not found below: " + ", ".join(ungrounded[:4]))
        subject = set(content_words(head)[:3])
        if prev_subject and subject and subject <= prev_subject:
            problems.append("repeats the previous heading's subject")
        prev_subject = subject
        rows.append((i, head, problems))
        if problems:
            failed += 1

    if a.json:
        print(json.dumps({"failed": failed,
                          "headings": [{"n": i, "heading": h, "problems": p}
                                       for i, h, p in rows]}, indent=2))
        return 1 if failed else 0

    print("## Headings\n")
    print("| # | Heading | Verdict |")
    print("| --- | --- | --- |")
    for i, head, problems in rows:
        print(f"| {i} | {head} | {'✅' if not problems else '❌ ' + '; '.join(problems)} |")
    print()
    print("Read on their own, in order:\n")
    for _, head, _ in rows:
        print(f"  {head}")
    print()
    if failed:
        print(f"**{failed} heading(s) do not carry their weight.** A reader who scans only the "
              "headings should get the argument, not the table of contents.")
    else:
        print("Every heading makes a grounded claim. Whether the sequence is any good is a "
              "judgement no script makes: that is step 5's.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
