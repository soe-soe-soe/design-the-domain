<!--
Glossary of one subdomain – ‹glossaries›/<subdomain>.md, file name as the subdomain folder
(lower case, umlauts spelled out). A glossary format in ‹project-rules› overrides this template. Headings of the table columns and
the Problem space / Solution space kinds are methodology (English); the placeholders are English.

- One table per section, always these five columns. Term and Description in ‹problem-space-language›,
  Solution space and Identifier in ‹solution-space-language› as in the code.
- The first table holds the Subdomain row (folders: the code folders of the bounded context) and
  the terms that belong to no business object (values, derived concepts of the subdomain).
- One section `## <Business Object>` per business object with an aggregate root; its first row is
  the Business Object, then its entities, values, domain events, commands and queries.
- Problem space → usual Solution space: Subdomain → Bounded Context, Business Object → Aggregate
  Root, Entity → Entity, Value → Value Object, Domain Event → Domain Event, Command → Command,
  Query → Query, Derived Concept → Domain Service or Query.
- Solution space and Identifier stay empty until the code name is decided: from code by
  problem-space-initialization, otherwise by the implementing plugin through the interface of the skill glossary.
- Description: what the term means in business terms, one or two sentences; terms to avoid as
  `Avoid: …`. No rules – they stand in the FRs.
This comment is not copied into a glossary.
-->
# <subdomain>

<What the subdomain stands for in business terms, one sentence.>

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | <subdomain> | Bounded Context | `<context>`; folders: `<folder>` | <what belongs to it in business terms> |

## <Business Object>

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | <term> | Aggregate Root | `<Class>` (`<path>`) | <meaning>. Avoid: <synonym>. |
| Value | <term> | Value Object | `<Class>` | <meaning; for an enumeration its values> |
| Command | <term> | Command | `<function>` | <what changes in business terms> |
