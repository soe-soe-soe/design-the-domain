# US-0002: Eine Frist hat eine Priorität

Status: ready · Topic: Priorität von Fristen · createdAt: 2026-11-17

Als Projektleitung möchte ich einer Frist eine Priorität geben, damit dringende Fristen auffallen.

## Why

Alle Fristen sehen heute gleich dringend aus. Mit einer Priorität lässt sich festhalten, welche
Fristen zuerst angegangen werden.

## Content

Eine Frist hat eine Priorität: hoch, normal oder niedrig. Eine neue Frist hat die Priorität
normal, solange keine andere gewählt ist. Die Priorität lässt sich jederzeit ändern. Bereits
vorhandene Fristen erhalten die Priorität normal.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Priorität einer Frist

  Szenario: AC1 – Eine neue Frist hat die Priorität normal
    Wenn eine Frist ohne Angabe einer Priorität angelegt wird
    Dann hat die Frist die Priorität normal

  Szenariogrundriss: AC2 – Die Priorität einer Frist lässt sich ändern
    Angenommen eine Frist hat die Priorität normal
    Wenn die Priorität auf <priorität> gesetzt wird
    Dann hat die Frist die Priorität <priorität>

    Beispiele:
      | priorität |
      | hoch      |
      | niedrig   |

  Szenario: AC3 – Bereits vorhandene Fristen haben die Priorität normal
    Angenommen eine Frist wurde vor der Einführung der Priorität angelegt
    Wenn die Frist angezeigt wird
    Dann hat sie die Priorität normal
```
