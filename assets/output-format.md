# Output format

Shared by the define-the-domain skills for what they show the user; not a skill itself. A skill that uses it
says so and reads this file once per session. Values in angle quotes are keys of the project
config `.claude/pts.md`.

## Context block

A message that follows reads of artifacts not yet listed in the session starts with this block,
one list item per new artifact, linked to its file – never several artifacts in one item, not even
files of the same type. Never listed: the user's prompt (requirement text,
ticket link, images), `‹project-rules›`, and `README.md` or other index files of a folder.

The heading and the descriptions are in ‹problem-space-language› (English here).

```
**Context**
- 📄 glossary: [area.md](domain-model/glossaries/area.md)
- 📘 refactoring: [planning-law-to-area.md](refactorings/planning-law-to-area.md)
- ⚙️ frontend: planning law section in the project overview
```

## Artifact icons

The type is the artifact's name in the repository; the icon groups. A reference to an artifact
anywhere in a message (e.g. a provenance line) carries the same icon: `📋 FR-deadlines-002/S1`.

| Space | Icon | Type | Where |
|---|---|---|---|
| Problem | 📘 | story | `‹requirements›/` and its `planned/`, `cancelled/` |
| Problem | 📋 | FR | `‹problem-space›/<subdomain>/`, planned changes in its `planned/` |
| Problem | 📄 | domain-map, glossary, glossary-map | `‹domain-map›`, `‹glossaries›`, `‹glossary-map›` |
| Solution | 🗂️ | structure, context-map | `‹structure›`, `‹context-map›` |
| Solution | 🏛️ | ADR, decision-record | `‹adr›`, `decision-records/` of a skill |
| Solution | 📘 | refactoring | `‹refactorings›` |
| Solution | ⚙️ | frontend, backend, migration | code, schema, `‹migrations›` |
| Solution | 🧪 | test | `‹backend-tests›`, `‹e2e-journeys›` |
| External | 🔗 | web | laws, authority sites, documentation |

An artifact of a type not in the table is a document: 📄 with its own type name.

Subdomain, business object, rule or variant are terms, not artifacts: they live in a glossary
or an FR. A reference names artifacts only, never a term (`📄 responsible person` is wrong).
