# DR 001: The placement is built as a shell without behaviour

**Status:** Accepted · **Date:** 2026-10-26

## Context

Tests written before the implementation import the placed building blocks. Without the files
they fail at import, and `pyright` is red for the whole time; with real code, the placement
would already be the implementation.

## Decision

After the placement, `solution-definition` builds the shell: new files and symbols with typed
signatures whose bodies only raise `NotImplementedError`, new facade methods and endpoint
registrations, and Alembic revisions with empty `upgrade()`/`downgrade()` (an empty migration
keeps the chain runnable, `NotImplementedError` would break it). Moves and renames only when
behaviour-preserving; deletion only of unreferenced code. Existing bodies are never changed. The
suite and `pyright` are as green afterwards as before.

## Considered alternatives

- **Empty files only:** the test still fails at import of the missing symbol, and the interface
  stays undecided although the placement decides it. Rejected.
- **No shell, the tests import paths that do not exist:** red for the wrong reason (import error),
  `pyright` red. Rejected.
- **Deleting replaced code in the shell:** deleting behaviour is a behaviour change; it belongs
  to an `@obsolete` scenario and the implementation. Rejected.
