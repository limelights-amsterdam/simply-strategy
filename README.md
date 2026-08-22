# Simply Strategy

Point it at a folder of strategy documents. Get back one page a board reads in four minutes.

```
/kompas ./material/acme/    once per client, drafts five fields from their own material
/simply ./material/acme/    no questions, about 25 minutes. Watch it with /workflows
```

Out comes `simple-strategy-artifact.html`. Black and white, big type, very few words, prints on any
machine in the room. Next to it `reasoning.html`, which shows what it read, what it threw away, and
where it is unsure.

---

## Why this exists

There is a plugin called `eli5` whose entire instruction is one sentence: explain this to someone who
knows nothing, using big pictures and few words. Its own example is `/eli5 how does DNS work`.

That example is why it works, and it is worth being precise about why.

**DNS has a ground truth.** It does one thing, in one way, and that way does not depend on who is
asking or who signed off on it. When you simplify it, the worst that happens is that you get it
wrong, and someone who knows DNS can point at the sentence and say no, that is not what happens. The
simplification is safe because there is something underneath it to be checked against.

**A strategy document usually has no ground truth.** It is not a description of how something works.
It is a set of claims about what an organisation intends to do, and a good number of those claims
were left unresolved on purpose, because vagueness is how a document gets signed by six people who
disagree. "We will strengthen our position in the market" is not a fact that has been badly
explained. It is a sentence that was written so that the person who wants to buy a competitor and the
person who wants to cut costs can both nod at it.

Now flatten that sentence. You get something like *we are going to win more customers.* Short, active,
concrete, and a ten-year-old follows it. It is also a decision that nobody made. Simplifying did not
reveal the meaning, because there was no meaning to reveal. It manufactured one, and put it on a page
in confident type where it will get quoted back in a meeting.

That is the failure this exists to prevent. Not a bad summary. A **beautifully simple lie**: short
sentences, big type, a decisive tone, and underneath it the same unmade decision, now harder to spot
because it reads so well.

So this is `eli5` with the check that has to happen first. Four angles read the material and test
whether there is a decision in it at all, before anything is simplified. Three reviewers then check
that the simplification stayed true to what the angles found. Every number on the page traces back to
a document and a page, and a number it cannot trace comes out as `[TO FILL: what is needed]` rather
than as a guess.

When the material genuinely contains no decision, the page says so. That is not the run failing.
That is the most useful thing it can tell you, and it is the one answer a summariser can never give,
because a summary of an empty document is a shorter empty document.

It is also not a summariser in the ordinary sense. A summary makes a document shorter. This makes it
understandable, which is a different job and usually a harder one. Sections often get longer where
the original skipped a step.

## Who it is for, and the bar it is held to

The page is written for the board. That is the audience.

The bar is not the same as the audience: anyone in a ten-thousand-person company should be able to
follow it. Not because they will all read it, but because a sentence a new starter has to read twice
is a sentence the CFO will also read twice, in a room, out loud, with an opinion.

That is also why every claim carries a document and a page number. Seniority changes what a reader
already knows. It does not change what makes a page worth trusting.

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
most uncomfortable line in `reasoning.html`.

## The Kompas

The intake asks what you refuse before it asks what you want.

A goal list can only tell you things you already knew to ask about. An anti-vision and a boundary let
an advisor notice something you never wrote a goal for. Describe a Tuesday five years out where this
strategy quietly failed, and name what you will not give up whatever happens, and a reader can now
say *this plan walks toward precisely that* or *this plan spends the thing you said you keep.*

Five fields, all optional. Fill it by pointing at their own deck and correcting the draft, or by
answering five questions. A half-filled Kompas still runs, and the artifact names what was missing.

It is written to `material/<client>/kompas.md`, next to the documents it describes, not to the
project root. It is client material, it travels with the folder it belongs to, and two clients can
be set up side by side.

## The seven steps

Linear where a step needs everything before it, parallel where it does not.

