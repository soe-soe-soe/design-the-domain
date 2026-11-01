# FR types

The type stands as a DDD term in the FR header. It decides the building block in the solution
space (skill `solution-definition`, table in `‹structure›`), and
through it the test level; the problem space names no test level.

| Type | Folder | Sign in the AC (German phrases from the pilot project; read them in `‹problem-space-language›`) | Example |
|---|---|---|---|
| Invariant | `invariants/` | "darf nur", "nie", permitted transitions | Nachweisstatus only via permitted transitions |
| Domain Service | `domain-services/` | "gilt als", "ergibt sich aus", "wird berechnet" | Überfälligkeit, Problemsignale, IRR, Phase aus Antragsstatus |
| Policy | `policies/` | "wenn X geschieht, dann …" across a subdomain boundary; "täglich", "jeden Montag", "um 6 Uhr" (scheduled) | Frist erledigt → entry in the Nachweishistorie; tägliche Fristerinnerung |
| Command | `commands/` | user creates, changes, deletes, advances | Projekt anlegen, Frist abhaken |
| Query | `queries/` | what a view or API returns: selection, visibility, order | Termine der Startseite, Teamübersicht |
| Anti-Corruption Layer | `acl/` | a foreign system: Auth0, ALKIS, e-mail delivery | Organisationsname aus Auth0 |
| Data Migration | `data-migrations/` | "bestehende … gelten / werden nach der Umstellung …": what happens to data that already exists | Bestehende Nachweise ohne Gültigkeitsdatum gelten als unbefristet |

The folder lies below the business object, or directly below the subdomain for an FR without
one, and is created with its first FR.

## Boundaries

- **Calculated value in a view:** if the Then step checks a calculated value ("zeigt 2
  Problemsignale"), the AC belongs to the Domain Service, even if the value appears in a view.
  Query only for what the view itself decides: which entries, who sees what, in which order.
- **Domain event:** an event is no FR. That it occurs is a scenario of the triggering
  Command; each reaction to it is an FR of its own of type Policy.
- **Existing data:** a scenario about data stored before the change is a Data Migration, even if
  the rule it carries over has an FR of another type. The new rule stays in that FR; the Data
  Migration FR says only what the existing data becomes.
- **Scheduled reaction:** what happens at a time rather than on an event ("täglich", "am
  Monatsersten") is a Policy with `Trigger: schedule`; it may stay inside its subdomain. The
  time itself ("06:00", "werktags") is part of the rule.
- **Process:** every Policy belongs to exactly one process – the chain from a trigger (a
  Command or a schedule) through the policies it sets off. The process file stands in the same
  `policies/` folder (`assets/process.md`).
- **Out of scope:** non-functional requirements (performance, availability, security, audit)
  and UI/UX (layout, wording, interaction) get no FR; pts does not model them.
- **One FR, one rule.** Two rules that can change independently are two FRs, even if one
  story touches both.
