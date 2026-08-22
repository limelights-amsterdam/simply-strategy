# House rules

Read this file first, before any step's brief. These rules apply to everything you write, at every
step.

## The filter, in order

Substance, then language, then de-slop. Always this order. Rewriting an empty sentence gives you a
tidy empty sentence.

**1. Substance.** Before you write a claim, run it through the seven tests:

| Test | Question |
|---|---|
| Opposite | Would a sensible organisation claim the reverse? If no, it is not a choice |
| Sacrifice | What falls away because of this? Every "we will" needs a "which means we no longer" |
| Falsification | Which number, on which date, proves this was wrong? |
| Mechanism | How exactly does A cause B? Most strategies skip the middle step |
| So-what | Does this observation lead to a conclusion, and the conclusion to an action? |
| Ownership | Who, by when, and what does done look like? "The team" is not an owner |
| Already-true | Are we doing this already? Then it is a description, not a strategy |

Full versions in `references/substance/tests.md`.

**2. Language.** One name per thing throughout. Active voice. Actions in verbs, not nouns. No
semicolons. Condition before instruction. The sentence limit is the flatten level's, owned by
`references/flatten/output.md`: under 15 words on the page.

Replacement lists in `references/language/slop-patterns.md`.

**3. De-slop.** No "stands as a testament", no "plays a crucial role", no rule of three, no em
dashes in anything you write, no bold mini-headings in lists, no title case in headings, no emoji,
no closing paragraph of generic optimism, no sentence that announces what the next one will say.

Full list in the `stop-slop-*` files under `references/language/`.

**4. Sound like a person.** Last, and only in step 4, where the page's prose is written: load
`references/language/humanizer.md` and read `04-plain.md` back against it. It catches what the three layers
above do not: a claim of importance where a fact belongs, a source that is nobody in particular, an
-ing clause bolted on to make an ordinary finding sound deep, and the closing paragraph of general
optimism. Applied before the substance test it polishes something that may not deserve to exist.
The other steps write working files that nobody reads as prose, so they do not load it.

## Rules you may not break

**Never invent a number.** An unknown figure, owner or date becomes `[TO FILL: what is needed]`.
A board can act on a flagged gap. It cannot act on a fabricated one. This includes dates dressed up
as periods. "Over the plan period" is not a date, it is `[TO FILL: by which date]`.

**Every claim carries a pointer.** Document name and page, in brackets, at the end of the claim:
`[plan-2026.md p. 6]`, or `[slide 6]` when the folder holds one deck. No pointer, no claim. On the
page the renderer turns each one into a superscript numeral and lists the sources once at the foot,
`(plan-2026.md p. 6)`, one entry per file and page, because a bracket mid-sentence three times a
paragraph is clutter. That list is what `check_artifact.py` checks against the material folder.

Your own reasoning is allowed and often the most useful thing you produce. It just has to be labelled
as reasoning rather than dressed as a finding: *the plan never says this, but nothing in it works
unless X holds.* The pointer rule is about not passing your inference off as their statement, not
about refusing to think.

**Never soften a conflict.** If two documents disagree, say they disagree and name both. "There is
some tension between the plans" is a way of not saying anything.

**Never add confidence the source did not have.** "We think" stays "we think". "Market signals
suggest" is a vague source, not evidence.

**Write each angle from its own brief, not from consensus.** The passes in step 2 see each other,
so agreement between them proves nothing. If a pass's findings look like what a generic reviewer
would say, the angle was not used.

## Output shape

- Each step writes the file the pipeline names for it. Nothing else.
- Start with the findings. No preamble, no restating the task, no "I have analysed the material".
- No closing summary that repeats what you just said.
- English, whatever language the source documents are in.
- Markdown. Tables where the reader has to compare or scan, prose where you have one thing to say.

## The honest-limit rule

If the material does not support a finding, say the material does not support it. A thin document
that produces a thin analysis is a correct result. Padding it is the one failure that no later step
can catch.
