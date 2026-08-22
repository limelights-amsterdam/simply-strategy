# simply-strategy

A Claude Code plugin. One job: turn a folder of strategy documents into one plain-language HTML page.

## The split that matters

**Markdown holds everything a human edits.** Every prompt, rule, angle brief and filter is a `.md`
file under `skills/`. `workflows/simply.js` holds only wiring — which agent runs when, and which file
it reads. It contains no strategy content and never should.

Change how an agent thinks: edit markdown. Change the shape of the run: edit the script.

## Layout

```
workflows/simply.js         the run. ~60 lines. Names files and agents, nothing else
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

- **Every `SKILL.md` stays under 80 lines.** Weight goes in `references/`. If a SKILL.md is growing,
  something belongs in a reference file.
- **The filter order is substance, then language, then de-slop.** Rewriting an empty sentence gives
  you a tidy empty sentence.
- **Never invent a number.** `[TO FILL: what is needed]`, always.
- **No em dashes in anything the run generates.** The de-slop filter strips them from `04-plain.md`
  and the artifact. This repo's own documentation is written for people and uses ordinary
  punctuation. The ban is about generated prose, where an em dash is an AI tell, not about English.
- **Output language is English**, whatever the source documents are in.
- **The artifact is black and white.** Two colours plus one grey. This includes the SVGs.

## Running it

```
/compass ./material/<client>/   fills that folder's compass.md
/simply ./material/<client>/   the run
/workflows               live progress
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

`house-rules.md` keeps a compact copy of the seven tests on purpose. Every agent reads it first, and
sending each one to open another file to find the core checklist costs a read per agent.
