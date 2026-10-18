# Portability contract

These skills are portable instructions plus one Python standard-library helper. They work in any agent harness that can read files, execute commands, and run Python 3.9+. Host-specific features are optional adapters, not requirements.

## Portable core

- `SKILL.md` with standard `name` and `description` frontmatter. No provider-specific fields are required.
- Markdown references under `references/` and deterministic helpers under `scripts/`.
- Capability-based instructions: when a feature is missing, the skill reports a gap or blocks instead of substituting an unsafe path.
- No assumption about model, provider, agent product, subagent API, browser tool, search tool, or VCS.

## Capability matrix

| Capability | Required by | Fallback if missing |
| --- | --- | --- |
| Read files and run commands | All skills | Not supported; the lifecycle needs a tool-using agent. |
| Python 3.9+ | Tracker helper | Do not substitute a different tracker; report the dependency. |
| POSIX file locking | Tracker mutations | Read-only commands work; use WSL on Windows. |
| Independent reviewer context | `work` completion | Fresh session, separate invocation, or human reviewer. If none, release to `blocked`. |
| Browser automation | Browser-facing review/reproduction | Report a gap and an `incomplete` review; do not claim runtime verification. |
| Git | Linked-worktree coordination | Optional; the tracker falls back to the supplied project root. |

## Tool mapping

| Capability | Examples | Fallback |
| --- | --- | --- |
| Content search | ripgrep, grep, editor search, a host search tool | Inspect candidate files directly; report the limitation if the repo is too large. |
| Repository instructions | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, host rule files | Use repository conventions; report the absence of `CODING_STANDARD.md`. |
| Browser automation | playwright-cli, a Playwright or Chrome DevTools MCP server, a built-in browser | Mark the browser gate incomplete. |
| Independent reviewer | subagent/task tool, fresh session, separate invocation, human | Release the task to `blocked`. |
| Version control | Git, another VCS, or a plain directory | The tracker uses the supplied project root. |

## Invocation

| Harness style | Example | Notes |
| --- | --- | --- |
| Slash-command hosts | `/specs`, `/work`, `/review` | Hosts that expose skills as slash commands. |
| Mention-style hosts | `$specs`, `$work`, `$review` | Hosts that invoke skills with a mention sigil. |
| At-mention clients | `@specs`, or the client's syntax | Use whatever the client documents. |
| Instructions-only | "Read <path>/SKILL.md and follow it." | Keep sibling folders reachable for `specs` and `review`. |
| Plain chat with file/command tools | "Use the skill at <path>/SKILL.md." | The agent must be able to execute Python and edit files. |

The skill name (`specs`, `work`, `review`) is the stable interface; the sigil is host syntax.

## Installation layouts

Keep the three folders as siblings. Native discovery directories vary by host; common conventions include `~/.claude/skills/`, `~/.codex/skills/`, `~/.cursor/skills/`, `~/.gemini/skills/`, and project-local `.agents/skills/`, `.claude/skills/`, or `.github/skills/`. Consult the host's documentation and avoid overwriting existing skills.

If the host supports only one instruction file, keep the folder tree on disk and reference `specs/SKILL.md`, `work/SKILL.md`, and `review/SKILL.md` by absolute path. Do not flatten the skills into a single prompt: they rely on on-demand references and the tracker script.

## Independence

Independence is a context property, not a product feature. A reviewer is independent when it did not implement the candidate and is not steered by the implementer's conclusion. Subagents, fresh sessions, separate model invocations, and human reviewers can all qualify. Self-review, a summary written by the implementer, or a reviewer primed with the desired verdict does not.

See [the independent-review guide](work/references/independent-review.md).

## Browser automation

Any browser capability is acceptable if it can navigate, inspect the page, interact, and expose console/network errors, and if its artifacts and profiles can stay outside the project. See [the browser procedure](review/references/browser-checks.md). Static review is still required; a browser check does not replace it.

## Tracker portability

The tracker is Markdown plus a Python helper. It works in a Git checkout or a plain directory. Under Git, linked worktrees share the primary checkout's records; without Git, the supplied project root is the coordinate. The helper uses `fcntl.flock` for mutations; read-only commands do not lock. On Windows, use WSL for mutations.

## Adding host support

Keep the portable core unchanged. Put host-specific metadata, wrappers, installation scripts, and frontmatter extensions in a separate adapter layer or generate them at install time. Do not add host-specific fields to the portable `SKILL.md` unless the skill is intentionally host-specific.

If a host needs a UI manifest, generate it from the skill's `name`, `description`, and README examples rather than making the workflow depend on it.
