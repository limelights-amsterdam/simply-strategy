# simply-strategy

A Claude Code plugin. One job: turn a folder of strategy documents into one plain-language HTML page.

## The split that matters

**Markdown holds everything a human edits.** Every prompt, rule, angle brief and filter is a `.md`
file under `skills/`. `workflows/simply.js` holds only wiring — which agent runs when, and which file
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
skills/simplify/            the flattener. eli5 for strategy
skills/plain/               language filter + plainlint.py
skills/plain-strategy/      substance filter + stratlint.py
skills/stop-slop/           de-slop filter
skills/red-team/            the attack angle
design/DESIGN.md            two colours, one column, print-clean
scripts/check_artifact.py   deterministic verification of the rendered output
templates/                  artifact.html, reasoning.html
runs/<slug>/                output. Durable, not /tmp
```

## House rules for working in this repo

- **Keep `SKILL.md` to what a reader needs to act.** Lookup tables, word lists and worked examples go
  to `references/`, which loads only when needed.

  Two budgets, because they cost differently. The **description** rides in every session whether the
  skill fires or not, so keep it under about 120 words. The **body** loads when the skill fires:
  under about 1000 words, and never past the documented 500 lines.

  These are ceilings with a reason, not targets. A file that is 40 words over and coherent beats one
  cut to fit. The one description worth spending over the ceiling on is trigger coverage: `plain`
  (152) and `plain-strategy` (149) both run long because they list trigger phrases in two languages,
  and a skill that never fires costs more than a description that runs long. Anything else over the
  ceiling is weight that belongs in `references/`.

  This replaces an 80-line rule that was stricter than the documented guidance, counted the wrong
  thing, and was broken by six of seven skills here. Lines are a bad proxy: a one-line description
  can carry 150 words and cost more than the body it introduces.
- **The filter order is substance, then language, then de-slop.** Rewriting an empty sentence gives
  you a tidy empty sentence.
- **Never invent a number.** `[TO FILL: what is needed]`, always.
- **No em dashes in anything the run generates.** The de-slop filter strips them from `04-plain.md`
  and the artifact. This repo's own documentation is written for people and uses ordinary
  punctuation. The ban is about generated prose, where an em dash is an AI tell, not about English.
- **Output language is English**, whatever the source documents are in.
- **The artifact is black and white.** Two colours plus one grey. This includes the SVGs.
- **Never write a bare path to a plugin file.** `skills/`, `scripts/`, `templates/` and `design/`
  live under the plugin, which is not the folder the user is working in. In `simply.js` build every
  such path from `root`. In a reference file an agent reads, the run tells it to prefix them. A path
  that is correct in a clone and wrong once installed is the failure mode this repo keeps hitting.
- **Publish the measured number, not the hoped-for one.** Runtimes, agent counts and word counts in
  the docs come from a real run. If you change the shape of the run, measure it again.

## Running it

```
/simply-strategy:compass ./material/<client>/   fills that folder's compass.md
/simply-strategy:simply  ./material/<client>/   the run
/workflows                                      live progress
```

Linters, on `runs/<slug>/04-plain.md`:

```
python3 skills/plain/scripts/plainlint.py runs/<slug>/04-plain.md
python3 skills/plain-strategy/scripts/stratlint.py runs/<slug>/04-plain.md
```

Under 1.5 weighted findings per 100 words is clean.

The artifact checker, after a run:

```
python3 scripts/check_artifact.py runs/<slug>/
```

## One owner per rule

Every normative rule lives in exactly one file. Everywhere else is a one-line summary and a pointer.
When you add a rule, put it where it belongs and link to it:

| Rule | Owner |
|---|---|
| The six sections, and what may be unanswered | `skills/simplify/references/output.md` |
| The four visual slots, and what fills them | `skills/simply/references/output-structure.md` |
| How anything looks, colour, type, print | `design/DESIGN.md` |
| The filter and the rules no agent may break | `skills/simply/references/house-rules.md` |
| What each step gets and must produce | `skills/simply/references/pipeline.md` |
| The seven substance tests, in full | `skills/plain-strategy/references/tests.md` |
| The language rules and replacement lists | `skills/plain/references/` |
| How the run is started, and where the plugin root comes from | `skills/simply/SKILL.md` |

`house-rules.md` keeps a compact copy of the seven tests on purpose. Every agent reads it first, and
sending each one to open another file to find the core checklist costs a read per agent.
