# FR types

The type stands as a DDD term in the FR header. It decides the test level here and the
building block in the solution space (skill `solution-sync`).

| Type | Sign in the AC | Example | Test level |
|---|---|---|---|
| Invariant | "darf nur", "nie", permitted transitions | Nachweisstatus only via permitted transitions (ADR 007) | Unit |
| Domain Service | "gilt als", "ergibt sich aus", "wird berechnet" | Überfälligkeit, Problemsignale, IRR, Phase aus Antragsstatus | Unit |
| Policy | "wenn X geschieht, dann …" across a subdomain boundary | Frist erledigt → entry in the Nachweishistorie | Unit + Integration |
| Command | user creates, changes, deletes, advances | Projekt anlegen, Frist abhaken | Integration |
| Query | what a view or API returns: selection, visibility, order | Termine der Startseite, Teamübersicht | Integration |
| Anti-Corruption Layer | a foreign system: Auth0, ALKIS, e-mail delivery | Organisationsname aus Auth0 | Integration with fake |

## Boundaries

- **Calculated value in a view:** if the Dann checks a calculated value ("zeigt 2
  Problemsignale"), the AC belongs to the Domain Service, even if the value appears in a view.
  Query only for what the view itself decides: which entries, who sees what, in which order.
- **Domain event:** an event is no FR. That it occurs is a scenario of the triggering
  Command; each reaction to it is an FR of its own of type Policy.
- **One FR, one rule.** Two rules that can change independently are two FRs, even if one
  story touches both.
