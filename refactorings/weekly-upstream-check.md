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

## Done

- Cloud scheduled task "Pocock-Skills: wöchentliche Upstream-Prüfung" (`trig_018xPKGg84XQPHjwNduobQ3V`),
  Mondays 19:43 Europe/Berlin, push notification to the phone. It runs the brief of
  `docs/upstream.md`, updates *Last checked* and pushes it to `main`.

## Left

- Disable or delete the local task `pocock-skills-watch` on the Mac and its `last-checked.txt`;
  carry its last checked commit into *Last checked* first if it is newer than `4ae2317`.
- Delete this file afterwards.
