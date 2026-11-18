# Review policy

The `reviewer` agent applies these passes to `git diff origin/<default>...HEAD` in a fresh context. The ship skill hands it the findings of `/code-review` for the bugs pass and of the `security` agent, which runs `/security-review`, for the security pass (skipped when every changed path is Markdown), and the reviewer confirms, ranks, or drops each. Findings inform the human reviewer and never approve a pull request; an Important finding still open in the third review cycle stops `/daedalus:ship` before it opens one.

## Passes

1. **Bugs.** Logic errors, unhandled failure paths, broken edge cases, and tests that pass without exercising the change.
2. **Security.** Injection, authorization gaps, secrets, unsafe deserialization, path traversal, and new dependencies.
3. **Conformance.** The diff against the issue's spec, its plan (including `## Files`), and the decisions in `docs/decisions/`.

## Severity

- **Important**: a defect, a security exposure, or a departure from the spec or plan. Each one is fixed before the pull request opens; `/daedalus:ship` stops for the operator when one is still open in its third review cycle.
- **Nit**: style or a small improvement. Report at most five of your own; list every finding passed in from `/code-review` or `/security-review` with its disposition.

## Callouts

The pull request lists each callout that applies under Reviewer callouts, above its evidence, so the human reviewer sees them first:

- **Harness paths.** Changed files under or named `.claude/`, `.github/`, `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `Makefile`, `GNUmakefile`, `justfile`, `package.json`, `pyproject.toml`, and the paths in the CLAUDE.md Harness paths section. They define the gates or the agent's instructions.
- **Dependencies and decisions.** New or loosened dependencies, and new files in `docs/decisions/`.
- **Project paths.** Changed paths that Project specifics below names for human review.

## Project specifics

- **Phrase lists stay dense.** The curated phrase lists in `check_draft.py` are kept on long lines on purpose, so `ruff format` is not part of `make check`. Do not flag them for formatting.
- **The checker and the template example agree.** `tests/test_check_draft.py` runs the example card in `references/profile-template.md` through `check_draft.py`. A change to either that breaks the other is an Important finding.
- **Research citations use primary sources.** Citations under `references/` cite vendor documentation or primary academic sources, not blog or influencer content.
