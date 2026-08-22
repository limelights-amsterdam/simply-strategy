#!/usr/bin/env python3
"""check_skills - keep SKILL.md files inside their context budget.

Two budgets, because they cost differently. The **description** is loaded in every
session whether the skill fires or not. The **body** is loaded only when it fires.
A house rule nobody measures is not a house rule, so this measures it.

    python3 scripts/check_skills.py skills/
    python3 scripts/check_skills.py skills/ --json

Exit code 1 when a skill is over budget and is not a named exception.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

MAX_DESCRIPTION_WORDS = 120
MAX_BODY_WORDS = 1000
MAX_BODY_LINES = 500          # the documented ceiling for a SKILL.md body

# Named exceptions, with the reason. A skill that lists its trigger phrases in two
# languages pays for it in the description, and a skill that never fires costs more
# than a description that runs long. Anything not on this list and over budget is
# weight that belongs in references/.
EXCEPTIONS = {
    "plain": "lists trigger phrases in English and Dutch",
    "plain-strategy": "lists trigger phrases in English and Dutch",
}


def measure(path: str) -> dict:
    src = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", src, re.S)
    front, body = (m.group(1), src[m.end():]) if m else ("", src)
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.sub(r"^name:.*$", "", front, flags=re.M)
    return {
        "skill": (name.group(1).strip() if name else os.path.basename(os.path.dirname(path))),
        "path": path,
        "description_words": len(re.findall(r"\w+", desc)),
        "body_words": len(re.findall(r"\w+", body)),
        "body_lines": body.count("\n"),
    }


def judge(row: dict) -> list[str]:
    over = []
    if row["description_words"] > MAX_DESCRIPTION_WORDS:
        over.append(f"description +{row['description_words'] - MAX_DESCRIPTION_WORDS}")
    if row["body_words"] > MAX_BODY_WORDS:
        over.append(f"body +{row['body_words'] - MAX_BODY_WORDS}")
    if row["body_lines"] > MAX_BODY_LINES:
        over.append(f"lines +{row['body_lines'] - MAX_BODY_LINES}")
    return over


def main() -> int:
    ap = argparse.ArgumentParser(description="Keep SKILL.md files inside their context budget.")
    ap.add_argument("root", nargs="?", default="skills", help="folder holding the skills")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = [measure(p) for p in sorted(glob.glob(os.path.join(a.root, "*", "SKILL.md")))]
    if not rows:
        print(f"no SKILL.md found under {a.root}", file=sys.stderr)
        return 2

    failed = []
    for row in rows:
        row["over"] = judge(row)
        row["excused"] = row["skill"] in EXCEPTIONS
        if row["over"] and not row["excused"]:
            failed.append(row)

    if a.json:
        print(json.dumps({"skills": rows, "failed": len(failed)}, indent=2))
        return 1 if failed else 0

    print("## Skill budgets\n")
    print(f"| Skill | Description | Body | Lines | Verdict |")
    print("| --- | --- | --- | --- | --- |")
    for row in rows:
        if not row["over"]:
            verdict = "✅ within"
        elif row["excused"]:
            verdict = f"⚠️ over, allowed: {EXCEPTIONS[row['skill']]}"
        else:
            verdict = "❌ " + ", ".join(row["over"])
        print(f"| {row['skill']} | {row['description_words']} | {row['body_words']} "
              f"| {row['body_lines']} | {verdict} |")
    print(f"\nBudgets: description {MAX_DESCRIPTION_WORDS} words, body {MAX_BODY_WORDS} words, "
          f"{MAX_BODY_LINES} lines.")
    print("The description rides in every session. The body loads only when the skill fires.")
    if failed:
        print(f"\n**{len(failed)} skill(s) over budget.** What is over is usually a lookup table, "
              "a word list or a worked example, and those belong in `references/`.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
