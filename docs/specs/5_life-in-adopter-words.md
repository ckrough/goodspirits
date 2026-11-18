---
title: Write profiles as life with the animal, in adopter words
issue: 5
date: 2026-11-17
---

# Write profiles as life with the animal, in adopter words

## Requirements

1. `SKILL.md` "Plain words, not clinical ones" states that shelter place and routine names (kennel, run, play yard, playgroup, quiet room, intake, the shelter's own location names) are shelter vocabulary, and that the card still names where a behavior was seen, in adopter words.
2. A second table, directly under the existing behavior-jargon table in that section, maps each shelter place or routine name to adopter words. No entry in its "What gets published" column contains a term from the checker's shelter-setting list (requirement 9).
3. `SKILL.md` "Show what being with the animal is like" says the card is a narrative that answers "what would it be like to live with this animal."
4. The same bullet tells the writer to lead with foster-home and outing observations (car rides, events, time alone, crate, household routines) when the record has them.
5. The same bullet says most records have no foster notes, and that the card is then built from the shelter observations, told in adopter words as life with the dog, with no invented home scene. The existing trace-to-the-record sentence stays.
6. Every example sentence in `SKILL.md` that models published copy uses adopter words. A setting a disclosure needs is written in plain words ("at the shelter," "in a group of dogs"). The specific lines are 41, 115, 129, 162, 163, 204, and 205.
7. `references/profile-template.md` line 73 gives adopter-word settings as its examples, and the worked example (lines 190-207) plus its "What it shows" notes (lines 209-215) use adopter words, with the Diamond Dog message word for word. The example stays on shelter observations told as life with the dog, the common case; the foster-led illustration lives in the `SKILL.md` bullet (requirement 4).
8. `references/worked-example.md` lines 10 and 23 and the "kennel noise" example in `references/research-basis.md` line 26 use adopter words.
9. `check_draft.py` has a `SHELTER_SETTING_WORDS` list holding `kennel`, `kennel door`, `kennel fence`, `dog run`, `play yard`, `playgroup`, `quiet room`, `intake`, and `adoption floor`. Each entry also matches its plural, so `dog run` covers "dog runs."
10. `check_draft.py` prints a "Shelter-setting words (review: ...)" line listing every hit, adds nothing to `problems`, and leaves the exit status unchanged. A longer listed term is not reported a second time as a shorter one ("kennel door" is not also reported as "kennel").
11. The checker does not report a bare "run" or "runs" or "shelter," or the phrases "at the shelter" and "in a group of dogs."
12. `SKILL.md` "Before you return" adds a check to reread every setting for shelter place and routine names, including the shelter's own location names, which the checker cannot catch. Step 8's list of checker output names the new review line.
13. The rewritten template example passes `check_draft.py`, its shelter-setting line reads `none`, and `references/profile-template.md` line 221 states the word and struggle counts the checker reports.
14. `references/research-basis.md` records the shelter-vocabulary rule and the foster-and-outing lead as editorial decisions resting on practitioner guidance, citing Humane World for Animals (2025) p. 19 and p. 24.
15. The README's list of checker checks and the `check_draft.py` docstring name the shelter-setting review list.
16. `plugin.json` version is `0.4.0`.
17. "Kennel card" is unchanged in the `SKILL.md` description, the README, and `plugin.json`. No disclosure rule is relaxed, the checker stays standard-library only, and no new prose carries an em-dash.

## Design

The change touches six files in one plugin and introduces no new module, dependency, or interface.

**`SKILL.md`, rules.** The "Plain words, not clinical ones" section gains one paragraph after its existing table. It names shelter place and routine words as shelter vocabulary, cites Humane World (2025) p. 19 ("Avoid shelter jargon"), restates that the setting still gets named because the observation-not-prediction rule depends on it, and introduces a second table:

| The record's words | What gets published |
|---|---|
| in playgroup, shelter playgroups | in a group of dogs, played in groups with other dogs |
| the play yards | a fenced yard |
| comes out of her kennel | as the leash goes on, on the way out for a walk |
| in his kennel, at the kennel | at the shelter |
| kennel door | when someone comes to her door |
| kennel fence, run fence | through a fence at the shelter |
| quiet room | a room with a couch |
| intake, at intake | when she arrived, her first weeks at the shelter |
| [the shelter's own location names] | the plain description of the place |

The "Show what being with the animal is like" bullet in Language rules gets three sentences. The first names the card as a narrative of life with the animal. The second says to lead with foster-home and outing observations when the record has them, citing Humane World (2025) p. 24. The third says most records have none, so the card tells the shelter observations in adopter words as life with the dog and never invents a home scene. The `SKILL.md:208` bullet "Plain vocabulary over shelter vocabulary. See the table above." becomes "the tables above."

**`SKILL.md`, examples.** Seven lines are rewritten in place, each keeping its fact:

- 41: "mostly in his kennel" becomes "mostly at the shelter".
- 115: "in playgroup" becomes "in groups of dogs".
- 129: "mostly happens in his kennel at the shelter" becomes "mostly happens at the shelter".
- 162: "guards his bowl at the kennel" becomes "guards his bowl at the shelter".
- 163: "through the kennel fence" becomes "through a fence at the shelter".
- 204: "sleeps through the kennel noise" becomes "sleeps through the barking around him".
- 205: "wrestles and chases in playgroup" and "lively in playgroup" become "with other dogs".

**`SKILL.md`, checks.** "Before you return" gets a new step, placed before the checker step: reread each setting for shelter place and routine names, including the shelter's own. The checker step's list of output gains "shelter-setting words (listed for review)".

**`references/profile-template.md`.** Line 73's examples become "in a group of dogs, on leash, at the shelter, or living in a home." The worked example drops "the shelter's quiet room," "her kennel," "shelter playgroups," and "the kennel door" for adopter words, keeping the same invented facts and the Diamond Dog message unchanged. It models the shelter-only path, and the `SKILL.md` bullet carries a foster-led example sentence. The "What it shows" bullet naming "playgroups, on leash" follows. Line 221 is set from a checker run on the rewritten example.

**`references/worked-example.md` and `references/research-basis.md`.** The card line and its annotation at worked-example lines 10 and 23 change "the shelter playgroup" to "groups of dogs at the shelter." Research-basis line 26 takes the same rewrite as `SKILL.md:204`. A new paragraph in research-basis records both rules as editorial decisions resting on Humane World (2025) p. 19 and p. 24, with no outcome study behind either.

**`scripts/check_draft.py`.** A new module-level `SHELTER_SETTING_WORDS` list sits beside `POSITIVE_TRAIT_LABELS`, with a comment giving the source. A small helper matches each term longest first with an optional trailing `s` (`\b<term>s?\b`) and blanks each match out of the working text before trying shorter terms, the same way trait denials are removed before negative trait words. `main()` prints the hits right after the positive-trait-label line and never appends to `problems`. Neither "run" nor "runs" is in the list, and neither is "shelter", so ordinary verbs and the required history-review line produce no hits. The docstring's Checks paragraph gains the list.

**README and `plugin.json`.** The README sentence listing what the checker checks adds "shelter-setting words (for review)". `plugin.json` goes from `0.3.0` to `0.4.0`.

## Decisions applied

- None. The repository has no `docs/decisions/`. The design adds no storage, dependency, external interface, or architectural pattern, so it records no ADR.

## Flagged concerns

- The repository has no test suite or `make check` target, so the acceptance tests are checker runs on short draft files, recorded in the plan. `/daedalus:ship` expects `make check`, so the plan will need to say how it proceeds without one.

## Acceptance tests

- Requirement 1: Read `SKILL.md` "Plain words, not clinical ones" and confirm it names the listed place and routine words and says the setting is still named.
- Requirement 2: The second table sits directly under the first. Running every "What gets published" cell through `check_draft.py`'s matcher returns no shelter-setting hits.
- Requirements 3-5: Read the "Show what being with the animal is like" bullet and confirm the narrative sentence, the foster-and-outing lead with its examples, the no-foster-notes path, and the trace-to-the-record sentence.
- Requirement 6: `grep -n -iE "kennel|playgroup|play yard|quiet room|intake" SKILL.md` returns only the rule text, the new table's record column, the skill description's "kennel cards," and "Before you return."
- Requirement 7: The same grep on `references/profile-template.md` returns only the "kennel cards" mention in its first line, and the Diamond Dog message in the example matches lines 138-142 character for character.
- Requirement 8: The same grep on `references/worked-example.md` and line 26 of `references/research-basis.md` returns nothing.
- Requirements 9-11: A draft whose prose contains "kennel door," "kennels," "playgroups," "play yard," "quiet room," "intake," "adoption floor," "dog runs," "runs," "run," "shelter," "at the shelter," and "in a group of dogs" makes the checker list each listed term once, with "kennel door" not also listed as "kennel," and nothing for "run," "runs," "shelter," or the two plain phrases. The exit status matches the same draft with that line removed.
- Requirement 12: Read "Before you return" and confirm the new reread step and the updated checker-output list.
- Requirement 13: Save the template example to a file, run `python3 scripts/check_draft.py` on it, and confirm PASS, a shelter-setting line of `none`, and that the narrative and struggle word counts match line 221.
- Requirement 14: Read `references/research-basis.md` and confirm the editorial-decision paragraph cites Humane World (2025) p. 19 and p. 24.
- Requirement 15: Read the README and the `check_draft.py` docstring for the shelter-setting review list.
- Requirement 16: `grep '"version"' plugins/adoption-profile-writing/.claude-plugin/plugin.json` shows `0.4.0`.
- Requirement 17: `git diff main -- plugins` shows "kennel cards" untouched in the description, README, and `plugin.json`, no new `import` outside the standard library in `check_draft.py`, no em-dash added, and no deleted disclosure-rule sentence.
