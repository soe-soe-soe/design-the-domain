---
name: fr-init
description: Legt das Fachmodell für bestehenden Code an – Glossar, Fachobjekte und FRs je Subdomäne, parallel.
disable-model-invocation: true
---

# FR-Init

Du ziehst das Fachmodell unter `domain-model/` für Code nach, der schon existiert: Glossar,
Fachobjekte und FRs je Subdomäne, die Szenarien aus den bestehenden Tests, und in jedem dieser
Tests den Verweis auf sein Szenario. Danach hat `fr-sync` einen Bestand, gegen den es
Widersprüche finden kann.

Du dirigierst: Jede Subdomäne bearbeitet ein eigener Subagent, alle gleichzeitig. Du startest
sie, gleichst ihre Ergebnisse ab und berichtest dem Nutzer. Alles, was du schreibst, ist
deutsch.

## Ablauf

1. **Umfang klären.** Lies `GLOSSARY-MAP.md` und frag den Nutzer mit AskUserQuestion, ob er eine
   Subdomäne, mehrere oder alle initialisieren will; bei mehreren lass ihn wählen. Nennt der
   Aufruf schon Subdomänen (`/fr-init fristen projekt`), entfällt die Frage. Querschnitt in
   `backend/core/` gehört nicht dazu.

2. **Subagenten starten**, alle in **einer** Nachricht, damit sie parallel laufen: je Subdomäne
   ein Subagent mit diesem Auftrag:

   > Initialisiere die Subdomäne `<subdomäne>` (Bounded Contexts: `<aus GLOSSARY-MAP.md>`) nach
   > `.claude/skills/fr-init/references/subdomain.md`. Schreib nur in
   > `domain-model/<subdomäne>/`, `domain-model/glossaries/<subdomäne>.md` und in Tests unter
   > `backend/tests/**/domain/<context>/` deiner Bounded Contexts. Deine letzte Nachricht ist der
   > Bericht in der Form, die die Referenz vorgibt.

3. **Abgleichen**, sobald alle Berichte da sind:
   - **Policies über Grenzen:** Haben zwei Subagenten dieselbe Reaktion beschrieben, bleibt der
     FR in der auslösenden Subdomäne; den anderen löschst du und setzt in dessen Tests den
     Verweis um.
   - **Beziehungen:** Trag neue Beziehungen zwischen Subdomänen aus den Berichten unter
     `## Relationships` in `GLOSSARY-MAP.md` ein.
   - **Kontrolle:** `cd backend && pytest --collect-only -q` läuft ohne Fehler; jeder
     `@pytest.mark.fr` nennt ein Szenario, das es gibt.

4. **Berichten.** Dem Nutzer je Subdomäne: Fachobjekte, Zahl der FRs und Szenarien, Tests mit
   Verweis, Szenarien ohne Test. Darunter die Fragen der Subagenten im Format der
   Grill-Session (CLAUDE.md, Herkunftszeile mit `🧩 fr-init`), gruppiert je Subdomäne. Zum
   Schluss die Frage, welche Subdomänen er im Block bestätigt.

5. **Bestätigen.** Für jede Subdomäne, die der Nutzer bestätigt, entfernst du `@unbestätigt` an
   allen ihren Szenarien. Szenarien, die eine offene Frage betreffen, behalten es, bis sie
   beantwortet ist.

Fertig bist du, wenn jede gewählte Subdomäne ein Glossar mit ihren Fachobjekten, FRs für ihre
Regeln und Fähigkeiten und Verweise in ihren Tests hat, und der Nutzer seine Bestätigung oder
seine Antworten gegeben hat.
