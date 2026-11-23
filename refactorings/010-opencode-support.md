# Refactoring 010: one neutral core, built for Claude Code and OpenCode

Status: Proposed · Date: 2026-11-23 · Corrected after the spike (`docs/spikes/opencode-v2.md`)

## Goal

The skills of the plugin run in Claude Code and in OpenCode (Claude as the model; tested with 1.15.10 and 1.19.6, no version calls itself "V2") from one
repository: the same skill text, the same slash names (`/requirement`, `/problem-space-initialization`,
…), the same project config `domain-model/config.md`.

## Research (2026-11-23, from the docs; the points marked *spike* were tried out)

- **OpenCode skills:** reads `SKILL.md` also in `.claude/skills` and `.agents/skills`; understands
  `disable-model-invocation`; the skill ID is the frontmatter `name`, not the path (*spike*: `design-the-domain/grilling` is "not found"); relative paths in a
  skill are relative to its folder; no counterpart to `${CLAUDE_PLUGIN_ROOT}`; same `name` in two sources:
  one wins silently, which one is not stable, only the log (`duplicate skill name`) says so (*spike*). Slash call of a skill is not documented (`@skill-id` is).
- **OpenCode commands:** markdown files in `.opencode/commands/`, file name = command, `$ARGUMENTS`.
- **OpenCode subagents:** markdown in `.opencode/agents/` with a model per agent, tool `task` in the tested versions (the docs call it `subagent`); *spike*: two in one message
  run in parallel and each call returns the subagent's last message as its result. Question tool: `question`.
- **OpenCode plugins (V2):** code (`Plugin.define`, `ctx.skill.transform`, `ctx.command.transform`),
  installed by `plugins` in `opencode.json` or `opencode plugin add`; no marketplace.
- **Headless (*spike*):** `opencode run --format json -m <provider/model> [--command <name>] "<args>" < /dev/null`
  writes `tool_use` lines (`skill`, `task`, `bash`) an eval can read; needs a timeout and a closed stdin.
  A skill load names its base directory, `python3 <base>/scripts/…` works.
- **Instructions:** `AGENTS.md`, `CLAUDE.md` as fallback.
- **Others:** Matt Pocock ships skills only, self-contained, each harness through its own installer
  (`npx skills add … -a opencode` copies the skill folders). Superpowers: one repo, one folder per
  harness, abstract action names in the skills, a mapping per harness (OpenCode: a plugin injects it).
  `npx skills` installs skills only, no commands, agents or hooks. The Agent Skills standard allows
  `scripts/`, `references/`, `assets/` inside a skill folder.

## Decisions

- **One repository, one neutral core, one adapter per harness.** Not two repositories.
- **Self-contained skills in the build output.** Source keeps `assets/` and `scripts/` once; a build
  script copies what each skill needs into its folder (`skills.json` lists it per skill). In the output
  `requirements.py` stands in several skill folders, in the source once. The skill text uses paths
  relative to its folder instead of `${CLAUDE_PLUGIN_ROOT}`.
- **Abstract actions in the skill text** ("load the skill", "start a subagent", "ask the user") instead of
  tool names; the mapping per harness stands in the adapter (`adapters/<harness>/`).
- **Names:** the entry skills a user types keep their short names (`/requirement`, …); the helper skills
  the model loads (`grilling`, `domain-modeling`, `tdd`, `code-review`, `codebase-design`) get a unique
  `name:` in the OpenCode output (for example `ddd-grilling`; a folder prefix does not help), because they
  collide with Matt Pocock's skills of the same name (silent override). Cross-references in the texts
  follow, and the build checks that no `name` occurs twice, also against known foreign skills.
- **Slash names** through command wrappers (`.opencode/commands/<name>.md`: load the skill, pass
  `$ARGUMENTS`); a command and its skill may have the same name (*spike*).
- **The build copies, no symlinks in the output:** symlinks work in a project (OpenCode and Claude Code,
  *spike*), not verified in the cache copy of an installed Claude plugin.
- **Skill folders install with `npx skills add … -a opencode`** (target `.agents/skills/<name>/`, all
  subfolders copied, *spike*); commands and agents need their own install route.
- **Model keys** in the config (`model-ground`, `model-writer`, `model-init`) must also express
  `provider/model` for OpenCode; the open names (`inherit`, `sonnet`, …) stay for Claude Code.
- **Evals run against the build output**, not the source; a check that the output matches the source
  guards against testing stale builds. A second eval runner for OpenCode.

## Plan

1. **Spike** (done, see below).
2. **Package 1, neutral core** (this workspace): replace the 37 uses of `${CLAUDE_PLUGIN_ROOT}`, the tool
   names (Skill tool, Agent, AskUserQuestion), `skills.json`, build script, Claude Code output as
   before; all Claude evals stay green.
3. **Package 2, OpenCode adapter**: command wrappers, mapping, installation, eval runner, tests on a real
   OpenCode installation.

## Spike (done 2026-11-23, report `docs/spikes/opencode-v2.md`)

| Question | Result |
|---|---|
| Headless with a readable trace | yes |
| Command loads a skill, passes `$ARGUMENTS` | yes |
| Skill IDs with a folder prefix | **no**, the ID is `name:`; duplicates are overridden silently |
| Parallel subagents, result back | yes, synchronous as the tool result (tool `task`) |
| Base directory, scripts, symlinks | yes; symlinks work in a project, not verified in a plugin cache |
| `npx skills add … -a opencode` | yes, complete, into `.agents/skills/` |

## Open

- Not tried in the spike: the `question` tool headless, the model per agent as `provider/model`, permission
  prompts in `run`.
- Whether `npx skills add` from a GitHub source behaves like the local one (probably yes).

- Install route for the commands (the `skills` installer does not know commands).
- Whether the model keys need a mapping file per harness.
- Version bump: 0.8.0 for the config move (refactoring 009) comes first; this one follows as 0.9.0 or 1.0.0.
