# Initialise one subdomain

You describe what the code of a subdomain does today as a problem-space model: glossary,
business objects, FRs and scenarios. You describe, you do not implement: code and test logic
stay unchanged. Problem-space content is German, methodology terms and headings English,
identifiers in the glossary English as in the code.

## Sources, by reliability

1. **Tests** of your folders (`backend/tests/unit/domain/<folder>/`,
   `backend/tests/integration/domain/<folder>/`): executable examples of behaviour. One test or
   parametrised group yields one scenario.
2. **Rules** under `backend/domain/<folder>/regeln/` or the building blocks under `model/`
   (ADR 008): the business rules.
3. **Facade, routers, services:** commands, queries and what other subdomains call.
4. **Cross-check:** the subdomain's glossary, `domain-model/glossaries/_methodology.md`
   (glossary type), `domain-model/problem-space/domain-map.md`, the ADRs under `docs/adr/`,
   `docs/domain/`.

## Steps

1. **Determine business objects.** A business object is an aggregate root: it changes on its
   own and usually has its own repository, service or router. What only changes with a root
   (history, contacts, assignments) is an entity of that root and gets no folder. Folder name
   German, lower case, umlauts spelled out, words joined by hyphens (`manuelle-frist`).

2. **Extend the glossary** (`domain-model/glossaries/<subdomain>.md`, format in CLAUDE.md):
   one section per business object with its row `Business Object | … | Aggregate Root`. Add
   rows for terms your FRs need that are missing: entities, values, domain events, commands,
   queries, derived concepts. The description comes from code, docstrings and tests; what you
   cannot back, you do not write. You do not change existing rows: if the code contradicts a
   description, that becomes a question. You sort existing rows into the matching section.

3. **Cut FRs**, one FR per rule or capability, type by
   `.claude/skills/fr-writer/references/fr-types.md`:
   - A rule module yields one or more FRs (Invariant, Domain Service, Policy).
   - Plain creating, changing and deleting of a business object yields **one** Command FR per
     business object ("Frist verwalten") with scenarios for validations and permissions only,
     not one FR per endpoint.
   - A query with logic of its own (selection, visibility, order) yields a Query FR.
   - A call into another subdomain that reacts to something yields a Policy FR in the
     triggering subdomain.
   - A foreign system (Auth0, ALKIS, e-mail) yields an Anti-Corruption Layer FR.

   Layout and template as in `fr-writer`: `domain-model/problem-space/<subdomain>/<business-object>/`
   or directly in the subdomain, template
   `.claude/skills/fr-writer/assets/functional-requirement.md`, numbers per subdomain from `001`.
   FRs contain no code locations.

4. **Write scenarios.** Per test (or parametrised group) one scenario in Gherkin by
   `.claude/skills/story-writer/references/gherkin.md`, phrased on the level of the FR's rule,
   with the test's concrete values. Code without a test gets a scenario from the code and is
   listed under "without test" in the report; you write no test for it. Every scenario carries
   `@existing @unconfirmed`. History: `- existing: created (problem-init, <YYYY-MM-DD>)`.

5. **Reference tests.** Every test that yielded a scenario gets the marker
   `@pytest.mark.fr("FR-<subdomain>-NNN/Sn")` directly above `def` (once for a parametrised
   group, above `class` for a class whose tests all check the same scenario). Otherwise you
   change nothing in the test; add `import pytest` where it is missing.

6. **Collect findings.** A question arises only if
   - code or test contradicts a glossary description or an ADR,
   - test and code say different things,
   - a branch is suspicious (unreachable, contradictory, marked TODO), or
   - the same rule is implemented in two places.

You are done when every rule and capability of your folders stands in an FR, every scenario
carries `@existing @unconfirmed` and every test a scenario came from references it.

## Report

Your last message, exactly in this form:

```
Subdomain: fristen
Business objects: Manuelle Frist
FRs: 6 (scenarios: 31, without test: 4)
- FR-fristen-001: Überfälligkeit einer Frist (Domain Service, 4 scenarios)
- …
Tests with reference: 27
Without test:
- FR-fristen-003/S5: Teamübersicht ohne Recht zeigt nur eigene Termine
Relationships:
- Fristen → Genehmigung: erledigte Fristen erscheinen in der Nachweishistorie
Questions:
1. Ref: <glossary>.md: <term> or FR-<subdomain>-NNN/Sn · Type: <FR type> · Case: <glossary | adr | test-vs-code | suspicious-branch | duplicate-rule>
   Question: <was auffällt, als Entscheidung formuliert>?
   Recommendation: <Antwort mit Begründung>.
```

Without questions it reads `Questions: none`. Phrase each question so that "ja" accepts your
recommendation.
