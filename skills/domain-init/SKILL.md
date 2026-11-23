---
name: domain-init
description: Takes existing code over into the problem-space model – drafts the domain map if missing, then glossary, subdomain map and FRs per subdomain, one subagent each, in parallel.
disable-model-invocation: true
---

# Domain-Init

You take the problem-space model (`‹problem-space›`, `‹glossaries›`) over from code that already
exists: glossary, business objects and FRs per subdomain, the scenarios from the existing tests.
Afterwards `design-the-domain:functional-requirement` has an existing state to find contradictions against.

This skill only states what differs from `design-the-domain:requirement`: the source is code, not
an interview, and the FRs are active at once, because the code implements them. Layout, naming,
numbering and templates are those of `design-the-domain:functional-requirement`, scenario format and glossary
format those of the assets it names.

You conduct: each subdomain is handled by a subagent of its own, all at once. You start them,
reconcile their results and report to the user. Problem-space content (glossary terms and
descriptions, FR rules, scenarios, questions to the user) is in `‹problem-space-language›`,
glossary identifiers in `‹solution-space-language›` as in the code; methodology is English as the
project config states.

**Project config.** Read `domain-model/config.md` in the project root before anything else; a name in
angle quotes (`‹domain-map›`) is one of its keys. Without the file, or while a key holds no value
or only a placeholder (`<name>`), step 1 fills it with the user; nothing else is read before that.

## Steps

1. **Config.** Read `domain-model/config.md`. If it exists and every key of the template
   `${CLAUDE_PLUGIN_ROOT}/assets/config.md` has a value that is not empty and not only a placeholder
   in angle brackets (`<name>`), go to step 2. Parts of other plugins in the file (under a heading of
   their own) are not yours: you neither check, fill nor change them. Otherwise you fill it
   with the user, first of all and in the main run; a key that does not apply gets `–`.
   - **Start from the template** `${CLAUDE_PLUGIN_ROOT}/assets/config.md`; values already filled stay.
   - **Derive a proposal** per open key from the project, with its source: the layout of the root,
     `CLAUDE.md`, `AGENTS.md` and the README (project rules, languages), build files and scripts
     (`pyproject.toml`, `package.json`, `Makefile`) for the source and test folders, an existing `domain-model/`. A value you do not find you do not guess: it stays open and is
     asked without a recommendation. The names of the people and the languages are always asked.
   - **Ask** in the question format of the interview, by hand: the script `interview-round.py` reads
     the config itself and cannot run without it. One question per group of the template – Project,
     Problem space, Code, Ticket system, Models – numbered from Q1 as
     `❓ **Qn** - **<group>**: …` with the open keys, each with its proposed value and source, and
     below it `➡️` the recommendation (take the proposals, name what is still open). In the
     language of the user. Write nothing before the answers and do not draft the domain map in the
     same message, not even name candidate subdomains or folders as a preview: the domain map follows
     in step 2, once the config is written.
   - **Write** `domain-model/config.md` as a copy of the template with the answers filled in (an
     existing file keeps the parts of other plugins below yours), no
     placeholder left except in a value that is a pattern (`FR-<subdomain>-NNN`). A key the user
     leaves open stays a placeholder: then say which keys are still open and stop, the skill
     continues with the next call.

