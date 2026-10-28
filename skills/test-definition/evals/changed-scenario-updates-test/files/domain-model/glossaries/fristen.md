# Fristen

Stichtage in Projekten und persönlich und was an Projekten als Problem auffällt.

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | Fristen | Bounded Context | `deadlines`; folders: `deadlines` | Stichtage, ihre Verantwortlichen und die Problemsignale je Projekt. |
| Derived Concept | Problemsignal | Query | `DeadlineService.get_signals` | Was in der Projektübersicht an einem Projekt als Problem auffällt: überfällige Fristen und Nachweise mit Problem. |
