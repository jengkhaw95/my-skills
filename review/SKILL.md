---
name: review
description: Read-only review of code changes or existing features for functional correctness, security, and repository coding standards. Use standalone or as the independent gate for work, with playwright-cli for browser features.
---

# Review

Return an evidence-backed assessment without modifying the project, tracker, or persistent external state. Temporary test/browser artifacts outside the project are allowed. Never fix code, update status, commit, install dependencies, run formatter/linter fix mode, or invoke `work` during review.

## Establish scope

Read applicable `AGENTS.md`, `CODING_STANDARD.md` if present, requirements/acceptance criteria, and relevant code/tests. Honor the supplied checkout/range. Include relevant untracked changes when in scope. Without a supplied range, inspect repository state; ask when multiple plausible scopes change the verdict. Existing-feature reviews need not have a diff.

Inspect check scripts before running them. Use check-only lint/format commands and relevant tests only when they preserve project files. Redirect caches, reports, builds, and browser profiles to disposable directories outside the project using supported settings. A command called `test` or `lint` is not necessarily read-only. If a check requires project-relative outputs, use a disposable test copy outside the project or request a prepared environment from the implementer. Copy the actual candidate, including relevant untracked files; do not change source to make tests pass. Avoid hard links, Git metadata pointing back to the original, and linked writable dependencies that could alter it. If isolation cannot be established, report the check as a gap. Check original repository state before/after for unexpected writes; disclose them without reverting or modifying unrelated changes.

## Assess

- **Feature:** acceptance criteria, normal flow, meaningful boundaries/error paths, regressions, and callers. Inspect surrounding implementation, not just diff lines. Distinguish observed behavior, static inference, and unverified claims.
- **Security:** relevant trust boundaries, authorization, input handling, sensitive data exposure, injection, and dependency/configuration effects. Report reachable risks with concrete conditions, not generic concerns.
- **Standards:** apply `CODING_STANDARD.md` and established conventions; check lint/format when configured. If the standard is absent, say so and use repository conventions. Personal preferences are not violations.

For browser-facing scope, including existing-feature reviews and changed flows, components, client state, navigation, accessibility interactions, or rendering, use **`playwright-cli`** and [the browser procedure](references/browser-checks.md). Static review or another browser tool cannot satisfy this dependency. Missing CLI, browser, server, credentials, or data is a gap. Browser tests do not replace static review or applicable lint/format checks.

## Precise report

Use this shape with findings ordered by impact:

```text
Verdict: pass | changes-required | incomplete
Scope: checkout + baseline/range or feature; current candidate identifier

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

P0: immediate severe impact; P1: high impact; P2: ordinary correctness/security/standard defect; P3: low-impact actionable issue. Give verified changed-code lines when possible; for missing behavior, name the relevant symbol/path. Keep optional improvements separate and do not let preferences block completion.

- `pass`: no actionable findings and every applicable acceptance/check gate verified. Explicitly say **“No actionable findings.”** Give concrete reasons for `not applicable` checks.
- `changes-required`: a substantiated actionable finding, even if checks are also blocked; list all gaps separately.
- `incomplete`: no substantiated finding, but scope/environment/evidence prevents complete assessment. Never present this as approval with caveats.

Standalone review returns the report to the user and leaves tracking untouched. As a work subagent, return it to the implementer, who owns fixes and tracking writes.
