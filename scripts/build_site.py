"""Build the book website, edition downloads, notes and archives."""
from __future__ import annotations
from datetime import date
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
REPO = "https://github.com/assafbar2/the-support-machine"

def page_shell(title,body,description,css="styles.css",url=BASE):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description,quote=True)}">
<meta name="author" content="Assaf Barnir">
<meta property="og:title" content="{html.escape(title,quote=True)}">
<meta property="og:description" content="{html.escape(description,quote=True)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{html.escape(url,quote=True)}">
<meta property="og:image" content="{BASE}assets/second-edition-social.png">
<meta property="og:image:alt" content="The Support Machine by Assaf Barnir — Second Edition">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{html.escape(url,quote=True)}">
<link rel="stylesheet" href="{css}">
</head><body>
<a class="skip-link" href="#main">Skip to content</a>
{body}
</body></html>
'''

def downloads(version):
    links=f'''<a href="the-support-machine-{version}.pdf">PDF</a>
<a href="downloads/the-support-machine-{version}.docx">DOCX</a>
<a href="downloads/the-support-machine-{version}.md">Markdown</a>'''
    if (DOCS/f'downloads/the-support-machine-{version}-markdown.zip').exists():
        links+=f'\n<a href="downloads/the-support-machine-{version}-markdown.zip">Markdown + images</a>'
    return links

def write(name,title,body,description,css="styles.css"):
    target=DOCS/name
    target.parent.mkdir(parents=True,exist_ok=True)
    url = BASE if name == "index.html" else BASE + name
    target.write_text(page_shell(title,body,description,css,url))

def edition_summary(meta):
    """Build agent-readable metadata with links to the edition's actual location."""
    version = meta['version']
    review = meta['status'] == 'review'
    ref = f'codex/support-machine-{version}' if review else 'main'
    raw = f'https://raw.githubusercontent.com/assafbar2/the-support-machine/{ref}/'
    reading_base = raw + 'docs/' if review else BASE
    notes = raw + f'release-notes/{version}.md' if review else BASE + 'notes.html'
    previous = f'{REPO}/tree/{ref}/docs/editions/{meta["previous"]}' if review else BASE + 'editions.html'
    label = meta['name'] + (' · Review copy' if review else '')
    artifact = version if review else meta['slug']
    return f'''# The Support Machine

> A field guide by Assaf Barnir to deploying and operating AI customer support without breaking trust.

{label}, {meta['date']}. {meta['chapters']} chapters, {meta['appendices']} appendices, {meta['illustrations']} illustrations, and two companion skills.

## Read

- [Full book in Markdown]({reading_base}downloads/the-support-machine-{artifact}.md)
- [PDF]({reading_base}the-support-machine-{artifact}.pdf)
- [DOCX]({reading_base}downloads/the-support-machine-{artifact}.docx)
- [What is new in the Second Edition]({notes})
- [Previous edition]({previous})
- [Read the Second Edition online]({BASE}book.html)

## Apply

- [The Support Machine skill]({REPO}/tree/{ref}/skills/the-support-machine)
- [Support AI Evals skill]({REPO}/tree/{ref}/skills/support-ai-evals)

The Support Machine skill contains the complete book and reusable templates. Appendix G starts with installation and includes 80 practical prompts. Support AI Evals covers continuing QA and a local cohort calculator. Each skill installs independently.

Keep reported resolution, reviewed quality, and later customer evidence separate. Use mature observation windows and declared coverage. Customer silence alone does not prove success. Verify account authority and action effects. Preserve legitimate objections, a tested human path, and controlled knowledge releases.

