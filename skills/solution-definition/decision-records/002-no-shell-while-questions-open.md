# DR 002: No shell while a question is open

**Status:** Accepted · **Date:** 2026-10-26

## Decision

With an open question the skill writes nothing under `backend/`. An answer can move a scenario to
another context or aggregate, and a shell built before would have to be undone.
