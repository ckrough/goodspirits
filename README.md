# goodspirits

Tools for animal-rescue volunteers and staff. The first one writes adoption profiles: the bios, kennel cards, and listings that help an animal find a home. You give Claude what you know about the animal, and it writes a profile based on what research says helps adopters respond.

I volunteer with a shelter, and I built this for that work, generalized so any rescue can use it.

## Install

You do not need to be technical. Paste this link into Claude (or another AI assistant) and ask it to install goodspirits for you:

```
https://github.com/ckrough/goodspirits
```

You can also paste `ckrough/goodspirits`. Claude will walk you through the few clicks it needs from you.

### For the agent doing the install

The person asking is likely not technical. Do the steps you can, and walk them through the ones only they can do, one step at a time, in plain words. Use no terminal commands unless they are in Claude Code. This repository is a plugin marketplace named `goodspirits`, with one plugin, `adoption-profile-writing`.

Pick the surface the person is using.

**Claude on the web, the desktop app, or Cowork.** You cannot click these buttons, so tell the person:

1. Open Customize, then Plugins.
2. Select Add, then Add marketplace.
3. Enter `ckrough/goodspirits`.
4. Find Adoption Profile Writing under Discover and select Add.

The plugin is saved to their account, so it also shows up in Claude Code signed in to the same account (after `/reload-plugins`).

**Claude Code.** Run these, then `/reload-plugins`:

```
/plugin marketplace add ckrough/goodspirits
/plugin install adoption-profile-writing@goodspirits
```

From a shell, this does both steps in one command: `claude plugin install adoption-profile-writing --marketplace ckrough/goodspirits`.

**Another assistant that reads Agent Skills.** Copy the folder `plugins/adoption-profile-writing/skills/adoption-profile-writing/` from this repository into that assistant's skills folder.

**Confirm it worked.** Ask Claude to write an adoption profile for an animal and check that the Adoption Profile Writing skill loads.

**If a step fails.**

- There is no Add marketplace option: on a Team or Enterprise plan, an owner may have turned it off. Ask the person to request it from their organization's owner.
- The plan has no plugins: tell the person, and use the skill-folder copy above if their assistant supports it.
- The marketplace already exists: skip to step 4 (or the `/plugin install` command).
- The skill works without Python. The draft checker described in the plugin README is optional.

## What's included

| Plugin | What it does |
|---|---|
| [adoption-profile-writing](plugins/adoption-profile-writing/) | Writes and rewrites adoptable-pet profiles (bios, kennel cards, listings) from the animal's own record. |

## Using it

Ask Claude to write a profile and paste in what you know about the animal. For example:

> Write an adoption profile for this dog. Here are the intake notes and what the volunteers have seen: ...

The plugin's [README](plugins/adoption-profile-writing/README.md) describes the result and the research behind it.

## License

Apache License 2.0. See [LICENSE](LICENSE) for the full text.

Copyright (C) 2026 Chris Krough
