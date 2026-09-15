# SVG card conventions

Every flashcard is one standalone file in `src/assets/<name>.svg`, 200×200, referenced from
`src/cards.js` (a card's `art` is either an asset name, `{ n: 1..10 }` for `number-N.svg`, or
`{ c: 'red' }` for `color-red.svg`).

```
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img">
  <style> … shared preamble: palette vars + .c-* classes … </style>
  <g> … the art: the only part that differs between cards … </g>
</svg>
```

## The rules

1. **The `<style>` preamble is frozen.** Each file shares its preamble byte-for-byte with 30-160
   siblings; `scripts/preamble-baseline.json` stores the sha256 of every file's preamble and
   `npm run check:assets` fails if one changes. To add a colour or class, change the file that owns
   the preamble *and* re-freeze the baseline deliberately — never for one card alone.
2. **Only the art body changes** — everything between `</style>` and `</svg>`.
3. **Paint with what the file already defines.** Either a class from its own preamble
   (`<circle class="c-cat"/>`) or inline paint from one of its own vars
   (`<path fill="var(--c-cat)" stroke="var(--c-line)" stroke-width="2.5"/>`). A class or `var(--x)`
   that the file does not define paints **solid black** — this is the deck's most common real bug
   (found in `book`, `piano`, `donut`, `violin`, `giraffe`).
4. **Do not add CSS**: no `<style>`, no new selectors, no `@media`, no `style="…"`, no gradients,
   no filters, no `<image>`, no external references.
5. **`<text>` is only allowed on the number cards** (`number-1.svg` … `number-10.svg`).
6. **Geometry**: art stays inside roughly `x∈[16,184]`, `y∈[14,190]`, centred on x=100, and keeps the
   `.shadow` ground ellipse (`cx="100" cy="185" rx="52" ry="9"`, or the file's own values) unless the
   object genuinely floats — a cloud, balloon, kite, plane, moon or rocket has no ground shadow.
7. **Faces**: animals, people and a few toys/shapes have two eyes and a smile. Produce, vehicles,
   food, clothing, furniture and instruments are faceless. Don't add a face to faceless art.
8. **Plural words draw a pair**: `socks`, `shoes`, `boots`, `maracas`, `cherry` (two cherries on one
   stem), `blocks` (a stack).
9. **Countable details are the pedagogy.** Eight octopus arms, five starfish arms, six insect legs,
   three legs per side on a crab, two humps on a camel, five-point stars, 2-3 groupings of black
   piano keys, the day's number of dots on `monday`…`sunday` (Mon 1 … Sun 7), bars of strictly
   decreasing length on a xylophone. Measure these; don't eyeball them.

## Checking your work

```bash
npm run validate        # cards.js ↔ assets: every card has a name in 3 languages and an existing SVG
npm run check:assets    # the 9 rules above, incl. the frozen preambles and the black-paint trap
npm run render:sheets   # contact sheets, one per category, into /tmp/cardsheets
python3 tools/show.py -o /tmp/check/cat.png --size 400 cat dog   # one-off large renders
```

Rendering notes (learned the hard way):

- use headless Chromium with **a fresh `--user-data-dir=$(mktemp -d)`** and
  `--run-all-compositor-stages-before-draw --virtual-time-budget=15000`; without the last two flags
  a sheet screenshots before the `file://` images paint and cells come back blank, and with a shared
  profile Chromium silently clamps `--window-size`, cropping your render.
- render **2-3 icons per sheet**, to a **unique output path per attempt** — images are cached per
  path, and concurrent workers overwrite a shared path such as `/tmp/show.png`.
- if a cell is still blank, inline the SVG as a `data:image/svg+xml;base64,…` URI instead of a
  `file://` `src`.
- look at the PNG. Several defects in this deck (a black bookmark, a bicycle with a detached front
  wheel, a violin whose f-holes were black blobs, a legless elephant) are invisible in markup and
  obvious in a render.
