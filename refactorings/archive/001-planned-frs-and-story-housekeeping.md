# Refactoring 001: Geplante FRs getrennt vom Ist-Stand, Housekeeping nach Abschluss einer Story

**Status:** Implemented · **Date:** 2026-10-28 · **Betrifft:** problem-fr-writer, problem-definition,
solution-definition, test-definition, story-workflow, neuer Skill `problem-housekeeping`,
neuer Validator `pts validate`

## Anlass

„Das möchte ich gerne eleganter lösen.“

Heute schreibt `problem-fr-writer` die Akzeptanzkriterien einer Story direkt in die FR-Dateien:
neue Szenarien werden angehängt, bestehende Szenarien **überschrieben** (Nummer bleibt), alles mit
`@planned` getaggt. `story-workflow` (Schritt 7) setzt danach die Story auf `done` und entfernt
`@planned`.

Probleme damit:

- **Ist und Soll sind vermischt.** Ändert eine Story ein umgesetztes Szenario, steht in der
  FR-Datei ab dem Grilling der Soll-Stand. Was die Anwendung *heute* tut, ist aus dem Problem
  Space nicht mehr lesbar – nur noch aus Git-History oder Code.
- **`@planned` ist ein Zustand pro Szenario, nicht pro Änderung.** Ein geändertes Szenario
  verliert seine alte Fassung; ein `@obsolete` aus einer offenen Story ist vom echten
  `@obsolete` nur über den Story-Tag unterscheidbar.
- **Der Abschluss ist implizit.** Das Aufräumen (Tags entfernen, Status setzen) steckt als
  Halbsatz in `story-workflow` und in `problem-fr-writer` („Once a story is `done`, remove
  `@planned`“) – zwei Stellen, keine Zuständigkeit.

## Zielbild

1. **Story sofort.** `problem-definition` schreibt die User Story wie bisher sofort; ihre
   Akzeptanzkriterien sind der Ausgangspunkt.
2. **AKs werden geplante FRs.** `problem-fr-writer` schreibt die AKs nicht mehr in die
   bestehenden FRs, sondern als **geplante FRs** neben sie. Die bestehenden FR-Dateien bleiben
   der Ist-Stand, die geplanten FRs sind der Soll-Stand nach Umsetzung. Die Story referenziert
   ihre geplanten FRs.
3. **Housekeeping nach Umsetzung.** Ist die Umsetzung fertig, meldet sie sich beim Problem Space:
   „Ich bin fertig, jetzt wird aufgeräumt.“ Ein neuer Skill `problem-housekeeping` bekommt die
   Story als Input, setzt sie auf `done`, integriert ihre geplanten FRs in den Ist-Stand und
   löscht die geplanten FRs.
4. **Im Hintergrund.** Das Housekeeping läuft als Subagent und belastet die Hauptsession nicht.

## Design

### Form der geplanten FRs

| Option | Beschreibung | Trade-off |
|---|---|---|
| A. Vollkopie | Geplante FR = komplette Zieldatei, beim Housekeeping ersetzt sie die Ist-Datei | Einfach zu lesen; zwei offene Stories auf derselben FR überschreiben sich gegenseitig (Last-Write-Wins) |
| B. Delta pro Story und FR | Geplante FR enthält nur neue, geänderte (mit Verweis auf `Sn` des Ist-Stands) und entfallende Szenarien | Merge ist eindeutig, parallele Stories bleiben getrennt; Soll-Stand muss im Kopf zusammengesetzt werden |
| C. Inline wie heute, aber alte Fassung erhalten | Ist- und Soll-Szenario nebeneinander in derselben Datei | Kein neues Artefakt; Dateien werden unübersichtlich, Ist-Stand bleibt schwer lesbar |

**Empfehlung: B.** Ablage z. B. unter `‹problem-space›/<subdomain>/planned/US-0042/FR-<subdomain>-NNN.md`
(Ordner pro Story → Housekeeping = Ordner integrieren und löschen). Eine neue FR liegt dort
vollständig, eine geänderte FR nur mit ihren Deltas:

```gherkin
  @US-0042 @changes:S2
  Szenario: S2 – <neue Fassung>

  @US-0042 @new
  Szenario: S5 – <neu>

  @US-0042 @drops:S3
```