| # | Step | Shape | Writes | Job |
|---|---|---|---|---|
| 1 | Spec Agent | linear | `01-spec.md` | Every file: what it is, its date, who owns it. And what the material references but does not contain |
| 2 | Panel | 4 parallel | `02-*.md` | substance · contradiction · kompas · red team |
| 3 | Plan Agent | linear | `03-plan.md` | Four angles into one. Tension check, then exactly three must-solve |
| 4 | Flattener | linear | `04-plain.md` | L1 |
| 5 | Reviewers | 3 parallel | `05-*.md` | Still true? Actually simple? Anything invented? |
| 6 | Review Coordinator | linear | `05-verdict.md` | Consolidates must-fix and applies it. One round |
| 7 | Artifact Agent | linear | two HTML pages | Renders, then verifies its own output |

Ten agents. Two fan-outs, five single minds, one repair round, no loops.

The angles are blind to each other on purpose. That is what makes step 3's **tension check** mean
something: if the four come back agreeing, an angle did not bite, and the Plan Agent sends that one
back to write from its own blind spot rather than from consensus. Four agents nodding politely is
worse than one agent, because it reads like confirmation.

## The rules it will not break

- **Exactly three must-solve items.** A model that may choose, doesn't. A model with three seats has
  to weigh.
- **Two reviewers calling something fatal stops it shipping.** One critic is an opinion, two is a
  signal.
- **It never invents a number.** An unknown figure, owner or date comes out as `[TO FILL: …]`,
  including dates dressed up as periods. A board can act on a flagged gap. It cannot act on a
  fabricated one.
- **Every claim carries a pointer.** No pointer, no claim. Your own reasoning is allowed and often
  the most useful thing in the run, but it is labelled as reasoning rather than dressed as a finding.
- **Nothing is softened.** If two documents disagree, the page says they disagree and names both.
- **The "where I'm unsure" section is never empty.** A run that discarded nothing is a pass-through,
  not a process.
- **Unanswered is not absent.** A section the material cannot answer says so in a full sentence. It
  is never dropped, because a missing section reads as a complete answer.

## It checks its own work

Rendering is the only step nothing downstream would catch, so it verifies itself:

```
python3 scripts/check_artifact.py runs/<slug>/
```

Thirteen checks: six sections present, no unfilled slots, nothing loaded over the network, exactly
three must-solve items, every one with a source pointer, every sentence under 15 words, no silently
empty section, every `[TO FILL]` describing what is needed, no em dashes, and a reasoning log whose
"what it threw away" and "where it is unsure" are not empty. Exit code 1 and it does not ship.

Checks a script can make are made by a script. The reviewers spend their judgement on what a script
cannot see: whether an abstraction is still an abstraction, whether a number has a real comparison,
and whether a sentence got shorter by losing meaning.

The two language linters run on the flattened markdown:

```
python3 skills/plain/scripts/plainlint.py runs/<slug>/04-plain.md --mode strict
python3 skills/plain-strategy/scripts/stratlint.py runs/<slug>/04-plain.md
```

Under 1.5 weighted findings per 100 words is clean.

## What is in here

```
workflows/simply.js         the run. ~70 lines of wiring, no strategy content
skills/simply/              what the run's agents read
  references/house-rules.md   prepended to every agent. The filter and the unbreakable rules
  references/pipeline.md      what each step gets, must produce, and how it fails
  references/angles.md        the four panel briefs
  references/output-structure.md  the four visual slots and the two files
skills/kompas/              the intake. Read a deck, or ask five questions
skills/simplify/            the flattener. references/output.md defines the six sections
skills/plain/               language filter + plainlint.py
skills/plain-strategy/      substance filter + stratlint.py
skills/stop-slop/           de-slop filter
skills/red-team/            the attack angle
scripts/check_artifact.py   deterministic verification of the rendered output
design/DESIGN.md            two colours, one column, print-clean
templates/                  artifact.html, reasoning.html
material/<client>/          input, plus that client's kompas.md. Git-ignored
runs/<slug>/                output. Git-ignored
```

Everything a human edits is markdown. `simply.js` names files and agents and holds nothing else, so
changing how the red team thinks means editing a `.md`, never the script.

Every normative rule has exactly one owner file. The table in `CLAUDE.md` says which.

## Install

```
/plugin marketplace add limelights-amsterdam/simply-strategy
/plugin install simply-strategy
```

Needs Claude Code 2.1.154 or later for the workflow runtime. Python 3 for the three scripts. Nothing
else, and nothing is fetched at run time.

## What it is not for

Writing the strategy. This flattens one that already exists. If the folder contains no decision, the
artifact says so, and that is the most useful thing it can return.
