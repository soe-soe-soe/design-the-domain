# Fristen

Stichtage in Projekten und persönlich und was an Projekten als Problem auffällt.

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | Fristen | Bounded Context | `deadlines`; folders: `deadlines` | Stichtage, ihre Verantwortlichen und die Problemsignale je Projekt. |
| Business Object | Frist | Aggregate Root | `Deadline` | Ein Stichtag mit Fälligkeitsdatum, Verantwortlicher und Erledigt-Status. |
| Derived Concept | Überfällig | Domain Service | `is_overdue` | Eine offene Frist, deren Fälligkeit verstrichen ist; ab welchem Tag, regelt FR-fristen-001. |
| Derived Concept | Problemsignal | Domain Service | `ProjectSignals` | Was in der Projektübersicht an einem Projekt als Problem auffällt: überfällige Fristen und als Problem gekennzeichnete Fristen. |
| Value | Problem | Value Object | `problem` | Kennzeichnung einer Frist als Problem. Ein Problem hat immer eine Notiz, die es begründet; ohne Notiz kann eine Frist nicht als Problem gekennzeichnet werden. |
| Value | Notiz | Value Object | `note` | Freitext an einer Frist. |
