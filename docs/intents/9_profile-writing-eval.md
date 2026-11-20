---
title: Build an eval set for the profile-writing skill
issue: 9
date: 2026-11-20
---

# Build an eval set for the profile-writing skill

## Problem

A change to the `adoption-profile-writing` skill ships once `check_draft.py` passes and a reviewer reads one rewrite, as #5 (life in adopter words) did. No fixed set of real records is re-run after a change, so nobody can tell whether a change made drafts better or worse, and a regression in a hard rule (a bite left out, a placement constraint softened, an old observation kept after the record changed) can ship unseen. The maintainer cannot measure a skill change, and the shelter's writers and adopters get whatever it produces.

## Outcome

The plugin carries its own eval suite: 3 to 5 anonymized cases, each pairing an animal's record (its shelter memos and behavior observations) with an ideal Description the operator provides, together covering a bite on file, a placement constraint, and a record that changed over time. Before shipping a skill change, the maintainer runs one command that has the current skill write a Description from every case's record and scores each draft against that case's ideal, so the maintainer can see whether the change helped or hurt. Each run the maintainer keeps is recorded in the repository with the commit hash of the skill it scored, so performance can be tracked over time. The eval tests only the skill: a set of inputs, the template and prompts, and the Description it produces.

## Constraints

- The eval tests the plugin and skill on their own: records in, Description out, scored against the operator's ideal examples, with no dependency on `foha-adoption-tools` or its profile grader (operator requirement).
- The suite uses Claude Code's built-in `claude plugin eval`, with cases under the plugin's `evals/` directory (operator requirement, Claude Code plugin-evals documentation).
- `claude plugin eval` has no grader that reads a reference-answer file, so each case's ideal Description is carried in the criteria of its `llm` graders, which judge the draft against it (Claude Code plugin-evals documentation, "Grader types").
- goodspirits adds no dependencies and no lockfile (goodspirits `CLAUDE.md`, `Makefile`).
- The eval runs only on the operator's machine, never in CI: the runner lacks the `claude` CLI, and GitHub passes no secrets to workflows from forks (`.github/workflows/check.yml`, GitHub Actions secrets documentation).
- A run costs paid model calls: one drafting run and its graders per case per run, three runs per case by default (Claude Code plugin-evals documentation).
- Anything pushed to the public `ckrough/goodspirits` repository cannot reliably be taken back, since it stays reachable in clones, forks, and cached commit views (GitHub "Removing sensitive data from a repository").
- Each case is de-identified to NIST SP 800-188: direct identifiers removed (the animal's name, shelter ID, people's names, addresses, exact dates) and quasi-identifiers generalized (breed, age, intake date, location) (NIST SP 800-188).
- Each case records its de-identification technique in ISO/IEC 20889 terms: pseudonymization, generalization, or suppression (ISO/IEC 20889:2018).
- The operator reviews every case before it is committed (operator requirement, NIST SP 800-188).
- The judge model is named in the eval command, so scores from two runs compare only under the same judge (Anthropic model deprecations).
- A Claude judge scoring a Claude draft is prone to self-enhancement and verbosity bias, so a score is a signal to read, not a verdict (Zheng et al. 2023, arXiv:2306.05685).
- Results are read per case, and no decision rests on a set-wide average, since 3 to 5 cases cannot detect small differences between skill versions (Miller 2024, arXiv:2411.00640).
- The residual risk that a case's text links it back to a published foha.org profile is accepted, since many profiles look alike (operator requirement).
- FOHA's approval is not needed to publish the anonymized cases (operator requirement).
- Case records come from the ShelterLuv memo export and the behavior observations in `animal-rescue/adoption-profiles` (operator requirement).
- The eval scores only the Description (the kennel card) text (operator requirement).

## Open questions

None.

## Acceptance criteria

- The 3 to 5 anonymized cases are stored in this repository, and no case names a real volunteer, staff member, or adopter.
- One command runs the current skill over every case and reports each draft's score against that case's ideal Description.
- At least one case has a bite on file, one has a placement constraint, and one has a record that changed over time, and each case is tagged with the rule it covers.
- Each case records how it was de-identified, in ISO/IEC 20889 terms.
- `make eval` runs `claude plugin eval` on the working-tree plugin with a named judge model.
- `make check` and CI do not run the eval, and `make check` passes on a machine without an API key.
- The eval report shows each case's score and its graders' verdicts on their own, and declares no set-wide pass or fail.
- Raw eval results are gitignored; a summary of each run the maintainer records, naming the commit hash of the skill it scored, is committed under the plugin's `evals/` directory (operator requirement).
- The goodspirits `CLAUDE.md` Commands table and the README document `make eval` and how to add a case.
