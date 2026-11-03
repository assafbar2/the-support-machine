# Talk to the Book: the full prompt library

Eighty prompts from *The Support Machine*, Second Edition, Appendix G. Start each one with the opening in Appendix G. The book prints ten of them; the numbers match.

### Find your way through the book

**01. Choose a reading route**

> I am [role] at [type of company], and our immediate problem is [problem]. Give me a reading route through five relevant chapters. For each, name the decision it will help me make and the evidence I should bring. Explain what can wait.

**02. Locate the current gate**

> Here is our AI support rollout status: [status]. Place us on the six-gate operating map. Distinguish work we completed from work we merely planned. Identify the first unmet condition and a concrete way to examine it.

**03. Explain a difficult idea**

> Explain [concept from the book] to a [support engineer, finance leader, product manager, or executive]. Use one ordinary support example and one counterexample. Keep the book's limits intact and show where the idea changes a decision.

**04. Challenge the book**

> Make the strongest practical case against the recommendation in [chapter or section] of the bundled book. State the conditions under which it would be wrong or too expensive. Then suggest an observation or experiment that could distinguish that case from the book's recommendation.

**05. Separate kinds of claims**

> Review [chapter or section] in the bundled book. Identify author experience, research findings, vendor descriptions, proposed practice, and fictional examples. Explain what each can support and which conclusions would need additional evidence. Do not turn an anecdote into a measured result.

### Gate 1 — diagnose the queue

**06. Audit a conversation sample**

> Use these sanitized conversations: [sample]. Identify the customer's actual task, the obstacle, the work Support performed, and evidence of the outcome. Suggest a small tagging scheme. Preserve ambiguous cases and explain which patterns the sample cannot establish.

**07. Find the repeated explanation**

> Customers repeatedly ask [question], although we have [documentation or onboarding]. Use Chapters 1 through 3 to investigate why. Compare discoverability, clarity, product behavior, and missing context. Recommend the smallest useful check before we buy another tool.

**08. Test whether AI is needed**

> Our proposed AI use case is [use case]. Compare an agent with a product fix, better documentation, a deterministic workflow, and doing nothing. Use the same customer success condition for every option. State what evidence would make the simplest option insufficient.

**09. Examine a healthy dashboard**

> Our CSAT and SLA results look healthy, but the team reports [repeated work]. Explain how both can be true. Propose three checks that reveal customer effort or avoidable work without inventing a hidden churn rate from silence.

**10. Build the initial case**

> Turn [queue findings, time estimates, and constraints] into a one-page business case. Show the customer problem, baseline, options, estimated effort, uncertainty, and next decision. Keep assumptions visibly separate from observed numbers.

### Resistance and your own backyard

**11. Examine an objection fairly**

> A stakeholder objects that [objection]. Use the NIMBY chapter to distinguish a testable requirement, an unresolved tradeoff, and a moving finish line. Do not infer the person's motives. Draft questions that let a valid objection improve the plan.

**12. Check my own resistance**

> I support AI adoption but want an exception for [my workflow]. Challenge my reasoning using Chapter 5. Who carries the cost of this exception? What specific risk does it address? Help me define a condition under which I would remove it.

**13. Stabilize a pilot decision**

> Our pilot criteria changed from [original] to [current]. Identify changes supported by new evidence and changes that need an explanation. Draft a decision record with a passing condition, remaining objections, owner, and decision date.

**14. Make delay visible**

> Compare launching within [bounded scope] with waiting [period]. Use [known workload, incident, and cost evidence]. Show the risk and ongoing work on both sides. Use ranges for uncertain inputs and avoid inventing a financial cost for every concern.

**15. Rehearse a difficult meeting**

> Role-play a reviewer who has a serious concern about [proposal]. Ask one question at a time and respond to my evidence. When we finish, separate the issue we resolved from the assumptions still open. Do not reward me for simply sounding confident.

### Gate 2 — build versus buy

**16. Choose the layer**

