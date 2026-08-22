# The pipeline

Seven steps. What each one gets, what it must produce, and where it fails.

Every step reads `house-rules.md` first. Every step writes exactly one file and owns it.

---

## 1 · spec — Spec Agent

**Gets:** the material folder, including its `compass.md`
**Writes:** `01-spec.md`

Read every file in the folder. Produce:

1. **An inventory table.** One row per file: name, what it is, date, which function owns it, page
   count. A file you could not read gets a row saying so — never omit it silently.
2. **The question**, in one sentence, derived from the material and from the Compass. If the Compass
   gives it, use theirs. If it does not, derive one and mark it `[DERIVED]`.
3. **What is not here.** Which document the material obviously references but does not include.

**Fails when** it summarises the documents. This step catalogues, it does not analyse.

---

## 2 · panel — four angles, in parallel

**Gets:** `01-spec.md`, the material, `<material>/compass.md`
**Writes:** `02-substance.md`, `02-contradict.md`, `02-compass.md`, `02-attack.md`

Briefs in `angles.md`. Each angle is blind to the others.

---

## 3 · plan — Plan Agent

**Gets:** all four `02-*.md` files, `01-spec.md`, `<material>/compass.md`
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

Then the four supporting sections, defined in `skills/simplify/references/output.md`: what we stop
doing, what has to be true, what the documents disagree about, what we do not know.

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

**Gets:** the four `02-*.md` files, `03-plan.md` and `04-plain.md`
**Writes:** `05-true.md`, `05-simple.md`, `05-invented.md`

Each reviewer returns findings marked **fatal** or **minor**, with the line it applies to.

| Reviewer | Question | Fatal means |
|---|---|---|
| `true` | Did anything get lost between what the panel found and what is on the page? Check both hops: `02-*` to `03-plan`, and `03-plan` to `04-plain` | A finding disappeared, changed meaning, or reversed at either hop |
| `simple` | Is it actually L1? | A sentence over 15 words, an abstraction with no actor, a number with no comparison |
| `invented` | Does every number trace to a document? | A figure, date or owner that appears in `04-plain.md` but not in the material |

The `true` reviewer covers two hops on purpose. Nothing else checks the plan itself, so a
mis-ranked plan would flatten faithfully into a confident, wrong page. Fidelity to the panel and
fidelity to the plan are the same question asked one step apart.

The `simple` reviewer does not count by eye. That count is the claim the whole product rests on, so
it is measured:

```bash
python3 skills/plain/scripts/plainlint.py runs/<slug>/04-plain.md --mode strict
python3 skills/plain-strategy/scripts/stratlint.py runs/<slug>/04-plain.md
```

Under 1.5 weighted findings per 100 words is clean. For the hard sentence-length and pointer checks,
`scripts/check_artifact.py` runs on the rendered artifact in step 7. Your job here is the judgement
the script cannot make: is an abstraction still an abstraction, does a number have a real comparison,
did a sentence get shorter by losing meaning.

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

**Gets:** `04-plain.md`, `05-verdict.md`, `01-spec.md`, `<material>/compass.md`, `design/DESIGN.md`
**Writes:** `simple-strategy-artifact.html`, `reasoning.html`

Read `output-structure.md` first. It says what to fill and what to check.

Fill `templates/artifact.html` from the six sections and `templates/reasoning.html` from the spec,
the verdict and the Compass.

Then verify your own work, because nothing downstream does:

```bash
python3 scripts/check_artifact.py runs/<slug>/
```

Exit code 0 or it does not ship. Fix what it reports and run it again. If a check cannot pass because
the material does not support it, that goes in section 6 and in the reasoning log, never in a silent
workaround.

**Fails when** it invents a layout, or when it reports success without running the checker.
