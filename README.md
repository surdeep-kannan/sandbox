# Sandbox

A small toolbox of developer utilities for everyday repository work. Pure Python
standard library, no runtime dependencies.

## Installation

```console
pip install -e .
```

Or run it without installing:

```console
PYTHONPATH=src python -m sandbox --help
```

## Commands

### `sandbox stats [path]`

Counts files and lines in a directory tree, grouped by extension. Common build
and cache directories such as `.git`, `__pycache__`, `node_modules` and `.venv`
are skipped automatically.

```console
$ sandbox stats .
Files: 12
Lines: 430

By extension:
  .py     8 files    340 lines
  .md     2 files     72 lines
  .toml   1 file      18 lines
```

### `sandbox todos [path]`

Scans for `TODO`, `FIXME`, `HACK` and `XXX` markers and prints them as
`path:line: TAG message`.

```console
$ sandbox todos ~/projects/api
src/api/routes.py:42: TODO add pagination
scripts/deploy.sh:11: FIXME handle missing env vars
```

### `sandbox git-clean [--apply]`

Lists local branches that are already merged into the default branch. Without
`--apply` it only reports; with `--apply` it deletes them with `git branch -d`,
so unmerged work is never lost.

```console
$ sandbox git-clean
remove feature/old-idea (already merged into main)
run again with --apply to delete them

$ sandbox git-clean --apply
deleted feature/old-idea
```

## Tests

```console
PYTHONPATH=src python -m unittest discover -s tests -v
```
