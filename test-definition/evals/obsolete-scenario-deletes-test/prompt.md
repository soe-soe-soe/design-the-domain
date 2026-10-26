---
tags: [test-definition]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Schreib die Tests für Story US-0052 (Zieltermin ist Pflicht). solution-definition hat sie in dieser Session eingeordnet und die Hülle angelegt, das ist ihr Bericht:

```
Placement US-0052: Zieltermin ist Pflicht
| Scenario | Type | Context / aggregate | Building block → file |
|---|---|---|---|
| FR-fristen-001/S4 | Domain Service | deadlines (not migrated) | obsolete: the branch for a missing due date in regeln/signals.py `is_overdue` goes away in the implementation |
Questions: none
```

Datenbank, Python-Abhängigkeiten und Node gibt es in dieser Umgebung nicht; lass die Tests nicht laufen, prüf sie nur statisch.
