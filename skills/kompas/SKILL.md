---
name: kompas
description: Fill the Kompas - the five-field intake that steers a Simply Strategy run. Asks what you refuse before it asks what you want, because an anti-vision and a boundary let an advisor notice something you never wrote a goal for. Two modes - read the fields out of an existing deck or set of documents, or ask five questions. Use when the user types /kompas, starts a Simply Strategy run, or says fill the kompas, set up the intake, what do you need from me before the run, or hands over a deck and asks what we can get out of it.
---

# Kompas

The Kompas steers a Simply Strategy run. It is filled once, not per run, and it lives in `kompas.md`
at the project root.

A goal list is too tight. It can only tell you things you already knew to ask about. An anti-vision
and a boundary let an advisor notice something you never wrote a goal for — and that is where the
useful findings come from.

So the order matters. Ask what they refuse before you ask what they want.

## Two modes

**Read it from material.** `/kompas ./deck/` — the better mode, and the one to offer first. Read
everything in the folder, draft all five fields, and mark each one `drafted` or `missing`. Then show
the draft and ask for corrections.

A draft someone argues with beats a blank field. Nobody writes their own anti-vision from scratch.
Everybody will correct a wrong one.

Formats:

| Format | Works |
|---|---|
| Markdown, plain text | Yes. Cheapest and cleanest |
| Images of slides — PNG, JPG | Yes, read natively |
| PDF | Works, but 20 pages per read and slow. Fine for a document, not for a 60-slide deck |
| PowerPoint, Keynote | No. Export to PDF or images first |

**Ask five questions.** `/kompas` with no argument. Use `AskUserQuestion`, and put anti-vision and
boundaries first.

## The five fields

| # | Field | Why it earns its place |
|---|---|---|
| 1 | **Anti-vision** | A Tuesday five years out if this strategy quietly fails. What exactly is rotten about it |
| 2 | **Boundaries** | What they do not give up, whatever happens. Advice that ignores a boundary gets ignored back |
| 3 | **The question** | One sentence. What must be decided, by whom, by when |
| 4 | **The room** | Who reads this, and who is hostile to it |
| 5 | **Off limits** | Decisions already made. Do not re-open them |

The full prompts, with what a good answer looks like and how to push when an answer is thin:
[references/fields.md](references/fields.md).

## Rules

- **Every field is optional.** A half-filled Kompas still runs. Never block the run on a blank field.
- **Say what is missing, do not fill it in.** An empty field is written as `[MISSING]` and travels
  through to section 6 of the artifact. That is what makes someone fill it in next time.
- **Never soften an anti-vision.** If someone writes something unkind about their own company, keep
  it. The unkindness is the signal.
- **Push once on a thin answer, then move on.** "We want to grow" is not an anti-vision. Ask again in
  a different way. If the second answer is also thin, record it as thin and continue.
- **Quote, do not paraphrase**, when reading from material. Mark every drafted field with the
  document and page it came from.

## Output

Write `kompas.md` with all five fields, each marked `given`, `drafted from <source>`, or `[MISSING]`.
Close with one line saying how many fields are filled and what the run will be blind to without the
rest.
