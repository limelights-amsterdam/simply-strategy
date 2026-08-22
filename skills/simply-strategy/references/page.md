# The page

The skeleton is `assets/page.html`. Start from it. This file says what goes in it and why.

A picture book, not a poster. One narrow column you read top to bottom. Numbered sections. Each
section asks one plain question, answers it in one claim, draws it, says two sentences, and names
the page it came from. Someone who knows nothing reads it in a few minutes and can retell it.

## The shape

- A wide page, about 64rem, on warm paper. A masthead with a rule above and below. In each section the picture runs the full width
  and the words under it sit on a wide measure in a large size. Dark ink, one sans, two accents at
  most (one warm, one cool) and one green for "decided". No web fonts needed. It prints clean.
- Header: a small kicker with the document's name, then a headline of one short sentence that says the
  whole story, then two or three short sentences under it: what they do, what they want, what they
  have not said. Nothing else; the sources under each section and the footer say
  where it all comes from.
- Then the sections, numbered. Each one has the same five parts, in this order:
  1. Kicker: the number and the question, in plain words. "3. The problem they name"
  2. Headline: the answer as one claim. "The allowance system is hard. Three things go wrong."
  3. Picture: an inline SVG drawn for this idea (see below).
  4. One or two sentences that say what the document says, in plain words.
  5. Source line: "Source: p. 5", and the document's own sentence in its own language when it
     carries the point. "De visie is een kompas en geen routekaart."
- The last section is always "What is decided, and what is not": two lists. Filled dots for what
  the document says, each with its page. Dashed circles for what it does not say, each as a plain
  sentence: "what each building block costs", "who owns each building block". Under the lists, one
  sentence that places the document (see decision.md).
- Footer: the document's full title, author, place, date, how pages are counted, and that every
  number on the page comes from it.

## The questions

The sections follow the document, not a template. Ask the questions a newcomer would ask, in the
order they would ask them. Usually some of these, rarely all:

| Question | Typical headline |
|---|---|
| Who is this about | One service, six million households, twenty-two billion euro a year |
| What kind of plan is this | A compass, not a route map |
| The problem they name | Three things go wrong |
| Where they want to go | One front door. You get what you are owed |
| How they want to get there | Four building blocks. Two for citizens, two for the organisation |
| What stops, what starts | Legacy platforms go. One foundation replaces them |
| What it costs, in people and money | Thirty percent fewer people, money moves from people to software |
| The clearest promise in the plan | Risk moves from the citizen to the government |
| What is decided, and what is not | Directions are chosen. Numbers, owners and dates are not in the document |

Drop a question the document does not answer. Do not add one it does not raise. If a deck has
eight slides on the market and one on the choice, the page still spends most of its room on the
choice, and says the market slides exist.

## The pictures

Every picture is drawn for the idea it explains. Inline SVG, `viewBox`, the page's own colours as
`var(--ink)` and so on, an `aria-label` that says what it shows. Never a stock icon, never a
decorative shape. Use a small vocabulary and keep it:

| To show | Draw |
|---|---|
| How many | A row of the thing, one shape per unit, and the figure next to it, huge |
| Today and tomorrow | Left half and right half, many small boxes on the left, one on the right |
| A choice made | A compass, an arrow, a filled dot |
| A choice not made | A crossed-out map, a dashed outline, a `?` |
| A problem | A tangled line, a coin with a line through it, an arrow turning back |
| Who carries what | Two figures and a weight that moves from one to the other |
| A number from the document | The number itself, set huge, with its unit and its page |
| What stops and what starts | The old thing struck through, the new thing next to it |

When the material is a deck with good slides, you may show a slide render as the picture, but only
when the slide itself is the clearest picture. A drawn pictogram beats a busy slide.

## Colours

The three colour values in the template are a start. Vary the accents and the paper tint from run to
run, or take them from the material's brand. Keep the shape.
