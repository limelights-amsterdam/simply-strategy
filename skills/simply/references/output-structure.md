# Rendering the artifact

This file owns how the artifact is built. It does not define what goes in it.

- **What the six sections are:** `skills/simplify/references/output.md`
- **How everything looks:** `design/DESIGN.md`

## The four visual slots

The slots are fixed. The renderer fills them and never invents a fifth, because a layout that varies
per run cannot be checked and cannot be trusted twice.

| Slot | Sits after | Filled from |
|---|---|---|
| 1 | Section 1 | The one sentence |
| 2 | Section 2 | The three must-solves |
| 3 | Section 3 | What stops, and what starts |
| 4 | Section 4 | The bet: assumption, test, date |

Their form, type sizes and rules live in `design/DESIGN.md` section 7. Do not restate them here.

A slot whose content is missing is dropped, and its section carries the unanswered line instead. An
empty graphic is worse than no graphic.

## The two files

**`simple-strategy-artifact.html`** from `templates/artifact.html`. The six sections, four slots.

**`reasoning.html`** from `templates/reasoning.html`. Five parts, and the first three may not be empty:

1. **What it read.** The inventory from `01-spec.md`, including files it could not read.
2. **What it threw away.** Everything demoted to important or nice-to-know, with why. A run that
   discarded nothing is a pass-through, not a process.
3. **Where it is unsure.** Every flag from `05-verdict.md`, every `[TO FILL]`, every `[MISSING]`
   intake field, and the flatten level the input came in at.
4. **The tension check.** Whether the angles agreed too much, and which one was sent back.
5. **Shipped with a flag.** What survived review with a note on it. Nothing is fixed silently.

This is the page that survives a hostile question.

## Before you call it done

Rendering is the only step nothing downstream checks, so it checks itself:

```bash
python3 {root}/scripts/check_artifact.py runs/<slug>/<stamp>/ --material <material folder>
```

`{root}` is the plugin root from your prompt. Exit code 0 or it does not ship.

The checker verifies the six sections, unfilled slots, sentence length, the three-item count, em
dashes, and that the reasoning log's cut list and unsure list are not empty. With `--material` it
also checks that every source pointer names a file that actually exists in that folder, which is the
one thing a confident citation of a document nobody has would otherwise get past.

It also enforces the length budget. Fix what it reports and run it again.

If a check cannot pass because the material genuinely does not support it, that belongs in section 6
and in the reasoning log. It does not belong in a silent workaround.
