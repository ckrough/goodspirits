---
title: Onboard goodspirits to the daedalus SDLC
issue: 6
type: Task
date: 2026-11-17
---

# Onboard goodspirits to the daedalus SDLC

## Context

This implements the acceptance criteria of #6. goodspirits has no CLAUDE.md, Makefile, CI, or tests, so daedalus has no check command to gate verification or `/daedalus:ship`. #5 (write profiles as life with the animal) is paused until this lands.

The repository is one standard-library Python script (`check_draft.py`) plus Markdown, with no `pyproject.toml` or lockfile. The targets therefore call `python3` and `uvx ruff@0.17.5` directly instead of the `uv run --frozen` the daedalus contract describes for uv projects:

- `setup` is a no-op, because there is nothing to install.
- `check` is `test` plus `lint`. It leaves out `format --check`, an operator decision, so the curated phrase lists in `check_draft.py` stay dense.
- `verify` is `check`, then `claude plugin validate` on the marketplace and on the plugin.

CI has no `claude` CLI, so it runs only a `check` job, on pushes to `main` and on pull requests, and CLAUDE.md records why.

The files are written by hand from the `/daedalus:setup` templates instead of by running the skill, because four parts depart from its proposal: the Makefile is not the uv template, `check` has no `format --check`, CI has no `verify` job, and `.gitignore` gets a negation. Files matches the paths the setup dry run listed, plus the test file.

## Files

- `Makefile`
- `tests/test_check_draft.py`
- `CLAUDE.md`
- `REVIEW.md`
- `.claude/settings.json`
- `.gitignore`
- `docs/intents/README.md`
- `docs/specs/README.md`
- `docs/plans/README.md`
- `docs/decisions/README.md`
- `.github/workflows/check.yml`

## Work order

1. Write `tests/test_check_draft.py` and `Makefile`, and commit when `make check` exits 0.
   - The test loads `check_draft.py` by path with `importlib` and pulls out the fenced card under `## Example` in `references/profile-template.md`.
   - It substitutes `Polly` for `[Name]` and `Riverside` for `[Shelter]`. The Diamond Dog matcher's name and shelter slots do not accept square brackets, and the skill tells writers to replace both placeholders before running the checker.
   - It writes the card to a temporary file, asserts that `main([path])` returns 0, and captures stdout with `contextlib.redirect_stdout`.
   - Two variants assert a return of 1: one with the TRAINING heading removed, and one with a first-person sentence added to ABOUT THIS PET.
   - The module docstring notes that the test depends on the example's heading, fence, and placeholders, so any change to that example lists this test in its plan.
   - The `Makefile` has `setup` (an echo: no dependencies, no lockfile), `test` (`python3 -m unittest discover -s tests`), `lint` (`uvx ruff@0.17.5 check plugins tests`), `format` (`uvx ruff@0.17.5 format plugins tests`), `check` (`test lint`), and `verify` (`check`, then `claude plugin validate .` and `claude plugin validate plugins/adoption-profile-writing`), all in `.PHONY`.
2. Runs in parallel with step 3, since the files are disjoint. Write these files, and commit when `make check` exits 0:
   - `CLAUDE.md` gets `## Commands`, which lists the six targets, explains that `setup` is a no-op because the repo has no dependencies or lockfile, explains that `format` is kept out of `check` on purpose, explains that CI has no `verify` job because it lacks the `claude` CLI, and gives `make check`'s healthy output with the numbers that change written as `N`. It also gets `## Issue tracker`: GitHub Issues on `origin`, with the type as a `bug`, `feature`, or `task` label and the priority as a `p0`-`p4` label, because `ckrough/*` cannot set issue types.
   - `REVIEW.md` comes from the template, with `## Project specifics` filled in: the phrase lists in `check_draft.py` stay dense and ruff format is excluded on purpose; the checker and the template example must keep agreeing, which `tests/test_check_draft.py` enforces; and research citations under `references/` use primary sources.
   - The four `docs/*/README.md` files come from the template.
   - `.gitignore` changes `.claude/` to `.claude/*` plus `!.claude/settings.json`.
   - `.claude/settings.json` enables `daedalus@backchain` and lists three marketplaces under `extraKnownMarketplaces`: `backchain` from `backchainai/daedalus`, `claude-plugins-official` from `anthropics/claude-plugins-official`, and `astral-sh` from `astral-sh/claude-code-plugins`. Its `permissions.deny` covers the `gh pr merge`/`review` commands, the `gh api` merge, approve, and auto-merge forms, `git push --force`, `-f`, and `+refspec`, `git reset --hard`, and the GitHub MCP merge and review tools, exactly as the setup skill lists them.
3. Runs in parallel with step 2. Write `.github/workflows/check.yml` from the setup `check.yml` template, and commit when `make check` exits 0. It has one `check` job, with no `if:`, that runs on `push` to `main` and on `pull_request`. The job checks out with `fetch-depth: 0`, installs `uvx` with `astral-sh/setup-uv@v7`, then runs `make setup` and `make check`. There is no `verify` job.

## Tests

`tests/test_check_draft.py` adds three tests:

- The template's example card, with the placeholders filled in, passes the checker. This proves the checker and the shipped example agree.
- The card with TRAINING removed fails with a missing-heading finding.
- The card with a first-person sentence fails with a first-person finding.

## Verification

- `make check` exits 0 and reports 3 tests passing and `All checks passed!` from ruff.
- `make verify` exits 0, and both `claude plugin validate` runs print `Validation passed`.
- `git check-ignore .claude/settings.json` prints nothing, and `git check-ignore .claude/worktrees/x` prints the path.
- `sh /Users/ckrough/.claude/plugins/cache/backchain/daedalus/12.3.1/scripts/daedalus.sh check-docs` reports 0 problems.

## Experiments

No experiment warranted. `ruff check`, `claude plugin validate`, and the checker's `main()` signature were confirmed by running them or reading the source. The architect ran the extracted example through the checker and found it fails with the literal placeholders and passes with them filled in, and step 1 now fills them in.

## Architect review

- Important: the template's example card fails `check_draft.py` as shipped, because the Diamond Dog matcher rejects the literal `[Name]` and `[Shelter]`, so step 1's main test would fail -> amended. The test substitutes a name and shelter first, and the Experiments line now says this was tested, not assumed. No Bug is filed: the skill tells writers to replace the placeholders before running the checker.
- Nit: the echo-only `setup` and bare `python3` depart from the contract's lockfile and `uv run --frozen` pattern, so interpreters can drift -> amended in part. CLAUDE.md now says why `setup` is a no-op. The interpreter is not pinned, because the script is standard-library only and has no dependencies to drift.
- Nit: say whether steps 2-3 run `/daedalus:setup` or are hand-written -> amended. Context says they are hand-written because of four deviations, and Files matches the dry run.
- Nit: fill REVIEW.md's `## Project specifics` -> amended in step 2.
- Nit: the new test depends on the example's location and placeholders, which #5 will rewrite -> amended. The test docstring says so, and #5's plan will list the test in its Files.
