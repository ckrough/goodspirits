# goodspirits

A Claude Code plugin marketplace for animal-rescue work. I volunteer with a shelter, and these are the tools I built for that work, generalized so any rescue can use them.

## Install

```
/plugin marketplace add ckrough/goodspirits
/plugin install adoption-profile-writing@goodspirits
```

## Plugins

| Plugin | What it does |
|---|---|
| [adoption-profile-writing](plugins/adoption-profile-writing/) | Writes and rewrites adoptable-pet profiles (bios, kennel cards, listings) from the animal's own record. |

### adoption-profile-writing

The skill drafts a profile in four sections: ABOUT, HOUSEHOLD FIT, TRAINING, and GOOD TO KNOW. Its rules come from published adoption research, chiefly Markowitz (2020), which compared 676,004 Petfinder profiles of adopted and unadopted pets, and Kelling et al. (2026), which tested how 561 readers understood adoption-ad wording. Rix et al. (2021) and Archer et al. (2025) add the voice and breed-label rules. `references/research-basis.md` cites each study and checks the rules against the Shelter Animals Count adoptions checklist.

- **Observed behavior, told as a scene.** It describes behavior that someone observed, from the side of a person spending time with the animal, and it does not predict how the animal will act in a new home. It writes behaviors rather than trait labels such as "timid" or "reactive", always in the third person, and leaves the breed to the attribute panel.
- **One or two light struggles.** Every card names at least one struggle an adopter would notice and no more than two, each with where it happens or how it is improving. The rest of the record goes to the shelter's history review before the meet.
- **Disclosure without alarm.** A household limit shows on the card as the behavior behind it ("when he sees a child, he tucks his tail and tries to get away"), leaving the reader to judge their own home; the limit itself is stated only when its sole source is an incident held back or nothing in the record bears on it. A bare tag with a related behavior on record gets the behavior, not the limit. Bites, attacks, guarding that made contact, incidents with children, and harm to cats or small animals do not go on the card. Instead the card says the shelter will review the animal's history with the adopter before they meet.
- **No gatekeeping.** It cuts conditions placed on the applicant ("experienced owners only") and keeps limits on the home ("no cats"). When a tag narrows a broad one, such as "No Small Kids" beside "Good with Kids", the card states the limit with the yes.
- **Measured length.** It targets 175 to 250 words and 3 to 5 photos.

`scripts/check_draft.py` checks a draft's headings, word count, struggle share, trait words, shelter-setting words (for review), first-person pronouns, breed words, banned phrases, and the Diamond Dog message. It needs only the Python 3 standard library:

```
python3 scripts/check_draft.py path/to/draft.md
```

Run it from the skill folder. It exits 0 when the draft passes and 1 when it lists fixes.

The profile examples use `[Name]` and `[Shelter]` placeholders. Replace them with your animal and your organization.

#### Evals

The plugin carries an eval suite under `plugins/adoption-profile-writing/evals/`, run by Claude Code's built-in `claude plugin eval`. Each case gives the skill one anonymized shelter record and asks for a profile, then scores the draft against an ideal profile written for that record, plus graders for the rules the record tests: a bite kept off the card, a placement limit stated as a limit on the home, and a record whose later entries overrule its earlier ones. Every case also runs without the skill, so the report shows each case's score with the skill, without it, and the difference.

```
make eval          # run every case once per writer model (paid model calls; run outside the Claude sandbox)
make eval-record   # write each model's summary from the newest sweep to evals/history/, for committing
```

`make eval-record` refuses when the plugin has uncommitted changes, so each committed summary names the commit of the skill it scored. The skill pins `model: claude-sonnet-5-5` in its frontmatter, so it runs on Sonnet 5.5 whatever the session model, and a sweep writes with Sonnet 5.5 to match; `MODELS="<model ...>"` adds other writers for comparison. The baseline sweep showed Haiku, Sonnet, and Opus 5.5 within a few points of each other on every case, so the skill, not the model, is what limits the card. Every run is judged by `claude-opus-5-5`, a stronger model than the writer, unless `JUDGE_MODEL=<model>` is given, and each summary records both models. Sweeps judged by Sonnet 5.5, the baseline included, do not compare with Opus-judged ones. A score is a signal to read per case, not a verdict: the judge is a Claude model grading a Claude draft, and four cases cannot show a small difference between two versions of the skill.

A marketplace install copies the whole plugin folder, so `evals/` ships with it. The cases are de-identified.

To add a case, create `evals/case-<pseudonym>/` with:

- `resources/record.md`: the record, de-identified, opening with a `Listing attributes:` block (Kids, Dogs, Cats, as the shelter's listing shows them). No real name of an animal or a person, no shelter ID, address, or calendar date; dates become days, weeks, or months from intake. No year anywhere in the case, citations included.
- `deidentification.md`: each change, named by its ISO/IEC 20889 technique (pseudonymization, generalization, or suppression).
- `ideal.md`: the ideal profile, passing `check_draft.py`. Two ideals run over its 250-word band and are kept: `case-clover` is the operator's published Description with its HOUSEHOLD FIT corrected against the record (29 over), and `case-marlow` carries two program blocks and an opening section the operator approved at that length (18 over).
- `case.yaml`: `schema_version: "1.1"`, `name`, `tags: [..]` in flow form (`bite`, `placement-constraint`, `changed-record`, `tag-conflict`, `foster-notes`, and `ideal-pending` until the ideal is approved), and `context: scaffold_script: fixture.sh`.
- `fixture.sh`, copied unchanged from another case: it copies `resources/` into the run's workspace.
- `prompt.md`: the request, asking for the profile saved to `profile.md`.
- `graders/`: copy the shared graders unchanged from another case (`profile-saved`, `skill-fired`, the four headings, and the `rubric-*` graders: regexes carrying the FOHA profile grader's lexicons for first-person voice, social words, adopter screening, and absolute claims, and judge graders for its register, concreteness, observed-not-promised, opening and flow, struggle balance, and length dimensions), then paste the ideal into `matches-ideal.md` and list under it the 3 to 5 required facts a card must state; the ideal's other facts are optional. Copy `record-fidelity.md` from another case and replace everything after "The record:" with the new record, so the judge can fail a card that says what the record does not. Add a grader per rule the record tests.

`tests/test_evals.py`, part of `make check`, checks each case's files, tags, and graders, that the shared graders are identical in every case, that each ideal passes its case's regex graders, that `matches-ideal.md` embeds `ideal.md`, that `record-fidelity.md` ends with `record.md` under the same instructions in every case, and that no case holds a calendar date.

## License

Apache License 2.0. See [LICENSE](LICENSE) for the full text.

Copyright (C) 2026 Chris Krough
