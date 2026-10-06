import re
from pathlib import Path

from .common import iter_files

MARKER = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b[:\s]*(.*)")


def find_todos(root):
    root = Path(root)
    hits = []
    for path in iter_files(root):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, start=1):
            match = MARKER.search(line)
            if match:
                location = path.relative_to(root)
                hits.append((str(location), number, match.group(1), match.group(2).strip()))
    return hits
