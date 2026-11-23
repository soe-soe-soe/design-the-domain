# Fristen

Stichtage in Projekten und persönlich.

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | Fristen | Bounded Context | `deadlines`; folders: `deadlines` | Stichtage und ihre Erinnerungen. |

## Frist

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | Frist | Aggregate Root | `Deadline` | Ein Stichtag mit Fälligkeitsdatum und Erledigt-Status. |

## Erinnerung

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | Erinnerung | Aggregate Root | `Reminder` | Eine Mitteilung, die vor der Fälligkeit einer Frist an deren Verantwortlichen geht. |
