---
name: story-workflow
description: Implements a ready story – placed and shelled with solution-definition, tests written first with test-definition, made green with tdd, reviewed with code-review – and closes it.
disable-model-invocation: true
---

# Story-Workflow

You implement one story. Its spec lives in the problem space: the story (why and acceptance
criteria) and its FR scenarios (the rules) – the planned changes in the `planned/` files next to
the active FRs, tagged with the story. Where the code goes follows from
`‹structure›`, applied by `pts:solution-definition`; which tests prove
it, from `pts:test-definition` (`‹test-strategy-adr›`). The craft comes from the skills `pts:tdd` and
`pts:code-review`; this skill feeds them the project's artefacts and closes the story afterwards.

**Project config.** Read `.claude/pts.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, stop and point the user to the
template `${CLAUDE_PLUGIN_ROOT}/templates/config.md`.

Called as `/pts:story-workflow US-0042`. Code, comments, docstrings and commits are English.

A question to the user here means the grilling missed something or the structure does not fit.
Ask only what blocks the work, and report each question as a lesson (step 8).

## Steps

1. **Read the spec.** The story `‹requirements›/planned/US-0042-*.md`, every scenario tagged
   `@US-0042` in the planned FR files (`planned/` below the FR folders of `‹problem-space›/`),
   and the active FRs they change. The story must be `ready` – or `in-progress` when a previous
   run stopped; if not, stop and name its open points.
   Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/requirements.py check US-0042`. If it reports a
   conflict – another story changed the same scenario since this one was written – set the story
   back to `Status: draft`, show the report and stop: the conflict goes back to
   `/pts:problem-definition`.
   Otherwise set `Status: in-progress` in the story header and, unless `‹ticket-system›` is
   `none`, sync the story by `${CLAUDE_PLUGIN_ROOT}/templates/ticket.md`. Note the current commit as the review's fixed
   point.

2. **Place.** Call the Skill tool with `pts:solution-definition` for the story. If it reports questions, ask
   them in one round and run it again with the answers. Its placement is your plan, its shell
   the ground for the tests.

3. **Define the tests.** Call the Skill tool with `pts:test-definition` with the story and the placement
   report. If it reports untestable scenarios, ask the user how each Dann is meant and run it
   again with the answers.

4. **Review gate.** Show the user test-definition's report and wait. They check that each test
   says what its scenario means; change the tests by their answer before you go on.

5. **Make them green.** Call the Skill tool with `pts:tdd` and follow its loop:
   - The red tests of step 3 are your "red". Take them one at a time: make one green, then the
     next. Tests the implementation needs below a scenario you add by `tdd`, without marker.
   - A test of step 3 changes only if it is wrong against its scenario – then tell the user.
     Selectors in page objects may follow the UI; assertions may not.
   - Schema changes fill the migration of the shell. Run `‹typecheck›` and the single test file
     (`‹test-file›`) regularly, `‹test-all›` once at the end, and the touched journey with
     `‹e2e-file›` if the story changed one.

6. **Review.** Call the Skill tool with `pts:code-review`: fixed point from step 1,
   spec = the story and its FR scenarios, standards include `‹structure›` and `‹test-strategy-adr›`. Fix what
   it finds that the spec or the repo's standards require.

7. **Close.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/requirements.py complete US-0042`. It
   checks the base once more, merges the story's planned changes into the active FRs, sets
   `Status: done` and `doneAt`, and moves the story to `‹requirements›/` – all or nothing. On a
   conflict it writes nothing: show its report and stop before committing; the story stays
   `in-progress` until `/pts:problem-definition` settled the conflict. Then commit placement,
   tests, implementation and the problem-space changes together by the commit convention in
   `‹project-rules›`; regenerate the context map with `‹context-map-command›` if the project has
   no hook doing it. Unless `‹ticket-system›` is `none`, sync the story by
   `${CLAUDE_PLUGIN_ROOT}/templates/ticket.md` – status done, link to its new path.

8. **Report.** What was built, the commit, and for every question you asked in steps 2, 3 and
   5: whether the grilling could have settled it, and which check in `problem-definition` or
   `problem-fr-writer` was missing. Without questions: `Lessons: none`.

You are done when every planned scenario of the story has a passing test with its marker, every
facade method of the placement its interface test, the full suite and `‹typecheck›` are green, the
review's findings are resolved, the story is `done` – merged by `requirements.py complete` – in
one commit, and the lessons are reported.
