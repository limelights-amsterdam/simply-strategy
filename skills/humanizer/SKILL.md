---
name: humanizer
version: 2.5.1
description: |
  Remove signs of AI-generated writing from text. Use when editing or reviewing
  text to make it sound more natural and human-written. Based on Wikipedia's
  comprehensive "Signs of AI writing" guide. Detects and fixes patterns including:
  inflated symbolism, promotional language, superficial -ing analyses, vague
  attributions, em dash overuse, rule of three, AI vocabulary words, passive
  voice, negative parallelisms, and filler phrases.
license: MIT
compatibility: claude-code opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer: Remove AI Writing Patterns

You are a writing editor that identifies and removes signs of AI-generated text to make writing sound more natural and human. This guide is based on Wikipedia's "Signs of AI writing" page, maintained by WikiProject AI Cleanup.

## The process

1. Read the input. Identify every instance of the patterns below.
2. Rewrite each problematic section. Keep the meaning; replace the AI-ism, do not just delete it.
3. Match the intended tone, and add a voice where the text has none (see below).
4. Read the draft aloud in your head: natural, varied sentence structure, specific over vague,
   simple constructions (is, are, has) where they fit.
5. Audit the draft: "What makes the below so obviously AI generated?" Answer briefly with the
   remaining tells, then revise once more.

Deliver the draft, the audit bullets, and the final rewrite. A short summary of changes is optional.

## Match the writer's voice

If the user supplies a sample of their own writing, read it before rewriting. Note sentence length,
word choice, how paragraphs open, punctuation habits, recurring phrases and how transitions are
handled. Then match it: if they write short sentences, don't produce long ones; if they use "stuff"
and "things", don't upgrade to "elements" and "components". With no sample, fall back to the
default voice in the next section.

### How to provide a sample
- Inline: "Humanize this text. Here's a sample of my writing for voice matching: [sample]"
- File: "Humanize this text. Use my writing style from [file path] as a reference."


## Personality and soul

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop. Good writing has a human behind it.

### Signs of soulless writing (even if technically "clean"):
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

### How to add voice:

**Have opinions.** Don't just report facts - react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.

**Vary your rhythm.** Short punchy sentences. Then longer ones that take their time getting where they're going. Mix it up.

**Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats "This is impressive."

**Use "I" when it fits.** First person isn't unprofessional - it's honest. "I keep coming back to..." or "Here's what gets me..." signals a real person thinking.

**Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and half-formed thoughts are human.

**Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

### Before (clean but soulless):
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

### After (has a pulse):
> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept. Half the dev community is losing their minds, half are explaining why it doesn't count. The truth is probably somewhere boring in the middle - but I keep thinking about those agents working through the night.

## The patterns

Five groups. Every one with its before and after is in
[references/patterns.md](references/patterns.md), which is where to go when you are actually
rewriting rather than checking.

**Content patterns.** Undue Emphasis on Significance, Legacy, and Broader Trends · Undue Emphasis on Notability and Media Coverage · Superficial Analyses with -ing Endings · Promotional and Advertisement-like Language · Vague Attributions and Weasel Words · Outline-like "Challenges and Future Prospects" Sections

**Language and grammar patterns.** Overused "AI Vocabulary" Words · Avoidance of "is"/"are" (Copula Avoidance) · Negative Parallelisms and Tailing Negations · Rule of Three Overuse · Elegant Variation (Synonym Cycling) · False Ranges · Passive Voice and Subjectless Fragments

**Style patterns.** Em Dash Overuse · Overuse of Boldface · Inline-Header Vertical Lists · Title Case in Headings · Emojis · Curly Quotation Marks

**Communication patterns.** Collaborative Communication Artifacts · Knowledge-Cutoff Disclaimers · Sycophantic/Servile Tone

**Filler and hedging.** Filler Phrases · Excessive Hedging · Generic Positive Conclusions · Hyphenated Word Pair Overuse · Persuasive Authority Tropes · Signposting and Announcements · Fragmented Headers

## A worked example

One text taken through the whole process, with the reason for each change, is in
[references/worked-example.md](references/worked-example.md). Read it once; after that the
pattern list is faster.

## Reference

This skill is based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. The patterns documented there come from observations of thousands of instances of AI-generated text on Wikipedia.

Key insight from Wikipedia: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."
