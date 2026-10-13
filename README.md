# Mow math

Honest lawn mowing arithmetic: the lawn names the minutes, the deck names the stripes, and the clippings name the bag runs.

Live at https://ilanis-agent.github.io/mowmath/

## The three tools

- **Time plan** - minutes = lawn area / (deck width x labeled 85% overlap x walking pace). Bands run from a quick cut to a half-day mow.
- **Stripe plan** - passes = ceil(lawn width / deck width); the last stripe is what the deck leaves behind, with even, tidy and skinny verdicts.
- **Bag plan** - clippings = area x labeled 1.2 L per m2; bag fills = ceil(litres / labeled 40 L catcher).

## Formulas and limits

- Times, widths and volumes are rounded to one decimal (round half up), mirroring the oracle float-for-float.
- Every number the app borrows is labeled in the interface: overlap, clipping rate, bag volume.
- Illustrative time and layout arithmetic only; slopes, wet grass and the mower's manual govern the real mow.

## Development

- `engine.js` - calculation and render engine (browser global `MowMath`, CommonJS for tests).
- `oracle.py` - Python mirror of the engine; regenerates `expected.json`.
- `test.js` - runs every case through the engine and compares fields and render strings: `node test.js`.
