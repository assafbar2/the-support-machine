# The Support Machine

_The Support Machine: How to Deploy AI in Customer Support Without Breaking Trust_ is both a full manuscript and an executable AI-agent skill.

The manuscript is the story and philosophy. The skill is the operating system: it helps a reader plan, audit, launch, and operate an AI support migration.

## Read It

- [Read the book online](https://assafbar2.github.io/the-support-machine/)
- [Download the PDF](https://assafbar2.github.io/the-support-machine/the-support-machine-v0.2.pdf)
- [Use the skill](https://assafbar2.github.io/the-support-machine/skill.html)
- [Read the Markdown source](skills/the-support-machine/references/book.md)

## What It Does

Use this skill when you need to:

- Diagnose whether AI support is actually the right answer
- Evaluate AI support vendors
- Design the support machine architecture and guardrails
- Run a shadow test before launch
- Build a zero-hour launch runbook
- Review the first 30 days after launch
- Define the post-launch operating model

Core thesis:

> AI support is not a chatbot project. It is an operating model migration.

## Repository Layout

```text
.
├── skills/the-support-machine/
│   ├── SKILL.md
│   ├── references/
│   │   └── book.md
│   └── templates/
│       ├── ai-support-rollout-plan.md
│       ├── first-30-days-review.md
│       ├── launch-day-runbook.md
│       ├── operating-model.md
│       ├── shadow-run-scorecard.md
│       └── vendor-scorecard.md
├── manuscript/
│   └── The Support Machine - manuscript v0.2.docx
├── scripts/
│   ├── build_site.py
│   └── export_docx_to_markdown.py
├── docs/
│   ├── index.html
│   ├── book.html
│   ├── skill.html
│   └── the-support-machine-v0.2.pdf
└── evals/
    └── evals.json
```

## How People Can Use It

### Claude Code / Codex-style local use

Copy or symlink the skill folder into your local skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/the-support-machine ~/.codex/skills/
```

Then ask:

```text
Use The Support Machine to build our AI support rollout plan.
```

Or:

```text
Use The Support Machine to audit this AI support vendor proposal.
```

### Claude.ai skill upload

Zip the skill folder:

```bash
cd skills
zip -r the-support-machine.skill the-support-machine
```

Upload `the-support-machine.skill` in Claude.ai under Skills.

### GitHub install pattern

For agents that can read skills from a GitHub repo, point them at:

```text
skills/the-support-machine/SKILL.md
```

## Example Prompts

```text
We are choosing between two AI support vendors. Build a scorecard and identify hidden risks.
```

```text
Help us plan a shadow run before exposing the AI support machine to customers.
```

```text
Create a launch-day runbook for our AI support rollout.
```

```text
We launched last month. Build a first-30-days review. Some metrics are missing, so mark what we still need.
```

## Patterns Borrowed From Open-Source Skill Repos

This repo follows common patterns from open-source skill repositories:

- A compact `SKILL.md` with strong trigger metadata.
- Long source material kept in `references/`.
- Reusable outputs kept in `templates/`.
- Optional scripts for deterministic maintenance.
- Eval prompts in `evals/` to test whether the skill behaves correctly.

Reference projects reviewed:

- [`anthropics/skills`](https://github.com/anthropics/skills)
- [`haowjy/creative-writing-skills`](https://github.com/haowjy/creative-writing-skills)
- [`coleam00/second-brain-skills`](https://github.com/coleam00/second-brain-skills)
- [`simonw/claude-skills`](https://github.com/simonw/claude-skills)

## Contributing

Pull requests are welcome for typo fixes, clearer examples, stronger templates, and better distribution ideas.

For manuscript edits, open a pull request against `skills/the-support-machine/references/book.md` and explain the intended manuscript change. For skill behavior, edit `SKILL.md`, templates, or evals directly.

Please preserve the book's metaphor system and do not turn the voice into generic AI-transformation copy.

## Contact

Website: [barnir.co](https://barnir.co)  
Email: [assafbar@gmail.com](mailto:assafbar@gmail.com)

This is a personal project, not an official Sentry support channel.

## Status

Public v0.2.

The manuscript is closed as a document, but the story is not. This repo is the path from static book to living skill.
