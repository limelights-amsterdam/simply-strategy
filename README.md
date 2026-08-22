# Simply Strategy

Point it at a folder of strategy documents. Get back one page a board reads in under six minutes.

```
/simply-strategy:compass ./material/acme/   once per client, drafts five fields from their material
/simply-strategy:simply  ./material/acme/   no questions, about 45 minutes. Watch it with /workflows
```

Out comes `simple-strategy-artifact.html`. Black and white, big type, very few words, prints on any
machine in the room. Next to it `reasoning.html`, which shows what it read, what it threw away, and
where it is unsure.

---

## What it is for

Distilling, not shortening. A folder of strategy documents holds a decision somewhere inside a great
deal of context, and the job is to boil that down until what is actually being decided is visible to
anyone who reads it. Not the leadership team. Anyone.

Two things follow from putting it that way.

**The context comes with it.** A distillation that drops what a claim rests on is just a shorter
document. So every figure on the page traces to a source, every section can show its own working,
and the reasoning log carries the chain in full.

**Nothing is added on the way down.** The one thing that must never happen is a page that reads
clearly and says something the material does not. That is why four angles test the material before
anything is flattened, and why a script traces every number back to the source rather than an agent
being asked to be careful.

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

## The Compass

The intake asks what you refuse before it asks what you want.

A goal list can only tell you things you already knew to ask about. An anti-vision and a boundary let
an advisor notice something you never wrote a goal for. Describe a Tuesday five years out where this
strategy quietly failed, and name what you will not give up whatever happens, and a reader can now
say *this plan walks toward precisely that* or *this plan spends the thing you said you keep.*

Five fields, all optional. Fill it by pointing at their own deck and correcting the draft, or by
answering five questions. A half-filled Compass still runs, and the artifact names what was missing.

It is written to `material/<client>/compass.md`, next to the documents it describes, not to the
project root. It is client material, it travels with the folder it belongs to, and two clients can
be set up side by side.

## The run, phase by phase

Six phases, the same six `/workflows` shows while it runs. Each phase reads files the phases before
it wrote, and writes its own. The numbers on the files are the step numbers in
`skills/simply/references/pipeline.md`. Steps 6 and 7 share the last phase.

```
runs/<slug>/<stamp>/
│
├─ Spec · 1 agent
│    reads   the material folder and its compass.md
│    writes  01-spec.md            every file, its date, its owner. And what the material cites
│                                  but does not contain
│
├─ Panel · 4 agents, in parallel, blind to each other
│    reads   the material, compass.md and 01-spec.md
│    writes  02-substance.md       is there a decision in here at all?
│            02-contradict.md      where do the documents disagree with each other?
│            02-compass.md         does the material walk toward what the client said they want?
│            02-attack.md          what does the world do to this plan? The red team
│
├─ Plan · 1 agent
│    reads   01-spec.md, the four 02 files and compass.md
│    writes  03-plan.md            tension check first, then exactly three must-solve items
│
├─ Flatten · 1 agent
│    reads   03-plan.md
│    writes  04-plain.md           the page in plain language, at level L1
│
├─ Review · 3 agents, in parallel
│    reads   the four 02 files, 03-plan.md and 04-plain.md. `invented` also re-reads the
│            material, because checking that a number traces to a document needs the document
│    writes  05-true.md            did anything get lost between panel, plan and page?
│            05-simple.md          is it actually L1? The linters count, the reviewer judges
│            05-invented.md        does every number trace back to a document?
│
└─ Artifact · 2 agents, one after the other
     coordinate
       reads   the three 05 files and 04-plain.md
       writes  05-verdict.md       what must be fixed. Two reviewers calling it fatal is decisive
               04-plain.md         revised, in one round
     artifact
       reads   04-plain.md for the page. 01-spec.md, the four 02 files, 03-plan.md and
               05-verdict.md for the log. Plus compass.md and the two templates
       writes  simple-strategy-artifact.html    the page
               reasoning.html                   what it read, who found what, what was demoted
                                                and why, and what shipped with a flag
       then runs check_artifact.py on both. Exit 0 or it does not ship

The page carries the finding and the log carries the chain. That is what keeps the page inside its
word budget without the evidence being the thing that gets cut. Nothing is deleted, it moves, and
the log is built from the files the earlier steps already wrote.
```

