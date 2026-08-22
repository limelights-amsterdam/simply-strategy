#!/usr/bin/env python3
"""Regression pass for check_artifact.py and check_headings.py.

Every fixture here exists because something was once silently wrong. A checker
that only ever passes is worthless, so most of these are pages that must fail,
and each one names the check it must fail on.

    python3 tests/run_fixtures.py
    python3 tests/run_fixtures.py --verbose

Exit 1 if any fixture behaves differently from what is recorded below.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "simply-strategy" / "scripts"
CHECKER = SCRIPTS / "check_artifact.py"
HEADINGS = SCRIPTS / "check_headings.py"

# fixture -> (exit code, {check id: expected state})
# Ids are the stable handles check_artifact.Result.add sets; display names may
# carry a budget number and are allowed to change. State is "pass", "fail" or
# "not run".
EXPECT = {
    "green":             (0, {}),
    "no-section-ids":    (1, {"sections": "fail",
                              "three-musts": "not run",
                              "sentence-length": "not run",
                              "thin-sections": "not run"}),
    "four-must-solve":   (1, {"three-musts": "fail"}),
    "remote-css":        (1, {"self-contained": "fail"}),
    "inline-svg":        (0, {"self-contained": "pass"}),
    "em-dash":           (1, {"em-dashes": "fail"}),
    "no-reasoning":      (1, {"reasoning-exists": "fail"}),
    "template-reasoning":(1, {"reasoning-unfilled": "fail"}),
    "table-short-cells": (0, {"sentence-length": "pass"}),
    "svg-text-label":    (0, {"sentence-length": "pass"}),
    "missing-source":    (1, {"pointers-exist": "fail"}),

    # The isolation test for the not-run state. Nothing here fails, so the only
    # reason to exit 1 is a check that could not run. Without this fixture,
    # no-section-ids exits 1 because its sections are missing and the gating is
    # never actually proven, which is how the gap survived in the first place.
    "green-no-material": (1, {"pointers-exist": "not run"}),
}

# Every fixture carries the material folder its pointers cite, so pointer
# validation runs on all of them. green-no-material is the exception on purpose:
# it is the same page run without the flag, to prove a check that cannot run
# stops the artifact.
NO_MATERIAL = {"green-no-material"}


# heading fixture -> (exit code, the problem the failing heading must report)
# Six small pages, each named for the rule it breaks, so a rule that stops
# firing is visible.
HEADING_EXPECT = {
    "story":            (0, None),
    "labels":           (1, "names the section"),
    "counting":         (1, "counts the page"),
    "ungrounded":       (1, "not found below"),
    "repeated-subject": (1, "repeats the previous"),
    "too-long":         (1, "words"),
    "no-headings":      (1, None),
}


def run_headings(name: str) -> tuple[int, list[str]]:
    f = ROOT / "tests" / "headings" / f"{name}.html"
    p = subprocess.run([sys.executable, str(HEADINGS), str(f), "--json"],
                       capture_output=True, text=True)
    try:
        data = json.loads(p.stdout)
    except json.JSONDecodeError:
        return p.returncode, []
    return p.returncode, [q for h in data["headings"] for q in h["problems"]]


def run(name: str) -> tuple[int, dict]:
    d = ROOT / "tests" / "fixtures" / ("green" if name == "green-no-material" else name)
    cmd = [sys.executable, str(CHECKER), str(d), "--json"]
    if name not in NO_MATERIAL:
        cmd += ["--material", str(d / "material")]
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(p.stdout)
    except json.JSONDecodeError:
        return p.returncode, {}
    state = {}
    for c in data["checks"]:
        state[c["id"]] = "pass" if c["ok"] is True else "fail" if c["ok"] is False else "not run"
    return p.returncode, state


def main() -> int:
    ap = argparse.ArgumentParser(description="Regression pass for the artifact checker.")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    failures = []
    print("## Fixture pass\n")
    print("| Fixture | Exit | Checks | Verdict |")
    print("| --- | --- | --- | --- |")
    for name, (want_code, want_checks) in EXPECT.items():
        code, state = run(name)
        problems = []
        if code != want_code:
            problems.append(f"exit {code}, wanted {want_code}")
        for cid, want in want_checks.items():
            got = state.get(cid)
            if got is None:
                problems.append(f'"{cid}" produced no row')
            elif got != want:
                problems.append(f'"{cid}" {got}, wanted {want}')
        verdict = "✅" if not problems else "❌ " + "; ".join(problems)
        print(f"| {name} | {code} | {len(want_checks)} asserted | {verdict} |")
        if problems:
            failures.append(name)
        if a.verbose:
            for k, v in state.items():
                print(f"|  | | `{k}` | {v} |")

    print("\n## Heading fixtures\n")
    print("| Fixture | Exit | Verdict |")
    print("| --- | --- | --- |")
    for name, (want_code, want_problem) in HEADING_EXPECT.items():
        code, problems = run_headings(name)
        problems_ = []
        if code != want_code:
            problems_.append(f"exit {code}, wanted {want_code}")
        if want_problem and not any(want_problem in q for q in problems):
            problems_.append(f'nothing reported "{want_problem}"')
        verdict = "✅" if not problems_ else "❌ " + "; ".join(problems_)
        print(f"| {name} | {code} | {verdict} |")
        if problems_:
            failures.append(f"headings/{name}")

    print()
    if failures:
        print(f"**{len(failures)} fixture(s) behaved differently from the record.** "
              "Either the checker regressed or the record is out of date. Decide which before editing either.")
        return 1
    print(f"All {len(EXPECT) + len(HEADING_EXPECT)} fixtures behave as recorded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
