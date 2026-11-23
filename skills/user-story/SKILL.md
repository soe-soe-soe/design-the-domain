---
name: user-story
description: Writes user stories with Gherkin acceptance criteria from the decisions of a grill session into ‹requirements›/planned/ and marks what is still open. Use from the writing subagent of /requirement after every answered round, or when the user wants requirements, decisions or a concept turned "into stories" or "into acceptance criteria".
---

# User-Story

You package business decisions into **stories**: short, with a why, followed by acceptance
criteria (AC) in Gherkin. A story describes a **change**; the living target state is kept by
the functional requirements (skill `design-the-domain:functional-requirement`).

You write what is decided and mark what is still open, in the story itself. You ask nothing:
`/design-the-domain:domain-interview` reads the open points and decides when to ask them.

**Project config.** Read `domain-model/config.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, or when a key you need holds no value or only a placeholder (`<name>`), stop and tell the
user, in their language and nothing else: fill in `domain-model/config.md` first, `/design-the-domain:domain-init` does it with them. Guess no value.

Language: story content (title, role sentence, why, scenarios with their Gherkin keywords, open
questions) is in `‹problem-space-language›`; methodology (headings, tags, status values, IDs, field
labels) is English as the project config states.

## Where stories live

```
‹requirements›/
  US-0007-….md        done – final, never edited
  planned/US-0042-….md  draft, ready, in-progress – the only stories you write
  cancelled/US-0031-….md  cancelled – final, never edited
```

The status flow and what each transition requires stand in the comment at the top of the
template [story.md](../../assets/story.md); read it.

## Steps

1. **Read the situation.** The input (the answers of the last round plus the requirement that started
   the session), `‹domain-map›`, the glossaries of the subdomains
   involved (`‹glossaries›/`), and
   all stories under `‹requirements›/` and its subfolders.

2. **Assign.** A story is a change a business person recognises as one thing. For each change
   in the input:
   - A story on the same topic in `planned/` (status `draft`, `ready` or `in-progress`) is
     continued. A `ready` or `in-progress` story you change goes back to `draft`; for
     `in-progress` say so in the report, because its shell and tests were built on the old
     version.
   - If the matching story is `done` or `cancelled`, leave it untouched: create a new story and
     reference a done one under `Supersedes in part` (e.g. "button blue" → "button red").
   - Otherwise create a new story with the next free number (`US-0001`, `US-0002`, … across
     all stories in all three folders).

3. **Check.** Every statement in an AC is **backed** (conversation, glossary, code) or
   **inconsequential** (wording, order, example names). Everything else is a **gap**. A gap is
   an open point only if a different answer would change a **Then** step, i.e. observable
   behaviour, and it concerns the topic of a decision in the input without being settled by
   it. What the input does not address at all (e.g. the display, when it only decides the
   counting rule) is no open point, and neither is re-asking what it decided (e.g. whether
   problems on an evidence count, when the input defined the problem signal through deadlines).
   Gaps that change no Then step you write in the obvious reading without recording them.

4. **Write.** The story by the template [story.md](../../assets/story.md) (without its
   comment), the AC by [assets/acceptance-criteria.md](../../assets/acceptance-criteria.md). A Then step stands only where
   the outcome is decided; an invented outcome is a guess.

5. **Mark what is open.** An AC an open point concerns carries the tag `@open`, meaning as in
   the term "Open point" in `‹methodology-glossary›`: a new AC whose outcome is
   open has no Then step, or is left out until decided. Open is any part of the outcome the answer
   could change – also how many, when or to whom; then the AC has no Then step at all, never a
   provisional one. Each open point gets one entry under
   `## Open`, in the format of that term, with source `user-story` and the field `Changes`.

6. **Resolve what is answered.** If the input answers an open point, take the answer into the
   AC, remove `@open` and the entry under `## Open`.

You are done when every decision of the input stands in an AC or is marked open.

**Status** is not yours beyond the two moves above: a new story starts as `draft`,
`design-the-domain:story-workflow` sets `ready` (when `/design-the-domain:domain-interview` closes its
session), `in-progress`, `done` and `cancelled`.

## Story file

`‹requirements›/planned/US-0042-problem-signals.md` (number, then a short slug in
`‹problem-space-language›`), structured exactly as the template.

- `createdAt` is set when the story is created and never changed; `doneAt` and `External` are
  not yours – leave them out of a new story.
- The role sentence (`As a … I want …`, in `‹problem-space-language›`) has no "so that": the why
  has its own section.
- `## Functional requirements` belongs to `design-the-domain:functional-requirement`: leave it out of a new story
  and do not change it.
- `Supersedes in part` and `## Open` are omitted when there is nothing to enter.
- AC numbers are fixed: a dropped AC stays as `Scenario: AC2 – dropped` (keyword and word in
  `‹problem-space-language›`), freed numbers are
  never reused. Tests and FRs reference them later.

## Report

Your last message is the report, exactly in this form and nothing else – no notes, assumptions
or explanations before or after it; it names what changed, not what is open (that stands in the
story):

```
Stories:
- US-0042: Problem signals in the project overview (new, draft)
- US-0039: Reminder before a deadline expires (continued, draft)
- US-0035: Digest e-mail (continued, in-progress → draft: shell and tests to rework)
```
