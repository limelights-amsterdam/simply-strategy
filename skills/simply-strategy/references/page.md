# The page

One HTML file. No build step. It opens from the folder it sits in. Big type, few words, and the
material's own pictures when it has any. You read it top to bottom as one argument. Each screen
answers the question a person who knows nothing would ask next.

## The screens, in order

| Screen | Question it answers | What is on it |
|---|---|---|
| Hero | What is this? | Title of the material, one sentence in the material's own words, the date and size of the material |
| The case | Why change at all? | The reasons the material gives, numbered, one sentence each |
| From → To | What changes? | One row per shift. What stops on the left, what replaces it on the right, the source under the row |
| What grows | Where does the effort go? | What the material says it will build or grow, as cards, biggest first |
| The numbers | What does it cost, in people and money? | Every figure in the material, set huge, with its source and the material's own caveat next to it |
| The bets | What does it assume about the world? | The trends or assumptions the material names |
| The gaps | What does it not say? | Owner, dates, amounts, sequence, as `[TO FILL: ...]`. Then one sentence that places the material (see decision.md) |
| Sources | Where did all this come from? | Every file and slide, as a thumbnail or a name, linked |

If the material has nothing for a screen, drop the screen and say so in the gaps. Do not fill a
screen with something the material does not say.

## The look

Pick one direction and hold it. Think poster.

- One dark ground, one light break for the numbers, one accent. If the material has a brand colour,
  use that as the accent. Use a second, warmer colour for everything you strike through.
- Three typefaces, each with a job: a condensed display face for headings and the ledger, an italic
  serif for the material's own sentences, a mono for labels and sources. Do not use Inter, Roboto,
  Arial or a system stack. Load from Google Fonts and give each a fallback, so the page still reads
  offline.
- Headings in capitals, set tight. Body short. Labels letter-spaced.
- When a ledger row scrolls into view, strike the "from" side through and slide the arrow in. Give
  each screen one staggered reveal. Nothing else moves.
- Set figures huge. Under them, a bar of blocks, one block per unit the material uses. Dashed blocks
  show the difference between two figures. The caption says what one block is.
- Keep `[TO FILL: ...]` visible, in the warm colour. Do not hide it in a footnote.
- A grain overlay and one soft radial glow give the dark ground depth. No purple gradients, no drop
  shadows, no icons.
- On a phone the ledger stacks, the arrow points down and the cards go full width.

## Tokens to start from

```css
:root{
  --ink:#0c0d0c; --coal:#161816; --ash:#2a2d2a; --fog:#8d938d; --bone:#e9e6dc; --paper:#f4f2ea;
  --accent:#00c300;            /* replace with the material's brand colour */
  --struck:#d9643a;            /* what stops, and the TO FILL markers */
  --display:"Anton","Impact","Arial Narrow",sans-serif;
  --serif:"Fraunces","Georgia",serif;
  --mono:"IBM Plex Mono","Menlo","Courier New",monospace;
}
```

Change the faces from run to run so no two pages look alike. Keep the three jobs.

## Sources on the page

Every row, card and figure names its source right under it, in the mono face: `Slide 6`,
`plan-2026.md p. 4`. The last screen lists each file once, with a thumbnail when the material is
slides or pages. The footer says which files you built the page from, and that you used nothing
else.
