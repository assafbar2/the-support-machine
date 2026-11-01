# Contributing

Preserve the direct field-guide voice and the machine, Rubicon, goalkeeper, wizard, tollbooth, shadow-run, launch-inventory, and zero-hour metaphors. Keep facts, proposals, fictional scenarios, and prototypes distinguishable. Never invent customer results.

## Manuscript workflow

The current formatted canonical source is `manuscript/The Support Machine - manuscript v0.3.docx`. Edit that file and regenerate downstream text:

```bash
python scripts/export_docx_to_markdown.py \
  "manuscript/The Support Machine - manuscript v0.3.docx" \
  skills/the-support-machine/references/book.md
```

For a major revision drafted in Markdown, use `scripts/import_markdown_to_docx.py working-draft.md output.docx`, inspect the resulting DOCX, then export it as above. The importer supports the book's flat Markdown subset: headings, lists, tables, paragraphs, quotes, code, and inline links/emphasis. Do not commit an unexplained competing canonical manuscript.

The exporter preserves hyperlinks, internal contents links, list numbers, emphasis, and tables. Keep generation changes in the same PR as affected outputs.

## Build every format

Install Python 3.10+ and `requirements.txt`. PDF conversion needs LibreOffice; render the canonical DOCX before copying its PDF into the release:

```bash
soffice --headless --convert-to pdf --outdir /tmp/support-book-render \
  "manuscript/The Support Machine - manuscript v0.3.docx"
python scripts/build_edition.py --pdf \
  "/tmp/support-book-render/The Support Machine - manuscript v0.3.pdf"
python -m unittest discover -s tests -v
python scripts/verify_edition.py
```

The build exports Markdown, copies the supplied rendered PDF, and regenerates HTML, versioned downloads, complete review text, the label-free reading copy, and matching ZIP/.skill packages. It does not modify the previous canonical DOCX/PDF. CSS in `docs/styles.css` is maintained directly.

Render and visually inspect every PDF page. Check the cover, contents, chapter starts, tables, field notes, page breaks and links. Text extraction and automated checks do not replace visual review.

The reading copy is a byte-for-byte copy of the canonical DOCX, so its visual verification uses the same render. The build and edition verifier check that equality. Keep editorial directions in this file or the research/review records, never in reader-facing chapter endings. Audit names, visible placeholders, and authoring residue when revising the manuscript. Reader prompts in Appendix G are intentional examples.

## Claims and release notes

Check time-sensitive product claims against current primary documentation. Record dates and limits in `research/`; keep the reader's version notes focused on what changed and why to reread. Preserve uncertainty and don't confuse an announcement with workspace access.

Update `edition.json`, `CHANGELOG.md`, reader notes, and the coverage record. Preserve previous editions and verify the archive checksums. Do not overwrite an old version to save a filename.

v0.3 is a review edition until accepted. Publication is a separate action: update the release status and the review-branch installation links in Appendix G and the README, regenerate all formats, merge the reviewed changes, verify Pages, and create a GitHub release with the versioned PDF, DOCX, Markdown and skill packages. Do not create or move a release tag before that decision.

## Skills and tests

Keep main instructions compact and use references/templates for detail. The evaluation skill remains standalone and its calculator never fetches customer data. Test meaningful cohort boundaries and failures when changing it. The prompts in `evals/evals.json` describe behavioral acceptance cases; they are not claims that a model evaluation has already run.

The main package must include the current canonical Markdown export and every template. ZIP and .skill downloads contain identical bytes; the verifier compares each packaged resource with its source. Keep installation instructions at the start of Appendix G and verify platform-specific steps against current official documentation.

## Contributions and licensing

Open a PR against main with the problem, resulting behavior, evidence, and relevant validation. Book text and formats are CC BY 4.0; reusable skills, templates, code, and repo documentation are MIT. See `LICENSE.md`.
