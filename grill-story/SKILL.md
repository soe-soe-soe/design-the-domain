---
name: grill-story
description: Grills a feature idea into ready stories – Pocock's grilling and domain-modeling for the interview, problem-sync after every round for stories, FRs and their questions.
disable-model-invocation: true
---

# Grill-Story

You interview the user about a feature until its problem space is settled: stories with
acceptance criteria, FR scenarios, glossary terms. The craft comes from Pocock's skills
`grilling` (the interview) and `domain-modeling` (glossary and ADRs); this skill runs the rounds
the project's way and feeds `problem-sync` in between. It is the problem-space counterpart of
`/implement-story`.

Called as `/grill-story <feature idea>`. Everything you say to the user is German.

## Steps

1. **Read the ground.** `GLOSSARY-MAP.md`, the glossaries it names for the subdomains the idea
   touches, `domain-model/problem-space/domain-map.md` and the stories under
   `domain-model/problem-space/stories/` with status `draft` on the same topic: the session may
   continue them.

2. **Load the craft.** Call the Skill tool with `mattpocock-skills:grilling` and with
   `mattpocock-skills:domain-modeling`. Follow both, with the project's rules on top: glossary
   rows go into the subdomain glossaries in the table format of `CLAUDE.md` (section
   „Fachmodell“), not into a root `GLOSSARY.md`.

3. **Run the rounds.**
   - **Round 1** is grilling alone, on the idea and what step 1 found.
   - **After every answered round** start a subagent that runs the skill `problem-sync` with the
     answers of that round and the idea that started the session, and wait for it. Build the
     next round only then: your own frontier plus the questions from its report.
   - **Group by story.** From round 2 on, put each question under the story it belongs to,
     `### 📘 US-0042: <Titel>`, questions without a story last under `### 🌐 Übergreifend`.
     Number Q1, Q2, … across all groups.
   - **Provenance line.** Every question ends, below the ➡️ recommendation, with one line whose
     entries are separated by three em spaces (U+2003); entries that do not exist yet are left
     out:

     🗣️ Alex/Pocock   🧩 fr-writer   🏷️ FR-fristen-003/S2   📐 Domain Service   🧪 Unit

     🗣️ is `Alex` for a question from problem-sync, `Pocock` for one only your grilling frontier
     has, `Alex/Pocock` when both have it (ask it once). 🧩 names the skill it came from
     (`grilling` for your own); 🏷️, 📐 and 🧪 come from problem-sync's report.

4. **Close.** The session is done when your frontier is empty, the last problem-sync reports
   `Questions: none`, and the user confirms the shared understanding (as `grilling` requires).
   Then tell the user which stories are `ready` and which are still `draft` with open points, and
   name the next step of the feature workflow in `CLAUDE.md`.

You are done when every decision of the session stands in a story or an FR, every term the
stories use is in a glossary, and the user has confirmed.