2. **Domain map.** Read `‹domain-map›`. If it exists and lists a subdomain, go to step 3: it is the
   user's decision, you do not rework it. Otherwise you draft it with the user, in the main run,
   before any subagent starts. The code does not tell what a subdomain is, and folders are not
   subdomains: you bring evidence, the user decides.
   - **Read the structure, not the code:** the folders of `‹backend›` (without `‹backend-shared›`),
     existing glossaries, router prefixes, the test
     folders, which folders import which (grep), and, with a git history, which files change together.
   - **Candidates.** Cut the code into candidate subdomains: name in `‹problem-space-language›`,
     one sentence in business terms, code folders, business object candidates (aggregate roots).
     Evidence for a cut: the same word means something else in two areas (strongest signal); other
     experts or roles ask; it changes for other reasons or at another pace; several business objects
     share rules and a lifecycle (one business object with rules is no subdomain); what must be
     consistent at once belongs together; who is the source of truth for the data. Few imports
     between two folders and rare common changes support a cut, many speak against it.
   - **Show the evidence** per candidate, short: folders, business objects, language signals,
     coupling. Where the cut is a close call, name both alternatives (merge or split) with the
     strongest argument for each and your recommendation. Say plainly where the code gives no
     evidence; never feign certainty.
   - **Ask** by `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/interview-round.py <file>` (JSON as in its
     header: `group` `false`, `source` `domain-init`, `start` 1), after the evidence:
     one question per uncertain cut, one on the types (Core, Supporting, Generic; a business
     judgement, so the recommendation is `open` unless the user has said more), and one on whether
     the cut stands as a whole. Change nothing in its output. Write nothing before the answers.
   - **Write** once answered: `‹domain-map›` by `${CLAUDE_PLUGIN_ROOT}/assets/domain-map.md` – the
     domain in one sentence, a row per subdomain with its type, the glossary link and `–` as subdomain
     map, the relationships table empty (step 5 fills it from the reports) – and per subdomain a
     glossary file by `${CLAUDE_PLUGIN_ROOT}/assets/glossary.md` with title, sentence and the
     Subdomain row with its code folders. An existing glossary stays as it is. Name of the subdomain,
     of its glossary file and of its problem-space folder is the problem-space term in
     `‹problem-space-language›` (`fristen.md`, folder rules of `design-the-domain:functional-requirement`),
     never the code name (`deadlines`), which stands only in the Subdomain row.

3. **Clarify scope.** Read `‹domain-map›` and ask the user with
   AskUserQuestion whether to take one subdomain over, several or all; for several, let them
   choose. If the call already names subdomains (`/design-the-domain:domain-init deadlines project`), skip the
   question. Cross-cutting code in `‹backend-shared›` is out of scope.

