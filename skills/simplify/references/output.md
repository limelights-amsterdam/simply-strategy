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

## Closing line

End with the flatten level the input came in at and the level it went out at. Usually `L5 → L1`.
It is the most uncomfortable line in the job and it belongs on the page.
