# simply-strategy

A Claude Code plugin. One job: turn a folder of strategy documents into one plain-language HTML page.

## The split that matters

**Markdown holds everything a human edits.** Every prompt, rule, angle brief and filter is a `.md`
file under `skills/`. `workflows/simply.js` holds only wiring, which agent runs when, and which file
it reads. It contains no strategy content and never should.

Change how an agent thinks: edit markdown. Change the shape of the run: edit the script.

## Layout

```
.claude-plugin/             plugin.json, and the marketplace entry that serves it
workflows/simply.js         the run. ~90 lines. Names files and agents, nothing else
skills/simply/              what the run's agents read
  references/house-rules.md   prepended to every agent. The filter
  references/pipeline.md      what each step gets and must produce
  references/angles.md        the four panel briefs
  references/output-structure.md  the six sections of the artifact
skills/compass/              the intake. Two modes: read a deck, or ask five questions
                            writes material/<client>/compass.md, never the project root
skills/flatten/            the flattener. eli5 for strategy
skills/plain/               language filter + plainlint.py
skills/plain-strategy/      substance filter + stratlint.py
skills/stop-slop/           de-slop filter
skills/red-team/            the attack angle
design/DESIGN.md            two colours, one column, print-clean
scripts/check_artifact.py   deterministic verification of the rendered output
scripts/check_facts.py      every figure traced back to the material
scripts/check_headings.py   the headings have to read as a story
scripts/check_skills.py     description and body budgets per skill
scripts/render_artifact.py  a mechanical render, for comparing two runs
templates/                  artifact.html, reasoning.html
examples/                   a worked, anonymised run. `check_artifact.py examples/` verifies it
runs/<slug>/<stamp>/       output, one directory per run. Durable, not /tmp
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

  One convention, everywhere an agent reads: **a command spells `{root}/`, prose may write the bare
  path.** In `simply.js` build the path from `root`. Never write a path relative to the file it sits
  in, such as `../plain/scripts/`: an agent resolves it against the working directory, not against
  your file.
- **Publish the measured number, not the hoped-for one.** Runtimes, agent counts and word counts in
  the docs come from a real run. If you change the shape of the run, measure it again.

## Running it

```
/simply-strategy:compass ./material/<client>/   fills that folder's compass.md
/simply-strategy:simply  ./material/<client>/   the run
/workflows                                      live progress
```

Linters, on `runs/<slug>/<stamp>/04-plain.md`:

```
python3 skills/plain/scripts/plainlint.py runs/<slug>/<stamp>/04-plain.md
python3 skills/plain-strategy/scripts/stratlint.py runs/<slug>/<stamp>/04-plain.md
```

Each linter prints its own verdict band and they are not the same number. Read the band, or gate
on it with `--fail-over`.

The artifact checker, after a run:

```
python3 scripts/check_artifact.py runs/<slug>/<stamp>/
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
