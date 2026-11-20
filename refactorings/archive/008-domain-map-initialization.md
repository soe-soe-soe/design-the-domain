# Refactoring 008: problem-space-initialization drafts the domain map

Status: Implemented · Date: 2026-11-20

## Goal

A project without a domain map gets one at the start of `problem-space-initialization`: an
overview of the subdomains, drafted from the code and decided by the user, before any subagent
takes a subdomain over.

## Why

The skill read `‹domain-map›` and asked only which of its subdomains to take over; that the map
exists and lists subdomains it assumed. For existing code (brownfield) the first step is missing.
Strategic design (Evans: draw the context map first, as it is; Brandolini: big picture before
details; Khononov: subdomains and their types are a business decision) starts with the overview.

## Decisions

- **Runs only when the map is missing or lists no subdomain.** An existing map is the user's
  decision and is not reworked; adding a subdomain later goes through the domain map by hand or
  `domain-modeling`.
- **The main run drafts, no subagent.** The cut of the subdomains is the user's decision, and the
  draft rests on structure (folders, imports, routers, ADRs, glossaries, tests), not on code bodies.
- **No hard rules, only evidence.** The code does not tell what a subdomain is; folders are not
  subdomains. The draft therefore brings, per candidate: code folders, business object candidates
  (aggregate roots), language signals (the same word with another meaning), coupling between the
  folders (imports, optionally the change coupling of the git history), and for a close call both
  alternatives (merge or split) with a recommendation.
- **The user decides in the question format of the interview** (`interview-round.py`, source
  `problem-space-initialization`): per uncertain cut one question, one on the types. The type
  (Core, Supporting, Generic) is a business judgement; the recommendation is `open` unless the
  user decides.
- **Nothing is written before the answers.**
- **What gets written:** the domain map by `assets/domain-map.md` (one sentence for the domain, a
  row per subdomain with the type, the glossary link and `–` as subdomain map; relationships stay
  empty, the reconcile step fills them from the reports) and a glossary skeleton per subdomain by
  `assets/glossary.md` (title, sentence, the Subdomain row with its code folders). The folders stay
  where the subagents already read them: in the Subdomain row of the glossary.

## Implemented

- `skills/problem-space-initialization/SKILL.md`: new step 1 "Domain map", the following steps
  renumbered, description and done criterion extended.
- Evals `problem-space-initialization/map-missing-drafts-proposal` (draft and questions, nothing
  written, no subagent) and `…/map-missing-written-after-confirmation` (map and skeletons after the
  confirmation).

## Open

- Evals run (2026-11-20): `map-missing-drafts-proposal` 3/3 green, `map-missing-written-after-confirmation`
  3/3 green after two grader fixes (empty relationships table read as a data row; the scope question
  of the next step is allowed) and one skill fix (glossary file named after the problem-space term,
  not the code name).
- The heuristics of the skill (language, ownership, rhythm of change, rules, consistency, data
  sovereignty) are not tested against a real project yet; the pilot on a small subdomain of
  the pilot project shows whether the evidence is enough.
