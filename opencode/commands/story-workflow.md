---
description: "Moves a story along its status flow – ready (draft → ready, after validation), start (ready → in-progress), done (in-progress → done, merges its planned FR changes into the active FRs) or cancel – by scripts/requirements.py, and syncs its ticket. Use from /design-the-domain:domain-interview when its session closes, when the user starts, finishes or drops a story, or from another plugin that implements stories (interface, see below)."
---

Load the skill `story-workflow` with the `skill` tool and follow it. Arguments: $ARGUMENTS
