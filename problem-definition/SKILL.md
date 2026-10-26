---
name: problem-definition
description: Grills a feature idea into ready stories – Pocock's grilling and domain-modeling for the interview, after every round a subagent writes stories and FRs with problem-story-writer and problem-fr-writer, their open points asked in the following rounds.
disable-model-invocation: true
---

# Problem-Definition

You interview the user about a feature until its problem space is settled: stories with
acceptance criteria, FR scenarios, glossary terms. The craft comes from Pocock's skills
`grilling` (the interview) and `domain-modeling` (glossary and ADRs); this skill runs the rounds
the project's way, lets the writers update the problem space in between and alone decides which
questions are asked.
It is the problem-space counterpart of `/story-workflow`.

Called as `/problem-definition <feature idea>`. Everything you say to the user is German.

## Open points

The writers (`problem-story-writer`, `problem-fr-writer`) ask nothing; they mark what is open where it belongs. A
scenario or AC with an open point carries the tag `@open`, and the story or FR lists the point
under `## Open`, in the format of the term "Open point" in
`domain-model/glossaries/_methodology.md`: reference, source skill, question, recommendation,
fields. The **session's open points** are those in the stories and FRs the session created or
changed (the ones the writers' reports name).

## Writing the problem space

After every answered round, one subagent brings `domain-model/problem-space/` up to date with
the round's decisions; it runs in its own context so the interview stays lean. Its brief:

> Run the skill `problem-story-writer` with the answers of this round: <answers> and the idea that
> started the session: <idea>. Then run the skill `problem-fr-writer` with the stories its
> report names. Write nothing yourself; the writers do. Your last message joins both reports,
> exactly in this form:
>
> ```
> Stories:
> - US-0042: Problemsignale in der Projektübersicht (new, draft)
> FRs:
> - FR-fristen-002: Zählung der Problemsignale (S3 new)
> - FR-fristen-001: Überfälligkeit einer Frist (S1 open)
> Domain map: unchanged
> ```

## Steps

1. **Read the ground.** `GLOSSARY-MAP.md`, the glossaries it names for the subdomains the idea
   touches, `domain-model/problem-space/domain-map.md` and the stories under
   `domain-model/problem-space/stories/` with status `draft` on the same topic: the session may
   continue them, including their open points.

2. **Load the craft.** Call the Skill tool with `mattpocock-skills:grilling` and with
   `mattpocock-skills:domain-modeling`. Follow both, with the project's rules on top: glossary
   rows go into the subdomain glossaries in the table format of `CLAUDE.md` (section
   „Fachmodell“), not into a root `GLOSSARY.md`.

3. **Run the rounds.**
   - **Rounds follow `grilling`:** each round asks its frontier, so its length depends on what is
     open, in grilling's question format (`❓ **Qn** - **<Titel>**: …`, then `➡️` with a
     recommendation for every question).
   - **Round 1** is grilling alone, on the idea and what step 1 found.
   - **After every answered round** start one subagent with the brief below and wait for it.
     Then read the `## Open` sections of the stories and FRs its report names, and build the
     next round: your
     own frontier plus every open point **from an FR**. Open points **from a story** wait for the
     closing round – the grilling often settles them on the way.
   - **Closing round.** When your frontier is empty and no FR of the session has an open point
     left, ask the open points still listed in the session's stories. If none are left, go to
     step 4.
   - **Group by story.** From round 2 on, put each question under the story it belongs to,
     `### 📘 US-0042: <Titel>`, questions without a story last under `### 🌐 Übergreifend`.
     Number the questions across the whole session: round 1 starts at Q1, every later round
     continues with the number after the last question of the previous round, across all groups.
     Only a new session starts again at Q1.
   - **Provenance line.** Every question ends, below the ➡️ recommendation, with one line whose
     entries are separated by a space; entries that do not exist yet are left out:

     🗣️ Alex/Pocock 🧩 problem-fr-writer 🏷️ FR-fristen-003/S2 📐 Domain Service

     🗣️ is `Alex` for an open point, `Pocock` for a question only your grilling frontier has,
     and `Alex/Pocock` only when your frontier already held the same question before you read
     the open points (ask it once). 🧩 names the skill that raised it: `grilling` for your own,
     the source skill of the open point for its questions, both joined with ` + ` for a shared
     one (`grilling + problem-fr-writer`). For an open point 🏷️ is its reference (`FR-fristen-002/S1`,
     `US-0042/AC2`), 📐 its field `Type`; your own questions may carry a
     🏷️ to what they refer to.
   - **Deferring.** The user may defer an open point instead of answering it. It stays in its
     story or FR, and you do not ask it again in this session.

4. **Close.** The session is done when your frontier is empty, every open point of the session
   is answered or deferred, and the user confirms the shared understanding (as `grilling`
   requires). Then edit the header line of every story file of the session without entries
   under `## Open` to `Status: ready` – the file is the record, saying it is not enough; the
   others stay `draft`. Only then tell the user which stories are `ready` and which are still
   `draft` with their deferred points, and name the next step of the feature workflow in
   `CLAUDE.md`.

You are done when every decision of the session stands in a story or an FR, every term the
stories use is in a glossary, every open point is answered or deferred, the user has
confirmed, and every story without open points says `Status: ready` in its file.