> Map [our proposed support system] into channels, identity, knowledge, reasoning, actions, handoff, and evaluation. For each layer, compare buying, extending, and building. Identify which requirement actually needs to be specific to our business.

**17. Price a year of operation**

> Build a twelve-month comparison from [vendor costs and internal estimates]. Include integration, evaluation, maintenance, incidents, knowledge work, and displaced engineering work. Mark missing inputs. Show how the answer changes if usage doubles or the maintainer leaves.

**18. Give both options the same exam**

> We are comparing [vendor] with [internal prototype]. Design a shared test using [representative cases]. Keep permissions, context, outcome conditions, and recovery requirements comparable. Record the human intervention each option needs to succeed.

**19. Challenge the weekend demo**

> Our prototype can [demonstrated behavior]. Identify the work between that demonstration and a service we can operate. Produce a bounded scope, ownership plan, and cost estimate structure. Explain what result would justify building it despite our default preference to buy.

**20. Retire a connector**

> We built [connector] to cover [gap], and a vendor now advertises a replacement. Define the behaviors the replacement must preserve, the comparison cases, migration dependencies, and retirement conditions. Do not treat matching feature names as evidence of equivalence.

### Vendor claims and changing products

**21. Read a capability announcement**

> Review [announcement and documentation]. Separate announced capability, documented availability, our workspace access, and tested behavior. Identify the claims that still need confirmation before we put the feature into a delivery commitment.

**22. Test an operational agent**

> An operational agent proposes [configuration change]. Build a review record showing the problem, affected audiences, expected benefit, relevant regression cases, approving owner, and recovery path. Check whether the proposal fixes the cause or merely makes the answer sound better.

**23. Review an acquisition**

> Our vendor has been acquired. Using [announcement, contract, and dependency map], identify which continuity assumptions need review. Separate current facts from possible future changes. Produce questions about support ownership, data terms, integrations, export, and exit cost.

**24. Inspect hidden operating work**

> The vendor promises [automation claim] and asks us for [onboarding work]. Help us trace who actually handles an unfamiliar case. Ask about human access, intervention, maintenance, and coverage. Do not infer deception from an onboarding questionnaire alone.

**25. Compare current vendors responsibly**

> Compare [vendors] against these customer tasks: [tasks]. Use current primary documentation if you can access it, date the check, and link each material capability claim. If you cannot verify current facts, produce the comparison framework and mark the cells requiring evidence.

### Gate 3 — knowledge and authority

**26. Map responsibilities in the machine**

> Review [architecture] using the Librarian, Judge, Clerk, Gatekeeper, and Auditor responsibilities. Identify where source selection, reasoning, permission, execution, and review occur. Find a failure whose owner is unclear. Do not assume we need a separate model for every role.

**27. Examine the data path**

> Trace [customer information] through [services and people]. Create a data-flow inventory with access, purpose, retention, deletion, and accountable owner. Identify unknowns by layer, including transcripts, retrieval indexes, evaluation copies, and subprocessors.

**28. Test audience boundaries**

> Our agent targets guidance using [audience rules]. Propose cases for overlapping membership, missing attributes, stale values, and attributes controlled by the client. Distinguish personalization from permission to retrieve protected data or perform an account action.

**29. Handle a customer agent**

> A customer's agent submits [request and identifiers]. Walk through identity, delegated authority, account scope, and evidence checks before answering or acting. Include an invalid identifier and a valid identifier from another account. Produce a useful clarification and handoff path.

**30. Review candidate knowledge**

> A human solved this case: [sanitized case]. Decide what could become reusable knowledge. Identify authoritative evidence, applicable versions and audiences, exceptions, privacy concerns, owner, and regression cases. Do not promote the entire conversation as approved guidance.

### Actions and receipts

**31. Define an action contract**

> We want an agent to perform [action]. Specify the customer's intent, permitted principal and account, parameters, preconditions, required confirmation, backend checks, completion evidence, and stop conditions. Identify the parts an ordinary deterministic workflow could handle.

**32. Investigate an unknown effect**

