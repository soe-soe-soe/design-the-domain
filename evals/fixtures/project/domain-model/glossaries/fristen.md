# Fristen

Stichtage in Projekten und persönlich, ihre Fälligkeit und wer sie verantwortet.

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | Fristen | Bounded Context | `deadlines`; folders: `deadlines` | Stichtage, ihre Fälligkeit und ihre Verantwortlichen. |
| Derived Concept | Frist | – | – | Oberbegriff für einen Stichtag, bis zu dem etwas erledigt sein muss: eine manuelle oder eine abgeleitete Frist. Avoid: Termin, Deadline. |
| Value | Fälligkeit | Value Object | `due_date` | Das Datum, an dem eine Frist abläuft. Avoid: Ablaufdatum. |
| Value | Verantwortlicher | Value Object | `owner` | Die Person, die eine Frist erledigen muss; jede Frist hat genau einen. Avoid: Zuständiger, Owner. |
| Derived Concept | Projekttermin | Query | `project_deadlines` | Eine Frist, die zu einem Projekt gehört; alle Projektbeteiligten sehen sie. |
| Derived Concept | Persönlicher Termin | Query | `personal_deadlines` | Eine manuelle Frist ohne Projekt; nur ihr Verantwortlicher sieht sie. |

## Manuelle Frist

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | Manuelle Frist | Aggregate Root | `ManualDeadline` | Eine Frist, die ein Nutzer selbst anlegt, mit Titel, Fälligkeit und Verantwortlichem. |
| Value | Zieltermin | Value Object | `target_date` | Ein freiwilliges internes Datum vor der Fälligkeit, bis zu dem die Frist erledigt sein soll. |
| Command | Frist anlegen | Command | `create_manual_deadline` | Ein Nutzer legt eine manuelle Frist an. |
| Command | Frist ändern | Command | `update_manual_deadline` | Titel, Fälligkeit, Zieltermin oder Verantwortlicher einer manuellen Frist ändern sich. |
| Command | Frist erledigen | Command | `complete_deadline` | Der Verantwortliche hakt die Frist als erledigt ab. |

## Abgeleitete Frist

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | Abgeleitete Frist | Aggregate Root | `DerivedDeadline` | Eine Frist, die aus einem Nachweis der Genehmigung entsteht: seine Fälligkeit ist das Lieferdatum des Nachweises. Niemand legt sie von Hand an. |
