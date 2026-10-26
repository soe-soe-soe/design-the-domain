# Placement US-NNNN: <story title>

Status: draft · Story: [US-NNNN](../../problem-space/stories/US-NNNN-<slug>.md) · Date: YYYY-MM-DD

## Scenarios

| Scenario | Type | Context / aggregate | Building block | File |
|---|---|---|---|---|
| FR-<subdomain>-NNN/Sn | <FR type> | <context> / <aggregate or –> | <building block> | <path under backend/domain/> (new \| exists) |

## Interfaces

- api: <METHOD /path> → <command or query file>
- facade: <Facade.method> (new \| changed), used by <context>
- event: <EventName> (<file>), raised by <command>, handled by <policy>

## Schema

- <table.column> (<type>, <nullable>) – Alembic migration

## Glossary

- <glossary>.md „<Begriff>“ → <solution-space type>, `<identifier>`

## Open

- **Question n:** <what waits for an answer> – blocks: <scenarios>
