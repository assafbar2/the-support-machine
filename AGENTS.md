# Repository Instructions

This repository packages **The Support Machine** as a public book and practical AI skills.

- Preserve the machine, Rubicon, zero hour, goalkeeper and midfield, wizard, tollbooth, shadow run, and launch inventory metaphors.
- Never invent customer results. Separate facts, author experience, proposals, fictional cases, and prototype demonstrations.
- Challenge claims with relevant primary sources; date vendor capabilities and distinguish announcement, availability, and observed results.
- Keep skill instructions compact. Use references for depth and templates for reusable work.
- The reader-facing title is **The Support Machine — Second Edition**. `v0.4` is a repository release identifier, not a third edition.
- The current canonical formatted source is `manuscript/The Support Machine - manuscript v0.4.docx`.
- Export `skills/the-support-machine/references/book.md` from the DOCX; it is the agent-readable full text, not a competing canonical source.
- A complete Markdown working draft may be imported for a substantial revision. Then inspect the DOCX and regenerate all downstream outputs.
- Follow `CONTRIBUTING.md` for rendering, build and verification. Visually review every PDF page before delivery.
- Preserve previous edition files and archive checksums. Keep version metadata, reader notes, changelog, downloads and skills consistent.
- Do not publish, send customer communications, or make production changes merely because a template describes them.

```bash
python scripts/export_docx_to_markdown.py \
  "manuscript/The Support Machine - manuscript v0.4.docx" \
  skills/the-support-machine/references/book.md
```