4. **Start subagents**, all in **one** message so they run in parallel, each with the model
   `‹model-init›` (leave the model out for `inherit`): one per subdomain, with this brief
   (fill in `<subdomain>` and its folders from the subdomain row of its glossary):

   > Take the subdomain `<subdomain>` (code folders: `<folders>`) over into the problem space.
   > Project config: `domain-model/config.md`, plugin root: `${CLAUDE_PLUGIN_ROOT}`. You describe what the code
   > does today; you implement nothing, code and tests stay unchanged. Write only in
   > `‹problem-space›/<subdomain>/` (the FRs and `subdomain-map.md`), `‹glossaries›/<subdomain>.md`
   > and, for a new glossary or subdomain map, its subdomain's row in `‹domain-map›`. Read the ground as `design-the-domain:requirement` defines it
   > (step 1), for your subdomain, and the code below.
   >
   > **Sources, by reliability:** (1) the tests of your folders under `‹backend-tests›`, executable
   > examples of behaviour; one test or parametrised group yields one scenario; (2) the rules in the
   > code of your folders under `‹backend›`; (3) facade, routers and services: commands, queries and what other
   > subdomains call.
   >
   > **Business objects.** A business object is an aggregate root: it changes on its own and usually
   > has its own repository, service or router. What only changes with a root (history, contacts,
   > assignments) is an entity of that root and gets no folder.
   >
   > **Glossary.** Extend `‹glossaries›/<subdomain>.md` by `${CLAUDE_PLUGIN_ROOT}/assets/glossary.md`
   > and the rules of `design-the-domain:glossary`: one section per business object with its
   > row `Business Object | … | Aggregate Root`, rows for the terms your FRs need. Descriptions come
   > from code, docstrings and tests; what you cannot back, you do not write. You do not change
   > existing rows: if the code contradicts one, that becomes a question.
   >
   > **Subdomain map.** Write `‹problem-space›/<subdomain>/subdomain-map.md` by
   > `${CLAUDE_PLUGIN_ROOT}/assets/subdomain-map.md` and set its link in your subdomain's row of
   > `‹domain-map›`: a class per business object and per entity of it, the attributes from the fields
   > of the aggregate in business language with a glossary term as type (not code types), composition
   > for what lives and dies with the root, association for a reference by identity to another
   > business object of your subdomain, with multiplicities from the code (nullable fields, collections).
   > A reference to another subdomain goes under `Relationships` of your report, not into the map.
   > An existing map you extend; you change none of its lines: if the code contradicts one, that
   > becomes a question (Case `glossary`).
   >
   > **FRs.** One FR per rule or capability, active at once (no planned file, no history). A rule that
   > already has an FR (active or planned) stays as it is: you change no existing FR; where the code
   > contradicts it, that becomes a question (Case `test-vs-code`). The type
   > by `${CLAUDE_PLUGIN_ROOT}/assets/functional-requirement-types.md`, from the code: a rule module
   > yields Invariant, Domain Service or Policy FRs; plain creating, changing and deleting a business
   > object yields one Command FR; a query with logic of its own yields a Query FR; a call into
   > another subdomain that reacts to something yields a Policy FR in the triggering subdomain; a
   > foreign system yields an Anti-Corruption Layer FR. Layout, header, template, process of a
   > Policy and numbering (run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/requirements.py next-fr
   > <subdomain>` from the project root, not from the plugin folder; count up for several new FRs)
   > as `design-the-domain:functional-requirement` states.
   >
   > **Scenarios.** Per test (or parametrised group) one scenario by
   > `${CLAUDE_PLUGIN_ROOT}/assets/acceptance-criteria.md`, phrased on the level of the FR's rule,
   > with the test's concrete values. Code without a test gets a scenario from the code and is
   > listed under "without test". Every scenario carries `@existing @unconfirmed`.
   >
   > **Questions.** A question arises only if code or test contradicts a glossary description
   > (Case `glossary`), test and code say different things (`test-vs-code`), a branch
   > is suspicious: unreachable, contradictory, marked TODO (`suspicious-branch`), or the same rule is
   > implemented in two places (`duplicate-rule`).
   >
   > You are done when every rule and capability of your folders stands in an FR, every business
   > object stands in the subdomain map and every scenario carries `@existing @unconfirmed`. Your last message is the report, exactly in this form:
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

5. **Reconcile** once all reports are in:
   - **Policies across boundaries:** if two subagents described the same reaction, the FR stays in
     the triggering subdomain; delete the other.
   - **Relationships:** add new relationships between subdomains from the reports to the
     relationships table of `‹domain-map›`, in business terms; also one to a subdomain that is not in
     the map yet (named as the report names it): its row follows when that subdomain is taken over.
   - **Check:** every glossary written has its subdomain's row in `‹domain-map›`, every subdomain map
     written is linked in that row, and no two FR files of a subdomain share a number.

6. **Report.** To the user, per subdomain: business objects, number of FRs and scenarios, scenarios
   without test. Below that the subagents' questions, rendered by
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/interview-round.py <file>` (JSON as in its header: one
   `headings` entry per subdomain, each question with its `group`, `source`
   `domain-init`, `ref` and `type`; `start` 1). Change nothing in its output. A question whose answer
   would change the behaviour belongs in a `design-the-domain:requirement` session, not here. Finally the question
   which subdomains they confirm as a block.

7. **Confirm.** For each subdomain the user confirms, remove `@unconfirmed` from all its
   scenarios. Scenarios concerned by an open question keep it until it is answered.

You are done when `domain-model/config.md` is filled in, the domain map lists the subdomains and every chosen subdomain has a glossary and a subdomain map with its business
objects and FRs for its rules and capabilities, and the user has given their confirmation or answers.
