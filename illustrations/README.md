# Book illustrations

The ten illustrations use a shared black-and-white architectural sketch style. The figures and their book-layout versions are generated into `docs/illustrations/`; the gallery there shows the complete set.

`briefs.json` preserves the concepts and their intended meaning. `draw_illustrations.py` generates editable SVG originals using Python's standard library. `render_illustrations.mjs` renders them with Sharp. It accepts an existing package directory through `SUPPORT_NODE_MODULES`.

```sh
python illustrations/draw_illustrations.py
node illustrations/render_illustrations.mjs
```

Full PNGs are 1950 × 1333 pixels at 300 DPI. Book PNGs crop the repeated title and takeaway from the full figure; the manuscript supplies that information in an adjacent caption. The artwork keeps its aspect ratio and is inserted inline with alternative text.

Handwritten accents use Bradley Hand when available and fall back to locally available fonts in SVG viewers. PNGs preserve the rendered appearance. Do not redistribute the font file.

After changing an illustration, update the manuscript images with `scripts/insert_illustrations.py`, render the canonical DOCX, inspect every page, and run the edition build. The DOCX exporter writes the embedded images beside the Markdown reference so the skill package remains self-contained.

Illustration artwork is part of the book and is CC BY 4.0. Generator scripts are MIT, as described in the repository license files.
