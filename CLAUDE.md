# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

goodspirits is a Claude plugin marketplace for animal-rescue volunteers and staff. Its one plugin, `adoption-profile-writing`, writes shelter adoption profiles. The only code is two standard-library Python scripts, the draft checker `plugins/adoption-profile-writing/skills/adoption-profile-writing/scripts/check_draft.py` and the eval recorder `plugins/adoption-profile-writing/evals/record_eval.py`, plus Markdown skill files and the eval suite under `plugins/adoption-profile-writing/evals/`.

## Installing for a user

The people who use this plugin are shelter volunteers working in the Claude desktop app. If the person asked you to install goodspirits, follow the "For the agent doing the install" section of `README.md`: walk them through Customize > Plugins > Add > Add marketplace, `ckrough/goodspirits`, then Add on Adoption Profile Writing, one step at a time in plain words.

In a Claude Code session, ask them to type `/plugin marketplace add ckrough/goodspirits`, then `/plugin install adoption-profile-writing@goodspirits`, then `/reload-plugins`. These three commands copy the ones in README.md's "For the agent doing the install" section; update both together.

Do not run `make` targets or edit files in this repository to install. The sections below are for maintainers.

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
| `make eval-record` | `evals/record_eval.py`: writes a summary of each model's run in the newest sweep, with the model and judge, to `evals/history/<run-start>_<hash>_<model>.json`, refusing when the plugin has uncommitted changes, or when the sweep ran at another commit, started with uncommitted plugin changes, or did not finish (`make eval` stamps each sweep with its commit and marks it complete) |

`make eval` makes paid model calls (the five cases three times with and three times without the skill, 30 runs, about 45 minutes; the Opus judge costs more than the $5 the Sonnet judge did) and cannot start its agents inside the Claude sandbox, so run it as `! make eval`. It stays out of `check`, `verify`, and CI. Its raw output under `evals/results/` is gitignored; commit only the summaries `make eval-record` writes. The writer is the model the skill pins in its frontmatter; `make eval` refuses any other in `MODELS`, because the pin takes over once the skill fires and the with- and without-skill arms would run on different models. Change the judge with `JUDGE_MODEL=<model>`. Compare scores only between runs with the same writer model and judge, and with no change to the graders between their commits.

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

## Plugin enablement

This section is for maintainers with access to the private `backchainai/daedalus` repository. Other contributors skip it; the tracked `permissions.deny` in `.claude/settings.json` still applies to them.

daedalus and its dependencies are enabled per clone in the gitignored `.claude/settings.local.json`, not in the tracked `.claude/settings.json`, because the `backchain` marketplace is private and this repository is public. The file holds:

```json
{
  "enabledPlugins": {
    "daedalus@backchain": true,
    "github@claude-plugins-official": true,
    "astral@astral-sh": true
  },
  "extraKnownMarketplaces": {
    "backchain": { "source": { "source": "github", "repo": "backchainai/daedalus" } },
    "claude-plugins-official": { "source": { "source": "github", "repo": "anthropics/claude-plugins-official" } },
    "astral-sh": { "source": { "source": "github", "repo": "astral-sh/claude-code-plugins" } }
  }
}
```

This departs from daedalus's documented setup on purpose. A `/daedalus:setup` rerun merges `enabledPlugins` and `extraKnownMarketplaces` into `.claude/settings.json`; keep both keys out of that file.

`.worktreeinclude` copies `.claude/settings.local.json` into worktrees made by `claude --worktree` or EnterWorktree. A worktree made with `git worktree add` needs the file copied in by hand.

To disable daedalus, set `daedalus@backchain` to `false` or remove it in `.claude/settings.local.json`, in each checkout and worktree. Editing `.claude/settings.json` does nothing.
