# Methodology

Terms of the method: how requirements, acceptance criteria, code and tests come about and connect. Unlike the subdomain glossaries it describes no business domain, so it has no problem-space and solution-space columns.

## Structure

**Problem space**:
What the business requires, independent of software. Its content is German and lives under `domain-model/problem-space/`.
_Avoid_: Fachseite, business side
_Code_: `domain-model/problem-space/`

**Solution space**:
How the code implements the business. Its content is English and is the code itself; its documents are the target structure and the generated context map.
_Code_: `backend/domain/`, `domain-model/solution-space/structure.md`, `domain-model/solution-space/context-map.md`

**Bridge**:
What connects problem and solution space. Three bridges, each for one kind of link: the glossaries for terms, the subdomain row of each glossary for structure (subdomain → bounded context → folders), and the tests for behaviour. There is no separate mapping document.
_Code_: `domain-model/glossaries/`, `@pytest.mark.fr`

**Language rule**:
Names follow their origin. Methodology (artefact types, structural folders, IDs, tags, status values, template headings) is English; problem-space content (subdomains, business objects, slugs, rules, scenarios) is German; solution-space content (identifiers, comments, docstrings, commits) is English. Prose in problem-space documents is German. Everything shown in the UI is German.

**Domain**:
The whole business field, wind farm project development. It has no instance in the application.
_Avoid_: Projekt (an aggregate of the subdomain Projekt)

**Subdomain**:
A part of the domain in the problem space, e.g. Genehmigung or Fristen. It is implemented by exactly one bounded context; until the code is restructured, that context may still span several folders. A functional requirement touching several subdomains belongs to the triggering one.
_Avoid_: module, area, domain
_Code_: folder `domain-model/problem-space/<subdomain>/`, glossary `domain-model/glossaries/<subdomain>.md`, row in `domain-model/problem-space/domain-map.md`

**Provisional subdomain**:
A subdomain with too little content for a folder of its own, e.g. Ausschreibung or Bau. It lives in the folder of the subdomain that hosts it today, as `subdomain-<name>/` with a README describing the extraction; its terms sit in their own section of the host's glossary, and the domain map lists it as provisional.
_Code_: `domain-model/problem-space/<subdomain>/subdomain-<name>/`

**Domain map**:
The problem-space overview: every subdomain with its type (Core, Supporting, Generic), its status and the business relationships between subdomains. Maintained by hand.
_Avoid_: context map (that is the solution-space counterpart)
_Code_: `domain-model/problem-space/domain-map.md`, template `assets/domain-map.md` of `problem-space-fr`

**Bounded context**:
The boundary in the solution space within which a model and its names are unambiguous. Its name is the English translation of its subdomain; the subdomain row of the glossary names it and the folders that implement it today.
_Avoid_: context alone (ambiguous), domain (for a folder under `backend/domain/`)
_Code_: `backend/domain/<context>/`, row `Subdomain | … | Bounded Context | \`<context>\`; folders: …`

**Context map**:
The solution-space overview: bounded contexts, their aggregates and building blocks, and which context calls which through its facade. Generated from the glossary rows and the code, never edited by hand.
_Code_: `domain-model/solution-space/context-map.md`, generator `backend/ops/generate_context_map.py`

**Target structure**:
Where every building block of the solution space and its test live and how they are named. The single source for placing code; skills and `backend/domain/CLAUDE.md` point to it.
_Avoid_: placement (the per-story result of solution-definition, given in conversation only)
_Code_: `domain-model/solution-space/structure.md`

**Business object**:
A central object of a subdomain that changes independently of others, e.g. Nachweis or Antrag. In the glossary it is a Business Object with an Aggregate Root; its parts (history, contacts) get no folder.
_Avoid_: entity, record
_Code_: folder `domain-model/problem-space/<subdomain>/<business-object>/`, section in the subdomain glossary

**Glossary type**:
The classification of every term of a subdomain glossary, once per space. Problem space: Subdomain, Business Object, Value, Domain Event, Command, Policy, Derived Concept, Reference Data, Role. Solution space: Bounded Context, Aggregate Root, Entity, Value Object, Invariant, Specification, Factory, Domain Event, Domain Service, Command, Query, Policy, Repository, Anti-Corruption Layer, Reference Data, Permission or –.
_Code_: columns "Problem space" and "Solution space" of the glossary tables

## Solution-space building blocks

**Aggregate**:
A cluster of objects that only changes together and consistently; one transaction changes one aggregate. Other aggregates refer to it by ID only. Each aggregate has exactly one aggregate root, the only entry from outside.
_Code_: `backend/domain/<context>/aggregates/<aggregate>/`, root in `model/root.py`

**Invariant**:
A rule that must hold for an aggregate at all times, e.g. permitted status transitions. It defines the aggregate's boundary, so it exists at aggregate level only.
_Code_: `model/invariants/`

**Specification**:
A predicate telling whether something meets a condition, e.g. "gilt als abgeschlossen".
_Code_: `model/specifications/`

