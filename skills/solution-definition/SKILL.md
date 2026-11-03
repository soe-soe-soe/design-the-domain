---
name: solution-definition
description: Places the planned FR scenarios of a ready story into the backend's solution space – bounded context, aggregate, building block, file, interfaces, schema – builds the shell of new files and symbols without behaviour, and reports boundary conflicts as questions. Use as the first step of /pts:story-workflow, or when the user asks where a requirement goes in the backend.
---

# Solution-Definition

You translate problem space into solution space: for every planned scenario of a story you
decide which code artefact changes, following `‹structure›`. The
backend structure is the solution model, so a placement is a path, not a description. You look
for **boundary conflicts** the problem space cannot see. Only those become questions.

You read the problem space (stories, FRs, domain map) and never write into it. The placement is
your report, the input of `test-definition` and the implementation in the same session; you
write no file for it. You write two things: the bridge – the solution-space columns
(`Solution space`, `Identifier`) of glossary rows whose code name you decide – and the **shell**
of the placement (step 4), which changes no behaviour. Everything you write is in
`‹solution-space-language›`; questions to the user are in `‹problem-space-language›`.

**Project config.** Read `.claude/pts.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, stop and point the user to the
template `${CLAUDE_PLUGIN_ROOT}/assets/config.md`.

## Steps

1. **Read the situation.** The story from the input (status `ready` or `in-progress`, under
   `‹requirements›/planned/`), every scenario tagged with it in the planned FR files (`planned/`
   below the FR folders) and the active FR each one changes. A planned scenario is changed
   (its `Sn` exists in the active FR), new, or `@obsolete` (it gets a row naming the code that
   goes away; the implementation removes it, the shell does not); a change line `Kind: deletion`
   makes every scenario of the active FR obsolete. Further: `‹glossaries›/` (subdomain row → bounded context
   and folders; business object → aggregate root), `‹structure›`
   and `‹context-map›`, the ADRs `‹architecture-adrs›`, and the code of every context involved: its folder
   layout, facade and the building blocks the scenarios touch.

2. **Place every scenario.** Per scenario:
   - **Context:** from the subdomain row of the FR's subdomain.
   - **Aggregate and level:** the FR's business object names the aggregate. No business object,
     or the rule spans several aggregates → context level.
   - **Building block and file:** by the FR type table and naming rules of the structure; reuse
     an existing file if it already holds this rule, otherwise name the new file. Mark every
     file `(exists)` or `(new)`. Not-migrated context: current layering plus target path.
   - **Interfaces:** each new or changed endpoint and facade method, where `‹structure›` puts
     them, and
     each domain event a command must raise for a policy.
   - **Schema change:** each new table or column, as a migration (`‹migrations›`).
   - **Names:** identifiers in `‹solution-space-language›` for new terms; enter them in the solution-space columns of
     the term's glossary row.
   - **Stored values:** a scenario that names a value of a set (a kind, a status) whose stored
     form a test must write or read – a data migration, a query filtering on it – gets that
     form into the `Identifier` column of the value's glossary row, from the code or decided
     here (`EvidenceKind.SOUND_REPORT` = `sound_report`). Otherwise `pts:test-definition` would have
     to guess it.

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
   `‹backend›`. The shell makes the placement importable, so the tests can be written against it;
   it never changes behaviour:
   - **New file or symbol:** create it with its signature – classes with their fields,
     functions and methods with typed parameters and return type – and a body that is only
     `‹not-implemented›`. A new facade method or endpoint goes where `‹structure›` puts it,
     including any registration the structure names.
   - **Migration:** create the revision (`‹migrations›`) for each schema change with empty
     upgrade and downgrade steps, so the chain stays runnable; models and columns are not
     touched.
   - **Move or rename:** only behaviour-preserving, with every import adjusted.
   - **Delete:** only code nothing references any more. Code with behaviour goes away through an
     `@obsolete` scenario and its test, in the implementation.
   - **Never** change the body of an existing symbol.

   Then run `‹typecheck›` and `‹test-all›`: both are as green as before.

Scenario references (`FR-…/Sn`) always use the number of the active FR; the planned file keeps
it.

You are done when every planned scenario of the story has a building block and file, or waits
for one of your questions, and – without open questions – the shell stands and the suite is
unchanged.

## Report

Your last message, exactly in this form:

Example (from a Python backend):

```
Placement US-0042: Validity of expert reports
| Scenario | Type | Context / aggregate | Building block → file |
|---|---|---|---|
| FR-permits-020/S1 | Domain Service | permits / evidence | domain service → aggregates/evidence/model/services/validity_end.py (new) |
| FR-deadlines-021/S1 | Query | deadlines (not migrated) | query → service.py `DeadlineService.get_all`; target application/queries/start_page_deadlines.py |
Interfaces:
- facade: PermitsFacade.get_expiring_evidences (new), used by deadlines
Schema: evidence.valid_until (date, nullable)
Glossary: permits.md "valid until" → Value Object, `Evidence.valid_until`
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
1. Story: US-0042 · Ref: FR-permits-021/S1 · Type: Query · Case: boundary
   Question: Should the application read the address of the project company through the project's facade instead of storing its own copy?
   Recommendation: Yes, the project company belongs to the project; a copy on the application goes stale unnoticed.
```

Omit `Interfaces`, `Schema`, `Glossary` or `Shell` when empty. Phrase each question so that
"yes" in `‹problem-space-language›` accepts your recommendation.
