# Glossary format

One glossary per subdomain, `‹glossaries›/<subdomain>.md`, as a table. The table is the bridge
between problem and solution space: the left columns are the business language, the right
columns the name the code gives it. `pts:solution-definition` and `pts:test-definition` read the
right columns; `pts:problem-init` fills both from existing code.

## Structure

```md
# Fristen

Stichtage in Projekten und persönlich und was an Projekten als Problem auffällt.

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | Fristen | Bounded Context | `deadlines`; folders: `deadlines` | Stichtage, ihre Verantwortlichen und die Problemsignale je Projekt. |

## Manuelle Frist

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | Manuelle Frist | Aggregate Root | `ManualDeadline` | Ein von Hand gepflegter Stichtag mit Verantwortlicher. Avoid: Termin, Aufgabe |
| Value | Erledigt | Value Object | `done_at` | Zeitpunkt, zu dem die Frist abgehakt wurde. |
```

- **The `Subdomain` row** comes first and names the bounded context and its folders in the code:
  `` `economics`; folders: `calculations`, `costs` ``. It is the bridge for the code structure.
- **One section per business object**, headed by its name, starting with its `Business Object`
  row (`Aggregate Root` in the solution space). Terms without a business object stay in the
  first table.
- **Problem space and Solution space** columns use the DDD types of `‹methodology-glossary›`
  (*Glossary type*): Business Object, Entity, Value, Derived Concept, Domain Event, Command,
  Query … on the left; Aggregate Root, Entity, Value Object, Domain Service, Policy … on the
  right.
- **Identifier** is the code name, English, empty until it is decided.
- **Description** in `‹content-language›`, one or two sentences: what it IS, not what it does.
  Words to avoid go at its end as `Avoid: …`.

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list
  the others under `Avoid:`.
- **Keep definitions tight.** One or two sentences max.
- **Only include terms specific to this domain.** General programming concepts (timeouts, error
  types, utility patterns) don't belong even if the project uses them extensively.
- **A new term is a new row.** Change an existing row only when the user settled its meaning anew.

## Glossary map

`‹glossary-map›` lists the glossaries and points to the domain map and the context map:

```md
# Glossary Map

- [Fristen](domain-model/glossaries/fristen.md): Stichtage und Problemsignale
- [Genehmigung](domain-model/glossaries/genehmigung.md): Antrag, Nachweise und Kosten
- Subdomains and their relationships: [domain-map.md](domain-model/problem-space/domain-map.md)
- Bounded contexts in the code: [context-map.md](domain-model/solution-space/context-map.md)
```
