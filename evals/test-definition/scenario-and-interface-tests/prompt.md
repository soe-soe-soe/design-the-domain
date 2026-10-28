---
tags: [test-definition]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Schreib die Tests für Story US-0044 (Abgelehnte Nachweise als Problemsignal). solution-definition hat sie in dieser Session eingeordnet und die Hülle angelegt, das ist ihr Bericht:

```
Placement US-0044: Abgelehnte Nachweise als Problemsignal
| Scenario | Type | Context / aggregate | Building block → file |
|---|---|---|---|
| FR-fristen-013/S1 | Query | deadlines (not migrated) | query → service.py `DeadlineService.get_signals` (exists); target application/queries/project_signals.py |
Interfaces:
- facade: PermitsFacade.get_rejected_evidences (new), used by deadlines
Shell:
- backend/domain/permits/facade/facade.py `PermitsFacade.get_rejected_evidences` (new method)
Questions: none
```

Die Datenbank gibt es in dieser Umgebung nicht; lass die Tests nicht laufen, prüf sie nur statisch.
