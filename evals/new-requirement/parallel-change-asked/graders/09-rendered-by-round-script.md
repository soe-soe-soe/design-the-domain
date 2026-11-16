---
type: llm
focus: trace
weight: 1
---

The run called scripts/round.py with a JSON description of the round (a Bash call), and every question of the round in the final message – title, body, recommendation and provenance line – appears exactly as in that call's output. Shell noise after the output (an exit code or a read-only file system message about the working directory) does not matter
