---
name: implement-story
description: Implements a ready story – placed with solution-sync, test-first with Pocock's tdd, reviewed with Pocock's code-review – and closes it.
disable-model-invocation: true
---

# Implement-Story

You implement one story. Its spec lives in the problem space: the story (why and acceptance
criteria) and its FR scenarios (the rules). Where the code goes follows from
`domain-model/solution-space/structure.md`, applied by `solution-sync`. The craft comes from
Pocock's skills `tdd` and `code-review`; this skill feeds them the project's artefacts and
closes the story afterwards.

Called as `/implement-story US-0042`. Code, comments, docstrings and commits are English.

A question to the user here means the grilling missed something or the structure does not fit.
Ask only what blocks the work, and report each question as a lesson (step 6).

## Steps

1. **Read the spec.** The story `domain-model/problem-space/stories/US-0042-*.md` and every FR
   scenario tagged `@US-0042` (search `domain-model/problem-space/`). The story must be `ready`;
   if not, stop and name its open points. Note the current commit as the review's fixed point.

2. **Place.** Run the skill `solution-sync` for the story. Its placement is your plan: building
   block and file per scenario, interfaces, schema changes. If it reports questions, ask them in
   one round and run it again with the answers.

3. **Implement test-first.** Call the Skill tool with `mattpocock-skills:tdd` and work through the
   placement scenario by scenario. The seams are agreed by convention, so tell the user which
   ones you use instead of asking: a building block under `model/` (unit), a command or query
   through `api/` or `facade/` (integration), a policy through the facade of its context. Tests
   go where `structure.md` puts them; each test that proves a scenario carries
   `@pytest.mark.fr("FR-<subdomain>-NNN/Sn")`, one main test per scenario. Schema changes go
   through an Alembic migration. Run `pyright` and the single test file regularly,
   `cd backend && pytest` once at the end.

4. **Review.** Call the Skill tool with `mattpocock-skills:code-review`: fixed point from step 1,
   spec = the story and its FR scenarios, standards include `structure.md`. Fix what it finds
   that the spec or the repo's standards require.

5. **Close.** Set `Status: done` in the story, remove `@planned` from its scenarios, and commit by
   the convention in `CLAUDE.md`; the pre-commit hook regenerates the context map.

6. **Report.** What was built, the commit, and for every question you asked in steps 2 and 3:
   whether the grilling could have settled it, and which check in `grill-story` or `fr-writer`
   was missing. Without questions: `Lessons: none`.

You are done when every planned scenario of the story has a passing test with its marker, the
full suite and `pyright` are green, the review's findings are resolved, the story is `done` in
one commit, and the lessons are reported.
