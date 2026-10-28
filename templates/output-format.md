# Output format

Shared by the project's skills for what they show the user; not a skill itself. A skill that
uses it says so and reads this file once per session.

## Context block

A message that follows reads of artifacts not yet listed in the session starts with this block,
one item per new artifact, linked to its file. Never listed: the user's prompt (idea text,
ticket link, images), `CLAUDE.md`, and `README.md` or other index files of a folder.

```
**Kontext**
- 📄 glossary: [flaeche.md](domain-model/glossaries/flaeche.md)
- 📘 refactoring: [planungsrecht-zur-flaeche.md](refactorings/planungsrecht-zur-flaeche.md)
- ⚙️ frontend: Abschnitt Planungsrecht in der Projektübersicht
```

## Artifact icons

The type is the artifact's name in the repository; the icon groups. A reference to an artifact
anywhere in a message (e.g. a provenance line) carries the same icon: `📋 FR-fristen-002/S1`.

| Space | Icon | Type | Where |
|---|---|---|---|
| Problem | 📘 | story | `domain-model/problem-space/stories/` |
| Problem | 📋 | FR | `domain-model/problem-space/<subdomain>/` |
| Problem | 📄 | domain-map, glossary, GLOSSARY-MAP | `domain-model/`, `docs/domain/` |
| Solution | 🗂️ | structure, context-map | `domain-model/solution-space/` |
| Solution | 🏛️ | ADR, decision-record | `docs/adr/`, `decision-records/` of a skill |
| Solution | 📘 | refactoring | `refactorings/` |
| Solution | ⚙️ | frontend, backend, migration | code, schema, Alembic |
| Solution | 🧪 | test | `tests/`, journeys |
| External | 🔗 | web | laws, authority sites, documentation |

An artifact of a type not in the table is a document: 📄 with its own type name.

Subdomain, business object, rule or variant are terms, not artifacts: they live in a glossary
or an FR. A reference names artifacts only, never a term (`📄 Verantwortlicher` is wrong).
