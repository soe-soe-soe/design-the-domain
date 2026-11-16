# define-the-domain project config

Template for the project config the define-the-domain skills read. Copy it to `.claude/pts.md` in the project
root and fill in the values; the skills read that file before anything else and stop if it is
missing. The plugin knows no project: every path, command and convention of a project stands
here, everything structural about the code (building blocks, test levels, markers, seams) in the
project's structure document (key `structure`).

A skill names a value by its key in angle quotes: `‹requirements›/US-0042-*.md` means the folder
under key `requirements`. Paths are relative to the project root. The values in the table are the
methodology's default layout; keep them unless the project already has another.

## Project

| Key | Meaning | Value |
|---|---|---|
| `problem-space-language` | Language of the problem space – stories, FRs and their scenarios (Gherkin keywords via `# language:`), process files, glossary terms and descriptions, domain map, folder names and slugs of subdomains and business objects – and of everything said to the user | English |
| `solution-space-language` | Language of the solution space – identifiers, code comments, docstrings, commit messages, solution-space documents and the solution-space columns of the glossaries | English |
| `user` | Name of the person answering the grilling, used in the provenance line (`🗣️`) | <name> |
| `project-rules` | File with the project's rules: commit convention, feature workflow; a glossary or glossary-map format here overrides the plugin templates | `CLAUDE.md` |

Methodology – template headings, field labels, tags, IDs, status values, change kinds, type
folders, report labels of the writers – is English in every project: it is the plugin's structure
and `scripts/requirements.py` parses it. Everything else follows the two language keys; a skill that
writes or says something names the key it follows.

## Problem space

| Key | Meaning | Value |
|---|---|---|
| `problem-space` | Root of the problem space: FRs per subdomain, planned changes in `planned/` below each FR folder | `domain-model/problem-space` |
| `requirements` | User stories: done ones in the folder, open ones (draft, ready, in-progress) in `planned/`, cancelled ones in `cancelled/` | `domain-model/problem-space/requirements` |
| `domain-map` | Subdomains, types, business relationships | `domain-model/problem-space/domain-map.md` |
| `glossaries` | One glossary per subdomain | `domain-model/glossaries` |
| `methodology-glossary` | Methodology terms, among them "Open point" | `domain-model/glossaries/_methodology.md` |
| `glossary-map` | Index of the glossaries, read by `domain-modeling` and new-requirement | `GLOSSARY-MAP.md` |

## Solution space

| Key | Meaning | Value |
|---|---|---|
| `structure` | Target structure of the code: building blocks, naming, test levels and markers | `domain-model/solution-space/structure.md` |
| `context-map` | Generated map of the bounded contexts | `domain-model/solution-space/context-map.md` |
| `context-map-command` | Command that regenerates `context-map` from the code | <command> |
| `refactorings` | Migration plans per bounded context | `refactorings` |
| `adr` | Architecture decision records | `docs/adr` |
| `architecture-adrs` | ADRs on building blocks and boundaries that placement must follow | <ADR numbers> |
| `test-strategy-adr` | ADR on the test strategy | <ADR number> |

## Code

| Key | Meaning | Value |
|---|---|---|
| `backend` | Backend source root | <path> |
| `backend-shared` | Cross-cutting backend code, out of scope for the init skills | <path> |
| `backend-tests` | Backend tests | <path> |
| `test-fixtures` | Shared test fixtures, registered in the root `conftest` or equivalent | <path> |
| `e2e-journeys` | UI journeys, one per business object: `‹e2e-journeys›/<subdomain>/<business-object>.<ext>` | <path> |
| `e2e-pages` | Page objects of the UI tests | <path> |
| `scenario-marker` | How a test references its FR scenario | <e.g. a decorator with the scenario ID> |
| `not-implemented` | Body of a shell symbol that has no behaviour yet | <e.g. raise NotImplementedError> |
| `migrations` | Schema migration tool and folder | <tool, path> |

## Commands

Run from the project root; a value may change directory first.

| Key | Meaning | Value |
|---|---|---|
| `typecheck` | Static type check of the backend | <command> |
| `test-all` | Full backend suite | <command> |
| `test-file` | One backend test file | <command with <file>> |
| `test-collect` | Collect backend tests without running them | <command> |
| `e2e-list` | List the UI tests without running them | <command> |
| `e2e-file` | Run one UI test file | <command with <file>> |

## Ticket system

Optional. The repository stays the source of truth: stories are written one way to the ticket
system by `${CLAUDE_PLUGIN_ROOT}/templates/ticket.md` (fields, description, when), never read
back. The ticket's ID goes into the story header as `External`.

| Key | Meaning | Value |
|---|---|---|
| `ticket-system` | `none`, `linear` or `jira`, used through the project's connector for it | `none` |
| `ticket-team` | Team (key) the tickets belong to | <team key, or – for none> |
| `ticket-project` | Project the tickets are assigned to, or `–` | `–` |
| `ticket-assignee` | Assignee of every ticket, or `–` | `–` |
| `ticket-labels` | `subdomain` (a label per subdomain of the story's FRs, named as in the domain map) or `–` | `subdomain` |
| `repository-url` | Base URL for links to files on the default branch | <e.g. https://github.com/<owner>/<repo>/blob/main> |

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
| `model-ground` | Subagent reading the ground in /define-the-domain:new-requirement (reads and summarises) | `inherit` |
| `model-writer` | Subagent running problem-space-story and problem-space-fr (finds open points) | `inherit` |
| `model-init` | Subagents of /define-the-domain:problem-init and /define-the-domain:solution-init, one per subdomain or context | `inherit` |
