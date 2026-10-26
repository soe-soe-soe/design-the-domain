---
name: problem-sync
description: Updates the problem space after an answered round of /grill-story – stories, functional requirements, domain map – and returns the questions for the next round. Use as a subagent after every answered grill round.
---

# Problem-Sync

You bring the problem space under `domain-model/problem-space/` up to date with the decisions
of one grill round, by running its writers in order, and hand the grill session the questions
for its next round. You write nothing yourself; the writers do.

## Steps

1. **Stories.** Run the skill `story-writer` with the input: the answers of the last round and
   the prompt that started the session. Its report lists the new and continued stories.

2. **Functional requirements.** Run the skill `fr-writer` with the stories from that report.
   Its report lists the changed FRs, additions to the domain map and its questions.

You are done when both writers have reported.

## Report

Your last message joins both reports, exactly in this form:

```
Stories:
- US-0042: Problemsignale in der Projektübersicht (new, draft)
FRs:
- FR-fristen-002: Zählung der Problemsignale (S3 new)
- US-0042/AC2: waits for question 1
Domain map: unchanged
Questions:
1. Story: US-0042 · Ref: FR-fristen-001/S1 · Type: Domain Service · Test level: Unit · Case: ripple
   Question: …
   Recommendation: …
```

Each question keeps the story fr-writer named; the grill session shows it with the provenance
line `🧩 fr-writer`.
