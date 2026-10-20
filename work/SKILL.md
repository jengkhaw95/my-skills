---
name: work
description: Implement a feature, fix a defect, refactor code, or improve measured behavior. Use for a change request that must reach a verified result, with proportionate planning and review.
---

# Work

Carry the authorized change through implementation, verification, and review.
Use the project's existing task records when relevant. No particular tracker or helper is required.

## Required language

Use ASD-STE100 Simplified Technical English for all prose, including replies, comments, documents, and instructions for other agents.
Use approved words with their approved meanings and parts of speech.
Use permitted technical nouns and technical verbs consistently.
Limit procedure sentences to 20 words and descriptive sentences to 25 words.
Use active voice and direct commands. Put conditions before actions.
Keep code, commands, identifiers, and direct quotations exact.
Check the official rules and dictionary when available.
If a vocabulary check is unavailable, report that gap. Do not claim full STE compliance without evidence.

## Establish the change

1. Read the request, relevant repository instructions, current implementation, and tests.
2. Inspect existing changes and preserve unrelated work.
3. State the user outcome, scope, constraints, and observable completion criteria.
4. Resolve factual uncertainty through inspection or a small experiment.
5. Ask about consequential missing requirements. Continue independent work while waiting.

For substantial work, identify dependencies, independent units, shared write targets, and the smallest safe sequence.
Define the data model, valid states, and ownership before writing logic.
Compare alternatives when a consequential design has no established solution.
Use the smallest change that solves the problem.

## Apply the matching procedure

| Change | Required evidence |
| --- | --- |
| Defect | Reproduce the failure, identify its cause, and verify the original case after the fix. |
| Feature | Define the observable behavior and verify normal, boundary, and relevant error cases. |
| Refactor | Capture the behavior before the change and prove that the new structure preserves it. |
| Performance | Capture a realistic baseline, identify the limiting resource, and compare repeated measurements. |
| Visual parity | Capture the reference and compare the same states, dimensions, content, and interactions. |
| Skill or instruction change | Check metadata and links. Exercise representative tasks when the change affects behavior. |

Fix the first incorrect decision instead of hiding its consequences.
Handle an unusual state locally only when that state is legitimate.
If two fixes fail under the same assumption, test the assumption before trying another fix.

During refactoring, remove unnecessary layers and migrate affected callers.
Delete an old internal interface when no required caller needs it.
Preserve external compatibility where required.
For migrations, declare verification boundaries and any temporary breakage inside the isolated work.

## Implement and verify

1. Make one coherent change.
2. Run the relevant behavioral check before building on that change.
3. Use repeatable scripts for mechanical edits or checks when they improve reliability.
4. Run applicable tests and configured checks.
5. Exercise the actual interface, including the browser or command line when relevant.
6. Inspect the final diff and actual artifacts.

For visual parity, keep the reference fixed and compare images under matching conditions.
Define any permitted difference before the change. Require zero difference when exact parity is the requirement.

Test outcomes that users or callers can observe.
Derive expected results from requirements rather than the implementation under test.
A test must detect broken behavior and survive a change to internal structure.
Keep comments that explain a necessary, non-obvious constraint.
Prefer types or executable checks for constraints that can be enforced.

For long work, record each material decision, its reason, evidence, and result.
Preserve a resume note at a safe pause boundary.

## Measure improvements honestly

Use the same realistic workload, versions, production settings, and cache conditions for both alternatives.
Confirm that the measured work completed and produced correct results.
Count errors and work units.
Use a separate profiling run to identify the limiter.
Alternate the alternatives across at least five runs each for a comparative performance claim.
Report units, sample count, median, spread, environment, and the effect on the full user operation.
Check the result against resource limits and the share of total time that the changed operation consumed.
If variation obscures the difference, report an inconclusive result.
Also report an inconclusive comparison when settings, errors, completed work, or the limiter remain unverified.

For sustained improvement, define a target, regression checks, and a stop condition before the loop.
Keep the measurement method fixed across attempts.
Change one hypothesis at a time. Keep verified improvements and remove unsuccessful task changes.
Do not weaken the target or check to manufacture success.

## Review and finish

Inspect correctness, relevant security boundaries, repository conventions, and unnecessary complexity.
For nontrivial changes, seek independent review when available.
Give the reviewer the exact candidate, requirements, scope, and verification evidence without suggesting a verdict.
Assess each finding on its evidence. Fix valid findings and reject unsupported findings with a concrete reason.
Rerun affected checks and obtain reassessment after changes to the reviewed candidate.

If independent review is unavailable, label self-review and report the gap.
If independent review is required by the task, leave completion open until it occurs.
Do not claim a failed or unavailable required check passed.
Publish, merge, deploy, or message other people only within the user's authorization.

Report the user effect, material design choice, verification results, review status, and unresolved limits.
