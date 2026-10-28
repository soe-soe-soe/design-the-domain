# DR 002: Existing data is a requirement – FR type Data Migration and case existing-data

**Status:** Accepted · **Date:** 2026-10-26

## Context

Once the application runs in production, every change to stored data raises the question what
becomes of the data that already exists. Migrations decided in the code alone hang on no
acceptance criterion.

## Decision

What becomes of existing data is phrased in business terms ("Bestehende Nachweise ohne
Gültigkeitsdatum gelten als unbefristet") and becomes an FR of the new type **Data Migration**.
problem-fr-writer marks an open point of the new case **existing-data** when a story changes what a
business object holds and no AC says what becomes of its existing instances.

## Considered alternatives

- **Schema changes as acceptance criteria:** tables and columns are solution space. Rejected.
