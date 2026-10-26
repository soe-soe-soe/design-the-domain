# Solution-space structure

The backend structure *is* the solution model: the context map
(`domain-model/solution-space/context-map.md`) is generated from folders, files and imports, so
every building block has exactly one place. This file is the single source for where code and
its tests go and how they are named; skills and `backend/domain/CLAUDE.md` point here. Terms as
in `domain-model/glossaries/_methodology.md`.

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
- **One building block per file.** No file for a pure forward: facade methods stay in one file.
- **Same names on both levels**; context level means "spanning several aggregates". Root,
  entities, invariants, events and persistence exist at aggregate level only. An invariant
  spanning two aggregates signals a wrong aggregate cut.
- **Folders appear when needed**: an empty building block gets no folder.
- **Building blocks under `model/` are pure**: no database, no HTTP, no SQLAlchemy (ADR 008).
  Commands and queries use repositories through the port.
- **Boundaries** (ADR 009): another context calls only `facade/`; the frontend only `api/`.
  Inside a context, direct imports are fine, also across its folders while it still spans
  several.

## Naming

All names English, `snake_case` for folders, files and functions, `PascalCase` for classes.

| Building block | Folder / file | File name | Main symbol |
|---|---|---|---|
| Bounded context | `backend/domain/<context>/` | as in the glossary's subdomain row (`permits`, `economics`) | – |
| Aggregate | `aggregates/<aggregate>/` | singular noun (`evidence`, `procedure`) | – |
| Aggregate root | `model/root.py` | fixed | class named after the aggregate (`Evidence`) |
| Entity, value object | `model/entities/`, `model/value_objects/` | singular noun (`history_entry.py`, `evidence_status.py`) | class of the same name (`HistoryEntry`, `EvidenceStatus`) |
| Invariant | `model/invariants/` | the rule as a noun phrase (`permitted_transitions.py`) | function `check_<rule>` raising a domain error |
| Specification | `model/specifications/` | the predicate (`is_completed.py`, `is_overdue.py`) | function of the same name returning `bool` |
| Factory | `model/factories/` | `create_<aggregate>.py` | function `create_<aggregate>` |
| Domain service | `model/services/` | what it derives (`application_progress.py`) | function `calculate_<thing>` or `derive_<thing>` |
| Domain event | `model/events/` | past tense (`evidence_rejected.py`) | dataclass `EvidenceRejected` |
| Repository | `model/repository.py`, `persistence/repository.py` | fixed | port `<Aggregate>Repository` (`Protocol`), adapter `Sql<Aggregate>Repository` |
| Command | `application/commands/` | imperative verb + object (`reject_evidence.py`) | function of the same name |
| Query | `application/queries/` | what it returns (`project_signals.py`) | function `get_<thing>` |
| Policy | `application/policies/` | `on_<event>.py` (`on_deadline_done.py`) | function of the same name |
| Endpoint | `api/endpoints/` | same name as its command or query | FastAPI route function of the same name |
| Schema | `api/schemas/` | per resource (`evidence.py`) | `<Thing>Request`, `<Thing>Response` |
| Facade | `facade/facade.py` | fixed | class `<Context>Facade`, one method per use case |
| Facade type | `facade/types/` | singular noun | dataclass of the same name |
| Adapter | `adapters/<system>/` | `client.py` plus mapping files | class `<System>Client` |

## Tests

A test mirrors the code it tests: `backend/tests/<unit|integration>/domain/<context>/<path of
the building block>/test_<file>.py`. Unit tests cover building blocks under `model/` without a
database; integration tests go through `api/` or `facade/` with the database. A test that proves
an FR scenario carries `@pytest.mark.fr("FR-<subdomain>-NNN/Sn")`; each scenario has exactly one
main test.

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
`schemas.py`, rules under `regeln/`) and ADR 008/009; solution-sync names the target path as
well, so the migration finds it.
