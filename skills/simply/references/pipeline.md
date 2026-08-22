# The pipeline

Six steps, run in order by one reader. What each one gets, what it must produce, and where it fails.

Read `house-rules.md` first. It applies to everything you write, at every step.

Each step writes numbered files and nothing is held in memory between them. That is the recovery
path: if you stop, look at which numbered file exists and start at the next step.

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

**Say what the sequence costs, in the file.** In the parallel version these four never see each
other, which is what makes agreement between them evidence. Here each pass knows what the last found,
so convergence proves nothing and there is no tension check.

Weight a finding instead by what it rests on: does the material state it, or is it arithmetic on the
material's own figures. Both are traceable without anyone agreeing.

**If `compass.md` does not exist, that pass writes one line saying so and stops.** Do not improvise
an anti-vision. The cost of running without an intake belongs in the output, not hidden.

**Fails when** a later pass quietly restates an earlier one. Name the pass that found each thing, so
step 3 can see a repeat for what it is.

---

## 3 · plan: rank to three, then write the argument

**Gets:** `02-angles.md`, `01-spec.md`, `<material>/compass.md`
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

Then the four supporting sections, defined in `skills/flatten/references/output.md`: what we stop
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

## 4 · flatten: down to L1

**Gets:** `03-plan.md`
**Writes:** `04-plain.md`

Load `skills/flatten/SKILL.md`. Produce the six sections at flatten level L1.

**The headings come from `## The argument` in `03-plan.md`, not from the section names.** One claim
per section, in that order. A reader who scans the headings and nothing else should get the case.
Verify with `python3 {root}/scripts/check_headings.py` on the rendered page in step 6.

Read `skills/flatten/references/before-after.md` and `references/output.md` first. The second one
carries the rule that makes the budget reachable: **write the finding, not the chain that supports
it.** One figure and one line per must-solve; the quotes, the arithmetic and the demoted findings
stay where they already are, in `02-angles.md` and `03-plan.md`, and step 6 surfaces them in the log.

You are not cutting evidence. You are declining to copy it forward.

**Every section carries at least one pointer, and every figure carries one.** This was measured, not
assumed: working through the steps alone produced 1.4 pointers per 100 words where the parallel
version produced 3.1. Alone it is easy to write a good sentence and lose where it came from, and a
distillation that drops what a claim rests on is a shorter document.

**Fails when** it drops a claim to make a sentence shorter, or when a section arrives with no
pointer in it. Losing content is the failure mode of this whole step.

---

## 5 · verify: three scripts, then one judgement

**Gets:** `02-angles.md`, `03-plan.md`, `04-plain.md`
**Writes:** `04-plain.md` revised, `05-verdict.md`

This step used to be three reviewers and a coordinator. Two of those reviewers were doing work a
script does better, and the measurement is not close.

On one run, the reviewer whose whole job was to catch invented
figures reported "two fatal, nine minor, no invented owner anywhere in the file". Running
`check_facts.py` over the same file found **nine figures that appear nowhere in the material**. An
agent asked to be thorough about numbers was beaten by eighty lines of Python, which is what should
happen: tracing a figure to a source is a lookup, not a judgement.

So the mechanical half is mechanical now, and one agent does the half that is not.

### First, run the three checks

```bash
python3 {root}/scripts/check_facts.py runs/<slug>/<stamp>/04-plain.md --material <material folder>
python3 {root}/skills/plain/scripts/plainlint.py runs/<slug>/<stamp>/04-plain.md --lang en --max-sentence 15
python3 {root}/skills/plain-strategy/scripts/stratlint.py runs/<slug>/<stamp>/04-plain.md --lang en
```

Every figure traces, or says whose arithmetic it is, or is `[TO FILL: …]`. Every sentence is under
fifteen words. Both linters clean. Fix what they report before you read anything.

### Count the pointers before you read anything else

```bash
grep -c '\[slide' runs/<slug>/<stamp>/04-plain.md
```

Under two per hundred words, go back to step 4 rather than forward. This is the failure mode of
running alone and it does not announce itself: the page reads well and cannot be checked.

### Then do the one thing no script can

**Did anything get lost between what the panel found and what is on the page?** Check both hops,
`02-angles` to `03-plan`, and `03-plan` to `04-plain`. Nothing else checks the plan itself, so a
mis-ranked plan would flatten faithfully into a confident, wrong page.

This is judgement, which is why it stays with an agent: a finding can survive word for word and
still lose the thing that made it matter. On the first real run the flattener kept shift-left's test
and dropped its consequence, which was the whole point of the finding, and no script would have
noticed because both versions mention shift-left.

Mark each finding **fatal** or **minor**, apply the fatal ones, and write `05-verdict.md`: what the
scripts reported, what you fixed, and anything shipping with a flag. **Nothing is fixed silently.**

**Fails when** it rewrites beyond what the scripts and the fidelity check reported. This is the last
agent to touch the text, and a free hand here undoes the ranking.

---

## 6 · artifact: render, then check the page

**Gets:** `04-plain.md` for the page. `01-spec.md`, `02-angles.md`, `03-plan.md` and
`05-verdict.md` for the log. Plus `<material>/compass.md` and `design/DESIGN.md`
**Writes:** `simple-strategy-artifact.html`, `reasoning.html`

Read `output-structure.md` first. It says what to fill and what to check.

Fill `templates/artifact.html` from the six sections.

Fill `templates/reasoning.html` from the files that already hold the evidence: `01-spec.md` for what
was read and what is missing, `02-angles.md` for who found what, `03-plan.md` for what was
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
