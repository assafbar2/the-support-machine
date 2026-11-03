"""Present the existing prompt library without maintaining a second copy."""
import html
import re
from manuscript_format import blocks, slugify
from render_markdown import inline

SOURCE_URL = 'https://github.com/assafbar2/the-support-machine/blob/main/skills/the-support-machine/references/prompts.md'


def prompt_groups(source):
    groups = []
    pending = None
    for kind, content, level in blocks(source):
        if pending:
            if kind != 'quote':
                raise ValueError('Prompt must be followed by its text: '+pending[0])
            groups[-1]['prompts'].append((*pending, content))
            pending = None
        elif kind == 'heading' and level == 3:
            groups.append({'title': content, 'anchor': slugify(content), 'prompts': []})
        elif kind == 'paragraph' and (match := re.fullmatch(r'\*\*(\d{2})\. (.+)\*\*', content)):
            if not groups:
                raise ValueError('Prompt has no category')
            pending = match.groups()
        elif kind == 'quote':
            raise ValueError('Prompt text has no title')
    if pending:
        raise ValueError('Prompt has no text: '+pending[0])
    numbers = [number for group in groups for number, _, _ in group['prompts']]
    if numbers != [f'{number:02}' for number in range(1, 81)]:
        raise ValueError('The prompt library must contain prompts 01–80 in order')
    return groups


def render_prompt_library(source, book):
    groups = prompt_groups(source)
    prompts = {number: (title, body) for group in groups for number, title, body in group['prompts']}
    opening = re.search(r'Start with this prompt, then choose an example below:\n\n> ([^\n]+)', book)
    if not opening:
        raise ValueError('The working-session opening is missing from Appendix G')
    picks = [
        ('19', 'See what stands between a good demo and a service you can operate.'),
        ('17', 'Include maintenance, evaluation, and the work somebody still has to do.'),
        ('52', 'Find the gap between a true answer and a useful one.'),
        ('42', 'Rehearse a failed launch while there is still time to change the plan.'),
        ('66', 'Turn a repeated customer problem into a small product or workflow change.'),
        ('04', 'Ask where the book could be wrong. It can take it.'),
    ]
    featured = '\n'.join(
        f'<a class="prompt-pick" href="#prompt-{number}"><span class="prompt-number">{number}</span>'
        f'<h3>{html.escape(prompts[number][0])}</h3><p>{html.escape(description)}</p></a>'
        for number, description in picks)
    navigation = '\n'.join(
        f'<a href="#{group["anchor"]}">{html.escape(group["title"])}</a>' for group in groups)
    sections = []
    for group in groups:
        entries = '\n'.join(
            f'<article class="prompt-entry" id="prompt-{number}">'
            f'<h3><span class="prompt-number">{number}</span> {html.escape(title)}</h3>'
            f'<blockquote>{inline(body)}</blockquote>'
            f'<a class="prompt-permalink" href="#prompt-{number}" aria-label="Link to prompt {number}: {html.escape(title, quote=True)}">Link to this prompt</a>'
            '</article>' for number, title, body in group['prompts'])
        companion = ('<p class="prompt-companion">Bring the <a href="shadow-run/">one-page Shadow Run field sheet</a> to your team review.</p>'
                     if group['anchor'] == 'gate-4-shadow-runs' else '')
        sections.append(f'<section class="prompt-category" aria-labelledby="{group["anchor"]}">'
                        f'<h2 id="{group["anchor"]}">{html.escape(group["title"])}</h2>{companion}{entries}</section>')
    return f'''<div class="landing prompt-page">
<header class="site-header"><a class="site-wordmark" href="index.html">The Support Machine</a>
<nav class="site-nav" aria-label="Main navigation"><a href="#all-prompts">Browse prompts</a><a href="shadow-run/">Shadow Run</a><a href="skill.html">Use the skills</a><a href="book.html">Read the book ↗</a></nav></header>
<main id="main">
<section class="prompt-hero" aria-labelledby="prompt-title">
<p class="eyebrow">A working companion to the Second Edition</p>
<h1 id="prompt-title">80 ways to put<br>the book to work.</h1>
<p class="prompt-dek">Challenge a demo. Price a year of operation. Rehearse a launch. Find the answer that is technically right and still useless.</p>
<p>Pick a prompt, bring your situation, and work through it with the book.<br>Use what helps. Change the rest.</p>
<div class="hero-actions"><a class="button button-primary" href="#all-prompts">Browse all 80 prompts ↓</a><a class="button" href="skill.html">Install the book as a skill ↗</a></div>
<p class="access-note">Free to read and use. The full library is included in the skill.</p>
</section>
<section class="prompt-featured" aria-labelledby="pick-title"><p class="eyebrow">Start with something real</p><h2 id="pick-title">What are you working on?</h2><div class="prompt-picks">{featured}</div></section>
<section class="prompt-setup" aria-labelledby="setup-title"><h2 id="setup-title">A minute of setup.</h2>
<p><a href="skill.html">Install The Support Machine skill</a> once so your assistant can use the book and its templates. Start with the opening below, then choose a prompt and replace the bracketed text with your context. You can also ask the installed skill for a prompt by number or topic.</p>
<details><summary>The opening for your working session</summary><blockquote>{inline(opening[1])}</blockquote></details>
<p class="prompt-source">Prefer Markdown? <a href="{SOURCE_URL}">Open the original prompt library on GitHub.</a> <a href="book.html#appendix-g-talk-to-the-book">Appendix G has the full setup guide.</a></p></section>
<section id="all-prompts" class="prompt-library" aria-label="All 80 prompts">
<aside class="prompt-sidebar"><p class="eyebrow">Find your task</p><nav aria-label="Prompt categories">{navigation}</nav></aside>
<div class="prompt-content">{''.join(sections)}</div></section>
</main><footer class="site-footer"><p>From <a href="book.html">The Support Machine — Second Edition</a>, by <a href="https://www.barnir.co/">Assaf Barnir</a>.</p><p>Keep the case, test the recommendation, and bring the resulting evidence back.</p></footer>
</div>'''
