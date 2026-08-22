---
name: simply
description: Turn a folder of strategy documents into one plain-language HTML page a CEO reads in under six minutes. Runs seven steps - inventory, a panel of four independent angles, a forced ranking to exactly three must-solve items, a flatten pass to child-level language, three reviewers, one repair round, and a black-and-white artifact. Use when the user types /simply, points at a folder of strategy material and asks for something readable out of it, or says flatten this folder, run the strategy through it, make one page out of these documents, or what do all these documents actually say together.
allowed-tools: Bash(date *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_artifact.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/plain/scripts/plainlint.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/plain-strategy/scripts/stratlint.py *)
---

# Simply

One folder in, one page out. The page says what the documents actually decided, in language a
ten-year-old follows, with every number traceable to a source. It is written for the board, and the
bar is that anyone in the company could follow it. The whole design rests on one problem:
**flattening a vague document produces a beautifully simple lie.** Most strategy documents are vague
on purpose, so four angles test the material before anything is simplified and three reviewers check
that the simplification stayed true.

## How to run it

```
/simply-strategy:compass ./material/<client>/   fills that folder's compass.md. Once per client
/simply-strategy:simply  ./material/<client>/   the run, about 45 minutes
```

The run is a dynamic workflow. Start it with the Workflow tool. Do not work the seven steps by hand
while the runtime is available. Run `date +%Y-%m-%d-%H%M` first, then make this call, unparaphrased:

```
Workflow({
  name: "simply-strategy:simply",
  args: { folder: "<the folder the user named>", root: "${CLAUDE_PLUGIN_ROOT}",
          stamp: "<what date printed>" }
})
```

`stamp` is what keeps a second run from overwriting the first. Output lands in
`runs/<slug>/<stamp>/`, grouped by client and sorted by time. The script cannot produce it, because
the workflow runtime forbids `Date.now()`, and it has to be stable across a resume: the same args
have to give the same path or `resumeFromRunId` writes somewhere new. Leave it out and the run
writes to `runs/<slug>/` and overwrites what was there. It says so in the progress log rather than
doing it quietly.

`root` is how the run finds this plugin's own files. Claude Code substitutes `${CLAUDE_PLUGIN_ROOT}`
in this file and not inside the workflow script, so the value has to be handed over here. From a
clone the placeholder stays literal, the script falls back to `.`, and the run starts with
`Workflow({ scriptPath: "workflows/simply.js", args: { folder: "<folder>", stamp: "<stamp>" } })`.

It runs in the background and asks nothing. Watch it with `/workflows`. When it returns, report the
two file paths and the final check table.

Steps 5 and 7 shell out to the three Python scripts. The frontmatter pre-approves them for the turn
that starts the run. A background run outlives that turn, and a workflow cannot ask, so a run can
sit and wait on a permission prompt. To settle it for good, add the three `Bash(python3 ...)` rules
to your own permission settings before a long run.

If the workflow runtime is unavailable, run the seven steps in
[references/pipeline.md](references/pipeline.md) yourself with subagents, same order, same names.

## The seven steps

Spec, a panel of four, plan, flatten, three reviewers, one repair round, artifact. Twelve agents,
two fan-outs, no loops. Output goes to `runs/<slug>/<stamp>/`. The first full run took 43.7 minutes
on 100KB of material, and a smaller folder is quicker.

What each step gets, must produce, and how it fails: [references/pipeline.md](references/pipeline.md).
That file owns the seven steps. Do not restate them here.

## What makes it more than four prompts

Every step reads [references/house-rules.md](references/house-rules.md) before its own brief. That
file owns the filter and the rules no agent may break: three must-solve seats and not four, no
invented number, a pointer on every claim, nothing softened. The Flattener compresses, it does not
rescue, so consultant prose in step 2 gives you tidy consultant prose in step 4. The four angles are
blind to each other, which is what makes step 3's tension check mean something, and two reviewers
calling one thing fatal is decisive because one critic is only an opinion.

## What ships

`simple-strategy-artifact.html`, black and white, self-contained, prints clean. Next to it
`reasoning.html`, whose cut list and unsure list may never be empty. Both structures, and what fills
them: [references/output-structure.md](references/output-structure.md).

Step 7 verifies itself with `check_artifact.py` under the plugin root, because rendering is the only
step nothing downstream would catch. Exit code 0 or it does not ship.

## What it is not for

Writing the strategy. This flattens one that already exists. If the folder contains no decision, the
artifact says so, which is the most useful thing it can return.
