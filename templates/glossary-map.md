<!--
Index of the glossaries – ‹glossary-map›, by default GLOSSARY-MAP.md in the project root; `define-the-domain:domain-modeling`
and new-requirement read it from that key. Links are relative to the project root.
A glossary-map format in ‹project-rules› overrides this template.

- One row per glossary file, the methodology glossary first. Whoever creates a glossary
  (problem-init, the grilling of new-requirement) adds its row in the same change.
- Subdomain and its type stand in ‹domain-map›; this map only says where to look up a term.
Texts in ‹problem-space-language›, column headings English (methodology).
This comment is not copied into the map.
-->
# Glossary Map

<Where a term stands: one glossary per subdomain, the methodology terms in one of their own.>

| Glossary | Subdomain | Covers |
|---|---|---|
| [_methodology.md](domain-model/glossaries/_methodology.md) | – | <terms of the method: story, FR, scenario, open point> |
| [<datei>.md](domain-model/glossaries/<datei>.md) | <subdomain> | <business objects and topics, one sentence> |