This is Assaf Barnir's personal project and does not speak for Sentry. Book text is CC BY 4.0; skills, templates, scripts, and repository documentation are MIT. See the repository's license files for terms.
'''

def build():
    meta=json.loads((ROOT/"edition.json").read_text())
    version,previous=meta["version"],meta["previous"]
    label=meta["name"]+(" · Review copy" if meta["status"]=="review" else "")
    artifact=meta["slug"]
    previous_label=meta["previous_name"]
    edition_date=date.fromisoformat(meta['date'])
    date_label=f'{edition_date:%B} {edition_date.day}, {edition_date.year}'
    DOCS.mkdir(exist_ok=True)
    (DOCS/"downloads").mkdir(exist_ok=True)
    for v in (version,previous):
        shutil.copyfile(ROOT/f"manuscript/The Support Machine - manuscript {v}.docx", DOCS/f"downloads/the-support-machine-{v}.docx")
    shutil.copyfile(BOOK,DOCS/f"downloads/the-support-machine-{version}.md")
    image_source=BOOK.parent/'illustrations'
    if image_source.exists():
        shutil.copytree(image_source,DOCS/'downloads/illustrations',dirs_exist_ok=True)
        with ZipFile(DOCS/f'downloads/the-support-machine-{version}-markdown.zip','w',compression=ZIP_DEFLATED) as bundle:
            entries=[(BOOK,'book.md'),(ROOT/'LICENSE-MANUSCRIPT.md','LICENSE-MANUSCRIPT.md')]
            entries += [(p,'illustrations/'+p.name) for p in sorted(image_source.glob('*.png'))]
            for path,member in entries:
                info=ZipInfo(member,tuple(map(int,meta['date'].split('-')))+(0,0,0))
                info.compress_type=ZIP_DEFLATED
                info.create_system=3
                info.external_attr=0o100644 << 16
                bundle.writestr(info,path.read_bytes())
    # Reader-facing filenames identify the edition; release-number paths stay valid.
    for suffix in ('pdf','docx','md','markdown.zip'):
        folder=DOCS if suffix=='pdf' else DOCS/'downloads'
        source=folder/f'the-support-machine-{version}.{suffix}' if suffix!='markdown.zip' else folder/f'the-support-machine-{version}-markdown.zip'
        destination=folder/f'the-support-machine-{artifact}.{suffix}' if suffix!='markdown.zip' else folder/f'the-support-machine-{artifact}-markdown.zip'
        shutil.copyfile(source,destination)
    book=re.sub(r"^> Markdown export of the manuscript\..*\n","",BOOK.read_text(),flags=re.M)
    book_html,toc=markdown_to_html(book,image_base='downloads')
    toc_html="\n".join(f'<a class="toc-l{level}" href="#{anchor}">{html.escape(title)}</a>' for level,title,anchor in toc if level<=2)
    actions=f'<div class="book-actions"><a href="index.html">Home</a>{downloads(artifact)}<a href="notes.html">What changed</a><a href="editions.html">Editions</a></div>'
    reader=f'''<div class="reader-layout"><aside class="sidebar">
<a class="brand" href="index.html">The Support Machine</a>
<p class="edition-label">{html.escape(label)}</p><nav aria-label="Book contents">{toc_html}</nav>
</aside><main class="book" id="main">{actions}{book_html}</main></div>'''
    write("book.html","The Support Machine — "+meta["name"],reader,f"The complete book, with {meta['chapters']} chapters and {meta['appendices']} appendices.")
    book_schema=json.dumps({
        "@context":"https://schema.org", "@type":"Book", "name":"The Support Machine",
        "bookEdition":meta["name"], "datePublished":meta["date"], "inLanguage":"en",
        "author":{"@type":"Person","name":"Assaf Barnir","url":"https://www.barnir.co/"},
        "url":BASE, "isAccessibleForFree":True,
        "description":"How to Deploy AI in Customer Support Without Breaking Trust",
        "license":"https://creativecommons.org/licenses/by/4.0/"
    })
    write("index.html","The Support Machine — Second Edition",f'''<div class="landing">
