---
name: run-dev-servers
description: Startet Backend (FastAPI, Port 8000) und Frontend (Vite, Port 3000) für lokale Entwicklung. Nutzen, wenn der Nutzer "starte frontend/backend", "starte den Server", "localhost:3000 geht nicht" o.ä. sagt.
---

# Dev-Server starten

Backend und Frontend laufen unabhängig voneinander und müssen einzeln gestartet werden.

## Vorher prüfen

Vor dem Start immer prüfen, ob die Ports schon belegt sind (z.B. von einer vorherigen Session):

```bash
lsof -i :8000 -sTCP:LISTEN -P   # Backend
lsof -i :3000 -sTCP:LISTEN -P   # Frontend
```

Ist ein Port bereits belegt, läuft der jeweilige Server vermutlich schon — nicht erneut starten, sondern mit `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:<port>` verifizieren, dass er antwortet.

## Backend starten (FastAPI, Port 8000, Hot-Reload)

```bash
cd backend && source venv/bin/activate && nohup python main.py > /tmp/backend-dev.log 2>&1 &
disown
```

Als `run_in_background`-Bash-Aufruf ausführen. Danach kurz warten und `/tmp/backend-dev.log` prüfen — bei `ERROR: [Errno 48] Address already in use` läuft bereits eine Instanz, das ist kein Fehlschlag.

## Frontend starten (Vite, Port 3000)

```bash
cd frontend && nohup npm start > /tmp/frontend-dev.log 2>&1 &
disown
```

Ebenfalls als `run_in_background`-Bash-Aufruf. Log zeigt bei Erfolg `VITE vX.X.X ready in ... ms` und `Local: http://localhost:3000/`.

## Smoke-Test

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/docs
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/
```

Beide sollten `200` liefern.
