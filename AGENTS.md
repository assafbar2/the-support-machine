# Repository Instructions

This repository packages **The Support Machine** as a public book manuscript and executable skill.

When editing the skill:

- Keep `skills/the-support-machine/SKILL.md` compact and operational.
- Put long book text in `skills/the-support-machine/references/book.md`.
- Put reusable artifacts in `skills/the-support-machine/templates/`.
- Do not invent customer metrics. Use placeholders and state what evidence is needed.
- Preserve the metaphor system: machine, Rubicon, zero hour, goalkeeper, wizard, tollbooth, shadow run, launch inventory.
- Regenerate `references/book.md` from the DOCX with:

```bash
python scripts/export_docx_to_markdown.py \
  "manuscript/The Support Machine - manuscript v0.2.docx" \
  "skills/the-support-machine/references/book.md"
```
