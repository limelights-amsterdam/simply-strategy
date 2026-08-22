# Simple Strategy Artifact — design system

Point a coding agent at this file and it produces the artifact. One HTML file, black and white,
opens without a network, prints on any machine in the room.

Format follows the awesome-design-md convention: identity → philosophy → colour → type → layout →
components → rules.

---

## 1. What this is

**Artefact:** one page that says what a folder of strategy documents actually decided.
**Reader:** a CEO or CFO with four minutes, standing up, possibly holding it on paper.
**Feel:** a printed editorial page, not a dashboard and not a deck.

The design has one job. Everything on the page has to look like it was decided by a person who
already knew the answer. Nothing decorative, nothing that hedges, nothing that suggests a machine
filled a template.

## 2. Philosophy

1. **Two colours.** Black and white, one grey for rules and captions. This includes the graphics.
2. **Type is the picture.** The visuals are typographic. No icon set, no illustration, no stock.
3. **One column.** A reading page. Never a grid of cards.
4. **Space carries rank.** Importance is shown by how much room something gets, not by colour or weight.
5. **Print is the real medium.** The screen version is a preview of the paper version.
6. **Nothing loads.** No CDN, no web font fetch, no script. It works on a laptop with no wifi.
7. **Absence is visible.** A missing answer gets a line saying it is missing, in the same type as
   everything else. It is never quietly dropped.

### Reference anchors

Pulled from Mobbin, not from memory. Each contributes one specific thing.

