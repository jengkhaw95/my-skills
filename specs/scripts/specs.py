#!/usr/bin/env python3
"""Local issue records with atomic, owner-checked transitions (Python 3.9+, stdlib)."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid

try:
    import fcntl
except ImportError:  # pragma: no cover - read-only commands still work on non-POSIX hosts
    fcntl = None


STATES = ("open", "needs-info", "working", "blocked", "completed", "closed")
KINDS = ("bug", "feature", "task")
PRIORITIES = ("P0", "P1", "P2", "P3")
ID_PATTERN = re.compile(r"SPEC-[0-9A-F]{8}\Z")
HOME_PATH_PATTERN = re.compile(
    r"(?<![A-Za-z0-9._-])(?:/Users[\\/]+|/home[\\/]+|[A-Za-z]:[\\/]+Users[\\/]+)[A-Za-z0-9._-]+"
)
FIELDS = {
    "schema", "id", "title", "kind", "status", "priority", "revision",
    "created_at", "updated_at", "owner", "claimed_at", "reviewer", "review_scope",
}


class TrackerError(Exception):
    pass


def now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise TrackerError(f"{label} must be nonempty")
    return value.strip()


def reject_home_paths(text, label):
    if HOME_PATH_PATTERN.search(text):
        raise TrackerError(
            f"{label} contains an absolute home path; identify the repository by name "
            "and use repository-relative paths"
        )


def hygienic(value, label):
    value = nonempty(value, label)
    reject_home_paths(value, label)
    return value


def git(directory, *args):
    result = subprocess.run(
        ["git", "-C", str(directory), *args], capture_output=True, text=True,
        check=False,
    )
    if result.returncode:
        raise TrackerError(result.stderr.strip() or "Git lookup failed")
    return result.stdout.strip()


def locate(directory):
    project = Path(directory).expanduser().resolve()
    if not project.is_dir():
        raise TrackerError(f"Project directory does not exist: {project}")
    try:
        probe = subprocess.run(
            ["git", "-C", str(project), "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, check=False,
        )
    except FileNotFoundError:
        probe = None
    if probe and probe.returncode == 0 and probe.stdout.strip() == "true":
        # -z avoids Git's path quoting for whitespace, Unicode, and newlines.
        entries = git(project, "worktree", "list", "--porcelain", "-z").split("\0")
        primary = next((e[9:] for e in entries if e.startswith("worktree ")), None)
        if not primary or not Path(primary).is_dir():
            raise TrackerError("Primary Git checkout is unavailable")
        project = Path(primary).resolve()
        common = Path(git(project, "rev-parse", "--git-common-dir"))
        if not common.is_absolute():
            common = project / common
        lock = common.resolve() / "local-specs" / "tracker.lock"
    else:
        # An inaccessible/corrupt Git repository must not become a second tracker.
        if any((ancestor / ".git").exists() for ancestor in (project, *project.parents)):
            raise TrackerError("Git metadata exists but repository lookup failed")
        lock = project / ".specs" / ".runtime" / "tracker.lock"
    return project, project / ".specs", lock


def issue_path(root, issue_id):
    if not ID_PATTERN.fullmatch(issue_id):
        raise TrackerError("ID must match SPEC- followed by 8 uppercase hex digits")
    return root / "issues" / f"{issue_id}.md"


def validate(meta, path):
    if set(meta) != FIELDS or type(meta["schema"]) is not int or meta["schema"] != 1:
        raise TrackerError(f"Unsupported or malformed record schema: {path}")
    if meta["id"] != path.stem or not ID_PATTERN.fullmatch(meta["id"]):
        raise TrackerError(f"Record ID does not match filename: {path}")
    if meta["status"] not in STATES or meta["kind"] not in KINDS:
        raise TrackerError(f"Invalid status/kind: {path}")
    if meta["priority"] not in PRIORITIES:
        raise TrackerError(f"Invalid priority: {path}")
    if type(meta["revision"]) is not int or meta["revision"] < 1:
        raise TrackerError(f"Invalid revision: {path}")
    for key in ("title", "created_at", "updated_at"):
        nonempty(meta[key], key)
    for key in ("owner", "claimed_at", "reviewer", "review_scope"):
        if meta[key] is not None:
            nonempty(meta[key], key)
    if meta["status"] in ("working", "completed"):
        nonempty(meta["owner"], "owner")
        nonempty(meta["claimed_at"], "claimed_at")
    if meta["status"] == "completed":
        nonempty(meta["reviewer"], "reviewer")
        nonempty(meta["review_scope"], "review_scope")
        if meta["reviewer"] == meta["owner"]:
            raise TrackerError("Review identity must differ from owner")


def read_record(path):
    if path.is_symlink():
        raise TrackerError(f"Issue records must not be symlinks: {path}")
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise TrackerError(f"Missing frontmatter: {path}")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise TrackerError(f"Unterminated frontmatter: {path}")
    meta = {}
    for line in lines[1:end]:
        key, sep, value = line.partition(":")
        if not sep or key in meta or key not in FIELDS:
            raise TrackerError(f"Invalid metadata line in {path}: {key}")
        try:
            meta[key] = json.loads(value.strip())
        except json.JSONDecodeError as exc:
            raise TrackerError(f"Metadata values must use JSON syntax: {path}") from exc
    validate(meta, path)
    return meta, "".join(lines[end + 1:]).lstrip("\n")


def render(meta, body):
    front = "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in meta.items())
    return f"---\n{front}\n---\n\n{body.rstrip()}\n"


@contextmanager
def locked(lock):
    if fcntl is None:
        raise TrackerError(
            "Tracker mutations require POSIX file locking; "
            "run under WSL or another POSIX environment"
        )
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open("a", encoding="utf-8") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def write_record(path, meta, body):
    validate(meta, path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=".specs-", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(render(meta, body))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def from_file(filename, label):
    return nonempty(Path(filename).read_text(encoding="utf-8"), label)


def expect_revision(meta, expected):
    if meta["revision"] != expected:
        raise TrackerError(f"Revision conflict: expected {expected}, current {meta['revision']}; reread")


def expect_owner(meta, owner):
    if meta["status"] != "working" or meta["owner"] != owner:
        raise TrackerError(f"Not owned by this run: status={meta['status']}, owner={meta['owner']}")


def clear_claim(meta):
    for key in ("owner", "claimed_at", "reviewer", "review_scope"):
        meta[key] = None


def output(meta, path):
    print(json.dumps({**meta, "path": str(path)}, ensure_ascii=False))


def scan(root):
    """One content-derived generation for the exact records read, no index writes."""
    digest = hashlib.sha256()
    records = []
    for path in sorted((root / "issues").glob("SPEC-*.md")):
        meta, body = read_record(path)
        digest.update(path.name.encode("utf-8") + b"\0")
        digest.update(render(meta, body).encode("utf-8") + b"\0")
        records.append((path, meta, body))
    return digest.hexdigest(), records


def execute(args):
    project, root, lock = locate(args.repo)
    if args.command == "root":
        print(json.dumps({"project_root": str(project), "tracking_root": str(root), "lock_path": str(lock)}))
        return
    if args.command == "list":
        rows = []
        terms = args.query.casefold().split()
        snapshot, records = scan(root)
        for path, meta, body in records:
            haystack = (meta["title"] + "\n" + body).casefold()
            if (not args.status or meta["status"] in args.status) and all(t in haystack for t in terms):
                rows.append({**meta, "path": str(path)})
        rows.sort(key=lambda row: (row["priority"], row["created_at"], row["id"]))
        payload = {"snapshot": snapshot, "issues": rows} if args.snapshot else rows
        print(json.dumps(payload, ensure_ascii=False))
        return
    if args.command == "show":
        path = issue_path(root, args.id)
        meta, body = read_record(path)
        print(render(meta, body), end="")
        return
    # Every read/modify/write transaction is protected by the shared local lock.
    with locked(lock):
        if args.command == "create":
            snapshot, _ = scan(root)
            if snapshot != args.expected_snapshot:
                raise TrackerError("Tracker changed since duplicate search; reread and reconcile before creating")
            body = from_file(args.body_file, "body")
            reject_home_paths(body, "body")
            while True:
                issue_id = "SPEC-" + uuid.uuid4().hex[:8].upper()
                path = issue_path(root, issue_id)
                if not path.exists():
                    break
            timestamp = now()
            meta = dict(
                schema=1, id=issue_id, title=hygienic(args.title, "title"), kind=args.kind,
                status=args.status, priority=args.priority, revision=1,
                created_at=timestamp, updated_at=timestamp,
                owner=None, claimed_at=None, reviewer=None, review_scope=None,
            )
        else:
            path = issue_path(root, args.id)
            meta, body = read_record(path)
            if hasattr(args, "expected_revision"):
                expect_revision(meta, args.expected_revision)
            if args.command == "claim":
                if meta["status"] != "open":
                    raise TrackerError(f"Task is not open: {meta['status']}, owner={meta['owner']}")
                meta.update(status="working", owner=hygienic(args.owner, "owner"), claimed_at=now())
            elif args.command == "update":
                if meta["status"] == "working":
                    expect_owner(meta, args.owner)
                    if args.status is not None:
                        raise TrackerError("Use release or complete to exit working")
                elif args.owner is not None:
                    raise TrackerError("Owner tokens only apply to working records")
                if not any(v is not None for v in (args.title, args.priority, args.status, args.body_file)):
                    raise TrackerError("No update supplied")
                if args.status is not None:
                    # Reopening retains report history in the body, resets attestations.
                    meta["status"] = args.status
                    clear_claim(meta)
                if args.title is not None:
                    meta["title"] = hygienic(args.title, "title")
                if args.priority is not None:
                    meta["priority"] = args.priority
                if args.body_file:
                    body = from_file(args.body_file, "body")
                    reject_home_paths(body, "body")
            elif args.command == "release":
                expect_owner(meta, args.owner)
                note = from_file(args.note_file, "handoff note")
                reject_home_paths(note, "handoff note")
                body += f"\n## Handoff ({now()})\n\n{note}\n"
                meta["status"] = args.status
                clear_claim(meta)
            elif args.command == "complete":
                expect_owner(meta, args.owner)
                reviewer = hygienic(args.reviewer, "reviewer")
                if reviewer == meta["owner"]:
                    raise TrackerError("Independent review identity must differ from owner")
                report = from_file(args.review_file, "review report")
                reject_home_paths(report, "review report")
                if report.splitlines()[0].strip() != "Verdict: pass" or "No actionable findings." not in report:
                    raise TrackerError("Completion requires a passing review report with no actionable findings")
                meta.update(status="completed", reviewer=reviewer,
                            review_scope=hygienic(args.scope, "review scope"))
                body += f"\n## Independent review ({now()})\n\n{report}\n"
            meta["revision"] += 1
            meta["updated_at"] = now()
        write_record(path, meta, body)
        output(meta, path)


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--repo", required=True, help="Project directory; linked worktrees share primary tracker")
    commands = cli.add_subparsers(dest="command", required=True)
    commands.add_parser("root", help="Locate tracker without creating files")
    listing = commands.add_parser("list", help="List metadata without creating files")
    listing.add_argument("--status", action="append", choices=STATES)
    listing.add_argument("--query", default="", help="Case-insensitive AND search of title/body")
    listing.add_argument("--snapshot", action="store_true", help="Include freshness token for compare-and-create")
    show = commands.add_parser("show")
    show.add_argument("id")
    create = commands.add_parser("create")
    create.add_argument("--title", required=True)
    create.add_argument("--kind", required=True, choices=KINDS)
    create.add_argument("--priority", choices=PRIORITIES, default="P2")
    create.add_argument("--status", choices=("open", "needs-info"), default="open")
    create.add_argument("--body-file", required=True)
    create.add_argument("--expected-snapshot", required=True, help="Token from final list --snapshot duplicate search")
    update = commands.add_parser("update")
    update.add_argument("id")
    update.add_argument("--expected-revision", type=int, required=True)
    update.add_argument("--owner")
    update.add_argument("--title")
    update.add_argument("--priority", choices=PRIORITIES)
    update.add_argument("--status", choices=("open", "needs-info", "blocked", "closed"))
    update.add_argument("--body-file")
    claim = commands.add_parser("claim")
    claim.add_argument("id")
    claim.add_argument("--expected-revision", type=int, required=True)
    claim.add_argument("--owner", required=True)
    release = commands.add_parser("release")
    release.add_argument("id")
    release.add_argument("--owner", required=True)
    release.add_argument("--status", choices=("open", "blocked"), required=True)
    release.add_argument("--note-file", required=True)
    complete = commands.add_parser("complete")
    complete.add_argument("id")
    complete.add_argument("--expected-revision", type=int, required=True)
    complete.add_argument("--owner", required=True)
    complete.add_argument("--reviewer", required=True)
    complete.add_argument("--scope", required=True)
    complete.add_argument("--review-file", required=True)
    return cli


def main():
    try:
        execute(parser().parse_args())
    except (TrackerError, OSError, UnicodeError) as exc:
        print(f"specs: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
