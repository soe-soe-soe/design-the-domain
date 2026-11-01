<!--
Index of the glossaries – ‹glossary-map›, in the project root: Pocock's `domain-modeling`
(‹skill-domain-modeling›) looks for GLOSSARY-MAP.md only there. Links are relative to the root.
A glossary-map format in ‹project-rules› overrides this template.

- One row per glossary file, the methodology glossary first. Whoever creates a glossary
  (problem-init, the grilling of problem-definition) adds its row in the same change.
- Subdomain and its type stand in ‹domain-map›; this map only says where to look up a term.
This comment is not copied into the map.
-->
# Glossary Map

Wo ein Begriff steht: je Subdomäne ein Glossar, die Methodenbegriffe in einem eigenen.

| Glossary | Subdomain | Covers |
|---|---|---|
| [_methodology.md](domain-model/glossaries/_methodology.md) | – | Begriffe der Methode: Story, FR, Szenario, Open point |
| [<datei>.md](domain-model/glossaries/<datei>.md) | <Subdomäne> | <Business Objects und Themen, ein Satz> |
