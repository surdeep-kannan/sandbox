import subprocess
import tempfile
import unittest
from pathlib import Path

from sandbox.gitutils import merged_branches


def run(repo, *args):
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )


class GitUtilsTests(unittest.TestCase):
    def test_merged_branches_excludes_base_and_unmerged(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            run(repo, "init", "-b", "main")
            run(repo, "config", "user.email", "tests@example.com")
            run(repo, "config", "user.name", "Tests")
            (repo / "file.txt").write_text("one\n", encoding="utf-8")
            run(repo, "add", "file.txt")
            run(repo, "commit", "-m", "initial")

            run(repo, "checkout", "-b", "feature/done")
            (repo / "file.txt").write_text("one\ntwo\n", encoding="utf-8")
            run(repo, "commit", "-am", "feature work")
            run(repo, "checkout", "main")
            run(repo, "merge", "--no-ff", "feature/done", "-m", "merge feature")

            run(repo, "checkout", "-b", "feature/wip")
            (repo / "other.txt").write_text("wip\n", encoding="utf-8")
            run(repo, "add", "other.txt")
            run(repo, "commit", "-m", "work in progress")
            run(repo, "checkout", "main")

            branches = merged_branches(repo, base="main")

            self.assertIn("feature/done", branches)
            self.assertNotIn("feature/wip", branches)
            self.assertNotIn("main", branches)


if __name__ == "__main__":
    unittest.main()
