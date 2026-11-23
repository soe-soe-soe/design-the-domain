# implement-the-domain project config

Template for the part of `domain-model/config.md` the implement-the-domain skills read. It is appended
below the design-the-domain part of the same file (heading `# implement-the-domain`); the keys of
that part (languages, `project-rules`, problem space, `backend`, `backend-shared`, `backend-tests`,
ticket system) are read from there. Everything structural about the code (building blocks, test
levels, markers, seams) stands in the project's structure document (key `structure`).

Scaffold (refactoring 011): no skill fills this part yet; copy it into the project's config by hand.

## Solution space

| Key | Meaning | Value |
|---|---|---|
| `structure` | Target structure of the code: building blocks, naming, test levels and markers | `domain-model/solution-space/structure.md` |
| `context-map` | Generated map of the bounded contexts | `domain-model/solution-space/context-map.md` |
| `context-map-command` | Command that regenerates `context-map` from the code | <command> |
| `refactorings` | Migration plans per bounded context | `refactorings` |
| `adr` | Architecture decision records | `docs/adr` |
| `architecture-adrs` | ADRs on building blocks and boundaries that placement must follow | <ADR numbers> |
| `test-strategy-adr` | ADR on the test strategy | <ADR number> |

## Code (solution space)

| Key | Meaning | Value |
|---|---|---|
| `test-fixtures` | Shared test fixtures, registered in the root `conftest` or equivalent | <path> |
| `e2e-journeys` | UI journeys, one per business object: `‹e2e-journeys›/<subdomain>/<business-object>.<ext>` | <path> |
| `e2e-pages` | Page objects of the UI tests | <path> |
| `scenario-marker` | How a test references its FR scenario | <e.g. a decorator with the scenario ID> |
| `not-implemented` | Body of a shell symbol that has no behaviour yet | <e.g. raise NotImplementedError> |
| `migrations` | Schema migration tool and folder | <tool, path> |

## Commands

Run from the project root; a value may change directory first.

| Key | Meaning | Value |
|---|---|---|
| `typecheck` | Static type check of the backend | <command> |
| `test-all` | Full backend suite | <command> |
| `test-file` | One backend test file | <command with <file>> |
| `test-collect` | Collect backend tests without running them | <command> |
| `e2e-list` | List the UI tests without running them | <command> |
| `e2e-file` | Run one UI test file | <command with <file>> |

## Models

| Key | Meaning | Value |
|---|---|---|
| `model-solution-init` | Subagents of /implement-the-domain:solution-init, one per bounded context | `inherit` |
