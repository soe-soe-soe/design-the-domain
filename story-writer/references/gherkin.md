# Gherkin für Akzeptanzkriterien

Akzeptanzkriterien sind Fachtext. Aus jedem Szenario wird später genau ein Test, deshalb muss
jedes für sich prüfbar sein.

## Schlüsselwörter (deutsch)

`# language: de` steht in der ersten Zeile des Blocks.

| Deutsch | Englisch |
|---|---|
| Funktionalität | Feature |
| Grundlage | Background |
| Szenario | Scenario |
| Szenariogrundriss | Scenario Outline |
| Beispiele | Examples |
| Angenommen | Given |
| Wenn | When |
| Dann | Then |
| Und / Aber | And / But |

## Regeln

- **Fachlich, nicht bedienend.** Schreibe, was geschieht, nicht, was geklickt wird:
  „Wenn die Frist erledigt wird“ statt „Wenn ich auf den Haken klicke“. UI-Details nur, wenn die
  Oberfläche selbst die Anforderung ist.
- **Ein Verhalten pro Szenario.** Genau ein `Wenn`, die `Dann` prüfen dessen Folgen. Zwei
  Auslöser ergeben zwei Szenarien.
- **Konkrete Beispielwerte.** Echte Daten, Beträge und Status statt „ein Datum“ oder „X“. Der
  erwartete Wert im `Dann` stammt aus der Entscheidung, nicht aus einer Rechnung, die der Code
  ebenso anstellen würde.
- **Wertetabellen als Szenariogrundriss.** Wird dieselbe Regel mit mehreren Werten geprüft
  (Grenzen, Berechnungen), schreibe einen `Szenariogrundriss` mit `Beispiele` statt mehrerer
  fast gleicher Szenarien.
- **Glossarbegriffe.** Verwende die Begriffe aus den Glossaren der Subdomänen, nicht die Wörter hinter „Nicht: …“.
- **Grenzen und Gegenfälle.** Gilt eine Regel ab einer Schwelle, gehört der Fall direkt
  darunter dazu. Gilt sie für einen Mandanten, Status oder eine Rolle, gehört der
  ausgeschlossene Fall dazu.
- **Name = Nummer + Aussage.** `Szenario: AK2 – Frist ohne Datum ist nie überfällig`. Die
  Aussage ist das erwartete Verhalten, kein Thema („Fristen ohne Datum“).

## Beispiel: Szenariogrundriss

```gherkin
# language: de
Funktionalität: Überfällige Fristen

  Szenariogrundriss: AK1 – Überfällig ab dem Fälligkeitstag
    Angenommen eine Frist ist fällig am <fällig>
    Wenn heute der 16.10.2026 ist
    Dann ist die Frist <ergebnis>

    Beispiele:
      | fällig     | ergebnis        |
      | 15.10.2026 | überfällig      |
      | 16.10.2026 | überfällig      |
      | 17.10.2026 | nicht überfällig |
```
