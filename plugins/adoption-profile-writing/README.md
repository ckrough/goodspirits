# Adoption Profile Writing

Writes the profile an adopter reads about a dog or cat in your care: the bio on your website, the kennel card, or the adoption listing. You give Claude the animal's own notes, and it writes a profile that is honest about behavior, warm to read, and built on published research about which profiles get pets adopted.

## Install

In the Claude desktop app:

1. Open **Customize** in the sidebar, then choose **Plugins**.
2. Choose **Add**, then **Add marketplace**.
3. Type `ckrough/goodspirits` and confirm.
4. Find **Adoption Profile Writing** in the list (under **Discover**) and choose **Add**.

Or paste this into Claude and it will walk you through those steps:

> Please help me install the plugins from https://github.com/ckrough/goodspirits.

The [main page](https://github.com/ckrough/goodspirits#install) has more help if a step doesn't work.

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
- **Good to know**: honest challenges an adopter would notice, with how they're improving. The whole profile names one or two, wherever they fit best.

It also suggests using 3 to 5 photos. The examples use `[Name]` and `[Shelter]` as placeholders; Claude fills in your animal's name and your organization.

## Why it's written this way

The rules come from published adoption research, chiefly Markowitz (2020), which compared 676,004 Petfinder profiles of adopted and unadopted pets, and Kelling et al. (2026), which tested how 561 readers understood adoption-ad wording. Rix et al. (2021) and Archer et al. (2025) add the voice and breed-label rules. [`research-basis.md`](skills/adoption-profile-writing/references/research-basis.md) cites each study and checks the rules against the Shelter Animals Count adoptions checklist.

- **Behavior someone saw, told as a scene.** The profile describes what someone actually observed, from the side of a person spending time with the animal. It doesn't predict how the animal will act in a new home. It describes behaviors instead of labels such as "timid" or "reactive", writes in the third person, and leaves the breed to your listing's breed field.
- **One or two honest struggles.** Every profile names at least one struggle an adopter would notice and no more than two, each with where it happens or how it's improving. The rest of the record is for the shelter's history review before the meet.
- **Disclosure without alarm.** Limits on placement stay on the card. Bites, attacks, guarding that made contact, incidents with children, and harm to cats or small animals don't go on the card. Instead the card says the shelter will review the animal's history with the adopter before they meet.
- **No gatekeeping.** It cuts conditions placed on the adopter ("experienced owners only") and keeps limits on the home ("no cats"). When a narrower tag sits beside a broad one, such as "No Small Kids" beside "Good with Kids", the profile states the limit along with the yes.

## What the plugin contains, runs, and sends

The plugin is one skill: written instructions for Claude plus reference pages, all plain text. It has no connectors, no hooks, and no agents. It doesn't connect to any service, collect anything, or send your notes anywhere. Your notes stay in your conversation with Claude, as with any other chat.

It includes one small script, [`check_draft.py`](skills/adoption-profile-writing/scripts/check_draft.py). Claude runs it on each draft when Python is available, in the same place Claude runs any other code for you. The script uses only Python's standard library. It reads the one draft file it's given and prints a list of fixes. It makes no network connections and writes no files.

The script checks the headings, word count, and how much of the profile covers struggles. It also flags trait words, shelter-setting words, first-person pronouns, breed words, and banned phrases. For dogs in a Diamond Dog behavior program, it checks the standard closing message about that program. You don't need to run it yourself, and the skill checks drafts by hand when Python isn't there.

To run it yourself, from the `skills/adoption-profile-writing` folder:

```
python3 scripts/check_draft.py path/to/draft.md
```

It exits 0 when the draft passes and 1 when it lists fixes.

## License

Apache License 2.0. See the [LICENSE](https://github.com/ckrough/goodspirits/blob/main/LICENSE) file.