> The tool timed out after [action], and we have [logs and receipts]. Separate confirmed effects, confirmed non-execution, and unknowns. Identify the provider evidence needed before continuing. Do not recommend a blind retry when the effect may already exist.

**33. Examine an idempotency contract**

> Read this provider's retry documentation: [text]. Explain key scope, retention, parameter matching, and behavior after expiration. Apply those limits to [workflow]. State what our own operation log cannot guarantee about an external provider.

**34. Recover a partial workflow**

> In [multi-step workflow], step one completed, step two is uncertain, and step three has not started. Produce an evidence-based recovery sequence. Separate retries from compensation and identify the approval and receipt required for each new effect.

**35. Ask a vendor to demonstrate failure**

> Prepare a short demonstration script for an agent that [consequential action]. Include an interruption after the provider commits, a duplicate request, and a missing receipt. State what we should inspect in account state and audit records, beyond the final chat message.

### Gate 4 — shadow runs

**36. Reconstruct a historical case**

> Turn [resolved conversation and source history] into a shadow-run case. Separate what the agent could have known when the request arrived from later evidence used to grade it. Mark any reconstruction gap instead of supplying hindsight as input.

**37. Design representative coverage**

> Our proposed release covers [tasks and audiences]. Design a case set that includes routine work, ambiguity, missing context, failed actions, and required escalation. Explain why each category belongs. Separate a frequency estimate from a deliberately difficult test.

**38. Define a release blocker**

> Translate the book's five stop categories into concrete tests for [product and release scope]. Distinguish a consequential failure from a style improvement. Explain which failure blocks which scope and what evidence would permit reconsideration.

**39. Verify shadow isolation**

> Review [test environment and available tools]. Identify every path that could send a customer message or change live state. Propose enforceable isolation and a way to verify it. A prompt telling the agent not to act does not count as the control.

**40. Write the release decision**

> Use [test results and unresolved cases] to draft Appendix B's release record. State the tested version, coverage, hard-stop results, human capacity, permitted scope, and owner. Choose ready, ready within a stated scope, or not ready, and explain the evidence.

### Gate 5 — launch and ownership

**41. Find the missing launch decisions**

> Audit [launch plan] against Chapter 24 and Appendix C. Identify decisions without owners, untested dependencies, missing baseline definitions, and gaps in the human path. Prioritize the omissions that can affect customers at cutover.

**42. Run a pre-mortem**

> Assume [launch] failed in its first day. Propose five plausible mechanisms grounded in our actual architecture. For each, name the earliest observable signal, containment action, owner role, and rehearsal that would expose it before launch.

**43. Size the human fallback**

> If we disable [automation scope], [known volume and case mix] reaches the team. Help estimate the required capacity with explicit assumptions. Identify priorities, backup coverage, and customer expectations. Do not assume an escalation rule creates available people.

**44. Retire the old process**

> We are migrating from [old process] to [new process]. Define the retirement conditions, required history, remaining dependencies, and recovery capabilities. Keep a workable service-containment path while eliminating duplicated sources of truth.

**45. Draft the launch explanation**

> Draft a customer-facing explanation of [tested capability]. State what the agent can use and do, where its scope ends, and how to reach a person. Use our direct product voice. Exclude intended capabilities that have not passed their checks.

### Gate 6 — delayed outcome checks

**46. Define the follow-up cohort**

> Design the seven- and thirty-day follow-up record for conversations our agent marks resolved. Specify original outcome events, identifiers, timestamps, issue evidence, and channel coverage. Identify the helpdesk fields or exports we still need to verify.

**47. Decide whether a return is related**

> Compare [original conversation] with [later contacts]. Identify evidence that they concern the same underlying issue, including contacts from colleagues on the account. Return confirmed related, confirmed unrelated, or uncertain with reasons. Do not decide from a topic label alone.

**48. Calculate the observed rate**

> Use [normalized cohort data] to calculate seven- and thirty-day recurrence separately. Include only mature, adequately observed conversations for each window and count each original once. Report missing evidence and explain why no observed return is not confirmed success.

