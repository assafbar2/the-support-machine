# Delayed outcome method

Moved from *The Support Machine*, Second Edition, Chapter 28. The chapter keeps the short version; this is the full method.

Every conversation Fin marks resolved should enter a follow-up cohort. Capture the conversation ID, account and contact identifiers, original resolution time, outcome definition, and available issue context. Preserve that original event. A later reopening must not erase the fact that the system previously counted the conversation as resolved.

At seven days and again at thirty days, ask whether the customer reopened the conversation, returned through a new one, or had a colleague contact us about the same underlying problem. A new question from the same account is not automatically a failed resolution. A different person describing the same broken setup may be.

Start with the events and conversations available in your helpdesk (for us, Intercom, with Fin handling AI conversations). Verify that the export or API exposes the history, identifiers, timestamps, and channels the check requires. "The data is in the helpdesk" is a hypothesis about access and coverage, not an implementation specification. If a customer moved to Slack or spoke to their account manager, your view may be incomplete.

Use a matching process that can explain itself. Exact issue references and account identifiers are stronger evidence than a shared topic label. Semantic matching can suggest related cases; uncertain matches should remain uncertain until reviewed. Retain a reason for the link so someone can correct it later.

For each window, calculate the share of eligible, originally resolved conversations that have at least one related repeat contact. Count each original conversation once in that rate, even if it produced several follow-ups. Track the additional contacts and human effort separately because one return and six returns do not impose the same cost.

**Only mature conversations belong in the denominator.** A conversation resolved yesterday cannot pass a thirty-day check. Seven- and thirty-day results use different eligible populations and are cumulative windows. Do not add them together.

Consider a fictional cohort of 100 conversations originally marked resolved. At review time, 80 have a complete seven-day window. Eight of those have a confirmed related return. The observed seven-day recurrence rate is 8 divided by 80, or 10%. The other 72 had no observed repeat contact in that window. That is all this calculation establishes.

It does not establish that 90% of customers succeeded. Some may have abandoned the task, found another channel, or accepted a workaround that does not meet their goal. Report confirmed success, observed recurrence, and insufficient outcome evidence separately. Keep any overlap visible: a customer can initially confirm success and encounter a later regression.

Seven and thirty days are proposed starting windows, not universal scientific thresholds. Choose additional windows when the product has a longer operating cycle, such as a monthly export or an annual renewal. Compare like cohorts, and investigate changes in product mix or customer population before crediting a prompt change.
