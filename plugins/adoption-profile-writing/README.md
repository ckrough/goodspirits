# Adoption Profile Writing

Writes the profile an adopter reads about a dog or cat in your care: the bio on your website, the kennel card, or the adoption listing. You give Claude the animal's own notes, and it writes a profile that is honest about behavior, warm to read, and built on published research about which profiles get pets adopted.

## Install

Paste this into Claude and send it:

> Please install the plugins from https://github.com/ckrough/goodspirits for me.

Claude will install it or walk you through a few clicks. The [install section](../../README.md#install) on the main page has the full steps for each app.

In Claude Code, one line does it:

```
/plugin install adoption-profile-writing --marketplace ckrough/goodspirits
```

## How to use it

1. Start a new conversation in Claude.
2. Paste in what you know about the animal: walk notes, foster notes, staff memos from your shelter's records system, or the current profile if you want it rewritten.
3. Ask, for example: "Write an adoption profile for Biscuit from these notes."

Claude writes from the notes you give it and doesn't guess. If the notes are thin, it asks you for more instead of making things up.

## What you get

A profile of about 175 to 250 words in four short sections:

- **About**: what spending time with the animal is like, told as a small scene.
- **Household fit**: kids, other pets, and the kind of home that suits them.
- **Training**: what they already know and what they're working on.
- **Good to know**: one or two honest challenges an adopter would notice, with how they're improving.

It also suggests using 3 to 5 photos. The examples use `[Name]` and `[Shelter]` as placeholders; Claude fills in your animal's name and your organization.

## Why it's written this way

The rules come from published adoption research, chiefly Markowitz (2020), which compared 676,004 Petfinder profiles of adopted and unadopted pets, and Kelling et al. (2026), which tested how 561 readers understood adoption-ad wording. Rix et al. (2021) and Archer et al. (2025) add the voice and breed-label rules. [`research-basis.md`](skills/adoption-profile-writing/references/research-basis.md) cites each study and checks the rules against the Shelter Animals Count adoptions checklist.

- **Behavior someone saw, told as a scene.** The profile describes what someone actually observed, from the side of a person spending time with the animal. It doesn't predict how the animal will act in a new home. It describes behaviors instead of labels such as "timid" or "reactive", writes in the third person, and leaves the breed to your listing's breed field.
- **One or two honest struggles.** Every profile names at least one struggle an adopter would notice and no more than two, each with where it happens or how it's improving. The rest of the record is for the shelter's history review before the meet.
- **Disclosure without alarm.** Limits on placement stay on the card. Bites, attacks, guarding that made contact, incidents with children, and harm to cats or small animals don't go on the card. Instead the card says the shelter will review the animal's history with the adopter before they meet.
- **No gatekeeping.** It cuts conditions placed on the adopter ("experienced owners only") and keeps limits on the home ("no cats"). When a narrower tag sits beside a broad one, such as "No Small Kids" beside "Good with Kids", the profile states the limit along with the yes.

## Optional: the draft checker

The plugin includes a small checker, [`check_draft.py`](skills/adoption-profile-writing/scripts/check_draft.py), that Claude runs on each draft when Python is available. It checks the headings, word count, how much of the profile covers struggles, trait words, shelter-setting words, first-person pronouns, breed words, banned phrases, and, for dogs in a Diamond Dog behavior program, the standard closing message about that program. You don't need to run it yourself, and the skill checks drafts by hand when Python isn't there.

To run it yourself, from the `skills/adoption-profile-writing` folder:

```
python3 scripts/check_draft.py path/to/draft.md
```

It exits 0 when the draft passes and 1 when it lists fixes. It needs only Python 3.

## License

Apache License 2.0. See [LICENSE](../../LICENSE).
