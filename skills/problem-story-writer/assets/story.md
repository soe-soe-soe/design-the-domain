<!--
Status flow – this comment is guidance for the skills and is not copied into a story file.

  draft ⇄ ready → in-progress → done
    ↘      ↘          ↘
     └──────┴──────────┴→ cancelled

| Transition | Who | Valid only if |
|---|---|---|
| (new) → draft | problem-story-writer | next free number; file in ‹requirements›/planned/; createdAt set |
| draft → ready | /pts:problem-definition at close | no entry under ## Open, no AC tagged @open, every AC has a Dann or is `entfallen`, every AC maps to a scenario under ## Functional requirements, `requirements.py check` passes |
| ready → draft | problem-story-writer | the story changes (any edit of a ready story) |
| ready → in-progress | /pts:story-workflow step 1 | `requirements.py check` passes |
| in-progress → draft | problem-story-writer | the story changes; story-workflow must run again, its shell and tests are reworked |
| in-progress → done | `requirements.py complete` (story-workflow step 7) | `requirements.py check` passes; merges the planned FR changes, sets doneAt, moves the file to ‹requirements›/ |
| draft, ready, in-progress → cancelled | `requirements.py cancel`, on the user's decision | drops the planned FR changes, moves the file to ‹requirements›/cancelled/ |

done and cancelled are final: the file is never edited again. A change to a done story is a new
story that names it under `Supersedes in part`.

Header fields: `External` only with a ticket system (`‹ticket-system›`, synced by templates/ticket.md of the plugin), `doneAt` only once done,
`Supersedes in part` only when there is something to enter.
-->
# US-NNNN: <Titel als Aussage>

Status: draft · Topic: <Thema der Grill-Session> · createdAt: YYYY-MM-DD · doneAt: YYYY-MM-DD · External: <ID im Ticketsystem>
Supersedes in part: US-NNNN (ACn)

Als <Rolle> möchte ich <Fähigkeit>.

## Why

<1–3 Sätze: welches Problem, welche Entscheidung.>

## Content

<Kurz, was sich ändert.>

## Acceptance criteria

```gherkin
# language: de
Funktionalität: <Titel>

  Szenario: AC1 – <erwartetes Verhalten>
    Angenommen <Ausgangslage>
    Wenn <genau ein Auslöser>
    Dann <beobachtbares Ergebnis>
```

## Functional requirements

- FR-<subdomain>-NNN (<new | edit | deletion>): AC1 → S1, AC2 → S4, AC3 → S3 obsolete

## Open

- **ACn** (problem-story-writer): <Frage, mit „ja“ annehmbar> – Recommendation: <Antwort> – Changes: <welches Dann>
