# Fristen

Stichtage in Projekten und persönlich.

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | Fristen | Bounded Context | `deadlines`; folders: `deadlines` | Stichtage und ihre Verantwortlichen. |

## Frist

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | Frist | Aggregate Root | `Deadline` | Ein Stichtag mit Fälligkeitsdatum und Erledigt-Status. |
| Value | Priorität | Value Object | `priority` | Wie dringend eine Frist ist: hoch, normal oder niedrig. |
