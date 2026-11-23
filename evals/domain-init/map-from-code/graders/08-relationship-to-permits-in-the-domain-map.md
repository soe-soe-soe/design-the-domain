---
type: regex
target: {source: file, path: domain-model/problem-space/domain-map.md}
match: contains
pattern: '\| *Fristen *\| *Genehmigung\w* *\| *[^|]*(gehör|zugeordnet|bezieh|Bezug)[^|]*\|'
weight: 1
---

The Relationships table has a row from Fristen to the permit subdomain (Genehmigung, Genehmigungen or Genehmigungsverfahren, as the subagent's report names it) saying that a deadline belongs to it.
