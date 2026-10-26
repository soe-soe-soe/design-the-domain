# US-0008: Frist ist erst ab dem Tag nach ihrer Fälligkeit überfällig

Status: bereit · Thema: Überfälligkeit neu definiert · Datum: 2026-10-25
Ersetzt teilweise: US-0007 (AK1)

Als Projektleitung möchte ich eine Frist erst dann als überfällig sehen, wenn ihr Fälligkeitstag vorbei ist.

## Warum

Am Fälligkeitstag kann eine Frist noch fristgerecht erledigt werden. Das Signal kam bisher einen
Tag zu früh und wurde deshalb ignoriert.

## Inhalt

Eine Frist gilt erst ab dem Tag nach ihrem Fälligkeitsdatum als überfällig, nicht mehr schon am
Fälligkeitstag.

## Akzeptanzkriterien

```gherkin
# language: de
Funktionalität: Frist ist erst ab dem Tag nach ihrer Fälligkeit überfällig

  Szenariogrundriss: AK1 – Überfällig erst ab dem Tag nach dem Fälligkeitsdatum
    Angenommen eine Frist ist fällig am <fällig>
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist <ergebnis>

    Beispiele:
      | fällig     | ergebnis                  |
      | 15.10.2026 | als überfällig            |
      | 16.10.2026 | nicht als überfällig      |
      | 17.10.2026 | nicht als überfällig      |

```
