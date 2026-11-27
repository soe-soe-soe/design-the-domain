---
name: domain-interview
description: Interviews the user about a requirement until its problem space is settled – reads the ground, runs domain-grilling and glossary, lets a subagent write stories and FRs after every round and asks what the writers find, then sets the session's stories ready through story-workflow.
disable-model-invocation: true
---

# Domain-Interview

Paths `assets/…` and `scripts/…` are relative to this skill's base directory (named when the skill loads; `<base directory>` below). Scripts run from the project root.

You interview the user about a requirement until its problem space is settled: stories with
acceptance criteria, FR scenarios, glossary terms. You compose three skills, as a grill with docs:
`domain-grilling` (how the interview is asked), `glossary`
(the language, scenarios, the check against code) and, after every round, the writers
`user-story` and `functional-requirement`. What this skill adds
is the ground before the first round, the writing between the rounds and the close.

**Project config.** Read `domain-model/config.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, or when a key you need holds no
value or only a placeholder (`<name>`), stop and tell the user, in their language and nothing else:
fill in `domain-model/config.md` first, `/domain-init` does it with them. Guess no
value.

Called as `/domain-interview <requirement>`. Everything you say to the user is in
`‹problem-space-language›`.

**Output format.** Read `assets/output-format.md` before your first message
and follow it: the context block at the start of a message after new reads, the artifact icons in
every reference. Artifacts the ground subagent read count as read by you.

## Steps

1. **Read the ground** in one subagent with the model `‹model-ground›` (leave the model out for
   `inherit`), so the files stay out of the interview. Its brief:

   > Read `‹domain-map›`, the glossaries it names and the subdomain maps it links for the
   > subdomains this requirement touches: <requirement>, the stories under
   > `‹requirements›/planned/` on the same topic, the planned FR files (`planned/` below the FR
   > folders) of the subdomains it touches, and whatever
   > else the requirement points to. Change nothing. Your last message has exactly these parts:
   > `Context:` one line per file read, in the format of `<base directory>/assets/output-format.md` (give the subagent that path in full);
   > `State:` the current state of the topic in at most 15 lines; `Terms:` every glossary
   > term the requirement touches with its one-line description and its `Avoid:` words;
   > `Drafts:` each story in `planned/` on the topic with its status and open points, or `none`;
   > `Planned:` each planned FR change of another story on the topic (`FR-…/Sn – US-…, Status`),
   > or `none`. Labels English, content in `‹problem-space-language›`.

   This is the **ground** every skill reads before it changes the problem space; other skills
   refer to it instead of listing the files again.

   The session may continue those stories, including their open points; a `ready` or
   `in-progress` one falls back to `draft` when it changes (its template says so). `done` and
   `cancelled` stories are final: a change to them is a new story. When a question needs more
   than the report gives, read the file yourself.
   Your questions use the terms of `Terms:` and never one of their `Avoid:` words on its own.

2. **Load the craft.** Call the Skill tool with `domain-grilling` and with
   `glossary`, and follow both. The first round is grilling alone, on the
   requirement and what step 1 found, with `group` `false`; from round 2 on, the session's stories
   go into `stories`.

3. **After every answered round** start one subagent with the model `‹model-writer›` (leave the
   model out for `inherit`) and wait for it; it brings `‹problem-space›/` up to date in its own
   context, so the interview stays lean. The writers put stories into `‹requirements›/planned/` and
   FR changes into the planned files next to the active FRs; an active FR stays untouched until its
   story is done. Its brief:

   > Call the Skill tool with `user-story` with the answers of this round: <answers> and the requirement that
   > started the session: <requirement>. Then call it with `functional-requirement` for the stories its
   > report names. Write nothing yourself; the writers do. Your last message joins both reports,
   > exactly in this form:
   >
   > ```
   > Stories:
   > - US-0042: Problem signals in the project overview (new, draft)
   > FRs:
   > - FR-deadlines-002: Counting problem signals (S3 new)
   > - FR-deadlines-001: Overdue deadline (S1 open)
   > Parallel:
   > - FR-deadlines-001/S1: also changed by US-0039 (ready)
   > Domain map: unchanged
   > ```
   >
   > `Parallel` only when the FR writer reports one.

   The stories its report names are the session's stories; the next round asks their open points
   (`domain-grilling` reads them).

   - **Parallel changes.** A `Parallel` entry (or a `Planned` entry of step 1 the session's
     changes touch) means another story changes the same scenario. Ask it in the next round under
     its story, with `ref` the scenario, and these options and your recommendation:
     **combine** – the change goes into one of the two stories;
     **sequence** – this story waits for the other; it is closed against the other's result, so
     a story that closes first makes the later one fail `requirements.py check` and come back here;
     **take out** – the overlapping part becomes a story of its own and stays `draft` with the
     point deferred, so this session can close without it.
   - **Cancelling.** If the user drops a story of the session altogether, call the Skill tool
     with `story-workflow US-0042 cancel`; it removes the story's planned FR
     changes, moves it to `‹requirements›/cancelled/` and syncs its ticket.

4. **Close** once the interview is at its end (`domain-grilling`, section End): for every story of
   the session call the Skill tool with `story-workflow US-0042 ready`. It
   validates the story, sets `ready` where it holds, leaves it `draft` otherwise and syncs its
   ticket either way. Then tell the user which stories are `ready` and which are still `draft`
   with their deferred points or failed checks – a deferred point by its reference and a short
   title (`📘 US-0042/AC2 <title>`), never asked again as a question – and name the next step where the project's
   instructions describe a feature workflow (look in `CLAUDE.md` or `AGENTS.md` at the project root).

You are done when every decision of the session stands in a story or an FR, every term the
stories use is in a glossary, every open point is answered or deferred, the user has confirmed,
and `story-workflow ready` has run for every story of the session.

## Harness notes (OpenCode)

- Subagents: start them with the `task` tool and the `subagent_type` named below. Their model comes from the agent file, not from a parameter: if `.opencode/agents/<subagent_type>.md` does not exist yet, or `domain-model/config.md` changed its `model-…` value, run `python3 <base directory>/scripts/opencode-agents.py` from the project root first (restart OpenCode after a changed model). A `model-…` value that is not `provider/model` means the session's model.
- `domain-ground` for the ground (`model-ground`), `domain-writer` for the writers (`model-writer`).
