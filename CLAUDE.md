# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

goodspirits is a Claude plugin marketplace for animal-rescue volunteers and staff. Its one plugin, `adoption-profile-writing`, writes shelter adoption profiles. The only code is `plugins/adoption-profile-writing/skills/adoption-profile-writing/scripts/check_draft.py`, a standard-library Python checker, plus Markdown skill files.

## Installing for a user

The people who use this plugin are shelter volunteers working in the Claude desktop app. If the person asked you to install goodspirits, follow the "For the agent doing the install" section of `README.md`: walk them through Customize > Plugins > Add > Add marketplace, `ckrough/goodspirits`, then Add on Adoption Profile Writing, one step at a time in plain words.

In a Claude Code session, run `claude plugin install adoption-profile-writing --marketplace ckrough/goodspirits` and ask them to type `/reload-plugins`. This copies `README.md`; update both together.

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
