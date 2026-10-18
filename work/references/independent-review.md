# Independent review without a specific harness

Independence is about context, not product features. A reviewer must not have implemented the candidate and must not be steered by the implementer's conclusion.

## Preferred options

1. **Subagent or task facility.** Start a fresh-context agent with the `review` skill and the candidate scope. This is the usual choice when available.
2. **Fresh session or separate invocation.** Open a new session, or run a separate agent/model invocation, and give it the same brief. The session must not inherit the implementation conversation.
3. **Human reviewer.** A person who did not implement the change can review and write the report, especially when no agent isolation is available.

A reviewer that reuses the implementer's context, receives the implementer's proposed verdict, or only reviews a summary is not independent.

## Reviewer brief

Provide:

- The installed `review` skill and its instructions; ask the reviewer to follow it.
- Candidate scope: checkout path, baseline/range, and relevant untracked files.
- Issue ID, requirements, and acceptance criteria.
- Repository instruction/standard files that apply.
- Test/lint/format evidence already collected, clearly labeled as implementer claims.
- A test URL, prepared environment, and safe credentials if browser checks apply.
- Prohibitions: no edits to project files, tracker, commits, dependency installation, formatter/linter fix mode, or persistent external state. Temporary artifacts outside the project are allowed.
- The required report shape, including one of `pass`, `changes-required`, or `incomplete`.

Do not include "please pass", your preferred verdict, or a defense of the implementation. Ask the reviewer to verify claims independently and report gaps.

## If no independent context exists

Do not self-review and do not mark the issue `completed`. Preserve the candidate and evidence, then release the claim with status `blocked` and a note naming the missing capability, for example:

```text
Independent reviewer unavailable: this harness provides no subagent, fresh session, or separate invocation, and no human reviewer is available. Candidate and checks are ready for review.
```

When a human reviews, record a stable reviewer identity such as `human:<name>` in `complete`, and save their report to a file outside the repository. The helper checks only that the reviewer string differs from the owner; independence and the report's accuracy remain your attestation.
