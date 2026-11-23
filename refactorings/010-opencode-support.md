# Refactoring 010: one neutral core, built for Claude Code and OpenCode

Status: Proposed · Date: 2026-11-23 · Corrected after the spike (`docs/spikes/opencode-v2.md`), adjusted to 011 and 005

**Order:** after refactoring 011 (split into design and implement) and 005 (stable evals). It works on
`design-the-domain` only; `implement-the-domain` follows the same build and adapter later.

## Goal

The skills of the plugin run in Claude Code and in OpenCode (Claude as the model; tested with 1.15.10
and 1.19.6, no version calls itself "V2") from one repository: the same skill text, the same slash
names (`/requirement`, `/problem-space-initialization`, …), the same project config
`domain-model/config.md`.

## Research (2026-11-23, from the docs; the points marked *spike* were tried out)

- **OpenCode skills:** reads `SKILL.md` also in `.claude/skills` and `.agents/skills`; understands
  `disable-model-invocation`; the skill ID is the frontmatter `name`, not the path (*spike*:
  `design-the-domain/grilling` is "not found"); relative paths in a skill are relative to its folder; no
  counterpart to `${CLAUDE_PLUGIN_ROOT}`; same `name` in two sources: one wins silently, which one is not
  stable, only the log (`duplicate skill name`) says so (*spike*). Slash call of a skill is not
  documented (`@skill-id` is).
- **OpenCode commands:** markdown files in `.opencode/commands/`, file name = command, `$ARGUMENTS`.
- **OpenCode subagents:** markdown in `.opencode/agents/` with a model per agent, tool `task` in the
  tested versions (the docs call it `subagent`); *spike*: two in one message run in parallel and each
  call returns the subagent's last message as its result. Question tool: `question`.
- **OpenCode plugins (V2):** code (`Plugin.define`, `ctx.skill.transform`, `ctx.command.transform`),
  installed by `plugins` in `opencode.json` or `opencode plugin add`; no marketplace.
- **Headless (*spike*):** `opencode run --format json -m <provider/model> [--command <name>] "<args>" < /dev/null`
  writes `tool_use` lines (`skill`, `task`, `bash`) an eval can read; needs a timeout and a closed stdin.
  A skill load names its base directory, `python3 <base>/scripts/…` works; Claude Code names it too.
- **Instructions:** `AGENTS.md`, `CLAUDE.md` as fallback.
- **Others:** Matt Pocock ships skills only, self-contained, each harness through its own installer
  (`npx skills add … -a opencode` copies the skill folders). Superpowers: one repo, one folder per
  harness, abstract action names in the skills, a mapping per harness (OpenCode: a plugin injects it).
  `npx skills` installs skills only, no commands, agents or hooks. The Agent Skills standard allows
  `scripts/`, `references/`, `assets/` inside a skill folder.

## What changes in the skill texts

| Kind | Places | Needed? |
|---|---|---|
| Paths `${CLAUDE_PLUGIN_ROOT}/assets/x.md` → relative to the skill folder | 37 | yes: the variable does not exist in OpenCode, and moving the files alone leaves the old paths dangling |
| Cross-references `design-the-domain:requirement` → the skill name | about 76 (design and implement together) | yes: the namespace is a Claude mechanism, OpenCode knows only `name:`; changes with the renaming of 011 anyway |
| Tool terms ("Skill tool", `AskUserQuestion`, "start a subagent") | about 8, 3 and a few | **not yet decided**: Claude sees the tool list of OpenCode (`skill`, `question`, `task`) and probably maps the terms itself; try the skills unchanged first and abstract only what fails |

## Decisions

- **One repository, one neutral core, one adapter per harness.** Not one repository per harness.
- **Self-contained skills in the build output.** The source keeps `assets/` and `scripts/` once; a build
  script copies what each skill needs into its folder. The build **derives** the files from the paths
  the `SKILL.md` names, including what those files need themselves (`interview-round.py` imports
  `requirements.py`), with a short list of exceptions; a path to a missing file fails the build. No
  hand-kept `skills.json`. In the output `requirements.py` stands in several skill folders, in the
  source once. A script call in the text names the script by the skill's base directory
  (`<base directory>/scripts/requirements.py`, run from the project root).
- **Names:** per the rule in refactoring 011 (area and function in the name, unique against known
  collections, folder name = `name:`, a folder prefix does not help in OpenCode). The build checks the
  rule. Entry skills keep short names.
- **Slash names** through command wrappers (`.opencode/commands/<name>.md`: load the skill, pass
  `$ARGUMENTS`); a command and its skill may have the same name (*spike*).
- **The build copies, no symlinks in the output:** symlinks work in a project (OpenCode and Claude Code,
  *spike*), not verified in the cache copy of an installed Claude plugin.
- **Skill folders install with `npx skills add … -a opencode`** (target `.agents/skills/<name>/`, all
  subfolders copied, *spike*); commands and agents need their own install route.
- **Model keys** in the config (`model-ground`, `model-writer`, `model-init`): Claude Code sets the
  model per call, OpenCode per agent definition. The adapter generates one agent file per model key;
  the keys must also express `provider/model`; the open names (`inherit`, `sonnet`, …) stay for Claude.
- **Evals run against the build output**, not the source; a check that the output matches the source
  guards against testing stale builds. A second eval runner for OpenCode (`opencode run --format json`).

## Plan

1. **Spike** (done, see below) and a small **addendum**: load a skill with `disable-model-invocation: true`
   through a command wrapper; model per agent file; the `question` tool headless.
2. **Package 1a, neutral core:** build script with derived dependencies, relative paths, names per 011,
   Claude Code output as before; all Claude evals stay green (basis: refactoring 005).
3. **Package 1b, tool terms:** only what the trial of the unchanged skills in OpenCode shows to fail.
4. **Package 2, OpenCode adapter:** command wrappers, agent files, installation, eval runner, tests on a
   real OpenCode installation.

## Spike (done 2026-11-23, report `docs/spikes/opencode-v2.md`)

| Question | Result |
|---|---|
| Headless with a readable trace | yes |
| Command loads a skill, passes `$ARGUMENTS` | yes (the tested skill had no `disable-model-invocation`) |
| Skill IDs with a folder prefix | **no**, the ID is `name:`; duplicates are overridden silently |
| Parallel subagents, result back | yes, synchronous as the tool result (tool `task`) |
| Base directory, scripts, symlinks | yes; symlinks work in a project, not verified in a plugin cache |
| `npx skills add … -a opencode` | yes, complete, into `.agents/skills/` |

## Open

- Spike addendum (step 1 of the plan): `disable-model-invocation: true` skill through a command, model
  per agent as `provider/model`, `question` headless, permission prompts in `run`.
- Whether `npx skills add` from a GitHub source behaves like the local one (probably yes).
- Install route for the commands (the `skills` installer does not know commands).
- Whether the model keys need a mapping file per harness.
- Version: after 009 (0.8.0) and 011; this one as 1.0.0 at the earliest.
