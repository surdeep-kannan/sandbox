import tempfile
import unittest
from pathlib import Path

from sandbox.todos import find_todos


class TodoTests(unittest.TestCase):
    def test_finds_markers_with_locations(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            todo = "TO" + "DO"
            fixme = "FIX" + "ME"
            (root / "app.py").write_text(
                f"# {todo} clean this up\nprint('ok')\n# {fixme} later\n",
                encoding="utf-8",
            )

            hits = find_todos(root)

            self.assertEqual(
                hits,
                [
                    ("app.py", 1, "TODO", "clean this up"),
                    ("app.py", 3, "FIXME", "later"),
                ],
            )

    def test_ignores_words_inside_other_words(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "notes.md").write_text("TODOLIST is not a marker\n", encoding="utf-8")

            self.assertEqual(find_todos(root), [])


if __name__ == "__main__":
    unittest.main()
