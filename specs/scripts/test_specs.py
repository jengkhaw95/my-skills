"""Integration tests for tracker ownership and storage invariants; all data is temporary."""

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("specs.py")


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="specs-tests-")
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / "project"
        self.repo.mkdir()
        self.body = self.base / "body.md"
        self.body.write_text("# Address bug\n\nValid Unicode address fails.\n\n---\n\nAcceptance: accepts 北京.\n")
        self.note = self.base / "note.md"
        self.note.write_text("Waiting for test credentials; no worker is running.\n")
        self.report = self.base / "review.md"
        self.report.write_text("Verdict: pass\nScope: current candidate\nNo actionable findings.\nChecks: passed\nGaps: none.\n")

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, repo=None, ok=True):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(repo or self.repo), *args],
            capture_output=True, text=True,
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def create(self, **kwargs):
        snapshot = json.loads(self.run_cli("list", "--snapshot", **kwargs).stdout)["snapshot"]
        return json.loads(self.run_cli(
            "create", "--title", 'Address: "Unicode" handling', "--kind", "bug",
            "--body-file", str(self.body), "--expected-snapshot", snapshot, **kwargs,
        ).stdout)

    def show(self, issue_id, **kwargs):
        return self.run_cli("show", issue_id, **kwargs).stdout

    def claim(self, issue, owner="worker"):
        return json.loads(self.run_cli(
            "claim", issue["id"], "--expected-revision", str(issue["revision"]),
            "--owner", owner,
        ).stdout)

    def test_read_only_commands_do_not_initialize(self):
        root = json.loads(self.run_cli("root").stdout)
        self.assertEqual(root["project_root"], str(self.repo))
        self.assertEqual(json.loads(self.run_cli("list").stdout), [])
        self.run_cli("show", "SPEC-00000000", ok=False)
        self.assertEqual(list(self.repo.iterdir()), [])

    def test_roundtrip_and_filtered_search(self):
        issue = self.create()
        raw = self.show(issue["id"])
        self.assertIn("北京", raw)
        self.assertIn("title: " + json.dumps(issue["title"]), raw)
        self.assertEqual(raw.count("\n---\n"), 2)
        matches = json.loads(self.run_cli("list", "--query", "UNICODE 北京", "--status", "open").stdout)
        self.assertEqual([x["id"] for x in matches], [issue["id"]])
        self.assertEqual(json.loads(self.run_cli("list", "--query", "unrelated").stdout), [])

    def test_revision_conflict_preserves_record(self):
        issue = self.create()
        before = self.show(issue["id"])
        self.run_cli("update", issue["id"], "--expected-revision", "2", "--title", "overwrite", ok=False)
        self.assertEqual(before, self.show(issue["id"]))

    def test_concurrent_claim_has_one_winner(self):
        issue = self.create()

        def attempt(number):
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--repo", str(self.repo), "claim", issue["id"],
                 "--expected-revision", "1", "--owner", f"worker-{number}"],
                capture_output=True, text=True,
            )

        with ThreadPoolExecutor(max_workers=12) as pool:
            results = list(pool.map(attempt, range(12)))
        self.assertEqual(sum(r.returncode == 0 for r in results), 1)
        winning = next(json.loads(r.stdout) for r in results if r.returncode == 0)
        self.assertEqual(winning["revision"], 2)
        self.assertEqual(winning["status"], "working")

    def test_concurrent_intake_requires_reconciliation(self):
        snapshot = json.loads(self.run_cli("list", "--snapshot", "--query", "address").stdout)["snapshot"]

        def attempt(number):
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--repo", str(self.repo), "create",
                 "--title", "Same address bug", "--kind", "bug", "--body-file", str(self.body),
                 "--expected-snapshot", snapshot], capture_output=True, text=True,
            )

        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(attempt, range(8)))
        self.assertEqual(sum(r.returncode == 0 for r in results), 1)
        self.assertTrue(all("reread and reconcile" in r.stderr for r in results if r.returncode))
        self.assertEqual(len(json.loads(self.run_cli("list").stdout)), 1)

    def test_claim_ownership_update_and_release(self):
        issue = self.claim(self.create())
        before = self.show(issue["id"])
        for command in (
            ("update", "--expected-revision", "2", "--title", "bad"),
            ("update", "--expected-revision", "2", "--owner", "imposter", "--title", "bad"),
            ("update", "--expected-revision", "2", "--owner", "worker", "--status", "open"),
            ("release", "--owner", "imposter", "--status", "open", "--note-file", str(self.note)),
        ):
            self.run_cli(command[0], issue["id"], *command[1:], ok=False)
            self.assertEqual(before, self.show(issue["id"]))
        edited = json.loads(self.run_cli(
            "update", issue["id"], "--expected-revision", "2", "--owner", "worker",
            "--body-file", str(self.body),
        ).stdout)
        self.assertEqual(edited["revision"], 3)
        released = json.loads(self.run_cli(
            "release", issue["id"], "--owner", "worker", "--status", "blocked",
            "--note-file", str(self.note),
        ).stdout)
        self.assertEqual(released["status"], "blocked")
        self.assertIsNone(released["owner"])
        self.assertIn("Waiting for test credentials", self.show(issue["id"]))

    def test_completion_requires_owner_revision_and_passing_report(self):
        issue = self.claim(self.create())
        before = self.show(issue["id"])

        def complete(owner="worker", reviewer="review-agent", revision="2", ok=True):
            return self.run_cli(
                "complete", issue["id"], "--owner", owner, "--reviewer", reviewer,
                "--expected-revision", revision, "--scope", "isolated checkout: candidate A",
                "--review-file", str(self.report), ok=ok,
            )

        complete(owner="other", ok=False)
        complete(reviewer="worker", ok=False)
        complete(revision="1", ok=False)
        self.report.write_text("Verdict: incomplete\nNo actionable findings.\nBrowser unavailable.\n")
        complete(ok=False)
        self.assertEqual(before, self.show(issue["id"]))
        self.report.write_text("Verdict: pass\nNo actionable findings.\nChecks: passed\n")
        finished = json.loads(complete().stdout)
        self.assertEqual(finished["status"], "completed")
        self.assertEqual(finished["reviewer"], "review-agent")
        reopened = json.loads(self.run_cli(
            "update", issue["id"], "--expected-revision", "3", "--status", "open",
        ).stdout)
        self.assertIsNone(reopened["reviewer"])
        self.assertIsNone(reopened["owner"])
        self.assertIn("No actionable findings.", self.show(issue["id"]))

    def test_unresolved_and_closed_cannot_be_claimed(self):
        snapshot = json.loads(self.run_cli("list", "--snapshot").stdout)["snapshot"]
        issue = json.loads(self.run_cli(
            "create", "--title", "Unresolved", "--kind", "feature", "--status", "needs-info",
            "--body-file", str(self.body), "--expected-snapshot", snapshot,
        ).stdout)
        self.run_cli("claim", issue["id"], "--expected-revision", "1", "--owner", "worker", ok=False)
        self.run_cli("update", issue["id"], "--expected-revision", "1", "--status", "closed")
        self.run_cli("claim", issue["id"], "--expected-revision", "2", "--owner", "worker", ok=False)

    def test_invalid_id_and_corrupt_metadata_are_not_repaired(self):
        self.run_cli("show", "../../escape", ok=False)
        issue = self.create()
        path = Path(issue["path"])
        broken = path.read_text().replace('status: "open"', "status: open")
        path.write_text(broken)
        self.run_cli("list", ok=False)
        self.run_cli("claim", issue["id"], "--expected-revision", "1", "--owner", "worker", ok=False)
        self.assertEqual(path.read_text(), broken)

    def test_linked_git_worktrees_share_records_and_claims(self):
        def git(*args):
            return subprocess.run(
                ["git", "-C", str(self.repo), *args], capture_output=True, text=True, check=True,
                env={**os.environ, "GIT_CONFIG_NOSYSTEM": "1"},
            )

        git("init", "-q")
        git("-c", "user.name=Tracker Test", "-c", "user.email=test@example.invalid",
            "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
            "commit", "--allow-empty", "-qm", "baseline")
        linked = self.base / "linked checkout 北京"
        git("-c", "core.hooksPath=/dev/null", "worktree", "add", "--detach", str(linked), "HEAD")
        primary_root = json.loads(self.run_cli("root").stdout)
        linked_root = json.loads(self.run_cli("root", repo=linked).stdout)
        self.assertEqual(primary_root, linked_root)
        issue = self.create(repo=linked)
        self.assertTrue(Path(issue["path"]).is_relative_to(self.repo))
        self.assertFalse((linked / ".specs").exists())
        self.assertIn(issue["id"], self.show(issue["id"]))
        self.claim(issue)
        self.run_cli("claim", issue["id"], "--expected-revision", "1", "--owner", "other", repo=linked, ok=False)


if __name__ == "__main__":
    unittest.main()
