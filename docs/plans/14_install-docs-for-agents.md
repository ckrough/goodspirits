---
title: Write install docs an agent can follow for laypeople
issue: 14
type: Task
date: 2026-11-24
---

# Write install docs an agent can follow for laypeople

## Context

This implements the acceptance criteria of #14. The audience is shelter volunteers who are not technical. They should be able to paste `https://github.com/ckrough/goodspirits` or `ckrough/goodspirits` into their agent and have the agent install the marketplace and its one plugin for them. Today the root README opens with two Claude Code slash commands and a research summary, the plugin has no README, and CLAUDE.md speaks only to maintainers.

An agent reaches this repository in one of two ways. A chat or Cowork agent fetches the GitHub page, which renders README.md, so README.md carries the full install instructions. A Claude Code agent may clone the repository, where CLAUDE.md loads automatically, so CLAUDE.md opens with a short install section that points to README.md. Other harnesses read AGENTS.md rather than CLAUDE.md, so they rely on README.md's skill-folder step.

The install paths come from Anthropic's current docs (claude.com/docs/plugins/overview, claude.com/docs/cowork/guide/plugins, code.claude.com/docs/en/plugins/install), read on 2026-11-24:

- claude.ai, the desktop app, and Cowork: Customize > Plugins > Add > Add marketplace, enter `ckrough/goodspirits`, then find Adoption Profile Writing under Discover and select Add. The plugin is saved to the account and shows up in chat, Cowork, and Claude Code signed in to the same account (after `/reload-plugins`). A chat agent cannot click these buttons, so the README tells the agent to walk the person through them one step at a time.
- Claude Code: `/plugin marketplace add ckrough/goodspirits` then `/plugin install adoption-profile-writing@goodspirits`, then `/reload-plugins`. From a shell, `claude plugin install adoption-profile-writing --marketplace ckrough/goodspirits` does both steps; `claude plugin install --help` confirms the `--marketplace` flag.
- Other harnesses that read Agent Skills: copy `plugins/adoption-profile-writing/skills/adoption-profile-writing/` into that harness's skills folder.

The research summary and checker usage move from the root README into the new plugin README, which is the plugin's own page. The maintainer sections of CLAUDE.md (Commands, Issue tracker, Plugin enablement) stay unchanged below the new section.

The acceptance criteria of #14, each with where it is covered:

| Criterion | Step | Verification |
|---|---|---|
| README.md is written for a non-technical reader, with an agent block giving steps per surface | 1 | headless README read-through |
| `plugins/adoption-profile-writing/README.md` exists and explains the plugin, its install, and its use | 1 | link check |
| CLAUDE.md opens with an agent install section ahead of the maintainer material | 2 | headless clone run |
| Install steps match current Anthropic docs | 1, 2 | CLI help and scratch install |
| `make check` passes | 1, 2 | `make check` |

## Files

- `README.md`
- `plugins/adoption-profile-writing/README.md`
- `CLAUDE.md`

## Work order

1. Rewrite `README.md` and create the plugin README, then commit when `make check` exits 0.
   - `README.md` holds a plain-language opening that says what goodspirits is and who it is for.
     - Its `## Install` section opens with a short paragraph for people: paste this link into Claude and ask it to install.
     - Under `## Install`, a `### For the agent doing the install` section gives the steps for each surface. It also covers how to confirm the install worked (ask Claude to write a profile and see the skill load) and what to do when a step fails: no Add marketplace option on a Team or Enterprise plan, a plan without plugins, a marketplace that already exists. It says the skill works without Python, because the checker is optional.
     - After the install sections come "What's included", "Using it" with one example request, and License.
   - `plugins/adoption-profile-writing/README.md` holds a plain-language description and a link to the root README's install section, without repeating the commands.
     - It explains how to use the plugin: paste in the animal's record.
     - It describes what the result looks like (four sections), gives the research summary moved from the root README, and shows the optional checker command.
2. After step 1, add a `## Installing for a user` section to the top of `CLAUDE.md`, before `## Commands`, then commit when `make check` exits 0.
   - The section is addressed to an agent: when the person asked to install, follow README.md's "For the agent doing the install" section.
   - It gives the two Claude Code commands inline, marked as a copy of README.md to update together.
   - It says not to run `make` targets or edit files to install.
   - Reword the opening paragraph so it reads for both audiences.

## Tests

No unit test is added or changed. The change is documentation with no code path for `unittest` to reach. Headless runs in Verification test the instructions instead.

## Verification

- `make check` exits 0.
- `make verify` exits 0.
- `sh /Users/ckrough/.claude/plugins/cache/backchain/daedalus/12.4.0/scripts/daedalus.sh check-docs` reports 0 problems.
- Scratch install. Use a throwaway `CLAUDE_CONFIG_DIR` in the scratchpad so the user's config is untouched.
  - `claude plugin marketplace add <worktree root>` succeeds.
  - `claude plugin install adoption-profile-writing@goodspirits` succeeds.
  - `claude plugin list` shows the plugin.
- README read-through. From an empty scratchpad directory, run `claude -p --setting-sources ""` with only README.md's text in the prompt and the question: "A friend who is not technical pasted ckrough/goodspirits and asked you to install it in the Claude desktop app. What do you tell them, step by step?"
  - The answer gives Customize > Plugins > Add marketplace with `ckrough/goodspirits`, then the Add step.
  - The answer contains no terminal commands.
- Clone run. From a scratch clone of the branch, run `claude -p --setting-sources project "The person asked you to install this."`.
  - The answer gives `/plugin marketplace add ckrough/goodspirits` and `/plugin install adoption-profile-writing@goodspirits`.
  - It proposes no `make` target and no file edit.
- Links. List every relative link in the three files with `grep -o '](\([^h)][^)]*\))'`; `ls` resolves each one.
- After merge, the operator adds the marketplace once by hand in the desktop app, because the click path cannot be run from here.

## Experiments

No experiment warranted: the install steps come from Anthropic's published docs. The Claude Code CLI forms were confirmed with `claude plugin install --help` and `claude plugin marketplace add --help`, and Verification runs a scratch install. The claude.ai and Cowork click path stays unverified on this machine, and the operator confirms it after merge.

## Architect review

- Important: no Verification step exercises an install command -> amended: CLI help checked and a scratch install added; the `--marketplace` flag exists.
- Important: the headless read-through would load CLAUDE.md and user rules, not just README -> amended: run from an empty directory with `--setting-sources ""` and README text only.
- Important: nothing checks the CLAUDE.md path -> amended: added a clone run with `--setting-sources project`.
- Nit: failure list covers only an Owner block -> amended: plan without plugins, existing marketplace, and the no-Python fallback added; the claude.ai code-execution prerequisite is left out because the docs read do not state it.
- Nit: other harnesses read AGENTS.md, not CLAUDE.md -> amended in Context.
- Nit: install commands in three places -> amended: the plugin README links instead of repeating them; CLAUDE.md keeps the commands, marked as a copy.
- Nit: steps 1 and 2 are not independent -> amended: step 2 runs after step 1, and the heading text is fixed in the plan.
- Nit: acceptance criteria not mapped -> amended: table in Context and the link-check method in Verification.
