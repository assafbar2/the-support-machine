# Contributing

Preserve the direct field-guide voice and the machine, Rubicon, goalkeeper, wizard, tollbooth, shadow-run, launch-inventory, and zero-hour metaphors. Keep facts, proposals, fictional scenarios, and prototypes distinguishable. Never invent customer results.

## Manuscript workflow

The current formatted canonical source is `manuscript/The Support Machine - manuscript v0.4.docx`. Edit that file and regenerate downstream text:

```bash
python scripts/export_docx_to_markdown.py \
  "manuscript/The Support Machine - manuscript v0.4.docx" \
  skills/the-support-machine/references/book.md
```

For a major revision drafted in Markdown, use `scripts/import_markdown_to_docx.py working-draft.md output.docx`, inspect the resulting DOCX, then export it as above. The importer supports the book's flat Markdown subset: headings, lists, tables, paragraphs, quotes, code, and inline links/emphasis. Do not commit an unexplained competing canonical manuscript.

The exporter preserves hyperlinks, internal contents links, list numbers, emphasis, tables, and embedded illustrations with alternative text. Image files live beside the Markdown reference and are included in the skill package and the Markdown ZIP. Keep generation changes in the same PR as affected outputs.

The ten illustration sources and regeneration steps are documented in [illustrations/README.md](illustrations/README.md). Refresh the manuscript's inline pictures with `python scripts/insert_illustrations.py` before rendering. That script preserves existing prose and tables, keeps each picture with its caption, and can be rerun after artwork changes.

## Build every format

Install Python 3.10+ and `requirements.txt`. PDF conversion needs LibreOffice; render the canonical DOCX before copying its PDF into the release:

```bash
soffice --headless --convert-to pdf --outdir /tmp/support-book-render \
  "manuscript/The Support Machine - manuscript v0.4.docx"
python scripts/build_edition.py --pdf \
  "/tmp/support-book-render/The Support Machine - manuscript v0.4.pdf"
python -m unittest discover -s tests -v
python scripts/verify_edition.py
```

The build exports Markdown, copies the supplied rendered PDF, and regenerates HTML, versioned downloads, edition-named downloads, and matching ZIP/.skill packages. It does not modify the previous canonical DOCX/PDF. CSS in `docs/styles.css` is maintained directly.

For website presentation updates, run `python scripts/build_site.py` and the existing tests and verifier. The public prompt page is generated directly from `skills/the-support-machine/references/prompts.md`; do not edit a second copy of its prompts. `release-notes/website-checksums.json` tracks the current website separately from the immutable versioned release manifests. Its scope is limited to the listed HTML, stylesheet, and discovery files. Book text, downloads, packages, and historical artifacts still use the release checksums. A website update does not create a new book edition or replace published release assets.

The Shadow Run landing page is rendered by `scripts/shadow_run.py` through the same site build. It uses the existing PDF and preview in `docs/shadow-run/`; preserve those published handout files when updating its presentation.

Render and visually inspect every PDF page. Check the cover, contents, chapter starts, tables, field notes, page breaks and links. Text extraction and automated checks do not replace visual review.

The downloadable DOCX is a byte-for-byte copy of the canonical manuscript. The build and edition verifier check that equality. Keep editorial directions in this file or the research/source records, never in reader-facing chapter endings. Audit names, visible placeholders, and authoring residue when revising the manuscript. Reader prompts in Appendix G are intentional examples.

## Claims and release notes

Check time-sensitive product claims against current primary documentation. Record dates and limits in `research/`; keep the reader's version notes focused on what changed and why to reread. Preserve uncertainty and don't confuse an announcement with workspace access.

Update `edition.json`, `CHANGELOG.md`, reader notes, and the coverage record. Preserve previous editions and verify the archive checksums. Do not overwrite an old version to save a filename.

The current book is the **Second Edition**, first published November 1, 2026. The revised printing uses repository release identifier `v0.4`; `v0.3` identifies the November 1, 2026 printing, and the First Edition uses `v0.2`. Use edition names in all reader-facing text. These technical identifiers do not number the book editions. `edition.json` keeps the edition name, printing date, public download slug, release identifier, and publication status together.

Publish approved changes by regenerating every format, merging the reviewed PR, verifying GitHub Pages and download checksums, and creating the corresponding GitHub release. Existing edition files and tags remain immutable. Public download names use `second-edition`; versioned `v0.3` paths preserve the prior printing.

## Skills and tests

Keep main instructions compact and use references/templates for detail. The evaluation skill remains standalone and its calculator never fetches customer data. Test meaningful cohort boundaries and failures when changing it. The prompts in `evals/evals.json` describe behavioral acceptance cases; they are not claims that a model evaluation has already run.

The main package must include the current canonical Markdown export and every template. ZIP and .skill downloads contain identical bytes; the verifier compares each packaged resource with its source. Keep installation instructions at the start of Appendix G and verify platform-specific steps against current official documentation.

## Contributions and licensing

Open a PR against main with the problem, resulting behavior, evidence, and relevant validation. Book text and formats are CC BY 4.0; reusable skills, templates, code, and repo documentation are MIT. See `LICENSING.md`.
