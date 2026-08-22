---
name: simplify
description: Flatten a strategy into language a child follows. Takes a strategic plan, memo, annual plan, board deck or recommendation and rewrites it at flatten level L1 - every sentence under 15 words, every abstraction turned into a person doing something, every number given a comparison. Use when someone says flatten this, simplify this strategy, explain this like I am five, make this understandable for the whole company, what does this actually say, translate this out of consultant language, or asks for the flatten level of a document. Not a summary - a summary makes a document shorter, this makes it understandable.
---

# Simplify

Flatten a strategy until a ten-year-old can repeat it back. That is a different job from summarising.
A summary makes a document shorter. This makes it understandable, and it usually gets longer in the
places that were skipped.

The danger is the whole reason this skill has rules. **Flattening a vague document produces a
beautifully simple lie.** Most strategy documents are vague on purpose, so the substance has to be
checked before the language is touched. If you are handed raw material rather than a checked plan,
say so and check it first.

## Flatten levels

Every document sits at a level. Name the input level before you start, and say it out loud. It is
usually the most uncomfortable line in the whole job.

| Level | Name | Test |
|---|---|---|
| **L5** | Board memo | As written. Jargon intact |
| **L4** | Plain | Jargon gone. Sentences under 25 words |
| **L3** | Choice | A decision is visible. What we stop doing is named |
| **L2** | Picture | Every abstraction is a person doing something. Every number has a comparison |
| **L1** | Child | Every sentence under 15 words. A ten-year-old repeats it back |

Most documents ship at L5 while the room believes they are at L2. You deliver L1.

## The five moves

1. **Every sentence under 15 words.** No exceptions. Split, do not compress.
2. **Every abstract noun becomes a person doing something.** Not "the transformation journey" but
   "we stop selling to shops and start selling online".
3. **Every number gets a comparison.** Not "12% market share" but "of every 100 people who buy this,
   12 buy it from us".
4. **Every recommendation gets its sacrifice.** "We do X" is not finished until "which means we stop
   doing Y" is written next to it.
5. **Nothing survives the opposite test.** Reverse the claim. If no sensible organisation would claim
   the reverse, it is not a choice and it does not go on the page.
6. **Group sentences into paragraphs.** The 15-word limit is on the sentence, not the paragraph. A
   page of one-line paragraphs reads like a telegram, and it is the failure mode this skill falls
   into when it is trying hardest. Sentences that serve one thought sit together.
7. **Stay inside the budget.** The whole page is 1200 words, and the evidence under each must-solve
   is 40. See [references/output.md](references/output.md). A finding that needs more room belongs
   in the reasoning log, not in smaller type.

Worked pairs on real strategy language: [references/before-after.md](references/before-after.md).
Read that file before you flatten anything — the move is easier to copy than to describe.

## What you may not do

- **Never invent a number.** An unknown figure, owner or date becomes `[TO FILL: what is needed]`.
  A board can act on a flagged gap. It cannot act on a fabricated one.
- **Never drop a claim to make a sentence shorter.** If a claim will not fit, it gets its own
  sentence. Losing content is the failure mode of this whole skill.
- **Never soften a conflict.** If two documents disagree, the flattened version says they disagree.
- **Never add confidence the source did not have.** "We think" stays "we think".

## Output

Six sections: the one sentence, the three things that must be solved, what we stop doing, what has to
be true, what the documents disagree about, what we do not know.

Sections 3 to 5 may say the plan does not answer them. They may never be dropped, because a missing
section reads as a complete answer. The definition, with the rule for each:
[references/output.md](references/output.md).

Close with the flatten level the input came in at, and what it went out at.

## Check yourself

```bash
python3 ../plain/scripts/plainlint.py output.md --mode strict --lang en
python3 ../plain-strategy/scripts/stratlint.py output.md --lang en
```

Under 1.5 weighted findings per 100 words is clean. Then count the sentences over 15 words by hand.
The linter will not do that count for you, and it is the claim the whole skill rests on.

## Rules and further reading

- [references/rules.md](references/rules.md) — the five moves in full, with the failure mode of each
- [references/before-after.md](references/before-after.md) — worked pairs. Read this one first
- [references/output.md](references/output.md) — the six sections, and what may be left unanswered
