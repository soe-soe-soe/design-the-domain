# Domain Map

Software für Projektierer von Windparks: von der Fläche über die
BImSchG-Genehmigung bis zur Wirtschaftlichkeit eines Projekts.

## Subdomains

| Subdomain | Type | Status | Glossary | Description |
|---|---|---|---|---|
| Projekt | open | established | [projekt.md](../glossaries/projekt.md) | Das Windparkprojekt mit seinem Stand und seiner Projektgesellschaft. |
| Genehmigung | open | established | [genehmigung.md](../glossaries/genehmigung.md) | Antrag, Nachweise und Kosten bis zur Bestandskraft der BImSchG-Genehmigung. |
| Fristen | open | established | [fristen.md](../glossaries/fristen.md) | Stichtage in Projekten und persönlich, ihre Verantwortlichen und die Problemsignale. |

## Relationships

| From | To | Description |
|---|---|---|
| Genehmigung | Fristen | Nachweise mit Problem werden zu Problemsignalen. |
| Fristen | Projekt | Problemsignale erscheinen in der Projektübersicht. |
| Genehmigung, Fristen | – | Notiz und Problem bedeuten an Nachweis und manueller Frist dasselbe (geteilte Begriffe). |
