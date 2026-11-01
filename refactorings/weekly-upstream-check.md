# Point the weekly upstream check to the plugin

## Goal

The weekly check of mattpocock/skills runs against `docs/upstream.md` of this plugin and reports
which upstream changes are worth taking over into the pts craft skills. Delete this file once the
scheduled task uses the new brief.

## Why

The craft skills `grilling`, `domain-modeling`, `tdd`, `code-review` and `codebase-design` are now
part of the plugin (November 2026). The scheduled task still checks Pocock's changes against
`.claude/pocock-skills.md` in the pilot project, which no longer exists on the branch
`claude/pts-requirements-layout` and asked a different question (does an upstream change break what
the workflow relies on), not the new one (should pts take an upstream change over).

## Current state

- The task is a local scheduled task on the user's machine: `pocock-skills-watch`, last checked
  commit in `~/.claude/scheduled-tasks/pocock-skills-watch/last-checked.txt`.
- Its brief reads `.claude/pocock-skills.md` of the pilot project.

## Target state

- The task's brief is the one under *Weekly check* in `docs/upstream.md`.
- The last checked commit is kept in `docs/upstream.md` (*Last checked*), not in a local file, so
  any machine or a cloud scheduled task can run the check.
- The old file `last-checked.txt` is removed.

## Before starting

- Decide where the task runs: stays local on the Mac, or becomes a cloud scheduled task on this
  repository (then it can update *Last checked* itself and commit it).
- Carry the last checked commit over from `last-checked.txt` into *Last checked*, if it is newer
  than `4ae2317`.