Die Nummernvergabe (`Sn`, `FR-…-NNN`) passiert weiter beim Planen, damit Tests ihren Marker
sofort tragen können und das Housekeeping keine IDs umschreiben muss. Zwei offene Stories, die
dasselbe Szenario ändern, sind ein Open Point (neuer Case oder Erweiterung von
`overwrite-implemented`).

### Neuer Skill `problem-housekeeping`

- **Input:** eine Story-ID. Aufgerufen von `story-workflow` Schritt 7 (nicht von
  `solution-definition` – die platziert nur, sie weiß nicht, wann die Umsetzung fertig ist).
- **Schritte:**
  1. Vorbedingung prüfen (siehe „Validierung“). Schlägt sie fehl: nichts ändern, melden.
  2. Story auf `Status: done`.
  3. Pro geplanter FR: Deltas in die Ist-FR übernehmen (`@changes` ersetzt, `@new` hängt an,
     `@drops` macht `@obsolete`), History-Eintrag `US-0042: implemented (…)`; neue FRs
     verschieben.
  4. `planned/US-0042/` löschen, Referenzen in der Story auf die Ist-FRs umbiegen.
  5. Eigener Commit nach `‹project-rules›`.
- **Fragt nie.** Konflikt (Ist-Szenario seit dem Planen geändert, Datei fehlt) → abbrechen und
  berichten.

### Anpassungen der bestehenden Skills

| Skill | Änderung |
|---|---|
| `problem-fr-writer` | Schreibt in `planned/<story>/` statt in Ist-FRs; `@planned` entfällt; Check `overwrite-implemented` liest den Ist-Stand, der jetzt sauber ist; Satz „Once a story is done…“ entfällt |
| `problem-definition` | Story verweist auf ihre geplanten FRs; Schluss unverändert (`ready`) |
| `solution-definition`, `test-definition` | Lesen „die geplanten FRs der Story“ statt „Szenarien mit `@planned`“; `@obsolete` aus der Story wird `@drops` |
| `story-workflow` | Schritt 7: Implementierung committen, dann `problem-housekeeping` anstoßen |
| Templates, Evals, `‹methodology-glossary›` | Begriff „Geplante FR“, Ablage, Tags `@new`/`@changes`/`@drops` |

### Validierung beim Housekeeping

Frage: Soll das Housekeeping noch einmal prüfen, ob die Story wirklich umgesetzt ist?

**Inhaltlich: nein, das wäre redundant.** Die Bedeutung ist schon dreifach gesichert:
`test-definition` schreibt pro Szenario einen roten Test mit Marker, der Mensch prüft die Tests
am Review-Gate (Schritt 4), `code-review` prüft gegen die Spec (Schritt 6), und die Suite muss
grün sein. Eine zweite semantische Prüfung durch ein LLM ohne Testausführung wäre schwächer als
das, was schon passiert ist, und kostet Tokens.

**Mechanisch: ja, als Guard.** Billig und deterministisch, keine Validierung im eigentlichen
Sinn:

- Jedes Szenario der geplanten FRs hat einen Test mit seinem Marker (`‹scenario-marker›`, grep).
- Der Implementierungs-Commit existiert (Story-Workflow übergibt ihn).
- Die Ist-Szenarien, auf die ein `@changes`/`@drops` zeigt, sind seit dem Planen unverändert.

Der Guard verhindert vor allem, dass Housekeeping auf eine Story läuft, die außerhalb von
`story-workflow` „fertig“ gemeldet wurde.

### Validator `pts validate`

Vorbild: `openspec validate`. OpenSpec prüft das Format seiner Specs mit einem Programm, nicht
mit einem LLM, weil `archive` die Deltas per Code in die Specs merged und Requirements über
ihren exakten Namen zuordnet. `archive` ruft die Prüfung selbst auf und verweigert bei Fehlern.
Mit den Deltas aus Option B gilt für das Housekeeping dasselbe: Der Merge ist nur so verlässlich
wie das Format der geplanten FRs.

**Template vs. Validator.** Die Templates sind eine Bitte an das LLM, die meistens befolgt wird.
Der Validator setzt durch: Was nicht passt, fällt jedes Mal durch, und Claude bekommt die
Fehlermeldung zurück.

**Regeln** (Auswahl, deterministisch prüfbar):

