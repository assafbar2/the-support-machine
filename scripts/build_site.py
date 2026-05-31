from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_MD = ROOT / "skills/the-support-machine/references/book.md"
DOCS = ROOT / "docs"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"_([^_]+)_", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def parse_table(lines: list[str], start: int) -> tuple[str, int]:
    rows = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        rows.append(cells)
        i += 1
    if len(rows) < 2:
        return inline(lines[start]), start + 1
    header = rows[0]
    body = rows[2:]
    parts = ["<div class=\"table-wrap\"><table><thead><tr>"]
    parts.extend(f"<th>{inline(cell)}</th>" for cell in header)
    parts.append("</tr></thead><tbody>")
    for row in body:
        parts.append("<tr>")
        parts.extend(f"<td>{inline(cell)}</td>" for cell in row)
        parts.append("</tr>")
    parts.append("</tbody></table></div>")
    return "".join(parts), i


def markdown_to_html(markdown: str) -> tuple[str, list[tuple[int, str, str]]]:
    lines = markdown.splitlines()
    out: list[str] = []
    toc: list[tuple[int, str, str]] = []
    list_open = False
    para: list[str] = []
    code_open = False
    code_lines: list[str] = []

    def flush_para() -> None:
        nonlocal para
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para = []

    def close_list() -> None:
        nonlocal list_open
        if list_open:
            out.append("</ul>")
            list_open = False

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if line.startswith("```"):
            flush_para()
            close_list()
            if code_open:
                out.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_open = False
                code_lines = []
            else:
                code_open = True
            i += 1
            continue
        if code_open:
            code_lines.append(raw)
            i += 1
            continue
        if not line:
            flush_para()
            close_list()
            i += 1
            continue
        if line.startswith("|"):
            flush_para()
            close_list()
            table, i = parse_table(lines, i)
            out.append(table)
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush_para()
            close_list()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            anchor = slugify(text)
            toc.append((level, text, anchor))
            out.append(f"<h{level} id=\"{anchor}\">{inline(text)}</h{level}>")
        elif line.startswith("> "):
            flush_para()
            close_list()
            out.append(f"<blockquote>{inline(line[2:].strip())}</blockquote>")
        elif line.startswith("- "):
            flush_para()
            if not list_open:
                out.append("<ul>")
                list_open = True
            out.append(f"<li>{inline(line[2:].strip())}</li>")
        elif re.match(r"^\d+\.\s+", line):
            flush_para()
            if not list_open:
                out.append("<ul>")
                list_open = True
            out.append(f"<li>{inline(re.sub(r'^\\d+\\.\\s+', '', line))}</li>")
        elif re.match(r"^PART [IVX]+$", line):
            flush_para()
            close_list()
            anchor = slugify(line)
            toc.append((2, line, anchor))
            out.append(f"<h2 class=\"part\" id=\"{anchor}\">{line}</h2>")
        else:
            para.append(line)
        i += 1
    flush_para()
    close_list()
    return "\n".join(out), toc


