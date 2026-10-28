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

Why it is this way: ADR 012. A test mirrors the code it tests:
`backend/tests/domain/<context>/<path of the building block>/test_<file>.py`. It imports the
building block from that path, so it turns green only where the placement put the code. The
tree under `backend/tests/` is the tree under `backend/` minus what has no test of its own
(repository, endpoint, schema), plus the test infrastructure:

```
backend/tests/
├── conftest.py               registers the plugins below (pytest_plugins), nothing else
├── plugins/levels.py         marks each test unit or integration from its path
├── fixtures/<concern>.py     shared fixtures, one module per concern (database.py)
├── core/                     mirrors backend/core/
├── ops/migrations/           mirrors backend/ops/migrations/
└── domain/<context>/
    ├── conftest.py           builders make_<aggregate> of this context
    ├── facade/test_facade.py
    └── aggregates/<aggregate>/model/…, application/…
```

**Level from the path:** under `domain/`, a path through `model/` is a unit test, any other an
integration test; `ops/` is integration, the rest unit. `tests/plugins/levels.py` sets the
marker, CI and local runs select with `pytest -m unit` or `pytest -m integration`. The level is
never a folder.

**Not-migrated context:** its tests stay in the former layout
`backend/tests/<unit|integration>/domain/<context>/test_<current file>.py`, where the folder
names the level, and move to the mirrored path with the migration of their context. A new test
in such a context goes there as well.

**Scenario test:** proves one FR scenario, `@pytest.mark.fr("FR-<subdomain>-NNN/Sn")`, exactly
one main test per scenario. **Interface test:** checks a facade method a story adds or changes,
`@pytest.mark.story("US-NNNN")`. Further tests the implementation needs (helpers, edge cases
below a scenario) carry no marker.

| Building block | Test level | Seam | Scenario test | Interface test |
|---|---|---|---|---|
| Invariant, specification, domain service, value object, factory | Unit | the function or class in `model/` | for FR types Invariant, Domain Service | – |
| Command (with the domain event it raises) | Integration | its endpoint in `api/`, else the facade | for FR type Command | – |
| Query | Integration | its endpoint in `api/`, else the facade | for FR type Query | – |
| Policy | Integration | the command that raises the event, effect read through the facade | for FR type Policy | – |
| Facade method | Integration | `facade/facade.py` | – | each new or changed method |
| Adapter | Integration with a fake of the foreign system | the `<System>Client` | for FR type Anti-Corruption Layer | – |
| Migration | Integration | `alembic upgrade` on seeded data | for FR type Data Migration | – |
| Repository, endpoint, schema | – | covered by the tests above | – | – |

- **Not-migrated context:** the seam is the method the placement names (e.g.
  `DeadlineService.get_signals`) as long as the context has no endpoint or facade for it.
- **Test data:** everything the scenario names (its Angenommen) stands visibly in the test
  body, with the scenario's literal values; a reader checks the test against the scenario
  without opening a fixture. Wiring – database session, repositories, facades, services, API
  client – comes from fixtures: shared ones in `tests/fixtures/`, a context's own in the
  `conftest.py` of its test folder. An aggregate built in several tests
  gets a builder fixture `make_<aggregate>` in its context's `conftest.py`: keyword arguments for
  what a scenario names, defaults for everything else. Unit tests construct values and
  aggregates directly. Integration tests store the arranged state through the repository or a
  command, never through SQL – except a migration test, whose seam is the stored data. "Heute"
  is passed in as a fixed date, never read from the clock.
- **Names:** `test_<scenario statement in English, snake_case>`, e.g.
  `test_deadline_is_overdue_from_due_date`; the ID stands in the marker. A Szenariogrundriss
  becomes one test parametrised over its Beispiele.
- **Migrations:** the test of a migration lives at
  `backend/tests/ops/migrations/versions/test_<file>.py`. Once, globally,
  `backend/tests/ops/migrations/test_migration_chain.py` runs every revision up and
  down and checks with `alembic check` that models and migrations agree.
- **Before the implementation** the tests are red: the shell raises `NotImplementedError`. They
  are committed together with the implementation, never `xfail`.

### End-to-end

One **journey** per business object with a UI: `frontend/e2e/journeys/<subdomain>/<business
object>.spec.ts` (`genehmigung/nachweis.spec.ts`), one `test.describe.serial` along the life
cycle on the happy path. A story that changes what a user does or sees adds or changes one step
(`test(...)` with tag `{ tag: '@US-NNNN' }`); variants and edge cases stay in backend tests.
Setup (log-in, data the step does not cover) goes through the API, not through clicks; pages are
driven through page objects in `frontend/e2e/pages/`. `smoke.spec.ts` runs on every commit, the
journeys before a deploy.

## FR type → building block

| FR type | Building block | Aggregate level | Context level |
|---|---|---|---|
| Invariant | Invariant | `model/invariants/` | – (wrong cut) |
| Domain Service | Domain service or specification | `model/services/`, `model/specifications/` | `model/services/`, `model/specifications/` |
| Policy | Policy, triggered by a domain event | `application/policies/` of the aggregate it changes | `application/policies/` |
| Command | Command (+ factory when it creates) | `application/commands/`, `model/factories/` | `application/commands/` |
| Query | Query | `application/queries/` | `application/queries/` |
| Anti-Corruption Layer | Adapter to a foreign system | – | `adapters/<system>/` |
| Data Migration | Alembic migration | – | `backend/ops/migrations/versions/` |

A domain event that a command raises goes to `model/events/` of the raising aggregate; the
scenario "event occurs" belongs to the command.

## Contexts not yet migrated

A context is migrated once its folder has `aggregates/`. Until then, new code follows the
folder's current layering (`models.py`, `repository.py`, `service.py`, `router.py`,
`schemas.py`, rules under `regeln/`) and ADR 008/009; solution-definition names the target
path as well, so the migration finds it.
