---
title: Write profiles as life with the animal, in adopter words
issue: 5
type: Feature
date: 2026-11-17
---

# Write profiles as life with the animal, in adopter words

## Context

This implements the 17 requirements of `docs/specs/5_life-in-adopter-words.md`. The skill teaches writers to name the setting of every behavior, but its own example sentences name it in shelter vocabulary (kennel, playgroup, quiet room, kennel door), and nothing tells the writer to lead with foster and outing notes or to frame the card as life with the dog. The change rewrites those rules and examples in adopter words and adds a review-only shelter-setting list to `check_draft.py`.

#6 resolved the spec's one flagged concern: `make check` now exists. `tests/test_check_draft.py` reads the template's `## Example` card, which this change rewrites, so the test file is in Files and gains the shelter-setting tests.

Four places the spec's acceptance greps would hit that its line list leaves out. The plan covers them so the greps return what the spec says:

- `profile-template.md:54` and `SKILL.md:152` list "a stray intake" among no-fault reasons. Both become "arriving as a stray".
- `worked-example.md:41` opens "Intake-week language comes out." It becomes "Language for a newly arrived dog comes out."
- `SKILL.md:14` says "kennel cards" in the scope sentence. It stays, under requirement 17, like the description.
- The record cells of `SKILL.md:129` ("Jumpy and mouthy in kennel") and `SKILL.md:131` ("kennel door") stay, because the record column holds the record's words.
- `references/sourcing-behavior-facts.md:19` keeps "intake". It is outside the spec's files, and it tells the writer how to read the record, so it is not copy that gets published. `worked-example.md:41` is rewritten anyway, because the spec's acceptance grep covers that whole file.

`.claude-plugin/marketplace.json` carries the plugin version twice (top level and the plugin entry). Every earlier release bumped both with `plugin.json`, so all three go to `0.4.0`.

## Files

