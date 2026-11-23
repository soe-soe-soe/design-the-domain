# Refactoring 011: split into design-the-domain (problem space) and implement-the-domain (solution space)

Status: In progress · Date: 2026-11-23

The problem-space part is done (design-the-domain 0.9.0, 2026-11-23); the solution-space part is a
scaffold, its points stand under "Solution space (open)".

## Goal

`design-the-domain` holds the problem space only; the skills of the solution space move into a plugin
of their own, `implement-the-domain`. Each plugin has one job, a smaller surface for the OpenCode work
(refactoring 010) and a name rule that keeps its skill names unique.

## Decisions (user, 2026-11-23)

- The split follows the two spaces: problem space → `design-the-domain`, solution space →
  `implement-the-domain`.
- Skill names carry what they do in the domain: `grilling` becomes `domain-grilling`.
- One repository with two plugins; `implement-the-domain/` is a subfolder of this repository.
- **Story status belongs to the problem space.** A new design skill `story-workflow` does
  `start` (ready → in-progress), `done` (`requirements.py complete`) and `cancel`, with the ticket
  sync. `requirement` cancels through it, implement calls it instead of the script.
- **`domain-modeling` is split.** Its glossary part becomes the skill `glossary`; the techniques
  "concrete scenarios" and "cross-reference with code" go into `requirement`; the ADR part goes to
  implement (`solution-definition`, section ADRs, with `ADR-FORMAT.md`). The weekly upstream check
  stays and maps the upstream skill onto the three parts (`docs/upstream.md`, *Split skills*).
- **ADRs belong to the solution space only.** No design skill reads or writes ADRs; business
  rationale stands in a story's Why and an FR's history.
- **`structure` and `architecture-adrs` belong to implement.** The design init no longer reads them;
  it takes the code over from folders, tests, routers and imports.
- **Glossary columns Solution space and Identifier stay** in design's format. Implement sets them
  through the interface of `glossary` (`set-solution`); the init fills them from code.
- **Interfaces of design** are documented in the section `## Interface` of each callable skill and
  listed in the README (section Interfaces), together with the file formats implement reads. The
  build warns when implement calls a design skill without that section.
- **`model-init`** stays with design (its init only); implement gets `model-solution-init`.
- No project names the renamed skills today; the README's release notes suffice. Version 0.9.0.
- implement's `story-workflow` is renamed `implement-story`, so the two plugins share no skill name.
- The prefix `problem-space-` goes: `problem-space-story` → `user-story`, `problem-space-fr` →
  `functional-requirement`, `problem-space-initialization` → `domain-init` (still in 0.9.0, before it
  reaches `dist`). Not `story` and `initialization`: too generic for OpenCode, where the name is the
  only ID.

## Assignment of the skills

| Skill | Plugin | Remark |
|---|---|---|
| `requirement` | design | entry skill; now also holds the scenario and code techniques |
| `user-story`, `functional-requirement` | design | writers; no ADRs any more |
| `domain-init` | design | entry skill; fills the design part of the config, domain map, glossary, subdomain map, FRs |
| `story-workflow` | design | new; status transitions after ready; interface |
| `domain-grilling` | design | was `grilling` |
| `glossary` | design | was `domain-modeling` without ADRs, scenarios and code check; interface `set-solution` |
| `solution-definition`, `solution-init` | implement | `solution-definition` now offers ADRs |
| `implement-story` (was `story-workflow`), `test-definition` | implement | `implement-story` calls design's `story-workflow` |
| `tdd`, `code-review`, `codebase-design` | implement | all three collide with Matt Pocock's skills; `code-review` also with Claude's built-in |

## Name rule

1. A name says its area and its function: `domain-…` (`domain-grilling`, `domain-init`) or the
   artefact it works on (`user-story`, `functional-requirement`, `glossary`, `story-workflow`) in
   design; `implement-…` or `solution-…` in implement. A plain generic word (`story`, `init`) is not
   enough.
2. A name is in no known collection: Matt Pocock, Anthropic, Superpowers, built-ins of Claude Code and
   OpenCode. The build checks every name against a deny list and against doubles in the own plugin
   and in the other plugin (OpenCode overrides a duplicate `name` silently, see refactoring 010).
3. Entry skills the user types keep a short name as long as they pass the check (`requirement`,
   `glossary`, `story-workflow`).
4. Folder name and `name:` are the same; `npx skills` names the target folder after `name:`.

