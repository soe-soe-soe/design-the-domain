# Plugin structure by space

## Goal

Skills and evals are grouped by space – problem, solution, test, workflow, craft – so a look at the
tree shows which files belong to which space. Skill names and commands stay as they are
(`/pts:problem-definition`).

## Why

`skills/` holds 14 skills side by side: four of the problem space, two of the solution space, one
of the test space, the story workflow and five craft skills taken over from mattpocock/skills.
Which skill belongs to which space is only written in the README. The same holds for `evals/`.

## Current state

- `skills/<skill>/`, flat; the default scan of `skills/` finds them, `plugin.json` names no paths.
- `evals/<skill>/<case>/`, flat; fixtures in `evals/fixtures/`, reached as `../../fixtures` from
  each `place-files.sh`.
- `scripts/` (requirements.py, round.py and their tests) and `assets/`, `references/` shared by several spaces.
- Paths into the plugin stand in the skills as `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/...`,
  `${CLAUDE_PLUGIN_ROOT}/scripts/...`, `${CLAUDE_PLUGIN_ROOT}/assets/...` and
  `${CLAUDE_PLUGIN_ROOT}/references/...`.

## Target state

The pattern of mattpocock/skills (`skills/engineering/tdd`, `skills/productivity/grill-me`, paths
listed in `plugin.json`), one level per space:

```
.claude-plugin/plugin.json      "skills": ["./skills/problem-space", "./skills/solution-space",
                                           "./skills/test-space", "./skills/workflow", "./skills/craft"]
skills/
├── problem-space/   problem-definition, problem-story-writer, problem-fr-writer, problem-init
├── solution-space/  solution-definition, solution-init
├── test-space/      test-definition
├── workflow/        story-workflow
└── craft/           grilling, domain-modeling, codebase-design, tdd, code-review
scripts/             requirements.py, round.py (+ tests) – used by problem-definition and story-workflow
assets/              shared templates: config, glossary, glossary map
references/          shared guidance: output format, ticket sync
evals/
├── fixtures/
├── problem-space/   problem-definition/, problem-story-writer/, problem-fr-writer/, problem-init/
├── solution-space/  solution-definition/
└── test-space/      test-definition/
```

- A `plugin.json` entry is a folder of `<skill>/SKILL.md` folders; `skills/` itself then holds no
  `SKILL.md` one level down, so the default scan adds nothing twice.
- `claude plugin eval` treats a folder without `prompt.md` or `case.yaml` as a group, so
  `evals/<space>/<skill>/<case>/` works. `--eval-dir evals/problem-space` runs one space;
  the tags in `case.yaml` stay as the filter for a run over everything.
- Not chosen: one root folder per space with its own `skills/`, `scripts/` and `evals/`. The
  eval runner knows one eval folder per run, `scripts/`, `assets/` and `references/` serve several spaces, and
  `story-workflow` belongs to none.

## Steps

1. `git mv` the skill folders into their space folder; add the `skills` array to `plugin.json`.
2. Replace `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/` with `${CLAUDE_PLUGIN_ROOT}/skills/<space>/<skill>/`
   in every skill, template and reference (`grep -rn 'CLAUDE_PLUGIN_ROOT}/skills/'`).
3. `git mv` the eval folders into `evals/<space>/`; `../../fixtures` becomes `../../../fixtures`
   in every `place-files.sh`.
4. Update README, DEVELOPING.md, `docs/upstream.md` (pts skill paths) and the weekly-check brief.
5. Check: `claude --plugin-dir .` lists all 14 skills under `/pts:`; one eval run per space;
   `tools/build-dist.sh` still takes `skills/` whole.
