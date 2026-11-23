---
type: regex
target: trace
match: contains
pattern: '\*\*S\d+\*\* \(functional-requirement\): [^\\]*\? – Recommendation: Ja'
weight: 1
---

The open point in the FR is a question (ends with ?) whose Recommendation starts with "Ja", so "ja" accepts it.
