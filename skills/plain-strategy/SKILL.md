---
name: plain-strategy
description: Write and review strategy in plain language, and test whether it contains an actual decision. Combines plain language (ASD-STE100 Simplified Technical English, Plain English, Google developer style) with seven substance tests drawn from Roger Martin, Richard Rumelt and Barbara Minto. Use this skill as soon as the user types /plain-strategy, or when writing, rewriting or reviewing a strategy document, positioning story, annual plan, vision paper, board memo, leadership deck, investor update, OKR set, market analysis or advisory report. Use it for questions like "is there actually a choice in here", "this is too vague", "what are we really saying", "review this strategy doc", "make this concrete", "strip out the consultant jargon", "is this a strategy or a wish list", "what's the so-what here". Trigger it whenever someone shares strategy text full of synergies, north star, value creation, holistic approach or transformation journey, even when the word plain never appears.
---

# Plain Strategy

Vague strategy is not mainly badly written. It is empty. That is a different problem, and the more expensive of the two.

*"We will become the leading partner for our clients."* That sentence is fine: short, active, no jargon. And it says nothing, because no sane organisation would choose the opposite.

So this skill does two things in order. First the substance test: is there a choice here. Then the language test: is that choice readable. In that order, because rewriting an empty sentence gives you a tidy empty sentence.

## Two jobs

**Job 1 — Review.** Someone hands you a strategy document. Run the seven tests, report each finding with its location and what is wrong with it, and give a verdict. Do not rewrite the whole thing unasked.

**Job 2 — Write.** Someone wants a strategy document. Apply the tests as you write, and deliver in the format below.

When in doubt: if an existing document is attached, it is job 1.

Answer in the language the user writes in. The tests and the format work the same in either language.

## The seven substance tests

Run them in this order. The first three are the heaviest, and most documents die there.

| # | Test | Question |
|---|---|---|
| 1 | **Opposite** | Would a sensible organisation claim the reverse? If not, it is a platitude |
| 2 | **Sacrifice** | Every "we will" needs a "which means we no longer". What falls away? |
| 3 | **Falsification** | Which number, on which date, proves this was wrong? |
| 4 | **Mechanism** | How exactly does A cause B? Most strategies skip the middle step |
| 5 | **So-what** | Does the fact lead to a conclusion, and the conclusion to an action? |
| 6 | **Ownership** | Who, by when, and what does done look like? "The team" is not an owner |
| 7 | **Already-true** | Are you doing this already? Then it is a description, not a strategy |

Each test with its origin, more examples and its follow-up questions:
[references/tests.md](references/tests.md). Read that file when reviewing.

## Jargon that hides emptiness

These words sound like a decision and are not. Full replacement lists live in `references/strategy-jargon.md`. The short version:

<!-- stratlint-ignore-start -->

**English:** synergies · leverage our core competencies · strategic alignment · value creation · holistic approach · north star · double down · unlock value · operating model · transformation journey · best-in-class · thought leadership · paradigm shift · at scale · low-hanging fruit · table stakes · boil the ocean · move the needle · win-win · going forward

**Dutch:** synergie · integrale aanpak · stip op de horizon · handelingsperspectief · randvoorwaardelijk · kaderstellend · toekomstbestendig · strategische verankering · ontzorgen · verbinden · versnellen · wendbaar · ecosysteem · laaghangend fruit · quick wins · in de keten · transitie · transformatie · opschalen · borgen · draagvlak

<!-- stratlint-ignore-end -->

Do not replace these with a synonym. Replace them with the fact, the number or the action the word stood in for. If you cannot name it, there was no content underneath.

## The language layer

Once the substance holds, the ordinary plain-language rules apply. Briefly:

- One name per thing, throughout the document.
- At most 25 words per sentence, averaging under 15. Vary the length, or it reads like a metronome.
- Active voice. Make it visible who acts, because in strategy that is often the information itself.
- Actions live in verbs, not in nouns. "We decide", not "the decision-making process".
- No semicolons, at most one em dash per page.
- No words that claim quality without evidence.
- Answer first, support after. The reader of a board memo reads the first paragraph and sometimes nothing else.

If the `plain` skill is also installed, use its references and linter for this layer. Otherwise the list above is enough.

## The delivery format

Answer first: what we will do, why now, and what it costs. Six sentences at most. Then the tables.

The most important one is **the assumptions this rests on**, with what must be true, how we test it,
and when we know. A strategy is a bet with a reason, and that is where the bet is written down. Put
in the assumptions that could overturn the decision, not the safe ones.

For a review, deliver a findings table instead, and close with one line placing the document: is this
a strategy, a plan, or a wish? That distinction helps more than a score.

All formats: [references/format.md](references/format.md).

## Check yourself

A linter ships with this skill. It counts the mechanical part: strategy jargon, empty claims, and whether the document contains a choice, a number, an owner and a date at all.

```bash
python3 scripts/stratlint.py strategy.md
python3 scripts/stratlint.py strategy.md --lang nl
python3 scripts/stratlint.py docs/*.md --fail-over 3.0
```

It also checks structure: is there a "we will not" anywhere, is there a date, is there a name. If those are missing, this is a direction rather than a strategy.

What the linter cannot do: judge whether the choice is smart. It sees that a choice was made, not whether it pointed the right way. That judgement stays with you and the reader.

## Where not to use this

Not on text meant to persuade or sell: external pitch decks, brand stories, campaigns, LinkedIn. Those need a voice and this flattens them. Use the copy and positioning skills for that.

Do use it on anything that has to carry an internal decision: strategy document, annual plan, board memo, investment proposal, OKR set, advisory report.

And the honest limit: this skill makes it visible that nothing is there. It cannot invent something to put in its place. If filling in the tables reveals the choice has not been made yet, say so to the user rather than padding the tables. That is the most useful outcome this tool has.

## Going deeper

- [references/strategy-jargon.md](references/strategy-jargon.md) — Full replacement lists in English and Dutch, with what to write instead of each term. Read this when rewriting.
- [references/tests.md](references/tests.md) — The seven tests in full, with their origin, more examples, and the follow-up questions per test. Read this when reviewing.
- [references/format.md](references/format.md) — Every delivery table, for writing and for review.
- [scripts/stratlint.py](scripts/stratlint.py) — The linter. Run with `--help` for all options.
