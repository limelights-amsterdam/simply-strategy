# The page

One HTML file, no build step, opens from the folder it sits in. Big type, few words, the material's
own pictures where it has them. It reads top to bottom as one argument, and every screen answers a
question a person who knows nothing would ask next.

## The screens, in order

| Screen | Question it answers | What is on it |
|---|---|---|
| Hero | What is this? | Title of the material, one sentence in the material's own words, date and size of the material |
| The case | Why change at all? | The reasons the material gives, numbered, each a sentence |
| From → To | What changes? | One row per shift: what stops on the left, what replaces it on the right, the source under each row |
| What grows | Where does the effort go? | The things the material says it will build or grow, as cards, biggest first |
| The numbers | What does it cost, in people and money? | Every figure the material contains, huge, with its source and the material's own caveat |
| The bets | What does it assume about the world? | The trends or assumptions the material names |
| The gaps | What does it not say? | Owner, dates, amounts, sequence, as `[TO FILL: ...]`, then one sentence that places the material (see decision.md) |
| Sources | Where did all this come from? | Thumbnails or names of every file and slide, linked |

Drop a screen when the material has nothing for it, and say so in the gaps. Never fill a screen
with something the material does not say.

## The look

Commit to one direction and hold it. The page is a poster, not a report.

- One dark ground, one light break for the numbers, one accent. Take the accent from the material's
  own brand if it has one. Everything struck through is in a second, warmer colour.
- A condensed display face for headings and the ledger, an italic serif for the material's own
  sentences, a mono for labels and sources. Never Inter, Roboto, Arial or a system stack. Load from
  Google Fonts with a fallback stack, so the page still reads offline.
- Headings in capitals, set tight. Body short. Labels letter-spaced.
- The ledger strikes the "from" side through when it scrolls into view, and the arrow slides in.
  One staggered reveal per screen, nothing else moves.
- Figures are set huge. A bar of blocks under them, one block per unit the material uses, dashed
  blocks for the difference between two figures. The caption says what one block is.
- `[TO FILL: ...]` is visible, in the warm colour, never hidden in a footnote.
- A grain overlay and one soft radial glow give the dark ground depth. No gradients in purple, no
  cards with drop shadows, no icons.
- Works on a phone: the ledger stacks, the arrow turns down, the cards go full width.

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

Change the faces between runs so no two pages look the same, but keep the roles: one display, one
italic serif, one mono.

## Sources on the page

Each row, card and figure names its source in the mono face, right under it: `Slide 6`,
`plan-2026.md p. 4`. The last screen lists every file once, with a thumbnail when the material is
slides or pages. The footer says the page was built from those files and nothing else.