**Factory**:
Creates an aggregate with its defaults, e.g. a new Antrag with its Basisnachweise.
_Code_: `model/factories/`

**Domain service**:
A stateless calculation that belongs to no single entity, e.g. Antragsfortschritt. It answers a question and changes nothing.
_Code_: `model/services/`

**Domain event**:
A business fact other parts react to, e.g. "Frist erledigt". It arises in exactly one aggregate. It is not a functional requirement of its own: that it occurs is a scenario of the triggering command, each reaction is a functional requirement of type Policy.
_Code_: `model/events/`; today without event classes, e.g. `DeadlineEvent` in `permits/facade.py`

**Command**:
A use case that changes an aggregate, e.g. "Nachweis ablehnen".
_Code_: `application/commands/`

**Query**:
A use case that only reads, e.g. "Termine der Startseite".
_Avoid_: read model
_Code_: `application/queries/`

**Policy**:
A reaction to a domain event: "whenever X happens, do Y". It calls a command and may use a domain service.
_Avoid_: rule (for the folder), service
_Code_: `application/policies/`

**Repository**:
Loads and saves whole aggregates through their root and hides the database; one per aggregate. Its interface is the port, its SQLAlchemy implementation the adapter.
_Code_: port `model/repository.py`, adapter `persistence/repository.py`

**Facade**:
The interface of a bounded context for other bounded contexts, in process. One file of thin forwards to commands and queries, plus the types that cross the boundary.
_Code_: `facade/facade.py`, `facade/types/`

**API**:
The interface of a bounded context for the frontend and external systems: one endpoint per file, each calling exactly one command or query, plus the request and response schemas.
_Code_: `api/endpoints/`, `api/schemas/`, registration order in `api/__init__.py`

**Building-block level**:
The same building-block names exist at aggregate level and at bounded-context level; at context level they mean "spanning several aggregates". Root, entities, invariants, domain events and persistence exist at aggregate level only.
_Code_: `backend/domain/<context>/{model,application}/` beside `aggregates/`

## Requirements

**User story**:
A business change with its why and its acceptance criteria, born in a grill session. It records what should change, not the current state: once done it stays unchanged, a later change is a new story. It names the functional requirements it changes, with the kind of change and which AC became which scenario. Status flow `draft ⇄ ready → in-progress → done`, each open status `→ cancelled`; done and cancelled are final. A changed `ready` or `in-progress` story falls back to `draft`. The checks per transition stand in the comment of the story template.
_Avoid_: ticket, requirement (for the story)
_Code_: `domain-model/problem-space/requirements/US-NNNN-<slug>.md` (done), `requirements/planned/` (draft, ready, in-progress), `requirements/cancelled/`; header fields `Status`, `createdAt`, `doneAt`, `External` (ID in a ticket system); section `## Functional requirements`; template `assets/story.md` of `problem-space-story`

**Acceptance criterion (AC)**:
A testable behaviour of a user story, written as a German Gherkin scenario with exactly one trigger. Its number stays fixed even if it is dropped.
_Avoid_: test case (the test comes later)
_Code_: `Szenario: ACn – …` in the story, reference `US-NNNN/ACn`

**Open point**:
Something a story or an FR cannot decide without an answer: in a story a gap that changes the outcome of an acceptance criterion (problem-space-story), in a planned FR a contradiction with the existing state (problem-space-fr); an active FR never carries one. The writers only mark it; `/requirement` asks it – FR points in the next round, story points in the closing round – and the user may defer it. One format in stories and FRs: the concerned scenario or AC carries the tag `@open` – an open point under `## Open` concerns it. A new scenario or AC whose outcome hangs on the answer has no Dann; an existing one keeps its Dann until the answer is in, and no other scenario states a contradicting Dann meanwhile. The artefact lists the point under `## Open` as
`- **<ACn or Sn>** (<source skill>): <Frage, mit „ja“ annehmbar> – Recommendation: <Antwort> – <Field>: <value> · …`
with the fields `Changes` (story) or `Story`, `Case`, `Type` and, for case glossary, `Glossary` (FR). Question and recommendation are German, labels English.
_Avoid_: assumption (nothing is guessed)
_Code_: tag `@open`, section `## Open` in the story or planned FR

**Functional requirement (FR)**:
The implemented target state of one business rule or capability (the active FR), assigned to exactly one subdomain and, if it hangs on one, to one business object. Stories change it through a planned FR; only completing the story merges the change in. It keeps no history: which stories changed it follows from the done stories that name it (`requirements.py history`). It contains no code locations: the link to the code is the test.
_Avoid_: specification, feature
_Code_: `domain-model/problem-space/<subdomain>/<business-object>/FR-<subdomain>-NNN-<slug>.md` (rules of a value without own business object directly in the subdomain folder), `Status: valid` or `obsolete`, template `assets/functional-requirement.md` of `problem-space-fr`

