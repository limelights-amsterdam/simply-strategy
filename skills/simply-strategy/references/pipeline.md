# The pipeline

An intake and six steps, run in order by one reader. What each one gets, what it must produce, and
where it fails.

Read `house-rules.md` first. It applies to everything you write, at every step.

Each step writes numbered files and nothing is held in memory between them. That is the recovery
path: if you stop, look at which numbered file exists and start at the next step.

## Where output goes

`runs/<slug>/<stamp>/`, grouped by source folder and sorted by time. The stamp arrives from outside
the run, so a second run on the same folder does not overwrite the first.

If no stamp arrives the path is flat, `runs/<slug>/`, and the run says so in its log rather than
overwriting in silence.

## Paths in this file

Commands spell `{root}/`. `SKILL.md` says where it comes from: the skill folder itself. Prose
references to reference files are written relative to that folder, `references/...`, and sit under
the same root.

---

## 0 · compass: the intake, once per client

**Gets:** the material folder
**Writes:** `<material>/compass.md`, only when the folder has none yet

If `compass.md` is already there, skip this step and note in `01-spec.md` that it was given. If it
is not, read `references/compass.md` and fill the five fields: drafted from the material when there is
material to draft from, asked as five questions when there is not. Mark every field on its heading
line, `given`, `drafted from <source, page>` or `[MISSING]`. Show the draft and take corrections
before moving on. A blank field never blocks the run; it travels to section 6 of the page.

**Fails when** it invents an anti-vision the material does not contain, or blocks the run on an
empty field. The cost of a thin intake belongs in the output, not hidden.

---

## 1 · spec: what is in the folder

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

## 2 · angles: four passes, in order

**Gets:** `01-spec.md`, the material
**Writes:** `02-angles.md`

Four readings of the same material, each with one lens, in this order. Briefs in `angles.md`.

| Pass | Looks at |
|---|---|
| `substance` | Each claim against itself. Is there a decision in this sentence at all |
| `contradict` | The documents against each other, or one document against itself |
| `compass` | The material against what this client said they refuse |
| `attack` | The plan against the outside world |

**Say in the file that the passes are not independent.** Each one knows what the last found, so
agreement between them proves nothing. Weight a finding by what it rests on instead: does the
material state it, or is it arithmetic on the material's own figures. Both are traceable without
anyone agreeing.

**If `compass.md` does not exist, that pass writes one line saying so and stops.** Do not improvise
an anti-vision. The cost of running without an intake belongs in the output, not hidden.

**Fails when** a later pass quietly restates an earlier one. Name the pass that found each thing, so
step 3 can see a repeat for what it is.

---

## 3 · plan: rank to three, then write the argument

**Gets:** `02-angles.md`, `01-spec.md`, `<material>/compass.md`
**Writes:** `03-plan.md`

**First, read `02-angles.md` for the pass that did not bite.** A pass whose findings restate an
earlier one added nothing. Name it in `03-plan.md` and weight its findings down, so a repeat is not
counted twice.

Then rank:

- **Exactly three must-solve.** Not four, not two. A model that may choose, doesn't. A model with
  three seats has to weigh.
- Everything else goes to **important** or **nice to know**, in a table, still visible. Demoted is
  not deleted.
- For each of the three: what it is, which angle found it, what it costs to leave it, and the pointer.

Then the four supporting sections, defined in `references/flatten/output.md`: what we stop
doing, what has to be true, what the documents disagree about, what we do not know.

### Then write the argument, which is the part that was missing

Everything above this line sorts. Step 2 finds, this step ranks, step 4 shortens, step 5 checks
faithfulness. None of that produces an argument, and a page assembled from sorted parts reads like
a list however good the parts are.

So you owe two more things, and they are the reason this step exists rather than a sort script.

**The governing thought.** One sentence that the whole page is evidence for. Not a summary of the
findings: the thing that is true because of them. Test it by removing any one must-solve. If the
sentence survives untouched, it is a summary. If it weakens, it is an argument.

**Say first what the plan decides, then what it lacks.** The run looks for what is missing, so a
page assembled from its findings reads as an audit however good the plan is. Correct for that here:
the governing thought and section 1 name the real choices the plan makes (the ones that passed the
opposite test in `02-angles.md`) before they name the gap. The one genuinely strong point the
`attack` pass opened with goes into section 1's support, with its pointer. A plan that chooses gets
credit for it on the page; a plan that does not, does not. This is not optimism, it is completeness.

**The order the findings have to come in.** Write the through-line as a numbered list of claims, one
per section, in the order a reader must meet them. Each one advances from the last. Read the list on
its own with nothing else: if it makes the case without the body, the page will too.

