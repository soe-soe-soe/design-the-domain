# US-0049: Fälligkeitstag ist noch nicht überfällig

Status: ready · Topic: Überfälligkeit · Date: 2026-10-26

Als Projektleiter möchte ich, dass eine Frist am Fälligkeitstag noch nicht als überfällig gilt.

## Why

Am Fälligkeitstag kann die Frist noch fristgerecht erledigt werden; ein Problemsignal wäre verfrüht.

Supersedes in part: FR-fristen-001/S1 (am Fälligkeitstag überfällig)

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Überfälligkeit einer Frist

  Szenario: AC1 – Am Fälligkeitstag ist eine Frist noch nicht überfällig
    Angenommen eine offene Frist ist fällig am 16.10.2026
    Wenn heute der 16.10.2026 ist
    Dann ist die Frist nicht überfällig
```
