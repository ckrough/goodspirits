---
title: Build an eval set for the profile-writing skill
issue: 9
date: 2026-11-20
---

# Build an eval set for the profile-writing skill

## Problem

A change to the `adoption-profile-writing` skill ships once `check_draft.py` passes and a reviewer reads one rewrite, as #5 (life in adopter words) did. No fixed set of real records is re-run after a change, so nobody can tell whether a change made drafts better or worse, and a regression in a hard rule (a bite left out, a placement constraint softened, an old observation kept after the record changed) can ship unseen. The maintainer cannot measure a skill change, and the shelter's writers and adopters get whatever it produces.

## Outcome

goodspirits holds 3 to 5 anonymized cases, each pairing an animal's shelter memo and behavior observations with the profile a person wrote from them, together covering a bite on file, a placement constraint, and a record that changed over time. Before shipping a skill change, the maintainer runs one command that drafts every case with the current skill, grades each draft with the `foha-adoption-tools` profile grader, and prints its grade beside the human profile's grade, so the maintainer can see whether the change helped or hurt.

## Constraints

- No real data enters `backchainai/foha-adoption-tools`: no case text, grades, or fixtures, including in any change made there for this eval (`tools/CLAUDE.md`).
- The grader has no text-file entry point; the new input path it needs writes nothing into the production results, ledger, or report under `data/grader/` (grader `CLAUDE.md`, `cli.py`, `judge.py`).
- goodspirits stays standard-library Python with no dependencies and no lockfile; the grader keeps its own uv environment (goodspirits `CLAUDE.md`, `Makefile`).
- The eval runs only on the operator's machine, never in CI: the runner lacks the `claude` CLI, cannot check out the private grader, and has no API key, and GitHub passes no secrets to workflows from forks (`.github/workflows/check.yml`, GitHub Actions secrets documentation).
- A run costs paid model calls: about 30 judge calls for 5 cases at 3 runs over draft and human profile, roughly 3 minutes, plus one drafting call per case; unchanged human profiles are served from the judge cache (grader `CLAUDE.md`, Anthropic pricing).
- Anything pushed to the public `ckrough/goodspirits` repository cannot reliably be taken back, since it stays reachable in clones, forks, and cached commit views (GitHub "Removing sensitive data from a repository").
- Each case is de-identified to NIST SP 800-188: direct identifiers removed (the animal's name, shelter ID, people's names, addresses, exact dates) and quasi-identifiers generalized (breed, age, intake date, location) (NIST SP 800-188).
- Each case records its de-identification technique in ISO/IEC 20889 terms: pseudonymization, generalization, or suppression (ISO/IEC 20889:2018).
- The operator reviews every case before it is committed (operator requirement, NIST SP 800-188).
- goodspirits finds the grader through a configured local path, such as an environment variable; the command stops with a clear message when the grader or the key is absent, and no grader code or rubric is copied into the public repository (`tools/CLAUDE.md`, goodspirits README license).
- The report shows the grader's computed dimensions apart from the LLM judge's dimensions, because a Claude judge scoring Claude drafts against human profiles is prone to self-enhancement and verbosity bias (Zheng et al. 2023, arXiv:2306.05685).
- The report shows each case with the judge's run-to-run spread and declares no pass or fail from an average, since 3 to 5 cases cannot detect small differences between skill versions (Miller 2024, arXiv:2411.00640).
- Each report records the judge model, effort, and judge-prompt hash; when any changes, the human profiles are regraded rather than compared against stored grades (Anthropic model deprecations).
- The residual risk that a human profile, published word for word on foha.org, links a case back to its live page is accepted, since many profiles look alike (operator requirement).
- FOHA's approval is not needed to publish the anonymized cases (operator requirement).
- Cases come from the ShelterLuv memo export and the behavior observations in `animal-rescue/adoption-profiles`, with the profile as published (operator requirement).
- The command runs the skill headless with `claude -p`, loading the plugin from the working tree, so it tests the unshipped change (operator requirement).
- The grader's text-input path is built as a separate issue on `foha-adoption-tools` that blocks this one (operator requirement).
- The eval grades only the Description (the kennel card) text: it evaluates the profile-writing skill, not the grading workflow, so dimensions that need labels or photos are left out (operator requirement).

## Open questions

None.

## Acceptance criteria

- The 3 to 5 anonymized cases are stored in this repository, and no case names a real volunteer, staff member, or adopter.
- One command runs the current skill over every case and reports each draft's grade beside the human profile's grade.
- At least one case has a bite on file, one has a placement constraint, and one has a record that changed over time, and each case names the rule it covers.
- Each case records how it was de-identified, in ISO/IEC 20889 terms.
- `make eval` drafts each case with the working-tree skill through headless `claude -p` and finds the grader through an environment variable pointing to its local clone.
- `make eval` stops with a clear message, before any model call, when the grader path or `ANTHROPIC_API_KEY` is missing.
- `make check` and CI are unchanged, and `make check` passes on a machine without the grader clone.
- The eval grades only the Description text, and dimensions that need labels or photos are left out for both the draft and the human profile.
- The report lists each case with the draft's grade beside the human profile's grade, shows the computed dimensions apart from the judge's dimensions, gives the judge's run-to-run spread, and declares no pass or fail.
- The report records the judge model, effort, and judge-prompt hash.
- The report goes to stdout and a gitignored folder; no grade is committed, and nothing is written into the grader's production `data/grader/`.
- The grader's text-input path is filed as an issue on `backchainai/foha-adoption-tools` that blocks #9.
- The goodspirits `CLAUDE.md` Commands table and the README document `make eval`.
