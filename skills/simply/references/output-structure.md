# The artifact

Six sections and four visual slots. Both fixed. The renderer fills them, it never invents a layout.

## The six sections

| # | Section | Content | Empty when |
|---|---|---|---|
| 1 | **The one sentence** | What this whole folder is actually about | Never. If this cannot be written, the run failed |
| 2 | **The three things that must be solved** | Exactly three, numbered | Never |
| 3 | **What we stop doing** | The sacrifice, per must-solve | Allowed, and then it says so: *the plan does not say what this costs* |
| 4 | **What has to be true** | The bet: assumption, how we test it, when we know | Allowed, and then it says so |
| 5 | **What the documents disagree about** | Named contradictions, both sides quoted | Allowed only if the contradict angle found none, and then it says that explicitly |
| 6 | **What we do not know** | Every `[TO FILL]`, plus every `[MISSING]` Kompas field | Never. An empty section 6 means something was papered over |

Sections 3 to 6 may say "the plan does not answer this". They may not be silently dropped. A missing
section reads as a complete answer, which is the one thing this artifact must never do.

## The four visual slots

| Slot | After section | Shows | Form |
|---|---|---|---|
| 1 | 1 | The one sentence | Type only, full bleed. No graphic |
| 2 | 2 | The three must-solves | Three equal blocks, numbered |
| 3 | 3 | Stop and start | A vertical split. Left what stops, right what starts |
| 4 | 4 | The bet | A row: assumption → test → date |

All four are inline SVG. Black, white, one grey. No gradients, no shadows, no icons from a library.

If a slot has no content — no sacrifice was named, say — the slot is dropped and the section carries
the "the plan does not answer this" line instead. An empty graphic is worse than no graphic.

## reasoning.html

The second file. Four parts, none of which may be empty:

1. **What it read.** The inventory table from `01-spec.md`, including files it could not read.
2. **What it threw away.** Everything demoted to important or nice-to-know, with why. A run that
   discarded nothing is a pass-through, not a process.
3. **Where it is unsure.** Every flag from `05-verdict.md`, every `[TO FILL]`, every `[MISSING]`
   Kompas field. Plus the flatten level the input came in at.
4. **The tension check.** Whether the four angles agreed too much, and which one was sent back.

This is the page that survives a hostile question. Parts 2 and 3 being non-empty is a hard check, not
a preference.

## Rules for both files

- Two colours plus one grey. This includes the SVGs.
- One column, roughly 65 characters wide.
- Self-contained: CSS inline, SVG inline, no CDN, no fonts fetched over the network.
- `@media print` that holds. The paper version is what goes on the table.
- A footer on every page: the run date, the source folder, and the line *AI-supported draft*.