**49. Look beyond the helpdesk**

> Our follow-up view covers [channels] but misses [other channels or customer paths]. Explain how that affects the outcome claims. Propose a feasible way to improve coverage or validate a sample without assuming that every silent customer succeeded or abandoned the task.

**50. Investigate a changed rate**

> Recurrence changed from [before] to [after] following [release]. Check cohort maturity, case mix, matching rules, channel coverage, and product changes before attributing the result to the release. Propose the comparison that would give us stronger evidence.

### Review answer quality and the reviewer

**51. Challenge an answer with evidence**

> Review [answer, customer request, and applicable sources]. Try to identify a concrete failure in intent, factual grounding, applicability, completeness, effort, or escalation. Support every finding. If the answer is sound, say so; do not invent a defect to satisfy the assignment.

**52. Find the correct but useless answer**

> This response contains true statements: [response]. Evaluate whether it helps this customer complete [task]. Identify missing prerequisites, a missing next step, or unnecessary effort. Draft a better answer only where the supplied evidence supports it.

**53. Calibrate two reviewers**

> These reviewers disagree on [cases and reasons]. Identify whether the difference comes from policy ambiguity, missing context, rubric wording, or a factual error. Propose reviewed reference cases and an adjudication process before comparing their scores.

**54. Keep sampling interpretable**

> Plan a weekly review of Fin and Kapa using [traffic and risk context]. Keep a random baseline sample separate from targeted complaints and risky cases. Explain what each sample can estimate and how differences in tasks and context constrain comparison.

**55. Compare evaluation products**

> Create a shared evaluation packet for [unitQ, Unwrap, vendor-native QA, or another reviewer]. Include valid answers, subtle failures, insufficient evidence, and a wrong reference answer. Compare false alarms, missed failures, explanations, correction history, and regrading effort.

### Metrics without false comfort

**56. Explain the 16 percent example**

> Explain the book's 40% involvement × 40% conditional resolution = 16% example using 100 eligible conversations. State the required denominator alignment. Then explain why 16 reported resolutions still need a separate customer-outcome check.

**57. Build a metric dictionary**

> Review [dashboard definitions]. For each metric, write numerator, denominator, unit, exclusions, time window, and definition version. Identify names that conceal different meanings, especially resolution, automation, deflection, and billable outcome.

**58. Reconcile a definition change**

> Our resolution rate rose after [definition change], while total resolutions stayed the same. Explain the arithmetic using the supplied counts. Show which periods remain comparable and where the chart needs a break or a restated historical series.

**59. Inspect customer and team effort**

> Ticket volume fell, but human handling time rose. Use [case mix, time, and staffing evidence] to investigate. Separate harder remaining cases, new QA work, rework, and capacity changes. Avoid treating lower ticket count as proof of lower workload.

**60. Price an evidenced outcome**

> Design a cost report for [operation]. Include platform and usage fees, review, integration maintenance, and recovery. Distinguish cost per eligible conversation, per reported resolution, and per confirmed outcome. Keep outcome coverage visible beside the last measure.

### Recovery when the machine fails

**61. Triage the incident**

> Here are the known facts of [agent failure]. Separate impact, scope, verified effects, and hypotheses. Recommend immediate containment, a recovery owner role, and evidence to preserve. Identify what needs a decision now and what can wait for diagnosis.

**62. Make a handoff actionable**

> Turn [alert or escalation] into a decision packet. Include the customer's goal, verified facts, attempted actions, uncertain effects, permitted options, deadline, backup owner, and resume conditions. Explain what acknowledgment alone would leave unresolved.

**63. Correct the customer update**

> Draft a correction for [wrong answer or failed action] using only [verified facts]. Explain what was wrong, the safe next step, who owns follow-up, and what remains uncertain. Do not claim the situation is fixed before the customer state is checked.

**64. Investigate the cause**

> Review [incident evidence]. Compare a source problem, applicability error, misunderstood intent, tool failure, routing failure, and missing human capacity. For each plausible cause, name the evidence that would distinguish it. Do not default every repair to another prompt warning.

