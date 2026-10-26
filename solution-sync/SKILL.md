---
name: solution-sync
description: Places the planned FR scenarios of ready stories into the backend's solution space – bounded context, aggregate, building block, file, interfaces, schema – writes the placement /implement works from, and reports boundary conflicts as questions. Use once after /grill-with-docs and before /implement, or when the user asks where a requirement goes in the backend.
---

# Solution-Sync

You translate problem space into solution space: for every planned scenario you decide which
code artefact changes, following [references/structure.md](references/structure.md). The
backend structure is the solution model, so a placement is a path, not a description. You look
for **boundary conflicts** the problem space cannot see. Only those become questions.

You read the problem space (stories, FRs, domain map) and never write into it. You write the
**placement** of each story under `domain-model/solution-space/placements/`, the spec
`/implement` works from, and the bridge: the solution-space columns (`Solution space`,
`Identifier`) of glossary rows whose code name you decide. Everything you write is English;
questions to the user are German.

## Steps

1. **Read the situation.** The stories from the input (status `ready`) and every FR scenario
   tagged with them and `@planned`, `domain-model/glossaries/` (subdomain row → bounded
   context and folders; business object → aggregate root),
   `domain-model/solution-space/context-map.md`, ADR 008 and 009, and the code of every
   context involved: its folder layout, facade and the building blocks the scenarios touch.

2. **Place every scenario.** Per scenario:
   - **Context:** from the subdomain row of the FR's subdomain.
   - **Aggregate and level:** the FR's business object names the aggregate. No business object,
     or the rule spans several aggregates → context level.
   - **Building block and file:** by the FR type table of the reference; reuse an existing file
     if it already holds this rule, otherwise name the new file. Not-migrated context: current
     layering plus target path.
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

   A difference between today's code and the placement is no question: it is the delta
   `/implement` closes. A scenario waiting for an answer stays unplaced.

4. **Write the placement**, one file per story:
   `domain-model/solution-space/placements/US-NNNN-<slug>.md` (same name as the story), by the
   template [assets/placement.md](assets/placement.md). Omit empty sections. Status `draft`
   while `## Open` has entries, otherwise `ready`. A placement of a story that is `done` stays
   unchanged; a later story gets its own placement. Only the implementation sets `done`.

You are done when every planned scenario of the input stories stands in a placement with
building block and file, or waits for one of your questions.

## Report

Your last message, exactly in this form:

```
Placements:
- domain-model/solution-space/placements/US-0042-nachbesserung.md (new, ready)
Questions:
1. Story: US-0042 · Ref: FR-fristen-013/S1 · Type: Query · Case: boundary
   Question: Soll Fristen abgelehnte Nachweise über die Fassade der Genehmigung lesen statt sie selbst zu speichern?
   Recommendation: Ja, der Nachweis gehört der Genehmigung; Fristen ist nachgelagert.
```

Without questions it reads `Questions: none`. Phrase each question so that "ja" accepts your
recommendation; the session shows it with the provenance line `🧩 solution-sync`. Once the
questions are answered, run again: the answers move the waiting scenarios into the placement.
