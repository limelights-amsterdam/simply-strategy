# The six sections

This file is the single definition of what a flattened strategy contains. The renderer, the
reviewers and the artifact template all read it from here.

Six sections, in this order.

| # | Section | Content | May be unanswered |
|---|---|---|---|
| 1 | **The one sentence** | What this whole thing is actually about | No. If this cannot be written, the job failed |
| 2 | **The three things that must be solved** | Exactly three. Numbered. Not four, not two | No |
| 3 | **What we stop doing** | The sacrifice, per must-solve | Yes |
| 4 | **What has to be true** | The bet: assumption, how we test it, when we know | Yes |
| 5 | **What the documents disagree about** | Named conflicts, both sides quoted | Yes, only when there genuinely are none |
| 6 | **What we do not know** | Every `[TO FILL]`, plus every `[MISSING]` intake field | No. An empty section 6 means something was papered over |

## Unanswered is not absent

Sections 3, 4 and 5 may say the plan does not answer them. They may never be dropped.

Write it as a full sentence, never a dash or a blank:

> The plan does not say what this costs.

A missing section reads as a complete answer. That is the one thing this output must never do,
because the reader has no way to tell the difference between "nothing to report" and "not checked".

## What goes on the page, and what goes behind it

This is the rule that makes the budget reachable. Without it the budget is a
number the writer has to hit by cutting, which means cutting evidence, which is
the one thing that must not go.

**The page carries the finding. The reasoning log carries the chain that
supports it.** Nothing is deleted; it moves.

| Section | On the page | In `reasoning.html` |
|---|---|---|
| 1 · The one sentence | The sentence, and the figure under it | The inventory it was drawn from |
| 2 · The three must-solves | The statement, one figure, one source pointer, one line on what it costs to leave it | The quotes, the arithmetic, which angle found it, and what was demoted around it |
| 3 · What we stop doing | Four stops and four starts, the ones that block a decision | All of them, with a pointer each |
| 4 · What has to be true | One figure, and the single heaviest bet in prose | Every bet, with what would test it and when |
| 5 · What the documents disagree about | The costliest two or three, as figures | All of them, with both sides quoted |
| 6 · What we do not know | The count, and the ones that block a decision on their own | Every gap, and every document named in the material but absent from the folder |

A reader who accepts the page stops there. A reader who does not goes to the
reasoning log, which is where a hostile question is answered anyway. Putting the
evidence on the page serves neither of them: it slows the first reader down and
it is not where the second one looks.

The test is not "did it fit". It is: **can a claim on the page be traced?** If a
line on the page has no matching entry in the log, it was cut rather than moved,
and that is the failure this rule exists to prevent.

## The headings carry the argument

The six sections have fixed content. Their **headings do not**: each one states the claim that
section proves, taken from `## The argument` in `03-plan.md`.

A heading that names the section is a label, and a page of labels is a table of contents:

| Label, what not to write | Claim, what to write |
|---|---|
| Three things must be solved | Not one of the three has a number you can act on |
| Nine pairs cannot both be true | Where the deck disagrees with itself, it is about money |
| Eight unknowns stop a decision | Four questions have to be answered before anyone decides |

The left column counts the page. The right column says something about the material, which is the
only kind of sentence a reader can disagree with.

`check_headings.py` enforces two of the three properties: a heading may not count the page, and a
number or a name in a heading must appear in the section beneath it. Whether the sequence is any
good is judgement, and step 5 owns it rather than a script.

## The length budget

Correct is not the same as short enough. A page can pass every accuracy check and still take
twice as long to read as it promised, so the budget is part of the output, not a matter of taste:

| Section | Words | Why |
|---|---|---|
| 1 · The one sentence | 150 | The sentence itself, plus the few lines that make it land |
| 2 · The three that must be solved | 350 | About 25 for each statement, about 40 for each piece of evidence |
| 3 · What we stop doing | 200 | |
| 4 · What has to be true | 200 | |
| 5 · What the documents disagree about | 200 | |
| 6 · What we do not know | 100 | A list of gaps, not a discussion of them |
| **Total** | **1200** | About six minutes at 200 words a minute |

`check_artifact.py` fails the run above 1200 words. Change the budget with `--max-words` when a
board genuinely wants more, but change it deliberately rather than drifting into it.

The per-section numbers are not enforced by anything. They are there so that a section carrying a
lot of findings, usually 5 and 6, is a deliberate overrun paid for by an underrun elsewhere rather
than an accident. That is fine as long as somebody chose it.

**The evidence under a must-solve is 40 words.** It is set in caption type, and an essay in caption
type puts the thing a CFO will attack in the smallest text on the page. If a finding needs more than
40 words to stand up, it belongs in `reasoning.html`, which has no budget and is where a hostile
reader goes next.

**Short is not the same as loose.** Sentences under 15 words do not each need their own paragraph.
A section of stacked one-line paragraphs reads like a telegram. Group sentences that belong to one
thought. The limit is on the sentence, not on the paragraph.

## Closing line

End `04-plain.md` with the flatten level the input came in at and the level it went out at.
Usually `L5 → L1`. It is the most uncomfortable line in the job. It goes in the reasoning log,
where `check_artifact.py` looks for it, not on the page: the reader of the page does not know what
an L5 is and does not need to.
