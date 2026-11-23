# design-the-domain – problem space skills

A Claude Code plugin for the problem space of domain-driven feature work:
`/design-the-domain:domain-interview` grills a requirement into ready user stories and functional
requirements (FRs) with Gherkin scenarios; `user-story` and `functional-requirement` write them,
`/design-the-domain:domain-init` derives the model from existing code;
`/design-the-domain:story-workflow` moves a story to ready, in-progress, done or cancelled.

The solution and test space (placement, tests first, implementation, review) is moving into a
plugin of its own, [implement-the-domain](implement-the-domain/README.md) (refactoring 011, not
published yet). design-the-domain works without it; an implementing plugin of your own uses the
interfaces below.

## Setup in a project

1. `domain-model/config.md` holds the paths and conventions of the project; the plugin itself
   knows no project. Every skill reads it first and, without it, says to fill it in first.
   `/design-the-domain:domain-init` fills it in with you, from the template
   [assets/config.md](assets/config.md) and what it finds in the project. Another plugin may add
   its own part below, under a heading of its own; design-the-domain leaves it alone.
2. Add the marketplace and enable the plugin in the project's `.claude/settings.json`:

   ```json
   {
     "extraKnownMarketplaces": {
       "design-the-domain": {
         "source": { "source": "github", "repo": "soe-soe-soe/design-the-domain" }
       }
     },
     "enabledPlugins": { "design-the-domain@design-the-domain": true }
   }
   ```

## Craft skills

`domain-interview` is built like Matt Pocock's `grill-with-docs`: it composes `domain-grilling`
(how the interview is asked: design tree, rounds, open points, closing round) and `glossary` (the
ubiquitous language, concrete scenarios, the check against code), and adds the problem-space
structure – the ground, the writers after every round, the close. `domain-init` asks through
`domain-grilling` too. They are based on [mattpocock/skills](https://github.com/mattpocock/skills) (MIT,
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)); what was taken over and changed, and the weekly
check against upstream, stand in [docs/upstream.md](docs/upstream.md).

## Interfaces

What another plugin – implement-the-domain or one of your own – may rely on. Everything else
(the writers, the interview and its rounds, the init, the transition `ready`) is internal and may change in any release.
The contract of a skill is the section `## Interface` of its `SKILL.md`; this list only points
there. Both plugins must be enabled; the caller uses the Skill tool with the full name.

| Interface | Kind | Use it to | Contract |
|---|---|---|---|
| `design-the-domain:story-workflow <story> start\|done\|cancel` | skill | move a story to in-progress when implementation starts, to done when it is implemented (merges its planned FR changes into the active FRs), or cancel it; syncs the ticket | [skills/story-workflow/SKILL.md](skills/story-workflow/SKILL.md) |
| `design-the-domain:glossary set-solution <subdomain>` | skill | set the columns `Solution space` and `Identifier` of existing glossary terms once their code name is decided | [skills/glossary/SKILL.md](skills/glossary/SKILL.md) |
| `scripts/requirements.py history <FR>` | script | print the history of an FR | [scripts/requirements.py](scripts/requirements.py) |
| Story file | format | read the story, its status, ACs and `## Functional requirements` | [assets/story.md](assets/story.md) |
| FR and planned FR file | format | read rules and scenarios; a scenario's ID `FR-<subdomain>-NNN/Sn` is what a test references | [assets/functional-requirement.md](assets/functional-requirement.md), [assets/planned-functional-requirement.md](assets/planned-functional-requirement.md) |
| Glossary, domain map | format | map subdomains to bounded contexts, business objects to aggregates | [assets/glossary.md](assets/glossary.md), [assets/domain-map.md](assets/domain-map.md) |

Read the problem space only through these formats and change it only through the two skills: an
implementing plugin never edits stories, FRs or the problem-space columns of a glossary itself.

Without implement-the-domain, wire your own workflow the same way: call `story-workflow … start`
before you implement a ready story and `story-workflow … done` once its scenarios pass, and report
code names through `glossary set-solution`.

## Release notes

**0.9.0** – The solution-space skills move into implement-the-domain (not published yet). Renamed:
`grilling` → `domain-grilling`, `domain-modeling` → `glossary`, `problem-space-story` →
`user-story`, `problem-space-fr` → `functional-requirement`, `problem-space-initialization` →
`domain-init`, `requirement` → `domain-interview`; the ADR part of `domain-modeling` moved to
implement-the-domain. New: `story-workflow` for ready, start, done and cancel of a story (it now
also validates a story at the close of an interview and syncs its ticket). `domain-grilling` holds
the rounds of the interview and is used by `domain-interview` and `domain-init`; the questions no
longer carry a provenance line, the artifact a question rests on stands after its title. The config template holds only the keys of
design-the-domain (Solution space, Commands and the code keys of the solution space left it); an
existing `domain-model/config.md` stays valid.

## Requirements and FRs

Stories live in `‹requirements›/` (done), `planned/` (draft, ready, in-progress) and `cancelled/`;
the status flow stands in [assets/story.md](assets/story.md).
An active FR is the implemented state; the writers put changes into one planned file per FR in
`planned/` next to it. [scripts/requirements.py](scripts/requirements.py) (Python 3, standard
library) checks, completes and cancels stories and prints an FR's history; `story-workflow` runs it
for you:

```
python3 scripts/requirements.py check    US-0042
python3 scripts/requirements.py complete US-0042
python3 scripts/requirements.py cancel   US-0042
python3 scripts/requirements.py history  FR-deadlines-003
```

[scripts/interview-round.py](scripts/interview-round.py) renders each round of `domain-grilling`: the model
supplies its own questions, the script adds the writers' open points, numbers, groups and puts
the artifact a question rests on after its title.

## Ticket system

Optional, one way from the repository: with `ticket-system` set in `domain-model/config.md`, every story
gets a ticket (Linear or Jira through the project's connector) by
[assets/ticket.md](assets/ticket.md) – title, team, project, assignee, labels per subdomain,
mapped status, and a description with role sentence, why, AC titles, FRs and a link to the story
file. The ticket ID is kept in the story as `External`.

## License

MIT, see [LICENSE](LICENSE). The craft skills based on mattpocock/skills carry its MIT license in
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
