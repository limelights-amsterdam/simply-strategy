# simply-strategy

A Claude Code plugin. One job: distil a folder of strategy documents into one plain-language HTML
page that anyone can read.

## What this is made of

**Markdown and Python, nothing else.** `/simply` is six steps that one reader walks in order, writing
numbered files. No subagents, no runtime, nothing fetched.

There was a nine-agent version in a JavaScript workflow, with the four angles blind to each other. On
the same 76-slide deck it produced 3848 words with nine untraced figures, where the sequential run
produced 714 with none. It is in the git history rather than in the repo.

**Every prompt, rule, angle brief and filter is a `.md` file under `skills/`.** Change how a step
thinks by editing markdown. The Python does the things a script does better than a judgement: tracing
a figure to its source, counting words, checking a rendered page.

## Layout

```
.claude-plugin/             plugin.json, and the marketplace entry that serves it
skills/simply/              the run
  references/house-rules.md   read first, at every step. The filter and the unbreakable rules
  references/pipeline.md      what each step gets, must produce, and how it fails
  references/angles.md        the four passes
  references/output-structure.md  the figures and the two files
skills/compass/             the intake. Reads a deck, or asks five questions
skills/flatten/             the flattener. references/output.md owns the six sections
skills/plain/               language filter, plainlint.py, textlib.py
skills/plain-strategy/      substance filter, stratlint.py
skills/stop-slop/           de-slop filter
skills/humanizer/           the last pass, so it reads like a person
skills/red-team/            the attack angle
scripts/check_facts.py      every figure traced back to the material
scripts/check_artifact.py   the rendered page, thirteen checks
scripts/check_headings.py   the headings have to read as a story
scripts/check_skills.py     description and body budgets per skill
scripts/render_artifact.py  a mechanical render, for comparing two runs
design/DESIGN.md            two colours, one column, print-clean, six figures
templates/                  artifact.html, reasoning.html, figures.html
examples/                   a worked, anonymised run that validates in CI
tests/                      twelve fixtures and their expected verdicts
material/<client>/          input, plus that client's compass.md. Git-ignored
runs/<slug>/<stamp>/        output. Git-ignored
```

## House rules for working in this repo

- **Keep `SKILL.md` to what a reader needs to act.** Lookup tables, word lists and worked examples go
  to `references/`, which loads only when needed.

  Two budgets, because they cost differently. The **description** rides in every session whether the
  skill fires or not, so keep it under about 120 words. The **body** loads when the skill fires:
  under about 1000 words, and never past the documented 500 lines.

  These are ceilings with a reason, not targets. A file that is 40 words over and coherent beats one
  cut to fit. The one thing worth spending over the ceiling on is trigger coverage: `plain` and
  `plain-strategy` both run long because they spell out the everyday phrases that should fire them,
  and a skill that never fires costs more than a description that runs long. Anything else over the
  ceiling is weight that belongs in `references/`.

  Do not quote the counts here. `python3 scripts/check_skills.py` measures them, names the two
  exceptions and exits 1 on anything else.
- **The filter order is substance, then language, then de-slop.** Rewriting an empty sentence gives
  you a tidy empty sentence.
- **Never invent a number.** `[TO FILL: what is needed]`, always.
- **No em dashes anywhere, including this repo's own documentation.** The de-slop filter strips them
  from `04-plain.md` and the artifact, and the docs now hold to the same rule. The earlier version of
  this line exempted the documentation on the grounds that the ban was about generated prose. That
  exemption covered 79 of them, which is what an exemption is for.
- **Output language is English**, whatever the source documents are in.
- **The artifact is black and white.** Two colours plus one grey. This includes the SVGs.
- **Never write a bare path to a plugin file.** `skills/`, `scripts/`, `templates/` and `design/`
  live under the plugin, which is not the folder the user is working in. A path that is correct in a
  clone and wrong once installed is the failure mode this repo keeps hitting.

  One convention, everywhere a step reads: **a command spells `{root}/`, prose may write the bare
- **Publish the measured number, not the hoped-for one.** Run times, step counts and word counts in
  the docs come from a real run. If you change the shape of the run, measure it again.

## Running it

```
/simply-strategy:compass ./material/<client>/   fills that folder's compass.md, once per client
/simply-strategy:simply  ./material/<client>/   the run, six steps in order
```

There is no progress screen, because there is nothing running in the background. Watch the numbered
files appear in `runs/<slug>/<stamp>/`. They are also the recovery path: if a run stops, look at the
highest number that finished and start at the next step.

All five checks, after a run:

```
python3 scripts/check_facts.py    runs/<slug>/<stamp>/04-plain.md --material material/<slug>/
python3 skills/plain/scripts/plainlint.py runs/<slug>/<stamp>/04-plain.md --lang en --max-sentence 15
python3 skills/plain-strategy/scripts/stratlint.py runs/<slug>/<stamp>/04-plain.md --lang en
python3 scripts/check_artifact.py runs/<slug>/<stamp>/ --material material/<slug>/
python3 scripts/check_headings.py runs/<slug>/<stamp>/simple-strategy-artifact.html
```

Each linter prints its own verdict band and they are not the same number: plainlint scores per
hundred words of prose it scanned, stratlint per hundred words of the whole document. Read each
against its own band, or gate on it with `--fail-over`.

And on the repo itself:

```
python3 scripts/check_skills.py skills/
python3 tests/run_fixtures.py
python3 scripts/check_artifact.py examples/ --material examples/material/
```

## One owner per rule

Every normative rule lives in exactly one file. Everywhere else is a one-line summary and a pointer.
When you add a rule, put it where it belongs and link to it:

| Rule | Owner |
|---|---|
| The six sections, and what may be unanswered | `skills/flatten/references/output.md` |
| The four visual slots, and what fills them | `skills/simply/references/output-structure.md` |
| How anything looks, colour, type, print | `design/DESIGN.md` |
| The filter and the rules no agent may break | `skills/simply/references/house-rules.md` |
| What each step gets and must produce | `skills/simply/references/pipeline.md` |
| The seven substance tests, in full | `skills/plain-strategy/references/tests.md` |
| The language rules and replacement lists | `skills/plain/references/` |
| How the run is started, and where the plugin root comes from | `skills/simply/SKILL.md` |
| The length budget: page, caption, sentence | `skills/flatten/references/output.md` |

`house-rules.md` keeps a compact copy of the seven tests on purpose. Every agent reads it first, and
sending each one to open another file to find the core checklist costs a read per agent.
