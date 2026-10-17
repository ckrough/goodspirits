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

The skill drafts a profile in four sections: ABOUT, HOUSEHOLD FIT, TRAINING, and GOOD TO KNOW. Its rules come from published adoption research, chiefly Markowitz (2020), which compared 676,004 Petfinder profiles of adopted and unadopted pets, and Kelling et al. (2026), which tested how 561 readers understood adoption-ad wording. `references/research-basis.md` cites both.

- **Observed behavior, told as a scene.** It describes behavior that someone observed, from the side of a person spending time with the animal, and it does not predict how the animal will act in a new home. It writes behaviors rather than trait labels such as "timid" or "reactive".
- **One or two light struggles.** Every card names at least one struggle an adopter would notice and no more than two, each with where it happens or how it is improving. The rest of the record goes to the shelter's history review before the meet.
- **Disclosure without alarm.** Placement constraints stay on the card. Bites, attacks, guarding that made contact, incidents with children, and harm to cats or small animals do not go on the card. Instead the card says the shelter will review the animal's history with the adopter before they meet.
- **No gatekeeping.** It cuts conditions placed on the applicant ("experienced owners only") and keeps limits on the home ("no cats").
- **Measured length.** It targets 175 to 250 words and 3 to 5 photos.

`scripts/check_draft.py` checks a draft's headings, word count, struggle share, trait words, banned phrases, and the Diamond Dog message. It needs only the Python 3 standard library:

```
python3 scripts/check_draft.py path/to/draft.md
```

Run it from the skill folder. It exits 0 when the draft passes and 1 when it lists fixes.

The profile examples use `[Name]` and `[Shelter]` placeholders. Replace them with your animal and your organization.

## License

Apache License 2.0. See [LICENSE](LICENSE) for the full text.

Copyright (C) 2026 Chris Krough