- `plugins/adoption-profile-writing/skills/adoption-profile-writing/scripts/check_draft.py`
- `tests/test_check_draft.py`
- `plugins/adoption-profile-writing/skills/adoption-profile-writing/references/profile-template.md`
- `plugins/adoption-profile-writing/skills/adoption-profile-writing/SKILL.md`
- `plugins/adoption-profile-writing/skills/adoption-profile-writing/references/worked-example.md`
- `plugins/adoption-profile-writing/skills/adoption-profile-writing/references/research-basis.md`
- `README.md`
- `plugins/adoption-profile-writing/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

## Work order

Steps 2, 3, and 4 start after step 1 commits. Each parallel step stages and commits only the files it owns. If they share one worktree, run them one after another.

1. **Checker and its tests.** Commit when `make check` exits 0.
   - In `check_draft.py`, add `SHELTER_SETTING_WORDS` beside `POSITIVE_TRAIT_LABELS`: `kennel`, `kennel door`, `kennel fence`, `dog run`, `play yard`, `playgroup`, `quiet room`, `intake`, `adoption floor`. Give it a comment naming the source (Humane World for Animals, 2025, p. 19, "Avoid shelter jargon") and saying the list is for review and never fails a draft.
   - Add `shelter_setting_hits(text: str) -> list[str]`. It lowercases the text and walks the terms longest first. For each term it collects one entry per match of `\b<escaped term>s?\b`, then replaces those matches with a space before the shorter terms run, the same way `main()` strips denials before negative words.
   - In `main()`, right after the positive-trait-label line, print `Shelter-setting words (review: name the setting in adopter words): <hits or 'none'>`. Nothing is added to `problems`.
   - Add the list to the docstring's Checks paragraph as "shelter place and routine words (listed for review, not failed)".
   - In `tests/test_check_draft.py`, add `test_shelter_setting_hits`. It runs the helper on "kennel door, kennels, kennel fence, playgroups, play yard, quiet room, intake, adoption floor, dog runs, runs, run, shelter, at the shelter, in a group of dogs". It asserts that the sorted result equals `['adoption floor', 'dog run', 'intake', 'kennel', 'kennel door', 'kennel fence', 'play yard', 'playgroup', 'quiet room']`. That proves plurals match, a longer term blocks its shorter one, and run, runs, shelter, and the two plain phrases are never reported.
   - Add `test_shelter_setting_words_do_not_fail`. It inserts "She naps in the quiet room by the kennel door." under ABOUT THIS PET in the example card and asserts that the exit code is 0. It also asserts that a stdout line starting `Shelter-setting words (review:` contains `'kennel door'` and `'quiet room'`.
2. **Template.** This runs after step 1 and in parallel with steps 3 and 4. Commit when `make check` exits 0.
   - Line 54: "a stray intake" becomes "arriving as a stray".
   - Line 73: the examples become "in a group of dogs, on leash, at the shelter, or living in a home."
   - Rewrite the example card. The facts, the page address line, the support sentence, and the closing lines stay as they are, and so does the Diamond Dog message, character for character:
     - ABOUT THIS PET opens "On a couch at the shelter, [Name] stretches out beside whoever is reading and rests her chin on their knee." and ends "After walks, she carries a stuffed toy back inside with her."
     - HOUSEHOLD FIT opens "In groups of dogs at the shelter, [Name] plays chase with dogs her size,".
     - TRAINING reads "She waits at her door until her walker says "okay,"".
     - GOOD TO KNOW reads "mostly when she greets people at her door, and it eases once she is out walking."
   - "What it shows": the household bullet's settings become "groups of dogs at the shelter, on leash". Add one bullet saying the card tells shelter observations as life with her, the common case when a record has no foster notes.
   - Line 221: set the word and struggle counts from a checker run on the card with Polly and Riverside filled in, the one-word names the sentence describes.
   - In `tests/test_check_draft.py`, add `test_example_card_has_no_shelter_setting_words`. It asserts that the example card's stdout contains `Shelter-setting words (review: name the setting in adopter words): none`.
3. **`SKILL.md`.** This runs after step 1 and in parallel with steps 2 and 4. Commit when `make check` exits 0.
   - Under the "Plain words, not clinical ones" table, add one paragraph. It says shelter place and routine names (kennel, run, play yard, playgroup, quiet room, intake, and the shelter's own location names) are shelter vocabulary, citing Humane World for Animals (2025) p. 19, "Avoid shelter jargon". It also says the card still names where each behavior was seen, in adopter words, because the observation-not-prediction rule depends on the setting.
   - After that paragraph, add the second table, copying every row of the spec's Design table word for word, with both columns as the spec gives them.
   - Fix the published column of line 129 to "The jumping mostly happens at the shelter".
   - Rewrite lines 41, 115, 162, 163, 204, and 205 with the spec's adopter phrases, adjusting the words around each phrase so the sentence reads well:
     - 115 becomes "has played well with larger dogs at the shelter".
     - 205 becomes "wrestles and chases with other dogs" and "lively with other dogs, wrestling and chasing".
   - Also and change line 152's "a stray intake" to "arriving as a stray".
   - Add three sentences to the "Show what being with the animal is like" bullet:
     - The card is a narrative that answers "what would it be like to live with this animal."
     - When the record has foster-home or outing observations (car rides, events, time alone, crate, household routines), lead with them. Cite Humane World for Animals (2025) p. 24, with one illustrative sentence marked as an example: "In her foster home she rides quietly in the car and settles in her crate while the family is out."
     - Most records have none. The card then tells the shelter observations in adopter words as life with the dog and never invents a home scene. The existing trace-to-the-record sentence stays.
   - Line 208: "the table above" becomes "the tables above".
   - In "Before you return", add a new step 8 ahead of the checker step: reread each setting on the card for shelter place and routine names, including the shelter's own location names, which the checker cannot catch, and rewrite them with the second table. The checker step becomes step 9. Its output list adds "shelter-setting words (listed for review)", and the References table's "Before you return" step 8 becomes step 9.
4. **The other references, README, and versions.** This runs after step 1 and in parallel with steps 2 and 3. Commit when `make check` exits 0.
   - `worked-example.md`:
     - Line 10 becomes "plays well with smaller dogs at the shelter".
     - Line 23 changes only "in playgroup", giving "plays in groups of dogs at the shelter".
     - Rewrite line 41 as Context gives.
   - `research-basis.md` line 26: change "sleeps through the kennel noise" to "sleeps through the barking around him". Then add a paragraph headed "Adopter words and the foster-and-outing lead" after "The takeaway". It records both rules as editorial decisions resting on practitioner guidance, Humane World for Animals (2025) p. 19 ("Avoid shelter jargon") and p. 24 (foster and outing observations), with no outcome study behind either.
   - `README.md` line 28: add "shelter-setting words (for review)" to the list of what the checker checks.
   - Set the version in `plugin.json` and both versions in `marketplace.json` to `0.4.0`.

## Tests

`tests/test_check_draft.py` grows from 3 tests to 6:

- `test_shelter_setting_hits`: the helper lists each shelter term once, matches plurals, never reports a shorter term inside a longer one, and ignores run, runs, shelter, "at the shelter", and "in a group of dogs" (requirements 9 and 11).
- `test_shelter_setting_words_do_not_fail`: a card with shelter words still exits 0 and lists them on the review line (requirement 10).
- `test_example_card_has_no_shelter_setting_words`: the rewritten example reports `none` (requirement 13).

The three existing tests keep passing against the rewritten example, which proves it still passes the checker, with the Diamond Dog message intact.

## Verification

- `make check` exits 0, reporting `Ran 6 tests` and `OK`, and ruff reports `All checks passed!`.
- `make verify` exits 0, with both `claude plugin validate` runs printing `Validation passed`.
- `grep -n -iE "kennel|playgroup|play yard|quiet room|intake"` on `SKILL.md`, `references/profile-template.md`, `references/worked-example.md`, and `references/research-basis.md` returns only the following:
  - `SKILL.md`: lines 3 and 14 ("kennel cards"), the rule paragraph, the new table's record column, the record cells on lines 129 and 131, and the new step 8.
  - `profile-template.md`: line 3.
  - `worked-example.md`: nothing.
  - `research-basis.md`: line 93 ("kennel cards") and the new paragraph's mention of the list.
- Each "What gets published" cell of the new `SKILL.md` table, run through `shelter_setting_hits`, returns `[]` (requirement 2).
- `git diff main -- plugins` adds no em-dash (`grep -c "—"` on added lines is 0), adds no non-stdlib `import`, and deletes no disclosure-rule sentence.
- The Diamond Dog message in the example matches `profile-template.md` lines 138-142 character for character.
- `sh "/Users/ckrough/.claude/plugins/cache/backchain/daedalus/12.3.1/scripts/daedalus.sh" check-docs` reports 0 problems.

## Experiments

No experiment warranted: the checker's matching behavior is settled by the new unit tests in step 1, and every other claim is a line number or string read directly from the repository.

## Architect review

- Important: the Verification grep list left out the record cell on `SKILL.md:129`, which still matches "kennel" -> amended. The cell is now in Verification and in Context.
- Nit: the grep target was not named, and `sourcing-behavior-facts.md` keeps "intake" while `worked-example.md:41` changes -> amended. The grep names the four files, and Context explains both choices.
- Nit: the spec describes the new rule paragraph without giving its text, and the shortened table rows contradicted "word for word" -> amended. Step 3 lists what the paragraph must contain and copies the spec's table rows whole.
- Nit: on `worked-example.md:23`, replacing "plays in playgroup" dropped the verb -> amended. Only "in playgroup" is replaced.
- Nit: the spec's phrases read awkwardly inside lines 115, 205, and 10 and in the template's GOOD TO KNOW -> amended. The surrounding words change so each sentence reads well, and line 221 is measured from the final card.
- Nit: requirement 2 had no verification -> amended. A Verification bullet runs each published cell through the helper.
- Nit: steps 3 and 4 could commit before the checker prints the new line, and parallel steps sharing a worktree would run `make check` on each other's half-done edits -> amended. All three start after step 1, and each stages only its own files.
