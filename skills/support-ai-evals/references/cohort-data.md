# Cohort input contract

This calculator is an illustrative local analysis tool, not an Intercom integration. It does not decide whether two issues match. Supply reviewed, normalized records using the schema illustrated in `../examples/cohort.json`.

Top-level fields:

- `as_of`: timezone-aware ISO timestamp; no event may be later.
- `coverage_scope`: the channels and data sources actually observed.
- `records`: one record per original conversation, at its original reported-resolution event.

Each original requires nonempty `conversation_id`, `account_id`, `definition_version`, a timezone-aware `resolved_at`, `observed_through`, and `coverage` of complete, partial or unknown. Complete means the declared scope is continuously observed from resolution through observed_through; it does not mean all possible channels are visible.

Optional `confirmed_success_at` must represent independent outcome evidence, not an assumed helpdesk closure. Returns use an `event_id` (unique event identity, so the original thread can reopen), `conversation_id`, `account_id`, `occurred_at`, `match` (confirmed, uncertain, unrelated), and a nonempty `reason`. Another contact on the same account can match. A different account is rejected rather than silently linked. Return event times must be after resolution and within observation.

The calculator rejects duplicate originals, conflicting duplicate events, naive timestamps, unknown fields, mixed definition versions, and invalid coverage. Identical repeated return events are deduplicated. Correct uncertain matches upstream and retain your review history there.

For each cumulative window, eligible = resolved_at + window <= as_of AND complete declared coverage through that boundary. Mature records with inadequate coverage remain visible as excluded; immature records remain visible too.

Outputs include confirmed recurrence, uncertain-match counts, observed repeated events, no observed confirmed return, and independently confirmed outcomes within the window. These categories can overlap. A possible-recurrence upper bound includes uncertain matches only to make uncertainty visible; it is not an estimate of actual recurrence. The complement of recurrence is never labeled successful resolution.

The sample is synthetic. Run:

```bash
python scripts/summarize_cohorts.py examples/cohort.json
```
