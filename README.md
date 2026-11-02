# The Support Machine

*How to Deploy AI in Customer Support Without Breaking Trust*, by Assaf Barnir.

A free field guide for support leaders at API, developer-tool, and B2B companies, and the executives who work with them. It covers choosing a system, preparing the team, testing the rollout, and improving the service after launch.

**v0.3 review edition:** 29 chapters, eight appendices, ten illustrations, and two companion skills. The latest published edition is v0.2.

## Read the book

- [Read with Google’s viewer](https://docs.google.com/gview?url=https%3A%2F%2Fraw.githubusercontent.com%2Fassafbar2%2Fthe-support-machine%2Fcodex%2Fsupport-machine-v0.3%2Freview%2Fthe-support-machine-v0.3-reading-copy.docx)
- [PDF](docs/the-support-machine-v0.3.pdf) · [Editable DOCX](review/the-support-machine-v0.3-reading-copy.docx) · [Markdown](skills/the-support-machine/references/book.md)
- [Browse the illustrations](docs/illustrations/README.md) · [Markdown with images](docs/downloads/the-support-machine-v0.3-markdown.zip)
- [Notes for the new version](release-notes/v0.3.md) · [Chapter reading map](release-notes/v0.3-coverage.md)
- [Published online edition](https://assafbar2.github.io/the-support-machine/book.html)

This edition builds on more use cases I've seen, discussed, researched, and worked through in collaboration with humans and AI since the first version was released. Returning readers will find new material on organizational NIMBY behavior, continuing evaluation, build versus buy, customer agents, action receipts, and recovery. The appendices collect the field notes, related projects, 80 practical prompts, and sources by chapter.

I also joined **The Prompt Room, Episode 4** to discuss reducing customer pain and how support work is changing. That conversation informs several chapters. [Watch on YouTube](https://www.youtube.com/watch?v=JxJb4FDqWdI) or [listen on Spotify](https://open.spotify.com/episode/6x73nZKsh9y1VIw46yCW5q).

## Use the book as a skill

[Appendix G](skills/the-support-machine/references/book.md#appendix-g-talk-to-the-book) starts with installation, verification, and update instructions, followed by 80 prompts. The skill reads the relevant chapters from its bundled book when you bring it a question or decision.

**The Support Machine** contains the full v0.3 book and fourteen reusable templates. [Download the ZIP](docs/downloads/the-support-machine.zip) or [.skill package](docs/downloads/the-support-machine.skill).

**Claude:** Upload the ZIP through Customize → Skills → + → Create skill → Upload a skill, then enable it. Code execution and file creation must be available under your account's policy. [Official guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

**Codex:** Ask the built-in installer:

```text
$skill-installer Install skills/the-support-machine from GitHub repository assafbar2/the-support-machine, ref codex/support-machine-v0.3.
```

Invoke `$the-support-machine` with a task. Restart Codex if it does not appear. [Official guide](https://learn.chatgpt.com/docs/build-skills).

Verify that the loaded edition is v0.3 and that the skill can read Chapter 28 and its build-versus-buy template. Reinstall or upload the new package after an edition change; installed copies do not automatically follow GitHub. Keep company-specific notes separately.

The optional [Support AI Evals skill](docs/downloads/support-ai-evals.zip) installs separately. It covers delayed outcome checks, independent review, and knowledge releases. Its local cohort calculator uses explicit reviewed data; it does not connect to a helpdesk or infer success from silence.

Try “Use The Support Machine to compare buying, extending, and building our support agent” or “Use Support AI Evals to review our seven-day repeat-contact cohort.”

## Previous edition and companion material

v0.2 remains available as [PDF](docs/the-support-machine-v0.2.pdf), [DOCX](manuscript/The%20Support%20Machine%20-%20manuscript%20v0.2.docx), [Markdown](docs/editions/v0.2/book.md), and [archived HTML](docs/editions/v0.2/book.html).

The [Shadow Run field sheet](docs/shadow-run/Shadow-Run-Field-Sheet-v0.13.pdf) accompanies the earlier talk. The book and current scorecard expand its release-gate guidance.

See the [changelog](CHANGELOG.md) for edition highlights and [contribution guide](CONTRIBUTING.md) for the manuscript and publishing workflow.

## Author and license

This is my personal project. The judgments and recommendations are mine; I do not speak for Sentry. This repository is not an official Sentry support channel.

Book text and book-format outputs: [CC BY 4.0](LICENSE-MANUSCRIPT.md). Skills, templates, scripts, and repository documentation: [MIT](LICENSE-SKILL.md). See [LICENSE.md](LICENSE.md).

[Website](https://barnir.co) · [Email](mailto:assafbar@gmail.com)
