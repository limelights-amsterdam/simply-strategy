# Reading the material

The argument is a folder, a file, or a set of images. Read all of it before you write anything.

## What it can be

| It is | Read it with |
|---|---|
| Markdown, text | `cat` |
| PDF | `pdftotext -layout file.pdf -` if it is installed. Otherwise read the PDF with the Read tool, page by page |
| PowerPoint | `unzip -p deck.pptx 'ppt/slides/slide*.xml' \| sed 's/<[^>]*>/ /g'` for the text. If the folder has slide renders, look at those too |
| Word | `unzip -p doc.docx word/document.xml \| sed 's/<[^>]*>/ /g'` |
| Images of slides or pages | Look at each one. The image is the source. A text extract, if there is one, is a help |
| A text extract next to the images | Read both. Where the extract garbles something, the image settles it |

Note everything the material names but does not contain: a budget sheet it refers to, an appendix
that is missing. Each of those goes on the gaps screen: "The deck refers to a budget sheet that is not in the material."

## What counts as a figure

A number, a date, a percentage, an amount of money, the name of a person or a role. Each one on the
page carries its source. You may do arithmetic on their figures. When you do, the page says the sum
is yours: "one block is 100 FTE, the dashed blocks are the difference between the two figures on
the slide".

## Pointers

`Slide 6` when the material is one deck. `plan-2026.md p. 4` when it is a folder of files. A quoted
phrase gets the same pointer. A claim without a pointer does not go on the page.

## Where the page goes

Next to the material, as `simply-strategy.html`. If the material is a folder, write it in that
folder. If it is a set of images, write it in the folder the images are in, so `<img
src="slide-6.png">` resolves. Use relative paths. Never an absolute path, never a remote image.

## When two files disagree

Say so. Name both, and show both figures with both pointers. Do not average them. Do not pick the
newer one without saying that is what you did.
