# US-0030: Fristen verwalten

Status: done · Topic: Fristen · createdAt: 2026-09-01 · doneAt: 2026-09-20

Als Projektleitung möchte ich Fristen anlegen und erledigen, damit kein Stichtag eines Projekts verloren geht.

## Why

Fristen standen bisher in Tabellen und gingen bei Übergaben verloren.

## Content

Nutzer legen manuelle Fristen mit Fälligkeit und Verantwortlichem an, mit oder ohne Projekt, und
erledigen sie. Nachweise der Genehmigung erscheinen als abgeleitete Fristen.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Fristen verwalten

  Szenario: AC1 – Projekttermin anlegen
    Angenommen Petra ist im Projekt Windpark Nord angemeldet
    Wenn sie die Frist „Schallgutachten beauftragen“ fällig am 15.11.2026 mit Verantwortlicher Jonas anlegt
    Dann ist die Frist ein Projekttermin von Windpark Nord und Jonas ist verantwortlich

  Szenario: AC2 – Nachweis erscheint als abgeleitete Frist
    Angenommen die Behörde verlangt das Schallgutachten mit Lieferdatum 23.10.2026
    Wenn die abgeleitete Frist dazu angezeigt wird
    Dann ist sie fällig am 23.10.2026
```

## Functional requirements

- FR-fristen-009 (new): AC1 → S1
- FR-fristen-006 (new): AC2 → S1
