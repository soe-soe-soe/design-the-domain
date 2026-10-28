# Genehmigung

Der Weg eines Projekts zur BImSchG-Genehmigung, vom Antrag bis zur Bestandskraft.

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | Genehmigung | Bounded Context | `permits`; folders: `permits` | Antrag, Nachweise und Kosten bis zur Bestandskraft. |

## Antrag

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | Antrag | Aggregate Root | `Procedure` (`aggregates/procedure/model/root.py`) | Ein BImSchG-Antrag eines Projekts bei der Genehmigungsbehörde. Avoid: Verfahren. |
| Command | Antrag einreichen | Command | `submit_procedure` (`aggregates/procedure/application/commands/submit_procedure.py`) | Der Antrag geht an die Behörde; sein Status wird Eingereicht. |

## Nachweis

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | Nachweis | Aggregate Root | `Evidence` (`aggregates/evidence/model/root.py`) | Ein Gutachten oder eine Unterlage am Antrag, z. B. das Schallgutachten. Avoid: Dokument. |
| Value | Nachweisstatus | Value Object | `EvidenceStatus` (`aggregates/evidence/model/value_objects/evidence_status.py`) | Offen, Beauftragt, Geliefert, In Prüfung, Freigegeben, Abgelehnt. |
| Command | Statusübergang | Command | `transition_evidence` (`aggregates/evidence/application/commands/transition_evidence.py`) | Eine benannte Aktion, die den Nachweisstatus ändert. |
| Value | Abgelehnt | Value Object | `EvidenceStatus.REJECTED` | Ein Nachweis, den die Prüfung zurückgewiesen hat; er muss nachgebessert werden. |
| Derived Concept | Nachweis mit Problem | Query | `PermitsFacade.get_problem_evidences` | Ein nicht archivierter Nachweis, an dem ein Problem gekennzeichnet ist. |
