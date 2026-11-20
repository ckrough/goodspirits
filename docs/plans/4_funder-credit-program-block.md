---
title: Accept a senior program block with a funder credit
issue: 4
type: Bug
date: 2026-11-20
---

# Accept a senior program block with a funder credit

## Context

This fixes the reproduction in #4. A card whose GOOD TO KNOW ends with a senior program block on its own line, closing with a funder credit such as "Polly is supported by a grant from the Example Fund for senior dogs.", fails `check_draft.py`. The checker prints "Program name shares a line with other copy" and `RESULT: FIX: ... give the support sentence its own paragraph`. This reproduces on c954959.

The own-line check (`check_draft.py:339-345`) skips a line only when every sentence on it contains a `PROGRAM_MARKERS` entry. The funder sentence contains none, and the line runs past 25 words, so the check reports it.

The fix adds a separate `FUNDER_MARKERS` tuple ("supported by a grant from", "funded by a grant from", "made possible by a grant from") beside `PROGRAM_MARKERS` (`check_draft.py:166`). The markers name no shelter or fund. A new helper `_is_program_line` treats a line as program boilerplate only when it carries at least one `PROGRAM_MARKERS` sentence and every sentence carries a program or funder marker. Departure from the first draft, which put a bare "a grant from" into `PROGRAM_MARKERS`: review found that matched animal history prose such as "her surgery was funded by a grant from Friends of Riverside", dropping that paragraph from the word count and letting a short one bypass the banned-word checks. The issue's other option, treating the sentences after a program sentence on the same line as part of the block, is rejected. It would accept "…reimburses up to $1,500. She loves car rides.", which breaks acceptance criterion 2.

`drop_program_lines` and the own-line check both call `_is_program_line`. The Diamond Dog order check keeps `PROGRAM_MARKERS` only, so a funder credit apart from a program sentence is not flagged there. A funder credit in its own paragraph apart from a program sentence is counted as copy and not reported, since it is not part of a block and names no program. A line that mixes a program sentence with other copy is no longer dropped from the word count; the own-line check still reports it past 25 words.

Out of scope: the 25-word threshold at `check_draft.py:343` is unchanged. A short line that mixes an animal sentence with a program or funder sentence still goes unreported, as it does today for the existing markers.

## Files

- `tests/test_check_draft.py`
- `plugins/adoption-profile-writing/skills/adoption-profile-writing/scripts/check_draft.py`
- `plugins/adoption-profile-writing/skills/adoption-profile-writing/references/profile-template.md`
- `plugins/adoption-profile-writing/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `docs/plans/4_funder-credit-program-block.md`

## Work order

1. Add `test_program_block_with_funder_credit_passes` and `test_program_sentence_with_animal_sentence_fails`, `test_grant_in_animal_history_is_not_program_block`, and `test_short_history_line_with_funder_phrase_is_still_checked` (the last two added after review) to `tests/test_check_draft.py`. Commit them while the first test fails, since it reproduces the bug.
2. Make these changes, and commit when `make check` exits 0:
   - Add `FUNDER_MARKERS` and `_is_program_line`, and call the helper from `drop_program_lines` and the own-line check.
   - Change the comment at `check_draft.py:165` to "Lines naming a program, its offer, or its funder are often stripped as boilerplate by scoring tools."
   - In `profile-template.md:183`, change "names the program, its fee waiver, or its reimbursement" to "names the program, its fee waiver, its reimbursement, or the grant that funds it".
   - Bump the version from 0.4.0 to 0.4.1 in `plugin.json` and in both entries of `marketplace.json`.

## Tests

- `test_program_block_with_funder_credit_passes` inserts the issue's senior program block and funder sentence into the example card (Polly, Riverside, "Example Fund"). The block goes in as its own paragraph, before the Diamond Dog paragraph. The test expects exit 0 and no "shares a line". It fails before the fix, which proves the bug.
- `test_program_sentence_with_animal_sentence_fails` uses the same block with "She loves car rides." appended on the same line. It expects exit 1 and "shares a line", which guards acceptance criterion 2.
- `test_grant_in_animal_history_is_not_program_block` puts a long history sentence with "funded by a grant from" at the start of ABOUT THIS PET and expects no "shares a line" report.
- `test_short_history_line_with_funder_phrase_is_still_checked` puts a short history line with that phrase and banned words on its own line. It expects exit 1 and "aggressive", which proves the line is not dropped as boilerplate.

## Verification

- `make check` exits 0 and reports `Ran 10 tests` and `OK`, with `test_program_block_with_funder_credit_passes` among them.
- `make verify` exits 0.
- On step 1's commit, `python3 -m unittest tests.test_check_draft` fails only `test_program_block_with_funder_credit_passes`.

## Experiments

No experiment warranted: the reproduction was run against c954959 and failed as the issue describes, and the architect traced the fix through `check_draft.py:335-345` and `drop_program_lines`.

## Architect review

- Nit: "supported by a grant from" covers one wording only -> amended to funder markers gated on a program sentence after review found the bare marker over-matched.
- Nit: a short mixed line under 25 words goes unreported -> not amended, because the threshold is pre-existing; Context now records it as out of scope.
- Nit: the third verification bullet named no runnable file -> amended to the `make check` test count and a red check on step 1's commit.
- Nit: step 1's test name read as a leftover edit -> amended.
- Nit: no exact wording for `profile-template.md:183` and the `:165` comment -> amended in step 2.
