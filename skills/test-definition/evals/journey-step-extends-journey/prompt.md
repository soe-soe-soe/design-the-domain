---
tags: [test-definition]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Schreib die Tests für Story US-0047 (Nachweis mit Begründung ablehnen). solution-definition hat sie in dieser Session eingeordnet und die Hülle angelegt, das ist ihr Bericht:

```
Placement US-0047: Nachweis mit Begründung ablehnen
| Scenario | Type | Context / aggregate | Building block → file |
|---|---|---|---|
| FR-genehmigung-024/S1 | Command | permits / evidence | command → aggregates/evidence/application/commands/reject_evidence.py (new) |
Interfaces:
- endpoint: POST /evidences/{evidence_id}/reject (new), api/endpoints/reject_evidence.py
Glossary: genehmigung.md „Begründung der Ablehnung“ → Value Object, `Evidence.rejection_reason`
Shell:
- backend/domain/permits/aggregates/evidence/application/commands/reject_evidence.py (new) `reject_evidence`
- backend/domain/permits/api/endpoints/reject_evidence.py (new) route `reject_evidence`
- backend/domain/permits/api/schemas/evidence.py (new) `RejectEvidenceRequest`
- backend/domain/permits/aggregates/evidence/model/root.py `Evidence.rejection_reason` (new field)
Questions: none
```

Datenbank, Python-Abhängigkeiten und Node gibt es in dieser Umgebung nicht; lass die Tests nicht laufen, prüf sie nur statisch.
