# DR 001: Stories live in ‹requirements› with planned/ and cancelled/, and a status flow

**Status:** Accepted · **Date:** 2026-11-01

## Context

Stories lay in one folder with draft, ready and done side by side. Nothing said which status may
follow which, and a done story could still be edited.

## Decision

- `‹requirements›/` holds done stories, `planned/` the open ones (draft, ready, in-progress),
  `cancelled/` the cancelled ones – the same split as active and planned FRs.
- Status flow `draft ⇄ ready → in-progress → done`, each open status `→ cancelled`, with the
  checks per transition in the comment of `assets/story.md`. done and cancelled are final; a
  change to a done story is a new story with `Supersedes in part`.
- A changed `in-progress` story falls back to `draft`; the implementation runs again.
- Header fields `createdAt` and `doneAt`; `doneAt` orders the history of an FR.
- With a ticket system the repository stays the source of truth: stories are written one way to
  the ticket system, its ID is kept as `External`.

## Considered alternatives

- **A `history/` folder for done stories:** the name fits done stories only, not the open ones
  in the same tree. Rejected for `‹requirements›`.
- **Two-way sync with the ticket system:** needs conflict resolution between two sources of
  truth. Rejected.