Every file in that folder is one agent's output, and nothing else writes it. If a run dies, the
last file tells you which step to restart from.

Nine agents. One fan-out, no loops.

The first full run took 43.7 minutes and 1.2M subagent tokens on 100KB of material, with no errors.
A smaller folder is quicker. Most of that time is the four angles each reading everything separately,
which is the part that makes the tension check worth having, so it is not the first thing to trade
away for speed.

The angles are blind to each other on purpose. That is what makes step 3's **tension check** mean
something: if the four come back agreeing, an angle did not bite, and the Plan Agent records its
findings as weak rather than treating agreement as confirmation. Four agents nodding politely is
worse than one agent, because it reads like a second opinion when it is an echo.

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
python3 scripts/check_artifact.py runs/<slug>/<stamp>/
```

It checks the six sections, unfilled slots, anything loading over the network, the three must-solve
items and their source pointers, sentence length, the page's reading time, silently empty sections,
what each `[TO FILL]` says, em dashes, and a reasoning log whose cut list and unsure list carry
something. With `--material` it also checks that every pointer names a file that exists.

A check that scanned nothing reports `not run`, not a tick, and blocks the same way a failure does.
Exit code 1 and it does not ship. The table it prints is the list; this paragraph is not kept in
step with it.

Checks a script can make are made by a script. The reviewers spend their judgement on what a script
cannot see: whether an abstraction is still an abstraction, whether a number has a real comparison,
and whether a sentence got shorter by losing meaning.

The two language linters run on the flattened markdown:

```
python3 skills/plain/scripts/plainlint.py runs/<slug>/<stamp>/04-plain.md --mode strict
python3 skills/plain-strategy/scripts/stratlint.py runs/<slug>/<stamp>/04-plain.md
```

Each linter prints its own verdict band, and the two bands are not the same number. Read the band,
or gate on it with `--fail-over`.

The three commands above are written from a clone of this repo. Installed as a plugin, the scripts
sit under the plugin directory rather than the one you are working in, and the run prefixes them
itself from the root the skill hands it.

## What is in here

Two folders you touch:

```
material/<client>/          input, plus that client's compass.md. Git-ignored
runs/<slug>/<stamp>/        output, one folder per run. Git-ignored. Its files are the phase tree above
```

Everything else is the plugin. `workflows/simply.js` is the run, about 90 lines of wiring with no
strategy content. `skills/` holds what the agents read, one folder per job: `simply/` the run's own
references, `compass/` the intake, `flatten/` the flattener, `plain/` and `plain-strategy/` the two
filters with their linters, `stop-slop/` and `red-team/`. `templates/` and `design/DESIGN.md` decide
how the page looks, `scripts/` verifies it, and `examples/` is a worked run the checker validates.

The full tree, kept current for people working on this, is in `CLAUDE.md`. It is not repeated here,
because two trees drift and one of them is then wrong.

Everything a human edits is markdown. `simply.js` names files and agents and holds nothing else, so
changing how the red team thinks means editing a `.md`, never the script.

Every normative rule has exactly one owner file. The table in `CLAUDE.md` says which.

## Install

```
/plugin marketplace add limelights-amsterdam/simply-strategy
/plugin install simply-strategy@limelights
```

Needs Claude Code 2.1.154 or later for the workflow runtime. Python 3 for the three scripts. Nothing
else, and nothing is fetched at run time.

Steps 5 and 7 shell out to Python, and a background run cannot stop to ask you. The rules to allow
before a long run, and why the skill's own pre-approval is not enough on its own, are in
`skills/simply/SKILL.md`, which owns that.

## What it is not for

Writing the strategy. This flattens one that already exists. If the folder contains no decision, the
artifact says so, and that is the most useful thing it can return.
