# The pipeline

Seven steps. What each one gets, what it must produce, and where it fails.

Every step reads `house-rules.md` first. Every step writes exactly one file and owns it.

## Where output goes

`runs/<slug>/<stamp>/`, grouped by source folder and sorted by time. The stamp arrives from outside
the run, so a second run on the same folder does not overwrite the first.

If no stamp arrives the path is flat, `runs/<slug>/`, and the run says so in its log rather than
overwriting in silence.

## Paths in this file

`{root}` is the plugin root, handed to you in your prompt. When the plugin is installed it is not the
working directory, so a bare `scripts/...` resolves to nothing.

Commands below are written with `{root}` spelled out, because a command with a wrong path fails
silently in the middle of a long run. Prose references to skill files are left bare for readability
and sit under the same root.

---

## 1 · spec: the Spec Agent

**Gets:** the material folder, including its `compass.md`
**Writes:** `01-spec.md`

Read every file in the folder. Produce:

1. **An inventory table.** One row per file: name, what it is, date, which function owns it, page
   count. A file you could not read gets a row saying so, never omit it silently.
2. **The question**, in one sentence, derived from the material and from the Compass. If the Compass
   gives it, use theirs. If it does not, derive one and mark it `[DERIVED]`.
3. **What is not here.** Which document the material obviously references but does not include.

**Fails when** it summarises the documents. This step catalogues, it does not analyse.

---

## 2 · panel: four angles, in parallel

**Gets:** `01-spec.md`, the material, `<material>/compass.md`
**Writes:** `02-substance.md`, `02-contradict.md`, `02-compass.md`, `02-attack.md`

Briefs in `angles.md`. Each angle is blind to the others.

---

## 3 · plan: the Plan Agent

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

### Then write the argument, which is the part that was missing

Everything above this line sorts. The panel finds, you rank, the flattener shortens, the reviewers
check faithfulness. None of that produces an argument, and a page assembled from sorted parts reads
like a list however good the parts are.

So you owe two more things, and they are the reason this step exists rather than a sort script.

**The governing thought.** One sentence that the whole page is evidence for. Not a summary of the
findings: the thing that is true because of them. Test it by removing any one must-solve. If the
sentence survives untouched, it is a summary. If it weakens, it is an argument.

**The order the findings have to come in.** Write the through-line as a numbered list of claims, one
per section, in the order a reader must meet them. Each one advances from the last. Read the list on
its own with nothing else: if it makes the case without the body, the page will too.

Write both at the top of `03-plan.md`, under `## The argument`. The flattener turns that list into
the page's headings, so this is where the story is decided.

Two rules, because this is the step where invention is easiest:

- **Every claim in the through-line rests on a finding an angle made.** Name which one. A line with
  no finding under it is a line you wrote because it sounded like the next beat.
- **A heading may not count the page.** "Nine pairs cannot both be true" describes the document.
  "Where the deck disagrees with itself, it is about money" describes the material. The second is
  checkable against the source; the first is only checkable against itself.

**Fails when** it keeps four or five must-solves "because they are all important". If that happens,
the ranking was never made and the run has produced a longer document rather than a decision.

---

## 4 · flatten: the Flattener

**Gets:** `03-plan.md`
**Writes:** `04-plain.md`

Load `skills/simplify/SKILL.md`. Produce the six sections at flatten level L1.

**The headings come from `## The argument` in `03-plan.md`, not from the section names.** One claim
per section, in that order. A reader who scans the headings and nothing else should get the case.
Verify with `python3 {root}/scripts/check_headings.py` on the rendered page in step 7.

Read `skills/simplify/references/before-after.md` and `references/output.md` first. The second one
carries the rule that makes the budget reachable: **write the finding, not the chain that supports
it.** One figure and one line per must-solve; the quotes, the arithmetic and the demoted findings
stay where they already are, in `02-*.md` and `03-plan.md`, and step 7 surfaces them in the log.

You are not cutting evidence. You are declining to copy it forward.

**Fails when** it drops a claim to make a sentence shorter. Losing content is the failure mode of
this whole step.

---

## 5 · review: three reviewers, in parallel

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
python3 {root}/skills/plain/scripts/plainlint.py runs/<slug>/<stamp>/04-plain.md \
  --lang en --max-sentence 15
python3 {root}/skills/plain-strategy/scripts/stratlint.py runs/<slug>/<stamp>/04-plain.md --lang en
```

Clean is under 1.5 for plainlint and under 1.0 for stratlint, and the two are not comparable:
plainlint scores per 100 words of prose it scanned, stratlint per 100 words of the whole document.
Read each verdict against its own band rather than against one number.

For the hard sentence-length and pointer checks,
`scripts/check_artifact.py` runs on the rendered artifact in step 7. Your job here is the judgement
the script cannot make: is an abstraction still an abstraction, does a number have a real comparison,
did a sentence get shorter by losing meaning.

---

## 6 · coordinate: the Review Coordinator

**Gets:** the three `05-*.md` files, `04-plain.md`
**Writes:** `04-plain.md` (revised), `05-verdict.md`

Tally. **A finding that two or more reviewers call fatal is decisive.** One critic is an opinion, two
is a signal.

Consolidate into must-fix and should-fix. Apply the must-fix list to `04-plain.md`. One round only, an endless polish loop eats the coffee.

**Then read it back as a person would.** Load `skills/humanizer/SKILL.md` and pass over
`04-plain.md` once. This is the last point where anyone reads the whole thing as prose rather than
as findings, and by now it has been through a panel, a ranking, a flattening and three reviewers.
Text handled that many times acquires a particular sound.

Two rules for this pass, because it is the one most likely to do harm:

- **Change no claim, no number, no pointer.** If a sentence needs a fact to read better, it stays
  as it is and the gap goes in the log.
- **Cut rather than smooth.** The failure mode here is polishing a sentence that should have been
  deleted.

Write `05-verdict.md`: what was fixed, what was left, and anything that survived with a flag on it.
Anything shipped with a flag appears in `reasoning.html`. Nothing gets fixed silently.

**Fails when** it treats a single reviewer's opinion as decisive, or when it rewrites beyond the
must-fix list.

---

## 7 · artifact: the Artifact Agent

**Gets:** `04-plain.md` for the page. `01-spec.md`, the four `02-*.md`, `03-plan.md` and
`05-verdict.md` for the log. Plus `<material>/compass.md` and `design/DESIGN.md`
**Writes:** `simple-strategy-artifact.html`, `reasoning.html`

Read `output-structure.md` first. It says what to fill and what to check.

Fill `templates/artifact.html` from the six sections.

Fill `templates/reasoning.html` from the files that already hold the evidence: `01-spec.md` for what
was read and what is missing, the four `02-*.md` for who found what, `03-plan.md` for what was
demoted and why, `05-verdict.md` for what was fixed and what shipped flagged.

Nothing gets written twice. The page and the log are two views of the same run, and the log is the
one that answers a hostile question, so it carries the chain in full.

**Every claim on the page needs a matching entry in the log.** A line with no entry behind it was
cut rather than moved, and that is the one failure this split exists to prevent.

Then verify your own work, because nothing downstream does:

```bash
python3 {root}/scripts/check_artifact.py runs/<slug>/<stamp>/ --material <material folder>
```

Exit code 0 or it does not ship. Fix what it reports and run it again. If a check cannot pass because
the material does not support it, that goes in section 6 and in the reasoning log, never in a silent
workaround.

**Fails when** it invents a layout, or when it reports success without running the checker.
