---
type: regex
target: trace
match: not_contains
pattern: '\\n## History'
weight: 1
---

No file the run wrote has a '## History' section (the trace escapes line breaks as \n).
