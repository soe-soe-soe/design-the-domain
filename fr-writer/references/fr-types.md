# FR types

The type stands as a DDD term in the FR header. It decides the building block in the solution
space (skill `solution-definition`, table in `domain-model/solution-space/structure.md`), and
through it the test level; the problem space names no test level.

| Type | Sign in the AC | Example |
|---|---|---|
| Invariant | "darf nur", "nie", permitted transitions | Nachweisstatus only via permitted transitions (ADR 007) |
| Domain Service | "gilt als", "ergibt sich aus", "wird berechnet" | Überfälligkeit, Problemsignale, IRR, Phase aus Antragsstatus |
| Policy | "wenn X geschieht, dann …" across a subdomain boundary | Frist erledigt → entry in the Nachweishistorie |
| Command | user creates, changes, deletes, advances | Projekt anlegen, Frist abhaken |
| Query | what a view or API returns: selection, visibility, order | Termine der Startseite, Teamübersicht |
| Anti-Corruption Layer | a foreign system: Auth0, ALKIS, e-mail delivery | Organisationsname aus Auth0 |
| Data Migration | "bestehende … gelten / werden nach der Umstellung …": what happens to data that already exists | Bestehende Nachweise ohne Gültigkeitsdatum gelten als unbefristet |

## Boundaries

- **Calculated value in a view:** if the Dann checks a calculated value ("zeigt 2
  Problemsignale"), the AC belongs to the Domain Service, even if the value appears in a view.
  Query only for what the view itself decides: which entries, who sees what, in which order.
- **Domain event:** an event is no FR. That it occurs is a scenario of the triggering
  Command; each reaction to it is an FR of its own of type Policy.
- **Existing data:** a scenario about data stored before the change is a Data Migration, even if
  the rule it carries over has an FR of another type. The new rule stays in that FR; the Data
  Migration FR says only what the existing data becomes.
- **One FR, one rule.** Two rules that can change independently are two FRs, even if one
  story touches both.
