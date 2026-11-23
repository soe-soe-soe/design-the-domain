---
name: implement-story
description: Implements a ready story – placed and shelled with solution-definition, tests written first with test-definition, made green with tdd, reviewed with code-review – and closes it.
disable-model-invocation: true
---

# Implement-Story

You implement one story. Its spec lives in the problem space: the story (why and acceptance
criteria) and its FR scenarios (the rules) – the planned changes in the `planned/` files next to
the active FRs, tagged with the story. Where the code goes follows from
`‹structure›`, applied by `implement-the-domain:solution-definition`; which tests prove
it, from `implement-the-domain:test-definition` (`‹test-strategy-adr›`). The craft comes from the skills `implement-the-domain:tdd` and
`implement-the-domain:code-review`; this skill feeds them the project's artefacts and closes the story afterwards.

**Project config.** Read `domain-model/config.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, or when a key you need holds no value or only a placeholder (`<name>`), stop and tell the
user, in their language and nothing else: fill in `domain-model/config.md` first, `/design-the-domain:domain-init` does it with them. Guess no value.

Called as `/implement-the-domain:implement-story US-0042`. Code, comments, docstrings and commits are in `‹solution-space-language›`.

A question to the user here means the grilling missed something or the structure does not fit.
Ask only what blocks the work, and report each question as a lesson (step 8).

## Steps

1. **Read the spec.** The story `‹requirements›/planned/US-0042-*.md`, every scenario tagged
   `@US-0042` in the planned FR files (`planned/` below the FR folders of `‹problem-space›/`),
   and the active FRs they change. The story must be `ready` – or `in-progress` when a previous
   run stopped; if not, stop and name its open points.
   Call the Skill tool with `design-the-domain:story-workflow US-0042 start`. If it reports
   `refused`, show its report and stop: a conflict goes back to `/design-the-domain:domain-interview`.
   Note the current commit as the review's fixed point.

2. **Place.** Call the Skill tool with `implement-the-domain:solution-definition` for the story. If it reports questions, ask
   them in one round and run it again with the answers. Its placement is your plan, its shell
   the ground for the tests.

3. **Define the tests.** Call the Skill tool with `implement-the-domain:test-definition` with the story and the placement
   report. If it reports untestable scenarios, ask the user how each Then step is meant and run it
   again with the answers.

4. **Review gate.** Show the user test-definition's report and wait. They check that each test
   says what its scenario means; change the tests by their answer before you go on.

5. **Make them green.** Call the Skill tool with `implement-the-domain:tdd` and follow its loop:
   - The red tests of step 3 are your "red". Take them one at a time: make one green, then the
     next. Tests the implementation needs below a scenario you add by `tdd`, without marker.
   - A test of step 3 changes only if it is wrong against its scenario – then tell the user.
     Selectors in page objects may follow the UI; assertions may not.
   - Schema changes fill the migration of the shell. Run `‹typecheck›` and the single test file
     (`‹test-file›`) regularly, `‹test-all›` once at the end, and the touched journey with
     `‹e2e-file›` if the story changed one.

6. **Review.** Call the Skill tool with `implement-the-domain:code-review`: fixed point from step 1,
   spec = the story and its FR scenarios, standards include `‹structure›` and `‹test-strategy-adr›`. Fix what
   it finds that the spec or the repo's standards require.

7. **Close.** Call the Skill tool with `design-the-domain:story-workflow US-0042 done`. It merges
   the story's planned changes into the active FRs, sets `Status: done` and moves the story to
   `‹requirements›/` – all or nothing – and syncs its ticket. If it reports `refused`, show its
   report and stop before committing; the story stays `in-progress` until
   `/design-the-domain:domain-interview` settled the conflict. Then commit placement,
   tests, implementation and the problem-space changes together by the commit convention in
   `‹project-rules›`; regenerate the context map with `‹context-map-command›` if the project has
   no hook doing it.

8. **Report.** What was built, the commit, and for every question you asked in steps 2, 3 and
   5: whether the grilling could have settled it, and which check in `domain-interview` or
   `functional-requirement` was missing. Without questions: `Lessons: none`.

You are done when every planned scenario of the story has a passing test with its marker, every
facade method of the placement its interface test, the full suite and `‹typecheck›` are green, the
review's findings are resolved, the story is `done` – merged by `design-the-domain:story-workflow` – in
one commit, and the lessons are reported.
