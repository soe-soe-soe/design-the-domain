# pts project config – eval fixture

Project config the eval cases place at `.claude/pts.md`; it describes the sample project their
files come from (a Python backend with a TypeScript UI). Paths are relative to the project root.

## Project

| Key | Meaning | Value |
|---|---|---|
| `problem-space-language` | Language of the problem space – stories, FRs and their scenarios (Gherkin keywords via `# language:`), process files, glossary terms and descriptions, domain map, folder names and slugs of subdomains and business objects – and of everything said to the user | German |
| `solution-space-language` | Language of the solution space – identifiers, code comments, docstrings, commit messages, solution-space documents and the solution-space columns of the glossaries | English |
| `user` | Name of the person answering the grilling, used in the provenance line (`🗣️`) | Alex |
| `project-rules` | File with the project's rules: commit convention, feature workflow; a glossary or glossary-map format here overrides the plugin templates | `CLAUDE.md` |

Methodology (template headings, field labels, tags, IDs, status values) stays English.

## Problem space

| Key | Meaning | Value |
|---|---|---|
| `problem-space` | Root of the problem space: FRs per subdomain, planned changes in `planned/` below each FR folder | `domain-model/problem-space` |
| `requirements` | User stories: done ones in the folder, open ones (draft, ready, in-progress) in `planned/`, cancelled ones in `cancelled/` | `domain-model/problem-space/requirements` |
| `domain-map` | Subdomains, types, business relationships | `domain-model/problem-space/domain-map.md` |
| `glossaries` | One glossary per subdomain | `domain-model/glossaries` |
| `methodology-glossary` | Methodology terms, among them "Open point" | `domain-model/glossaries/_methodology.md` |
| `glossary-map` | Index of the glossaries, read by `domain-modeling` and problem-definition | `GLOSSARY-MAP.md` |

## Solution space

| Key | Meaning | Value |
|---|---|---|
| `structure` | Target structure of the code: building blocks, naming, test levels and markers | `domain-model/solution-space/structure.md` |
| `context-map` | Generated map of the bounded contexts | `domain-model/solution-space/context-map.md` |
| `context-map-command` | Command that regenerates `context-map` from the code | `python backend/ops/generate_context_map.py` |
| `refactorings` | Migration plans per bounded context | `refactorings` |
| `adr` | Architecture decision records | `docs/adr` |
| `architecture-adrs` | ADRs on building blocks and boundaries that placement must follow | ADR 007–011; placement follows above all 008 and 009 |
| `test-strategy-adr` | ADR on the test strategy | ADR 012 |

## Code

| Key | Meaning | Value |
|---|---|---|
| `backend` | Backend source root | `backend` |
| `backend-shared` | Cross-cutting backend code, out of scope for the init skills | `backend/core` |
| `backend-tests` | Backend tests | `backend/tests` |
| `test-fixtures` | Shared test fixtures, registered in the root `conftest` or equivalent | `backend/tests/fixtures` |
| `e2e-journeys` | UI journeys, one per business object: `‹e2e-journeys›/<subdomain>/<business-object>.<ext>` | `frontend/e2e/journeys` (`.spec.ts`) |
| `e2e-pages` | Page objects of the UI tests | `frontend/e2e/pages` |
| `scenario-marker` | How a test references its FR scenario | `@pytest.mark.fr("FR-<subdomain>-NNN/Sn")` directly above `def` |
| `not-implemented` | Body of a shell symbol that has no behaviour yet | `raise NotImplementedError` |
| `migrations` | Schema migration tool and folder | Alembic, `backend/ops/migrations/versions` |

## Commands

Run from the project root; a value may change directory first.

| Key | Meaning | Value |
|---|---|---|
| `typecheck` | Static type check of the backend | `cd backend && pyright` |
| `test-all` | Full backend suite | `cd backend && pytest` |
| `test-file` | One backend test file | `cd backend && pytest <file>` |
| `test-collect` | Collect backend tests without running them | `cd backend && pytest --collect-only -q` |
| `e2e-list` | List the UI tests without running them | `cd frontend && npx playwright test --list` |
| `e2e-file` | Run one UI test file | `cd frontend && npx playwright test <file>` |

## Ticket system

Optional. The repository stays the source of truth: stories are written one way to the ticket
system by `${CLAUDE_PLUGIN_ROOT}/references/ticket.md` (fields, description, when), never read
back. The ticket's ID goes into the story header as `External`.

| Key | Meaning | Value |
|---|---|---|
| `ticket-system` | `none`, `linear` or `jira`, used through the project's connector for it | `none` |
| `ticket-team` | Team (key) the tickets belong to | – |
| `ticket-project` | Project the tickets are assigned to, or `–` | `–` |
| `ticket-assignee` | Assignee of every ticket, or `–` | `–` |
| `ticket-labels` | `subdomain` (a label per subdomain of the story's FRs, named as in the domain map) or `–` | `–` |
| `repository-url` | Base URL for links to files on the default branch | – |

### Ticket status

| Story status | Ticket status |
|---|---|
| draft | Backlog |
| ready | Todo |
| in-progress | In Progress |
| done | Done |
| cancelled | Canceled |

## Models

Model of the subagents the skills start: `inherit` (the session's model), `haiku`, `sonnet` or
`opus`. The skills themselves run on the model of whoever calls them; only a subagent's model
can be set per project.

| Key | Meaning | Value |
|---|---|---|
| `model-ground` | Subagent reading the ground in /pts:problem-definition (reads and summarises) | `inherit` |
| `model-writer` | Subagent running problem-story-writer and problem-fr-writer (finds open points) | `inherit` |
| `model-init` | Subagents of /pts:problem-init and /pts:solution-init, one per subdomain or context | `inherit` |