The deny-list check itself is not built yet (belongs to 010, which needs it for OpenCode).

## Renames and evals

Refactoring 005 (stable evals) was planned to run **before** the renames and writes the skill names
of its time into graders, prompts and `expected_outcome` (`grilling`, `domain-modeling`). Whoever
renames a skill in 011 carries every reference in the evals along:

- `case.yaml` (`expected_outcome`), `graders/*.md`, `prompt.md`, `files/` and `evals/fixtures/` –
  search with `grep -rn '<old-name>' evals/` (for implement: `implement-the-domain/evals/`).
- Most affected: `evals/requirement/round-1-grilling-only/graders/02-*` (provenance line with
  `🧩 grilling` or `domain-modeling`).
- Afterwards the affected cases run once.

State (2026-11-23): the design renames (`grilling` → `domain-grilling`, `domain-modeling` →
`glossary`) came before 005, in commit `0247c7b`; their eval references are carried along (the
provenance lines in `evals/requirement/*`, `scripts/test_interview_round.py`, the methodology
fixture), a grep for the old names in `evals/` finds none. The second round of renames (`problem-space-…` → `user-story`,
`functional-requirement`, `domain-init`) moved the eval folders and carried the references and
provenance lines along the same way. The affected cases have **not run** yet
(`evals/requirement/*`, `evals/domain-init/config-*`). The rule holds for every
further rename, the three craft skills of implement included, and for 005 if it starts after
this: it uses the new names.

**Fixtures (decision, 2026-11-23).** `evals/fixtures/` and `implement-the-domain/evals/fixtures/`
are kept separately, not synchronised. 005 builds out `evals/fixtures/` only. Where 011 splits the
config (`adr`, `structure`, `architecture-adrs` and the code paths of the solution space to
implement; `backend`, `backend-shared`, `backend-tests` stay with design), the fixture config of
each plugin is adjusted on its own.

## Done (2026-11-23)

- Solution-space skills, their evals (with a copy of `evals/fixtures/`), licenses and a manifest in
  `implement-the-domain/`; references read `implement-the-domain:<skill>`.
- design: `story-workflow` new; `grilling` → `domain-grilling` (provenance lines, script, tests and
  evals follow); `domain-modeling` → `glossary`; ADR and `structure` reads removed from the writers
  and the init; config template cut to the design part (Project, Problem space, Code with
  `backend`, `backend-shared`, `backend-tests`, Ticket system, Models), the init fills only that
  part and leaves other parts alone; config evals adjusted.
- implement: its part of the config template in `implement-the-domain/assets/config.md`
  (`model-solution-init` included); `implement-story` (was `story-workflow`) and `solution-definition` call
  the design interfaces.
- `docs/upstream.md` (split mapping, brief of the weekly check), `THIRD_PARTY_LICENSES.md` of both
  plugins, README (Interfaces, release notes), version 0.9.0.
- `tools/build-dist.sh` builds design only, warns about `implement-the-domain:` in what it publishes
  and about implement calling a design skill without `## Interface`.

Not run: the evals (`claude plugin eval`), neither design's nor implement's.

## Solution space (open)

Points of implement-the-domain, parked while design comes first.

1. **Names of the three colliding craft skills:** `implement-tdd`, `implement-review`,
   `implement-design`.
2. **Config step:** implement has its template part but no skill that fills it; its skills still
   point to `/design-the-domain:domain-init` when the config is missing.
3. **Dependency on design:** implement only works with design enabled; Claude Code plugins have no
   declared dependency [Vermutung, not checked]. Say so in its README and check it at the start of
   `implement-story`.
4. **Publishing:** implement needs its own build (or a parameterised `build-dist.sh`), its own `dist`
   branch or path, and its own marketplace entry.
5. **Evals:** `implement-the-domain/evals/fixtures/` started as a copy of `evals/fixtures/` and is
   kept on its own (section "Renames and evals"); its config still holds the full key set and
   needs `model-solution-init`. Whether `claude plugin eval .` at the root also finds `implement-the-domain/evals/`
   is not checked [Vermutung: no, it looks in `./evals`]. No eval covers the calls to design's
   interfaces yet.
6. **The pilot project:** where the solution-space skills stand today stays as it is (they were never in
   `dist`).

## Effects on other refactorings

- 005 (stable evals) shrinks to the evals of design; the evals of implement move with their skills.
- 010 (OpenCode) works on design only; implement follows the same build and adapter later.
