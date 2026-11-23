---
name: domain-grilling
description: The interview of design-the-domain – a design tree asked in rounds of numbered questions with recommendations, rendered by scripts/interview-round.py, with open points from the stories and FRs, deferring and a closing round. Use from /design-the-domain:domain-interview and /design-the-domain:domain-init; not for grilling a plan outside a project with domain-model/config.md.
---

> Based on [mattpocock/skills](https://github.com/mattpocock/skills) `skills/productivity/grilling` (MIT, © 2026 Matt Pocock),
> commit `4ae2317`. The first part is upstream unchanged; the section *Rounds in this project* is ours (numbering,
> grouping, open points, deferring, closing round, rendering by script). See `THIRD_PARTY_LICENSES.md` and
> `docs/upstream.md` in the source repository.

# Domain-Grilling

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent with a fresh context window to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Rounds in this project

The skill that calls you (`domain-interview`, `domain-init`) decides what the interview is about
and what happens between rounds; you decide how it is asked. Everything you say to the user is in
`‹problem-space-language›` of `domain-model/config.md`.

- **Render every round with the script.** You decide the content of your own questions; the script
  `${CLAUDE_PLUGIN_ROOT}/scripts/interview-round.py` adds the open points from the files, numbers,
  groups and puts the artifact a question rests on after its title (`❓ **Q3** - **<title>**
  (📋 FR-fristen-013/S2): …`). Write the round as JSON to a scratch file and run
  `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/interview-round.py <file>` from the project root; its
  standard output is your message for the round – change nothing in it, add nothing between the
  questions. To change a question, change the JSON and run the script again. It needs the
  project config; before it exists (`domain-init`, step 1) you write the format above by hand.
- **The keys** (see the script's header): `start` – the next question number: Q1 in the first
  round, afterwards the number the previous run printed on standard error (`next question number:
  N`), so numbering runs across the whole session; `group` – `false` for the first round, `true`
  from round 2 on (headings per story, questions without a story last under `crosscutting` – the
  word in `‹problem-space-language›`, e.g. "Cross-cutting"), or `headings` to group by another key
  (a subdomain); `closing` – `true` for the closing round; `stories` – the stories whose open
  points belong to this interview; `deferred` – the open points the user deferred; `questions` –
  your own frontier: `title`, `body` (options included), `recommendation`, and where they apply
  `story` or `group`, `ref` (the artifact the question rests on, never a glossary term) and
  `same_as` (an open point your frontier already held before you read it – the script asks it once).
- **Open points.** The writers (`design-the-domain:user-story`, `design-the-domain:functional-requirement`)
  ask nothing; they mark what is open where it belongs: the tag `@open` on the scenario or AC, and an
  entry under `## Open` of the story or FR in the format of the term "Open point" in
  `‹methodology-glossary›`. The script reads them for the `stories` you pass: the points **from an
  FR** in every round, the points **from a story** only in the closing round – the grilling often
  settles them on the way. Never write an open point into `questions` yourself.
- **Deferring.** The user may defer an open point instead of answering it. It stays in its story or
  FR; add it to `deferred`, so it is not asked again in this session.
- **Closing round.** When your frontier is empty and no FR open point is left, run one round with
  `closing` `true` for the open points still listed in the stories. Without any, the interview is at
  its end.
- **End.** The interview is done when your frontier is empty, every open point is answered or
  deferred, and the user confirms the shared understanding (above). Then the calling skill goes on.
