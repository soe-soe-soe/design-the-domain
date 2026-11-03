# Ticket template

Shared by `/pts:problem-definition` and `/pts:story-workflow` when `‹ticket-system›` is not
`none`; not a skill itself. Values in angle quotes are keys of the project config
`.claude/pts.md`. The ticket system is reached through the project's connector for it (e.g. the
Linear MCP server).

## Rules

- **The repository is the source of truth.** Sync goes one way, story → ticket. Nothing is read
  back from the ticket; edits to its fields are overwritten by the next sync, comments stay and
  are never read.
- **One ticket per story,** draft stories included. Its ID goes into the story header as
  `External: <ID>` (e.g. `External: VIN-123`) when the ticket is created; a story with an
  `External` ID is updated, never created twice.
- **Every sync writes all fields** of the table below, the description and the link included –
  so the link follows the file when it moves from `planned/` to `‹requirements›/` or
  `cancelled/`.

## When

| Moment | Who | Sync |
|---|---|---|
| Session closes | `/pts:problem-definition` step 4 | every story of the session: create without `External`, update with |
| Story cancelled | `/pts:problem-definition` after `requirements.py cancel` | the story, status cancelled, link into `cancelled/` |
| Implementation starts | `/pts:story-workflow` step 1 | the story, status in-progress |
| Story done | `/pts:story-workflow` step 7, after `requirements.py complete` | the story, status done, link into `‹requirements›/` |

## Fields

| Field | Value |
|---|---|
| Title | `US-0042: <story title>` |
| Team | `‹ticket-team›` |
| Project | `‹ticket-project›`; none for `–` |
| Assignee | `‹ticket-assignee›`; none for `–` |
| Labels | one per subdomain of the story's FRs (`## Functional requirements`), named as in the column `Subdomain` of `‹domain-map›`; a provisional subdomain takes its host's label. A label missing in the ticket system: see *Missing label*. None when `‹ticket-labels›` is `–`. |
| Status | the story status mapped by the table *Ticket status* in `.claude/pts.md` |
| Description | the template below, its texts in `‹problem-space-language›` |

## Missing label

Before the sync, compare the labels the stories need with those of `‹ticket-team›`. For the
missing ones ask the user once, all in one question (AskUserQuestion, multi-select): which to
create in `‹ticket-team›`, named exactly as in `‹domain-map›`. Create the confirmed ones through
the connector, then sync. A label the user declines is left off the ticket and named in the
report; the next sync asks again. Never create a label without that answer.

## Description

````markdown
<role sentence of the story: As … I want …>

**<Why>:** <section Why of the story>

**<Acceptance criteria>:**
- AC1 – <title of the scenario>
- AC2 – <title of the scenario>

**Functional Requirements:** FR-deadlines-002 (edit), FR-deadlines-004 (new)

**<Open points>:** <number of entries under ## Open; line left out without open points>

**<Source>:** [US-0042-<slug>.md](<‹repository-url›>/<path of the story file>)
````

Labels in angle brackets are written in `‹problem-space-language›` (e.g. „Warum“, „Akzeptanzkriterien“,
„Offene Punkte“, „Quelle“ for German). Acceptance criteria as titles only, never Gherkin: the
scenarios live in the repository. Dropped ACs are left out.
