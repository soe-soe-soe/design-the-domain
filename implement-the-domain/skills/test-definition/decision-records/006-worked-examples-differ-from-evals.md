# DR 006: Worked examples differ from the eval cases

**Status:** Accepted · **Date:** 2026-10-26

## Context

`scenario-to-test.md` shows how a scenario becomes a test. Its first version used the
same stories as the evals (US-0045, US-0047, US-0048); the runs then copied the examples almost
verbatim, so the evals measured copying, not the skill.

## Decision

The worked examples come from another subdomain (deadlines) than the eval cases (mostly
permits) and never share a story, FR or file name with them. A new eval case checks this
before it is added.
