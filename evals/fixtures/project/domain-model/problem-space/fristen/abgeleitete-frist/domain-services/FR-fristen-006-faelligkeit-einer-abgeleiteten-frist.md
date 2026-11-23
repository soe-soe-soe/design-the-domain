# FR-fristen-006: Fälligkeit einer abgeleiteten Frist

Subdomain: fristen · Business object: abgeleitete-frist · Type: Domain Service · Status: valid

## Rule

Eine abgeleitete Frist ist fällig am Lieferdatum ihres Nachweises; sie ist erledigt, sobald der
Nachweis geliefert ist, und wird wieder offen, wenn die Behörde ihn nachfordert.

## Scenarios

```gherkin
# language: de
Funktionalität: Fälligkeit einer abgeleiteten Frist

  @US-0030
  Szenario: S1 – Fällig am Lieferdatum des Nachweises
    Angenommen die Behörde verlangt das Schallgutachten mit Lieferdatum 23.10.2026
    Wenn die abgeleitete Frist dazu angezeigt wird
    Dann ist sie fällig am 23.10.2026

  @US-0030
  Szenario: S2 – Geliefert heißt erledigt
    Angenommen eine abgeleitete Frist zum Schallgutachten ist offen
    Wenn das Schallgutachten als geliefert erfasst wird
    Dann ist die abgeleitete Frist erledigt

  @US-0030
  Szenario: S3 – Nachgefordert heißt wieder offen
    Angenommen eine abgeleitete Frist zum Schallgutachten ist erledigt
    Wenn die Behörde das Schallgutachten mit neuem Lieferdatum 30.11.2026 nachfordert
    Dann ist die abgeleitete Frist offen und fällig am 30.11.2026
```
