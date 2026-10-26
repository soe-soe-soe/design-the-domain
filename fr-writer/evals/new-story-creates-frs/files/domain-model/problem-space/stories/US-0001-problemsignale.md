# US-0001: Projektübersicht zeigt je Projekt die Zahl der Problemsignale

Status: ready · Topic: Problemsignale in der Projektübersicht · Date: 2026-10-25

Als Projektleitung möchte ich in der Projektübersicht je Projekt die Zahl der Problemsignale sehen.

## Why

Projektleitungen übersehen heute überfällige Fristen, weil sie nur im Projekt selbst sichtbar
sind. Die Projektübersicht zählt deshalb je Projekt die Problemsignale, damit Handlungsbedarf
auffällt, ohne jedes Projekt zu öffnen.

## Content

Die Projektübersicht zeigt an jedem Projekt die Zahl seiner Problemsignale. Ein Problemsignal
ist eine überfällige Frist oder eine Frist mit Problem. Überfällig ist eine Frist, deren
Fälligkeit heute oder früher liegt; eine Frist ohne Fälligkeit ist nie überfällig. Eine
überfällige Frist mit Problem zählt zweimal, einmal als überfällig und einmal als Problem.
Erledigte Fristen zählen nie.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Problemsignale in der Projektübersicht

  Grundlage:
    Angenommen heute ist der 25.10.2026
    Und das Projekt „Windpark Nordheide“ hat keine weiteren Fristen als die genannten

  Szenariogrundriss: AC1 – Eine offene Frist ist ab dem Fälligkeitstag überfällig und zählt als Problemsignal
    Angenommen das Projekt „Windpark Nordheide“ hat eine offene Frist ohne Problem, fällig am <fällig>
    Wenn die Projektübersicht angezeigt wird
    Dann zeigt sie bei „Windpark Nordheide“ <anzahl> Problemsignale

    Beispiele:
      | fällig     | anzahl |
      | 24.10.2026 | 1      |
      | 25.10.2026 | 1      |
      | 26.10.2026 | 0      |

  Szenario: AC2 – Eine Frist ohne Fälligkeit ist nie überfällig
    Angenommen das Projekt „Windpark Nordheide“ hat eine offene Frist ohne Fälligkeit und ohne Problem
    Wenn die Projektübersicht angezeigt wird
    Dann zeigt sie bei „Windpark Nordheide“ 0 Problemsignale

  Szenario: AC3 – Eine nicht überfällige Frist mit Problem zählt als ein Problemsignal
    Angenommen das Projekt „Windpark Nordheide“ hat eine offene Frist mit Problem, fällig am 15.11.2026
    Wenn die Projektübersicht angezeigt wird
    Dann zeigt sie bei „Windpark Nordheide“ 1 Problemsignal

  Szenario: AC4 – Eine überfällige Frist mit Problem zählt einmal als überfällig und einmal als Problem
    Angenommen das Projekt „Windpark Nordheide“ hat eine offene Frist mit Problem, fällig am 20.10.2026
    Wenn die Projektübersicht angezeigt wird
    Dann zeigt sie bei „Windpark Nordheide“ 2 Problemsignale

  Szenariogrundriss: AC5 – Eine erledigte Frist zählt nie als Problemsignal
    Angenommen das Projekt „Windpark Nordheide“ hat eine erledigte Frist <problem>, fällig am <fällig>
    Wenn die Projektübersicht angezeigt wird
    Dann zeigt sie bei „Windpark Nordheide“ 0 Problemsignale

    Beispiele:
      | fällig     | problem      |
      | 20.10.2026 | ohne Problem |
      | 15.11.2026 | mit Problem  |
      | 20.10.2026 | mit Problem  |

  Szenario: AC6 – Die Problemsignale werden je Projekt gezählt
    Angenommen das Projekt „Windpark Nordheide“ hat eine offene Frist ohne Problem, fällig am 20.10.2026
    Und das Projekt „Solarpark Elbaue“ hat eine offene Frist mit Problem, fällig am 20.10.2026
    Und das Projekt „Solarpark Elbaue“ hat eine offene Frist ohne Problem, fällig am 23.10.2026
    Und das Projekt „Repowering Geestland“ hat keine Fristen
    Wenn die Projektübersicht angezeigt wird
    Dann zeigt sie bei „Windpark Nordheide“ 1 Problemsignal
    Und bei „Solarpark Elbaue“ 3 Problemsignale
    Und bei „Repowering Geestland“ 0 Problemsignale
```
