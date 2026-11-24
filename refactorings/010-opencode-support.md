# Refactoring 010: one neutral core, built for Claude Code and OpenCode

Status: Proposed · Date: 2026-11-23 · Corrected after the spike (`docs/spikes/opencode-v2.md`), adjusted to 011, 012 and 005 · Trial and apm research 2026-11-23

**Order:** after refactoring 011 (split into design and implement) and 005 (stable evals). 005 is done,
012 too (its evals stable), and design 0.9.0 is in `dist`; 011 is open only on the implement side, which
does not block this one. It works on `design-the-domain` only; `implement-the-domain` follows the same build and adapter later.

## Goal

The skills of the plugin run in Claude Code and in OpenCode (Claude as the model; tested with 1.15.10
and 1.19.6, no version calls itself "V2") from one repository: the same skill text, the same slash
names (`/domain-interview`, `/domain-init`, …), the same project config
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
- **apm (Microsoft Agent Package Manager, docs read 2026-11-23, about 0.38):** dependencies in
  `apm.yml` (GitHub `owner/repo/path`, pinned by tag, branch, commit or semver range), `apm.lock.yaml`
  with a hash per deployed file, `apm install`, `apm update`, `apm install --frozen`. Target `opencode`:
  skills into `.agents/skills/<name>/`, **commands into `.opencode/commands/`, agents into
  `.opencode/agents/`**, hooks skipped; a `model` per agent is documented only for Kiro. A Claude Code
  plugin (`.claude-plugin/plugin.json`) is copied whole to `.agents/plugins/<plugin>/` for the targets
  `claude` and `copilot`, where `${CLAUDE_PLUGIN_ROOT}` in commands and hooks resolves to that folder;
  for other targets it is "split into primitives".
- **apm tried (0.37.0, 2026-11-23):** `apm install soe-soe-soe/design-the-domain#dist --target opencode`
  (private repo, the git credentials sufficed) resolves `dist` as a plugin, keeps the whole package in
  `apm_modules/` (put into `.gitignore`) and copies each skill folder to `.agents/skills/<name>/`;
  `apm.lock.yaml` pins the commit. With a local probe plugin: a skill folder is copied **with its
  subfolders** (`scripts/`, `assets/`), for `opencode` and `claude` alike; **markdown links** to files
  outside the skill folder are rewritten to `apm_modules/…`; relative paths **in code** (inline or
  fenced) and `${CLAUDE_PLUGIN_ROOT}` are **not** rewritten – a script call by `${CLAUDE_PLUGIN_ROOT}`
  breaks. `commands/` and `agents/` of the plugin go to `.opencode/commands/` and `.opencode/agents/`
  (and `.claude/…` for `claude`); an agent's `model: haiku` is copied **verbatim**, OpenCode expects
  `provider/model`. The user's own install on another machine (paths as `design-the-domain/…`) was
  laid out by hand, not by apm.

## What changes in the skill texts

| Kind | Places | Needed? |
|---|---|---|
| Paths `${CLAUDE_PLUGIN_ROOT}/assets/x.md` → relative to the skill folder | 28 in design (2026-11-23) | yes: the variable does not exist in OpenCode, and moving the files alone leaves the old paths dangling |
| Cross-references `design-the-domain:domain-interview` → the skill name | in design 27 calls and 19 slash mentions (`/design-the-domain:…`); implement 6 calls, 6 slash mentions (2026-11-23) | yes: the namespace is a Claude mechanism, OpenCode knows only `name:`; changes with the renaming of 011 anyway |
| Tool terms ("Skill tool", `AskUserQuestion`, "start a subagent") | a few; `AskUserQuestion` once in design (`domain-init`) | **partly settled by the trial below**: "Skill tool" and "start a subagent" map by themselves (`skill`, `task`); `AskUserQuestion` still open – the one question in the trial was not asked |

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
- **Install route for OpenCode: apm** (user, 2026-11-23, after the apm trial above). It installs the
  self-contained skill folders, the command wrappers and the agent files of the OpenCode build from one
  GitHub source with a lockfile. Consequences: script and template paths in a skill point **inside its
  own folder** (`scripts/…`, `assets/…` from the base directory) – the self-contained build output
  above is what makes apm work, `${CLAUDE_PLUGIN_ROOT}` must not stay; the OpenCode agent files carry
  `provider/model`, since apm passes `model` through unchanged. `npx skills add` (*spike*) stays
  possible for the skills alone, without commands and agents.
