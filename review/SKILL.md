---
name: review
description: Review a design, code change, or existing behavior for correctness, security, simplicity, and verification. Use for a read-only assessment, a second opinion, or independent review before delivery.
---

# Review

Assess the actual candidate and return findings supported by evidence.
Do not edit project files or persistent external state.
Use disposable copies when checks would write files.

## Required language

Use ASD-STE100 Simplified Technical English for all prose, including findings, reports, and instructions for other agents.
Use approved words with their approved meanings and parts of speech.
Use permitted technical nouns and technical verbs consistently.
Limit procedure sentences to 20 words and descriptive sentences to 25 words.
Use active voice and direct commands. Put conditions before actions.
Keep code, commands, identifiers, and direct quotations exact.
Check the official rules and dictionary when available.
If a vocabulary check is unavailable, report that gap. Do not claim full STE compliance without evidence.

## Establish scope

1. Identify the requirements and exact design, version, diff, or existing behavior under review.
2. Inspect repository instructions, relevant code, callers, tests, and current changes.
3. Include relevant untracked files when they belong to the candidate.
4. State whether the review is independent. Label review of your own work as self-review.
5. Inspect check commands before running them. Isolate writes and avoid production side effects.

Do not treat the implementer's summary or another reviewer's conclusion as proof.
Do not broaden the scope to unrelated cleanup.
Ask when materially different review scopes are plausible.

## Examine the candidate

- Verify the requested behavior and the conditions under which it can fail.
- Trace callers and surrounding code instead of reading only changed lines.
- Check valid states, data ownership, errors, retries, persistence, and concurrency where relevant.
- Inspect relevant authorization, input validation, injection risks, and sensitive data handling.
- Check required compatibility and migration of callers.
- Apply documented standards and established conventions.
- Identify unnecessary mutable state, duplicated decisions, or layers that hide no meaningful complexity.
- Check that comments explain necessary constraints and agree with the code.
- Verify that tests assert observable behavior and can detect the relevant failure.

For browser or command-line behavior, use that interface when the environment permits it.
For visual equivalence, compare matching states and exercise interactions.
For performance claims, inspect the workload, repeated samples, errors, completed work, and limiting resource.
For a design, test assumptions against failure cases and compare viable simpler alternatives.

Treat automated findings as claims to verify.
Merge duplicate findings and assess each remaining claim on its merits.
Explain why a disputed finding is valid or unsupported.
Personal preferences do not become defects without a requirement or concrete impact.

## Report precisely

Lead with one verdict:

- `pass`: No actionable findings remain, and all applicable checks have evidence.
- `changes-required`: At least one actionable defect has supporting evidence.
- `incomplete`: No defect is established, but missing scope or evidence prevents a complete assessment.

State the reviewed candidate and whether the review was independent.
Order findings by impact. Each finding must include:

- The affected path and line, symbol, or design element.
- The triggering condition and expected behavior.
- The observed result or a clearly labeled static inference.
- The concrete impact and supporting evidence.
- The smallest corrective outcome, without applying it.

List checks as passed, failed, not run, or not applicable with a reason.
Keep optional improvements separate from blocking findings.
Include all evidence gaps, even when the verdict is `changes-required`.
An approval applies only to the candidate that was reviewed.
Return the report without fixing the candidate or changing task status.
