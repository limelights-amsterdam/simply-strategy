---
name: plain
description: Write and speak in plain language, based on ASD-STE100 Simplified Technical English, Plain English and the Google developer documentation style guide. Two jobs - (1) a conversation mode that keeps explanations short and scannable and closes every answer with a status table plus next steps, and (2) a rewrite tool for existing text such as READMEs, documentation, error messages, release notes, mail, quotes and manuals. Use this skill as soon as the user types /plain or "plain". Use it for requests like "explain this simply", "talk normally to me", "write this so people understand it", "strip the jargon", "make this shorter", "this sounds like AI", "this is too woolly", "summarise in a table", or for the terms plain language, plain English, B1 reading level, controlled language, Simplified Technical English or ASD-STE100. Use it when the user complains that a text is vague, markety or unreadable, even when the word plain never appears.
---

# Plain

Unclear text is nearly always ambiguous text. The reader has to guess what you meant. This skill
removes the ambiguity with rules you can check, not with a feel for style.

The rules come from three sources that cover each other's gaps. ASD-STE100, the aerospace standard,
gives the hard limits: sentence length, one name per thing, active voice, no semicolons. Plain
English gives concreteness: what the reader actually has to do. The Google developer style guide
gives the tone. That last one is not decoration. ASD-STE100 alone makes text clear *and* robotic,
because it was built for repair manuals rather than conversation.

## Two jobs

**Conversation mode.** The user wants you to talk like this. Apply the rules to your own answers and
close with tables. The mode stays on for the rest of the conversation.

**Rewrite.** The user hands you a text. Rewrite it and show what changed. Throw nothing away: the
difference between what you cut and what you lose is the whole task.

When in doubt: if a text or file is attached, it is a rewrite. Otherwise it is conversation mode.

## Two modes

**Normal** for explanation, READMEs, mail, status updates and conversation. Max 25 words per
sentence, averaging under 15. Second person. Contractions are fine.

**Strict** for instructions, procedures, error messages, API docs and warnings — anywhere misreading
costs money or safety. Max 20 words in an instruction and 25 in description, one instruction per
sentence, imperative, no semicolons, no em dashes. See
[references/strict-mode.md](references/strict-mode.md).

When in doubt: normal. Strict is a torque wrench. You use it on a bolt, not on everything.

## The seven patterns

Vague text nearly always matches one of seven named patterns. Walk them before you send anything.

1. **Synonym rotation** — the same thing gets three names in one paragraph
2. **Stacked hedging** — auxiliaries pile up until nothing happens
3. **Frozen verbs** — a verb disguised as a noun, with an empty verb in front
4. **Marketing adjectives** — words that claim quality instead of showing it
5. **Run-on sentences** — four ideas joined by dashes where four sentences belonged
6. **Office speak** — words that sound like work but point at nothing
7. **Abstract instruction** — correct, but nobody can tell what to do

Each one with examples and the fix, plus the tone rules that keep the result from reading like a
manual: [references/patterns.md](references/patterns.md).

The single most important tone rule: **vary your sentence length.** The limit is a ceiling, not a
target. Every sentence at 18 words reads like a metronome. Put a four-word sentence next to a
twenty-word one. That is how you hear a person.

## Close with tables

After a long explanation the reader wants two things: where it stands, and what now. Use a table for
three or more points, or two or more next steps. Below that a table is noise.

Status values: ✅ done · ⚠️ watch · ❌ failed · ⏳ running · ⏭️ skipped

The table has to be honest. A status table that is all green is worse than no table, because the
reader stops looking for themselves. Formats in
[references/tables.md](references/tables.md).

## Check yourself

You do not improve text by banning words. In one test a banned-word list improved a text by 3
percent. A complete rule system improved the same text by 74 percent.

```bash
python3 scripts/plainlint.py text.md --lang en --max-sentence 15
python3 scripts/plainlint.py text.md --mode strict --lang en
```

The linter counts sentence length, semicolons, passive, marketing words, frozen verbs, office speak
and synonym rotation, and returns weighted findings per 100 words. Under 1.5 is clean, over 8 is a
lot of noise. Run it on longer text. For short answers, walk the seven patterns in your head.

It cannot tell mention from use. If you are discussing these words, wrap that part in
`<!-- plainlint-ignore-start -->` and `<!-- plainlint-ignore-end -->`.

What it cannot do is judge whether a sentence is true or useful. An empty paragraph becomes a tidy,
readable empty paragraph. If you notice you are only polishing form, say so instead of polishing on.

## Where not to use this

For text where invisible clarity is the point: documentation, instructions, error messages, status
updates, explanation.

Not for text that needs a voice. Posts, ads, brand stories and landing pages go flat here. That is a
torque wrench on a poem. If the user asks anyway, do it, and say once that the text becomes more
neutral.

## Going deeper

- [references/patterns.md](references/patterns.md) — the seven patterns in full, plus the tone rules
- [references/slop-patterns.md](references/slop-patterns.md) — replacement lists: marketing words,
  office speak, frozen verbs, hedges, with an alternative per word
- [references/strict-mode.md](references/strict-mode.md) — the ASD-STE100 rules that matter, plus the
  format for warnings and safety instructions
- [references/tables.md](references/tables.md) — the closing table formats
