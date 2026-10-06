import argparse

from . import __version__
from .gitutils import delete_branch, merged_branches
from .stats import format_report, gather_stats
from .todos import find_todos


def build_parser():
    parser = argparse.ArgumentParser(
        prog="sandbox",
        description="Small developer utilities for everyday repository work.",
    )
    parser.add_argument("--version", action="version", version=f"sandbox {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    stats = commands.add_parser("stats", help="count files and lines by extension")
    stats.add_argument("path", nargs="?", default=".")
    stats.set_defaults(func=cmd_stats)

    todos = commands.add_parser("todos", help="list TODO/FIXME markers in a tree")
    todos.add_argument("path", nargs="?", default=".")
    todos.set_defaults(func=cmd_todos)

    clean = commands.add_parser("git-clean", help="list or delete already merged local branches")
    clean.add_argument("--repo", default=".")
    clean.add_argument("--apply", action="store_true", help="delete the listed branches")
    clean.set_defaults(func=cmd_git_clean)

    return parser


def cmd_stats(args):
    print(format_report(gather_stats(args.path)))


def cmd_todos(args):
    for path, number, tag, message in find_todos(args.path):
        suffix = f" {message}" if message else ""
        print(f"{path}:{number}: {tag}{suffix}")


def cmd_git_clean(args):
    branches = merged_branches(args.repo)
    if not branches:
        print("no merged branches to clean")
        return
    for branch in branches:
        if args.apply:
            delete_branch(args.repo, branch)
            print(f"deleted {branch}")
        else:
            print(f"remove {branch} (already merged)")
    if not args.apply:
        print("run again with --apply to delete them")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
