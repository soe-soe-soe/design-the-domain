---
name: tdd
description: Test-driven development – what a good test is, where tests go, the anti-patterns and the red → green loop. Use from design-the-domain:test-definition and /design-the-domain:story-workflow, or when the user wants to build or fix something test-first.
---

> Based on [mattpocock/skills](https://github.com/mattpocock/skills) `skills/engineering/tdd` (MIT, © 2026 Matt Pocock),
> commit `4ae2317`, adapted for design-the-domain: seams agreed in the project's structure document, scenario
> tests written before the loop. See `THIRD_PARTY_LICENSES.md` and `docs/upstream.md` in the source repository.

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth
keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every
section applies on every cycle: consult them before and during the loop, not after.

**Project config.** Read `.claude/pts.md` in the project root if it exists; a name in angle quotes
(`‹structure›`) is one of its keys. Without it, the project has no agreed seams: agree them with
the user as described below.

When exploring the codebase, read the glossaries (`‹glossaries›`) so test names and interface
vocabulary match the project's domain language, and respect the ADRs (`‹adr›`) in the area you're
touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change
entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid
cart" tells you exactly what capability exists, and it survives refactors because it doesn't care
about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without
reaching inside. Tests live at seams, never against internals.

**Test only at agreed seams.** In a design-the-domain project the seams are agreed once, in the seam table of
`‹structure›` (which building block is tested where, at which level): use them and do not ask
again. Only where the structure names no seam for what you test – or without a design-the-domain config – write
down the seams under test and confirm them with the user before writing a test; give each
proposed seam a one-line note on what it catches and what it misses. You can't test everything,
so agreeing the seams up front is how testing effort lands on the critical paths and complex
logic instead of every edge case.

When the shape of that interface is itself in question (how deep the module is, where the seam
belongs, what the interface should expose), call the Skill tool with `design-the-domain:codebase-design` for
the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage
and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies
  through a side channel (querying the database instead of using the interface). The tell: the
  test breaks when you refactor but behavior hasn't changed. Exception: a data-migration test,
  whose seam is the stored data itself.
- **Tautological**: the assertion recomputes the expected value the way the code does
  (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted
  equal to itself), so it passes by construction and can never disagree with the code. Expected
  values must come from an independent source of truth: a known-good literal, a worked example,
  the spec – in a design-the-domain project the literals of the scenario's Dann.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify
  _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests
  go insensitive to real changes, and you commit to test structure before understanding the
  implementation. Work in **vertical slices** instead: one test → one implementation → repeat,
  each test a **tracer bullet** that responds to what the last cycle taught you.
  **Exception in design-the-domain:** `design-the-domain:test-definition` writes one test per FR scenario of a story before the
  loop. Those scenarios are settled in the problem space, not imagined; the loop then makes them
  green one at a time, and tests below a scenario that the implementation needs still follow the
  vertical rule.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't
  anticipate future tests or add speculative features. The red scenario tests of
  `design-the-domain:test-definition` count as written: take them one at a time.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (`design-the-domain:code-review`),
  not the red → green implementation cycle.
