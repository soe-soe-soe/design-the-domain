---
type: regex
target: trace
flags: i
match: contains
pattern: '# FR-fristen-\d+: [^\\]*(Problemsignal|Zählung)[^\\]*\\n\\nSubdomain: fristen · Business object: [^·]+ · Type: Domain Service'
weight: 1
---

The FR about counting problem signals has the type Domain Service (not Query).
