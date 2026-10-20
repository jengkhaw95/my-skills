---
name: engineering
description: Main entry skill for engineering tasks. Select and coordinate the supporting skills for investigation, design, implementation, review, and technical writing while applying shared engineering principles.
---

# Engineering

Deliver the requested outcome with the least complexity that meets the requirements.
Select the supporting procedure from the request and keep responsibility for the complete outcome.

## Required language

Use ASD-STE100 Simplified Technical English for all prose, including replies, comments, documents, and instructions for other agents.
Use approved words with their approved meanings and parts of speech.
Use permitted technical nouns and technical verbs consistently.
Limit procedure sentences to 20 words and descriptive sentences to 25 words.
Use active voice and direct commands. Put conditions before actions.
Keep code, commands, identifiers, and direct quotations exact.
Check the official rules and dictionary when available.
If a vocabulary check is unavailable, report that gap. Do not claim full STE compliance without evidence.

## Route the task

Read the selected supporting skill in full before using its procedure.
Resolve each link from this file's directory, not the project's working directory.
If installation changes the layout, locate the installed skill by its exact name through available skill discovery.
Routing means reading and following instructions. It does not require another agent or a special invocation API.

| Request or phase | Supporting skill | Boundary |
| --- | --- | --- |
| Explain behavior, diagnose a symptom, analyze a trace, or recommend an option. | [investigate](../investigate/SKILL.md) | Return evidence and conclusions without product changes. |
| Define architecture, data models, interfaces, or compare consequential alternatives. | [design](../design/SKILL.md) | Produce a design or disposable prototype. Implement only when also requested. |
| Build a feature, fix a defect, refactor, or improve measured behavior. | [work](../work/SKILL.md) | Carry the requested change through verification and review. |
| Assess a design, implementation, or existing feature. | [review](../review/SKILL.md) | Return an assessment without editing the candidate. |
| Write or edit prose, documents, comments, or skill instructions. | [technical-writing](../technical-writing/SKILL.md) | Apply the writing procedure to the requested text and task reports. |

Read `technical-writing` once for prose produced during the task.
For other procedures, load only the skills needed for the current request or phase.
For a small task outside these categories, use the shared principles below directly.

For mixed requests, select a primary procedure from the requested outcome.
Use supporting procedures at the relevant phase instead of forcing every task through all five skills.
For example, a substantial feature can require investigation, design, implementation, and review.
A read-only question ends with its answer unless the user also requested implementation.
A review finding does not authorize a fix by itself.

Keep the original scope, user instructions, and completion criteria across phase changes.
An explicit skill choice or restriction from the user takes precedence over automatic routing.
Do not route supporting skills back through this entry point or create recursive skill calls.
If a required skill is missing, report its name and the affected phase.
Continue only work covered by available instructions. Do not invent the missing procedure or claim it ran.

Use an independent context for independent review when available or required.
Reading `review` in the implementer's context remains self-review.
Keep responsibility for integration, evidence, and the final report in the coordinating context.

## Establish the outcome

1. State the user outcome, scope, constraints, and observable completion criteria.
2. Inspect the current implementation, relevant instructions, and existing changes.
3. Separate observed facts from assumptions and preferences.
4. Use a small experiment to settle an observable question.
5. Ask the user about consequential preferences or missing requirements that evidence cannot resolve.

Proceed with authorized, reversible work. Explain material assumptions.
Respect explicit approval requirements and stop requests.
Obtain authorization before destructive actions, publication, deployment, or messages to other people unless already authorized.
Challenge an unsupported premise. Give your judgment with evidence.

## Keep the design simple

- Define the data model, valid states, ownership, and access patterns before writing logic.
- Encode domain rules in types, state transitions, tables, or suitable collections.
- Validate external data where it enters the system.
- Use validated internal data without repeated checks for states the model excludes.
- Keep business rules separate from transport, storage, and framework details.
- Remove unnecessary code within scope before adding a new mechanism.
- Reduce hidden state, pass-through layers, and speculative abstractions.
- Consider the target design with the new requirement present from the start.
- Preserve compatibility when external callers require it.
- Make retries and interrupted operations converge to the intended state.
- Separate concurrent write targets where possible. Control access when a shared target is necessary.
- Prefer a clear user experience and a small public interface over implementation convenience.

## Execute in verifiable units

1. Divide substantial work into small units with a check at each boundary.
2. Identify dependencies, shared writes, and the riskiest unknown before starting independent work.
3. Use the smallest repeatable script when it makes an edit or check more reliable.
4. Verify the current unit before building on it.
5. Inspect the actual output or behavior. A successful build alone does not prove the requested result.
6. Test observable behavior. Keep tests independent of incidental implementation details.
7. Replace recurring corrections with types, checks, or automation when practical.

For long work, record decisions, reasons, evidence, and outcomes at meaningful checkpoints.
On resume, inspect the saved state and verify material claims before continuing.
On pause, preserve the current work and record the next action.

## Delegate only when useful

Use delegation only when available, permitted, and likely to improve coverage or independent judgment.
A script is preferable to several agents repeating the same mechanical operation.

- Give each worker the outcome, constraints, file scope, exact candidate, verification method, and expected report.
- Assign separate write targets. Define how results will be combined.
- For parallel checks, map every required area to an owner.
- Prefer a fresh context for new work. Reuse a worker when essential live state would otherwise be lost.
- Inspect each result and its evidence yourself. A missing or failed result is a gap.
- Resolve disagreements through evidence. Agreement alone is not proof.

Without delegation, perform the applicable steps sequentially and report limits on independent review.

## Report the result

Lead with the effect on the user.
Explain material choices and what the maintainer must understand.
State what was verified, how it was verified, and what remains uncertain.
Link only evidence you inspected or produced.
Do not turn an incomplete check into a success claim.
