<!--
Glossary of one subdomain – ‹glossaries›/<subdomain>.md, file name as the subdomain folder
(lower case, umlauts spelled out). A glossary format in ‹project-rules› overrides this template.

- One table per section, always these five columns. Term and Description in ‹content-language›,
  Identifier as in the code (English).
- The first table holds the Subdomain row (folders: the code folders of the bounded context) and
  the terms that belong to no business object (values, derived concepts of the subdomain).
- One section `## <Business Object>` per business object with an aggregate root; its first row is
  the Business Object, then its entities, values, domain events, commands and queries.
- Problem space → usual Solution space: Subdomain → Bounded Context, Business Object → Aggregate
  Root, Entity → Entity, Value → Value Object, Domain Event → Domain Event, Command → Command,
  Query → Query, Derived Concept → Domain Service or Query.
- Solution space and Identifier stay empty until solution-definition decides them.
- Description: what the term means in business terms, one or two sentences; terms to avoid as
  `Avoid: …`. No rules – they stand in the FRs.
This comment is not copied into a glossary.
-->
# <Subdomäne>

<Wofür die Subdomäne fachlich steht, ein Satz.>

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | <Subdomäne> | Bounded Context | `<context>`; folders: `<folder>` | <was fachlich dazugehört> |

## <Business Object>

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | <Begriff> | Aggregate Root | `<Class>` (`<path>`) | <Bedeutung>. Avoid: <Synonym>. |
| Value | <Begriff> | Value Object | `<Class>` | <Bedeutung, bei Aufzählungen die Werte> |
| Command | <Begriff> | Command | `<function>` | <was sich fachlich ändert> |
