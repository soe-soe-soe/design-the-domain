---
name: story-workflow
description: Moves a story along its status flow – start (ready → in-progress), done (in-progress → done, merges its planned FR changes into the active FRs) or cancel – by scripts/requirements.py, and syncs its ticket. Use when the user starts, finishes or drops a story, or from another plugin that implements stories (interface, see below).
---

# Story-Workflow

A story moves through `draft ⇄ ready → in-progress → done`, or to `cancelled`. The writers and
`/design-the-domain:requirement` handle draft and ready; this skill does the three transitions after
that. Each is one call of `scripts/requirements.py`, which checks the base and writes all or nothing,
plus the ticket sync. The status flow and what each transition requires stand in the comment at the
top of `${CLAUDE_PLUGIN_ROOT}/assets/story.md`.

**Project config.** Read `domain-model/config.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, or when a key you need holds no
value or only a placeholder (`<name>`), stop and tell the user, in their language and nothing else:
fill in `domain-model/config.md` first, `/design-the-domain:domain-init` does it with
them. Guess no value.

Everything you say to the user is in `‹problem-space-language›`. Run the script from the project
root, not from the plugin folder.

## Interface

Called by the user or through the Skill tool by another plugin (`implement-the-domain` calls it at
the start and at the end of implementing a story).

- **Call:** `design-the-domain:story-workflow <story> <transition>`, e.g. `US-0042 start`.
  `<transition>` is `start`, `done` or `cancel`.
- **Result:** your last message, exactly one of
  `Story-Workflow: US-0042 start → in-progress` (or `done → done`, `cancel → cancelled`), or
  `Story-Workflow: US-0042 <transition> refused` followed by the script's report unchanged.
- **Guarantees:** changes only the story file, the planned and active FR files of that story and,
  with a ticket system, its ticket. On `refused` nothing was changed, except that `start` sets a
  story whose check reports a conflict back to `draft`. Never touches code or tests.
- **Not done here:** committing. The caller commits the problem-space changes together with its own.

## Steps

1. **Read** the story (`‹requirements›/**/US-0042-*.md`) and its status.

2. **Transition.**
   - **start** (ready → in-progress; an `in-progress` story is left as it is and reported as
     started): run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/requirements.py check US-0042`. If it exits
     0, edit the header line to `Status: in-progress`. If it reports a conflict – another story
     changed the same scenario since this one was written – set the header back to
     `Status: draft` and refuse: the conflict goes back to `/design-the-domain:requirement`.
   - **done** (in-progress → done): run
     `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/requirements.py complete US-0042`. It checks the base once
     more, merges the story's planned changes into the active FRs, sets `Status: done` and `doneAt`,
     and moves the story to `‹requirements›/`. On a conflict it writes nothing: refuse; the conflict
     is settled in `/design-the-domain:requirement`.
   - **cancel** (draft, ready or in-progress → cancelled), only on the user's decision: run
     `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/requirements.py cancel US-0042`. It removes the story's
     planned FR changes and moves it to `‹requirements›/cancelled/`.

   Any other starting status (e.g. `start` on a draft) is refused with the status it has.

3. **Ticket.** Unless `‹ticket-system›` is `none` and only after a transition that was not refused:
   sync the story by `${CLAUDE_PLUGIN_ROOT}/assets/ticket.md` – status and the link to its new path.

4. **Report** in the form of the interface.
