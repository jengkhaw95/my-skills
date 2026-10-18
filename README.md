# Local development lifecycle skills

Three portable Agent Skills share a local issue lifecycle:

```text
specs  → validate + deduplicate + triage → open
work   → atomic claim → working → implement ↔ independent review → completed
```

`needs-info` holds unresolved requests; `blocked` records an impediment; `closed` records duplicates, declined requests, and invalid issues. Work stays claimed during review and corrections. Standalone review never changes issue status.

The skills are designed to be harness-agnostic. They do not require a particular agent product, model, subagent API, browser tool, or version-control system. [PORTABILITY.md](PORTABILITY.md) records the capability contract and fallbacks.

## Get started

### Install with the skills CLI

The [skills CLI](https://github.com/vercel-labs/skills) installs Agent Skills into the directory used by your harness. It requires Node.js 22.20+; the tracker also needs Python 3.9+.

```bash
npx skills add jengkhaw95/my-skills
```

The command prompts for the target harness and install scope. The `--list` preview should report `review`, `specs`, and `work`. Non-interactive examples:

```bash
# All three skills, globally, for Codex
npx skills add jengkhaw95/my-skills --skill '*' -a codex -g -y

# Every skill to every detected harness
npx skills add jengkhaw95/my-skills --all

# Preview without installing
npx skills add jengkhaw95/my-skills --list
```

Replace `codex` with `claude-code`, `cursor`, `gemini-cli`, `opencode`, `github-copilot`, or another agent ID supported by the CLI. Add `--copy` on systems where symlinks are restricted. Review skill contents before installing; installed skills run with the agent's permissions.

### Install from a local checkout

From the parent directory of a Git checkout named `my-skills`:

```bash
npx skills add my-skills
```

Or point at the folder explicitly from anywhere:

```bash
npx skills add ./path/to/my-skills
```

`npx skills add my-skills` is a local-path form; the CLI resolves the bare name as a Git repository on disk. For a remote install, the CLI needs an `owner/repo` source, so use `npx skills add jengkhaw95/my-skills`.

### Install manually

Keep the three skill folders together as siblings in the directory your harness scans for Agent Skills:

```text
<skills-directory>/
  specs/
  work/
  review/
```

Common locations include `~/.claude/skills/`, `~/.codex/skills/`, `~/.cursor/skills/`, `~/.gemini/skills/`, and project-local `.agents/skills/`, `.claude/skills/`, or `.github/skills/`. Consult your harness's documentation; the list is illustrative, not a requirement. Do not overwrite existing skills with the same names.

If the harness has no native skill discovery, point it at the relevant `SKILL.md` file (or paste that file as instructions) and keep the sibling folders reachable so `work` can find `specs` and `review`. The repository is the source of these skills; project issue records are created in the project where they are invoked.

### Verify and manage

```bash
npx skills list
npx skills update
npx skills remove specs work review
```

Add `-g` for global installs and `-a <agent>` to limit an operation to specific harnesses.

## Usage

Invoke a skill by name using your harness's syntax. Examples: `/specs` in Claude Code, `$specs` in Codex, `@specs` in clients that use mentions, or a plain request such as "use the specs skill to ...". Most harnesses also select a skill automatically from its description.

| Skill | Use it for | Example request |
| --- | --- | --- |
| `specs` | Validate, deduplicate, and triage a request into a tracked issue | `specs Users cannot save an address containing Unicode characters.` |
| `work` | Claim a task, implement it, and drive independent review | `work SPEC-1234ABCD` |
| `review` | Read-only review of a change or existing feature | `review Review the current changes against SPEC-1234ABCD without editing files.` |

More examples:

- `work Pick up the highest-priority actionable local issue.`
- `work Add keyboard navigation to the settings menu.` — runs intake before claiming.

To run several tasks, have a coordinating agent start `work` in separate worker contexts, or run separate sessions yourself. Each worker claims its own issue and obtains an independent reviewer. Use isolated working copies (for example Git worktrees) for overlapping implementation areas; claims prevent duplicate task pickup, not conflicting edits to the same files.

## Dependencies and capabilities

| Capability | Needed for | If unavailable |
| --- | --- | --- |
| File read/write and command execution | All skills | The lifecycle cannot run. |
| Python 3.9+ (standard library only) | Tracker helper | Intake, claim, and completion are unavailable; do not substitute a different tracker. |
| POSIX file locking (macOS, Linux, or WSL) | Tracker mutations | Read-only `root`, `list`, and `show` still work; use WSL on Windows. |
| Independent reviewer context (subagent, fresh session, separate invocation, or human) | `work` completion | Release to `blocked`; self-review cannot satisfy the gate. See [the independent-review guide](work/references/independent-review.md). |
| Browser automation (for example playwright-cli, a Playwright or Chrome DevTools MCP server, or a built-in browser tool) | Browser-facing review and reproduction | Record a gap; do not claim browser verification. See [the browser procedure](review/references/browser-checks.md). |
| Git | Worktree coordination | Optional. Without Git, the tracker uses the supplied project root and coordinates only that filesystem. |

`CODING_STANDARD.md` applies when present; absence is reported rather than treated as a setup failure. Tests, lint, and format follow the target project's configuration, using check-only modes during review. Repository instruction files (for example `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or harness-specific rule files) are read when present.

Review may create temporary artifacts outside the project. It must preserve project files, local tracking records, and persistent external state. Checks that cannot honor that restriction need a prepared disposable environment or an `incomplete` verdict.

No tracker or coding standard is created merely by installing the skills. The first authorized issue creation initializes `.specs/issues/` in its target project. See [the tracking contract](specs/references/tracking.md) for schema, transitions, CLI usage, and interrupted-claim recovery.

## Design choices

- **Markdown with small YAML metadata**, rather than JSON-only issue documents: readable specifications, searchable headers, and machine-readable status. The helper accepts a deliberately restricted YAML format with JSON-encoded values and needs no YAML package.
- **One record per issue**, without an index: smaller reads and fewer shared-file conflicts. IDs look like `SPEC-1234ABCD`.
- **Atomic claims and freshness checks**: a Python helper uses OS file locking and atomic replacement. Creation checks a snapshot from the final duplicate search, so concurrent intake must reconcile instead of creating duplicate tasks from a stale backlog. Updates check issue revisions. Linked Git worktrees share the primary checkout's `.specs/issues/` directory. Separate clones or hosts need another coordination service.
- **Durable ownership**: no automatic lease expiry that could start a second worker while the first still runs. Interrupted tasks need deliberate release after checking their owner stopped.
- **Independent review with three verdicts**: `pass`, `changes-required`, `incomplete`. Missing required verification cannot count as success. The completion helper records the worker's attestation; it is not a security boundary against an agent fabricating evidence.

## Verification

Run `python3 specs/scripts/test_specs.py -v` for isolated integration tests, including concurrent claim races and linked-worktree coordination. All test records live outside this repository in temporary directories.

## Portability and harness adapters

The portable core uses only the standard `SKILL.md` frontmatter (`name`, `description`). Host-specific metadata, wrappers, or installation scripts belong in a separate adapter layer, not in the skill body. This keeps the same skill usable when copied between harnesses. Some harnesses accept optional per-skill UI metadata; add it at install time rather than committing it into the portable skill.
