# Refactoring 007: subdomain map – structure of a subdomain in the problem space

Status: Implemented · Date: 2026-11-17

## Goal

The problem space holds the structure of every subdomain once and in one place: its business
objects, what each holds and how they relate, so that the solution space can be derived from it.
The glossary stays what it is: terms and the link between problem and solution space.

## Why

The domain map covers the level of subdomains (types, relationships between subdomains). One level
below – business objects, their attributes, whether one contains or only refers to another –
nothing held the structure: it showed only indirectly in glossary descriptions, in invariants and in
policies. That structure decides the aggregate boundaries, which are business decisions
(consistency within one object or eventual consistency between two).

## Decisions

- **One file per subdomain:** `‹problem-space›/<subdomain>/subdomain-map.md`, beside the business
  object folders. One file, not one per business object: the relationships between the objects are
  the point.
- **Format:** a Mermaid `classDiagram` in the file itself – source and view at once. Template:
  `assets/subdomain-map.md`.
  - A class per business object (aggregate root) and per entity of it the structure needs.
  - Composition (`*--`) for an entity that lives and dies with its root; association (`-->`) for a
    reference by identity to another business object of the subdomain; multiplicities and a label
    in business terms on every relationship.
  - Attributes in business language, the type is a glossary term (Value or plain business type),
    optional ones with `?`. No operations (commands stand in the glossary and the FRs), no
    visibility. Inheritance only where the business itself names a specialisation.
  - Class ids ASCII (umlauts spelled out, as folder names), the term as label:
    `class ManuelleFrist["Manuelle Frist"]`.
- **Division of labour:** terms and their meaning only in the glossary; rules only in the FRs;
  relationships *between* subdomains only in the domain map, which links every map in a new column
  `Subdomain map`.
- **Who maintains it:** `problem-space-initialization` writes it from the code (aggregate fields,
  ownership); `problem-space-fr` updates it when an AC adds or changes a business object, an
  attribute or a relationship, and with the answer to the cases *consistency* and *existing-data*;
  the ground read of `requirement` reads it. Whoever creates a map sets its link in the domain map;
  `domain-modeling` writes a new row with `–` there.
- **Not in scope:** lifecycle of a business object (refactoring 006), a check in `requirements.py`
  that every class exists as a glossary term.

## Implemented

`assets/subdomain-map.md` (new); `assets/domain-map.md` (column), `assets/output-format.md` (icon
row), `skills/problem-space-initialization`, `skills/problem-space-fr`, `skills/requirement`,
`skills/domain-modeling`.

## Before starting (done) / open

- Open: probe the Mermaid syntax of the template in a renderer (class ids with label, optional
  `?` in a member).
- Evals written (2026-11-17): `problem-space-initialization/map-from-code`,
  `problem-space-fr/attribute-updates-map` (both 3/3 runs green) and
  `problem-space-fr/open-consistency-leaves-map` (red in 2 of 3 runs, see below); the domain-map
  fixtures of all cases carry the column `Subdomain map`.
- Decided (2026-11-17): while a *consistency* point is open the map carries the relationship as an
  association until the answer decides composition (small aggregates by default).
  `problem-space-fr` step 2 and grader 01 of `open-consistency-leaves-map` adjusted; rerun
  3/3 green (1.00).