- Kopfzeile: Felder vollständig, `Type` ∈ FR-Typen, `Status` ∈ {valid, obsolete}; Story-Status
  ∈ {draft, ready, done}.
- IDs: FR-Nummern und `Sn` eindeutig, nie wiederverwendet (Abgleich mit Git); AC-Nummern stabil.
- Gherkin parsebar (offizieller Parser), genau ein `Wenn` pro Szenario.
- Tags nur aus der erlaubten Menge; `@US-NNNN` zeigt auf eine existierende Story.
- `@open` am Szenario ⇔ Eintrag unter `## Open`, Eintrag im Format des Begriffs „Open point“.
- Story `ready` ⇒ kein `## Open`.
- Deltas: Ziel von `@changes:Sn` / `@drops:Sn` existiert im Ist-Stand; zwei offene Stories ändern
  nicht dasselbe `Sn` (sonst Open Point); `planned/<story>/` gehört zu einer existierenden Story.
- Merge-Probelauf wie bei OpenSpec: zeigt, was das Housekeeping tun würde, ohne zu schreiben.

**Einbindung:**

1. Skript im Plugin (z. B. Node mit `@cucumber/gherkin`), aufrufbar als `pts validate [--strict]`.
2. PostToolUse-Hook auf Write/Edit unter `‹problem-space›` und `‹stories›`: Fehler gehen direkt
   als Feedback an Claude.
3. Abschlusskriterium in `problem-story-writer`, `problem-fr-writer` und `problem-definition`.
4. `problem-housekeeping` ruft ihn als ersten Schritt des Guards auf und bricht bei Fehlern ab.
5. Optional in der CI des Projekts.

### Hintergrund-Ausführung

Machbar per Subagent (Agent-Tool, `run_in_background`). Trade-offs:

- **Pro:** Kontext und Wartezeit der Hauptsession bleiben frei.
- **Contra Atomarität:** Heute ist „Story done“ ein Commit. Mit Hintergrund-Housekeeping gibt es
  ein Zwischenstadium (Code umgesetzt, Problem Space noch Soll). Startet in der Zeit die nächste
  Grilling-Session oder Story auf derselben FR, liest sie einen veralteten Ist-Stand.
- **Contra Rückfragen:** Ein Hintergrund-Agent kann nicht fragen – daher „fragt nie, bricht ab
  und berichtet“.
- **Aufwand:** Der Merge ist klein und weitgehend mechanisch; er dauert Sekunden.

**Empfehlung:** Subagent ja (hält den Kontext sauber), Hintergrund ja, aber mit zwei Regeln:
eigener Commit, und `problem-fr-writer`/`problem-definition` prüfen beim Start, ob für eine
berührte FR noch ein `planned/<story>/` einer `done`-Story liegt – dann erst Housekeeping
nachholen. Damit ist das Zwischenstadium sichtbar statt still inkonsistent.

## Offene Fragen

1. Delta-Format (Option B) oder doch Vollkopie (A) – wie oft ändern parallel offene Stories
   dieselbe FR?
2. Ablage `planned/` pro Subdomain oder zentral pro Story unter `‹stories›/US-0042/`?
3. Migration bestehender Projekte: vorhandene `@planned`-Szenarien in `planned/` überführen oder
   auslaufen lassen?
4. Decision Record in `problem-fr-writer/decision-records/` beim Umsetzen anlegen.
5. Validator: als Hook im Plugin ausliefern oder vom Projekt einbinden lassen? `--strict`
   standardmäßig an?

## Umsetzung

Umgesetzt am 2026-11-01 (Commits 027ba3c, e219423, c771cc4 auf `origin/main`), mit Abweichungen
vom Entwurf:

- Geplante FRs: **eine Planned-Datei pro FR** in `planned/` neben der aktiven FR statt Ordner pro
  Story (Entscheidung: `problem-fr-writer/decision-records/003-planned-fr-files.md`); Tags
  `@base-<tag>` statt `@changes`/`@drops`.
- Housekeeping: **Skript `scripts/requirements.py`** (`check`, `complete`, `cancel`, `history`)
  statt Skill `problem-housekeeping`, synchron vor dem Commit statt im Hintergrund
  (`story-workflow/decision-records/003-housekeeping-by-script.md`).
- Validator `pts validate` und Hook: nicht umgesetzt; `requirements.py check` deckt Basis- und
  Parallelitätsprüfung ab.
