---
tags: [test-definition]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Schreib die Tests für Story US-0048 (Nachbesserung nach Ablehnung). solution-definition hat sie in dieser Session eingeordnet und die Hülle angelegt, das ist ihr Bericht:

```
Placement US-0048: Nachbesserung nach Ablehnung
| Scenario | Type | Context / aggregate | Building block → file |
|---|---|---|---|
| FR-genehmigung-025/S1 | Policy | permits / procedure | policy → aggregates/procedure/application/policies/on_evidence_rejected.py (new); event → aggregates/evidence/model/events/evidence_rejected.py (new), published by transition_evidence (exists) |
Interfaces:
- event: EvidenceRejected (new), published by transition_evidence through the EventBus when the target is rejected; on_evidence_rejected is already subscribed in build_event_bus
Glossary: genehmigung.md „Nachbesserung“ → Value Object, `ProcedureStatus.REWORK` = `rework`
Shell:
- backend/domain/permits/aggregates/evidence/model/events/evidence_rejected.py (new) `EvidenceRejected`
- backend/domain/permits/aggregates/procedure/application/policies/on_evidence_rejected.py (new) `on_evidence_rejected`
- backend/domain/permits/aggregates/procedure/model/root.py `ProcedureStatus.REWORK` (new member)
Questions: none
```

Datenbank, Python-Abhängigkeiten und Node gibt es in dieser Umgebung nicht; lass die Tests nicht laufen, prüf sie nur statisch.
