import tempfile
import unittest
from pathlib import Path

from sandbox.stats import format_report, gather_stats


class StatsTests(unittest.TestCase):
    def make_tree(self, root):
        (root / "a.py").write_text("x = 1\ny = 2\n", encoding="utf-8")
        (root / "b.md").write_text("hello\n", encoding="utf-8")
        cache = root / "__pycache__"
        cache.mkdir()
        (cache / "junk.pyc").write_text("junk\n", encoding="utf-8")
        git_dir = root / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("ignored\n", encoding="utf-8")

    def test_counts_files_and_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_tree(root)

            stats = gather_stats(root)

            self.assertEqual(stats["files"], 2)
            self.assertEqual(stats["lines"], 3)
            self.assertEqual(stats["by_extension"][".py"], [1, 2])
            self.assertEqual(stats["by_extension"][".md"], [1, 1])

    def test_report_contains_totals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_tree(root)

            report = format_report(gather_stats(root))

            self.assertIn("Files: 2", report)
            self.assertIn("Lines: 3", report)
            self.assertIn(".py", report)


if __name__ == "__main__":
    unittest.main()
