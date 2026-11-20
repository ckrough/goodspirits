---
title: Build an eval set for the profile-writing skill
issue: 9
date: 2026-11-20
---

# Build an eval set for the profile-writing skill

## Requirements

1. The plugin holds 3 to 5 eval cases under `plugins/adoption-profile-writing/evals/<case-id>/`, each loadable by `claude plugin eval`.
2. Each case gives the skill one anonymized record (`resources/record.md`: the ShelterLuv memos and behavior observations in date order) and asks for a Description from it, with the skill as the only tool beyond reading.
3. Each case scores the draft against the operator's ideal Description with weighted graders: an `llm` grader carrying the ideal in its criteria, `llm` graders for the case's hard-rule expectations, and a `regex` grader per required section heading.
4. Across the set, at least one case has a bite on file, one has a placement constraint, and one has a record that changed over time; each case's `tags` name the rules it covers, drawn from `bite`, `placement-constraint`, and `changed-record`.
5. Each case records how it was de-identified in `deidentification.md`, naming for each change the ISO/IEC 20889 technique (`pseudonymization`, `generalization`, `suppression`) and the kind of field it was applied to.
6. No case names a real volunteer, staff member, or adopter, or carries the animal's real name, its ShelterLuv ID, an address, or a calendar date; record dates are relative to intake ("day 1", "week 3"), and the animal carries one pseudonym across the record and the ideal.
7. `make eval` runs `claude plugin eval plugins/adoption-profile-writing` with a named judge model (`JUDGE_MODEL`, default `claude-sonnet-5-5`) and `--threshold 0`, so a low score reports without failing the command.
8. The run keeps the default with-without ablation, so the report shows each case's score with the skill, without it, and the difference.
9. Raw eval results under `plugins/adoption-profile-writing/evals/results/` are gitignored.
10. `make check` and CI do not run the eval, and `make check` passes on a machine with no API key; `.github/workflows/check.yml` is unchanged.
11. A standard-library test checks every case's structure, tags, de-identification record, and the absence of calendar dates, and runs in `make test`.
12. The goodspirits `CLAUDE.md` Commands table and the README document `make eval`, `make eval-record`, `JUDGE_MODEL`, and how to add a case.
13. `make eval-record` writes a summary of the latest run to `plugins/adoption-profile-writing/evals/history/<timestamp>_<short-hash>.json`, naming the commit hash of the skill it scored, the Claude Code version, the judge model, each case's score with and without the skill and the difference, and each grader's pass rate in each arm; it refuses to record when the plugin has uncommitted changes, so the hash names the skill that ran. The operator commits the summary.

## Design

**Case layout.** One directory per case, the id a short slug of the pseudonym:

```
plugins/adoption-profile-writing/evals/case-juniper/
  prompt.md                 # frontmatter: tags, runs, max_turns, allowed_tools; body: the request
  case.yaml                 # schema_version, name, context.add_dirs: [resources]
  resources/record.md       # the anonymized record
  deidentification.md       # what was changed, by ISO/IEC 20889 technique
  graders/
    matches-ideal.md        # llm, weight 3: the ideal Description, and PASS when the draft carries its facts and placement terms without adding any
    <rule>.md               # llm, weight 2 each: one hard-rule expectation, e.g. "discloses the bite on day 4 in plain words", "states the no-cats limit as a home requirement", "uses the week-6 leash observation, not the week-1 one"
    heading-<section>.md    # regex, weight 1 each: ABOUT THIS PET, HOUSEHOLD FIT, TRAINING, GOOD TO KNOW
    skill-fired.md          # tool_used Skill: an indicator in the with-only arm, outside the score
```

The prompt body reads like a writer's request: write the Description for this animal from `resources/record.md`. `allowed_tools` is `[Read, Glob, Grep, Skill]`, so the skill cannot run `check_draft.py`; the eval measures the prose the skill's instructions produce. The draft is the last message, which every grader reads by default.

