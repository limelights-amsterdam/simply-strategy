# Rendering the artifact

This file owns how the artifact is built. It does not define what goes in it.

- **What the six sections are:** `skills/flatten/references/output.md`
- **How everything looks:** the templates. `templates/artifact.html` and `templates/reasoning.html`
  carry the type, the colours and the print rules; `templates/figures.html` carries the drawings.

## The four visual slots

The slots are fixed. The renderer fills them and never invents a fifth, because a layout that varies
per run cannot be checked and cannot be trusted twice.

| Slot | Sits after | Filled from | Drawn as |
|---|---|---|---|
| 1 | Section 1 | The one sentence | `hero`, one number alone, or type only when there is no single number |
| 2 | Section 2 | The three must-solves | One per must-solve: `gap` when it is promise against delivery, `overlap` only when the overlap is the finding |
| 3 | Section 3 | What stops, and what starts | Two columns of type, stops left and starts right. No figure |
| 4 | Section 4 | The bet: assumption, test, date | `timeline`, left to right is always time. Its strongest use is the empty one: four marks with no dates says more than a sentence |

Section 6 may add `eisenhower`, every gap placed by what it stops, when there are more gaps than a
list carries well. That is the whole vocabulary: five drawings in `{root}/templates/figures.html`.
Copy from there and fill in the numbers rather than writing SVG from scratch. A figure with an
invented number is worse than no figure, so `[TO FILL]` never becomes a drawing.

A slot whose content is missing is dropped, and its section carries the unanswered line instead. An
empty graphic is worse than no graphic.

## How it looks

The templates are the design. The renderer fills them and changes nothing about them. The rules
that are easy to break while filling:

- Four colour values, the ones in the template's `:root`. No fifth, inside the SVGs too. Two things
  being compared are told apart by fill, one solid and one outline, never by two greys, because a
  mono printer collapses them.
- Every mark is labelled where it sits. No legend, no pie, no donut, no dual axis, no stacked
  anything: without colour those are guessing.
- No `<img>`, no icon library, no emoji, no CDN, no JavaScript. One file, opens with no network.
- Sentence case in every heading. No em dashes in the copy.
- Every claim carries a source pointer, or it does not go on the page.
- It prints. The templates carry the `@media print` rules; test by printing, not by print preview.

## The two files

**`simple-strategy-artifact.html`** from `templates/artifact.html`. The six sections, four slots.

**`reasoning.html`** from `templates/reasoning.html`. Four parts, and the first three may not be empty:

1. **What it read.** The inventory from `01-spec.md`, including files it could not read.
2. **What it threw away.** Everything demoted to important or nice-to-know, with why. A run that
   discarded nothing is a pass-through, not a process.
3. **Where it is unsure.** Every flag from `05-verdict.md`, every `[TO FILL]`, every `[MISSING]`
   intake field, and the flatten level the input came in at.
4. **Shipped with a flag.** What survived step 5 with a note on it, and which pass in step 2 did
   not bite. Nothing is fixed silently.

This is the page that survives a hostile question.

## Before you call it done

Rendering is the only step nothing downstream checks, so it checks itself:

```bash
python3 {root}/scripts/check_artifact.py runs/<slug>/<stamp>/ --material <material folder>
python3 {root}/scripts/check_headings.py runs/<slug>/<stamp>/simple-strategy-artifact.html
```

Exit code 0 on both, or it does not ship. The first prints what it checks; `--material` is what lets
it confirm that every pointer names a file that exists, which a confident citation of a document
nobody has would otherwise get past. The second reads the headings on their own as an argument.

Fix what they report and run them again. If a check cannot pass because the material genuinely does
not support it, that belongs in section 6 and in the reasoning log, not in a silent workaround.
