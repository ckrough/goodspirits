---
title: Move daedalus enablement to local settings
issue: 11
type: Task
date: 2026-11-20
---

# Move daedalus enablement to local settings

## Context

This implements the acceptance criteria of #11. goodspirits is public, but its tracked `.claude/settings.json` enables `daedalus@backchain` and declares the `backchain` marketplace, which lives in the private `backchainai/daedalus`. A cloner gets settings that point at a plugin they cannot install. #6 put the enablement there. This change moves it to the gitignored `.claude/settings.local.json` and keeps the `permissions.deny` list tracked, since that list protects every contributor.

`.gitignore` already ignores `.claude/settings.local.json`, because `.claude/*` is ignored and only `!.claude/settings.json` is re-included, so no ignore change is needed. A tracked `.worktreeinclude` listing `.claude/settings.local.json` makes `claude --worktree` and EnterWorktree copy the file into each new worktree, as daedalus's own repository does. A worktree made with plain `git worktree add` still needs a manual copy, and CLAUDE.md says so.

This departs from daedalus's documented setup: its `docs/sdlc.md` names the tracked `.claude/settings.json` as where daedalus is switched on, and `/daedalus:setup` merges `enabledPlugins` and `extraKnownMarketplaces` back into that file. CLAUDE.md records the departure so that a `/daedalus:setup` rerun keeps both keys out of the tracked file.

The main checkout's `.claude/settings.local.json` today enables `astral`, `context7`, and `github` and declares no marketplaces. The worktree has no local settings file. Both files are untracked, so their edits appear in no commit, and Verification checks them directly. The main-checkout file cannot be written from this worktree: the daedalus gate refuses edits on `main`, and the sandbox blocks the path. The operator edits it. `.claude/settings.json` and `CLAUDE.md` are daedalus harness paths, so their edits ask the operator.

## Files

- `.claude/settings.json`
- `.worktreeinclude`
- `CLAUDE.md`
- `.claude/settings.local.json`

## Work order

1. Write the local settings, strip the tracked ones, run the headless load check, and commit when `make check` exits 0.
   - Write the worktree's `.claude/settings.local.json`. Its `enabledPlugins` sets `true` for `daedalus@backchain`, `github@claude-plugins-official`, and `astral@astral-sh`. Its `extraKnownMarketplaces` declares three `github` sources: `backchain` (`backchainai/daedalus`), `claude-plugins-official` (`anthropics/claude-plugins-official`), and `astral-sh` (`astral-sh/claude-code-plugins`).
   - Delete the `enabledPlugins` and `extraKnownMarketplaces` blocks from `.claude/settings.json`, leaving `permissions.deny` unchanged.
   - Add `.worktreeinclude` with a one-line comment and the line `.claude/settings.local.json`.
   - Add a `## Plugin enablement` section to `CLAUDE.md`. It covers:
     - The section is for maintainers with access to `backchainai/daedalus`. Other contributors skip it, and the tracked `permissions.deny` still applies to them.
     - daedalus and its dependencies are enabled per clone in the gitignored `.claude/settings.local.json`, because the `backchain` marketplace is private and the repository is public. The section gives the file's JSON.
     - This departs from daedalus's documented setup on purpose: a `/daedalus:setup` rerun must keep `enabledPlugins` and `extraKnownMarketplaces` out of `.claude/settings.json`.
     - `.worktreeinclude` copies the file into worktrees made by `claude --worktree` or EnterWorktree. A worktree made with `git worktree add` needs the file copied in by hand.
     - To disable daedalus, set `daedalus@backchain` to `false` or remove it in `.claude/settings.local.json`, in each checkout and worktree. Editing `.claude/settings.json` does nothing.
   - Run the headless check from Verification, after the strip and before the commit.
   - Commit `.claude/settings.json`, `.worktreeinclude`, and `CLAUDE.md`.
2. The operator edits the main checkout's `.claude/settings.local.json` (`file:///Users/ckrough/Code/goodspirits/.claude/settings.local.json`). In the hand-off, I give them the keys to add, which are `daedalus@backchain` under `enabledPlugins` and the three `extraKnownMarketplaces` entries, plus the `context7@claude-plugins-official` entry to remove. They edit the existing file rather than replace it, so any permission rules saved there later survive. No commit.

## Tests

No unit test is added or changed. The change is harness configuration and documentation, with no code path for `unittest` to reach, so Verification checks the settings directly.

## Verification

- `make check` exits 0.
- `jq -c 'keys' .claude/settings.json` prints `["permissions"]`, and `diff <(git show origin/main:.claude/settings.json | jq .permissions) <(jq .permissions .claude/settings.json)` prints nothing.
- `jq -c '.enabledPlugins, (.extraKnownMarketplaces | keys)' .claude/settings.local.json` prints the three plugins as `true` with no `context7`, then `["astral-sh","backchain","claude-plugins-official"]`.
- `git check-ignore .claude/settings.local.json` prints the path, and `git status --porcelain` does not list it.
- In this worktree, after the strip, `claude -p --setting-sources project,local --permission-mode auto "Quote the daedalus SDLC status from your session context, or say none"` quotes the `Branch worktree-issue-11, issue #11` status. Dropping the user layer shows that the project-local file alone loads daedalus.
- `sh /Users/ckrough/.claude/plugins/cache/backchain/daedalus/12.4.0/scripts/daedalus.sh check-docs` reports 0 problems.
- After step 2 and the merge, the operator confirms two things on the main checkout: a fresh session prints the daedalus SessionStart status, and a new `claude --worktree` worktree contains `.claude/settings.local.json`.

## Experiments

No experiment warranted: local-scope `enabledPlugins` and `extraKnownMarketplaces` and `.worktreeinclude` are documented harness behavior (the changelog records `.worktreeinclude` fixes, and daedalus ships one). The `--setting-sources project,local` run in Verification tests the local-only load before the commit. Local-scope marketplace declaration stays untested on this machine, because the marketplaces are already installed.

## Architect review

- Important: daedalus's `docs/sdlc.md` and `/daedalus:setup` put enablement in the tracked `.claude/settings.json`, so a setup rerun would restore the private marketplace -> amended. The CLAUDE.md section records the departure and tells a rerun to keep both keys out. No ADR is written. CLAUDE.md loads in every session where setup would rerun, so it is the guard that fires at the right time.
- Important: a plain `claude -p` loads the user settings layer too, so it could pass without the local file -> amended. The run uses `--setting-sources project,local`, as daedalus's own CLAUDE.md prescribes, and happens after the strip and before the commit. Experiments now says local marketplace declaration remains untested.
- Nit: the main-checkout write is certain to be refused, by the daedalus gate on `main` and by the sandbox -> amended. It is now step 2, an operator edit that adds keys and removes `context7` rather than replacing the file.
- Nit: daedalus's rollback note says to disable it in `.claude/settings.json`, which does nothing here -> amended. CLAUDE.md says how to disable it locally.
- Nit: the public CLAUDE.md gives JSON that most cloners cannot use -> amended. The section opens by scoping itself to maintainers with access to `backchainai/daedalus`.
