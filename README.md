# Local development lifecycle skills

Three skills share a local issue lifecycle:

```text
$specs → validate + deduplicate + triage → open
$work  → atomic claim → working → implement ↔ independent $review → completed
```

`needs-info` holds unresolved requests; `blocked` records an impediment; `closed` records duplicates, declined requests, and invalid issues. Work stays claimed during review and corrections. Standalone review never changes issue status.

## Usage

- `$specs Users cannot save an address containing Unicode characters.`
- `$work SPEC-1234ABCD`
- `$work Pick up the highest-priority actionable local issue.`
- `$work Add keyboard navigation to the settings menu.` — runs intake before claiming.
- `$review Review the current changes against SPEC-1234ABCD without editing files.`

To run several tasks, ask the coordinator to invoke `work` on implementing subagents. Each worker claims its own issue and gets an independent reviewer. Use separate worktrees for overlapping implementation areas; claims prevent duplicate task pickup, not conflicting edits to the same files.

## Design choices

- **Markdown with small YAML metadata**, rather than JSON-only issue documents: readable specifications, searchable headers, and machine-readable status. The helper accepts a deliberately restricted YAML format with JSON-encoded values and needs no YAML package.
- **One record per issue**, without an index: smaller reads and fewer shared-file conflicts. IDs look like `SPEC-1234ABCD`.
- **Atomic claims and freshness checks**: a Python helper uses local OS locking and atomic replacement. Creation checks a snapshot from the final duplicate search, so concurrent intake must reconcile instead of creating duplicate tasks from a stale backlog. Updates check issue revisions. Linked Git worktrees share the primary checkout's `.specs/issues/` directory. Separate clones/hosts need another coordination service.
- **Durable ownership**: no automatic lease expiry that could start a second worker while the first still runs. Interrupted tasks need deliberate release after checking their owner stopped.
- **Independent review with three verdicts**: `pass`, `changes-required`, `incomplete`. Missing required verification cannot count as success. The completion helper records the worker's attestation; it is not a security boundary against an agent fabricating evidence.

## Dependencies and installation

Keep the three skill folders installed together. For Codex, place or symlink `specs/`, `work/`, and `review/` in your configured skills directory (normally `~/.codex/skills/`); do not overwrite existing skills with the same names. The repository is the source of these skills; project issue records are created in the project where they are invoked.

The tracker requires Python 3.9+ on macOS/Linux. Git is required only for Git/worktree coordination. `work` requires subagent support. Browser review requires an installed `playwright-cli`, browser runtime, and prepared safe test environment. `CODING_STANDARD.md` applies when present; absence is reported rather than treated as a setup failure. Tests/lint/format follow the target project's configuration.

Review may create temporary artifacts outside the project. It must preserve project files, local tracking records, and persistent external state. Checks that cannot honor that restriction need a prepared disposable environment or an `incomplete` verdict.

No tracker or coding standard is created merely by installing the skills. The first authorized issue creation initializes `.specs/issues/` in its target project. See [the tracking contract](specs/references/tracking.md) for schema, transitions, CLI usage, and interrupted-claim recovery.

## Verification

Run `python3 specs/scripts/test_specs.py -v` for isolated integration tests, including concurrent claim races and linked-worktree coordination. All test records live outside this repository in temporary directories.
