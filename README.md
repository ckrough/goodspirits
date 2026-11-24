# goodspirits

Free writing helpers for people who volunteer or work at animal shelters and rescues. I volunteer with a shelter, built these tools for that work, and shaped them so any rescue can use them.

The one helper here today writes **adoption profiles**: the short write-up about a dog or cat that goes on your website, kennel card, or adoption listing. You give it the animal's notes, and it gives you back an honest, warm profile that helps the right family say yes.

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

## License

Apache License 2.0. See [LICENSE](LICENSE) for the full text.

Copyright (C) 2026 Chris Krough
