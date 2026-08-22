# Reading the material

The argument is a folder, a file, or a set of images. Read all of it before writing anything.

## What it can be

| It is | Read it with |
|---|---|
| Markdown, text | `cat` |
| PDF | `pdftotext -layout file.pdf -` when installed, otherwise read the PDF directly with the Read tool, page by page |
| PowerPoint | `unzip -p deck.pptx 'ppt/slides/slide*.xml' \| sed 's/<[^>]*>/ /g'` for the text, and the slide images if the folder has renders |
| Word | `unzip -p doc.docx word/document.xml \| sed 's/<[^>]*>/ /g'` |
| Images of slides or pages | Look at each one. The image is the source; the text extract, if any, is a help |
| A text extract next to the images | Read both. The images settle what the extract garbles |

Note everything the material names but does not contain: a budget sheet it refers to, an appendix
that is missing. That goes on the gaps screen as `[TO FILL: ...]`.

## What counts as a figure

A number, a date, a percentage, a name of a person or a role, an amount of money. Each one on the
page carries its source. Your own arithmetic on their figures is allowed, and the page says it is
yours: "one block is 100 FTE, the dashed blocks are the difference between the two figures on the
slide".

## Pointers

`Slide 6` when the material is one deck. `plan-2026.md p. 4` when it is a folder of files. A
quoted phrase gets the same pointer. No pointer, no claim.

## Where the page goes

Next to the material, as `simply-strategy.html`. If the material is a folder, in that folder. If it
is a set of images, in the folder the images are in, so `<img src="slide-6.png">` resolves. Relative
paths only, never absolute, never a remote image.

## When two files disagree

Say so, name both, show both figures with both pointers. Do not average, do not pick the newer one
without saying that is what you did.
