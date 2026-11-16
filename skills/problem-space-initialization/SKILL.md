---
name: problem-space-initialization
description: Takes existing code over into the problem-space model – glossary, business objects and FRs per subdomain, one subagent each, in parallel.
disable-model-invocation: true
---

# Problem-Space-Initialization

You take the problem-space model (`‹problem-space›`, `‹glossaries›`) over from code that already
exists: glossary, business objects and FRs per subdomain, the scenarios from the existing tests.
Afterwards `define-the-domain:problem-space-fr` has an existing state to find contradictions against.

This skill only states what differs from `define-the-domain:requirement`: the source is code, not
an interview, and the FRs are active at once, because the code implements them. Layout, naming,
numbering and templates are those of `define-the-domain:problem-space-fr`, scenario format and glossary
format those of the assets it names.

You conduct: each subdomain is handled by a subagent of its own, all at once. You start them,
reconcile their results and report to the user. Problem-space content (glossary terms and
descriptions, FR rules, scenarios, questions to the user) is in `‹problem-space-language›`,
glossary identifiers in `‹solution-space-language›` as in the code; methodology is English as the
project config states.

**Project config.** Read `.claude/pts.md` in the project root before anything else; a name in
angle quotes (`‹domain-map›`) is one of its keys. Without the file, stop and point the user to the
template `${CLAUDE_PLUGIN_ROOT}/assets/config.md`.

## Steps

1. **Clarify scope.** Read `‹domain-map›` and ask the user with
   AskUserQuestion whether to take one subdomain over, several or all; for several, let them
   choose. If the call already names subdomains (`/define-the-domain:problem-space-initialization deadlines project`), skip the
   question. Cross-cutting code in `‹backend-shared›` is out of scope.

2. **Start subagents**, all in **one** message so they run in parallel, each with the model
   `‹model-init›` (leave the model out for `inherit`): one per subdomain, with this brief
   (fill in `<subdomain>` and its folders from the subdomain row of its glossary):

   > Take the subdomain `<subdomain>` (code folders: `<folders>`) over into the problem space.
   > Project config: `.claude/pts.md`, plugin root: `${CLAUDE_PLUGIN_ROOT}`. You describe what the code
   > does today; you implement nothing, code and tests stay unchanged. Write only in
   > `‹problem-space›/<subdomain>/`, `‹glossaries›/<subdomain>.md` and, for a new glossary, its
   > subdomain's row in `‹domain-map›`. Read the ground as `define-the-domain:requirement` defines it
   > (step 1), for your subdomain, and the code below.
   >
   > **Sources, by reliability:** (1) the tests of your folders under `‹backend-tests›`, executable
   > examples of behaviour; one test or parametrised group yields one scenario; (2) the rules in the
   > code of your folders under `‹backend›`, or the building blocks of `‹structure›` (ADRs
   > `‹architecture-adrs›`); (3) facade, routers and services: commands, queries and what other
   > subdomains call.
   >
   > **Business objects.** A business object is an aggregate root: it changes on its own and usually
   > has its own repository, service or router. What only changes with a root (history, contacts,
   > assignments) is an entity of that root and gets no folder.
   >
   > **Glossary.** Extend `‹glossaries›/<subdomain>.md` by `${CLAUDE_PLUGIN_ROOT}/assets/glossary.md`
   > and the rules of `define-the-domain:domain-modeling`: one section per business object with its
   > row `Business Object | … | Aggregate Root`, rows for the terms your FRs need. Descriptions come
   > from code, docstrings and tests; what you cannot back, you do not write. You do not change
   > existing rows: if the code contradicts one, that becomes a question.
   >
   > **FRs.** One FR per rule or capability, active at once (no planned file, no history). A rule that
   > already has an FR (active or planned) stays as it is: you change no existing FR; where the code
   > contradicts it, that becomes a question (Case `test-vs-code`). The type
   > by `${CLAUDE_PLUGIN_ROOT}/assets/functional-requirement-types.md`, from the code: a rule module
   > yields Invariant, Domain Service or Policy FRs; plain creating, changing and deleting a business
   > object yields one Command FR; a query with logic of its own yields a Query FR; a call into
   > another subdomain that reacts to something yields a Policy FR in the triggering subdomain; a
   > foreign system yields an Anti-Corruption Layer FR. Layout, header, template, process of a
   > Policy and numbering (`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/requirements.py next-fr
   > <subdomain>`, count up for several new FRs) as `define-the-domain:problem-space-fr` states.
   >
   > **Scenarios.** Per test (or parametrised group) one scenario by
   > `${CLAUDE_PLUGIN_ROOT}/assets/acceptance-criteria.md`, phrased on the level of the FR's rule,
   > with the test's concrete values. Code without a test gets a scenario from the code and is
   > listed under "without test". Every scenario carries `@existing @unconfirmed`.
   >
   > **Questions.** A question arises only if code or test contradicts a glossary description or an
   > ADR (Case `glossary` or `adr`), test and code say different things (`test-vs-code`), a branch
   > is suspicious: unreachable, contradictory, marked TODO (`suspicious-branch`), or the same rule is
   > implemented in two places (`duplicate-rule`).
   >
   > You are done when every rule and capability of your folders stands in an FR and every scenario
   > carries `@existing @unconfirmed`. Your last message is the report, exactly in this form:
   >
   > ```
   > Subdomain: deadlines
   > Business objects: Manual deadline
   > FRs: 6 (scenarios: 31, without test: 4)
   > - FR-deadlines-001: Overdue deadline (Domain Service, 4 scenarios)
   > - …
   > Without test:
   > - FR-deadlines-003/S5: team overview without permission shows only own deadlines
   > Relationships:
   > - Deadlines → Permits: done deadlines appear in the evidence history
   > Questions:
   > 1. Ref: <glossary>.md: <term> or FR-<subdomain>-NNN/Sn · Type: <FR type> · Case: <glossary | adr | test-vs-code | suspicious-branch | duplicate-rule>
   >    Question: <what stands out, phrased as a decision>?
   >    Recommendation: <answer with reason>.
   > ```
   >
   > Without questions it reads `Questions: none`. Phrase each question so that "yes" in
   > `‹problem-space-language›` accepts your recommendation.

3. **Reconcile** once all reports are in:
   - **Policies across boundaries:** if two subagents described the same reaction, the FR stays in
     the triggering subdomain; delete the other.
   - **Relationships:** add new relationships between subdomains from the reports to the
     relationships table of `‹domain-map›`, in business terms.
   - **Check:** every glossary written has its subdomain's row in `‹domain-map›`, and no two FR files of a
     subdomain share a number.

4. **Report.** To the user, per subdomain: business objects, number of FRs and scenarios, scenarios
   without test. Below that the subagents' questions, rendered by
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/interview-round.py <file>` (JSON as in its header: one
   `headings` entry per subdomain, each question with its `group`, `source`
   `problem-space-initialization`, `ref` and `type`; `start` 1). Change nothing in its output. A question whose answer
   would change the behaviour belongs in a `define-the-domain:requirement` session, not here. Finally the question
   which subdomains they confirm as a block.

5. **Confirm.** For each subdomain the user confirms, remove `@unconfirmed` from all its
   scenarios. Scenarios concerned by an open question keep it until it is answered.

You are done when every chosen subdomain has a glossary with its business objects and FRs for its
rules and capabilities, and the user has given their confirmation or answers.