**Planned FR**:
The changes of a functional requirement not implemented yet, next to the active FR in `planned/`: one file per FR for every story touching it. A line per story names the kind – new (the FR does not exist yet), edit, deletion (the whole FR becomes obsolete) – and whether the rule text changes; below stand only the scenarios a story changes, adds or drops, numbered as in the active FR. `requirements.py complete` merges one story's changes into the active FR when the story is done; `requirements.py cancel` drops them.
_Avoid_: delta FR (as a file per story)
_Code_: `<FR folder>/planned/FR-<subdomain>-NNN-<slug>.md` (same file name as the active FR), `Status: planned`, section `## Changes` with `- US-NNNN · Kind: new|edit|deletion · Rule: changed|unchanged`, template `assets/planned-functional-requirement.md` of `problem-space-fr`

**Base tag**:
The story tag an active scenario carried when a planned change to it was written. If the active scenario carries another tag by the time the change is checked or merged, another story changed it in between – a parallel change, which blocks completing the story until `/requirement` settled it.
_Code_: tag `@base-US-NNNN` or `@base-existing` on a changed or dropped scenario of a planned FR; checked by `requirements.py check`

**FR type**:
Which kind of rule a functional requirement describes, as a DDD term: Invariant, Domain Service, Policy, Command, Query, Anti-Corruption Layer or Data Migration (what becomes of data stored before a change). It decides the building block in the solution space, and through it the test level; the problem space names no test level.
_Code_: header field `Type:` of the FR, table in `references/fr-types.md` of `problem-space-fr`

**Scenario**:
A testable behaviour of a functional requirement. Each scenario gets exactly one main test that references it. Numbers are never renumbered or reused. A changed scenario keeps its number in the planned FR, so tests and placements reference the same `FR-…/Sn` before and after the merge. Tags show origin and reliability: in an active FR the story that last changed it or `@existing`, `@unconfirmed` (derived from code), `@obsolete`; in a planned FR additionally `@planned`, `@base-…` and `@open` (an open point concerns it). Every scenario of an active FR counts as implemented, those with `@unconfirmed` as not yet confirmed by the user.
_Code_: `Szenario: Sn – …` in the FR, reference `FR-<subdomain>-NNN/Sn`, in the test `@pytest.mark.fr("FR-<subdomain>-NNN/Sn")`

**Ripple**:
A change from a story touches another functional requirement the story says nothing about, e.g. a new overdue threshold and the FR of the problem signals. problem-space-fr marks it as an open point in the planned FR of the other requirement, as well as when a story changes an implemented scenario without superseding it, or when a scenario contradicts a glossary term.
_Code_: field `Case: ripple`, `Case: overwrite-implemented` or `Case: glossary` of an open point in the FR; besides these, problem-space-fr marks `Case: ownership` (which subdomain owns a term or rule), `Case: consistency` (must a rule across two business objects hold at once or may it follow), so boundary questions are settled in the problem space, and `Case: existing-data` (what becomes of data stored before the change)

## Tests

**Test as bridge**:
The test connects problem and solution space for behaviour: its marker names the scenario it proves, its path mirrors the code it tests and its import fixes where that code lives. The link FR → test → code follows from both and is never written down by hand (Specification by Example, Living Documentation). Decided in ADR 012, written by `test-definition`.
_Code_: `@pytest.mark.fr`, `backend/tests/domain/<context>/…` mirroring `backend/domain/<context>/…`

**Seam**:
The point where a test attaches to code from outside without reaching into internals: a building block in `model/`, the facade or API of a context, or the UI.
_Avoid_: interface (ambiguous), boundary

**Test level**:
How far a test reaches: Unit (a building block without database), Integration (facade or API with database) or E2E (a journey in the UI). It follows from the building block, not from the FR; the table is in the target structure. A backend test's level is a marker derived from its path, never a folder.
_Code_: `@pytest.mark.unit`, `@pytest.mark.integration` set by `backend/tests/plugins/levels.py`, `frontend/e2e/journeys/`, table in `domain-model/solution-space/structure.md`

**Scenario test**:
The one main test that proves an FR scenario, written before the implementation by `test-definition`.
_Code_: `@pytest.mark.fr("FR-<subdomain>-NNN/Sn")`

**Interface test**:
A test of a facade method a story adds or changes: the contract between two bounded contexts, which no scenario names.
_Code_: `@pytest.mark.story("US-NNNN")`

**Shell**:
The placed building blocks before their implementation: new files and symbols with signatures whose body raises `NotImplementedError`, empty migrations. Built by `solution-definition`, it makes the tests importable and changes no behaviour.
_Avoid_: stub (a test double), skeleton

**Journey**:
The end-to-end test of one business object with a UI: its life cycle on the happy path, one step per story that changes what a user does or sees there.
_Avoid_: E2E test per story
_Code_: `frontend/e2e/journeys/<subdomain>/<business-object>.spec.ts`, step tag `@US-NNNN`

**Provenance line**:
The last line of every question in a grill session: who raised it (Alex, grilling or both), which skill it comes from and, where available, reference and FR type.
_Code_: format in the skill `requirement`, step "Run the rounds"
