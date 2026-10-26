# FR-<subdomäne>-NNN: <Regel oder Fähigkeit>

Subdomäne: <subdomäne> · Fachobjekt: <fachobjekt oder –> · Typ: <DDD-Begriff (FR-Typ)> · Status: gültig

## Regel

<Problemraum: die Regel in Glossarbegriffen, ohne Module und Klassen.>

## Szenarien

```gherkin
# language: de
Funktionalität: <Regel oder Fähigkeit>

  @US-NNNN @geplant
  Szenario: S1 – <erwartetes Verhalten>
    Angenommen <Ausgangslage>
    Wenn <genau ein Auslöser>
    Dann <beobachtbares Ergebnis>
```

## Umsetzung

<Lösungsraum: verantwortliche Module, z. B. `domain/deadlines/regeln/signals.py` → `is_overdue`;
„offen“, solange es noch keins gibt.>

## Historie

- US-NNNN: angelegt (AK1 → S1, AK2 → S2)
- US-NNNN: S1 geändert (AK1 → S1)
