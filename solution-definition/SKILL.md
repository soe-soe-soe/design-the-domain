---
name: solution-definition
description: Places the planned FR scenarios of a ready story into the backend's solution space – bounded context, aggregate, building block, file, interfaces, schema – builds the shell of new files and symbols without behaviour, and reports boundary conflicts as questions. Use as the first step of /implement-story, or when the user asks where a requirement goes in the backend.
---

# Solution-Definition

You translate problem space into solution space: for every planned scenario of a story you
decide which code artefact changes, following `domain-model/solution-space/structure.md`. The
backend structure is the solution model, so a placement is a path, not a description. You look
for **boundary conflicts** the problem space cannot see. Only those become questions.

You read the problem space (stories, FRs, domain map) and never write into it. The placement is
your report, the input of `test-definition` and the implementation in the same session; you
write no file for it. You write two things: the bridge – the solution-space columns
(`Solution space`, `Identifier`) of glossary rows whose code name you decide – and the **shell**
of the placement (step 4), which changes no behaviour. Everything you write is English;
questions to the user are German.

## Steps

1. **Read the situation.** The story from the input (status `ready`) and every FR scenario
   tagged with it and `@planned`, `domain-model/glossaries/` (subdomain row → bounded context
   and folders; business object → aggregate root), `domain-model/solution-space/structure.md`
   and `context-map.md`, ADR 008 and 009, and the code of every context involved: its folder
   layout, facade and the building blocks the scenarios touch.

2. **Place every scenario.** Per scenario:
   - **Context:** from the subdomain row of the FR's subdomain.
   - **Aggregate and level:** the FR's business object names the aggregate. No business object,
     or the rule spans several aggregates → context level.
   - **Building block and file:** by the FR type table and naming rules of the structure; reuse
     an existing file if it already holds this rule, otherwise name the new file. Mark every
     file `(exists)` or `(new)`. Not-migrated context: current layering plus target path.
   - **Interfaces:** each new or changed endpoint (`api/`) and facade method (`facade/`), and
     each domain event a command must raise for a policy.
   - **Schema change:** each new table or column, as an Alembic migration.
   - **Names:** English identifiers for new terms; enter them in the solution-space columns of
     the term's glossary row.

3. **Check for conflicts.** A question arises in four cases only:
   - **boundary:** the scenario needs data or behaviour that two contexts could own, and the
     glossary does not settle which one. If the glossary names the owner, a missing facade method
     is no question: list it under Interfaces.
   - **aggregate-cut:** an invariant spans two aggregates, or one command must change two
     aggregates consistently.
   - **misplacement:** the rule belongs to subdomain X, but the data or code it needs lives in
     folders the glossary row of X does not name.
   - **glossary-identifier:** an existing identifier in the glossary contradicts the code, or a
     new name would collide with one.

   A difference between today's code and the placement is no question: it is the delta the
   implementation closes. A scenario waiting for an answer stays unplaced.

4. **Build the shell** – only when no question is open; otherwise write nothing under
   `backend/`. The shell makes the placement importable, so the tests can be written against it;
   it never changes behaviour:
   - **New file or symbol:** create it with its signature – classes with their fields,
     functions and methods with typed parameters and return type – and a body that only raises
     `NotImplementedError`. A new facade method goes into `facade/facade.py`, a new endpoint
     into its file and the registration in `api/__init__.py`.
   - **Migration:** create the Alembic revision for each schema change with empty `upgrade()`
     and `downgrade()` (`pass`), so the chain stays runnable; models and columns are not
     touched.
   - **Move or rename:** only behaviour-preserving, with every import adjusted.
   - **Delete:** only code nothing references any more. Code with behaviour goes away through an
     `@obsolete` scenario and its test, in the implementation.
   - **Never** change the body of an existing symbol.

   Then run `cd backend && pyright` and `pytest`: both are as green as before.

You are done when every planned scenario of the story has a building block and file, or waits
for one of your questions, and – without open questions – the shell stands and the suite is
unchanged.

## Report

Your last message, exactly in this form:

```
Placement US-0042: Gültigkeit von Gutachten
| Scenario | Type | Context / aggregate | Building block → file |
|---|---|---|---|
| FR-genehmigung-020/S1 | Domain Service | permits / evidence | domain service → aggregates/evidence/model/services/validity_end.py (new) |
| FR-fristen-021/S1 | Query | deadlines (not migrated) | query → service.py `DeadlineService.get_all`; target application/queries/start_page_deadlines.py |
Interfaces:
- facade: PermitsFacade.get_expiring_evidences (new), used by deadlines
Schema: evidence.valid_until (date, nullable)
Glossary: genehmigung.md „Gültig bis“ → Value Object, `Evidence.valid_until`
Shell:
- backend/domain/permits/aggregates/evidence/model/services/validity_end.py (new) `calculate_validity_end`
- backend/domain/permits/facade/facade.py `PermitsFacade.get_expiring_evidences` (new method)
- backend/ops/migrations/versions/<rev>_evidence_valid_until.py (new, empty)
Questions: none
```

With open questions, the scenario waiting for one reads `– waits for question 1` in the last
column, `Shell` is omitted (nothing is built yet), and the questions follow:

```
Questions:
1. Story: US-0042 · Ref: FR-genehmigung-021/S1 · Type: Query · Case: boundary
   Question: Soll der Antrag die Anschrift der Projektgesellschaft über die Fassade des Projekts lesen, statt eine eigene Kopie am Antrag zu speichern?
   Recommendation: Ja, die Projektgesellschaft gehört dem Projekt; eine Kopie am Antrag veraltet unbemerkt.
```

Omit `Interfaces`, `Schema`, `Glossary` or `Shell` when empty. Phrase each question so that
"ja" accepts your recommendation.
