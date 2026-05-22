# Gates and Statuses

> Gate semantics and the default status taxonomy. Projects can extend; the PM follows whatever the project documents.

## Default status taxonomy

| Status | Meaning | Set when |
|---|---|---|
| `Draft` | Phase is documented; work has not started. | Initial plan state. |
| `In progress` | Phase is actively being worked. | Previous phase's gate is approved; this phase begins. |
| `Blocked` | Phase cannot progress; needs external input. | User reports a blocker; PM logs it. |
| `Approved` | Gate met; user explicitly confirmed. | After Phase Transition flow (Flow 3). |
| `Done` | Phase fully complete; all sub-tasks closed. | Optional terminal; for projects distinguishing "approved" (concept) from "done" (shipped). |
| `On hold` | Phase intentionally paused; not blocked, deprioritized. | User signals a pause; PM logs the reason. |

`Approved` is the most common terminal state. `Done` is used when a project tracks both client approval and operational completion separately.

## Gate definition

A **gate** is the explicit, testable condition that must be true to advance from one phase to the next.

Format in `plan/00.Plan.md`:

```markdown
**Gate to advance:** <condition>
```

The condition should be:

- **Testable** — someone can check whether it's met.
- **Specific** — names files, approvals, or events.
- **Owned** — implies who's responsible for confirming (usually the user / client).

Good gate examples:

- *"Client approves Brand Analysis summary."*
- *"`copy/automotive.md` has zero `TBD` or `SAMPLE` flags on launch-blocking sections."*
- *"Page deployed to staging URL; Kendall has signed off via email or DM."*
- *"`SEO_Master.xlsx` has all `High` priority keywords mapped to pages; cannibalization check passes."*

Bad gate examples (PM should flag these for refinement):

- *"Brand work is done."* — Done by whose call?
- *"Copy is ready."* — Ready meaning what?
- *"We're happy."* — No testable condition.

## Gate confirmation protocol

The PM **never** assumes a gate is met. The protocol for confirming:

1. **Read** the gate text from the current phase.
2. **Ask** the user: *"Gate for Step N reads: '\<exact gate text\>'. Is this condition met?"*
3. **Wait** for explicit confirmation. *"Looks good"* is enough; *"I think so"* is not — ask again.
4. **Record** the confirmation in the handoff `History` entry with a date.
5. **Advance** the pointer.

Why so strict: silent gate advancement is the #1 way the PM loses sync with reality. The user must say yes.

## Blocked status — special handling

When a phase is `Blocked`:

- The PM logs the blocker in `workflow/Handoff.md` under `## Blockers`.
- The phase's `Status` in `plan/00.Plan.md` flips from `In progress` to `Blocked`.
- The `## Next step` in the handoff describes what's needed to *unblock*, not what to do *after* the block.
- During Briefing flow (Flow 1), blocked phases are highlighted — the user needs to know there's an external dependency.

When the blocker resolves:

- The PM moves status from `Blocked` back to `In progress`.
- Logs the resolution in handoff history.

## Status mutation rules

The PM writes to `Status` only in these scenarios:

| Flow | Mutation |
|---|---|
| Phase Transition (Flow 3) | `In progress` → `Approved` for current; `Draft` → `In progress` for next. |
| Session Close (Flow 2) | Update `Status` only if a gate was approved during the session, else leave alone. |
| Explicit user request | Any user-driven mutation, with confirmation if structural (e.g., flipping multiple phases at once). |

The PM **never**:

- Skips from `Draft` directly to `Approved`. There must be an `In progress` interval.
- Flips a phase from `Approved` back to `In progress` silently. Reopening a phase is a meaningful event; document why in history.
- Marks a phase `Done` when its gate text says `Approved`. Follow the project's terminal vocabulary.

## Multi-phase parallel progress

When a project has parallel workstreams, multiple phases may be `In progress` simultaneously. The PM:

- Lists all `In progress` phases when briefing.
- Tracks gates independently — gate for the copy track is different from gate for the dev track.
- Does **not** consider the project "done" until all `In progress` phases reach their gates.

## Extending the taxonomy

Some projects need additional states:

| Custom status | Common use |
|---|---|
| `Review` | Phase output is being reviewed by an external party before approval. |
| `Revised` | Phase was re-opened after `Approved` due to scope change. |
| `Deferred` | Phase exists in the plan but is intentionally postponed to a later release. |
| `Cancelled` | Phase is no longer in scope. |

If a project adds custom states, document them in a project memory and reference from `plan/00.Plan.md`. The PM reads the memory and respects the extension.

## Gate types — cheat sheet

Different gates need different verification:

| Gate type | Verification |
|---|---|
| **Client approval** | User confirms they got the approval (email, call, message). PM logs the source. |
| **Internal team approval** | User confirms with the named owner. |
| **Deliverable shipped** | File exists, deploy URL responds, commit pushed. PM can verify some of these directly. |
| **Quality threshold** | Tests pass, length budgets fit, no flagged violations. PM can run light checks. |
| **External milestone** | E.g., "Q3 budget approved." User confirms. |

The PM verifies what it can verify mechanically (file exists, URL responds). For anything human-judgment (approvals, quality calls), the PM asks the user and trusts their confirmation.

## Status visibility

The current status of every phase should be readable from `plan/00.Plan.md` in one pass. If the PM has to dig into sub-files to figure out where the project is, the master is incomplete. Recommend an update.

The handoff's `## Current phase` is the *operative* status — what the team is actually working on now, which should match the plan's `In progress` markers. If they don't match, the PM flags the inconsistency.
