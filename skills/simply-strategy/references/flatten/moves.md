# Flatten: the levels and the seven moves

Step 4 loads this file first.

Flatten a strategy until a ten-year-old can repeat it back. That is a different job from summarising.
A summary makes a document shorter. This makes it understandable, and it usually gets longer in the
places that were skipped.

The danger is the whole reason this step has rules. **Flattening a vague document produces a
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

## The seven moves

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
   page of one-line paragraphs reads like a telegram, and it is the failure mode this step falls
   into when it is trying hardest. Sentences that serve one thought sit together.
7. **Stay inside the budget.** [output.md](output.md) owns it. A finding that
   needs more room belongs in the reasoning log, not in smaller type.

Worked pairs on real strategy language: [before-after.md](before-after.md).
Read that file before you flatten anything, the move is easier to copy than to describe.

## What you may not do

**Never drop a claim to make a sentence shorter.** If a claim will not fit, it gets its own
sentence. Losing content is the failure mode of this whole step.

The rules every step shares, never invent a number, never soften a conflict, never add confidence
the source did not have, are owned by `references/house-rules.md` and apply here
unchanged.

## Output

Six sections, defined in [output.md](output.md), with what each may leave
unanswered and the closing line that names the level in and the level out.

## Check yourself

```bash
python3 {root}/scripts/plainlint.py 04-plain.md --max-sentence 15
python3 {root}/scripts/stratlint.py 04-plain.md
```

`{root}` is the skill folder, see `SKILL.md`. Clean is under 1.5 for plainlint and
under 1.0 for stratlint. The bands differ because the denominators do: plainlint counts the prose
it scanned, stratlint counts the whole document. `--max-sentence 15` is the claim the whole skill
rests on, so it is the flag that checks it.

## Rules and further reading

- [rules.md](rules.md). The first five moves in full, with the failure mode of each, and
  the page's vocabulary: one name per thing, none of the run's own words, no fragments
- [before-after.md](before-after.md). Worked pairs. Read this one first
- [output.md](output.md). The six sections, and what may be left unanswered
