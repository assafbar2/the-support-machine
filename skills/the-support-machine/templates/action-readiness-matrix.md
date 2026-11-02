# Action Readiness and Customer-Agent Boundary

Customer goal / account / authenticated principal:

Delegated authority, expiry, and scope (if a customer agent is involved):

Supplied IDs and links verified against authorized source:

| Action | Preconditions and permission | Intent / operation ID | Provider evidence | Safe retry contract | Unknown-effect owner |
|---|---|---|---|---|---|
| | | | | | |

Distinguish authorized, confirmed complete, confirmed not executed, and unknown. Log the approved intent before dispatch. Check idempotency-key scope, retention, parameter changes, and concurrency behavior.

Separate effects in a workflow: account change / customer message / ticket status. Resume at the unfinished step; do not replay completed effects.

Test: nonexistent object, another account's object, expired delegation, absent permission, missing context, legitimate duplicate intent, lost acknowledgment, worker interruption, and repeated automated conversation.

Loop or retry limit and evidence of progress:

Compensation authority and effects that cannot be undone:

Human packet: known effects, receipts, uncertain effects, safe next actions, decision due, backup, and resume conditions.
