# Plan one bounded context

You classify the existing code of one bounded context into aggregates and building blocks and
write the migration plan. You change no code. Values in angle quotes are keys of the project
config `.claude/pts.md`. Target structure and FR type mapping:
`‹structure›`; terms:
`‹methodology-glossary›`.

## Sources

1. The code of your folders: models, repositories, services, routers, schemas, rule
   modules, facade, initializers, clients.
2. The glossary of your subdomain: business objects with aggregate root, solution-space column
   and identifiers.
3. The FRs of your subdomain (`‹problem-space›/<subdomain>/`): their type tells the
   building block of the code that implements them; tests with `‹scenario-marker›` lead from a
   scenario to that code.
4. the ADRs `‹architecture-adrs›` and the refactorings under `‹refactorings›` touching your folders.

## Steps

1. **Cut aggregates.** An aggregate is a consistency boundary: what one transaction must keep
   consistent. Start from the glossary's aggregate roots; check each against the code (own
   repository, own commands, referenced by ID from elsewhere). A folder of today is no
   aggregate by itself: a folder may hold several aggregates or be part of one. Name each
   aggregate in `‹solution-space-language›`, singular (`evidence`, `procedure`).

2. **Assign every module.** Each class or function with logic becomes exactly one building
   block at aggregate or context level, with its target file. Split modules that hold several
   blocks (e.g. one rules module → invariants, specifications, value objects). A service
   method that writes is a command, one that reads a query; a response mapper goes to the
   query. Routers, schemas, facade, its types and clients of foreign systems go where `‹structure›`
   puts them; facade methods stay thin forwards.

3. **Move the tests along.** Each test file gets the mirrored target path of the code it
   tests, under `‹backend-tests›` as `‹structure›` (section Tests) lays
   it out; markers stay.

4. **Collect findings.** A question arises only if
   - an invariant or command spans two aggregates (**aggregate-cut**),
   - code of your context imports another context past its facade, or is imported that way
     (**boundary**),
   - code in your folders belongs to another subdomain, or code of your subdomain lies outside
     them (**misplacement**),
   - a glossary identifier or solution-space type contradicts the code
     (**glossary-identifier**).

## Migration plan

`‹refactorings›/solution-structure-<context>.md`, in the form of the other refactorings (Goal,
Why, Current state, Target state, Before starting), with Target state as:

```
### Aggregates
- evidence (root `EvidenceDB` → `aggregates/evidence/model/root.py`): evidence
### Moves
| Current | Building block | Target |
|---|---|---|
| regeln/evidence_status.py `ERLAUBTE_UEBERGAENGE` | invariant | aggregates/evidence/model/invariants/permitted_transitions.py |
### Order
1. <step that keeps the tests green, e.g. one aggregate at a time>
```

## Report

Your last message, exactly in this form:

```
Context: permits (folders: permits)
Aggregates: evidence, procedure, application_component, cost_item
Modules: 64 assigned (invariant 6, specification 4, domain service 5, factory 2, command 18, query 14, policy 1, api 9, adapter 0, other 5)
Boundary violations: 3
- areas imports domain.permits.models past the facade (2 files)
Plan: ‹refactorings›/solution-structure-permits.md
Questions:
1. Ref: <file or FR-…/Sn> · Type: <FR type or building block> · Case: <aggregate-cut | boundary | misplacement | glossary-identifier>
   Question: <what stands out, phrased as a decision>?
   Recommendation: <answer with reason>.
```

Without questions it reads `Questions: none`. Phrase each question so that "yes" in `‹problem-space-language›` accepts your
recommendation.
