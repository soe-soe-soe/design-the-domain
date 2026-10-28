---
name: story-workflow
description: Implements a ready story – placed and shelled with solution-definition, tests written first with test-definition, made green with Pocock's tdd, reviewed with Pocock's code-review – and closes it.
disable-model-invocation: true
---

# Story-Workflow

You implement one story. Its spec lives in the problem space: the story (why and acceptance
criteria) and its FR scenarios (the rules). Where the code goes follows from
`‹structure›`, applied by `pts:solution-definition`; which tests prove
it, from `pts:test-definition` (`‹test-strategy-adr›`). The craft comes from Pocock's skills `tdd` and
`code-review`; this skill feeds them the project's artefacts and closes the story afterwards.

**Project config.** Read `.claude/pts.md` in the project root before anything else; a name in
angle quotes (`‹stories›`) is one of its keys. Without the file, stop and point the user to the
template `${CLAUDE_PLUGIN_ROOT}/templates/config.md`.

Called as `/pts:story-workflow US-0042`. Code, comments, docstrings and commits are English.

A question to the user here means the grilling missed something or the structure does not fit.
Ask only what blocks the work, and report each question as a lesson (step 8).

## Steps

1. **Read the spec.** The story `‹stories›/US-0042-*.md` and every FR
   scenario tagged `@US-0042` (search `‹problem-space›/`). The story must be `ready`;
   if not, stop and name its open points. Note the current commit as the review's fixed point.

2. **Place.** Call the Skill tool with `pts:solution-definition` for the story. If it reports questions, ask
   them in one round and run it again with the answers. Its placement is your plan, its shell
   the ground for the tests.

3. **Define the tests.** Call the Skill tool with `pts:test-definition` with the story and the placement
   report. If it reports untestable scenarios, ask the user how each Dann is meant and run it
   again with the answers.

4. **Review gate.** Show the user test-definition's report and wait. They check that each test
   says what its scenario means; change the tests by their answer before you go on.

5. **Make them green.** Call the Skill tool with `‹skill-tdd›` and follow its loop,
   with these project rules on top:
   - The red tests of step 3 are your "red". Take them one at a time: make one green, then the
     next. Tests the implementation needs below a scenario you add by `tdd`, without marker.
   - The seams are agreed in `‹structure›`; you do not ask for them.
   - A test of step 3 changes only if it is wrong against its scenario – then tell the user.
     Selectors in page objects may follow the UI; assertions may not.
   - Schema changes fill the migration of the shell. Run `‹typecheck›` and the single test file
     (`‹test-file›`) regularly, `‹test-all›` once at the end, and the touched journey with
     `‹e2e-file›` if the story changed one.

6. **Review.** Call the Skill tool with `‹skill-code-review›`: fixed point from step 1,
   spec = the story and its FR scenarios, standards include `‹structure›` and `‹test-strategy-adr›`. Fix what
   it finds that the spec or the repo's standards require.

7. **Close.** Set `Status: done` in the story, remove `@planned` from its scenarios, and commit
   placement, tests and implementation together by the commit convention in `‹project-rules›`;
   regenerate the context map with `‹context-map-command›` if the project has no hook doing it.

8. **Report.** What was built, the commit, and for every question you asked in steps 2, 3 and
   5: whether the grilling could have settled it, and which check in `problem-definition` or
   `problem-fr-writer` was missing. Without questions: `Lessons: none`.

You are done when every planned scenario of the story has a passing test with its marker, every
facade method of the placement its interface test, the full suite and `‹typecheck›` are green, the
review's findings are resolved, the story is `done` in one commit, and the lessons are reported.
