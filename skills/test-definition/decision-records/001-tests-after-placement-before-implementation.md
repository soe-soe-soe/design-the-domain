# DR 001: Tests after the placement, before the implementation

**Status:** Accepted · **Date:** 2026-10-26

## Context

A test mirrors the path of the code it tests and imports it from there. Written before the
placement, it would have to guess where the code goes; written during the implementation (Pocock's
`tdd` alone), nobody checks it against the scenario before code depends on it.

## Decision

`test-definition` runs after `solution-definition` has placed the story and built its shell, and
before the implementation. It writes every test of the story at once; the user reviews them;
`tdd` then makes them green one at a time. The import of the placed path makes the placement
binding: a test turns green only where the placement put the code.

## Considered alternatives

- **Tests before the placement:** the test would guess the path. Rejected.
- **Tests inside the `tdd` loop only:** no review of the tests against the scenarios. Rejected.
- **A placement file checked after the implementation:** a second artefact to keep in sync;
  the import already enforces the placement. Rejected.

## Consequences

Pocock's `tdd` warns against writing all tests first (horizontal slicing). The warning targets
tests of imagined behaviour; these scenarios are settled in the problem space, and the
implementation still arms them one at a time.
