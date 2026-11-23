# design-the-domain project config

Template for the project config the design-the-domain skills read. `/design-the-domain:domain-init` fills it in with you; or copy it to `domain-model/config.md` in the project
root and fill in the values; the skills read that file before anything else and stop if it is
missing. The plugin knows no project: every path and convention of a project stands here.

The file may hold more parts below this one: another plugin that works on the same problem space
(e.g. implement-the-domain for the solution space) adds its sections under a heading of its own.
The design-the-domain skills read and fill only the sections of this template.

A skill names a value by its key in angle quotes: `‹requirements›/US-0042-*.md` means the folder
under key `requirements`. Paths are relative to the project root. The values in the table are the
methodology's default layout; keep them unless the project already has another.

## Project

| Key | Meaning | Value |
|---|---|---|
| `problem-space-language` | Language of the problem space – stories, FRs and their scenarios (Gherkin keywords via `# language:`), process files, glossary terms and descriptions, domain map, folder names and slugs of subdomains and business objects – and of everything said to the user | English |
| `solution-space-language` | Language of the solution space – identifiers, code comments, docstrings, commit messages, solution-space documents and the solution-space columns of the glossaries | English |
| `user` | Name of the person answering the grilling | <name> |
| `project-rules` | File with the project's rules: commit convention, feature workflow; a glossary format here overrides the plugin template | `CLAUDE.md` |

Methodology – template headings, field labels, tags, IDs, status values, change kinds, type
folders, report labels of the writers – is English in every project: it is the plugin's structure
and `scripts/requirements.py` parses it. Everything else follows the two language keys; a skill that
writes or says something names the key it follows.

## Problem space

| Key | Meaning | Value |
|---|---|---|
| `problem-space` | Root of the problem space: FRs per subdomain, planned changes in `planned/` below each FR folder | `domain-model/problem-space` |
| `requirements` | User stories: done ones in the folder, open ones (draft, ready, in-progress) in `planned/`, cancelled ones in `cancelled/` | `domain-model/problem-space/requirements` |
| `domain-map` | Subdomains with their types and glossaries, business relationships; the index of the glossaries | `domain-model/problem-space/domain-map.md` |
| `glossaries` | One glossary per subdomain | `domain-model/glossaries` |
| `methodology-glossary` | Methodology terms, among them "Open point" | `domain-model/glossaries/_methodology.md` |

## Code

The code the problem space is taken over from (`/design-the-domain:domain-init`).

| Key | Meaning | Value |
|---|---|---|
| `backend` | Backend source root | <path> |
| `backend-shared` | Cross-cutting backend code, out of scope for the init skills | <path> |
| `backend-tests` | Backend tests | <path> |

## Ticket system

Optional. The repository stays the source of truth: stories are written one way to the ticket
system by `${CLAUDE_PLUGIN_ROOT}/assets/ticket.md` (fields, description, when), never read
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