| Reference | What it contributes |
|---|---|
| [Kinfolk](https://mobbin.com/sites/sections/1557474b-af5b-48e0-b8d3-541af616713b) | The full-width hairline above the header, the small all-caps kicker, the serif deck underneath |
| [SSENSE](https://mobbin.com/sites/sections/4de98a06-dbff-4e54-83c6-a301c519bba0) | One enormous statement, centred, no chrome around it. This is section 1 |
| [TIDAL](https://mobbin.com/sites/sections/356d601a-f6c9-4b62-a844-524df05e7ff1) | Single-column article measure, black-and-white band, byline in small type |
| [Vucko](https://mobbin.com/sites/sections/72f31890-b4dd-46f4-b6f6-11ce33361d24) | The huge numeral in the left margin next to a statement, thin rule beneath, small supporting text. This is visual slot 2 |
| [Duna](https://mobbin.com/sites/sections/17bdeb3c-afab-4461-a607-d0e407846c87) | Restraint in a three-part row: generous space, small labels, no boxes |

## 3. Colour

```css
--ink:    #0A0A0A;   /* all text, all graphics */
--paper:  #FFFFFF;   /* page */
--muted:  #6B6B6B;   /* caption text, source pointers, the "not answered" line */
--rule:   #C9C9C9;   /* 1px hairlines only. Never text */
```

Four values. Nothing else, ever, including inside the SVG. No gradient, no shadow, no tint of ink
used as a fifth colour.

The split between `--muted` and `--rule` matters. A source pointer is the credibility of the whole
page and has to be readable on paper, so it gets `--muted` at 4.9:1 contrast. `--rule` is for
hairlines and touches no text ever. Setting caption text in hairline grey makes it vanish on an
office printer, which is exactly where it is needed.

## 4. Type

System stack. No font is fetched over the network.

```css
--serif: ui-serif, "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
--sans:  ui-sans-serif, -apple-system, "Helvetica Neue", Arial, sans-serif;
--mono:  ui-monospace, "SF Mono", Menlo, Consolas, monospace;
```

| Role | Family | Size | Weight | Tracking | Leading |
|---|---|---|---|---|---|
| The one sentence | serif | `clamp(2.75rem, 6vw, 5rem)` | 400 | -0.02em | 1.05 |
| Section heading | sans | `0.75rem` | 600 | 0.16em, uppercase | 1 |
| Must-solve statement | serif | `clamp(1.6rem, 3vw, 2.4rem)` | 400 | -0.01em | 1.15 |
| Margin numeral | sans | `clamp(4rem, 9vw, 8rem)` | 300 | -0.04em | 0.8 |
| Body | serif | `1.125rem` | 400 | 0 | 1.6 |
| Caption, source pointer | sans | `0.8125rem` | 400 | 0 | 1.45 |
| `[TO FILL: …]` | mono | `0.8125rem` | 400 | 0 | 1.45 |

Sentence case in headings. Never title case.

`[TO FILL: …]` is set in mono with a 1px `--rule` border and 2px padding. It has to look like a hole
in the page, because that is what it is.

## 5. Layout

```css
--measure: 34rem;        /* ~65 characters */
--margin:  12rem;        /* left gutter for numerals, collapses under 900px */
--gap-section: 7rem;
--gap-block:   2.5rem;
```

One column, centred, `--measure` wide. The left margin holds numerals and section labels and is the
only thing that ever sits outside the measure.

Vertical rhythm: `--gap-section` between the six sections, `--gap-block` between items inside one.
Space is the only separator. No boxes, no cards, no background fills.

Under 900px the margin collapses and numerals move above their statement.

## 6. Components

**Section head.** A 1px `--rule` hairline the full width of the measure, then the label in small
uppercase sans, then `--gap-block`. Nothing else. From Kinfolk.

**The one sentence.** Serif at the largest size, centred, and **wider than the measure** — it
breaks out to `48rem` so a long sentence does not wrap six times. Alone on the screen, `6rem` above
and below. Nothing may share this space. From SSENSE.

**Must-solve block.** Numeral in the left margin at `--margin` size. Statement in serif to its right.
A 1px hairline beneath the pair, full measure. Supporting line in caption sans, in `--muted`, under the hairline.
Repeat three times. From Vucko.

**Stop / start split.** Two columns, equal width, separated by a single 1px vertical hairline.
Left column headed `STOPS`, right headed `STARTS`, both in section-head type. Items in body serif.

**The bet.** A three-part row: assumption, test, date. Separated by `→` in `--rule`. Labels and body in `--ink`. Labels in
caption sans above each part. From Duna's restraint — no boxes.

**Source pointer.** Caption sans, in `--muted`, in brackets, at the end of the claim it belongs to:
`(annual-plan-2027.md, p.12)`.

**The not-answered line.** Body serif, italic, in `--muted`:
*The plan does not say what this costs.* Always a full sentence, never a dash or a blank.

**Footer.** On every page: run date, source folder, and the line `AI-supported draft`. Caption sans in `--muted`, above a full-width hairline.

## 7. The four visual slots

This section owns how each slot looks. What fills them is defined in
`skills/simply/references/output-structure.md`, and the sections themselves in
`skills/simplify/references/output.md`. One definition each, so they cannot drift apart.

| Slot | Form |
|---|---|
| 1 | Type only, full bleed, wider than the measure. No graphic |
| 2 | Three numeral-and-statement blocks, hairline under each |
| 3 | Vertical split, one 1px hairline between the columns |
| 4 | A three-part row, separated by `→` in `--rule` |

All inline SVG or plain HTML. No `<img>`, ever.

A slot whose content is missing is dropped. An empty graphic is worse than no graphic.

## 8. Print

```css
@media print {
  @page { size: A4; margin: 18mm; }
  html { font-size: 11pt; }
  section { break-inside: avoid; }
  h1, h2 { break-after: avoid; }
  .one-sentence { break-after: page; }
  .footer { position: fixed; bottom: 0; }
}
```

The page has to survive a black-and-white office printer. That is why there is no colour and no
grey fill: a 40% tint prints as a smear.

Test it by printing, not by looking at print preview.

## 9. Hard rules

- Four colour values. No fifth. `--rule` never touches text.
- No `<img>`, no icon library, no emoji, no CDN, no JavaScript.
- No box shadow, no border radius above 0, no gradient.
- Sentence case in every heading.
- No em dashes in the copy. The de-slop filter strips them.
- Every claim carries a source pointer, or it does not go on the page.
- Every file self-contained. CSS in a `<style>` block, SVG inline.
- The footer stamp `AI-supported draft` appears on every printed page.
