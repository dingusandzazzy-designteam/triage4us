# Session Briefing

> The under-200-word answer the PM gives at session start. Optimized for fast resumption: the user finishes reading in 30 seconds and knows exactly what to do.

## Template

```markdown
**Current phase:** <Plan step N — name>. <One sentence on what this phase is producing.>

**Last action:** <One sentence — what the most recent session shipped. Reference the file or commit if relevant.>

**Open items** ⚠ <count>:
- <Most important pending item.>
- <Second most important — only if material.>
- (Full list in `workflow/Handoff.md`.)

**Blockers** 🚧 <count>:
- <Active blocker with owner.>
- (Or: "None.")

**Next step:** <Specific recommendation. Which skill, which artifact, what input.>
```

Target length: **150–180 words.** Hard cap: 200.

## Filling each section

### `Current phase`

Read from handoff's `## Current phase`. Cross-check against `plan/00.Plan.md` `Status: In progress` line. If they match, state it. If they don't match, flag:

> **⚠ State discrepancy:** handoff says Step 6, plan says Step 5. Resolve before proceeding.

Then describe in one sentence what the phase is for. Pull from the phase sub-file's `Goal` if available.

### `Last action`

Read from handoff's `## Last action`. Don't paraphrase — quote tightly. If the original is too long, trim to one sentence; never invent details.

If `Last action` is missing or stale (e.g., date is months old), say so:

> Last action: *No recent activity logged; handoff last updated 2026-02-12.*

### `Open items`

From handoff's `## Open items`. Show the **top 2–3 most material**, not the full list. Pick:

1. Items with named owners (someone needs to deliver something).
2. Items that block the next step.
3. Items the user explicitly flagged as priority.

Skip:

- Stale items open >5 sessions without resolution (flag separately).
- Items that are now obviously resolved (PM cleans these in session close).

Always end with: *"(Full list in `workflow/Handoff.md`.)"* so the user knows it's a summary.

### `Blockers`

From handoff's `## Blockers`. Include **all** active blockers (not summarized — these are by definition critical). If there are no blockers, write `🚧 None.` explicitly.

### `Next step`

The most important sentence. Pull from handoff's `## Next step`. If the handoff doesn't have one, run the routing logic:

1. Current phase → expected deliverable.
2. Deliverable type → matching skill.
3. Prerequisites met?
4. Recommend the invocation.

The recommendation should be **specific**:

- ✅ *"Invoke `<project>-copy` on `copy/<page>.md` to apply the deferred copy sweep."*
- ✅ *"Wait for Audrey's LOI confirmation — no actionable work until then."*
- ❌ *"Continue working on the project."*

## Anti-patterns

- **Dumping the whole plan** as the briefing. The plan is hundreds of lines; the briefing is a paragraph.
- **Recommending without checking prerequisites.** *"Run `seo-copy-sync`"* is wrong if the briefs don't exist yet.
- **Listing every open item.** Pick 2–3 most material. The user can read the file.
- **Including transcript fragments.** *"Last session you said 'hmm let me think about it'"* — useless. State and decisions only.
- **Inventing dates or timelines.** If the handoff doesn't say when something is due, the briefing doesn't either.
- **Exceeding 200 words.** This is the budget. If you can't fit, the project is in a complex state and the briefing should call that out: *"Project has 4 parallel workstreams; recommend a scoped briefing — which workstream do you want?"*

## Edge cases

### Empty / missing handoff

```markdown
**Current phase:** Cannot determine — `workflow/Handoff.md` is missing or empty.

**Recommendation:** Either point me at the right handoff file (and I'll save the path), or let's start a fresh handoff by walking through current state.
```

### Empty plan

```markdown
**Current phase:** No plan found at `plan/00.Plan.md`.

**Recommendation:** Either point me at the plan location, or we start by defining the phases. (PM doesn't write plans from scratch — that's a strategic decision.)
```

### Conflicting state (handoff says X, plan says Y)

```markdown
**⚠ State discrepancy:** handoff says we're in `<phase from handoff>`, plan master says `<phase from plan>`. These need to match before I can brief reliably.

**Recommendation:** Tell me which is correct, I'll update the other. Then ask for the briefing again.
```

### Project in `Blocked` state

```markdown
**Current phase:** Step N — <name> 🚧 **BLOCKED**.

**Blocker:** <what's blocking, who owns the unblock>.

**Last action:** <unchanged since the block>.

**Next step:** Resolve the blocker — <specific path to unblock>. No useful work downstream until then.
```

### Multi-workstream project

```markdown
**Current phases** (parallel):
- Copy: Step 6 — Copywriting (In progress). <one sentence>
- Dev: Step 9 — Homepage Generation (In progress). <one sentence>

**Which workstream do you want briefed in detail?**
```

Then run a scoped briefing for the chosen workstream.

## Example — session-start briefing

```markdown
**Current phase:** Step 6 — Copywriting (In progress). Drafting and refining `copy/*.md` per `<project>-copy` skill rules, propagating to `index.html`.

**Last action:** Applied client feedback to `copy/<page>.md` + propagated to `index.html`; refactored copy files to table-of-fields format. Pushed to main; deployed.

**Open items** ⚠ 2:
- Copy sweep on remaining vertical pages (deferred from last session).
- Sample-row name approvals — confirm or anonymize before launch.
- (Full list in `workflow/Handoff.md`.)

**Blockers** 🚧 1:
- Client — awaiting confirmation on X before proceeding.

**Next step:** Run `<project>-copy` on the next page copy file. Same rule set as previous page — no client input needed.
```

~175 words. Hits the budget. User can resume in 30 seconds.
