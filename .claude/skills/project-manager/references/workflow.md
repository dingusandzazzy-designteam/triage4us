# Workflow — `project-manager`

> Four flows, one per trigger context. Each flow has a precondition, ordered steps, and an exit criterion. The PM never improvises beyond these.

## Flow 1 — Session Briefing (trigger: session start)

**Precondition:** the user opened a conversation and asked for current state ("where are we?", "status?", "what's next?", "retomada", etc.). No prior context from this session.

**Steps:**

1. Read `workflow/Handoff.md` (or the configured handoff path). If missing, ask the user once where it lives, then save the path as a project memory.
   - **First contact only:** if the handoff exists but its section structure doesn't match the prescribed template, run **Format detection** per `handoff-format.md` and save the schema mapping as a project memory. Future sessions read the mapping and skip detection.
2. Read `plan/00.Plan.md`. Locate the **current phase** marker (the step whose `Status` is `In progress`, or whose gate is the last one *not* marked approved).
3. Read the current-phase sub-file (e.g., `plan/02.Sitemap-Strategy.md`).
4. Cross-check: handoff says phase X, plan says phase Y. If they disagree, flag the discrepancy in the briefing and ask the user to resolve before proceeding.
5. Produce the briefing per `session-briefing.md` template — **under 200 words**.

**Exit criterion:** user has a coherent picture of (a) what was last done, (b) what's currently open, (c) what to do next and which skill owns it.

**Anti-patterns:**

- Dumping the full plan as the briefing. The plan is hundreds of lines; the briefing is a paragraph.
- Briefing without reading the handoff. If the handoff is empty, say so and ask for context, don't fabricate state.
- Recommending a next step that requires an upstream artifact the project doesn't have yet.

---

## Flow 2 — Session Close (trigger: session end)

**Precondition:** the user has finished a chunk of work and wants the state saved. Trigger phrases: "fecha sessão," "save the state," "wrap up," "log this," "handoff update."

**Steps:**

1. Inventory what changed in this session:
   - Decisions made (look for "decidi," "vamos com," approvals).
   - Files modified (the conversation should already reference them; if not, ask).
   - Deliverables shipped (push, deploy, commit, send-to-client).
   - Skills invoked (which produced what).
2. Read the current `workflow/Handoff.md`. Identify which sections need updates.
3. Apply updates per `handoff-format.md`:
   - `Current phase` — same as last session unless a gate was approved.
   - `Last action` — one or two sentences on what this session accomplished.
   - `Open items` — append new pending items; check existing ones off if resolved.
   - `Blockers` — add new ones; remove resolved ones.
   - `Next step` — explicit instruction for the next session (which skill, which artifact, what input is needed).
4. If a gate was approved this session, update `plan/00.Plan.md` (or the sub-file) to mark the step as `Approved` and advance the pointer.
5. Surface anything that needs the user's attention *before* the next session can be productive (e.g., "Kendall needs to confirm current LOI figure").

**Exit criterion:** the handoff is current. If a future session reads only the handoff + plan, it has everything it needs to resume.

**Anti-patterns:**

- Overwriting the handoff with a fresh draft, losing previous decisions. Always preserve history.
- Marking a gate approved when the user hasn't explicitly approved. Ask.
- Logging the conversation transcript. The handoff is state, not transcript.

---

## Flow 3 — Phase Transition (trigger: gate approved / milestone)

**Precondition:** a plan step's gate condition was met (user confirms, deliverable shipped, client approves).

**Steps:**

1. Read the current step's "Gate to advance" line in `plan/00.Plan.md` or the sub-file.
2. Confirm with the user that the gate is met. **Do not assume** from context. Ask explicitly: *"Gate for Step N reads: '\<gate text\>'. Confirm this is met?"*
3. Once confirmed:
   - Mark the completed step's `Status` as `Approved` (or `Done` per the project's taxonomy — see `gates-and-statuses.md`).
   - Set the next step's `Status` to `In progress`.
4. Identify the skills relevant to the new phase:
   - Read each `.claude/skills/<name>/SKILL.md` `description` frontmatter.
   - Match the new phase's deliverable type to a skill's trigger description.
   - Surface the matched skill(s) to the user as the next routing option.
5. Check prerequisites for the new phase:
   - What inputs does the next phase need? (Read its plan sub-file.)
   - Are those inputs available? (Check file existence, prior phase outputs.)
   - If something is missing, surface as a blocker and pause the transition.
6. Update `workflow/Handoff.md`:
   - `Current phase` → new phase.
   - `Last action` → "Gate for Step N approved. Phase moved to Step N+1."
   - `Next step` → the recommended skill invocation.

**Exit criterion:** plan pointer moved, handoff updated, user knows which skill to invoke next and what inputs it needs.

**Anti-patterns:**

- Silently bumping the phase pointer without user confirmation.
- Skipping a phase because "we already did most of it." Each phase has a deliverable; partial work doesn't satisfy the gate.
- Routing to a skill whose prerequisites are missing. Always check first.

---

## Flow 4 — Status Report (trigger: explicit question)

**Precondition:** the user asks a specific question about project state. Examples: "o que tá bloqueado?", "what's the timeline?", "what does Audrey owe us?", "punch list before deploy?", "qual o status do SEO?"

**Steps:**

1. Identify the **scope** of the question:
   - Whole project, one phase, one workstream, one stakeholder, one deliverable?
   - Time horizon: current state, near-term, full timeline?
2. Read only the files relevant to the scope. Don't sweep the whole plan if the question is "what's blocked on copy?"
3. Produce a tight answer per `status-report.md`:
   - Direct response to the question first.
   - Source citations second (file:line where possible).
   - Open questions or things needing the user's input last.
4. If the question can't be answered from the files alone (e.g., "when will Kendall approve X?"), say so honestly. Don't fabricate timelines.

**Exit criterion:** the user has an answer scoped to what they asked, with traceable sources, and any unanswerable parts called out.

**Anti-patterns:**

- Dumping the full plan when asked a narrow question.
- Inventing timelines or stakeholder commitments.
- Confidently answering "yes, it's done" without checking the file. Always trace claims to sources.

---

## When flows compound

A session may trigger multiple flows in sequence:

- Session start → user asks for status → run Briefing flow.
- During the session, a gate gets approved → run Phase Transition flow.
- User finishes work → run Session Close flow.

Run each flow independently. Each one starts with reading the current state of the relevant files (the previous flow's writes are now part of state). Don't try to merge multiple flows into one mega-action — they have different exit criteria.
