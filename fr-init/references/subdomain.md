# Eine Subdomäne initialisieren

Du beschreibst, was der Code einer Subdomäne heute tut, als Fachmodell: Glossar, Fachobjekte,
FRs und Szenarien. Du beschreibst, du implementierst nicht: Code und Testlogik bleiben
unverändert. Alles, was du schreibst, ist deutsch, die Bezeichner im Glossar englisch wie im
Code.

## Quellen, nach Verlässlichkeit

1. **Tests** der Bounded Contexts (`backend/tests/unit/domain/<context>/`,
   `backend/tests/integration/domain/<context>/`): Sie sind ausführbare Beispiele für Verhalten.
   Ein Test oder eine parametrisierte Gruppe ergibt ein Szenario.
2. **Regeln** unter `backend/domain/<context>/regeln/` (ADR 008): die fachlichen Regeln.
3. **Fassade, Router, Services:** Commands, Abfragen und was andere Subdomänen aufrufen.
4. **Abgleich:** das Glossar der Subdomäne, `domain-model/glossaries/_methodik.md`
   (Glossar-Art), `GLOSSARY-MAP.md`, die ADRs unter `docs/adr/`, `docs/domain/`.

## Ablauf

1. **Fachobjekte bestimmen.** Ein Fachobjekt ist eine Aggregate Root: Es wird für sich
   geändert und hat meist eigenes Repository, eigenen Service oder Router. Was nur mit einer
   Root geändert wird (Historie, Kontakte, Zuordnungen), ist eine Entity dieser Root und bekommt
   keinen Ordner. Ordnername deutsch, kleingeschrieben, Umlaute ausgeschrieben, Wörter mit
   Bindestrich (`manuelle-frist`).

2. **Glossar ergänzen** (`domain-model/glossaries/<subdomäne>.md`, Format in CLAUDE.md): je
   Fachobjekt ein Abschnitt mit seiner Zeile `Business Object | … | Aggregate Root`. Ergänze
   Zeilen für Begriffe, die deine FRs brauchen und die noch fehlen: Entities, Values, Domain
   Events (z. B. Aufrufe über eine Fassade, die melden, was geschehen ist), Commands, Derived
   Concepts. Die Beschreibung stammt aus Code, Docstrings und Tests; was du nicht belegen
   kannst, schreibst du nicht. Bestehende Zeilen änderst du nicht: Widerspricht der Code einer
   Beschreibung, wird das eine Frage. Bestehende Zeilen ordnest du dem passenden Abschnitt zu.

3. **FRs schneiden**, ein FR je Regel oder Fähigkeit, Typ nach
   `.claude/skills/fr-sync/references/fr-types.md`:
   - Ein Regel-Modul ergibt einen oder mehrere FRs (Ableitung, Invariante, Policy).
   - Reines Anlegen, Ändern und Löschen eines Fachobjekts ergibt **einen** Command-FR je
     Fachobjekt („Frist verwalten“) mit Szenarien nur für Validierungen und Rechte, nicht einen
     FR je Endpunkt.
   - Eine Abfrage mit eigener Logik (Auswahl, Sichtbarkeit, Sortierung) ergibt einen Read-Model-FR.
   - Ein Aufruf in eine andere Subdomäne, der auf etwas reagiert, ergibt einen Policy-FR in der
     auslösenden Subdomäne.
   - Ein fremdes System (Auth0, ALKIS, E-Mail) ergibt einen Anti-Corruption-Layer-FR.

   Ablage und Vorlage wie bei `fr-sync`: `domain-model/<subdomäne>/<fachobjekt>/` bzw. direkt
   in der Subdomäne, Vorlage `.claude/skills/fr-sync/assets/functional-requirement.md`, Nummern
   je Subdomäne ab `001`.

4. **Szenarien schreiben.** Je Test (oder parametrisierte Gruppe) ein Szenario in Gherkin nach
   `.claude/skills/story-writer/references/gherkin.md`, formuliert auf der Ebene der Regel des
   FR, mit den konkreten Werten des Tests. Code ohne Test bekommt ein Szenario aus dem Code und
   steht im Bericht unter „ohne Test“; einen Test schreibst du dafür nicht. Jedes Szenario trägt
   `@Bestand @unbestätigt`. Historie: `- Bestand: angelegt (fr-init, <Datum>)`. Unter Umsetzung
   die Module.

5. **Tests verweisen.** Jeder Test, aus dem ein Szenario entstanden ist, bekommt den Marker
   `@pytest.mark.fr("FR-<subdomäne>-NNN/Sn")` direkt über `def` (bei einer parametrisierten
   Gruppe einmal, bei einer Klasse, deren Tests alle dasselbe Szenario prüfen, über `class`).
   Sonst änderst du am Test nichts; `import pytest` ergänzt du, wo es fehlt.

6. **Auffälliges sammeln.** Eine Frage entsteht nur, wenn
   - Code oder Test einer Glossarbeschreibung oder einer ADR widerspricht,
   - Test und Code Unterschiedliches sagen,
   - ein Zweig fachlich verdächtig ist (unerreichbar, widersprüchlich, als TODO markiert), oder
   - dieselbe Regel an zwei Stellen umgesetzt ist.

Fertig bist du, wenn jede Regel und Fähigkeit deiner Bounded Contexts in einem FR steht, jedes
Szenario `@Bestand @unbestätigt` trägt und jeder Test, aus dem ein Szenario entstand, darauf
verweist.

## Bericht

Deine letzte Nachricht, genau in dieser Form:

```
Subdomäne: fristen
Fachobjekte: Manuelle Frist
FRs: 6 (Szenarien: 31, davon ohne Test: 4)
- FR-fristen-001: Überfälligkeit einer Frist (Domain Service (Ableitung), 4 Szenarien)
- …
Tests mit Verweis: 27
Ohne Test:
- FR-fristen-003/S5: Teamübersicht ohne Recht zeigt nur eigene Termine
Beziehungen:
- Fristen → Genehmigung: DeadlineEvent meldet erledigte Fristen an die Nachweishistorie
Fragen:
1. Bezug: <glossar>.md: <Begriff> bzw. FR-<subdomäne>-NNN/Sn · Typ: <DDD-Begriff (FR-Typ)> · Testebene: <Unit | Integration | E2E> · Fall: <Glossar | ADR | Test gegen Code | Verdächtiger Zweig | Doppelte Regel>
   Frage: <was auffällt, als Entscheidung formuliert>?
   Empfehlung: <Antwort mit Begründung>.
```

Ohne Fragen steht dort `Fragen: keine`. Formuliere jede Frage so, dass „ja“ deine Empfehlung
annimmt.