def page_shell(title: str, body: str, description: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  {body}
</body>
</html>
"""


def build() -> None:
    DOCS.mkdir(exist_ok=True)
    book = BOOK_MD.read_text()
    filtered: list[str] = []
    skipped_duplicate_title = False
    for line in book.splitlines():
        stripped = line.strip()
        if stripped.startswith("> Markdown export of the manuscript."):
            continue
        if not skipped_duplicate_title and stripped == "The Support Machine" and filtered:
            skipped_duplicate_title = True
            continue
        filtered.append(line)
    book = "\n".join(filtered)
    book_html, toc = markdown_to_html(book)
    toc_items = "\n".join(
        f'<a class="toc-l{level}" href="#{anchor}">{html.escape(text)}</a>'
        for level, text, anchor in toc
        if level <= 2
    )

    (DOCS / "index.html").write_text(
        page_shell(
            "The Support Machine",
            """
<main class="home">
  <p class="eyebrow">Book + executable AI skill</p>
  <h1>The Support Machine</h1>
  <p class="dek">How to deploy AI in customer support without breaking trust.</p>
  <div class="actions">
    <a href="book.html">Read online</a>
    <a href="the-support-machine-v0.2.pdf">Download PDF</a>
    <a href="skill.html">Use the skill</a>
  </div>
  <section class="thesis">
    <p>AI support is not a chatbot project. It is an operating model migration.</p>
    <p>A bot answers. A support machine routes, reasons, retrieves, escalates, measures, learns, and changes the work humans do around it.</p>
  </section>
</main>
""",
            "The Support Machine book and AI skill.",
        )
    )

    (DOCS / "book.html").write_text(
        page_shell(
            "Read The Support Machine",
            f"""
<div class="reader-layout">
  <aside class="sidebar">
    <a class="brand" href="index.html">The Support Machine</a>
    <nav>{toc_items}</nav>
  </aside>
  <main class="book">
    <div class="book-actions">
      <a href="index.html">Home</a>
      <a href="the-support-machine-v0.2.pdf">PDF</a>
      <a href="skill.html">Skill</a>
    </div>
    {book_html}
  </main>
</div>
""",
            "Read The Support Machine online.",
        )
    )

    (DOCS / "skill.html").write_text(
        page_shell(
            "Use The Support Machine Skill",
            """
<main class="skill-page">
  <a class="back" href="index.html">The Support Machine</a>
  <h1>Use the skill</h1>
  <p>The skill turns the book into an operating guide. Use it when you are planning, auditing, launching, or operating AI customer support.</p>
  <section>
    <h2>Install locally</h2>
    <pre><code>mkdir -p ~/.codex/skills
git clone https://github.com/assafbar2/the-support-machine.git
cp -R the-support-machine/skills/the-support-machine ~/.codex/skills/</code></pre>
    <p>Restart Codex so the skill is loaded.</p>
  </section>
  <section>
    <h2>Ask it for artifacts</h2>
    <pre><code>Use The Support Machine to build our AI support rollout plan.
Use The Support Machine to evaluate this AI support vendor.
Use The Support Machine to create a launch-day runbook.
Use The Support Machine to review our first 30 days.</code></pre>
  </section>
  <section>
    <h2>Source</h2>
    <p><a href="https://github.com/assafbar2/the-support-machine/tree/main/skills/the-support-machine">View the skill folder on GitHub</a></p>
  </section>
</main>
""",
            "How to install and use The Support Machine AI skill.",
        )
    )

    (DOCS / "styles.css").write_text(CSS)
    (DOCS / ".nojekyll").write_text("")


CSS = r"""
:root {
  color-scheme: light;
  --ink: #141414;
  --muted: #64625d;
  --line: #d8d2c5;
  --paper: #fbfaf6;
  --panel: #f2efe7;
  --accent: #b13d22;
  --accent-dark: #772817;
  --code: #eee8db;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.62;
}
a { color: var(--accent-dark); text-decoration-thickness: 1px; text-underline-offset: 3px; }
.home, .skill-page {
  min-height: 100vh;
  max-width: 980px;
  margin: 0 auto;
  padding: 8vh 24px 12vh;
}
.eyebrow {
  margin: 0 0 24px;
  color: var(--accent-dark);
  font: 700 13px/1.2 ui-monospace, SFMono-Regular, Menlo, monospace;
  letter-spacing: 0;
  text-transform: uppercase;
}
h1 {
  max-width: 820px;
  margin: 0;
  font-size: clamp(56px, 11vw, 124px);
  line-height: .88;
  letter-spacing: 0;
}
.dek {
  max-width: 640px;
  margin: 28px 0 0;
  color: var(--muted);
  font-size: 26px;
  line-height: 1.25;
}
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 36px;
}
.actions a, .book-actions a {
  display: inline-flex;
  align-items: center;
  min-height: 42px;
  border: 1px solid var(--ink);
  padding: 8px 14px;
  color: var(--ink);
  text-decoration: none;
  font: 700 13px/1 ui-monospace, SFMono-Regular, Menlo, monospace;
  text-transform: uppercase;
}
.actions a:first-child {
  background: var(--ink);
  color: var(--paper);
}
.thesis {
  margin-top: 72px;
  max-width: 760px;
  border-top: 2px solid var(--ink);
  padding-top: 26px;
  font-size: 24px;
  line-height: 1.36;
}
.reader-layout {
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
}
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: auto;
  border-right: 1px solid var(--line);
  background: var(--panel);
  padding: 22px;
}
.brand {
  display: block;
  margin-bottom: 20px;
  color: var(--ink);
  font: 800 15px/1.2 ui-monospace, SFMono-Regular, Menlo, monospace;
  text-transform: uppercase;
  text-decoration: none;
}
nav a {
  display: block;
  padding: 7px 0;
  color: var(--muted);
  font: 13px/1.25 ui-monospace, SFMono-Regular, Menlo, monospace;
  text-decoration: none;
}
nav a:hover { color: var(--accent-dark); }
.toc-l1 { color: var(--ink); font-weight: 800; margin-top: 8px; }
.toc-l2 { padding-left: 10px; }
.book {
  max-width: 820px;
  padding: 48px 28px 96px;
  margin: 0 auto;
}
.book-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 44px;
}
.book h1 {
  font-size: clamp(44px, 8vw, 84px);
  line-height: .95;
  margin-bottom: 24px;
}
.book h2 {
  margin-top: 68px;
  padding-top: 22px;
  border-top: 1px solid var(--line);
  font-size: 34px;
  line-height: 1.1;
}
.book h3 {
  margin-top: 34px;
  font-size: 22px;
  line-height: 1.2;
}
.book p, .book li, .skill-page p, .skill-page li {
  font-size: 19px;
}
blockquote {
  margin: 28px 0;
  border-left: 4px solid var(--accent);
  padding: 10px 0 10px 18px;
  color: var(--accent-dark);
  background: #f7f0e8;
  font-weight: 700;
}
.part {
  color: var(--accent-dark);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 18px !important;
  text-transform: uppercase;
}
.table-wrap {
  overflow-x: auto;
  margin: 28px 0;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 15px;
  background: #fffdf8;
}
th, td {
  border: 1px solid var(--line);
  padding: 9px 10px;
  vertical-align: top;
}
th {
  text-align: left;
  background: var(--code);
}
pre {
  overflow-x: auto;
  padding: 18px;
  background: var(--code);
  border: 1px solid var(--line);
}
code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .9em;
}
.back {
  display: inline-block;
  margin-bottom: 34px;
  font: 800 13px/1 ui-monospace, SFMono-Regular, Menlo, monospace;
  text-transform: uppercase;
}
@media (max-width: 860px) {
  .reader-layout { display: block; }
  .sidebar {
    position: relative;
    height: auto;
    max-height: 42vh;
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }
  .book { padding-top: 28px; }
  .book-actions { position: sticky; top: 0; background: var(--paper); padding: 10px 0; }
}
"""


if __name__ == "__main__":
    build()
