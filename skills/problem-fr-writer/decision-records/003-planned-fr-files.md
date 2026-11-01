# DR 003: Planned changes stand next to the active FR, not in it

**Status:** Accepted · **Date:** 2026-11-01

## Context

problem-fr-writer changed a scenario of the FR in place and marked it `@planned`. Until the
story was done, the FR mixed the implemented and the planned state, and the implemented Dann of a
changed scenario was gone. The FR's `## History` was kept by hand and duplicated what the stories
already say.

## Decision

- An **active FR** is the implemented state. Only `scripts/requirements.py close` writes it, when
  its story is done (problem-init writes active FRs for code taken over).
- problem-fr-writer writes **one planned file per FR** in `planned/` below the active FR's folder,
  same file name: a line per story under `## Changes` (Kind new, edit or deletion; Rule changed or
  unchanged) and only the scenarios a story changes, adds or drops.
- Scenarios keep the **numbers of the active FR**, so tests and placements reference the same
  `FR-…/Sn` before and after the merge. A changed scenario carries `@base-<tag>`, the story tag
  the active scenario had when the change was written; a different tag at close is a parallel
  change and blocks the merge.
- The FR keeps **no history**. The story lists its FRs under `## Functional requirements` (kind
  and AC → scenario), and `requirements.py history` derives an FR's history from the done
  stories, latest first.
- Open points stand in planned files only; a ripple or overwrite-implemented point copies the
  active scenario into the planned file.

## Considered alternatives

- **`@planned` inside the active FR** (before): mixes states, loses the implemented Dann. Rejected.
- **One delta file per story and FR** (`FR-….US-0042.md`): file names carry the story; two stories
  on one FR hide their overlap in two files. Rejected for one planned file per FR.
- **Own numbering in the delta:** needs a mapping table at merge, tests would point at the wrong
  scenario. Rejected.
- **`## History` in the FR, written at close:** duplicates the stories. Rejected.