<header class="site-header"><a class="site-wordmark" href="index.html">The Support Machine</a>
<nav class="site-nav" aria-label="Main navigation"><a href="#whats-new">What's new</a><a href="skill.html">Use the skills</a><a href="book.html">Read the book <span aria-hidden="true">↗</span></a></nav></header>
<main id="main">
<section class="edition-hero" aria-labelledby="book-title">
<div class="hero-copy"><p class="eyebrow">Second Edition · November 2026</p>
<h1 id="book-title">The Support<br>Machine</h1>
<p class="hero-subtitle">How to Deploy AI in Customer Support Without Breaking Trust</p>
<p class="hero-byline">A field guide by <a href="https://www.barnir.co/">Assaf Barnir</a></p>
<div class="hero-actions"><a class="button button-primary" href="book.html">Read the Second Edition <span aria-hidden="true">↗</span></a><a class="button" href="the-support-machine-{artifact}.pdf">Download PDF <span aria-hidden="true">↓</span></a></div>
<p class="access-note">Free to read, download, and put to work.</p></div>
<figure class="hero-drawing"><div class="drawing-label"><span>From the book</span><span>Gate 2 / 6</span></div>
<img src="illustrations/book/02-choose-the-machine.png" alt="Support architecture split into layers, with a choice to buy, extend, or build at each layer." width="2040" height="993" fetchpriority="high">
<figcaption>Choose the layer before choosing the answer.</figcaption></figure>
</section>
<div class="edition-facts" aria-label="Inside the Second Edition"><p><strong>29</strong> chapters</p><p><strong>10</strong> illustrations</p><p><strong>80</strong> practical prompts</p><p><strong>2</strong> AI skills</p></div>
<section class="new-edition" id="whats-new" aria-labelledby="new-title">
<div class="section-intro"><p class="eyebrow">For returning readers</p><h2 id="new-title">The work continues<br>after launch.</h2><p>Six new chapters, expanded playbooks, and lessons from more use cases, conversations, research, and work with humans and AI.</p></div>
<div class="new-topics"><article><span class="topic-number">01</span><h3>Make the right call</h3><p>Build versus buy, vendor exit risk, and the organizational resistance that can stop progress.</p></article>
<article><span class="topic-number">02</span><h3>Follow the outcome</h3><p>Customer agents, action receipts, recovery, and evaluation seven and thirty days after the answer.</p></article>
<article><span class="topic-number">03</span><h3>Put it to work</h3><p>Collected field notes, fourteen templates, ten drawings, and 80 prompts for your own decisions.</p></article></div>
<a class="text-link" href="notes.html">See what's new and where to reread <span aria-hidden="true">↗</span></a>
</section>
<section class="apply-section" aria-labelledby="apply-title"><div><p class="eyebrow">Read it. Then work with it.</p><h2 id="apply-title">Bring your next<br>support decision.</h2></div><div><p>For support leaders at API, developer-tool, and B2B companies—and the executives who work with them.</p><p>Install the book as a skill. Your assistant can use its chapters and templates to help compare vendors, design evaluations, or rehearse a difficult launch.</p><a class="text-link" href="book.html#appendix-g-talk-to-the-book">Start with Appendix G <span aria-hidden="true">↗</span></a></div></section>
<section class="formats-section" id="downloads" aria-labelledby="formats-title"><h2 id="formats-title">Your copy. Your format.</h2><div class="format-links"><a href="book.html"><span>Read online</span><small>Complete book in your browser</small></a><a href="the-support-machine-{artifact}.pdf"><span>PDF <span aria-hidden="true">↓</span></span><small>Second Edition, ready to keep</small></a><a href="downloads/the-support-machine-{artifact}.docx"><span>DOCX <span aria-hidden="true">↓</span></span><small>For Word or Google Docs</small></a><a href="downloads/the-support-machine-{artifact}-markdown.zip"><span>Markdown <span aria-hidden="true">↓</span></span><small>Full text and illustrations</small></a><a href="skill.html"><span>AI skills <span aria-hidden="true">↗</span></span><small>Installation and practical prompts</small></a></div></section>
<section class="more-section" aria-label="Explore the book"><div><p class="eyebrow">Hear the conversation</p><h2>The Prompt Room</h2><p>I joined Episode 4 to talk about reducing customer pain and how support work is changing. That conversation helped shape this edition.</p><p><a href="https://www.youtube.com/watch?v=JxJb4FDqWdI">Watch on YouTube</a> · <a href="https://open.spotify.com/episode/6x73nZKsh9y1VIw46yCW5q">Listen on Spotify</a></p></div><div><p class="eyebrow">Keep exploring</p><p><a href="illustrations/">The ten illustrations</a></p><p><a href="editions.html">The preserved First Edition</a></p><p><a href="shadow-run/Shadow-Run-Field-Sheet-v0.13.pdf">Shadow Run field sheet</a></p><p><a href="{REPO}">Source and companion tools on GitHub</a></p></div></section>
</main><footer class="site-footer"><p>© Assaf Barnir · <a href="https://www.barnir.co/">barnir.co</a></p><p>A personal field guide. The judgments and recommendations are mine; I do not speak for Sentry.</p><p>Book and illustrations: CC BY 4.0 · Skills and code: MIT</p></footer>
<script type="application/ld+json">{book_schema}</script></div>''',"The Second Edition of Assaf Barnir's free field guide to AI customer support. 29 chapters, ten illustrations, and practical skills for the work after launch.")
    notes_html,_=markdown_to_html((ROOT/f"release-notes/{version}.md").read_text())
    write("notes.html","Notes for the "+meta["name"],f'<main class="book notes-page" id="main">{actions}{notes_html}</main>',"What changed in this edition and why to reread.")
    editions=f'''<main class="skill-page" id="main"><a class="back" href="index.html">The Support Machine</a>
