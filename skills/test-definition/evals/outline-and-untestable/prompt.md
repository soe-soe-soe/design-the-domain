---
tags: [test-definition]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Schreib die Tests für Story US-0045 (Gültigkeit von Gutachten). solution-definition hat sie in dieser Session eingeordnet und die Hülle angelegt, das ist ihr Bericht:

```
Placement US-0045: Gültigkeit von Gutachten
| Scenario | Type | Context / aggregate | Building block → file |
|---|---|---|---|
| FR-genehmigung-020/S1 | Domain Service | permits / evidence | domain service → aggregates/evidence/model/services/validity_end.py (new) |
| FR-genehmigung-020/S2 | Domain Service | permits / evidence | domain service → aggregates/evidence/model/services/validity_end.py (new) |
Shell:
- backend/domain/permits/aggregates/evidence/model/services/validity_end.py (new) `calculate_validity_end`
Questions: none
```

Die Datenbank gibt es in dieser Umgebung nicht; lass die Tests nicht laufen, prüf sie nur statisch.
