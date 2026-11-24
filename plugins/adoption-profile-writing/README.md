# adoption-profile-writing

A Claude skill that writes and rewrites adoptable-pet profiles (bios, kennel cards, listings) from the animal's own record.

To install it, follow the [install steps in the main README](../../README.md#install).

## Using it

Ask Claude to write a profile and paste in what you know about the animal: the intake notes, behavior notes, tags, and anything staff or volunteers have observed. For example, "Write an adoption profile for this dog" followed by the record. The skill loads on its own.

The result is a profile in four sections: ABOUT, HOUSEHOLD FIT, TRAINING, and GOOD TO KNOW.

## What the skill does

The skill drafts a profile in four sections. Its rules come from published adoption research, chiefly Markowitz (2020), which compared 676,004 Petfinder profiles of adopted and unadopted pets, and Kelling et al. (2026), which tested how 561 readers understood adoption-ad wording. Rix et al. (2021) and Archer et al. (2025) add the voice and breed-label rules. `skills/adoption-profile-writing/references/research-basis.md` cites each study and checks the rules against the Shelter Animals Count adoptions checklist.

- **Observed behavior, told as a scene.** It describes behavior that someone observed, from the side of a person spending time with the animal, and it does not predict how the animal will act in a new home. It writes behaviors rather than trait labels such as "timid" or "reactive", always in the third person, and leaves the breed to the attribute panel.
- **One or two light struggles.** Every card names at least one struggle an adopter would notice and no more than two, each with where it happens or how it is improving. The rest of the record goes to the shelter's history review before the meet.
- **Disclosure without alarm.** Placement constraints stay on the card. Bites, attacks, guarding that made contact, incidents with children, and harm to cats or small animals do not go on the card. Instead the card says the shelter will review the animal's history with the adopter before they meet.
- **No gatekeeping.** It cuts conditions placed on the applicant ("experienced owners only") and keeps limits on the home ("no cats"). When a tag narrows a broad one, such as "No Small Kids" beside "Good with Kids", the card states the limit with the yes.
- **Measured length.** It targets 175 to 250 words and 3 to 5 photos.

The profile examples use `[Name]` and `[Shelter]` placeholders. Replace them with your animal and your organization.

## Optional draft checker

`skills/adoption-profile-writing/scripts/check_draft.py` checks a draft's headings, word count, struggle share, trait words, shelter-setting words (for review), first-person pronouns, breed words, banned phrases, and the Diamond Dog message. It needs only the Python 3 standard library, and the skill works without it:

```
python3 scripts/check_draft.py path/to/draft.md
```

Run it from the skill folder. It exits 0 when the draft passes and 1 when it lists fixes.
