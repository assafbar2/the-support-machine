"""Build the book website, versioned downloads, notes and complete review text."""
from __future__ import annotations
import html
import json
from pathlib import Path
import re
import shutil
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from render_markdown import markdown_to_html

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BOOK = ROOT / "skills/the-support-machine/references/book.md"
BASE = "https://assafbar2.github.io/the-support-machine/"

def page_shell(title,body,description,css="styles.css"):
    image = BASE+"assets/the-support-machine-social.png"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description,quote=True)}">
<meta property="og:title" content="{html.escape(title,quote=True)}">
<meta property="og:description" content="{html.escape(description,quote=True)}">
<meta property="og:image" content="{image}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{css}">
</head><body>
<a class="skip-link" href="#main">Skip to content</a>
{body}
</body></html>
'''

def downloads(version):
    return f'''<a href="the-support-machine-{version}.pdf">PDF</a>
<a href="downloads/the-support-machine-{version}.docx">Word</a>
<a href="downloads/the-support-machine-{version}.md">Markdown</a>'''

def write(name,title,body,description,css="styles.css"):
    target=DOCS/name
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(page_shell(title,body,description,css))

def build():
    meta=json.loads((ROOT/"edition.json").read_text())
    version,previous=meta["version"],meta["previous"]
    label=version+(" · Review edition" if meta["status"]=="review" else "")
    DOCS.mkdir(exist_ok=True)
    (DOCS/"downloads").mkdir(exist_ok=True)
    for v in (version,previous):
        shutil.copyfile(ROOT/f"manuscript/The Support Machine - manuscript {v}.docx", DOCS/f"downloads/the-support-machine-{v}.docx")
    shutil.copyfile(BOOK,DOCS/f"downloads/the-support-machine-{version}.md")
    book=re.sub(r"^> Markdown export of the manuscript\..*\n","",BOOK.read_text(),flags=re.M)
    book_html,toc=markdown_to_html(book)
    toc_html="\n".join(f'<a class="toc-l{level}" href="#{anchor}">{html.escape(title)}</a>' for level,title,anchor in toc if level<=2)
    actions=f'<div class="book-actions"><a href="index.html">Home</a>{downloads(version)}<a href="notes.html">What changed</a><a href="editions.html">Editions</a></div>'
    reader=f'''<div class="reader-layout"><aside class="sidebar">
<a class="brand" href="index.html">The Support Machine</a>
<p class="edition-label">{html.escape(label)}</p><nav aria-label="Book contents">{toc_html}</nav>
</aside><main class="book" id="main">{actions}{book_html}</main></div>'''
    write("book.html","Read The Support Machine "+version,reader,f"The complete book, with {meta['chapters']} chapters and {meta['appendices']} appendices.")
    write("index.html","The Support Machine",f'''<main class="home" id="main">
<p class="eyebrow">Book + practical AI skills · {html.escape(label)}</p>
<h1>The Support Machine</h1>
<p class="dek">How to deploy AI in customer support without breaking trust.</p>
<div class="actions"><a href="book.html">Read the book</a>{downloads(version)}<a href="skill.html">Use the skills</a></div>
<p class="edition-links"><a href="notes.html">Notes for the new version</a> · <a href="editions.html">Previous editions</a> · <a href="review.html">Complete review text</a></p>
<figure class="hero-preview"><img src="assets/the-support-machine-social.png" alt="Building AI support happening now"></figure>
<section class="thesis"><p>AI support is an operating model migration.</p>
<p>The new edition follows the work beyond launch: customer agents, action receipts, ongoing evaluation, recovery, and support teams that ship improvements.</p></section>
<section class="edition-summary"><h2>Returning to the book?</h2>
<p>Six new chapters and coordinated revisions cover organizational resistance, build versus buy, the 16% problem, customer promises, and the work that never ends after the first answer.</p>
<p><a href="notes.html">See what changed and where to reread.</a> The earlier {previous} edition remains available in its original formats.</p></section>
<p><a href="shadow-run/Shadow-Run-Field-Sheet-v0.13.pdf">Download the Shadow Run field sheet</a></p>
</main>''',"A field guide to deploying and operating AI customer support.")
    notes_html,_=markdown_to_html((ROOT/f"release-notes/{version}.md").read_text())
    write("notes.html","Notes for "+version,f'<main class="book notes-page" id="main">{actions}{notes_html}</main>',"What changed in this edition and why to reread.")
    editions=f'''<main class="skill-page" id="main"><a class="back" href="index.html">The Support Machine</a>
