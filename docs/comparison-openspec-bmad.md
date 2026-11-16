# Vergleich: Problem Definition, OpenSpec, BMAD

Stand: 2026-10-28 · Umfang: nur die fachliche Analyse (Problemraum). Ideation, Marktrecherche und
Umsetzung sind außen vor.

Die Tabelle listet Ergebnisse, nicht Methodik. ✅ erfüllt · ◐ teilweise · ❌ fehlt.

| Ergebnis | Problem Definition | OpenSpec | BMAD |
|---|---|---|---|
| **Aktueller Soll-Zustand an einer Stelle** | ✅ FRs | ✅ `specs/` | ❌ Code ist die Quelle |
| **Änderungen nachvollziehbar** | ◐ Story + History; Delta-Operationen geplant ([Refactoring 001](../refactorings/archive/001-planned-frs-and-story-housekeeping.md)) | ✅ Delta-Operationen + Archiv | ◐ `Decision:`-Zeilen, aufbewahrte Pläne |
| **Was an die Umsetzung übergeben wird** | Story + FR-Referenzen | Change mit Proposal, Deltas, Design und Tasks | Story-Plan-Datei |
| **Testbare Szenarien, im Test referenziert** | ✅ Gherkin + Marker im Test | ◐ WHEN/THEN, ohne Verknüpfung zum Test | ◐ „woran erkennbar erfüllt“ |
| **Einheitliche Fachsprache** | ✅ Glossar je Subdomain | ❌ | ❌ |
| **Fachliche Einordnung jeder Anforderung** (bestimmt Baustein und Testebene) | ✅ FR-Typ | ❌ | ❌ |
| **Widersprüche zum Bestand erkannt** | ✅ sechs Prüffälle | ◐ nur Konflikte beim Merge (Format) | ◐ PRD-Update zeigt Konflikte mit früheren Entscheidungen |
| **Bestandsdaten fachlich geklärt** | ✅ FR vom Typ Data Migration | ◐ technisch im Design (Vermutung) | ❌ |
| **Interview** | ✅ Entscheidungsbaum, Empfehlung je Frage | ◐ Explore optional, danach Entwurf | ✅ Coaching je Abschnitt / Fast mit Annahmen |
| **Offene Punkte nachverfolgt** | ✅ `@open` + Folgerunden | ❌ | ✅ Assumption- und Open-question-Zeilen |
| **Formatsicherheit** | ◐ Templates; Validator geplant ([Refactoring 001](../refactorings/archive/001-planned-frs-and-story-housekeeping.md)) | ✅ CLI-Validierung | ◐ Prüfung durch LLM |
| **Einstieg in ein bestehendes System** | ✅ `problem-init` | ◐ Specs wachsen mit den Changes | ◐ nur Agenten-Kontext (`AGENTS.md`) |

## Quellen

- Problem Definition: die Skills unter [skills/](../skills/).
- OpenSpec: [README](https://github.com/Fission-AI/OpenSpec), [CLI-Referenz](https://openspec.dev/docs/cli).
- BMAD: [Requirements](https://docs.bmad-method.org/plan/define-requirements-and-a-specification/),
  [Stories](https://docs.bmad-method.org/plan/break-work-into-stories-and-track-it/),
  [Bestehende Codebasen](https://docs.bmad-method.org/existing-codebases/start-in-an-existing-codebase/).