**65. Earn the return to service**

> We changed [system element] after [incident]. Propose regression cases for the original failure and neighboring behaviors. Define the permitted return scope, accountable review, customer follow-up, and observations that would require renewed containment.

### Move Support into midfield

**66. Turn friction into a small change**

> Use [repeated customer problem] to propose a bounded documentation, UI, workflow, or product change. Identify the evidence, affected audience, reviewer, and later customer check. Compare it with answering the same question faster.

**67. Give the team working conditions**

> We want support engineers to ship improvements. With [staffing and queue constraints], propose protected time, access, training, reviewer availability, and a fallback when volume rises. Make the tradeoffs explicit instead of adding the work to an already full queue.

**68. Plan a first contribution**

> Design a learning plan for a support engineer making [small product change]. Include reproducing the customer problem, understanding relevant code, using AI assistance, review, and checking the result. Keep the plan realistic for [time and experience level].

**69. Change the performance conversation**

> Review [team performance measures]. Identify incentives that reward repeated rescue while neglecting prevention or good escalation. Propose an impact record that recognizes customer outcomes and useful learning without making PR count the new ticket-count target.

**70. Audit the weekly operating review**

> Here are [meeting notes and improvement backlog]. Identify findings without owners, fixes without regression cases, and releases without later checks. Redesign the next review around decisions the team can actually make and capacity it has to act.

### Promises and customer success

**71. Reconcile a customer commitment**

> Compare [original promise], [engineering status], [account configuration], and [customer evidence]. Assess built, enabled, and customer-verified separately. Preserve contradictions and stale evidence. State what can truthfully be communicated now.

**72. Define a useful customer goal**

> We want an agent to help with [onboarding, adoption, or re-engagement]. Define the customer's observable milestone, eligible audience, time horizon, necessary evidence, contact preferences, stop conditions, and owner of exceptions. Do not use message count as the outcome.

**73. Resolve conflicting goals**

> An agent is pursuing [growth goal] while the customer has [unresolved support problem]. Propose a priority rule, handoff, and condition for resuming the goal. Explain how the system can recognize the conflict from available evidence.

**74. Group cases without losing differences**

> These conversations appear to share a problem: [cases]. Identify a possible common repair, then check version, permission, entitlement, and account differences. Recommend the population the repair could apply to and the exceptions requiring separate work.

**75. Close the company feedback loop**

> Turn [customer evidence] into a brief for Product, Documentation, GTM, and Customer Success. Identify the expectation, affected customers, evidence, responsible decision, and later check. Keep the original examples available so the summary can be challenged.

### Working sessions and executive decisions

**76. Prepare the executive decision**

> Turn [operating evidence] into a one-page decision for [executive audience]. State the customer problem, options, recommendation, costs, uncertainty, and decision needed. Include the strongest reason to choose differently and the evidence that would change your view.

**77. Run a practical workshop**

> Design a 60-minute workshop around [chapter and real team problem]. Include a short case, individual judgment before group discussion, an exercise using our evidence, and one decision record to complete. Label any invented teaching scenario fictional.

**78. Challenge our favorite plan**

> We favor [plan]. Build the strongest evidence-based alternative, including a simpler non-AI option if relevant. Compare both against the same customer task and operating constraints. Identify the cheapest informative test before either option receives a larger commitment.

**79. Turn the book into next week's work**

> Given [our current gate, people, and capacity], propose a one-week work plan grounded in the book. Limit it to work we can staff. Name deliverables, dependencies, owner roles, and how we will know whether each item helped the next decision.

**80. Revisit an older edition**

> Use the installed edition's notes to explain what changed since [earlier edition] and which decisions deserve another look for [our situation]. Separate changed advice from clearer wording. If both full editions are accessible, compare them directly; otherwise state that you are relying on edition notes and do not invent a diff.

The value of the conversation is the work it helps you inspect. Keep the case, test the recommendation, and bring the resulting evidence back. That gives the next discussion something better than another confident summary.
