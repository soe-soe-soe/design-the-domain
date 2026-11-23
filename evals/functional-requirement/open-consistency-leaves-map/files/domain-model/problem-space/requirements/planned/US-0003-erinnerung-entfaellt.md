# US-0003: Eine Erinnerung entfällt, wenn ihre Frist erledigt wird

Status: ready · Topic: Erinnerungen an Fristen · createdAt: 2026-11-17

Als Verantwortliche möchte ich keine Erinnerung an eine Frist bekommen, die ich schon erledigt habe.

## Why

Erinnerungen an bereits erledigte Fristen verwirren und werden irgendwann nicht mehr ernst genommen.

## Content

Zu einer Frist gibt es eine Erinnerung, die vor der Fälligkeit versendet wird. Wird die Frist
erledigt, bevor die Erinnerung versendet wurde, entfällt die Erinnerung. Eine bereits versendete
Erinnerung bleibt bestehen.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Erinnerung und erledigte Frist

  Szenario: AC1 – Eine noch nicht versendete Erinnerung entfällt, wenn die Frist erledigt wird
    Angenommen eine Frist hat eine Erinnerung, die noch nicht versendet wurde
    Wenn die Frist erledigt wird
    Dann entfällt die Erinnerung

  Szenario: AC2 – Eine bereits versendete Erinnerung bleibt bestehen
    Angenommen eine Frist hat eine Erinnerung, die schon versendet wurde
    Wenn die Frist erledigt wird
    Dann bleibt die Erinnerung bestehen
```
