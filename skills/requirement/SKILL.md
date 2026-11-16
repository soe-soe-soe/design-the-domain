---
name: requirement
description: Grills a requirement into ready stories – grilling and domain-modeling for the interview, after every round a subagent writes stories and FRs with problem-space-story and problem-space-fr, their open points asked in the following rounds.
disable-model-invocation: true
---

# Requirement

You interview the user about a requirement until its problem space is settled: stories with
acceptance criteria, FR scenarios, glossary terms. The craft comes from the skills
`define-the-domain:grilling` (the interview) and `define-the-domain:domain-modeling` (glossary and ADRs); this skill runs the rounds
the project's way, lets the writers update the problem space in between and alone decides which
questions are asked.

**Project config.** Read `.claude/pts.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, stop and point the user to the
template `${CLAUDE_PLUGIN_ROOT}/assets/config.md`.

Called as `/define-the-domain:requirement <requirement>`. Everything you say to the user is in
`‹problem-space-language›`.

## Open points

The writers (`define-the-domain:problem-space-story`, `define-the-domain:problem-space-fr`) ask nothing; they mark what is open where it belongs. A
scenario or AC with an open point carries the tag `@open`, and the story or FR lists the point
under `## Open`, in the format of the term "Open point" in
`‹methodology-glossary›`: reference, source skill, question, recommendation,
fields. The **session's open points** are those in the stories and FRs the session created or
changed (the ones the writers' reports name).

## Output format

Read `${CLAUDE_PLUGIN_ROOT}/assets/output-format.md` before your first message and follow it: the context block at
the start of a message after new reads, the artifact icons in every reference. Artifacts the
ground subagent read count as read by you.

## Writing the problem space

After every answered round, one subagent brings `‹problem-space›/` up to date with
the round's decisions; it runs in its own context so the interview stays lean. Start it with the
model `‹model-writer›` (leave the model out for `inherit`). The writers put stories into
`‹requirements›/planned/` and FR changes into the planned files next to the active FRs; an active
FR stays untouched until its story is done. Its brief:

> Call the Skill tool with `define-the-domain:problem-space-story` with the answers of this round: <answers> and the requirement that
> started the session: <requirement>. Then call it with `define-the-domain:problem-space-fr` for the stories its
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

## Steps

1. **Read the ground** in one subagent with the model `‹model-ground›`, so the files stay out
   of the interview. Its brief:

   > Read `‹glossary-map›`, the glossaries it names for the subdomains this requirement touches:
   > <requirement>, `‹domain-map›`, the stories under
   > `‹requirements›/planned/` on the same topic, the planned FR files (`planned/` below the FR
   > folders) of the subdomains it touches, and whatever
   > else the requirement points to. Change nothing. Your last message has exactly these parts:
   > `Context:` one line per file read, in the format of `${CLAUDE_PLUGIN_ROOT}/assets/output-format.md`;
   > `State:` the current state of the topic in at most 15 lines; `Terms:` every glossary
   > term the requirement touches with its one-line description; `Drafts:` each story in
   > `planned/` on the topic with its status and open points, or `none`; `Planned:` each planned
   > FR change of another story on the topic (`FR-…/Sn – US-…, Status`), or `none`. Labels
   > English, content in `‹problem-space-language›`.

   The session may continue those stories, including their open points; a `ready` or
   `in-progress` one falls back to `draft` when it changes (its template says so). `done` and
   `cancelled` stories are final: a change to them is a new story. When a question needs more
   than the report gives, read the file yourself.

2. **Load the craft.** Call the Skill tool with `define-the-domain:grilling` and with
   `define-the-domain:domain-modeling`, and follow both. `domain-modeling` writes glossary rows into the
   subdomain glossaries under `‹glossaries›/` by `${CLAUDE_PLUGIN_ROOT}/assets/glossary.md`
   (unless `‹project-rules›` sets its own format) and a new glossary's row into `‹glossary-map›`.
   This skill decides on top of `grilling` how rounds are grouped, numbered and what each
   question carries.

3. **Run the rounds.**
   - **Rounds follow `grilling`:** each round asks its frontier, so its length depends on what is
     open, in grilling's question format (`❓ **Qn** - **<title>**: …`, then `➡️` with a
     recommendation for every question).
   - **Round 1** is grilling alone, on the requirement and what step 1 found.
   - **After every answered round** start one subagent with the brief below and wait for it.
     Then read the `## Open` sections of the stories and FRs its report names, and build the
     next round: your
     own frontier plus every open point **from an FR**. Open points **from a story** wait for the
     closing round – the grilling often settles them on the way.
   - **Closing round.** When your frontier is empty and no FR of the session has an open point
     left, ask the open points still listed in the session's stories. If none are left, go to
     step 4.
   - **Render every round with the script.** You decide the content of your own questions; the
     script `${CLAUDE_PLUGIN_ROOT}/scripts/interview-round.py` adds the open points from the files, numbers,
     groups and writes each provenance line. Write the round as JSON to a scratch file and run
     `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/interview-round.py <file>`; its standard output, after the context block,
     is your message for the round – change nothing in it, add nothing between the questions. The keys (see the script's header):
     `start` – the next question number: Q1 in round 1, afterwards the number the previous run
     printed on standard error (`next question number: N`), so numbering runs across the whole session;
     `group` – `false` for round 1, `true` from round 2 on (headings per story, questions without
     a story last under `crosscutting` – the word in `‹problem-space-language›`, e.g. "Cross-cutting"); `closing` – `true` for the closing round; `stories` – the session's stories;
     `deferred` – the open points the user deferred (`FR-deadlines-013/S2`, `US-0051/AC2`);
     `questions` – your own frontier: `title`, `body` (options included), `recommendation`, and
     where they apply `story`, `ref` (the artifact the question rests on, never a glossary term),
     `type` (FR type), `source` (a skill other than `grilling` that raised it) and `same_as` (the
     open point your frontier already held before you read it – the script asks it once).
     Never write an open point of the writers into `questions` yourself: the script reads them.
   - **Provenance line** (written by the script, for reading it): 🗣️ who raised the question –
     `‹user›` for an open point, `grilling` for your own, `‹user›/grilling` for a shared one;
     🧩 the skill; the referenced artifact with the icon of its type; 📐 the FR type.
   - **Parallel changes.** A `Parallel` entry of the writers (or a `Planned` entry of step 1 the
     session's changes touch) means another story changes the same scenario. Ask it in the next
     round under its story, with these options and your recommendation:
     **combine** – the change goes into one of the two stories;
     **sequence** – this story waits for the other; it is closed against the other's result, so
     a story that closes first makes the later one fail `requirements.py check` and come back here;
     **take out** – the overlapping part becomes a story of its own and stays `draft` with the
     point deferred, so this session can close without it.
     Pass it in `questions` with `source` `problem-space-fr`, `ref` the scenario and its `story`.
   - **Deferring.** The user may defer an open point instead of answering it. It stays in its
     story or FR, and you do not ask it again in this session.
   - **Cancelling.** If the user drops a story of the session altogether, run
     `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/requirements.py cancel US-0042`; it removes the
     story's planned FR changes and moves it to `‹requirements›/cancelled/`. With a ticket
     system, sync the story by `${CLAUDE_PLUGIN_ROOT}/assets/ticket.md`.

4. **Close.** The session is done when your frontier is empty, every open point of the session
   is answered or deferred, and the user confirms the shared understanding (as `grilling`
   requires). Then, for every story of the session:
   - **Validate draft → ready** by the status flow in the comment of
     `${CLAUDE_PLUGIN_ROOT}/assets/story.md`: no entry under
     `## Open`, no AC tagged `@open`, every AC under `## Functional requirements`, and
     `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/requirements.py check US-0042` exits 0.
   - If it holds, edit its header line to `Status: ready` – the file is the record, saying it is
     not enough. Otherwise it stays `draft`; a failing check you name with its output.
   - **Ticket system.** Unless `‹ticket-system›` is `none`: sync every story of the session – draft
     ones too – by `${CLAUDE_PLUGIN_ROOT}/assets/ticket.md`, and write a new ticket's ID into
     the story header as `External: <ID>`.

   Only then tell the user which stories are `ready` and which are still `draft` with their
   deferred points, and name the next step of the feature workflow in `‹project-rules›`.

You are done when every decision of the session stands in a story or an FR, every term the
stories use is in a glossary, every open point is answered or deferred, the user has
confirmed, every story that passes the validation says `Status: ready` in its file, and – with
a ticket system – every story of the session has its `External` ID.
