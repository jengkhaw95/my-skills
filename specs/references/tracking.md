# Local tracking contract

## Format and location

One `.specs/issues/SPEC-<8-uppercase-hex>.md` per issue, committed with the repository when desired. Markdown provides readable specs; flat YAML frontmatter provides searchable metadata. The helper writes JSON-encoded YAML values using Python's standard library; it has no host-specific dependency. This is **restricted YAML**: every line is `key: <JSON value>`; do not convert it to general YAML, comments, folded strings, or unquoted text. The body is ordinary Markdown, including fences and horizontal rules.

Fields: `schema`, `id`, `title`, `kind`, `status`, `priority`, `revision`, `created_at`, `updated_at`, `owner`, `claimed_at`, `reviewer`, `review_scope`. Schema is 1; timestamps are UTC; IDs are immutable. Every mutation increments revision. `list` emits metadata only; `show` emits a full record; `list --query` searches titles/bodies with case-insensitive ANDed terms. Try separate searches for different terminology. No aggregate index requires synchronization.

For final duplicate discovery use `list --snapshot`, which emits `{snapshot, issues}`. The snapshot hashes all records, even with query/status filters. `create --expected-snapshot TOKEN` compares that generation under the mutation lock and rejects creation if any issue changed. On conflict repeat discovery and inspect matches, not merely refresh the token. This closes concurrent intake races for agents following the search protocol; it cannot detect semantic duplicates by itself. Two intentionally sequential requests still require careful duplicate assessment.

`root` emits `project_root`, `tracking_root`, `lock_path`. Linked Git worktrees share `.specs` in the primary worktree from `git worktree list`; mutations there are intentional and output identifies the location. The primary checkout must remain accessible. Outside Git, callers must supply the same project root. Locking uses `fcntl.flock` on POSIX; read-only commands do not lock. On Windows, use WSL for mutations. Locks cannot coordinate separate clones/hosts or arbitrary editors. Do not edit metadata directly or mix helper versions on a shared tracker.

## Path and identity hygiene

Records may be committed and published. Identify the checkout by repository name and use repository-relative paths (`src/config.ts`, `HEAD 0dca40d`); the record's own location already identifies the repository. Never write an absolute path containing a home directory or user name (`/Users/<name>`, `/home/<name>`, `C:\Users\<name>`), a hostname, or a private checkout layout. Use role-neutral reviewer identities such as `human:reviewer-1` rather than a personal name. The helper rejects body, title, scope, handoff-note, and review-report text containing an absolute home path.

## Lifecycle

| Status | Meaning | Pickup? |
| --- | --- | --- |
| `needs-info` | Required clarification unresolved | No |
| `open` | Actionable and unclaimed | Yes |
| `working` | Claimed implementation, correction, or review | No |
| `blocked` | Impediment recorded | No |
| `completed` | Candidate passed independent review and checks | No |
| `closed` | Duplicate, invalid, declined, superseded; reason recorded | No |

`claim` atomically changes `open → working`, requiring the inspected revision and a unique owner token. Concurrent losers fail without writing. Ownership has no timeout. `update` requires a revision and the owner token for working issues; it cannot exit `working`. `release` requires ownership and a handoff note, changing `working → open|blocked`. To recover an interrupted claim, first verify that its worker stopped, then deliberately release using the recorded token. This is administrative recovery, not permission to impersonate a running worker. There is no force/expiry flag.

`complete` requires ownership, revision, a distinct reviewer identity (an agent, a fresh session, or a human such as `human:reviewer-1`), scope, and a saved report starting `Verdict: pass` and containing `No actionable findings.`. This records an attestation, not proof of independent/correct review. Nonworking states can be changed through revision-checked `update`, except entering `working`/`completed` is forbidden. Explicit reopening clears prior ownership/review metadata; historical reports stay in the body. Do not reopen completed/closed records without a user-directed reason or silently enlarge their scope.

P0: urgent critical outage/loss/exposure; P1: high impact or core flow blocked; P2: normal bug/feature priority (default); P3: minor improvement. Priority expresses impact, not certainty.

## Body template

Keep relevant sections:

```markdown
# <Title>

## Request
Problem/user outcome; expected versus actual behavior.

## Validation
Evidence, reproduction/results or feature rationale.
Separate facts from hypotheses; identify checks not run and why.

## Scope
Scope, constraints, and explicit exclusions where needed.

## Acceptance criteria
- Observable, checkable result.

## Context
Relevant paths, related IDs, dependencies, unresolved questions.

## Progress and handoff
Implementation/check evidence or blocker when applicable.
```

## CLI

Resolve `TRACKER` to the installed specs skill's `scripts/specs.py`. `PROJECT`, `BODY`, `NOTE`, `REPORT` denote actual absolute paths. Prepare input files outside the project. Pass user text as argument arrays or safely quoted arguments/file inputs, never shell code.

```text
python3 TRACKER --repo PROJECT root
python3 TRACKER --repo PROJECT list
python3 TRACKER --repo PROJECT list --status open --status working --query "checkout error"
python3 TRACKER --repo PROJECT list --snapshot --query "valid address"
python3 TRACKER --repo PROJECT show SPEC-1234ABCD
python3 TRACKER --repo PROJECT create --expected-snapshot TOKEN --title "Checkout rejects valid address" --kind bug --priority P2 --body-file BODY
python3 TRACKER --repo PROJECT update SPEC-1234ABCD --expected-revision 1 --body-file BODY
python3 TRACKER --repo PROJECT claim SPEC-1234ABCD --expected-revision 2 --owner AGENT-RUN-TOKEN
python3 TRACKER --repo PROJECT update SPEC-1234ABCD --expected-revision 3 --owner AGENT-RUN-TOKEN --body-file BODY
python3 TRACKER --repo PROJECT release SPEC-1234ABCD --owner AGENT-RUN-TOKEN --status blocked --note-file NOTE
python3 TRACKER --repo PROJECT complete SPEC-1234ABCD --expected-revision 4 --owner AGENT-RUN-TOKEN --reviewer REVIEW-AGENT-ID --scope "checkout + baseline + candidate identifier" --review-file REPORT
```

These are separate examples, not a sequence. Reread after mutations and use the actual revision. `create --status needs-info` captures an unresolved request only when asked. `update --status closed --body-file BODY` records a closure reason; `update --status open --body-file BODY` deliberately unblocks/reopens a nonworking record.

`root`, `list`, and mutations emit JSON; `show` emits Markdown. Errors exit nonzero without repairing corrupt records. Mutations take the same short-lived lock and use atomic replacement. Lock files live in the shared Git directory or `.specs/.runtime/` outside Git; do not commit non-Git runtime files. Process exit releases the OS lock, while the durable task claim remains.

Install the set together as sibling `specs`, `work`, `review` directories and locate them by skill discovery or from their common parent directory; do not assume the project's working directory contains them. Standalone review needs no tracker.
