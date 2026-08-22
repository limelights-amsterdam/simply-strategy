---
name: simply
description: Turn a folder of strategy documents into one plain-language HTML page a CEO reads in four minutes. Runs seven steps - inventory, a panel of four independent angles, a forced ranking to exactly three must-solve items, a flatten pass to child-level language, three reviewers, one repair round, and a black-and-white artifact. Use when the user types /simply, points at a folder of strategy material and asks for something readable out of it, or says flatten this folder, run the strategy through it, make one page out of these documents, or what do all these documents actually say together.
---

# Simply

One folder in, one page out. The page says what the documents actually decided, in language a
ten-year-old follows, with every number traceable to a source.

It is written for the board. The bar is that anyone in a ten-thousand-person company could follow
it, which is a standard rather than a distribution list. A sentence a new starter reads twice is a
sentence the CFO reads twice too, out loud, in a room, with an opinion.

The whole design rests on one problem: **flattening a vague document produces a beautifully simple
lie.** Most strategy documents are vague on purpose. So four angles check the material before
anything is simplified, and three reviewers check that the simplification stayed true.

## How to run it

The run is a workflow: `workflows/simply.js`. It executes in the background and asks nothing while it
runs. Watch it with `/workflows`.

```
/kompas ./material/<client>/    fills that folder's kompas.md. Once per client, not per run
/simply ./material/<client>/    the run, about 25 minutes
```

If the workflow runtime is unavailable, run the seven steps in `references/pipeline.md` yourself with
subagents, in the same order and with the same file names. The result is the same, the progress
screen is not.

## The seven steps

| # | Step | Shape | Writes |
|---|---|---|---|
| 1 | Spec Agent | linear | `01-spec.md` |
| 2 | Panel — substance · contradict · kompas · attack | 4 parallel | `02-*.md` |
| 3 | Plan Agent | linear | `03-plan.md` |
| 4 | Flattener | linear | `04-plain.md` |
| 5 | Reviewers — true · simple · invented | 3 parallel | `05-*.md` |
| 6 | Review Coordinator | linear | `04-plain.md` revised, `05-verdict.md` |
| 7 | Artifact Agent | linear | the two HTML pages |

Output goes to `runs/<slug>/`. Ten agents, two fan-outs, one repair round, no loops.

Details per step, including how each one fails: [references/pipeline.md](references/pipeline.md).

## What makes it more than four prompts

**Every step reads the filter first.** [references/house-rules.md](references/house-rules.md) is
prepended to every agent. The Flattener compresses, it does not rescue — consultant prose in step 2
gives you tidy consultant prose in step 4.

**The angles are blind to each other.** Independence is what makes step 3's tension check mean
something. If the four come back agreeing, an angle did not bite, and its findings are marked weak.

**Two reviewers, not one.** A finding that two or more reviewers call fatal is decisive. One critic
is an opinion.

**Three seats.** Exactly three must-solve items. A model that may choose, doesn't. Everything else is
demoted in a visible table, never deleted.

**No invented numbers.** An unknown figure, owner or date is `[TO FILL: what is needed]`. A board can
act on a flagged gap.

## What ships

`simple-strategy-artifact.html` — six sections, four fixed visual slots, black and white,
self-contained, prints clean.

`reasoning.html` — what it read, what it threw away, where it is unsure, and whether the tension
check fired. Parts two and three may never be empty.

Both structures: [references/output-structure.md](references/output-structure.md).

Step 7 verifies itself with `scripts/check_artifact.py`, because rendering is the only step nothing
downstream would catch. Exit code 0 or it does not ship.

## What it is not for

Writing the strategy. This flattens one that already exists. If the folder contains no decision, the
artifact says so — and that is the most useful thing it can return.
