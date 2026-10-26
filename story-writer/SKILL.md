---
name: story-writer
description: Writes user stories with Gherkin acceptance criteria from the decisions of a grill session into domain-model/problem-space/stories/. Use from problem-sync after every answered round of /grill-story, or when the user wants requirements, decisions or a concept turned "into stories" or "into acceptance criteria".
---

# Story-Writer

You package business decisions into **stories**: short, with a why, followed by acceptance
criteria (AC) in Gherkin. A story describes a **change**. The living target state is kept by
the functional requirements (skill `fr-writer`), not by the story.

You run after every answered round of a grill session that interviews the user. Others ask
the questions: the grilling itself and `fr-writer`. You write only what is decided and make gaps
visible in the story without reporting them as questions.

Language: methodology terms, headings, status values and IDs are English; story content
(title, role sentence, why, scenarios) is German, as the problem space is German.

## Steps

1. **Read the situation.** Read the input (the answers of the last round plus the prompt that
   started the session), `domain-model/problem-space/domain-map.md`, the glossaries of the
   subdomains involved (`domain-model/glossaries/`), the ADRs under `docs/adr/` as far as they
   touch the topic, and all stories under `domain-model/problem-space/stories/`.

2. **Cut.** A story is a change a business person recognises as one thing. For each change in
   the input:
   - If a story on the same topic has status `draft` or `ready`, continue that one.
   - If the matching story is `done`, leave it untouched. Create a new story and reference
     the old one under `Supersedes in part` (e.g. "button blue" → "button red").
   - Otherwise create a new story with the next free number (`US-0001`, `US-0002`, … across
     all stories).

3. **Write the AC.** Every statement in an AC is **backed** (conversation, glossary, ADR,
   code) or **inconsequential** (wording, order, example names). Everything else is a
   **gap**. Gherkin rules: [references/gherkin.md](references/gherkin.md).

4. **Record gaps.** A gap becomes an open point only if a different answer would change a
   **Dann**, i.e. observable behaviour, **and** it concerns the topic of a decision in the
   input. What the input does not address at all (e.g. the display, when it only decides the
   counting rule) is no open point of this story. For an open point:
   - A Dann stands only where the outcome is decided. If it is open, write the scenario
     without Dann and mark it `# open: <what is undecided>`, or leave the scenario out until it
     is decided. An invented outcome with `# open` next to it is a guess.
   - Add the point under `## Open`. It stays there for readers of the story; the grill
     session does not ask it.
   Gaps that change no Dann you write in the obvious reading without recording them.

5. **Resolve open points.** If the input answers an open point of an existing story, take the
   answer into the AC and remove the marker and the entry under `## Open`.

6. **Set the status.** `draft` while `## Open` has entries, otherwise `ready`. Only the
   implementation sets `done`, never you.

You are done when every decision of the input stands in an AC or is recorded as an open point.

## Story file

File name `domain-model/problem-space/stories/US-0042-problemsignale.md` (number, then a short
German slug). Structure exactly as in the template [assets/story.md](assets/story.md); read it
before you write the first story.

- The line `Als … möchte ich …` has no "damit": the why has its own section.
- `Supersedes in part` and `## Open` are omitted when there is nothing to enter.
- AC numbers are fixed: a dropped AC stays as `Szenario: AC2 – entfallen`, freed numbers are
  never reused. Tests and FRs reference them later.

## Report

Your last message is the report, exactly in this form. problem-sync passes it on; the grill
session groups its next round of questions by these stories:

```
Stories:
- US-0042: Problemsignale in der Projektübersicht (new, draft)
- US-0039: Erinnerung vor Fristablauf (continued, ready)
```
