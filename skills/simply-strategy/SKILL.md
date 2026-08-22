---
name: simply-strategy
description: Explain a strategy like I'm 5. Use when the user types /simply-strategy <folder or file of strategy documents>, or asks for a dead-simple picture explainer of what a strategy, annual plan, vision paper or board deck actually says.
---

# simply-strategy

Explain this strategy like I'm someone who knows nothing about it, using an HTML artifact with big
pictures and few words.

Material: $ARGUMENTS

Three things a strategy needs that a topic does not:

- Say only what the material says. If it contains no decision, the page says so. Do not invent one.
- Never invent a number, owner or date. If the material does not give one, the page says so in plain words.
- Every figure on the page comes from the material, and the page says where.

Four short files under `references/` say how. Read them before you write:

- [material.md](references/material.md): how to read what the user gave you, and where the page goes.
- [decision.md](references/decision.md): how to tell whether the material contains a decision, and what the page says when it does not.
- [words.md](references/words.md): how the page sounds.
- [page.md](references/page.md): what the page looks like, section by section.

The page is [assets/page.html](assets/page.html). Copy that file to the output path and fill it
in. Keep the `<style>` block as it is; only the colour values may change. Keep the header, the
section shape, the class names and the footer. Replace everything in square brackets, draw the
pictures as inline SVG, add or drop sections to follow the material. Do not design a new page and
do not write new CSS.

Write the artifact beside the material as `simply-strategy.html`.
