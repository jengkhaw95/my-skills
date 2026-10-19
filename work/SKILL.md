---
name: work
description: Implement a tracked local task, pick up ready backlog work, or execute a raw change request, then obtain independent review and resolve findings before completion.
---

# Work

Carry implementation through verification and independent review. Keep the issue `working` throughout review and correction.

## Resolve and claim

Read the repository's instruction files when present (for example `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or harness-specific rule files) and `CODING_STANDARD.md` if present. Locate the installed `specs` and `review` skills—by skill discovery or by resolving them from the same parent directory as this skill—and read their entrypoints and the specs tracking contract. If either skill/helper is missing, report the dependency; do not substitute a different tracker or self-review.

- **Tracking ID:** inspect the record and acceptance criteria. `completed`/`closed` does not authorize reopening; determine whether this is a regression or explicit reopening. Resolve `needs-info`/`blocked` before moving to `open`.
- **Backlog pickup:** select an actionable `open` task by priority, dependencies, and fit. Read its full record. If another agent wins the claim, choose another suitable task when general pickup was authorized; for an explicit ID, report its owner and stop.
- **Raw request:** run specs intake, including deduplication, first. Reuse an actionable record or create one, then claim it. This is authorized by the implementation request; no separate intake approval is necessary. Do not implement unresolved requests.

Choose an owner token unique to this run (for example an agent identity plus a UUID) and run atomic `claim` with that token and the inspected revision **before editing source**. A read followed by a manual status edit is not a claim. Never steal a task, expire ownership automatically, or resume another run's token. Deliberate release requires verifying the former worker stopped. Claims coordinate the same local filesystem; in a Git checkout, linked worktrees share the primary tracker's records, while separate clones or hosts need external coordination.

For delegated work, each implementing agent claims its own ID. A coordinator must not claim using another token and hand over implicitly. Different IDs may touch the same files: use isolated working copies (for example Git worktrees) where appropriate and coordinate overlapping scopes. Claims alone do not make simultaneous source edits safe.

## Implement and verify

Establish existing changes, intended scope, and acceptance criteria. Preserve unrelated work. Implement, run relevant tests, and run applicable lint/format checks. Fix applicable failures; distinguish pre-existing failures with evidence. Avoid unrelated cleanup.

Keep scope and evidence accurate through owner-checked record updates. Ask about facts that change requested behavior; continue only independent work while waiting. If blocked, record the impediment and release to `blocked`; do not claim completion.

## Independent review loop

1. Freeze a candidate. Capture repository identity (name and baseline/commit), repository-relative paths for the changed and relevant untracked files, acceptance criteria, tracking revision, and validation evidence. Never record an absolute checkout or home-directory path; the record's location already identifies the repository. In a shared checkout, identify this task's changes and preserve other agents' edits.
2. **Obtain an independent reviewer.** Use the strongest isolated context the harness offers: a subagent/task tool, a fresh session, a separate agent/model invocation, or a human reviewer. Follow [the independent-review guide](references/independent-review.md) for the reviewer brief and fallbacks. Explicitly instruct the reviewer to use the installed `review` skill. Provide candidate scope, issue, requirements, standards, local test URL/setup, and test evidence. Require its structured verdict; prohibit writes to project files, tracker, or persistent external state. Temporary artifacts outside the project are allowed. Do not prime the verdict. If no independent context is available, required review is blocked; self-review cannot satisfy it.
3. Fix valid findings and rerun affected checks. For disputed findings, provide evidence and request reassessment. Send the latest candidate back for review, including intervening changes: earlier approval does not cover later edits. Keep the claim. Continue until `pass` with evidence for every applicable gate. If progress stalls or needs a user decision, preserve findings, release to `blocked`, and report the specific impediment rather than loop indefinitely.
4. `incomplete` requires missing evidence and another review; unavailable browser/environment, failed applicable checks, or untested acceptance criteria cannot become a pass. `changes-required` needs correction or evidence-backed reassessment.
5. On `pass`, verify the approved candidate is still current. Save the response to a temporary file outside the repository. Use `complete` with your owner token, a distinct reviewer identity (agent, session, or human), reviewed scope, report file, and inspected record revision. The helper records the caller's attestation; it cannot prove reviewer independence or code correctness. Keep `working` until completion succeeds.

Report ID, change, verification, independent review result, and material limitations. Completion means implementation and review passed; publishing, merging, deployment, and messaging others require their own authorization.
