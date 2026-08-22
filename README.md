# Simply Strategy

A Claude Code plugin. Point it at a folder of strategy documents. Get back one page a board reads in
under six minutes.

```
/simply-strategy:compass ./material/acme/    once per client, five questions or a deck
/simply-strategy:simply  ./material/acme/    six steps, about half an hour
```

Out comes `simple-strategy-artifact.html`: black and white, big type, few words, prints on any
machine in the room. Beside it `reasoning.html`, which shows what was read, what was set aside, and
where the run is unsure.

## What it is for

**Distilling, not shortening.** A folder holds a decision somewhere inside a great deal of context.
The job is to boil that down until what is actually being decided is visible to anyone who reads it.
Not the leadership team. Anyone.

Two things follow from putting it that way.

**The context comes down with it.** A distillation that drops what a claim rests on is just a shorter
document. So every figure on the page traces to a source, every section can show its own working, and
the reasoning log carries the chain in full.

**Nothing is added on the way.** The one thing that must never happen is a page that reads clearly
and says something the material does not.

## Why it is not a summariser

There is a plugin called `eli5` whose whole instruction is one sentence: explain this to someone who
knows nothing, using big pictures and few words. Its example is `/eli5 how does DNS work`, and that
example is why it works.

**DNS has a ground truth.** It does one thing, in one way, and that way does not depend on who is
asking. Simplify it wrongly and someone who knows DNS can point at the sentence. The simplification
is safe because there is something underneath to check against.

**A strategy document usually has no ground truth.** It is not a description of how something works.
It is a set of claims about what an organisation intends, and many of them were left unresolved on
purpose, because vagueness is how a document gets signed by six people who disagree.

"We will strengthen our position in the market" is not a fact badly explained. It is a sentence
written so that the person who wants to buy a competitor and the person who wants to cut costs can
both nod at it.

Flatten that and you get *we are going to win more customers*. Short, concrete, and a decision nobody
made. Simplifying did not reveal the meaning. It manufactured one, in confident type, where it will
be quoted back in a meeting.

That is the failure this prevents. Not a bad summary. A **beautifully simple lie**.

When the material genuinely contains no decision, the page says so. That is the most useful thing it
can return, and it is the one answer a summariser cannot give, because a summary of an empty document
is a shorter empty document.

## Who it is for, and the bar

The page is written for the board. That is the audience.

The bar is different: anyone in a ten-thousand-person company should be able to follow it. Not
because they will all read it, but because a sentence a new starter reads twice is a sentence the CFO
reads twice too, out loud, in a room, with an opinion.

## Flatten levels

Every document sits at a level. Most ship at L5 while the room believes they are at L2.

| Level | Name | Test |
|---|---|---|
| **L5** | Board memo | As written. Jargon intact |
| **L4** | Plain | Jargon gone. Sentences under 25 words |
| **L3** | Choice | A decision is visible. What we stop doing is named |
| **L2** | Picture | Every abstraction is a person doing something. Every number has a comparison |
| **L1** | Child | Every sentence under 15 words. A ten-year-old repeats it back |

The artifact ships at L1. The run also reports the level the input came in at, which is usually the
most uncomfortable line in the reasoning log.

## The Compass

The intake asks what you refuse before it asks what you want.

A goal list can only tell you things you already knew to ask about. An anti-vision and a boundary let
a reader notice something you never wrote a goal for. Describe a Tuesday five years out where this
strategy quietly failed, name what you will not give up whatever happens, and an angle can say *this
plan walks toward precisely that*.

Five fields, all optional. Fill it by pointing at the client's own deck and correcting the draft, or
by answering five questions. A half-filled Compass still runs, and the page names what was missing.

It lives at `material/<client>/compass.md`, beside the documents it describes.

## The six steps

One reader walks them in order. No subagents. Nothing is held in memory between steps, so the
numbered files are the state and a stopped run resumes at the next one. Each step sees what the last
one wrote, which is what keeps the argument whole and the figures traceable.

| # | Step | Writes |
|---|---|---|
| 1 | Inventory the folder, and what it names but does not contain | `01-spec.md` |
| 2 | Read it from four angles: substance, contradiction, compass, red team | `02-angles.md` |
| 3 | Rank to exactly three, and write the argument | `03-plan.md` |
| 4 | Flatten to L1, headings taken from the argument | `04-plain.md` |
| 5 | Run three scripts, then check both fidelity hops | `05-verdict.md` |
| 6 | Render, then check the rendered page | two HTML files |

**Step 3 owes an argument, not a sort.** A governing thought the whole page is evidence for, and the
through-line as one claim per section, which becomes the headings. Without it the page is a
well-ranked list, which is what it was before that step existed.

## The rules it will not break

Exactly three must-solve items. No invented numbers: an unknown figure, owner or date comes out as
`[TO FILL: …]`. Its own arithmetic says so on the line. Every claim carries a pointer, at least two
per hundred words. Nothing is softened. A section the material cannot answer says so in a full
sentence. The "where I'm unsure" section is never empty.

The full versions, with the why, are in `skills/simply/references/house-rules.md`, which every step
reads first.

## It checks its own work

Three checks and a fixture pass, because a check a script can make should not be a judgement call.

```bash
python3 scripts/check_facts.py     runs/<slug>/<stamp>/04-plain.md --material material/<slug>/
python3 scripts/check_artifact.py  runs/<slug>/<stamp>/ --material material/<slug>/
python3 scripts/check_headings.py  runs/<slug>/<stamp>/simple-strategy-artifact.html
python3 tests/run_fixtures.py
```

| Script | What it will not let through |
|---|---|
| `check_facts` | A figure that appears nowhere in the material and does not say whose arithmetic it is, or a page with too few pointers |
| `check_artifact` | A missing section, an unfilled slot, a sentence over fifteen words, a page that loads something |
| `check_headings` | A heading that counts the page or names its own section instead of claiming anything |
| `run_fixtures` | A regression in `check_artifact` or `check_headings`, across eighteen recorded cases |

Tracing a figure to a source is a lookup, not a judgement, which is why a script does it and not a
reader who is also trying to be thorough about six other things.

A check that cannot run is not a check that passed. `check_artifact` reports **not run** as its own
outcome and stops the artifact the same way a failure does.

## What is in here

```
skills/simply/            the run. references/ holds the pipeline, the angles and the house rules
skills/compass/           the intake
skills/flatten/           the flattener, and what L1 means
skills/plain/             language filter, plainlint.py, textlib.py
skills/plain-strategy/    substance filter, stratlint.py
skills/stop-slop/         de-slop filter
skills/humanizer/         the last pass, so it reads like a person
skills/red-team/          the attack angle
scripts/                  the three checks
design/DESIGN.md          two colours, one column, print-clean, six figures
templates/                artifact.html, reasoning.html, figures.html
tests/                    eighteen fixtures and their expected verdicts
material/<client>/        input, plus that client's compass.md. Git-ignored
runs/<slug>/<stamp>/      output. Git-ignored
```

Everything a human edits is markdown. Every normative rule has one owner file, listed in `CLAUDE.md`.

## Install

```
/plugin marketplace add limelights-amsterdam/simply-strategy
/plugin install simply-strategy
```

Python 3 for the scripts. Nothing else, and nothing is fetched at run time.

## What it is not for

Writing the strategy. This distils one that already exists.
