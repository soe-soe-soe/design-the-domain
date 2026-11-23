---
name: solution-init
description: Plans the migration of existing backend code into the solution-space structure – aggregates and building blocks per bounded context, in parallel.
disable-model-invocation: true
---

# Solution-Init

You lay out, once, how the existing backend (`‹backend›`) moves into the target structure of
`‹structure›`: per bounded context which aggregates it
has, which building block every module becomes and where it goes. The result is one migration
plan per context under `‹refactorings›`, carried out later per context. Afterwards
`implement-the-domain:solution-definition` places new requirements into a structure that holds.

You plan, you do not move code. You conduct: each bounded context is handled by a subagent of
its own, all at once. Everything you write is in `‹solution-space-language›`; questions to the user are in
`‹problem-space-language›`.

**Project config.** Read `domain-model/config.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, or when a key you need holds no value or only a placeholder (`<name>`), stop and tell the
user, in their language and nothing else: fill in `domain-model/config.md` first, `/design-the-domain:domain-init` does it with them. Guess no value.

## Steps

1. **Clarify scope.** Read the subdomain rows of `‹glossaries›/*.md` (bounded
   context and its folders) and ask the user with AskUserQuestion whether to plan one context,
   several or all; for several, let them choose. If the call names contexts
   (`/implement-the-domain:solution-init permits deadlines`), skip the question. `‹backend-shared›` is out of scope.
   Read `‹refactorings›/solution-init-seed.md` if it exists: it lists code locations formerly
   kept in the FRs; hand each subagent its part.

2. **Start subagents**, all in **one** message so they run in parallel, each with the model
   `‹model-solution-init›` (leave the model out for `inherit`): one per context, with
   this brief:

   > Plan the migration of the bounded context `<context>` (folders: `<folders>`, subdomain
   > `<subdomain>`) by `${CLAUDE_SKILL_DIR}/context.md` (project config:
   > `domain-model/config.md`). Write only `‹refactorings›/solution-structure-<context>.md`. Your last message is the report in the
   > form the reference prescribes.

3. **Reconcile** once all reports are in:
   - **Cross-context moves:** if two plans claim the same module, or one plan moves code into
     another context (e.g. planning law from `projects` to `areas`), keep the move in the
     receiving context's plan and reference it from the other.
   - **Facade usage:** every call a plan routes through another context's facade must exist in
     that context's planned facade (`‹structure›`).
   - **Context map:** run `‹context-map-command›`; it rewrites
     `‹context-map›` from today's code.
   - **Seed:** delete `‹refactorings›/solution-init-seed.md` once every context in it is planned.

4. **Report.** To the user, per context: aggregates, number of modules per building block,
   boundary violations found (imports bypassing a facade). Below that the subagents' questions
   in the question format of `design-the-domain:domain-grilling` (the artifact a question rests on after its title), grouped per
   context. Finally the
   question which context to migrate first.

You are done when every chosen context has a migration plan that assigns every module of its
folders, the context map is regenerated, and the user has their questions.
