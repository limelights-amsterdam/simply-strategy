# simply-strategy

A Claude Code plugin with one skill, `simply-strategy`. One job: distil a folder of strategy documents
into one plain-language HTML page that anyone can read. The skill walks an intake and six steps in
order; everything it reads, runs or fills sits under `skills/simply-strategy/`.

## What this is made of

**Markdown and Python, nothing else.** `/simply-strategy` is an intake and six steps that one reader walks
in order, writing numbered files. No subagents, no runtime, nothing fetched. Each step sees what the
last one wrote, which is what makes the argument hold together and the figures trace.

**Every prompt, rule, angle brief and filter is a `.md` file under `skills/simply-strategy/references/`.**
Change how a step thinks by editing markdown. The Python does the things a script does better than a
judgement: tracing a figure to its source, counting words, checking a rendered page.

## Layout

```
.claude-plugin/             plugin.json, and the marketplace entry that serves it
skills/simply-strategy/
  SKILL.md                  the run, and where {root} comes from
  references/
    house-rules.md            read first, at every step. The filter and the unbreakable rules
    pipeline.md               what each step gets, must produce, and how it fails
    angles.md                 the four passes
    output-structure.md       the figures and the two files
    compass.md                step 0, the intake. compass-fields.md and compass-template.md beside it
    flatten/                  moves.md (levels and the seven moves), output.md (owns the six
                              sections and the budget), rules.md, before-after.md
    substance/                tests.md (the seven tests in full), strategy-jargon.md
    language/                 plain-patterns.md, slop-patterns.md, the stop-slop-* files,
                              humanizer.md and its patterns. Loaded in step 4 only
  scripts/
    textlib.py                one ruler: word count, sentence split, budgets, shapes
    plainlint.py              language, per hundred words of prose
    stratlint.py              substance, per hundred words of document
    check_facts.py            every figure traced back to the material
    check_artifact.py         the rendered page
    check_headings.py         the headings have to read as a story
  assets/                   artifact.html, reasoning.html, figures.html
tests/                      nineteen fixtures and their expected verdicts
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
  cut to fit. The one thing worth spending over the ceiling on is trigger coverage: the description
  spells out the everyday phrases that should fire it, and a skill that never fires costs more than a
  description that runs long. Anything else over the ceiling is weight that belongs in `references/`.
- **The filter order is substance, then language, then de-slop.** Rewriting an empty sentence gives
  you a tidy empty sentence.
- **Never invent a number.** `[TO FILL: what is needed]`, always.
- **No em dashes anywhere, including this repo's own documentation.** The de-slop filter strips them
  from `04-plain.md` and the artifact, and the docs now hold to the same rule. The earlier version of
  this line exempted the documentation on the grounds that the ban was about generated prose. That
  exemption covered 79 of them, which is what an exemption is for.
- **Output language is English**, whatever the source documents are in.
- **The artifact is black and white.** Two colours plus one grey. This includes the SVGs.
- **Never write a bare path to a plugin file.** `references/`, `scripts/` and `assets/` live under
  the skill, which is not the folder the user is working in. A path that is correct in a clone and
  wrong once installed is the failure mode this repo keeps hitting.

  One convention, everywhere a step reads: **a command spells `{root}/`, prose may write the path
  relative to the skill folder.** `skills/simply-strategy/SKILL.md` says where `{root}` comes from: the
  folder that `SKILL.md` sits in.
- **Publish the measured number, not the hoped-for one.** Run times, step counts and word counts in
  the docs come from a real run. If you change the shape of the run, measure it again.

## Running it

```
/simply-strategy ./material/<client>/   the run. Fills compass.md first if the folder has none
```

There is no progress screen, because there is nothing running in the background. Watch the numbered
files appear in `runs/<slug>/<stamp>/`. They are also the recovery path: if a run stops, look at the
highest number that finished and start at the next step.

The five checks, after a run, from a clone:

```
S=skills/simply-strategy/scripts
python3 $S/check_facts.py     runs/<slug>/<stamp>/04-plain.md --material material/<slug>/
python3 $S/plainlint.py       runs/<slug>/<stamp>/04-plain.md --max-sentence 15
python3 $S/stratlint.py       runs/<slug>/<stamp>/04-plain.md
python3 $S/check_artifact.py  runs/<slug>/<stamp>/ --material material/<slug>/
python3 $S/check_headings.py  runs/<slug>/<stamp>/simple-strategy-artifact.html
```

Each linter prints its own verdict band and they are not the same number: plainlint scores per
hundred words of prose it scanned, stratlint per hundred words of the whole document. Read each
against its own band, or gate on it with `--fail-over`.

And on the repo itself, the fixture pass for the two page checkers:

```
python3 tests/run_fixtures.py
```

## One owner per rule

Every normative rule lives in exactly one file. Everywhere else is a one-line summary and a pointer.
When you add a rule, put it where it belongs and link to it:

| Rule | Owner |
|---|---|
| The six sections, and what may be unanswered | `references/flatten/output.md` |
| The four visual slots, and what fills them | `references/output-structure.md` |
| How anything looks, colour, type, print | `assets/`, and the rules for filling them in `references/output-structure.md` |
| The filter and the rules no agent may break | `references/house-rules.md` |
| What each step gets and must produce | `references/pipeline.md` |
| The five intake fields | `references/compass.md` and `compass-fields.md` |
| The seven substance tests, in full | `references/substance/tests.md` |
| The language rules and replacement lists | `references/language/` |
| How the run is started, and where `{root}` comes from | `SKILL.md` |
| The length budget: page, caption, sentence | `references/flatten/output.md` |
| The headings carry the argument | `references/flatten/output.md` |
| The shape of a source pointer | `references/house-rules.md` |

Paths in this table are relative to `skills/simply-strategy/`.

`house-rules.md` keeps a compact copy of the seven tests on purpose. Every step reads it first, and
opening another file to find the core checklist would cost a read per step. The scripts read their
budgets from one place too: `scripts/textlib.py`, which copies the numbers from
`references/flatten/output.md`.
