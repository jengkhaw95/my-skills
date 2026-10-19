---
name: review
description: Read-only review of code changes or existing features for functional correctness, security, and repository coding standards. Use standalone or as the independent gate for the work skill; use the harness's browser automation for browser-facing behavior.
---

# Review

Return an evidence-backed assessment without modifying the project, tracker, or persistent external state. Temporary test/browser artifacts outside the project are allowed. Never fix code, update status, commit or publish, install dependencies, run formatter/linter fix mode, or invoke `work` during review.

## Independence

Review a candidate you did not implement. Do not accept the implementer's conclusion or summary as evidence; inspect the code, tests, and runtime behavior yourself. If you implemented the candidate, say so and stop rather than issuing a verdict.

## Establish scope

Read the repository's instruction files when present (for example `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or harness-specific rule files), `CODING_STANDARD.md` if present, requirements/acceptance criteria, and relevant code/tests. Honor the supplied checkout/range. Include relevant untracked changes when in scope. Without a supplied range, inspect repository state; ask when multiple plausible scopes change the verdict. Existing-feature reviews need not have a diff.

Inspect check scripts before running them. Use check-only lint/format commands and relevant tests only when they preserve project files. Redirect caches, reports, builds, and browser profiles to disposable directories outside the project using supported settings. A command called `test` or `lint` is not necessarily read-only. If a check requires project-relative outputs, use a disposable test copy outside the project or request a prepared environment from the implementer. Copy the actual candidate, including relevant untracked files; do not change source to make tests pass. Avoid hard links, VCS metadata pointing back to the original, and linked writable dependencies that could alter it. If isolation cannot be established, report the check as a gap. Check original repository state before/after for unexpected writes; disclose them without reverting or modifying unrelated changes.

## Assess

- **Feature:** acceptance criteria, normal flow, meaningful boundaries/error paths, regressions, and callers. Inspect surrounding implementation, not just diff lines. Distinguish observed behavior, static inference, and unverified claims.
- **Security:** relevant trust boundaries, authorization, input handling, sensitive data exposure, injection, and dependency/configuration effects. Report reachable risks with concrete conditions, not generic concerns.
- **Standards:** apply `CODING_STANDARD.md` and established conventions; check lint/format when configured. If the standard is absent, say so and use repository conventions. Personal preferences are not violations.

For browser-facing scope, including existing-feature reviews and changed flows, components, client state, navigation, accessibility interactions, or rendering, use the browser automation available to the harness and [the browser procedure](references/browser-checks.md). Static review alone cannot verify runtime behavior. Missing browser capability, browser runtime, server, credentials, or data is a gap. Browser tests do not replace static review or applicable lint/format checks.

## Precise report

Use this shape with findings ordered by impact:

```text
Verdict: pass
Scope: repository name + baseline/range or feature; current candidate identifier; repository-relative paths for changed files

Findings:
- [P1] Specific title — path:line
  Condition, observed/expected behavior, and concrete impact.
  Evidence: code path, reproduction, or check output.
  Requested change: smallest corrective outcome, without editing it.

Checks:
- Feature: criterion/path — passed / failed / not run; evidence
- Security: boundaries examined and outcome
- Standards: standard path or absent; lint/format results or not applicable
- Browser: scenarios/results, not applicable with reason, or blocked with reason

Gaps: unresolved evidence/environment limits, or none.
```

The first line must be exactly `Verdict: pass`, `Verdict: changes-required`, or `Verdict: incomplete`. Use `pass` only when every applicable gate is verified. Keep paths repository-relative and identify the repository by name; a report may be saved into a committed issue record, so do not include absolute checkout or home-directory paths.

P0: immediate severe impact; P1: high impact; P2: ordinary correctness/security/standard defect; P3: low-impact actionable issue. Give verified changed-code lines when possible; for missing behavior, name the relevant symbol/path. Keep optional improvements separate and do not let preferences block completion.

- `pass`: no actionable findings and every applicable acceptance/check gate verified. Explicitly say **“No actionable findings.”** Give concrete reasons for `not applicable` checks.
- `changes-required`: a substantiated actionable finding, even if checks are also blocked; list all gaps separately.
- `incomplete`: no substantiated finding, but scope/environment/evidence prevents complete assessment. Never present this as approval with caveats.

Standalone review returns the report to the user and leaves tracking untouched. As a reviewer for `work`—whether you run as a subagent, a fresh session, a separate invocation, or a human—return it to the implementer, who owns fixes and tracking writes.
