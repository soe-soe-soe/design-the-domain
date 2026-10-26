# DR 001: The problem space names no test level

**Status:** Accepted · **Date:** 2026-10-26

## Context

FR types used to carry a test level (Unit, Integration), shown in open points and the provenance
line of the grill session. The test level depends on the building block a rule becomes, which is
a solution-space decision.

## Decision

FR types say which kind of rule an FR describes; the test level follows from the building block
in `domain-model/solution-space/structure.md`. Open points and the provenance line carry no test
level.
