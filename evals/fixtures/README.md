# Eval fixtures

`project/` is an invented sample project for the `requirement` evals: software for project developers that keeps
deadlines (Fristen) and permit procedures (Genehmigung). German problem space, English solution
space, as `config.md` says. The `place-files.sh` of a case copies `project/` into the run
directory, then `config.md` and `methodology.md`, then the case's own `files/`.

Facts the graders rely on:

- `project/domain-model/glossaries/fristen.md` holds Frist, Manuelle Frist, Abgeleitete Frist, Fälligkeit,
  Verantwortlicher, Projekttermin, Persönlicher Termin, Zieltermin; "Termin" alone is an Avoid entry.
- The active FR-fristen-009 S6 was last changed by US-0042; a planned change with `@base-US-0030`
  fails `requirements.py check`.
- No story of the fixture is open: `requirements/planned/` is empty; the cases bring their own.
