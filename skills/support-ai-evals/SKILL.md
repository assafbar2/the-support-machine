---
name: support-ai-evals
description: Design or audit ongoing evaluation of support AI such as Fin, Kapa, or an internal agent. Use for 7/30-day repeat-contact cohorts, independent QA, evaluator comparisons, rubric calibration, regression testing, and knowledge releases. Produces an evidence-based evaluation plan or cohort report without treating silence as proven resolution.
---

# Support AI Evals

Use this focused skill for continuing evaluation, including after the first thirty days. It is self-contained; the broader migration book is optional.

## Establish the task

Identify the customer job, systems, time period, available evidence and decision owner. Distinguish an evaluation design from analysis of actual data. Never imply that a helpdesk is connected, a demo occurred, or a production change was made without evidence.

Read `references/rubric.md` for review and calibration. Read `references/cohort-data.md` before using the calculator.

## Three-part workflow

1. **Delayed outcomes:** retain original reported-resolution events and definitions. Match reopened or new contacts to the same underlying issue using account identity and defensible evidence. Review uncertain matches. For each 7/30-day window, count only mature originals with complete coverage of the declared channels. Count an original once even if it has several returns. Show incomplete coverage and unknown matches separately. No observed return is not confirmed success. Method and worked example: `references/delayed-outcome-method.md`.
2. **Independent challenge:** sample an ordinary random baseline and a separate risk/failure set. Compare like tasks across systems. Grade with current product evidence and reviewed references; include valid answers and incorrect reference answers to test false positives. Calibrate humans and models, inspect disagreement, and permit insufficient evidence. Evaluator comparison: `references/evaluator-comparison.md`.
3. **Current failures:** evaluate intent, factual grounding, applicability, completeness, effort, escalation and action results. A technically true answer can be useless or impossible for the customer's plan/version/permissions. An unauthorized action or missed consequential escalation cannot be offset by tone.

## Optional deterministic calculation

Run `python scripts/summarize_cohorts.py input.json --output report.json` from this skill folder. Python 3.10+ standard library only. The script reads local normalized data; it does not fetch, match, or send conversations. The input must already contain reviewed same-issue links and declared observation coverage.

Keep the generated counts and input assumptions in the report. Do not rename recurrence as a real resolution rate, infer success from silence, combine cumulative windows, or mix metric-definition versions. If the data fails validation, repair the source or describe the gap; do not silently discard it.

## Turn findings into a change

Record case → diagnosis → owner → correction → regression → release → later outcome. Route product, policy, retrieval, tool, knowledge, and staffing problems to their owners. Keep tuning cases separate from holdouts. Version sources, system configuration and graders; use repeated trials where variability matters.

Treat a solved ticket as candidate knowledge. Check authority, applicability, privacy and conflicts, then test and release with a withdrawal path.

## Deliver

Provide the decision, counts and denominators, coverage, uncertainty, failure examples, owned repairs and next observation date. For vendor evaluation, distinguish documented features, actual workspace access, and tested results. Vendor-native QA and a separate company both need calibration. Do not perform live writes or customer communication without authorization.