- **Model keys** in the config (`model-ground`, `model-writer`, `model-init`): Claude Code sets the
  model per call, OpenCode per agent definition. The adapter generates one agent file per model key;
  the keys must also express `provider/model`; the open names (`inherit`, `sonnet`, …) stay for Claude.
- **Evals run against the build output**, not the source; a check that the output matches the source
  guards against testing stale builds. A second eval runner for OpenCode (`opencode run --format json`).

## Plan

1. **Spike** (done, see below) and a small **addendum**: load a skill with `disable-model-invocation: true`
   through a command wrapper; model per agent file; the `question` tool headless.
2. **Package 1a, neutral core (done 2026-11-23, see below):** build script with derived dependencies, relative paths, names per 011,
   Claude Code output as before; all Claude evals stay green (basis: refactoring 005).
3. **Package 1b, tool terms (done 2026-11-24, see below):** only what the trial of the unchanged skills in OpenCode shows to fail.
4. **Package 2, OpenCode adapter (built 2026-11-24, eval runner and real-model test open, see below):** command wrappers, agent files, installation, eval runner, tests on a
   real OpenCode installation.

## Package 1a, done (2026-11-23)

- `tools/build.py`: builds `build/design-the-domain/` (gitignored) with `assets/` and `scripts/`
  inside each skill folder, derived from the paths a skill's files name (`assets/<file>`,
  `scripts/<file>`, `<base directory>/scripts/<file>`), from what those files name themselves and from
  script imports; a path to a missing file fails. `--with-evals` adds `evals/`, `--check` compares an
  existing build with a fresh one. The name rule of 011 is checked (folder = `name:`, lowercase words,
  `tools/denied-skill-names.txt`, no double in `implement-the-domain/`).
- `tools/build-dist.sh` builds `dist` from that output; the dist tree is no longer `assets/` and
  `scripts/` at the root but the self-contained skill folders.
- Skill texts: `${CLAUDE_PLUGIN_ROOT}/assets/x` → `assets/x`, script calls →
  `python3 <base directory>/scripts/x`, `../../assets/x` links → `assets/x`; each skill says once that
  these paths are relative to its base directory. The subagent briefs hand the base directory over
  (`domain-init`, `domain-interview`). The three fixture configs carry the same change.
- Not done here: the cross-references `design-the-domain:<skill>` stay as they are (Claude namespace);
  where they become bare names is a decision for 1b or the adapter (the build can rewrite them for
  OpenCode), as the evals call the namespaced names. The deny list is a first list, to be completed.
- **Not run:** the Claude evals against the build (`cd build/design-the-domain`, `claude plugin eval`);
  unit tests and the build checks ran. Run at least `domain-init/*` and `domain-interview` cases
  before the version bump.

## Packages 1b and 2, built (2026-11-24)

Decisions (user): the OpenCode build lives in the subfolder `opencode/` of the branch `dist`; the
model per subagent comes from `provider/model` values of the project config.

- **Build:** `python3 tools/build.py --target opencode` (`build/opencode/`). The same self-contained
  skill folders; the `design-the-domain:` namespace is stripped in skills, assets and scripts (the
  source keeps it, the Claude evals call the namespaced names); `commands/<skill>.md` wrappers (load the
  skill, pass `$ARGUMENTS`); a manifest `design-the-domain-opencode`, which apm needs to take the folder as
  a package. `tools/build-dist.sh` puts it into `dist/opencode/`.
- **1b, tool terms:** a section "Harness notes (OpenCode)" appended to `domain-interview` and
  `domain-init` in the OpenCode output only: `task` with a named `subagent_type`, and the `question`
  tool for the `AskUserQuestion` step (plain text if the tool is missing, never skipped). The Claude text
  is unchanged.
- **Model per subagent:** `scripts/opencode-agents.py` reads `model-ground`, `model-writer`, `model-init`
  and writes `.opencode/agents/domain-ground|domain-writer|domain-init-worker.md`; a `provider/model` value
  becomes `model:`, `inherit` and the Claude names leave the agent on the session's model (the script
  says so). `assets/config.md` names the new value form. The skills' notes tell the model to run it.