**Ideal examples.** The operator writes each ideal Description, starting from the published profile where that helps, and it lives only in `graders/matches-ideal.md`. The rule graders state their expectation as facts, so they do not repeat the ideal.

**Scoring.** `claude plugin eval` scores a run as the weighted share of graders that pass, a case as the mean of its runs (3 by default), and votes each `llm` grader PASS on 2 of 3 judge calls. `--threshold 0` keeps the exit status for load and run errors only. The HTML report and `aggregate-result.json` land in `evals/results/<timestamp>/`.

**History.** `evals/record_eval.py`, standard library only, reads the newest `aggregate-result.json` (or one named on the command line), takes the commit from `git rev-parse HEAD`, refuses when `git status --porcelain` lists a change under the plugin outside `evals/results/` and `evals/history/`, and writes the summary JSON. `make eval-record` runs it.

**Make target.** `eval` in the `Makefile`, with `JUDGE_MODEL ?= claude-sonnet-5-5`. It is not a prerequisite of `check` or `verify`.

**Test.** `tests/test_evals.py` walks `evals/`, skipping `results/`, and for each case asserts `prompt.md`, `case.yaml`, `resources/record.md`, `deidentification.md`, `graders/matches-ideal.md`, and the four heading graders exist; that `tags` in the `prompt.md` frontmatter hold only known rule names and together cover all three; that `deidentification.md` names at least one technique; and that no case file holds a four-digit year or a `YYYY-MM-DD` date. It parses the frontmatter with the standard library.

## Decisions applied

- None. `docs/decisions/` holds no ADR yet.

## Flagged concerns

- Whether `evals/` ships to users who install the plugin from the marketplace is not documented. If it does, installs carry the cases and the ideals. The plan checks this by installing from a local marketplace, and if it ships, moves the suite under a path the marketplace excludes or accepts it.
- The path at which `context.add_dirs` exposes `resources/` to the agent is not documented; the plan confirms it with `--keep-temp` and words the prompt to match.
- `claude plugin eval` publishes its HTML report to claude.ai by default. Should `make eval` pass `--no-publish` to keep reports local? The design assumes yes.
- The judge never sees the record, only the draft and the ideal, so a fact the draft invents that the ideal lacks fails `matches-ideal` without saying which fact. Judging against the record would need the record copied into a grader too.

## Acceptance tests

- Requirement 1: `claude plugin eval plugins/adoption-profile-writing` loads every case with no load error; `tests/test_evals.py` finds 3 to 5 cases.
- Requirement 2: the test asserts `resources/record.md` exists and `case.yaml` lists `resources` in `add_dirs`; a run's trace shows the record read and the skill invoked.
- Requirement 3: the test asserts `matches-ideal.md` and the four heading graders exist; reading each case's graders.
- Requirement 4: the test asserts every tag is a known rule name and the set covers all three.
- Requirement 5: the test asserts `deidentification.md` names an allowed technique.
- Requirement 6: the operator's review of each case before commit, recorded in the pull request; the test rejects a four-digit year or a `YYYY-MM-DD` date.
- Requirement 7: `make -n eval` shows `claude plugin eval plugins/adoption-profile-writing --judge-model claude-sonnet-5-5 --threshold 0`.
- Requirement 8: one `make eval` run's report shows WITH, W/OUT, and Δ per case.
- Requirement 9: `git check-ignore plugins/adoption-profile-writing/evals/results/x` succeeds.
- Requirement 13: a unit test feeds the recorder a fixture `aggregate-result.json` and checks the summary fields and the refusal on a dirty plugin; the operator records one real run and commits it.
- Requirement 10: `make -n check` does not mention `eval`; `make check` passes in CI on the pull request; `git diff main -- .github/workflows/check.yml` is empty.
- Requirement 11: `make test` runs `tests/test_evals.py`.
- Requirement 12: reading the `CLAUDE.md` Commands table and the README section.
