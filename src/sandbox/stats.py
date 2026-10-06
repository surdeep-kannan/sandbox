from .common import iter_files


def _read_lines(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        return handle.read().splitlines()


def gather_stats(root):
    files = 0
    lines = 0
    by_extension = {}
    for path in iter_files(root):
        try:
            content_lines = _read_lines(path)
        except OSError:
            continue
        files += 1
        lines += len(content_lines)
        extension = path.suffix.lower() or "(none)"
        entry = by_extension.setdefault(extension, [0, 0])
        entry[0] += 1
        entry[1] += len(content_lines)
    return {"files": files, "lines": lines, "by_extension": by_extension}


def format_report(stats):
    rows = sorted(stats["by_extension"].items(), key=lambda item: (-item[1][1], item[0]))
    width = max((len(extension) for extension, _ in rows), default=0)
    output = [f"Files: {stats['files']}", f"Lines: {stats['lines']}", "", "By extension:"]
    for extension, (count, line_count) in rows:
        output.append(f"  {extension:<{width}}  {count:>3} files  {line_count:>6} lines")
    return "\n".join(output)
