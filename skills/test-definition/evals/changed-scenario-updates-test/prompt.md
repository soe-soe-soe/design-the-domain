---
tags: [test-definition]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Schreib die Tests für Story US-0049 (Fälligkeitstag ist noch nicht überfällig). solution-definition hat sie in dieser Session eingeordnet und die Hülle angelegt, das ist ihr Bericht:

```
Placement US-0049: Fälligkeitstag ist noch nicht überfällig
| Scenario | Type | Context / aggregate | Building block → file |
|---|---|---|---|
| FR-fristen-001/S1 | Domain Service | deadlines (not migrated) | specification → regeln/signals.py `is_overdue` (exists); target aggregates/deadline/model/specifications/is_overdue.py |
Questions: none
```

Datenbank, Python-Abhängigkeiten und Node gibt es in dieser Umgebung nicht; lass die Tests nicht laufen, prüf sie nur statisch.
