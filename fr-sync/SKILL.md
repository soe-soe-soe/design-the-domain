---
name: fr-sync
description: Schreibt die Functional Requirements (FRs) unter domain-model/ aus neuen oder geänderten User Stories fort und meldet Widersprüche zum Bestand als Fragen. Nutzen nach dem story-writer in jeder Runde von /grill-with-docs oder wenn der Nutzer Stories „in FRs übernehmen“ oder den FR-Bestand abgleichen will.
---

# FR-Sync

Ein **FR** ist der gültige Soll-Stand einer Regel oder Fähigkeit, genau einer Subdomäne
zugeordnet. Stories beschreiben Änderungen, FRs das Ergebnis aller Änderungen. Du überträgst
die Akzeptanzkriterien (AK) der Stories in FR-Szenarien und suchst dabei **Widersprüche zum
Bestand**, die das Gespräch nicht sehen kann. Nur daraus werden Fragen.

Du schreibst ausschließlich FRs unter `domain-model/<subdomäne>/`. Stories, Glossare und ADRs
liest du nur. Alles, was du schreibst, auch die Rückmeldung, ist deutsch.

## Ablage

```
domain-model/
  <subdomäne>/                     z. B. genehmigung, fristen (Umlaute ausgeschrieben)
    <fachobjekt>/                  nur Fachobjekte mit Aggregate Root, z. B. nachweis
      FR-<subdomäne>-NNN-<slug>.md
    FR-<subdomäne>-NNN-<slug>.md   Regeln ohne eigenes Fachobjekt, z. B. eines Value
    subdomaene-<name>/             vorläufige Subdomäne (siehe ihre README), FR-IDs der Trägerin
```

Welche Subdomänen es gibt und welche Bounded Contexts sie umsetzen, steht in `GLOSSARY-MAP.md`;
welche Fachobjekte eine Subdomäne hat, in den Abschnitten ihres Glossars
(`domain-model/glossaries/<subdomäne>.md`). Die Nummer `NNN` zählt je Subdomäne.

## Ablauf

1. **Lage lesen.** Lies die Stories aus dem Input (neu oder fortgeschrieben), `GLOSSARY-MAP.md`,
   die Glossare und alle FRs der Subdomänen, die sie berühren, die ADRs zum Thema und im Code
   die Bounded Contexts, um die es geht (`regeln/`, `facade.py`).

2. **Zuordnen.** Bestimme für jedes AK die Subdomäne, das Fachobjekt und den FR-Typ nach
   [references/fr-types.md](references/fr-types.md). Eine Abfrage gehört zur Subdomäne, die die
   Daten liefert, eine Policy zu der, die sie auslöst.

3. **Widersprüche prüfen**, bevor du schreibst. Eine Frage entsteht nur in drei Fällen:
   - **Ausstrahlung:** Die Änderung berührt einen anderen FR, über den die Story nichts sagt,
     z. B. eine neue Überfälligkeitsgrenze und der FR „Problemsignale“, der auf Überfälligkeit
     aufsetzt. Die Story lässt offen, ob der andere FR mitzieht.
   - **Umgesetztes überschreiben:** Ein AK widerspricht einem umgesetzten Szenario (ohne
     `@geplant` und `@unbestätigt`), und die Story löst es nicht über `Ersetzt teilweise` ab.
     Dieses Szenario änderst du nicht, bis die Frage beantwortet ist.
   - **Glossar:** Ein Szenario, das du schreiben musst, widerspricht der Beschreibung eines
     Begriffs im Glossar oder hängt an einem Begriff, dessen Bedeutung das Glossar offen lässt.
     Frag nur, wenn das Ergebnis eines Szenarios davon abhängt; Wortwahl und Stil sind kein
     Fall. Das betroffene AK wartet auf die Antwort. Das Glossar selbst änderst du nicht, das
     pflegt das Grilling.

   Ein Unterschied zum Code ist keine Frage: Er ist das Delta, das umgesetzt werden soll.
   Widersprüche zu ADRs fragt das Grilling selbst.

4. **Fortschreiben.** Für jedes AK, das nicht auf eine Antwort wartet:
   - **Auf die Regel des FR formulieren.** Ein Szenario prüft genau die Regel seines FR. Übernimm
     ein AK nicht wörtlich, wenn es eine andere Regel mitprüft: „Die Projektübersicht zeigt 1
     Problemsignal“ wird im FR „Überfälligkeit“ zu „Dann gilt die Frist als überfällig“; der
     Zählwert gehört in den FR der Problemsignale.
   - Gehört es zu einem bestehenden FR derselben Regel, ändere das passende Szenario (Nummer
     bleibt) oder hänge das nächste `Sn` an.
   - Sonst lege einen FR mit der nächsten freien Nummer der Subdomäne an, nach der Vorlage
     [assets/functional-requirement.md](assets/functional-requirement.md).
   - Jedes Szenario trägt das Tag seiner Story, solange sie nicht umgesetzt ist auch
     `@geplant`. Ist eine Story inzwischen `umgesetzt`, entferne `@geplant` an ihren Szenarien.
   - Ein AK, das als `entfallen` markiert ist, macht sein Szenario zu `@entfallen`; die
     Nummer bleibt belegt.
   - Trage in der Historie ein, welches AK zu welchem Szenario wurde.
   - Unter **Umsetzung** stehen nur Module, die es gibt; sonst „offen“.

Fertig bist du, wenn jedes AK der Input-Stories einem Szenario zugeordnet ist oder auf eine
deiner Fragen wartet.

## Tags je Szenario

| Tag | Bedeutung |
|---|---|
| `@US-0042` | Story, aus der das Szenario zuletzt geändert wurde |
| `@Bestand` | Aus dem bestehenden Code übernommen (fr-init), ohne Story |
| `@geplant` | Die Story ist noch nicht umgesetzt |
| `@unbestätigt` | Aus dem Code abgeleitet, vom Nutzer noch nicht bestätigt |
| `@entfallen` | Gilt nicht mehr; die Nummer wird nicht neu vergeben |

Die Kopfzeile des FR kennt nur `Status: gültig` oder `Status: entfallen`.

## Rückmeldung an die Grill-Session

Deine letzte Nachricht ist die Rückmeldung, genau in dieser Form. Die Session macht aus jeder
Frage eine Frage ihrer nächsten Runde, unter der genannten Story:

```
FRs:
- FR-fristen-001: Überfälligkeit einer Frist (S1 geändert)
- FR-fristen-004: Fristerinnerung per E-Mail (neu)
- US-0009/AK1: wartet auf Frage 1
Fragen:
1. Story: US-0008 · Bezug: FR-fristen-002/S1 · Typ: Domain Service (Ableitung) · Testebene: Unit · Fall: Ausstrahlung
   Frage: Soll am Fälligkeitstag auch kein Problemsignal mehr erscheinen?
   Empfehlung: Ja, das Glossar beschreibt das Problemsignal über „überfällig“.
```

`Fall` ist `Ausstrahlung`, `Umgesetztes überschreiben` oder `Glossar`; bei `Glossar` nennt
`Bezug` Glossar und Begriff (`fristen.md: Problem`). Ein AK, das auf eine Antwort wartet, steht
einmal in der FR-Liste, auch wenn mehrere Fragen es betreffen. Ohne Fragen steht dort
`Fragen: keine`. Formuliere jede Frage so, dass „ja“ deine Empfehlung annimmt.
