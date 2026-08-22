#!/usr/bin/env python3
"""render_artifact - turn a flattened markdown page into the artifact, deterministically.

The renderer in the run is an agent, which is right for a real run: it chooses which
figure fits a finding. This is the ablation version. It maps the six sections onto
the template mechanically, so two runs can be compared on their text rather than on
two different agents' taste in layout.

    python3 scripts/render_artifact.py runs/<slug>/<stamp>/04-plain.md

Writes simple-strategy-artifact.html next to the input.
"""

from __future__ import annotations

import argparse
import html
import pathlib
import re
import sys

IDS = ["one", "must-solve", "stop", "bet", "conflicts", "gaps"]


def inline(md: str) -> str:
    t = html.escape(md)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[TO FILL:([^\]]*)\]", r'<span class="tofill">[TO FILL:\1]</span>', t)
    return t


def blocks(body: str) -> str:
    out, buf, in_list = [], [], False
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith(("- ", "* ")):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(s[2:])}</li>")
            continue
        if in_list and not s.startswith(("- ", "* ")):
            out.append("</ul>"); in_list = False
        if not s:
            if buf:
                out.append(f"<p>{inline(' '.join(buf))}</p>"); buf = []
            continue
        if s.startswith("|") or s.startswith("#"):
            continue
        buf.append(s)
    if buf:
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Render a flattened page into the artifact.")
    ap.add_argument("plain")
    ap.add_argument("--title", default="Simple strategy artifact")
    ap.add_argument("-o", "--out", help="where to write. Defaults next to the input")
    ap.add_argument("--force", action="store_true", help="overwrite an existing file")
    a = ap.parse_args()

    src = pathlib.Path(a.plain)
    md = src.read_text()
    parts = re.split(r"^##\s+(.+)$", md, flags=re.M)[1:]
    pairs = list(zip(parts[0::2], parts[1::2]))
    if not pairs:
        print("no '## ' sections found", file=sys.stderr)
        return 2

    css = pathlib.Path("templates/artifact.html").read_text()
    css = re.search(r"<style>(.*?)</style>", css, re.S).group(1)

    body = []
    for i, (head, text) in enumerate(pairs[: len(IDS)]):
        head = re.sub(r"^\d+\.\s*", "", head.strip())
        tag = "h1" if i == 0 else "h2"
        body.append(f'<section id="{IDS[i]}"><hr><{tag}>{inline(head)}</{tag}>{blocks(text)}</section>')

    out = pathlib.Path(a.out) if a.out else src.with_name("simple-strategy-artifact.html")
    if out.exists() and not a.force:
        # This defaulted to writing beside the input and destroyed a real run's
        # artifact, the one an agent had rendered with the figures it chose. runs/
        # is git-ignored, so there was nothing to recover it from.
        print(f"{out} already exists. Pass -o to write elsewhere, or --force to replace it.",
              file=sys.stderr)
        return 2
    out.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{html.escape(a.title)}</title><style>{css}</style></head><body>"
        f'<main class="page">{"".join(body)}'
        '<footer><hr><div class="m"><span class="caption">AI-supported draft</span>'
        '<span class="caption">rendered mechanically, for comparison</span></div></footer>'
        "</main></body></html>")
    print(f"wrote {out}  ({len(pairs)} sections found, {len(IDS)} rendered)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
