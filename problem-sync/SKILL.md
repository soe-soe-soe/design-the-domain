---
name: problem-sync
description: Updates the problem space after an answered round of /problem-definition – stories, functional requirements, domain map – and reports what changed. Use as a subagent after every answered grill round.
---

# Problem-Sync

You bring the problem space under `domain-model/problem-space/` up to date with the decisions
of one grill round, by running its writers in order. You write nothing yourself; the writers
do. What is still open the writers mark in the stories and FRs (`@open`, `## Open`);
`/problem-definition` reads it there.

## Steps

1. **Stories.** Run the skill `story-writer` with the input: the answers of the last round and
   the idea that started the session. Its report lists the new and continued stories.

2. **Functional requirements.** Run the skill `fr-writer` with the stories from that report.
   Its report lists the changed FRs and additions to the domain map.

You are done when both writers have reported.

## Report

Your last message joins both reports, exactly in this form:

```
Stories:
- US-0042: Problemsignale in der Projektübersicht (new, draft)
FRs:
- FR-fristen-002: Zählung der Problemsignale (S3 new)
- FR-fristen-001: Überfälligkeit einer Frist (S1 open)
Domain map: unchanged
```
