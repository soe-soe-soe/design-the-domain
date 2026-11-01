# US-0008: Frist ist erst ab dem Tag nach ihrer Fälligkeit überfällig

Status: ready · Topic: Überfälligkeit neu definiert · createdAt: 2026-10-25
Supersedes in part: US-0007 (AC1)

Als Projektleitung möchte ich eine Frist erst dann als überfällig sehen, wenn ihr Fälligkeitstag vorbei ist.

## Why

Am Fälligkeitstag kann eine Frist noch fristgerecht erledigt werden. Das Signal kam bisher einen
Tag zu früh und wurde deshalb ignoriert.

## Content

Eine Frist gilt erst ab dem Tag nach ihrem Fälligkeitsdatum als überfällig, nicht mehr schon am
Fälligkeitstag.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Frist ist erst ab dem Tag nach ihrer Fälligkeit überfällig

  Szenariogrundriss: AC1 – Überfällig erst ab dem Tag nach dem Fälligkeitsdatum
    Angenommen eine Frist ist fällig am <fällig>
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist <ergebnis>

    Beispiele:
      | fällig     | ergebnis                  |
      | 15.10.2026 | als überfällig            |
      | 16.10.2026 | nicht als überfällig      |
      | 17.10.2026 | nicht als überfällig      |

```
