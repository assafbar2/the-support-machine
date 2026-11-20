# Paired LLM Evals: Baseline vs. Candidate

*Did the model change earn a rollout?*

Use this to decide what a model, prompt, or fine-tuning change earns. Work from paired results or design a read-only shadow run. If the runs have not happened, return the test plan and what would count as a pass; do not invent results.

## Agree on the test before looking at the scores

- Name the baseline and candidate, the one change under test, and who decides. If several things changed together, report the effect of the bundle; do not credit one change on its own.
- Use the same case IDs, available records, tool permissions, run limits, and grading rules in both runs. Keep the test cases out of tuning. Keep live writes and customer messages off. The models may choose to look up different records; that difference is part of the result.
- Agree on the minimum worthwhile improvement and the failures that stop a release, such as an unauthorized action or a missed consequential handoff. Do not set a threshold after seeing the results and call it a pre-set rule.

## Compare case by case

Match results by case ID. Count pass/pass, fail/pass, pass/fail, and fail/fail pairs. Report the total tested, the matched denominator, and any missing or ungradeable pairs separately. A trace that shows the model timed out may be a scored failure; a missing trace is not evidence that it failed. If the runs differ in coverage or rules, explain what a comparable rerun would take.

Show unsupported recommendations and missed required handoffs for each version, with their applicable denominators. Score a good handoff as valid when the evidence runs out and the case calls for escalation. Grade what the model can support from the records it actually inspected, not whether it guessed the expected answer.

Pick one trace that improved and one that still failed. Prefer a new regression if there is one. For each, show the records checked, the next step the model took, and why the grade changed or stayed the same. If the artifacts don’t contain either kind of example, say so.

## Make the call

Return a short review: what changed, the paired counts, the two traces, any stop condition, and one recommendation:

- **Hold** if a stop condition fired or the candidate missed the agreed pass rule.
- **Gather more evidence** if the test cannot support a decision. Name the missing evidence, the next check, and who owns it.
- **Consider a limited rollout** only for the scope that passed, with a human owner, a way to stop or roll back, and a check on real outcomes. If the evidence is only synthetic, name the production-relevant checks still needed before exposing customers. A passing simulation earns the next test, not a live launch.

## Worked example: QueueLab

Both models were evaluated on the same 60 fictional support cases before and after fine-tuning.

| Model | Supported decisions | Improved / regressed / still failed | Cases with unsupported recommendations |
| --- | --- | --- | --- |
| SmolLM2 | 0/60 → 53/60 | 53 / 0 / 7 | 36/60 → 7/60 |
| Falcon | 0/60 → 3/60 | 3 / 0 / 57 | 0/60 → 39/60 |

- **Improved, `holdout-02-1`:** SmolLM2 timed out after checking the run history in the first run. After fine-tuning, it checked the receipt, asked for the expected folder, and used the mismatch to support a correction.
- **Still failed, `holdout-01-1`:** After fine-tuning, SmolLM2 found that no job had run. It checked delivery instead of the schedule and guessed a delivery access problem. The records it checked didn’t support that advice.

**Recommendation:** Gather more evidence for SmolLM2, starting with fresh disabled-schedule cases and a check on the handoff. Hold Falcon under the tested setup; it did not meet the pass rule. Neither result shows what would happen to customers on a live queue. See the [replay](https://assafbar2.github.io/queuelab/post-training/) and [scorecard and raw traces](https://github.com/assafbar2/queuelab/tree/main/reports/post-training-2026-11-20#measured-results).

**Try it:** “Here are the before-and-after runs. Show me one case that got better, one that still went wrong, and what would stop you from approving this change.”
