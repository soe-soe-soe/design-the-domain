---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Du bist der Story-Writer für eine laufende Grill-Session. Antworten der letzten Fragerunde zum Thema „Problemsignale in der Projektübersicht“:

- Die Projektübersicht zeigt je Projekt die Zahl der Problemsignale.
- Ein Problemsignal ist eine überfällige Frist oder eine als Problem gekennzeichnete Frist.
- Überfällig ist eine Frist, wenn ihr Fälligkeitsdatum heute oder früher liegt.
- Eine Frist ohne Fälligkeitsdatum ist nie überfällig.
- Eine überfällige Frist, die zugleich als Problem gekennzeichnet ist, zählt einmal als überfällig und einmal als Problem.
- Erledigte Fristen zählen nie als Signal.
- Begründung: Projektleitungen übersehen heute überfällige Fristen, weil sie nur im Projekt selbst sichtbar sind.

Schreib die Stories und gib die Rückmeldung an die Session.
