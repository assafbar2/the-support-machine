"""Present the existing talk handout as a practical companion to the book."""

PDF_NAME = 'Shadow-Run-Field-Sheet-v0.13.pdf'
TALK_URL = 'https://events.customersuccesscollective.com/location/supportsf/speaker/assafbarnir'


def homepage_feature():
    return f'''<section class="sheet-feature" aria-labelledby="sheet-feature-title">
<div><p class="eyebrow">The take-home from the talk</p><h2 id="sheet-feature-title">The Shadow Run<br>field sheet.</h2>
<p class="sheet-dek">Before your AI touches customers.</p>
<p>A one-page cheat sheet for testing an AI workflow. Six checks, five stop conditions, failure owners, and a plan for Monday.</p>
<p>Print it. Mark it up. Bring it to your next review.</p>
<div class="hero-actions"><a class="button button-primary" href="shadow-run/">Get the field sheet ↗</a><a class="text-link" href="shadow-run/{PDF_NAME}">Download the one-page PDF ↓</a></div></div>
<figure class="sheet-preview"><a href="shadow-run/" aria-label="See the Shadow Run field sheet"><img src="shadow-run/field-sheet-preview.png" alt="The Shadow Run field sheet: a printable scorecard, stop conditions, failure owners, starting plan, and decision record." width="1391" height="1800" loading="lazy"></a><figcaption>One page to keep beside the work.</figcaption></figure>
</section>'''


def render_shadow_run(repo):
    scorecard = repo + '/blob/main/skills/the-support-machine/templates/shadow-run-scorecard.md'
    return f'''<div class="landing sheet-page">
<header class="site-header"><a class="site-wordmark" href="../index.html">The Support Machine</a>
<nav class="site-nav" aria-label="Main navigation"><a href="../prompts.html">80 prompts</a><a href="../skill.html">Use the skills</a><a href="../book.html">Read the book ↗</a></nav></header>
<main id="main">
<section class="sheet-hero" aria-labelledby="sheet-title">
<div><p class="eyebrow">Shadow Run · Field sheet</p><h1 id="sheet-title">Before your AI<br>touches customers.</h1>
<p class="sheet-dek">The one-page cheat sheet for running an AI candidate beside your live workflow.</p>
<p>Six checks. Five stop conditions. A place to name who fixes what.</p>
<p class="sheet-talk">The take-home from my talk, <a href="{TALK_URL}">Shadow running AI: The framework for safer AI adoption</a>.</p>
<div class="hero-actions"><a class="button button-primary" href="{PDF_NAME}">Download the one-page PDF ↓</a><a class="button" href="#use-it">Use it with your team</a></div>
<p class="access-note">Free to download. Print it, mark it up, and use it in your next review.</p></div>
<figure class="sheet-preview"><a href="{PDF_NAME}" aria-label="Open the printable Shadow Run field sheet"><img src="field-sheet-preview.png" alt="One-page Shadow Run field sheet with six checks, five stop conditions, failure owners, a starting plan, and a release decision." width="1391" height="1800" fetchpriority="high"></a><figcaption>The sheet from the talk. Open the PDF to print it.</figcaption></figure>
</section>
<section class="sheet-contents" aria-labelledby="inside-title"><h2 id="inside-title">The review, on one page.</h2>
<dl><div><dt>Score the case</dt><dd>Answer quality, source grounding, escalation judgment, tone and format, permissions, and handoff quality.</dd></div>
<div><dt>Know when to stop</dt><dd>Five conditions to hold the affected scope, with room to record the evidence.</dd></div>
<div><dt>Give the failure an owner</dt><dd>Knowledge, agent setup, product promises, routing, policy, and tools each need someone to fix what failed.</dd></div>
<div><dt>Make the call</dt><dd>Record ready, hold, or constrained scope, with an owner and a date. Keep the counts behind the percentages.</dd></div></dl></section>
<section class="sheet-use" id="use-it" aria-labelledby="use-title"><div><p class="eyebrow">Start on Monday</p><h2 id="use-title">Bring one workflow.<br>Start there.</h2>
<p>Use it before a first rollout, and again when a model, tool, policy, or knowledge source materially changes.</p>
<p>The test shows how the candidate behaved on those cases. Keep watching customer outcomes after release.</p></div>
<ol><li>Pick one workflow and name its owner.</li><li>Write the acceptance bar, limits, and stop conditions before testing.</li><li>Mix routine and risky cases. Keep fresh cases aside, and use only the context available when each request arrived.</li><li>Disable customer messages and live account changes through tools and permissions.</li><li>Review the results against evidence. Score each case and record what failed.</li><li>Give each failure an owner. Fix and retest, including load, routing, shutoff, and fallback.</li><li>Record the decision and allowed scope. Start a small rollout of the work that passes, and keep reviewing.</li></ol></section>
<section class="sheet-next" aria-labelledby="next-title"><h2 id="next-title">When you need the detail.</h2><p>The sheet is ready to use on its own. The Second Edition develops the method further.</p>
<ul><li><a href="../book.html#22-the-shadow-run">Chapter 22: The Shadow Run</a> — the method and the reasoning.</li>
<li><a href="../book.html#appendix-b-shadow-run-and-change-release-record">Appendix B: Shadow Run and Change Release Record</a> — the fuller release record.</li>
<li><a href="{scorecard}">Editable shadow-run scorecard</a> — adapt the record to your workflow.</li>
<li><a href="../prompts.html#gate-4-shadow-runs">Shadow-run prompts</a> — work through the cases with the book skill.</li></ul></section>
</main><footer class="site-footer"><p>A companion to <a href="../book.html">The Support Machine — Second Edition</a>, by <a href="https://www.barnir.co/">Assaf Barnir</a>.</p></footer>
</div>'''
