# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

goodspirits is a Claude Code plugin marketplace. Its one plugin, `adoption-profile-writing`, writes shelter adoption profiles. The only code is two standard-library Python scripts, the draft checker `plugins/adoption-profile-writing/skills/adoption-profile-writing/scripts/check_draft.py` and the eval recorder `plugins/adoption-profile-writing/evals/record_eval.py`, plus Markdown skill files and the eval suite under `plugins/adoption-profile-writing/evals/`.

## Commands

| Command | Runs |
|---|---|
| `make setup` | Nothing: the repo has no dependencies and no lockfile, so it only prints a note |
| `make test` | `python3 -m unittest discover -s tests` |
| `make lint` | `uvx ruff@0.17.5 check plugins tests` |
| `make format` | `uvx ruff@0.17.5 format plugins tests` |
| `make check` | `make test`, then `make lint` |
| `make verify` | `make check`, then `claude plugin validate` on the marketplace and on the plugin |
| `make eval` | `claude plugin eval` on the working-tree plugin with `--judge-model $(JUDGE_MODEL)` (default `claude-sonnet-5-5`), `--threshold 0`, `--no-publish`, `--scaffold`, `--trust-plugin`, and `--allow-tools Write` |
| `make eval-record` | `evals/record_eval.py`: writes the newest run's summary to `evals/history/<run-start>_<hash>.json`, refusing when the plugin has uncommitted changes or a commit newer than the run |

`make eval` makes paid model calls (about $9 for the four cases at three runs each) and cannot start its agents inside the Claude sandbox, so run it as `! make eval`. It stays out of `check`, `verify`, and CI. Its raw output under `evals/results/` is gitignored; commit only the summary `make eval-record` writes. Override the judge with `make eval JUDGE_MODEL=<model>`, and compare scores only between runs with the same judge.

`format` is kept out of `check` on purpose, so the curated phrase lists in `check_draft.py` stay dense.

CI runs `make setup` and `make check` on pushes to `main` and on pull requests. It has no `verify` job, because the runner lacks the `claude` CLI that `claude plugin validate` needs; run `make verify` locally before shipping.

Healthy `make check` output:

```
python3 -m unittest discover -s tests
...
----------------------------------------------------------------------
Ran N tests in N.NNNs

OK
uvx ruff@0.17.5 check plugins tests
All checks passed!
```

## Issue tracker

GitHub Issues on `origin` (`ckrough/goodspirits`). The repository is user-owned and cannot set native issue types, so each issue carries a type label (`bug`, `feature`, or `task`) and a priority label (`p0` through `p4`).
