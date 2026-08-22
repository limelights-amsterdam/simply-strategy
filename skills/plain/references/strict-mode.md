# Strict mode — the ASD-STE100 rules that matter

Use strict mode when misreading costs money, time or safety: instructions, procedures, error
messages, warnings, API reference, migration steps, installation guides.

The full standard has 53 rules and a dictionary of 875 approved words. That dictionary is
deliberately not here. Locking the vocabulary is exactly what makes text robotic. The gain sits in
the rules below, and you can walk those without giving your language a personality transplant.

Rule numbers refer to ASD-STE100 Issue 9 (January 2025), so you can look them up.

## The hard limits

| Limit | Rule |
| --- | --- |
| An instruction sentence is 20 words at most | 5.1 |
| A descriptive sentence is 25 words at most | 6.3 |
| A note is 25 words per sentence at most | 5.5 |
| A paragraph is 6 sentences at most | 6.6 |
| A paragraph covers one topic | 6.5 |
| One instruction per sentence, unless two actions happen at once | 5.2 |
| A compound noun is 3 words at most | 2.1 |
| No semicolons | 8.1 |

For counting: a number with a unit, an abbreviation, a proper name, a piece of quoted text and a
hyphenated word each count as one word (8.6, 8.7). Text in brackets counts as one word (8.5). In a
list, a colon works like a full stop (8.4).

The limit is a ceiling, not a target. Sentences that are all the same length read like a metronome.
Vary them.

## The language rules

**One name per thing (1.11).** Pick one term per part, function or action and keep it for the whole
document. This is the rule with the largest payoff. It kills synonym rotation at the source.

**One meaning per word (1.3).** Use a word in one sense within a document. In the standard, *follow*
only means "come after", never "comply with"; for that you use *obey*. Take that discipline for the
words that matter in your text, and record them in a glossary if needed.

**A verb for an action, not a noun (3.7).** *Analyze*, not *perform an analysis*.

**No compound verb constructions (3.4).** No stacks of auxiliaries. Allowed forms: infinitive,
imperative, present, past, future, and past participle used as an adjective (3.2).

**Active (3.6).** In descriptive text, passive is allowed only when the actor is unknown. In
instructions, never.

**Imperative for instructions (5.3).** "Remove the panel." Not "The panel should be removed" and not
"You can now remove the panel".

**No vague verb combinations (9.3).** Name the action itself. *Remove*, not *take off*.

**Article before the noun (4.5).** Use *the*, *a*, *this* or *these* where you can. Telegram style
("Remove panel") looks shorter but costs the reader time.

**Condition before the action.** Put the condition at the start of the sentence: "If the engine is
cold, close the valve." Otherwise someone reads a step that does not apply and has to backtrack.

## Warnings and safety instructions

The standard distinguishes three levels (section 7):

| Level | When |
| --- | --- |
| **Warning** | Risk of injury or death |
| **Caution** | Risk of damage to equipment, data or systems |
| **Note** | Information only, no instruction (5.5) |

When two levels apply at once, use the heavier one (7.1).

Build every safety instruction in two parts:

1. **The command or condition first** (7.2). What the reader must or must not do.
2. **Then the reason** (7.3). Which risk or consequence sits behind it.

- ✅ **Warning:** Do not touch the pipe before the system has cooled. The pipe reaches 180 °C and
  causes severe burns.
- ❌ Due to the high temperatures that can occur in the system, care is advised when handling the pipe.

The reason is not decoration. A reader who knows *why* still complies when the situation differs
slightly from the book.

A note carries information only. Never put an instruction in one — readers skip notes.

## Checklist

- Every instruction is imperative and contains one action.
- No sentence over the limit: 20 words for instructions, 25 for description and notes.
- No paragraph over 6 sentences, and each paragraph covers one topic.
- Every thing has the same name throughout the document.
- Every word that matters has the same meaning throughout the document.
- No semicolons, no em dashes.
- Active, unless the actor is genuinely unknown.
- Actions sit in verbs, not in nouns.
- Conditions come before the instruction.
- Every warning states the level, the command and the reason.
- Compound nouns are three words at most.

## What this mode does not solve

The rules remove ambiguity from the form. They say nothing about the content. A paragraph with no
message becomes a tidy paragraph with no message. If you notice you are polishing form while the
content is missing, that is the real problem — say so.
