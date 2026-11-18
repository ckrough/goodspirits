---
title: Write profiles as life with the animal, in adopter words
issue: 5
date: 2026-11-17
---

# Write profiles as life with the animal, in adopter words

## Problem

The adoption-profile-writing skill tells writers to "show what being with the animal is like," but its own guidance and examples point them toward shelter settings and shelter vocabulary. A draft that follows the skill closely reads as a tour of the shelter's routines rather than a picture of the animal in the reader's home.

A rewrite that passed `check_draft.py` with no findings still used "the play yards," "playgroup," and "comes out of her kennel." The reviewer said adopters don't know what those are, because they belong to the shelter, and asked for copy that shows what living with the dog would be like. The revision kept every fact, rewrote the settings in adopter terms ("a fenced yard," "played in groups with other dogs," "as the leash goes on"), and led with the foster-home notes and the outings.

The skill pulls the other way in four places:

- `references/profile-template.md` line 73 gives "in playgroup, on leash, at the kennel" as its example settings.
- The worked example in `references/profile-template.md` (lines 193-202) uses "the shelter's quiet room," "her kennel," "shelter playgroups," and "the kennel door."
- `SKILL.md` examples use "mostly in his kennel" (line 41), "in playgroup" (lines 115, 205), "kennel noise" (line 204), and "kennel fence" (line 163). `references/worked-example.md` (lines 10, 23) and `references/research-basis.md` (line 26) repeat the same vocabulary.
- "Plain words, not clinical ones" covers behavior jargon ("reactivity," "barrier frustration") but says nothing about the shelter's place and routine names, and "Show what being with the animal is like" does not say to prefer foster and outing observations.

Most dogs have no foster notes, so most cards are built from shelter observations alone. The skill gives no guidance for telling those as life with the dog.

## Outcome

A writer following the skill produces a card that reads as a narrative answering "what would it be like to live with this animal," in words an adopter knows. Shelter place and routine names are translated by a table in `SKILL.md`, the setting of each behavior is still named, foster-home and outing observations lead when the record has them, and a card without them is built from shelter observations told in plain language. Every example in the skill models this, and `check_draft.py` lists shelter-setting nouns for review without failing the draft.

## Constraints

- `check_draft.py` stays standard-library Python only (`check_draft.py` docstring, README).
- The checker lists shelter-setting nouns for review and never fails a draft on them; exit status is unchanged, following the `POSITIVE_TRAIT_LABELS` pattern (issue #5 acceptance criterion 5, `check_draft.py` lines 74-76 and 289).
- A card still names where each behavior was seen, because the observation-not-prediction rule depends on it (`SKILL.md` "Disclose the observation, not the prediction", `references/profile-template.md` line 73).
- Every detail in a rewritten example or a foster or outing lead traces to the record: no added details, no joining separate observations into one scene, and no invented home scene when the record has no foster notes (`SKILL.md` line 202 and "Before you return" step 7, operator requirement).
- Examples keep the `[Name]` and `[Shelter]` placeholders (`SKILL.md` line 10, README).
- The Diamond Dog message stays word for word in the rewritten template example (`references/profile-template.md` lines 136-142, `check_draft.py`).
- No em-dashes in new prose (`SKILL.md` line 214).
- The template example's stated counts (226 words, 38 in struggles) are re-measured with the checker after the rewrite and corrected (`references/profile-template.md` line 221).
- The README's list of what the checker checks is updated (README, global docs rule).
- The plugin version goes from 0.3.0 to 0.4.0 (each prior skill change bumped it, git log of `plugin.json`).
- `references/worked-example.md` lines 10 and 23 and `references/research-basis.md` line 26 are rewritten in adopter terms, so no reference file contradicts the new rule (consistency across the skill).
- The review list does not flag "shelter" or the plain settings the issue allows ("at the shelter," "in a group of dogs"), because the required history-review line and `[Shelter]` carry the word (issue #5 acceptance criterion 3, `SKILL.md` line 70).
- The shelter-vocabulary rule cites Humane World for Animals (2025) p. 19 ("Avoid shelter jargon and write clearly"), and the foster-and-outing lead cites p. 24 ("Prioritize photos and videos of the pet ... in a home environment"; foster and off-site outings to document personality) (`references/research-basis.md`, operator-supplied handbook).
- The narrative lead does not relax any disclosure rule: a home-life opening may not stage a struggle at the tail of a gentle sentence or spin a limit into a compliment (`SKILL.md` lines 87-93, Best Friends Animal Society "Write compelling adoption bios").
- `references/research-basis.md` records both new rules as editorial decisions resting on practitioner guidance, not research findings (`references/research-basis.md`, `SKILL.md` line 46).
- "Kennel card" stays unchanged in the `SKILL.md` description, the README, and `plugin.json`: the change governs profile prose, not internals (operator requirement).

## Open questions

None.

## Acceptance criteria

- "Plain words, not clinical ones" in `SKILL.md` also covers shelter place and routine names (kennel, run, play yard, playgroup, quiet room, intake, the shelter's own location names), with a second table, placed directly under the existing behavior-jargon table, mapping each one to adopter words, and still names where a behavior was seen.
- "Show what being with the animal is like" says the card is a narrative that answers "what would it be like to live with this animal," and tells the writer to lead with foster-home and outing observations (car rides, events, time alone, crate, household routines) when the record has them. Every detail still traces to the record.
- "Show what being with the animal is like" says most records have no foster notes, and that the card is then built from the shelter observations, told in adopter words as life with the dog, with no invented home scene.
- The worked example in `references/profile-template.md` and the examples in `SKILL.md` are rewritten in adopter terms, with no shelter place names except where a disclosure needs the setting, and then in plain words ("at the shelter," "in a group of dogs").
- Line 73 of `references/profile-template.md` lists adopter-word settings as its examples.
- `references/worked-example.md` lines 10 and 23 and the "kennel noise" example in `references/research-basis.md` line 26 are rewritten in adopter terms.
- `check_draft.py` reports shelter-setting nouns for review, the way it lists positive trait labels, without failing the draft.
- The checker's review list holds `kennel`, `kennel door`, `kennel fence`, `dog run`, `runs`, `play yard`, `playgroup`, `quiet room`, `intake`, and `adoption floor`, and does not flag a bare "run," "shelter," "at the shelter," or "in a group of dogs."
- "Before you return" in `SKILL.md` adds a check to reread every setting for shelter place and routine names, including the shelter's own location names, which the checker cannot catch.
- The rewritten template example passes `check_draft.py`, its shelter-setting review list is empty, and the word and struggle counts on `references/profile-template.md` line 221 match the checker's output.
- `references/research-basis.md` records both new rules as editorial decisions and cites Humane World for Animals (2025) p. 19 and p. 24.
- The README's list of checker checks names the shelter-setting review list.
- `plugin.json` version is 0.4.0.
