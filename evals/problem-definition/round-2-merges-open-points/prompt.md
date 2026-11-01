---
tags: [skill-creator, problem-space]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

/pts:problem-definition Requirement: Verantwortliche sollen vor Ablauf einer Frist per E-Mail erinnert werden.

Runde 1 (gestellt vom Grilling):
Q1 – Wer bekommt die Erinnerung? → Antwort: die verantwortliche Person der Frist.
Q2 – Wie lange vor der Fälligkeit? → Antwort: 7 Kalendertage, fest.
Q3 – Erledigte Fristen? → Antwort: werden nicht erinnert.
Q4 – Kann man Erinnerungen abbestellen? → Antwort: ja, je Nutzer; ob es dann eine Sammelmail gibt, weiß ich noch nicht.

Der Subagent mit den Writern ist für diese Runde bereits gelaufen (nicht erneut starten), hier sein Bericht:

```
Stories:
- US-0050: Erinnerung vor Fristablauf per E-Mail (new, draft)
- US-0051: Erinnerungen abbestellen (new, draft)
FRs:
- FR-fristen-013: Fristerinnerung per E-Mail (new, S2 open)
- FR-fristen-014: Erinnerungen abbestellen (new, S1 open)
Domain map: unchanged
```

Stell mir jetzt Runde 2.
