# Spike: OpenCode V2 (Refactoring 010)

Datum: 2026-11-23 · Modell: `openrouter/anthropic/claude-sonnet-4.6` (Haiku 4.5 für Q5) ·
OpenCode installiert 1.15.10, Q3–Q5 zusätzlich mit 1.19.6 (latest, per npm in Scratch) wiederholt ·
Claude Code (`claude -p`, haiku) für Symlinks. Nichts am Plugin geändert; Wegwerf-Projekte im Session-Scratchpad.

Hinweis „V2": 1.15.10 enthält `opencode debug v2` (V2-Katalog), 1.x ist die aktuelle Linie (`latest` 1.19.6, Tag `tui-v2`
existiert). Ich habe keine Version gefunden, die sich eindeutig „V2" nennt; Ergebnisse gelten für 1.15.10/1.19.6.

Konfidenz: [Sicher] = ausprobiert · [Wahrscheinlich] · [Vermutung]

## 1. Headless + lesbarer Trace — ja
`opencode run --format json -m <provider/model> [--command <name>] "<args>" < /dev/null` liefert JSON-Zeilen
(`step_start`, `tool_use`, `text`, `step_finish`). Jedes `tool_use` enthält `tool`, `state.input`, `state.output`,
`state.time`; Subagenten stehen als `task`-Aufruf mit `sessionId`. Zusätzlich `opencode export <sessionID>`. [Sicher]
Stolperstein: ohne `< /dev/null` hing der erste Lauf ohne Ausgabe (stdin offen); nach Umleitung lief alles. [Wahrscheinlich, Ursache nicht isoliert]
Ein Runner braucht außerdem ein Timeout (macOS hat kein `timeout`).

## 2. Command lädt Skill und reicht `$ARGUMENTS` durch — ja
`.opencode/commands/probe.md` mit „Load the skill … with the skill tool … Arguments: $ARGUMENTS", Aufruf
`--command probe "alpha beta"`: Trace zeigt `tool_use skill {name: probe}`, danach lief das Skript mit
`"alpha beta"`. Command und Skill gleichen Namens (`probe`) kollidieren nicht. [Sicher] (nur 1.15.10 getestet)

## 3. Skill-IDs mit Ordnerpräfix — nein, Annahme falsch
- Die ID ist das Frontmatter-`name`, nicht der Pfad. `design-the-domain/grilling` → „Skill not found";
  `grilling` und `other-name` (Ordner `odd/`, `name: other-name`) laden. `opencode debug skill` listet nach `name`. [Sicher, 1.15.10 + 1.19.6]
- Gleiche `name` aus zwei Ordnern: genau einer gewinnt, der andere verschwindet; Hinweis nur im Log
  (`level=WARN message="duplicate skill name" name=grilling existing=… duplicate=…`, sichtbar mit `--print-logs --log-level DEBUG`).
  Welcher gewinnt, war nicht stabil (Listing zeigte `design-the-domain/`, Laden lieferte `mattpocock/`). [Sicher]
- Folge: Eindeutigkeit nur über ein eigenes `name:` im OpenCode-Build (z. B. `ddd-grilling`); Ordnerpräfix hilft nicht.

## 4. Parallele Subagenten — ja, Ergebnis kommt synchron zurück
Agent `.opencode/agents/reporter.md` (`mode: subagent`), zwei `task`-Aufrufe in einer Nachricht: Startzeiten
…21.978 und …22.728 ms, Aufruf A lief noch → überlappend. Jeder `task`-Aufruf liefert als Tool-Ergebnis
`<task id="ses_…" state="completed"><task_result>…letzte Nachricht des Subagenten…</task_result></task>`;
der Aufrufer wartet also und bekommt den Bericht als Ergebnis (kein Polling nötig). [Sicher]
Beobachtung: das Modell hat den Prompt von A umgeschrieben (Skript nicht ausgeführt) — Prompt-Treue ist Modellsache. Tool heißt `task` (nicht `subagent`). [Sicher]

## 5. Basisverzeichnis und Symlinks
- Skill-Load liefert „Base directory for this skill: <abs>" und „Relative paths … are relative to this base directory".
  `python3 <base>/scripts/hello.py` aus dem Projektroot lief; ebenso `python3 scripts/…` mit `workdir=<base>`. [Sicher]
  `<skill_files>` ist „sampled", bei Symlink-Unterordnern leer — harmlos.
- Symlink als Skill-Ordner und Symlink-Unterordner (`scripts -> ../../shared/scripts`) funktionieren in OpenCode
  (`.opencode/skills/`) und Claude Code (`.claude/skills/`, Projekt-Ebene). [Sicher]
  Nicht geprüft: Symlinks in einem per Marketplace installierten Claude-Plugin (Cache-Kopie). [Vermutung: werden dort nicht zuverlässig aufgelöst → Build kopiert besser]
- Claude Code liefert ebenfalls „Base directory for this skill: …".

## 6. `npx skills add … -a opencode` — ja, vollständig
Lokales Git-Repo mit `skills/<ordner>/{SKILL.md,assets/,scripts/,references/}`, `npx skills@latest add <repo> -a opencode -y`:
Ziel `./.agents/skills/<name>/` (Name = Frontmatter-`name`, nicht Ordnername), alle Unterordner kopiert („copied"),
zusätzlich `skills-lock.json`. OpenCode findet den Skill dort (`debug skill`). [Sicher] (lokale Quelle; GitHub-Quelle nicht getestet [Wahrscheinlich gleich])

## Empfehlung
Der Zuschnitt (ein Kern, Adapter je Harness, selbstständige Skill-Ordner mit kopierten Assets/Scripts, relative Pfade,
Command-Wrapper) hält. Anpassen:
1. **Eindeutige IDs über `name:`**, nicht über Ordnerpräfix; Querverweise im Text nennen diese `name`. Im Build prüfen, dass kein
   `name` doppelt vorkommt (auch gegen bekannte fremde Skills wie Matt Pocock) — OpenCode meldet Kollisionen nur im Log.
2. **Slash-Namen über Command-Wrapper** (`.opencode/commands/<name>.md` → Skill laden + `$ARGUMENTS`), Skill darf gleich heißen.
3. **Keine Symlinks als Auslieferung**, Build kopiert (Symlinks gehen im Projekt, im Plugin-Cache ungeprüft).
4. **`npx skills` taugt für die Skill-Ordner** (Ziel `.agents/skills/`), Commands/Agents brauchen weiter eigenen Installationsweg.
5. **Eval-Runner**: `opencode run --format json … < /dev/null` + Timeout, Trace aus `tool_use`-Zeilen (`skill`, `task`, `bash`).
6. Offen/ungeprüft: Frage-Tool (`question`) headless, Agent-Modell je `provider/model`, Verhalten bei Rechte-Prompts in `run`.
