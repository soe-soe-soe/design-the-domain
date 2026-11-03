# pts – problem, test and solution space skills

A Claude Code plugin for domain-driven feature work in three spaces:

- **Problem space:** `/pts:problem-definition` grills a requirement into ready user stories and
  functional requirements (FRs) with Gherkin scenarios; `problem-story-writer` and
  `problem-fr-writer` write them, `/pts:problem-init` derives the model from existing code.
- **Solution space:** `solution-definition` places a story's scenarios into bounded contexts,
  aggregates and building blocks and builds a shell without behaviour; `/pts:solution-init`
  plans the migration of existing code into that structure.
- **Tests:** `test-definition` writes red scenario, interface, migration and journey tests
  against the shell; `/pts:story-workflow` runs placement, tests, implementation, review and
  closing for one story.

## Setup in a project

1. Copy [assets/config.md](assets/config.md) to `.claude/pts.md` in the project and fill in
   paths, commands and conventions. The skills read it first and stop without it; the plugin
   itself knows no project.
2. Keep the code structure (building blocks, test levels, markers) in the document the config
   names under `structure`.
3. Add the marketplace and enable the plugin in the project's `.claude/settings.json`:

   ```json
   {
     "extraKnownMarketplaces": {
       "problem-test-solution-skills": {
         "source": { "source": "github", "repo": "soe-soe-soe/problem-test-solution-skills" }
       }
     },
     "enabledPlugins": { "pts@problem-test-solution-skills": true }
   }
   ```

## Craft skills

`grilling`, `domain-modeling`, `tdd`, `code-review` and `codebase-design` come with the plugin.
They are based on [mattpocock/skills](https://github.com/mattpocock/skills) (MIT,
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)); what was taken over and changed, and the weekly
check against upstream, stand in [docs/upstream.md](docs/upstream.md).

## Requirements and FRs

Stories live in `‹requirements›/` (done), `planned/` (draft, ready, in-progress) and `cancelled/`;
the status flow stands in [skills/problem-story-writer/assets/story.md](skills/problem-story-writer/assets/story.md).
An active FR is the implemented state; the writers put changes into one planned file per FR in
`planned/` next to it. [scripts/requirements.py](scripts/requirements.py) (Python 3, standard
library) checks, completes and cancels stories and prints an FR's history:

```
python3 scripts/requirements.py check    US-0042
python3 scripts/requirements.py complete US-0042
python3 scripts/requirements.py cancel   US-0042
python3 scripts/requirements.py history  FR-deadlines-003
```

[scripts/round.py](scripts/round.py) renders each round of `/pts:problem-definition`: the model
supplies its own questions, the script adds the writers' open points, numbers, groups and writes
the provenance lines.

## Ticket system

Optional, one way from the repository: with `ticket-system` set in `.claude/pts.md`, every story
gets a ticket (Linear or Jira through the project's connector) by
[references/ticket.md](references/ticket.md) – title, team, project, assignee, labels per subdomain,
mapped status, and a description with role sentence, why, AC titles, FRs and a link to the story
file. The ticket ID is kept in the story as `External`.

## License

MIT, see [LICENSE](LICENSE). The craft skills based on mattpocock/skills carry its MIT license in
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