Write both at the top of `03-plan.md`, under `## The argument`. The flattener turns that list into
the page's headings, so this is where the story is decided.

Two rules, because this is the step where invention is easiest:

- **Every claim in the through-line rests on a finding an angle made.** Name which one. A line with
  no finding under it is a line you wrote because it sounded like the next beat.
- **A heading may not count the page.** It states something about the material, which a reader
  can disagree with. The rule and its examples: `references/flatten/output.md`.

**Fails when** it keeps four or five must-solves "because they are all important". If that happens,
the ranking was never made and the run has produced a longer document rather than a decision.

---

## 4 · flatten: down to L1

**Gets:** `03-plan.md`
**Writes:** `04-plain.md`

Load `references/flatten/moves.md`. Produce the six sections at flatten level L1.

**The headings come from `## The argument` in `03-plan.md`, not from the section names.** One claim
per section, in that order. A reader who scans the headings and nothing else should get the case.
Verify with `python3 {root}/scripts/check_headings.py` on the rendered page in step 6.

Read `references/flatten/before-after.md` and `references/flatten/output.md` first. The second one
carries the rule that makes the budget reachable: **write the finding, not the chain that supports
it.** One figure and one line per must-solve; the quotes, the arithmetic and the demoted findings
stay where they already are, in `02-angles.md` and `03-plan.md`, and step 6 surfaces them in the log.

You are not cutting evidence. You are declining to copy it forward.

**Every section carries at least one pointer, and every figure carries one.** Writing alone it is
easy to produce a good sentence and lose where it came from. Step 5 counts them.

**Fails when** it drops a claim to make a sentence shorter, or when a section arrives with no
pointer in it. Losing content is the failure mode of this whole step.

---

## 5 · verify: three scripts, then one judgement

**Gets:** `02-angles.md`, `03-plan.md`, `04-plain.md`
**Writes:** `04-plain.md` revised, `05-verdict.md`

Tracing a figure to a source is a lookup, not a judgement, so a script does it. What is left for
judgement is whether the page still says what the plan said.

### First, run the three checks

```bash
python3 {root}/scripts/check_facts.py runs/<slug>/<stamp>/04-plain.md --material <material folder>
python3 {root}/scripts/plainlint.py runs/<slug>/<stamp>/04-plain.md --max-sentence 15
python3 {root}/scripts/stratlint.py runs/<slug>/<stamp>/04-plain.md
```

Every figure traces, or says whose arithmetic it is, or is `[TO FILL: …]`. Every sentence is under
fifteen words. Both linters clean. Fix what they report before you read anything.

`check_facts.py` also counts the pointers. Under two per hundred words it exits 1, and the answer is
to go back to step 4 rather than forward. This is the failure mode of writing alone and it does not
announce itself: the page reads well and cannot be checked.

### Then do the one thing no script can

**Did anything get lost between what step 2 found and what is on the page?** Check both hops,
`02-angles` to `03-plan`, and `03-plan` to `04-plain`. Nothing else checks the plan itself, so a
mis-ranked plan would flatten faithfully into a confident, wrong page.

This is judgement, which is why it is not a script: a finding can survive word for word and still
lose the thing that made it matter. A flattener that keeps a finding's test and drops its
consequence has kept the words and lost the point, and both versions still mention the same thing.

Mark each finding **fatal** or **minor**, apply the fatal ones, and write `05-verdict.md`: what the
scripts reported, what you fixed, and anything shipping with a flag. **Nothing is fixed silently.**

**Fails when** it rewrites beyond what the scripts and the fidelity check reported. This is the last
step to touch the text, and a free hand here undoes the ranking.

---

## 6 · artifact: render, then check the page

**Gets:** `04-plain.md` for the page. `01-spec.md`, `02-angles.md`, `03-plan.md` and
`05-verdict.md` for the log. Plus `<material>/compass.md` and the three files in `assets/`
**Writes:** `simple-strategy-artifact.html`, `reasoning.html`

Read `output-structure.md` first. It says what to fill and what to check.

Fill `assets/artifact.html` from the six sections.

Fill `assets/reasoning.html` from the files that already hold the evidence: `01-spec.md` for what
was read and what is missing, `02-angles.md` for who found what, `03-plan.md` for what was
demoted and why, `05-verdict.md` for what was fixed and what shipped flagged.

Nothing gets written twice. The page and the log are two views of the same run, and the log is the
one that answers a hostile question, so it carries the chain in full.

**Every claim on the page needs a matching entry in the log.** A line with no entry behind it was
cut rather than moved, and that is the one failure this split exists to prevent.

Then run the two checks under "Before you call it done" in `output-structure.md`. Exit code 0 on
both, or it does not ship.

**Fails when** it invents a layout, or when it reports success without running the checks.
