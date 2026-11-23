---
type: regex
target: last_message
match: contains
pattern: '^Stories:\n- US-\d{4}: [^\n]+ \(new, draft\)\s*$'
weight: 1
---

The final message is only the report: `Stories:` and one line `- US-NNNN: <title> (new, draft)`, nothing before or after it.
