---
type: llm
focus: trace
weight: 1
---

Every question of round 1 in the final message ends with a provenance line that starts with `🗣️ domain-grilling   🧩 domain-grilling`, except a question about a glossary term, which may start with `🗣️ Alex   🧩 glossary` (scripts/interview-round.py writes the user as 🗣️ for a question another skill raised). Further entries after the 🧩 entry, such as the artifact the question rests on (📋 FR-…, 📘 US-…, 📄 …) or 📐 with an FR type, are allowed. Spaces between the entries do not matter.
