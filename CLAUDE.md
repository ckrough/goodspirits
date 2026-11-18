# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

goodspirits is a Claude Code plugin marketplace. Its one plugin, `adoption-profile-writing`, writes shelter adoption profiles. The only code is `plugins/adoption-profile-writing/skills/adoption-profile-writing/scripts/check_draft.py`, a standard-library Python checker, plus Markdown skill files.

## Commands

| Command | Runs |
|---|---|
| `make setup` | Nothing: the repo has no dependencies and no lockfile, so it only prints a note |
| `make test` | `python3 -m unittest discover -s tests` |
| `make lint` | `uvx ruff@0.17.5 check plugins tests` |
| `make format` | `uvx ruff@0.17.5 format plugins tests` |
| `make check` | `make test`, then `make lint` |
| `make verify` | `make check`, then `claude plugin validate` on the marketplace and on the plugin |

`format` is kept out of `check` on purpose, so the curated phrase lists in `check_draft.py` stay dense.

CI runs `make setup` and `make check` on pushes to `main` and on pull requests. It has no `verify` job, because the runner lacks the `claude` CLI that `claude plugin validate` needs; run `make verify` locally before shipping.

Healthy `make check` output:

```
python3 -m unittest discover -s tests
...
Ran N tests in N.NNNs

OK
uvx ruff@0.17.5 check plugins tests
All checks passed!
```

## Issue tracker

GitHub Issues on `origin` (`ckrough/goodspirits`). The repository is user-owned and cannot set native issue types, so each issue carries a type label (`bug`, `feature`, or `task`) and a priority label (`p0` through `p4`).
