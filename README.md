# Simply Strategy

Point it at a folder of strategy documents. Get back one page a CEO reads in four minutes.

```
/kompas ./deck/         once — drafts five fields from their own material, you correct it
/simply ./material/     no questions, about 25 minutes. Watch it with /workflows
```

Out comes `simple-strategy-artifact.html`: black and white, big pictures, very few words. Plus
`reasoning.html`, which shows what it read, what it threw away, and where it is unsure.

## Why it is not a summariser

A summary makes a document shorter. This makes it understandable, which is a different job and
usually a harder one.

Flattening a strategy document without checking it first gives you a beautifully simple lie. Most
strategy documents are vague on purpose. So four angles read the material before anything gets
simplified, three reviewers check that the simplification stayed true, and every number on the page
traces back to a document and a page. A number it cannot trace comes out as `[TO FILL: …]`.

## Flatten levels

Every document sits at a level. Most ship at L5 while the room believes they are at L2.

| Level | Name | Test |
|---|---|---|
| **L5** | Board memo | As written. Jargon intact |
| **L4** | Plain | Jargon gone. Sentences under 25 words |
| **L3** | Choice | A decision is visible. What we stop doing is named |
| **L2** | Picture | Every abstraction is a person doing something. Every number has a comparison |
| **L1** | Child | Every sentence under 15 words. A ten-year-old repeats it back |

The artifact ships at L1. The run reports the level the input came in at, which is often the most
uncomfortable line in `reasoning.html`.

## The seven steps

| # | Step | Shape | Produces |
|---|---|---|---|
| 1 | Spec Agent | linear | What is in the folder, and the question |
| 2 | Panel | 4 parallel | substance · contradiction · kompas · red team |
| 3 | Plan Agent | linear | Four angles into one. Exactly three must-solve |
| 4 | Flattener | linear | L1 |
| 5 | Reviewers | 3 parallel | Still true? Actually simple? Anything invented? |
| 6 | Review Coordinator | linear | Consolidates must-fix and applies it. One round |
| 7 | Artifact Agent | linear | The two HTML pages |

Ten agents. Two fan-outs, five single minds, one repair round, no loops.

## The rules it will not break

- **Exactly three must-solve items.** A model that may choose, doesn't. A model with three seats has
  to weigh.
- **Two reviewers calling something fatal stops it shipping.** One critic is an opinion, two is a
  signal.
- **It never invents a number.** Unknown figure, owner or date comes out as `[TO FILL: …]`. A board
  can act on a flagged gap. It cannot act on a fabricated one.
- **Every claim carries a pointer** — document name and page.
- **The "where I'm unsure" section is never empty.** A thinking process with nothing discarded is a
  pass-through, not a process.

## The Kompas

The intake asks what you refuse before it asks what you want. A goal list can only tell you things
you already knew to ask about. An anti-vision and a boundary let an advisor notice something you
never wrote a goal for.

Five fields, all optional. A half-filled Kompas still runs, and the artifact names what was missing.

## What it is not for

Writing the strategy. This flattens one that already exists. If the folder contains no decision, the
artifact says so, and that is the most useful thing it can return.

## Install

```
/plugin marketplace add <this repo>
/plugin install simply-strategy
```

Needs Claude Code 2.1.154 or later for the workflow runtime.