<h1>Editions</h1><h2>{version} · November 1, 2026</h2><p>{html.escape(label)}. {meta['chapters']} chapters, {meta['appendices']} appendices, and two companion skills.</p>
<div class="actions"><a href="book.html">Read online</a>{downloads(version)}<a href="notes.html">Version notes</a></div>
<h2>{previous} · Previous edition</h2><p>The original PDF, Word manuscript, and Markdown are preserved. The archived online book keeps the previous text and styling.</p>
<div class="actions"><a href="editions/{previous}/book.html">Read {previous}</a>{downloads(previous)}</div>
<p>The repository's previous public tag is {previous}; no v1.0 edition was present. Version numbers follow that existing sequence.</p></main>'''
    # The previous Markdown download uses the preserved archive.
    shutil.copyfile(DOCS/f"editions/{previous}/book.md",DOCS/f"downloads/the-support-machine-{previous}.md")
    write("editions.html","Editions of The Support Machine",editions,"Current and preserved previous editions in every book format.")
    write(f"editions/{previous}/index.html",f"The Support Machine {previous}",f'''<main class="skill-page" id="main">
<h1>The Support Machine</h1><p>Preserved {previous} edition.</p>
<p><a href="book.html">Read the original text</a> · <a href="../../the-support-machine-{previous}.pdf">PDF</a> · <a href="../../downloads/the-support-machine-{previous}.docx">Word</a> · <a href="book.md">Markdown</a></p>
<p><a href="../../editions.html">All editions</a></p></main>''',"Preserved previous edition.","../../styles.css")
    review_intro='<p class="review-notice">Complete v0.3 text for review. This includes every chapter, all appendices, and the front matter. The version notes summarize changes; the text below is the full book.</p>'
    write("review.html","The Support Machine complete review text",reader.replace(actions,actions+review_intro,1),"All of the new edition for review.")
    (ROOT/"review").mkdir(exist_ok=True)
    (ROOT/f"review/{version}-complete-text.md").write_text(book)
    ref = f"codex/support-machine-{version}" if meta["status"]=="review" else "main"
    install_prompt = f"$skill-installer Install skills/the-support-machine from GitHub repository assafbar2/the-support-machine, ref {ref}."
    write("skill.html","Use The Support Machine Skills",f'''<main class="skill-page" id="main">
<a class="back" href="index.html">The Support Machine</a><h1>Use the skills</h1>
<p>The book is already packaged as a skill. The {version} bundle contains the complete revised manuscript, all eight appendices, podcast additions, and fourteen practical templates. <a href="book.html#appendix-g-talk-to-the-book">Start with Appendix G for setup and 80 prompts.</a></p>
<h2>The Support Machine</h2><p>For the full migration and operating model: build versus buy, vendors, release gates, action safety, customer promises, recovery, and team design.</p>
<p><a href="downloads/the-support-machine.zip">Download the skill ZIP</a> · <a href="downloads/the-support-machine.skill">.skill package</a></p>
<h2>Install in Claude</h2><p>Leave the ZIP zipped. In Customize → Skills, choose + → Create skill → Upload a skill. Upload the ZIP and enable it. Code execution and file creation must be enabled; organization policy may control availability. Start with “Use The Support Machine skill to help me with [decision].”</p>
<h2>Install in Codex</h2><p>Ask the built-in installer:</p><pre><code>{html.escape(install_prompt)}</code></pre>
<p>Invoke <code>$the-support-machine</code> followed by your task. Restart Codex if the skill does not appear. For manual installation, copy the complete skill folder, including references and templates, into <code>~/.agents/skills/</code>.</p>
<h2>Verify and update your copy</h2><p>Ask the skill to read its bundled book reference, identify {version}, and locate Chapter 28 and the build-versus-buy template. Install the new package when a new edition arrives; a local or uploaded copy does not automatically follow the GitHub repository. Keep company-specific notes separately.</p>
<h2>Support AI Evals</h2><p>For ongoing QA: delayed outcome checks, independent review, calibration, knowledge changes, and a local cohort calculator. It reads normalized local data and does not connect to a helpdesk.</p>
<p><a href="downloads/support-ai-evals.zip">Download the evaluation skill ZIP</a> · <a href="downloads/support-ai-evals.skill">.skill package</a>. This optional skill works independently; install it separately if useful.</p>
<h2>Try a concrete task</h2><pre><code>Use The Support Machine to compare buying, extending, and building our support agent.
Use The Support Machine to rehearse an action whose result is unknown.
Use Support AI Evals to review our seven-day repeat-contact cohort.
Use Support AI Evals to design a calibrated comparison of two QA systems.</code></pre>
<p><a href="https://github.com/assafbar2/the-support-machine">Repository and installation instructions</a></p>
<p>Current platform guidance: <a href="https://learn.chatgpt.com/docs/build-skills">OpenAI Build skills</a> · <a href="https://support.claude.com/en/articles/12512180-use-skills-in-claude">Use skills in Claude</a>.</p>
</main>''',"Two focused skills and their practical tools.")
    for skill in ("the-support-machine","support-ai-evals"):
        source=ROOT/"skills"/skill
        entries=[(path,str(path.relative_to(ROOT/"skills"))) for path in sorted(source.rglob("*"))
                 if path.is_file() and "__pycache__" not in path.parts and path.suffix!=".pyc"]
        if skill=="the-support-machine":
            entries += [(ROOT/name,f"{skill}/{name}") for name in ("LICENSE.md","LICENSE-MANUSCRIPT.md","LICENSE-SKILL.md")]
        else:
            entries.append((ROOT/"LICENSE-SKILL.md",f"{skill}/LICENSE.md"))
        with ZipFile(DOCS/f"downloads/{skill}.skill","w",compression=ZIP_DEFLATED) as bundle:
            for path,archive_name in sorted(entries,key=lambda entry:entry[1]):
                stamp=tuple(map(int,meta["date"].split("-")))+(0,0,0)
                info=ZipInfo(archive_name,stamp)
                info.compress_type=ZIP_DEFLATED
                info.create_system=3
                info.external_attr=0o100644 << 16
                bundle.writestr(info,path.read_bytes())
        shutil.copyfile(DOCS/f"downloads/{skill}.skill", DOCS/f"downloads/{skill}.zip")
    (DOCS/".nojekyll").write_text("")
    (DOCS/"llms.txt").write_text((ROOT/"llms.txt").read_text())

if __name__=="__main__":
    build()