<h1>Editions</h1><h2>{meta["name"]} · {date_label}</h2><p>{html.escape(label)}. {meta['chapters']} chapters, {meta['appendices']} appendices, {meta['illustrations']} illustrations, and two companion skills.</p>
<div class="actions"><a href="book.html">Read online</a>{downloads(artifact)}<a href="notes.html">Edition notes</a></div>
<h2>{previous_label}</h2><p>The original PDF, DOCX, and Markdown remain available, alongside the archived online book.</p>
<div class="actions"><a href="editions/{previous}/book.html">Read the First Edition</a>{downloads(previous)}</div>
</main>'''
    # The previous Markdown download uses the preserved archive.
    shutil.copyfile(DOCS/f"editions/{previous}/book.md",DOCS/f"downloads/the-support-machine-{previous}.md")
    write("editions.html","Editions of The Support Machine",editions,"Current and preserved previous editions in every book format.")
    write(f"editions/{previous}/index.html",f"The Support Machine — {previous_label}",f'''<main class="skill-page" id="main">
<h1>The Support Machine</h1><p>{previous_label} · Preserved in its original form.</p>
<p><a href="book.html">Read the original text</a> · <a href="../../the-support-machine-{previous}.pdf">PDF</a> · <a href="../../downloads/the-support-machine-{previous}.docx">DOCX</a> · <a href="book.md">Markdown</a></p>
<p><a href="../../editions.html">All editions</a></p></main>''',"Preserved previous edition.","../../styles.css")
    # Keep the former reading-copy route useful without presenting review material.
    write("review.html","The Support Machine — Second Edition",'<main class="skill-page" id="main"><h1>The Second Edition is here.</h1><p><a href="book.html">Read the complete book</a> or <a href="notes.html">see what is new</a>.</p></main>',"Read the complete Second Edition.")
    ref = f"codex/support-machine-{version}" if meta["status"]=="review" else "main"
    install_prompt = f"$skill-installer Install skills/the-support-machine from GitHub repository assafbar2/the-support-machine, ref {ref}."
    write("skill.html","Use The Support Machine Skills",f'''<main class="skill-page" id="main">
<a class="back" href="index.html">The Support Machine</a><h1>Use the skills</h1>
<p>The {meta["name"]} skill contains the full book, all {meta['appendices']} appendices, and fourteen practical templates. <a href="book.html#appendix-g-talk-to-the-book">Start with Appendix G for setup and 80 prompts.</a></p>
<h2>The Support Machine</h2><p>For the full migration and operating model: build versus buy, vendors, release gates, action safety, customer promises, recovery, and team design.</p>
<p><a href="downloads/the-support-machine.zip">Download the skill ZIP</a> · <a href="downloads/the-support-machine.skill">.skill package</a></p>
<h2>Install in Claude</h2><p>Leave the ZIP zipped. In Customize → Skills, choose + → Create skill → Upload a skill. Upload the ZIP and enable it. Code execution and file creation must be enabled; organization policy may control availability. Start with “Use The Support Machine skill to help me with [decision].”</p>
<h2>Install in Codex</h2><p>Ask the built-in installer:</p><pre><code>{html.escape(install_prompt)}</code></pre>
<p>Invoke <code>$the-support-machine</code> followed by your task. Restart Codex if the skill does not appear. For manual installation, copy the complete skill folder, including references and templates, into <code>~/.agents/skills/</code>.</p>
<h2>Verify and update your copy</h2><p>Ask the skill to read its bundled book reference, identify the {meta["name"]}, and locate Chapter 28 and the build-versus-buy template. Install the new package when a new edition arrives; a local or uploaded copy does not automatically follow the GitHub repository. Keep company-specific notes separately.</p>
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
    summary=edition_summary(meta)
    (ROOT/"llms.txt").write_text(summary)
    (DOCS/"llms.txt").write_text(summary)

if __name__=="__main__":
    build()
