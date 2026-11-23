<!--
Status flow – this comment is guidance for the skills and is not copied into a story file.

  draft ⇄ ready → in-progress → done
    ↘      ↘          ↘
     └──────┴──────────┴→ cancelled

| Transition | Who | Valid only if |
|---|---|---|
| (new) → draft | user-story | next free number; file in ‹requirements›/planned/; createdAt set |
| draft → ready | /design-the-domain:requirement at close | no entry under ## Open, no AC tagged @open, every AC has a Then step or is dropped, every AC maps to a scenario under ## Functional requirements, `requirements.py check` passes |
| ready → draft | user-story | the story changes (any edit of a ready story) |
| ready → in-progress | /design-the-domain:story-workflow `start` (called by the implementing plugin) | `requirements.py check` passes |
| in-progress → draft | user-story | the story changes; the implementation must run again, its shell and tests are reworked |
| in-progress → done | /design-the-domain:story-workflow `done` (`requirements.py complete`) | `requirements.py check` passes; merges the planned FR changes, sets doneAt, moves the file to ‹requirements›/ |
| draft, ready, in-progress → cancelled | /design-the-domain:story-workflow `cancel` (`requirements.py cancel`), on the user's decision | drops the planned FR changes, moves the file to ‹requirements›/cancelled/ |

done and cancelled are final: the file is never edited again. A change to a done story is a new
story that names it under `Supersedes in part`.

Header fields: `External` only with a ticket system (`‹ticket-system›`, synced by assets/ticket.md of the plugin), `doneAt` only once done,
`Supersedes in part` only when there is something to enter.

Language: headings and field labels stay English (methodology); title, role sentence, texts,
Gherkin keywords (`# language: <code>`) and open questions are in ‹problem-space-language›. The
placeholders below are English.
-->
# US-NNNN: <title as a statement>

Status: draft · Topic: <topic of the grill session> · createdAt: YYYY-MM-DD · doneAt: YYYY-MM-DD · External: <ID in the ticket system>
Supersedes in part: US-NNNN (ACn)

As a <role> I want <capability>.

## Why

<1–3 sentences: which problem, which decision.>

## Content

<In short, what changes.>

## Acceptance criteria

```gherkin
# language: en
Feature: <title>

  Scenario: AC1 – <expected behaviour>
    Given <starting situation>
    When <exactly one trigger>
    Then <observable result>
```

## Functional requirements

- FR-<subdomain>-NNN (<new | edit | deletion>): AC1 → S1, AC2 → S4, AC3 → S3 obsolete

## Open

- **ACn** (user-story): <question, accepted by "yes"> – Recommendation: <answer> – Changes: <which Then>
