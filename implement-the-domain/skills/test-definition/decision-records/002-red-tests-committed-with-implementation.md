# DR 002: Red tests, committed together with the implementation

**Status:** Accepted · **Date:** 2026-10-26

## Context

Between `test-definition` and the end of the implementation, the new tests fail. The suite on
`main` must stay green.

## Decision

The tests stay plainly red (they fail with `NotImplementedError` from the shell or with their
assertion) and are never committed on their own: shell, tests and implementation land in one
commit at the end of `implement-story`.

## Considered alternatives

- **`xfail(strict=True)`, committed before the implementation:** keeps `main` green and turns into
  a failure once the code passes, which forces removing the marker. Rejected: a module missing
  at import fails at collection, not inside the test, so every planned import would have to move
  into the test function.

## Consequences

The tests of a story exist only in the working tree until the story is done.
