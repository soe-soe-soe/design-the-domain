# FR-deadlines-001: Überfälligkeit einer Frist

Kontext: deadlines · Typ: Domain Service (Ableitung) · Status: gültig

## Regel

Eine Frist ist überfällig, wenn ihr Fälligkeitsdatum heute oder früher liegt. Eine Frist ohne
Fälligkeitsdatum ist nie überfällig.

## Szenarien

```gherkin
# language: de
Funktionalität: Überfälligkeit einer Frist

  @US-0007
  Szenario: S1 – Heute fällige Frist ist überfällig
    Angenommen eine Frist ist fällig am 16.10.2026
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist als überfällig

  @US-0007
  Szenario: S2 – Frist ohne Datum ist nie überfällig
    Angenommen eine Frist hat kein Fälligkeitsdatum
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist nicht als überfällig
```

## Umsetzung

`domain/deadlines/regeln/signals.py` → `is_overdue`

## Historie

- US-0007: angelegt (AK1 → S1, AK2 → S2)
