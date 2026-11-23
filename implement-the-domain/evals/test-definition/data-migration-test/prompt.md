---
tags: [test-definition]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Schreib die Tests für Story US-0046 (Gültig bis für bestehende Gutachten). solution-definition hat sie in dieser Session eingeordnet und die Hülle angelegt, das ist ihr Bericht:

```
Placement US-0046: Gültig bis für bestehende Gutachten
| Scenario | Type | Context / aggregate | Building block → file |
|---|---|---|---|
| FR-genehmigung-022/S1 | Data Migration | permits / evidence | migration → backend/ops/migrations/versions/c3d4e5f6a7b8_evidence_valid_until.py (new) |
Schema: evidence.valid_until (date, nullable)
Shell:
- backend/ops/migrations/versions/c3d4e5f6a7b8_evidence_valid_until.py (new, empty)
Questions: none
```

Die Datenbank gibt es in dieser Umgebung nicht; lass die Tests nicht laufen, prüf sie nur statisch.
