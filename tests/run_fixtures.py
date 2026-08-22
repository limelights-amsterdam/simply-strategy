#!/usr/bin/env python3
"""Regression pass for check_artifact.py.

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
CHECKER = ROOT / "scripts" / "check_artifact.py"

# fixture -> (exit code, {check name fragment: expected state})
# state is "pass", "fail" or "not run".
EXPECT = {
    "green":             (0, {}),
    "no-section-ids":    (1, {"All six sections": "fail",
                              "Exactly three must-solve": "not run",
                              "Every sentence under": "not run",
                              "No section is silently empty": "not run"}),
    "four-must-solve":   (1, {"Exactly three must-solve": "fail"}),
    "remote-css":        (1, {"Self-contained": "fail"}),
    "inline-svg":        (0, {"Self-contained": "pass"}),
    "em-dash":           (1, {"No em dashes": "fail"}),
    "no-reasoning":      (1, {"reasoning.html exists": "fail"}),
    "template-reasoning":(1, {"reasoning.html has no unfilled slots": "fail"}),
    "table-short-cells": (0, {"Every sentence under": "pass"}),
    "svg-text-label":    (0, {"Every sentence under": "pass"}),
    "missing-source":    (1, {"Pointers name real files": "fail"}),

    # The isolation test for the not-run state. Nothing here fails, so the only
    # reason to exit 1 is a check that could not run. Without this fixture,
    # no-section-ids exits 1 because its sections are missing and the gating is
    # never actually proven, which is how the gap survived in the first place.
    "green-no-material": (1, {"Pointers name real files": "not run"}),
}

# fixtures that are the green page run without --material on purpose
NO_MATERIAL_ON_PURPOSE = {"green-no-material"}

# fixtures that carry their own material/ folder and must be run with --material
WITH_MATERIAL = {"missing-source"}


def run(name: str) -> tuple[int, dict]:
    d = ROOT / "tests" / "fixtures" / ("green" if name == "green-no-material" else name)
    cmd = [sys.executable, str(CHECKER), str(d), "--json"]
    if name in WITH_MATERIAL:
        cmd += ["--material", str(d / "material")]
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(p.stdout)
    except json.JSONDecodeError:
        return p.returncode, {}
    state = {}
    for c in data["checks"]:
        state[c["check"]] = "pass" if c["ok"] is True else "fail" if c["ok"] is False else "not run"
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
        for frag, want in want_checks.items():
            got = next((v for k, v in state.items() if frag in k), None)
            if got is None:
                problems.append(f'"{frag}" produced no row')
            elif got != want:
                problems.append(f'"{frag}" {got}, wanted {want}')
        verdict = "✅" if not problems else "❌ " + "; ".join(problems)
        print(f"| {name} | {code} | {len(want_checks)} asserted | {verdict} |")
        if problems:
            failures.append(name)
        if a.verbose:
            for k, v in state.items():
                print(f"|  | | `{k}` | {v} |")

    print()
    if failures:
        print(f"**{len(failures)} fixture(s) behaved differently from the record.** "
              "Either the checker regressed or the record is out of date. Decide which before editing either.")
        return 1
    print(f"All {len(EXPECT)} fixtures behave as recorded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
