---
name: problem-init
description: Builds the problem-space model for existing code – glossary, business objects and FRs per subdomain, in parallel.
disable-model-invocation: true
---

# FR-Init

You derive the problem-space model under `domain-model/` for code that already exists:
glossary, business objects and FRs per subdomain, the scenarios from the existing tests, and in
each of those tests the reference to its scenario. Afterwards `fr-writer` has an existing state
to find contradictions against.

You conduct: each subdomain is handled by a subagent of its own, all at once. You start them,
reconcile their results and report to the user. Methodology terms, headings and tags are
English; problem-space content (glossary descriptions, FR rules, scenarios, questions to the
user) is German.

## Steps

1. **Clarify scope.** Read `domain-model/problem-space/domain-map.md` and ask the user with
   AskUserQuestion whether to initialise one subdomain, several or all; for several, let them
   choose. If the call already names subdomains (`/problem-init fristen projekt`), skip the
   question. Cross-cutting code in `backend/core/` is out of scope.

2. **Start subagents**, all in **one** message so they run in parallel: one per subdomain,
   with this brief:

   > Initialise the subdomain `<subdomain>` (folders: `<from the subdomain row of its
   > glossary>`) by `.claude/skills/problem-init/references/subdomain.md`. Write only in
   > `domain-model/problem-space/<subdomain>/`, `domain-model/glossaries/<subdomain>.md` and in
   > tests under `backend/tests/**/domain/<folder>/` of your folders. Your last message is the
   > report in the form the reference prescribes.

3. **Reconcile** once all reports are in:
   - **Policies across boundaries:** if two subagents described the same reaction, the FR
     stays in the triggering subdomain; delete the other and move the references in its tests.
   - **Relationships:** add new relationships between subdomains from the reports to the
     relationships table of `domain-model/problem-space/domain-map.md`, in business terms.
   - **Check:** `cd backend && pytest --collect-only -q` runs without errors; every
     `@pytest.mark.fr` names a scenario that exists.

4. **Report.** To the user, per subdomain: business objects, number of FRs and scenarios,
   tests with reference, scenarios without test. Below that the subagents' questions in the
   grill-session format (CLAUDE.md, provenance line with `🧩 problem-init`), grouped per subdomain.
   Finally the question which subdomains they confirm as a block.

5. **Confirm.** For each subdomain the user confirms, remove `@unconfirmed` from all its
   scenarios. Scenarios concerned by an open question keep it until it is answered.

You are done when every chosen subdomain has a glossary with its business objects, FRs for its
rules and capabilities and references in its tests, and the user has given their confirmation
or answers.
