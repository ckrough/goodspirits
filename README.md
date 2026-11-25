# goodspirits

Free writing helpers for people who volunteer or work at animal shelters and rescues. I volunteer with a shelter, built these tools for that work, and shaped them so any rescue can use them.

The helper here writes **adoption profiles**: the short write-up about a dog or cat that goes on your website, kennel card, or adoption listing. You give it the animal's notes, and it gives you back an honest, warm profile that helps the right family say yes.

It works in the Claude desktop app, and in claude.ai in a web browser.

## Install

Open the Claude desktop app, paste this message, and send it:

> Please help me install the plugins from https://github.com/ckrough/goodspirits.

Claude reads this page and walks you through four clicks. It takes about two minutes.

If you'd rather do it yourself, these are the same four steps:

1. In the Claude desktop app, open **Customize** in the sidebar, then choose **Plugins**.
2. Choose **Add**, then **Add marketplace**.
3. Type `ckrough/goodspirits` and confirm.
4. Find **Adoption Profile Writing** in the list (under **Discover**) and choose **Add**.

That's it. Start a new conversation to use it.

### For the agent doing the install

You are helping a shelter volunteer who uses the Claude desktop app. Use plain words, give one step at a time, and wait for them to say each step is done before you give the next. Keep everything inside the app.

This repository is a plugin marketplace named `goodspirits`. It holds one plugin, `adoption-profile-writing`, shown in the app as **Adoption Profile Writing**. You can't press buttons in their app, so guide them through the four steps above, in order. The same steps work in claude.ai in a browser.

The plugin is saved to their Claude account, so after these steps it works in every new chat and Cowork task on that account.

**Check that it worked.** Ask them to start a new conversation and say "Help me write an adoption profile." Claude should use the Adoption Profile Writing skill and ask for the animal's notes.

**If a step fails:**

- *No Add marketplace option, or adding it is refused.* On a Team or Enterprise plan, the organization's Owner decides whether members can add marketplaces. Ask them to send their Owner this page's link.
- *No Customize or Plugins page.* Their app may need updating, or their plan may not offer plugins. Ask them to update the Claude desktop app and try again.
- *"Marketplace already added."* That's fine. Go straight to step 4.
- *Anything mentions Python.* They can ignore it. The plugin's draft checker is optional, and the skill checks drafts by hand without it.

Don't edit any files in this repository or run its `make` commands to install. Those are for people who maintain this project.

In a Claude Code session, ask them to type `/plugin marketplace add ckrough/goodspirits`, then `/plugin install adoption-profile-writing@goodspirits`, then `/reload-plugins`. In another app that reads Agent Skills, copy the folder [`plugins/adoption-profile-writing/skills/adoption-profile-writing`](plugins/adoption-profile-writing/skills/adoption-profile-writing/) into that app's skills folder.

## What's included

| Plugin | What it does |
|---|---|
| [Adoption Profile Writing](plugins/adoption-profile-writing/) | Writes and rewrites adoptable-pet profiles (bios, kennel cards, listings) from the animal's own notes. |

## Using it

After installing, start a new conversation and paste in what you know about the animal: walk notes, foster notes, staff memos, or the current profile you want to improve. Then ask, for example:

> Write an adoption profile for Biscuit from these notes.

The [plugin's page](plugins/adoption-profile-writing/) explains what the profile looks like, why it's written that way, and what the plugin does with your notes.

## Evals

This section is for people who maintain the plugin.

The plugin carries an eval suite under `plugins/adoption-profile-writing/evals/`, run by Claude Code's built-in `claude plugin eval`. Each case gives the skill one anonymized shelter record and asks for a profile, then scores the draft against an ideal profile written for that record, plus graders for the rules the record tests: a bite kept off the card, a placement limit shown as the behavior behind it rather than stated, and a record whose later entries overrule its earlier ones. Every case also runs without the skill, so the report shows each case's score with the skill, without it, and the difference.

```
make eval          # run every case on the skill's pinned writer model (paid model calls; run outside the Claude sandbox)
make eval-record   # write each model's summary from the newest sweep to evals/history/, for committing
```

`make eval` stamps each sweep with the commit it starts at and marks it complete when it finishes, and `make eval-record` refuses a sweep that ran at another commit, started with uncommitted plugin changes, or did not finish, so each committed summary names the commit of the skill it scored. The skill pins `model: claude-sonnet-5-5` in its frontmatter, so it runs on Sonnet 5.5 whatever the session model, and a sweep writes with Sonnet 5.5 to match. `make eval` refuses any other writer: the pin takes over once the skill fires, so the with-skill arm would run on Sonnet and the without-skill arm on the other model. The baseline sweep showed Haiku, Sonnet, and Opus 5.5 within a few points of each other on every case, so the skill, not the model, is what limits the card. Every run is judged by `claude-opus-5-5`, a stronger model than the writer, unless `JUDGE_MODEL=<model>` is given, and each summary records both models. Sweeps judged by Sonnet 5.5, the baseline included, do not compare with Opus-judged ones. A score is a signal to read per case, not a verdict: the judge is a Claude model grading a Claude draft, and five cases cannot show a small difference between two versions of the skill.

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
