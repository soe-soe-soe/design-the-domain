# US-0051: Erinnerungen abbestellen

Status: draft · Topic: Fristerinnerung · createdAt: 2026-10-27

Als Nutzer möchte ich Fristerinnerungen abbestellen, damit ich keine Mails bekomme, die ich nicht brauche.

## Why

Wer seine Fristen anders im Blick behält, soll nicht mit E-Mails überhäuft werden.

## Content

Nutzer können die einzelnen Erinnerungen abbestellen; offen ist noch, ob es stattdessen eine Sammelmail gibt.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Erinnerungen abbestellen

  Szenario: AC1 – Abbestellte Erinnerungen werden nicht verschickt
    Angenommen Petra hat Fristerinnerungen abbestellt
    Und eine offene Frist von Petra ist fällig in 7 Tagen
    Wenn die Erinnerungen verschickt werden
    Dann erhält Petra keine Erinnerung
```

## Functional requirements

- FR-fristen-014 (new): AC1 → S1

## Open

- **AC2** (user-story): Gibt es statt einzelner Mails eine wöchentliche Sammelmail für alle, die Erinnerungen abbestellt haben? – Recommendation: Nein, wer abbestellt, bekommt keine Mails; eine Sammelmail wäre eine eigene Story. – Changes: welche Mails Petra erhält
