# goodspirits

Free writing helpers for people who volunteer or work at animal shelters and rescues. I volunteer with a shelter, built these tools for that work, and shaped them so any rescue can use them.

The one helper here today writes **adoption profiles**: the short write-up about a dog or cat that goes on your website, kennel card, or adoption listing. You give it the animal's notes, and it gives you back an honest, warm profile that helps the right family say yes.

It works inside Claude: the Claude app on your computer or phone, claude.ai in a web browser, Cowork, or Claude Code.

## Install

You don't need to know anything technical. Open Claude, paste this message, and send it:

> Please install the plugins from https://github.com/ckrough/goodspirits for me.

Claude reads this page and either installs the plugin for you or walks you through a few clicks. It takes about two minutes. If Claude can't open web links, follow the steps below for your app yourself.

### For the agent doing the install

You are helping someone who may not be technical. Use plain words, give one step at a time, and wait for them to say each step is done before you give the next. Don't ask them to open a terminal unless they are already using Claude Code.

This repository is a plugin marketplace named `goodspirits`. It holds one plugin, `adoption-profile-writing` (shown as **Adoption Profile Writing**). Install that plugin. Work out which app the person is using, then follow the matching steps.

**Claude app on the desktop or phone, claude.ai in a browser, or Cowork.** You can't press these buttons yourself, so guide the person through them:

1. Open **Customize** in the sidebar, then choose **Plugins**.
2. Choose **Add**, then **Add marketplace**.
3. Type `ckrough/goodspirits` and confirm.
4. Find **Adoption Profile Writing** in the list (under **Discover**) and choose **Add**.

The plugin is saved to their Claude account, so it also works in chat, in Cowork, and in Claude Code signed in to the same account. A new conversation or task picks it up.

**Claude Code.** If you can run shell commands, run this one yourself. It adds the marketplace and installs the plugin:

```
claude plugin install adoption-profile-writing --marketplace ckrough/goodspirits
```

Then ask the person to type `/reload-plugins` in Claude Code, or start a new session.

You can't type slash commands for them. If you can't run shell commands, ask the person to type these into Claude Code one at a time:

```
/plugin marketplace add ckrough/goodspirits
/plugin install adoption-profile-writing@goodspirits
/reload-plugins
```

**Another agent app that supports Agent Skills.** Copy the folder [`plugins/adoption-profile-writing/skills/adoption-profile-writing`](plugins/adoption-profile-writing/skills/adoption-profile-writing/) into that app's skills folder, keeping the folder name. The skill's instructions are in `SKILL.md` inside it.

**Check that it worked.** Ask the person to start a new conversation and say "Help me write an adoption profile." Claude should use the Adoption Profile Writing skill and ask for the animal's notes.

**If a step fails:**

- *No Add marketplace option, or adding it is refused.* On a Team or Enterprise plan, the organization's Owner decides whether members can add marketplaces. Ask the person to send their Owner this page's link.
- *No Plugins page at all.* Their plan or app version may not offer plugins. Use the Claude Code steps if they have Claude Code, or the Agent Skills copy step in another app.
- *"Marketplace already added."* That's fine. Go straight to installing the plugin.
- *No Python on their computer.* That's fine too. The plugin's draft checker is optional, and the skill checks drafts by hand without it.

Don't run the repository's `make` commands or edit any files to install. Those are for people who maintain this project.

## What's included

| Plugin | What it does |
|---|---|
| [Adoption Profile Writing](plugins/adoption-profile-writing/) | Writes and rewrites adoptable-pet profiles (bios, kennel cards, listings) from the animal's own notes. |

## Using it

After installing, start a new conversation and paste in what you know about the animal: walk notes, foster notes, staff memos, or the current profile you want to improve. Then ask, for example:

> Write an adoption profile for Biscuit from these notes.

The [plugin's page](plugins/adoption-profile-writing/) explains what the profile looks like and why it's written that way.

## License

Apache License 2.0. See [LICENSE](LICENSE) for the full text.

Copyright (C) 2026 Chris Krough