- **Checked:** `apm install build/opencode --target opencode` lays out `.opencode/commands/` (8) and
  `.agents/skills/` (8, with their `assets/` and `scripts/`); OpenCode 1.15.10 lists the skills and, after
  the script ran, the three agents as subagents. Unit tests: `scripts/test_opencode_agents.py`,
  `tools/test_build.py`.
- **Not checked:** a real run with a model (a command wrapper calling `domain-interview`, a subagent
  with its own model, `question`); whether OpenCode reads agent files written mid-session (the note says
  restart); `apm install owner/repo/opencode#dist` from GitHub (only the local folder was installed);
  the `description:` of the wrappers when a skill description holds characters YAML dislikes (JSON string
  used). **Not built:** the OpenCode eval runner (`opencode run --format json`, permission config per
  project). The Claude evals did not run on the new build either (stopped, see 1a).

## Spike (done 2026-11-23, report `docs/spikes/opencode-v2.md`)

| Question | Result |
|---|---|
| Headless with a readable trace | yes |
| Command loads a skill, passes `$ARGUMENTS` | yes (the tested skill had no `disable-model-invocation`) |
| Skill IDs with a folder prefix | **no**, the ID is `name:`; duplicates are overridden silently |
| Parallel subagents, result back | yes, synchronous as the tool result (tool `task`) |
| Base directory, scripts, symlinks | yes; symlinks work in a project, not verified in a plugin cache |
| `npx skills add … -a opencode` | yes, complete, into `.agents/skills/` |

## Trial of the unchanged skills (2026-11-23)

Plugin 0.9.0 (after 012) installed the way `apm install` lays it out: the skill folders in
`.agents/skills/<name>/`, `assets/` and `scripts/` under `design-the-domain/` in the project,
`${CLAUDE_PLUGIN_ROOT}` replaced by `design-the-domain`. OpenCode 1.15.10, Sonnet 5.5 through
OpenRouter, headless (`opencode run --format json`), on the eval fixtures: `domain-interview` on
`evals/fixtures/project/` (round 1, then round 2 by `--session` with answers), `domain-init` on the
files of `evals/domain-init/two-subdomains-reconciled` (`model-init: sonnet`), called without
subdomains.

| Question | Result |
|---|---|
| Skill by name, also with `disable-model-invocation: true` | yes, without a command wrapper ("Nutze den Skill domain-interview") |
| "Call the Skill tool" for `domain-grilling` and `glossary` | yes, mapped to `skill` by the model |
| Assets and scripts under `design-the-domain/…` | yes, found; `interview-round.py` renders rounds 1 and 2 (references after the title, grouping, numbering) |
| Subagents (ground, writer, one per subdomain) | yes, `task` with `subagent_type: general`, two in one message in parallel, report back |
| Writers write | yes: 2 stories, 4 FRs, a deferred point stays `@open` in the story |
| **Model per subagent** | **no**: `task` has no model parameter; `model-init: sonnet` was dropped silently, the subagents ran on the main model, and the final report still said "Subagenten (`sonnet`)" |
| **`AskUserQuestion` (domain-init step 3)** | **not asked**: the run took both subdomains ("Ihr Auftrag nennt keine Subdomain"); open whether `question` is missing in `run` or the model skipped the step |
| Permissions in `run` | a bash call needing approval is rejected and **ends the run** (a `for … cat` loop in domain-init); an eval runner needs a permission config per project |

Seen in passing, probably the same in Claude Code (check with the evals of 005): the main run writes a
"Kontext/Stand" block before the round; FRs without a business object stand directly in
`‹subdomain›/<type>/planned/`.

Environment: the local OpenCode database had been migrated by a newer version (`session_message.seq`
NOT NULL error with 1.15.10); the trial ran with its own `XDG_DATA_HOME`.

## Open

- Spike addendum (step 1 of the plan): `disable-model-invocation: true` skill through a command, model
  per agent as `provider/model`, `question` headless, permission prompts in `run`. The trial confirms
  that the model needs agent files (the decision above stands) and leaves `question`: test it
  interactively.
- ~~Where the OpenCode build lives~~ decided: `opencode/` in `dist`; the local apm install works, the
  GitHub one is not tried.
- ~~Model keys~~ decided: `provider/model` in the config, an agent file per key by script.
- `confluence-publish` (new in 0.9.0): needs the Atlassian MCP; whether OpenCode reaches it the same
  way is not tried.
- Version: design is at 0.9.0 (in `dist` since 2026-11-23); this one as 1.0.0 at the earliest.
