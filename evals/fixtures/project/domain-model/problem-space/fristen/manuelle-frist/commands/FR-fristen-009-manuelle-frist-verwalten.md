# FR-fristen-009: Manuelle Frist verwalten

Subdomain: fristen · Business object: manuelle-frist · Type: Command · Status: valid

## Rule

Ein Nutzer legt manuelle Fristen an, ändert und erledigt sie; jede manuelle Frist hat einen Titel,
eine Fälligkeit und genau einen Verantwortlichen, ein Zieltermin liegt nie nach der Fälligkeit.

## Scenarios

```gherkin
# language: de
Funktionalität: Manuelle Frist verwalten

  @US-0030
  Szenario: S1 – Anlegen mit Titel, Fälligkeit und Verantwortlichem
    Angenommen Petra ist im Projekt Windpark Nord angemeldet
    Wenn sie die Frist „Schallgutachten beauftragen“ fällig am 15.11.2026 mit Verantwortlicher Jonas anlegt
    Dann ist die Frist ein Projekttermin von Windpark Nord und Jonas ist verantwortlich

  @US-0030
  Szenario: S2 – Anlegen ohne Projekt ergibt einen persönlichen Termin
    Angenommen Petra ist angemeldet
    Wenn sie die Frist „Urlaubsantrag“ fällig am 01.12.2026 ohne Projekt anlegt
    Dann ist die Frist ein persönlicher Termin von Petra

  @US-0030
  Szenario: S3 – Ohne Fälligkeit wird nichts angelegt
    Angenommen Petra ist im Projekt Windpark Nord angemeldet
    Wenn sie die Frist „Netzanfrage“ ohne Fälligkeit anlegt
    Dann wird keine Frist angelegt und Petra erfährt, dass die Fälligkeit fehlt

  @US-0042
  Szenario: S4 – Zieltermin nach der Fälligkeit wird abgelehnt
    Angenommen eine manuelle Frist fällig am 15.11.2026
    Wenn Petra den Zieltermin 20.11.2026 setzt
    Dann bleibt die Frist ohne Zieltermin und Petra erfährt, dass der Zieltermin vor der Fälligkeit liegen muss

  @US-0030
  Szenario: S5 – Erledigen
    Angenommen eine offene manuelle Frist mit Verantwortlicher Jonas
    Wenn Jonas sie erledigt
    Dann ist die Frist erledigt

  @US-0042
  Szenario: S6 – Ändern der Fälligkeit verschiebt den Zieltermin nicht
    Angenommen eine manuelle Frist fällig am 15.11.2026 mit Zieltermin 08.11.2026
    Wenn die Fälligkeit auf den 01.12.2026 geändert wird
    Dann ist sie fällig am 01.12.2026 und ihr Zieltermin bleibt der 08.11.2026
```
