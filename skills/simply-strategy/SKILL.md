---
name: simply-strategy
description: Distil a folder of strategy documents into one plain-language HTML page that anyone can read, with every figure traced to its source. You run it yourself, in order - fill the five-field intake if the folder has none, inventory the folder, read it from four angles, rank to exactly three must-solve items and write the argument, flatten to child-level language, verify every figure with three scripts, render a black-and-white page and check it. Use when the user types /simply-strategy, points at a folder or deck of strategy material and wants something readable out of it, or says simplify this, flatten this, distil these documents, make one page out of this, explain this strategy to a ten-year-old, or what do all these documents actually say together.
allowed-tools: Bash(python3 *), Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Simplify

Distilling, not shortening. A folder holds a decision inside a great deal of context. The job is to
boil it down until what is being decided is visible to anyone, and to bring the context down with
it: every figure traces to a source, and nothing is added on the way.

## You run this yourself, in order

One intake and six steps, one after another, each writing a file. **No subagents.** Nothing is held
in memory between steps, so the files are the state and you can stop and resume at any of them.

Each step sees everything the last one wrote. That is what makes the argument hold together and the
figures trace, and it is also why agreement between the four angles in step 2 is not evidence: they
are not independent. Weight a finding by what it rests on, not by how many passes repeat it.

**The one number to watch is the pointers.** Working alone, it is easy to write a good sentence and
forget where it came from. A distillation that drops what a claim rests on is a shorter document.
`check_facts.py` counts them in step 5.

## The steps

| # | Step | Writes |
|---|---|---|
| 0 | Fill the Compass, only if the folder has no `compass.md` yet | `<material>/compass.md` |
| 1 | Inventory the folder, and what it names but does not contain | `01-spec.md` |
| 2 | Read it from four angles, one pass each | `02-angles.md` |
| 3 | Rank to exactly three, and **write the argument** | `03-plan.md` |
| 4 | Flatten to L1, headings from the argument | `04-plain.md` |
| 5 | Run three scripts, then check both fidelity hops | `05-verdict.md` |
| 6 | Render, then check the rendered page | two HTML files |

What each one gets, must produce, and how it fails: [references/pipeline.md](references/pipeline.md).
That file owns the steps. Do not restate them here.

Output goes to `runs/<slug>/<stamp>/`. Get the stamp before you start, so a second run does not
overwrite the first:

```bash
python3 -c "import datetime; print(datetime.datetime.now().strftime('%Y-%m-%d-%H%M'))"
```

## Where `{root}` is

Commands in the references spell `{root}/`. `{root}` is the folder this `SKILL.md` sits in:
`${CLAUDE_PLUGIN_ROOT}/skills/simply-strategy` when this runs as an installed plugin, `skills/simply-strategy` in a
clone of the repository. It is never the folder the user is working in, so a bare `scripts/...`
resolves to nothing. Resolve it once at the start and use it in every command. Everything the run
reads or runs sits under it:

```
references/   the briefs: house rules, pipeline, angles, output structure, the Compass,
              flatten/ substance/ language/
scripts/      the three checks and the two linters
assets/       artifact.html, reasoning.html, figures.html
```

## What makes it more than six prompts

**The filter runs on every step.** [references/house-rules.md](references/house-rules.md) is the
first thing to read and it applies to everything you write.

**Step 3 owes an argument, not a sort.** A governing thought the whole page is evidence for, and the
through-line as one claim per section. The flattener turns that into the headings. Without it the
page is a well-ranked list, which is what it was before this step existed.

**Step 5 is three scripts and one judgement.** Tracing a figure to a source is a lookup, so
`check_facts.py` does it. What is left for you is whether anything was lost between the plan and
the page, which no script can see.

**Three seats.** Exactly three must-solve items. A model that may choose, doesn't.

**No invented numbers.** An unknown figure, owner or date is `[TO FILL: what is needed]`. Your own
arithmetic on their figures is allowed and must say so on the same line.

## What ships

`simple-strategy-artifact.html`, six sections, black and white, prints clean.
`reasoning.html`, what you read, what you set aside, where you are unsure.

Both structures: [references/output-structure.md](references/output-structure.md).

## What it is not for

Writing the strategy. This distils one that exists. If the folder contains no decision, the page says
so, and that is the most useful thing it can return.
