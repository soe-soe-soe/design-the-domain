# Genehmigung

Genehmigungsverfahren eines Projekts und die Nachweise, die die Behörde verlangt.

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | Genehmigung | Bounded Context | `permits`; folders: `permits` | Genehmigungsverfahren und ihre Nachweise. |
| Value | Behörde | Value Object | `authority` | Die Stelle, die das Verfahren führt und Nachweise verlangt. |

## Genehmigungsverfahren

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | Genehmigungsverfahren | Aggregate Root | `Permit` | Das Verfahren, in dem die Behörde über die Genehmigung eines Projekts entscheidet. Avoid: Antrag. |
| Value | Verfahrensstatus | Value Object | `PermitStatus` | Stand des Verfahrens: vorbereitet, eingereicht, genehmigt oder abgelehnt. |
| Entity | Nachweis | Entity | `Evidence` | Ein Gutachten oder Dokument, das die Behörde bis zu einem Lieferdatum verlangt. Avoid: Unterlage. |
| Value | Lieferdatum | Value Object | `delivery_date` | Das Datum, bis zu dem ein Nachweis bei der Behörde sein muss. |
| Value | Nachweisstatus | Value Object | `EvidenceStatus` | Stand eines Nachweises: angefordert, in Arbeit, geliefert oder nachgefordert. |
