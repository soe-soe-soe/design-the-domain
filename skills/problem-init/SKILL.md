---
name: problem-init
description: Builds the problem-space model for existing code – glossary, business objects and FRs per subdomain, in parallel.
disable-model-invocation: true
---

# FR-Init

You derive the problem-space model (`‹problem-space›`, `‹glossaries›`) for code that already exists:
glossary, business objects and FRs per subdomain, the scenarios from the existing tests, and in
each of those tests the reference to its scenario. Afterwards `define-the-domain:problem-space-fr` has an existing state
to find contradictions against.

You conduct: each subdomain is handled by a subagent of its own, all at once. You start them,
reconcile their results and report to the user. Problem-space content (glossary terms and
descriptions, FR rules, scenarios, questions to the user) is in `‹problem-space-language›`,
glossary identifiers in `‹solution-space-language›` as in the code; methodology is English as the
project config states.

**Project config.** Read `.claude/pts.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, stop and point the user to the
template `${CLAUDE_PLUGIN_ROOT}/templates/config.md`.

## Steps

1. **Clarify scope.** Read `‹domain-map›` and ask the user with
   AskUserQuestion whether to initialise one subdomain, several or all; for several, let them
   choose. If the call already names subdomains (`/define-the-domain:problem-init deadlines project`), skip the
   question. Cross-cutting code in `‹backend-shared›` is out of scope.

2. **Start subagents**, all in **one** message so they run in parallel, each with the model
   `‹model-init›` (leave the model out for `inherit`): one per subdomain,
   with this brief:

   > Initialise the subdomain `<subdomain>` (folders: `<from the subdomain row of its
   > glossary>`) by `${CLAUDE_SKILL_DIR}/references/subdomain.md`
   > (plugin root: `${CLAUDE_PLUGIN_ROOT}`, project config: `.claude/pts.md`). Write only in
   > `‹problem-space›/<subdomain>/`, `‹glossaries›/<subdomain>.md`, its row in `‹glossary-map›` and in
   > tests of your folders under `‹backend-tests›`. Your last message is the
   > report in the form the reference prescribes.

3. **Reconcile** once all reports are in:
   - **Policies across boundaries:** if two subagents described the same reaction, the FR
     stays in the triggering subdomain; delete the other and move the references in its tests.
   - **Relationships:** add new relationships between subdomains from the reports to the
     relationships table of `‹domain-map›`, in business terms.
   - **Check:** `‹test-collect›` runs without errors; every
     scenario marker (`‹scenario-marker›`) names a scenario that exists.

4. **Report.** To the user, per subdomain: business objects, number of FRs and scenarios,
   tests with reference, scenarios without test. Below that the subagents' questions in the
   question format of `/define-the-domain:new-requirement` (provenance line with `🧩 problem-init`), grouped per subdomain.
   Finally the question which subdomains they confirm as a block.

5. **Confirm.** For each subdomain the user confirms, remove `@unconfirmed` from all its
   scenarios. Scenarios concerned by an open question keep it until it is answered.

You are done when every chosen subdomain has a glossary with its business objects, FRs for its
rules and capabilities and references in its tests, and the user has given their confirmation
or answers.
