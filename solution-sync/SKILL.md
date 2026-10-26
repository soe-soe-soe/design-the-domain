---
name: solution-sync
description: Places the planned FR scenarios of a ready story into the backend's solution space – bounded context, aggregate, building block, file, interfaces, schema – and reports boundary conflicts as questions. Use as the first step of /implement-story, or when the user asks where a requirement goes in the backend.
---

# Solution-Sync

You translate problem space into solution space: for every planned scenario of a story you
decide which code artefact changes, following `domain-model/solution-space/structure.md`. The
backend structure is the solution model, so a placement is a path, not a description. You look
for **boundary conflicts** the problem space cannot see. Only those become questions.

You read the problem space (stories, FRs, domain map) and never write into it. The placement is
your report, the input of the implementation in the same session; you write no file for it. The
only thing you write is the bridge: the solution-space columns (`Solution space`, `Identifier`)
of glossary rows whose code name you decide. Everything you write is English; questions to the
user are German.

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
     an existing file if it already holds this rule, otherwise name the new file. Not-migrated
     context: current layering plus target path.
   - **Interfaces:** each new or changed endpoint (`api/`) and facade method (`facade/`), and
     each domain event a command must raise for a policy.
   - **Schema change:** each new table or column, as an Alembic migration.
   - **Names:** English identifiers for new terms; enter them in the solution-space columns of
     the term's glossary row.

3. **Check for conflicts.** A question arises in four cases only:
   - **boundary:** the scenario needs data or behaviour of another context its facade does not
     offer, and it is unclear which context owns it.
   - **aggregate-cut:** an invariant spans two aggregates, or one command must change two
     aggregates consistently.
   - **misplacement:** the rule belongs to subdomain X, but the data or code it needs lives in
     folders the glossary row of X does not name.
   - **glossary-identifier:** an existing identifier in the glossary contradicts the code, or a
     new name would collide with one.

   A difference between today's code and the placement is no question: it is the delta the
   implementation closes. A scenario waiting for an answer stays unplaced.

You are done when every planned scenario of the story has a building block and file, or waits
for one of your questions.

## Report

Your last message, exactly in this form:

```
Placement US-0042: Nachbesserung abgelehnter Nachweise
| Scenario | Type | Context / aggregate | Building block → file |
|---|---|---|---|
| FR-genehmigung-014/S1 | Invariant | permits / evidence | invariant → aggregates/evidence/model/invariants/permitted_transitions.py (exists) |
| FR-fristen-013/S1 | Query | deadlines (not migrated) | query → service.py `DeadlineService.get_signals`; target application/queries/project_signals.py |
Interfaces:
- api: POST /evidences/{id}/reject → aggregates/evidence/application/commands/reject_evidence.py
- facade: PermitsFacade.get_rejected_evidences (new), used by deadlines
- event: EvidenceRejected (aggregates/evidence/model/events/evidence_rejected.py)
Schema: evidence.rejection_reason (text, nullable)
Glossary: genehmigung.md „Abgelehnt“ → Value Object, `EvidenceStatus.REJECTED`
Questions:
1. Story: US-0042 · Ref: FR-fristen-013/S1 · Type: Query · Case: boundary
   Question: Soll Fristen abgelehnte Nachweise über die Fassade der Genehmigung lesen statt sie selbst zu speichern?
   Recommendation: Ja, der Nachweis gehört der Genehmigung; Fristen ist nachgelagert.
```

Omit `Interfaces`, `Schema` or `Glossary` when empty. Without questions it reads
`Questions: none`. Phrase each question so that "ja" accepts your recommendation.
