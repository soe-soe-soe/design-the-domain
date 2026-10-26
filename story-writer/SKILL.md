---
name: story-writer
description: Writes user stories with Gherkin acceptance criteria from the decisions of a grill session into domain-model/problem-space/stories/ and marks what is still open. Use from problem-sync after every answered round of /problem-definition, or when the user wants requirements, decisions or a concept turned "into stories" or "into acceptance criteria".
---

# Story-Writer

You package business decisions into **stories**: short, with a why, followed by acceptance
criteria (AC) in Gherkin. A story describes a **change**; the living target state is kept by
the functional requirements (skill `fr-writer`).

You write what is decided and mark what is still open, in the story itself. You ask nothing:
`/problem-definition` reads the open points and decides when to ask them.

Language: methodology terms, headings, tags, status values, IDs and field labels are English;
story content (title, role sentence, why, scenarios, open questions) is German.

## Steps

1. **Read the situation.** The input (the answers of the last round plus the idea that started
   the session), `domain-model/problem-space/domain-map.md`, the glossaries of the subdomains
   involved (`domain-model/glossaries/`), the ADRs under `docs/adr/` that touch the topic, and
   all stories under `domain-model/problem-space/stories/`.

2. **Assign.** A story is a change a business person recognises as one thing. For each change
   in the input:
   - A story on the same topic with status `draft` or `ready` is continued; a `ready` story you
     change goes back to `draft`.
   - If the matching story is `done`, leave it untouched: create a new story and reference the
     old one under `Supersedes in part` (e.g. "button blue" → "button red").
   - Otherwise create a new story with the next free number (`US-0001`, `US-0002`, … across
     all stories).

3. **Check.** Every statement in an AC is **backed** (conversation, glossary, ADR, code) or
   **inconsequential** (wording, order, example names). Everything else is a **gap**. A gap is
   an open point only if a different answer would change a **Dann**, i.e. observable
   behaviour, and it concerns the topic of a decision in the input without being settled by
   it. What the input does not address at all (e.g. the display, when it only decides the
   counting rule) is no open point, and neither is re-asking what it decided (e.g. whether
   problems on a Nachweis count, when the input defined the problem signal through Fristen).
   Gaps that change no Dann you write in the obvious reading without recording them.

4. **Write.** The story by the template [assets/story.md](assets/story.md), the AC by
   [references/gherkin.md](references/gherkin.md). A Dann stands only where the outcome is
   decided; an invented outcome is a guess.

5. **Mark what is open.** An AC an open point concerns carries the tag `@open`, meaning as in
   the term "Open point" in `domain-model/glossaries/_methodology.md`: a new AC whose outcome is
   open has no Dann, or is left out until decided. Each open point gets one entry under
   `## Open`, in the format of that term, with source `story-writer` and the field `Changes`.

6. **Resolve what is answered.** If the input answers an open point, take the answer into the
   AC, remove `@open` and the entry under `## Open`.

You are done when every decision of the input stands in an AC or is marked open.

**Status** is not yours: a new story starts as `draft`, `/problem-definition` sets `ready` when the
session closes, the implementation sets `done`.

## Story file

`domain-model/problem-space/stories/US-0042-problemsignale.md` (number, then a short German
slug), structured exactly as the template.

- The line `Als … möchte ich …` has no "damit": the why has its own section.
- `Supersedes in part` and `## Open` are omitted when there is nothing to enter.
- AC numbers are fixed: a dropped AC stays as `Szenario: AC2 – entfallen`, freed numbers are
  never reused. Tests and FRs reference them later.

## Report

Your last message is the report, exactly in this form; it names what changed, not what is open:

```
Stories:
- US-0042: Problemsignale in der Projektübersicht (new, draft)
- US-0039: Erinnerung vor Fristablauf (continued, draft)
```
