# The pipeline

Seven steps. What each one gets, what it must produce, and where it fails.

Every step reads `house-rules.md` first. Every step writes exactly one file and owns it.

---

## 1 · spec — Spec Agent

**Gets:** the material folder, `kompas.md`
**Writes:** `01-spec.md`

Read every file in the folder. Produce:

1. **An inventory table.** One row per file: name, what it is, date, which function owns it, page
   count. A file you could not read gets a row saying so — never omit it silently.
2. **The question**, in one sentence, derived from the material and from the Kompas. If the Kompas
   gives it, use theirs. If it does not, derive one and mark it `[DERIVED]`.
3. **What is not here.** Which document the material obviously references but does not include.

**Fails when** it summarises the documents. This step catalogues, it does not analyse.

---

## 2 · panel — four angles, in parallel

**Gets:** `01-spec.md`, the material, `kompas.md`
**Writes:** `02-substance.md`, `02-contradict.md`, `02-kompas.md`, `02-attack.md`

Briefs in `angles.md`. Each angle is blind to the others.

---

## 3 · plan — Plan Agent

**Gets:** all four `02-*.md` files, `01-spec.md`, `kompas.md`
**Writes:** `03-plan.md`

**First, the tension check.** Read the four angle files side by side. If they broadly agree, an angle
did not bite. Record which one, and in `03-plan.md` note that its findings are treated as weak. Four
agents nodding politely is worse than one agent, because it reads like confirmation.

Then bundle. Forced ranking:

- **Exactly three must-solve.** Not four, not two. A model that may choose, doesn't. A model with
  three seats has to weigh.
- Everything else goes to **important** or **nice to know**, in a table, still visible. Demoted is
  not deleted.
- For each of the three: what it is, which angle found it, what it costs to leave it, and the pointer.

Then the four supporting sections: what we stop doing, what has to be true, what the documents
disagree about, what we do not know.

**Fails when** it keeps four or five must-solves "because they are all important". If that happens,
the ranking was never made and the run has produced a longer document rather than a decision.

---

## 4 · flatten — Flattener

**Gets:** `03-plan.md`
**Writes:** `04-plain.md`

Load `skills/simplify/SKILL.md`. Produce the six sections at flatten level L1.

Read `skills/simplify/references/before-after.md` first.

**Fails when** it drops a claim to make a sentence shorter. Losing content is the failure mode of
this whole step.

---

## 5 · review — three reviewers, in parallel

**Gets:** `03-plan.md` and `04-plain.md`
**Writes:** `05-true.md`, `05-simple.md`, `05-invented.md`

Each reviewer returns findings marked **fatal** or **minor**, with the line it applies to.

| Reviewer | Question | Fatal means |
|---|---|---|
| `true` | Does the flattened text still say what the plan said? | A claim changed meaning, reversed, or disappeared |
| `simple` | Is it actually L1? | A sentence over 15 words, an abstraction with no actor, a number with no comparison |
| `invented` | Does every number trace to a document? | A figure, date or owner that appears in `04-plain.md` but not in the material |

The `simple` reviewer runs both linters and counts sentences over 15 words by hand. That count is the
claim the whole product rests on, so it gets counted, not estimated.

---

## 6 · coordinate — Review Coordinator

**Gets:** the three `05-*.md` files, `04-plain.md`
**Writes:** `04-plain.md` (revised), `05-verdict.md`

Tally. **A finding that two or more reviewers call fatal is decisive.** One critic is an opinion, two
is a signal.

Consolidate into must-fix and should-fix. Apply the must-fix list to `04-plain.md`. One round only —
an endless polish loop eats the coffee.

Write `05-verdict.md`: what was fixed, what was left, and anything that survived with a flag on it.
Anything shipped with a flag appears in `reasoning.html`. Nothing gets fixed silently.

**Fails when** it treats a single reviewer's opinion as decisive, or when it rewrites beyond the
must-fix list.

---

## 7 · artifact — Artifact Agent

**Gets:** `04-plain.md`, `05-verdict.md`, `01-spec.md`, `kompas.md`, `design/DESIGN.md`
**Writes:** `simple-strategy-artifact.html`, `reasoning.html`

Fill `templates/artifact.html` from the six sections. Fill `templates/reasoning.html` from the spec,
the verdict and the Kompas.

Both files self-contained: CSS inline, SVG inline, no CDN, no build step. Black and white only.

**Fails when** it invents a layout. The four visual slots are fixed. See `output-structure.md`.
