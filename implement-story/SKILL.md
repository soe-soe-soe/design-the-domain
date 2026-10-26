---
name: implement-story
description: Implements a ready story from its placement – test-first with Pocock's tdd, reviewed with Pocock's code-review – and closes story and placement.
disable-model-invocation: true
---

# Implement-Story

You implement one story. Its spec has three parts, all under `domain-model/`: the story (why and
acceptance criteria), its FR scenarios (the rules), and its placement (which code artefacts
change). The craft comes from Pocock's skills `tdd` and `code-review`; this skill feeds them the
project's artefacts and closes the story afterwards.

Called as `/implement-story US-0042`. Code, comments, docstrings and commits are English.

## Steps

1. **Read the spec.** The story `domain-model/problem-space/stories/US-0042-*.md`, every FR
   scenario tagged `@US-0042` (search `domain-model/problem-space/`), and the placement
   `domain-model/solution-space/placements/US-0042-*.md`. Story and placement must both be
   `ready`; if not, stop and name what is missing (open points, open questions, no placement:
   run `solution-sync` first). Note the current commit as the review's fixed point.

2. **Agree the seams.** From the placement, propose one seam per building block: a building block
   under `model/` (unit), a command or query through `api/` or `facade/` (integration), a policy
   through the facade of its context. Each with a one-line note on what it catches. Confirm them
   with the user in one question before any test is written.

3. **Implement test-first.** Call the Skill tool with `mattpocock-skills:tdd` and work through the
   placement scenario by scenario, at the agreed seams. Each test that proves a scenario carries
   `@pytest.mark.fr("FR-<subdomain>-NNN/Sn")`, one main test per scenario, at the path mirroring
   the code it tests. Schema changes go through an Alembic migration. Run `pyright` and the single
   test file regularly, `cd backend && pytest` once at the end.

4. **Review.** Call the Skill tool with `mattpocock-skills:code-review`: fixed point from step 1,
   spec = story, FR scenarios and placement. Fix what it finds that the spec or the repo's
   standards require.

5. **Close.** Set `Status: done` in story and placement, remove `@planned` from the story's
   scenarios, and commit by the convention in `CLAUDE.md`; the pre-commit hook regenerates the
   context map.

You are done when every scenario of the placement has a passing test with its marker, the full
suite and `pyright` are green, the review's findings are resolved, and story and placement are
`done` in one commit.
