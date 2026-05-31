from __future__ import annotations

import sys
import re
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("lie.It’s", "lie. It’s")
    text = text.replace("Accuracy:Of", "Accuracy: Of")
    text = text.replace("whywe", "why we")
    text = text.replace("like<a ", "like <a ")
    return text.strip()


def table_to_markdown(table) -> list[str]:
    rows = []
    for row in table.rows:
        rows.append([clean_text(cell.text.replace("\n", " ")) for cell in row.cells])
    if not rows:
        return []
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    lines = ["| " + " | ".join(rows[0]) + " |"]
    lines.append("| " + " | ".join(["---"] * width) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    return lines


def export_docx(src: Path, dst: Path) -> None:
    doc = Document(src)
    lines = [
        "# The Support Machine",
        "",
        f"> Markdown export of the manuscript. The canonical formatted source is `manuscript/{src.name}`.",
        "",
    ]

    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            p = Paragraph(child, doc)
            text = clean_text(p.text)
            if not text:
                continue
            style = p.style.name
            if style == "Title":
                lines.extend([f"# {text}", ""])
            elif style == "Heading 1":
                lines.extend([f"## {text}", ""])
            elif style == "Heading 2":
                lines.extend([f"### {text}", ""])
            elif style == "Heading 3":
                lines.extend([f"#### {text}", ""])
            elif style == "List Bullet":
                lines.append(f"- {text}")
            elif style == "List Number":
                lines.append(f"1. {text}")
            elif style == "Quote":
                lines.extend([f"> {text}", ""])
            else:
                lines.extend([text, ""])
        elif child.tag == qn("w:tbl"):
            lines.extend(table_to_markdown(Table(child, doc)))

    markdown = "\n".join(line.rstrip() for line in lines).rstrip() + "\n"
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    dst.write_text(markdown)


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: export_docx_to_markdown.py input.docx output.md", file=sys.stderr)
        raise SystemExit(2)
    export_docx(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
