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

## The length budget

Correct is not the same as short enough. The first real run produced a page that passed every
accuracy check and took **eleven minutes to read** against a promise of four. Nothing anywhere
constrained how much went on it.

So the budget is part of the output, not a matter of taste:

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

**The evidence under a must-solve is 40 words.** It is set in caption type, and an essay in caption
type puts the thing a CFO will attack in the smallest text on the page. If a finding needs more than
40 words to stand up, it belongs in `reasoning.html`, which has no budget and is where a hostile
reader goes next.

**Short is not the same as loose.** Sentences under 15 words do not each need their own paragraph.
The first run turned section 1 into twelve stacked one-line paragraphs, which reads like a telegram.
Group sentences that belong to one thought. The limit is on the sentence, not on the paragraph.

## Closing line

End with the flatten level the input came in at and the level it went out at. Usually `L5 → L1`.
It is the most uncomfortable line in the job and it belongs on the page.
