---
title: Build an eval set for the profile-writing skill
issue: 9
type: Feature
date: 2026-11-20
---

# Build an eval set for the profile-writing skill

## Context

This implements `docs/specs/9_profile-writing-eval.md`, from the intent `docs/intents/9_profile-writing-eval.md`: an eval suite inside the plugin that `claude plugin eval` runs, scoring each Description the skill writes against the operator's ideal for that case.

The cases come from ShelterLuv Memos exports and volunteer behavior notes the operator supplied. The conversions and the mapping from each case to its source animal live only in the session scratchpad, outside every repository; no real animal name, person's name, or history detail is written under goodspirits, this plan included.

| Case | Rules |
|---|---|
| `case-bramble` | `bite` |
| `case-juniper` | `changed-record`, `placement-constraint` |
| `case-marlow` | `placement-constraint`, plus a serious incident the skill must route to the history review |
| `case-tansy` | `placement-constraint` |

Pseudonyms are placeholders the operator may change at review.

Departures from the spec, each deliberate:

- **Ideals.** At the operator's direction, Claude drafts each ideal from the published Description, anonymized and corrected until `check_draft.py` lists no fixes, and the case carries the tag `ideal-pending` until the operator rewrites or approves its ideal; removing the tag records that approval. The spec's "The operator writes each ideal Description" is met when the last tag is removed. Pending cases run in `make eval` like the rest, and the report names them by tag.
- **Tags** live in `case.yaml`, a documented top-level key, not `prompt.md` (experiment below), and `ideal-pending` joins the three rule names.
- **Record delivery.** The spec's `context.add_dirs: [resources]` did not reach the agent: on Claude Code 2.1.329 the session started with no additional directories and every read outside the working directory was denied. Each case instead carries `fixture.sh`, a `context.scaffold_script` that copies `resources/` into the empty workspace, the plugin-eval scaffold pattern and the agentskills.io input-files pattern. `make eval` passes `--scaffold`, which runs that script as the operator, so every case's `fixture.sh` must be byte-identical to the one copy-only script, enforced by the test.
- **Graded file.** Each prompt asks the skill to save the finished profile to `profile.md`, `allowed_tools` adds `Write` (granted with `--allow-tools Write`), and every grader reads that file (`target`/`focus: {source: file, path: profile.md}`) with a `file_exists` grader `profile-saved` beside them. A `regex` grader cannot be limited to the text under the headings, and the skill's notes after a draft name the incidents it held back. `make eval` also passes `--trust-plugin`, since a run without a terminal cannot answer the trust prompt.
- **`matches-ideal`** passes when the draft carries the ideal's behavior facts and placement terms and contradicts none; facts the ideal lacks do not fail it (operator decision after the first case run).
- **Marlow** has no serious incident under the skill's five: the lunge and the guarding made no contact. The case instead tests that the guarding is named as an ordinary struggle and that the senior program block precedes the Diamond Dog message.
- **`ideal.md` stays in each case** as the copy the operator edits; `tests/test_evals.py` fails when `graders/matches-ideal.md` no longer embeds it word for word.
- **Recorded history** (operator requirement, amending the intent): `evals/record_eval.py` and `make eval-record` write a committed summary per kept run to `evals/history/`. `make eval` runs one sweep per call: the suite once for each writer model in `MODELS` (Haiku, Sonnet, and Opus 5.5), each pinned with `--model` and written to `evals/results/<sweep>/<model>/`, to show where quality falls off. `make eval-record` writes one summary per model, naming the model from its run directory, since the result file names only the judge. An unpinned run would score whatever the account's default model is, and a later change of default would move the history with nothing recording why (operator decision after the first full run started).
- **The bite expectation.** The spec's example grader "discloses the bite on day 4 in plain words" contradicts the skill: a bite stays off the card and GOOD TO KNOW ends with the history-review line (`SKILL.md` "Serious incidents go to the consultation", `references/profile-template.md` line 130). The graders follow the skill.

