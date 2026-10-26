# FR-Typen

Der Typ steht als DDD-Begriff mit dem FR-Typ in Klammern in der Kopfzeile und bestimmt die
Testebene.

| Typ | Erkennungszeichen im AK | Beispiel | Testebene |
|---|---|---|---|
| Aggregat-Invariante (Invariante) | „darf nur“, „nie“, zulässige Übergänge | Nachweisstatus nur über zulässige Übergänge (ADR 007) | Unit |
| Domain Service (Ableitung) | „gilt als“, „ergibt sich aus“, „wird berechnet“ | Überfälligkeit, Problemsignale, IRR, Phase aus Antragsstatus | Unit |
| Policy (Reaktion) | „wenn X geschieht, dann …“ über eine Grenze zwischen Subdomänen | Frist erledigt → Eintrag in der Nachweishistorie | Unit + Integration |
| Command (Kommando) | Nutzer legt an, ändert, löscht, schaltet weiter | Projekt anlegen, Frist abhaken | Integration |
| Read Model (Abfrage) | was eine Ansicht oder API liefert: Auswahl, Sichtbarkeit, Sortierung | Termine der Startseite, Teamübersicht | Integration |
| Anti-Corruption Layer (Anbindung) | ein fremdes System: Auth0, ALKIS, E-Mail-Versand | Organisationsname aus Auth0 | Integration mit Fake |

## Abgrenzungen

- **Berechneter Wert in einer Ansicht:** Prüft das Dann einen berechneten Wert („zeigt 2
  Problemsignale“), gehört das AK zur Ableitung, auch wenn der Wert in einer Ansicht erscheint.
  Read Model nur für das, was die Ansicht selbst entscheidet: welche Einträge, wer was sieht,
  in welcher Reihenfolge.
- **Domain Event:** Ein Event ist kein FR. Dass es eintritt, ist ein Szenario des auslösenden
  Command; jede Reaktion darauf ist ein eigener FR vom Typ Policy (Reaktion).
- **Ein FR, eine Regel.** Zwei Regeln, die sich unabhängig ändern können, sind zwei FRs, auch
  wenn eine Story beide berührt.
