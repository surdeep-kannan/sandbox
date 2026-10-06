# Notes

Quick reference for commands and snippets used while experimenting in this repo.

## Git

- Undo last commit, keep changes staged: `git reset --soft HEAD~1`
- List branches sorted by last commit: `git branch --sort=-committerdate`
- Show remotes with URLs: `git remote -v`

## GitHub CLI

- Create a PR: `gh pr create --fill`
- View CI status: `gh pr checks`
- List open issues: `gh issue list`
