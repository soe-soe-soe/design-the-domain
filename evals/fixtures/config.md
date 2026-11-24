# design-the-domain project config – eval fixture

Project config the eval cases place at `domain-model/config.md`; it describes the sample project their
files come from (a Python backend with a TypeScript UI); only the design-the-domain part. Paths are relative to the project root.

## Project

| Key | Meaning | Value |
|---|---|---|
| `problem-space-language` | Language of the problem space – stories, FRs and their scenarios (Gherkin keywords via `# language:`), process files, glossary terms and descriptions, domain map, folder names and slugs of subdomains and business objects – and of everything said to the user | German |
| `solution-space-language` | Language of the solution space – identifiers, code comments, docstrings, commit messages, solution-space documents and the solution-space columns of the glossaries | English |
| `user` | Name of the person answering the grilling | Alex |
| `project-rules` | File with the project's rules: commit convention, feature workflow; a glossary format here overrides the plugin template | `CLAUDE.md` |

Methodology (template headings, field labels, tags, IDs, status values) stays English.

## Problem space

| Key | Meaning | Value |
|---|---|---|
| `problem-space` | Root of the problem space: FRs per subdomain, planned changes in `planned/` below each FR folder | `domain-model/problem-space` |
| `requirements` | User stories: done ones in the folder, open ones (draft, ready, in-progress) in `planned/`, cancelled ones in `cancelled/` | `domain-model/problem-space/requirements` |
| `domain-map` | Subdomains, types, business relationships | `domain-model/problem-space/domain-map.md` |
| `glossaries` | One glossary per subdomain | `domain-model/glossaries` |
| `methodology-glossary` | Methodology terms, among them "Open point" | `domain-model/glossaries/_methodology.md` |

## Code

| Key | Meaning | Value |
|---|---|---|
| `backend` | Backend source root | `backend` |
| `backend-shared` | Cross-cutting backend code, out of scope for the init skills | `backend/core` |
| `backend-tests` | Backend tests | `backend/tests` |

## Ticket system

Optional. The repository stays the source of truth: stories are written one way to the ticket
system by `assets/ticket.md` (fields, description, when), never read
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

## Confluence

Optional. Read by `/design-the-domain:confluence-publish`, which writes the problem space one way to
a Confluence Cloud space; the repository stays the source of truth.

| Key | Meaning | Value |
|---|---|---|
| `confluence-space` | Key of the space the pages go into, or `–` for none | `–` |
| `confluence-parent` | Title of the page the Domain Map page hangs under, or `–` for the top of the space | `–` |
| `confluence-title-prefix` | Prefix of every page title, since titles are unique per space, or `–` | `–` |

## Models

Model of the subagents the skills start: `inherit` (the session's model), `haiku`, `sonnet` or
`opus`. The skills themselves run on the model of whoever calls them; only a subagent's model
can be set per project.

| Key | Meaning | Value |
|---|---|---|
| `model-ground` | Subagent reading the ground in /design-the-domain:domain-interview (reads and summarises) | `inherit` |
| `model-writer` | Subagent running user-story and functional-requirement (finds open points) | `inherit` |
| `model-init` | Subagents of /design-the-domain:domain-init, one per subdomain | `inherit` |
