# Evals for problem-init

## Goal

`problem-init` has eval cases under `evals/problem-init/` that run with `claude plugin eval .`
like the other skills.

## Why

Five of eight skills have evals; `problem-init` has none. It writes the starting state that
`problem-fr-writer` later checks contradictions against – a wrong glossary or FR here spreads
into every later session without anyone noticing.

## Current state

- `skills/problem-init/SKILL.md` and `references/subdomain.md` exist, no `evals/problem-init/`.
- The skill asks the scope with AskUserQuestion unless the call names subdomains
  (`/pts:problem-init deadlines project`) and runs one subagent per subdomain in parallel.

## Target state

Cases in the existing layout (`case.yaml`, `prompt.md`, `place-files.sh` with
`evals/fixtures/pts.md`, `files/`, `graders/`), at least:

- **one-subdomain-from-code:** a small backend with tests for one subdomain → glossary rows in
  the project's table format, FRs with scenarios from the existing tests, each test carries the
  reference to its scenario.
- **suspicious-branch-asks:** code with an unreachable or TODO-marked branch → becomes a
  question to the user, not an FR rule (`references/subdomain.md`, step on suspicious branches).
- **shared-code-out-of-scope:** code under `‹backend-shared›` gets no FR.

## Before starting

- Name the subdomains in the prompt so the AskUserQuestion step is skipped – an eval cannot
  answer it.
- Check whether the fixture config `evals/fixtures/pts.md` has every key the skill reads
  (`‹backend-shared›`, `‹glossaries›`, `‹scenario-marker›`).
