# QueueLab: proposed companion for The Shadow Run

Editorial draft for *The Support Machine — Second Edition*. The text below is ready to review in context. It does not revise the published printing or its downloads.

## Chapter 22 placement

Insert after **Build a set that can disappoint you**, before **Six checks for each case**. Use this as a short example of designing a test that can distinguish investigation from guessing.

### One ticket, three possible explanations

An engineering support ticket comes in: “Our nightly export stopped arriving after the upgrade.” You can write a convincing reply before you open a single record. You can't yet tell the customer what happened.

In one version of the case, the run log shows no export since the upgrade, and the schedule record shows it was turned off. Check the schedule before recommending that someone re-enable it. In a second version, the job completed. The receipt shows an old folder and the account record names a different one. Correcting the destination makes more sense than rerunning a job that worked. In a third version, the records have expired. Escalate with what you couldn't verify and what the next person should look for. It is the same opening message every time.

QueueLab is a small engineering support experiment built around cases like this. The model can read fictional records, ask a bounded question, recommend a next step, or escalate. It cannot touch a customer account. The grader checks the decision against the records the model actually saw. If it correctly guesses that the schedule was disabled without inspecting evidence for it, the guess doesn't pass.

**Post-training** means training a model further after its initial training. QueueLab asks whether that can make a small model investigate better. The method here is fine-tuning on reviewed investigations, one decision at a time. Given the complaint and the records seen so far, what did the support engineer check next? When did they have enough evidence to make a recommendation? When did they stop? Fine-tuning uses those examples to change learned parameters. A new prompt changes what you ask the model at run time; a better tool changes what it can see or do. Neither retrains it.

The proposed method is **LoRA**. Leave the original model weights fixed and train a small add-on, called an adapter. Run the same model with the adapter off and on. The goal is to teach habits such as checking the run history before suggesting a delivery fix. The account's current schedule still belongs in a record the model can look up, not in its weights.

![Reviewed engineering support investigations train an adapter. The same base model, with and without the adapter, investigates the same unseen tickets. Both decisions are scored against the evidence each model saw.](figures/queuelab-post-training.png)

*Figure: The missing-export case tests whether adding an adapter changes the next step the model can justify. The diagram explains the comparison, not its results.*

Keep the prompt, permissions, and cases identical in both runs. Use tickets that weren't used to train the adapter, including look-alike complaints with different causes and cases where escalation is right. Count decisions supported by evidence. A higher score alone isn't enough if the model also makes more unsupported claims, or if the apparent gain could be noise. Save the traces so someone else can see where it changed its behavior.

The development run has exercised the simulator with scripted actions and unchanged models. It has not yet measured a post-training gain. Even a good result here would tell us how the model behaved on fictional cases, not whether it solved more customer problems. That takes a separate check after release.

## Appendix F placement

Add an entry under **Repositories Behind the Book**. Keep the link out of the printed text until the companion and the evidence it references are public.

### QueueLab

Read with Chapter 22, *The Shadow Run*. Start with the missing nightly export. Keep the complaint fixed, change the records, and see whether the recommended next step changes with them. A useful escalation counts when the available evidence cannot support a diagnosis.

The cases are fictional and the simulator is read-only. The proposed post-training comparison tests the same model with a small trained adapter on and off. The scripted replay explains the grading, not the adapter's performance or the experience of live customers.

## Editorial checks before publication

- Add a public companion link only after access and the replay destination are verified. Keep private run artifacts out of this draft.
- Update the status language from a reproducible before-and-after run, if available. Don't substitute the scripted checklist's score or example animation scores for that comparison.
- Keep Chapter 28 focused on ongoing evaluation. Cross-reference this experiment there only once there is a measured comparison worth discussing, whether or not the adapter helped.
- For the LoRA explanation: [Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models*](https://arxiv.org/abs/2106.09685). For publication, apply approved text to the canonical manuscript and regenerate the next printing without replacing the existing release.
