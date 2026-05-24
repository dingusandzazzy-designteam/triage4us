# Plan Structure

> The PM reads from `plan/`. Convention is loose by design — projects come in many shapes. What's enforced is the *master file + numbered sub-files + gate semantics* pattern.

## Expected layout

```
plan/
├── 00.Plan.md                  ← master, ordered phases overview
├── 01.<phase-name>.md          ← phase 1 detail
├── 02.<phase-name>.md          ← phase 2 detail
├── …
└── NN.<phase-name>.md          ← phase N detail
```

Minimum: `00.Plan.md`. Sub-files are *recommended* but not required for short projects.

Numbering can include half-steps (`02.5.<phase>.md`) when phases are inserted between existing ones without renumbering everything. The PM treats `02.5` as a valid sortable position.

## `00.Plan.md` master — required sections

The master file is the index. Each numbered phase appears with at least:

```markdown
## Step N — <Phase Name>

**Goal:** <one-sentence outcome>

**Deliverable:** <what file(s) produced, what state achieved>

**Gate to advance:** <explicit condition>

**Status:** Draft | In progress | Approved | Blocked | Done
```

The PM reads `**Status:**` to determine the project pointer. The phase whose status is `In progress` is the current phase. If multiple phases are `In progress`, it's a project running parallel workstreams — the PM lists all of them.

If `Status:` lines are missing, the PM falls back to inferring state from the handoff and the order of `Gate to advance` approvals. Document the project's convention in a project memory.

## Numbered sub-files

Each sub-file is the *detail* of one master phase. Recommended sections:

```markdown
# NN — <Phase Name>

**Status:** <mirrors 00.Plan.md, or independently tracked>

## Goal
<expanded outcome>

## How
1. <ordered steps>

## Deliverable
<artifact details>

## Open questions
- <items needing user decision>

## Gate to advance
<exact condition, copied from 00.Plan.md>
```

The PM reads sub-files when:

- Briefing the current phase in detail (Flow 1).
- Identifying deliverables and inputs during phase transitions (Flow 3).
- Producing scoped status reports about a specific phase (Flow 4).

## Status taxonomy

The default vocabulary (extend per-project, document the extension):

| Status | Meaning | When the PM sets it |
|---|---|---|
| `Draft` | Phase is documented but not started. | Initial state. |
| `In progress` | Phase is actively being worked. | When the previous phase's gate is approved and this phase begins. |
| `Approved` | Gate has been met and the user confirmed. | After Phase Transition flow (Flow 3). |
| `Blocked` | Phase cannot progress due to an external dependency. | When the user surfaces a blocker; the PM logs it. |
| `Done` | Phase fully complete, all sub-tasks closed. | Optional terminal state past `Approved` for projects that distinguish "approved" from "shipped." |

A project may collapse `Approved` and `Done` into one. Document in `gates-and-statuses.md`-style overlay.

## Gate semantics

A gate is the explicit condition that must be met to move from phase N to phase N+1. It lives in `**Gate to advance:**` text within the phase.

The PM:

- **Reads** the gate text.
- **Confirms** with the user that the condition is met before bumping the pointer.
- **Never** infers gate approval from context alone.

Examples of good gate text:

- *"Client approves Brand Analysis summary."*
- *"All copy sections marked LOCKED or DRAFT-approved; no TBD or SAMPLE on launch-blocking sections."*
- *"Page deployed to staging URL and Kendall has signed off."*

Examples of bad gate text (too vague — surface for refinement):

- *"Brand work is done."*
- *"We're happy with the copy."*

## How the PM handles plan mutations

Plan files change over time. The PM only writes to plan files in these cases:

| Trigger | Write |
|---|---|
| Phase transition (Flow 3) | Update `Status` of the completed and next phases. |
| Session close (Flow 2) | Update `Status` only if a gate was approved during the session. |
| Explicit user request | Anything the user asks (with confirmation if structural). |

The PM **does not**:

- Renumber phases.
- Rewrite phase descriptions.
- Add new phases without explicit user say-so.
- Delete phases.

Any structural change to the plan is a human decision. The PM can *propose* one (e.g., "you mentioned SEO should slot at 2.5 — want me to add `plan/02.5.SEO-Research.md`?") but always asks first.

## Multi-workstream projects

Some projects have parallel workstreams (e.g., copy track + dev track + design track) running concurrently. The plan can express this two ways:

1. **Single master with parallel `In progress` phases.** `02.Copy.md` and `02.Dev.md` both `In progress`. The PM lists both.
2. **Separate plan folders per workstream** (`plan/copy/`, `plan/dev/`, etc.). The PM treats each as a sub-project; the user picks which one to brief.

Default is single-master. Multi-folder is opt-in via project memory.

## Edge cases

| Situation | Handling |
|---|---|
| `00.Plan.md` exists but no `Status` lines anywhere | Infer state from handoff alone; surface the gap and recommend adding status flags. |
| Multiple phases marked `In progress` | List them; ask user which is primary. |
| Phase numbered out of order (`05` before `04`) | Read sortable order; if intentional (parallel work), respect it. Otherwise flag as inconsistency. |
| Phase with no `Gate to advance` | Treat as in-progress until user explicitly says "done." Recommend adding a gate. |
| Plan written in a language other than English | Read it. The PM is language-agnostic. |
