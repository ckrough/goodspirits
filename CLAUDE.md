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
| `make eval` | One sweep: `claude plugin eval` on the working-tree plugin once per writer model in `$(MODELS)` (default `claude-sonnet-5-5`, the model the skill pins), each with `--model`, `--judge-model $(JUDGE_MODEL)` (default `claude-opus-5-5`, a stronger model than the writer), `--threshold 0`, `--no-publish`, `--scaffold`, `--trust-plugin`, `--allow-tools Write`, and `--output-dir evals/results/<sweep>/<model>/` |
| `make eval-record` | `evals/record_eval.py`: writes a summary of each model's run in the newest sweep, with the model and judge, to `evals/history/<run-start>_<hash>_<model>.json`, refusing when the plugin has uncommitted changes or a commit newer than a run |

`make eval` makes paid model calls (the five cases three times with and three times without the skill, 30 runs, about 45 minutes; the Opus judge costs more than the $5 the Sonnet judge did) and cannot start its agents inside the Claude sandbox, so run it as `! make eval`. It stays out of `check`, `verify`, and CI. Its raw output under `evals/results/` is gitignored; commit only the summaries `make eval-record` writes. Compare other writers with `make eval MODELS="<model> ..."` and change the judge with `JUDGE_MODEL=<model>`. Compare scores only between runs with the same writer model and judge, and with no change to the graders between their commits.

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
