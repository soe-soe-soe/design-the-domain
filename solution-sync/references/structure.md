# Solution-space structure

The backend structure *is* the solution model: the context map
(`domain-model/solution-space/context-map.md`) is generated from folders, files and imports, so
every building block has exactly one place. Terms as in `domain-model/glossaries/_methodology.md`.

## Target layout of a bounded context

```
backend/domain/<context>/                 bounded context, named in the subdomain row of its glossary
├── api/                                  frontend and external systems
│   ├── __init__.py                       registers all endpoints, in route order
│   ├── endpoints/<use_case>.py           one endpoint per file, calls one command or query
│   └── schemas/                          request and response schemas
├── facade/                               other bounded contexts, in process
│   ├── facade.py                         one class, thin forwards to commands and queries
│   └── types/                            types crossing the boundary, one file each
├── model/                                spanning several aggregates
│   ├── value_objects/
│   ├── specifications/
│   └── services/                         domain services
├── application/                          spanning several aggregates
│   ├── commands/                         only flows across aggregates, sparingly
│   ├── queries/
│   └── policies/
├── adapters/<system>/                    anti-corruption layer to a foreign system (ALKIS, Auth0)
└── aggregates/<aggregate>/               one folder per aggregate, English singular
    ├── model/
    │   ├── root.py                       aggregate root
    │   ├── entities/
    │   ├── value_objects/
    │   ├── invariants/
    │   ├── specifications/
    │   ├── factories/
    │   ├── events/
    │   ├── services/                     domain services of this aggregate
    │   └── repository.py                 port
    ├── application/
    │   ├── commands/
    │   ├── queries/
    │   └── policies/                     reactions that change this aggregate
    └── persistence/
        └── repository.py                 adapter (SQLAlchemy)
```

Rules:
- **One building block per file**, file name = what it does (`reject_evidence.py`,
  `permitted_transitions.py`). No file for a pure forward: facade methods stay in one file.
- **Same names on both levels**; context level means "spanning several aggregates". Root,
  entities, invariants, events and persistence exist at aggregate level only. An invariant
  spanning two aggregates signals a wrong aggregate cut.
- **Folders appear when needed**: an empty building block gets no folder.
- **Building blocks under `model/` are pure**: no database, no HTTP, no SQLAlchemy (ADR 008).
  Commands and queries use repositories through the port.
- **Boundaries** (ADR 009): another context calls only `facade/`; the frontend only `api/`.
  Inside a context, direct imports are fine, also across its folders while it still spans
  several.

## FR type → building block

| FR type | Building block | Aggregate level | Context level |
|---|---|---|---|
| Invariant | Invariant | `model/invariants/` | – (wrong cut) |
| Domain Service | Domain service or specification | `model/services/`, `model/specifications/` | `model/services/`, `model/specifications/` |
| Policy | Policy, triggered by a domain event | `application/policies/` of the aggregate it changes | `application/policies/` |
| Command | Command (+ factory when it creates) | `application/commands/`, `model/factories/` | `application/commands/` |
| Query | Query | `application/queries/` | `application/queries/` |
| Anti-Corruption Layer | Adapter to a foreign system | – | `adapters/<system>/` |

A domain event that a command raises goes to `model/events/` of the raising aggregate; the
scenario "event occurs" belongs to the command.

## Contexts not yet migrated

A context is migrated once its folder has `aggregates/`. Until then, new code follows the
folder's current layering (`models.py`, `repository.py`, `service.py`, `router.py`,
`schemas.py`, rules under `regeln/`) and ADR 008/009, and the placement names the target path
as well, so the migration finds it.