A marketplace install copies the whole plugin directory, so `evals/` ships to installers. The cases are anonymized and the repository is public, so this adds no exposure the intent has not accepted; the plugin version moves to 0.5.0 because installs change.

## Files

- `plugins/adoption-profile-writing/evals/`
- `plugins/adoption-profile-writing/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `tests/test_evals.py`
- `tests/test_record_eval.py`
- `Makefile`
- `.gitignore`
- `CLAUDE.md`
- `README.md`
- `plugins/adoption-profile-writing/skills/adoption-profile-writing/SKILL.md` and `plugins/adoption-profile-writing/skills/adoption-profile-writing/references/profile-template.md`: departure, at the operator's direction. Shelters do not test animals with children; how an animal does with children is known or not known. The skill said "has not been tested with children", which every eval run copied.

## Work order

1. **Harness spike, then the make target.** Build a made-up toy case (a dog "Pat" with three observations) in a scratch copy of the plugin under the session scratchpad and have the operator run it once outside the Claude sandbox, where `claude plugin eval` can start its agent: `! claude plugin eval <scratch copy> --runs 1 --ablation none --judge-model claude-sonnet-5-5 --threshold 0 --no-publish --keep-temp --trust-plugin`. Read the kept workspace and trace to settle where `resources/` appears to the agent, whether naming `resources/record.md` in the prompt works, whether an `llm` grader carrying a reference text and told to grade only the text under the four headings votes sensibly, and how many turns and seconds a drafting run takes. Fix the case template from what it shows, and set `max_turns` and `timeout_seconds` at twice the observed values. Then add the `eval` target and `JUDGE_MODEL ?= claude-sonnet-5-5` to `Makefile` (`claude plugin eval plugins/adoption-profile-writing --judge-model $(JUDGE_MODEL) --threshold 0 --no-publish --scaffold`), add `plugins/adoption-profile-writing/evals/results/` to `.gitignore`, run `make check`, and commit.
2. **Build the four cases, stopping for the operator.** For each animal, in the scratchpad:
   - Read the memos and volunteer notes in date order. Write `resources/record.md` with the pseudonym, no person's name (staff and volunteers become roles: "a volunteer", "the behavior team"), no ShelterLuv ID, address, or calendar date, dates rewritten relative to intake ("day 4", "month 7"), breed and age generalized.
   - Write `deidentification.md` listing each change by technique (`pseudonymization`, `generalization`, `suppression`), citing ISO/IEC 20889 without its year.
   - Write `case.yaml` (`schema_version: "1.1"`, `name`, `tags: [..]` in flow form, `context:` with `scaffold_script: fixture.sh`), copy the shared `fixture.sh`, and write `prompt.md` (`runs`, `max_turns`, `timeout_seconds`, `allowed_tools: [Read, Glob, Grep, Skill]`, a writer's request naming `resources/record.md`).
   - Write the graders. Every `llm` grader's criteria say to grade only the text under the four headings and ignore notes before or after it.
     - `graders/matches-ideal.md`: `llm`, weight 3, the ideal plus PASS when the card carries the ideal's behavior facts and placement terms and adds none.
     - `bite` and any serious incident: `graders/no-incident-words.md`, `regex`, `match: not_contains`, `pattern: '\b(bite[sd]?|bitten|biting|nipped|snapped at|attack(ed)?)\b'`, `flags: i`, weight 2; and `graders/history-review.md`, `regex`, `pattern: 'full history with you'`, `flags: i`, weight 2.
     - `placement-constraint`: `graders/placement-<limit>.md`, `llm`, weight 2, PASS when HOUSEHOLD FIT states the limit as a requirement of the home, not a condition on the adopter.
     - `changed-record`: `graders/latest-observation.md`, `llm`, weight 2, naming the earlier and later observation and PASS when the card reflects the later one.
     - Four heading graders, `regex`, weight 1: `pattern: '^\s*#{0,6}\s*[*_]*\s*<HEADING>\s*[*_:]*\s*$'`, `flags: m`, matching the headings `check_draft.py` accepts.
     - `graders/skill-fired.md`: `tool_used`, `tool: Skill`, `input_match: '"skill"\s*:\s*"(?:[\w-]+:)?adoption-profile-writing"'`, an indicator outside the score under the default ablation.
   - Draft the ideal from the published Description, anonymized, and run `scripts/check_draft.py` on it until it lists no fixes. Tag the case `ideal-pending`.
   - Search every scratch case file for the source animal's real name, its ShelterLuv ID, and every person's name in the memo export's author and staff fields and the volunteer-notes name column. Report any hit and fix it.
   - **Stop and show the operator the record, the de-identification log, the graders, and the draft ideal. Copy a case into `plugins/adoption-profile-writing/evals/` only after the operator approves its anonymization.**

   Then write `tests/test_evals.py`, run `make check`, and commit the cases with the test.
3. **Recorder.** Write `tests/test_record_eval.py` first against a fixture result, then `plugins/adoption-profile-writing/evals/record_eval.py` and the `eval-record` target; add `--trust-plugin` and `--allow-tools Write` to `eval`. Run `make check` and commit.
4. **Docs and version.** Add `make eval`, `make eval-record`, and `JUDGE_MODEL` to the `CLAUDE.md` Commands table, with a note that the eval runs outside the Claude sandbox (`! make eval`) and stays out of `check`, `verify`, and CI. Add an "Evals" part to the README's plugin section: what the suite measures, how to run it, that `evals/` ships with installs, and how to add a case (the files, `case.yaml` in flow form, the tags, `ideal-pending`, the de-identification rule, and no year on any citation in a case file). Bump `version` to 0.5.0 in `plugin.json` and in both places in `marketplace.json`. Run `make check` and commit. Steps 2 and 3 touch disjoint files and may run in parallel once step 1 lands.

## Tests

`tests/test_evals.py`, standard library only, in `make test`:

- finds 3 to 5 case directories under `plugins/adoption-profile-writing/evals/`, skipping `results/` and `history/`;
- each holds `case.yaml`, `prompt.md`, `fixture.sh`, `resources/record.md`, `deidentification.md`, `graders/matches-ideal.md`, `graders/profile-saved.md`, `graders/skill-fired.md`, and the four heading graders, and every scored grader reads `profile.md`;
- each `case.yaml` names `fixture.sh` as its `scaffold_script`, every `fixture.sh` is byte-identical to the copy-only script, and each `case.yaml`'s `tags` hold only `bite`, `placement-constraint`, `changed-record`, and `ideal-pending`, with the three rule tags covered across the set;
- a case tagged `bite` holds the incident-words and history-review graders;
- each `deidentification.md` names at least one of `pseudonymization`, `generalization`, `suppression`;
- no case file holds a `YYYY-MM-DD` date, a `M/D/YYYY` date, or a four-digit year from 1990 to 2099;
- no grader pattern holds an inline flag group (`(?i)`, `(?m)`), which the JavaScript regex engine rejects, and each heading grader carries `flags: m`.

`tests/test_record_eval.py` feeds `record_eval.py` a small fixture `aggregate-result.json` and a fake git state, and checks the summary's commit, versions, per-case with, without, and Δ, and per-grader pass rates, and that it refuses when the plugin has uncommitted changes.

The test proves the suite's shape and the de-identification rules a machine can check; the name search and the operator's review in step 2 cover names and recognizable detail.

## Verification

- `make check` exits 0.
- `make verify` exits 0 (`claude plugin validate` on the marketplace and the plugin at 0.5.0).
- `make -n eval` shows a loop over `claude-haiku-5-5 claude-sonnet-5-5 claude-opus-5-5` running `claude plugin eval plugins/adoption-profile-writing --model $model --judge-model claude-sonnet-5-5 --threshold 0 --no-publish --scaffold --trust-plugin --allow-tools Write --output-dir plugins/adoption-profile-writing/evals/results/$sweep/$model`.
- The operator runs `! make eval-record` on a clean tree and commits the summary it writes.
- `make -n check` and `make -n verify` do not mention `eval`; `git diff main -- .github/workflows/check.yml` is empty.
- `git check-ignore plugins/adoption-profile-writing/evals/results/x` succeeds.
- The operator runs `! make eval` once outside the sandbox; it loads all four cases without a load error, and the report shows WITH, W/OUT, and Δ per case with each grader's verdict. The result counts as done when every case runs, whatever its score.

## Experiments

- A marketplace install of a relative-path plugin copies the whole plugin directory, so `evals/` ships: supported. Evidence: the Claude Code plugin loading documentation, and an installed plugin's cache holding its `evals/`. Plan change: version bump to 0.5.0 and an install note in the README; no exclusion mechanism exists.
- `claude plugin eval` loads a case from `case.yaml` with `context.add_dirs`, `prompt.md`, and `graders/*.md`, and accepts `--judge-model claude-sonnet-5-5` and `--threshold 0`: supported. Evidence: a toy case loaded with all five graders parsed; the run itself failed `run could not start (EPERM)` inside the Claude sandbox. Plan change: `make eval` runs outside the sandbox, and step 1 settles the agent-side behavior with one operator-run toy case.
- `tags` read from `prompt.md` frontmatter: unknown; the result JSON carried no tags. Plan change: tags go in `case.yaml`.
- An inline `(?m)` in a `regex` grader: ruled out. Evidence: graders use JavaScript regex, which rejects it as an invalid group. Plan change: `flags: m`, enforced by the test.
- The `tool_used: Skill` grader under the default with-without ablation: supported as an indicator only, outside the score (plugin-evals documentation). Plan change: none.
- `context.add_dirs` gives the agent read access to `resources/`: ruled out. Evidence: two operator-run spikes on Claude Code 2.1.329; the trace's init shows `additional_directories: []`, and Glob, Grep, and Read outside the working directory were denied in `dontAsk` mode. Plan change: a copy-only `scaffold_script` and `--scaffold`.
- A `scaffold_script` puts `resources/record.md` where the prompt names it: supported. Evidence: the third spike read `home/cwd/resources/record.md`, invoked the skill, and drafted the four sections in 6 turns and 36 seconds for $0.30; the `llm` grader graded only the text under the headings. Plan change: `max_turns: 15` and `timeout_seconds: 120`, twice the observed values rounded up for records longer than the toy's three entries.

## Architect review

- Important: the Context table mapped each pseudonym to its real animal and history, published with the plan -> amended: the mapping stays in the scratchpad, and step 2 adds a mechanical name and ID search before the operator review.
- Important: draft ideals are committed before the operator approves them, and a published card may break the skill's own rules -> amended in part: each draft ideal must pass `check_draft.py` with no fixes; not amended on the gate, because the operator directed that Claude draft the ideals and that the operator rewrite or approve them later, recorded by the `ideal-pending` tag and listed as a spec departure.
- Important: hard-rule graders were unspecified, and the spec's bite example rewards breaking the rule -> amended: each rule's expectation is stated, the fixed-answer checks are free `regex` graders, and the departure is recorded.
- Important: the heading regex rejected bold headings `check_draft.py` accepts -> amended: the pattern follows `_HEADING_LINE`, and the test bans only inline flag groups.
- Important: the matches-ideal rubric did not say which part of the reply to grade -> amended: every `llm` grader grades only the text under the four headings.
- Nit: the spike needs `--trust-plugin` -> amended.
- Nit: use the documented skill-fired `input_match` -> amended, and dropped from the spike.
- Nit: set `max_turns` and `timeout_seconds` -> amended, at twice the spike's observed values.
- Nit: verify `make -n eval` -> amended.
- Nit: the README install note was missing from step 3 -> amended.
- Nit: record the tag and `ideal-pending` departures -> amended.
- Nit: the year check would trip on a cited standard's year, and the `case.yaml` parser needs a fixed form -> amended: no year on citations, flow-form `case.yaml`, both in the README how-to.
