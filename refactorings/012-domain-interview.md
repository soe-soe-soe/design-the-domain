# Refactoring 012: the interview cut like Matt Pocock's skills – `domain-interview`

Status: Implemented, evals not run · Date: 2026-11-23

## Why

`domain-grilling` (a copy of upstream `grilling`) and `requirement` were both "the interview": the
real round rules of the project (numbering, grouping, open points, closing round, the script) stood
in `requirement`, and `domain-init` repeated part of them by hand. `requirement` mixed how the
interview is asked with what happens to the problem space. The upstream description of
`domain-grilling` ("grill the user relentlessly … any 'grill' trigger phrases") competed with an
installed `mattpocock-skills:grilling`.

Matt Pocock composes: `grill-with-docs` is one line ("call the Skill tool for grilling and
domain-modeling"); `domain-modeling` holds the language with scenarios and the code check; the
artifacts come from separate skills (`to-spec`, `to-tickets`).

## Decisions (user, 2026-11-23)

- The cut follows Pocock's, filled with the DDD structure:

  | Pocock | design-the-domain | Holds |
  |---|---|---|
  | `grilling` | `domain-grilling` | upstream text plus *Rounds in this project*: rendering by `interview-round.py`, numbering, grouping, open points of the writers (FR points every round, story points in the closing round), deferring, closing round, end; used by `domain-interview` and `domain-init` |
  | `domain-modeling` | `glossary` | as before, plus "discuss concrete scenarios" and "cross-reference with code" back from `requirement` |
  | `grill-with-docs` | `domain-interview` (was `requirement`) | entry: ground, loads `domain-grilling` and `glossary`, writers after every round, parallel changes, cancel, close through `story-workflow ready` |
  | `to-spec` | `user-story`, `functional-requirement` | the writers |
  | `to-tickets` | `story-workflow` | status and ticket; new transition `ready` |

- **The writers run after every round** (not at the end like `to-spec`): their DDD checks – glossary
  conflicts, ripples, parallel changes – flow into the running interview.
- **`story-workflow ready`** validates draft → ready (no `## Open`, no `@open`, every AC mapped,
  `requirements.py check`) and syncs the ticket, also for a story that stays draft. It is internal,
  no part of the interface for other plugins. The writers still set a changed story back to draft.
- **The provenance line goes.** No 🗣️, 🧩 or 📐 any more; the artifact a question rests on stands
  in parentheses after its title: `❓ **Q5** - **<title>** (📋 FR-fristen-013/S2): …`. The script
  ignores `source` and `type`; the open-point format in the files keeps its source skill.
- Still part of 0.9.0, which has not reached `dist`.

## Done (2026-11-23)

- `skills/requirement` → `skills/domain-interview`, rewritten as the thin entry; its decision
  records moved along unchanged.
- `domain-grilling`: narrow description, section *Rounds in this project*.
- `glossary`: the two techniques; description and header.
- `story-workflow`: transition `ready`, ticket sync at close, conflicts go back to
  `domain-interview`.
- `domain-init`: asks through `domain-grilling`; no `source` keys; Case `adr` removed from the
  report template (ADRs left design in 011).
- `scripts/interview-round.py` and its tests: references after the title instead of the provenance
  line (16 tests green).
- References followed: assets (`story.md`, `ticket.md`, `config.md`, `domain-map.md`,
  `output-format.md`), the writers, implement-the-domain (`implement-story`, `solution-init`, fixtures),
  methodology fixtures (term "Question reference" replaces "Provenance line"), `docs/upstream.md`
  (`grill-with-docs` row, split table), `THIRD_PARTY_LICENSES.md`, README, refactorings 002, 006, 011.
- Evals: `evals/requirement/` → `evals/domain-interview/`; transcripts in the prompts carry the
  references after the title; graders and `expected_outcome` on the provenance line rewritten
  (round-1 grader 02 and round-2 grader 06: no provenance line; closing-round grader 03,
  parallel-change grader 03, round-2 grader 04: reference after the title; graders 09: "title with
  its references").

Not changed on purpose: the archive, decision records, refactoring 004 (describes its own past
state), refactoring 005 and `DEVELOPING.md` (changed in parallel by the 005 session, see below).

## Open

- **Merged with 005 (2026-11-23).** 005's fixture moves (FRs under `commands/`, `policies/`) now
  sit under `evals/domain-interview/*`; its widened provenance graders (round 1 grader 02, round 2
  grader 06) gave way to "no provenance line". `DEVELOPING.md`, `evals/fixtures/README.md` and the
  sample project's `CLAUDE.md` name `domain-interview`. 005's own text keeps the old names as history.
- **Evals not run** – the `domain-interview` cases run on the fixture of 005 now, but have not run
  since this refactoring.
