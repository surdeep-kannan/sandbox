import subprocess


def _git(repo, *args):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or "git command failed"
        raise RuntimeError(message)
    return result.stdout


def default_branch(repo="."):
    try:
        output = _git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    except RuntimeError:
        return "main"
    return output.strip().rsplit("/", 1)[-1]


def merged_branches(repo=".", base=None):
    base = base or default_branch(repo)
    output = _git(repo, "branch", "--merged", base, "--format=%(refname:short)")
    protected = {base, "main", "master", "HEAD"}
    branches = []
    for name in output.splitlines():
        name = name.strip()
        if name and name not in protected:
            branches.append(name)
    return branches


def delete_branch(repo, branch):
    _git(repo, "branch", "-d", branch)
