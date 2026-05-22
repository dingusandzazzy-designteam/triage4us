# Handoff Format

> The handoff file is the project's *state* — what's true *right now*. It's the first file the PM reads at session start and the last file it writes at session end.

## Default location

`workflow/Handoff.md` (the convention used in this skill's docs).

Common alternatives the PM should recognize:

- `STATUS.md` at project root
- `HANDOFF.md` at project root
- `.claude/handoff.md`
- `docs/status.md`

When the PM can't find a handoff file on first session, it asks the user once and saves the path as a project memory.

## Two scenarios — new project vs existing project

The PM handles two cases when it first encounters a handoff:

| Case | Behavior |
|---|---|
| **New project (no handoff file, or empty/skeleton handoff)** | Use the **prescribed template** below verbatim. The skill creates the file with the documented section structure. |
| **Existing project (handoff already populated with a different structure)** | **Adapt to the existing structure**, do not impose the template. Run the *Format detection* flow below on first contact, save the mapping as a project memory, and respect it for every future read/write. |

The prescribed template is the **default for new projects**. For existing projects, the PM never overwrites an established structure — it detects and preserves.

## Format detection (first contact with an existing handoff)

When the PM reads a handoff for the first time in a project and the structure doesn't match the prescribed template:

1. **List the existing `## ` sections** in the file.
2. **Map each prescribed concept to an existing section** by semantic match (not string match). The standard mapping table:

   | Prescribed concept | Common existing section names |
   |---|---|
   | Current phase | `Current Status`, `Current Phase`, `Status`, `Project Status` |
   | Last action | `Last action`, `Recent activity`, often a bullet inside `Current Status` |
   | Open items | `Open Items`, `Open`, `Pending`, `TODOs` |
   | Blockers | `Blockers`, `Known Issues`, `Issues`, `Risks` |
   | Next step | `Next Step`, `Suggested Next Step`, `Next`, `Recommendations` |
   | History | `Session Log`, `History`, `Changelog`, `Activity Log` |

3. **Surface the mapping to the user for confirmation** the first time. Format:

   > I detected your handoff uses a different structure. Here's how I'm mapping it:
   > - Current phase → `Current Status` (combined with Last action)
   > - Open items → `Open Items` (1:1)
   > - Blockers → `Known Issues` (semantic match)
   > - Next step → `Suggested Next Step`
   > - History → `Session Log`
   >
   > Confirm this mapping? Once confirmed, I'll save it as a project memory and respect this structure going forward.

4. **Save the confirmed mapping as a project memory** named `project_pm_handoff_schema.md`. Future sessions read this memory and skip detection.

5. **Sections the prescribed template doesn't have but the existing handoff does** (e.g., `Project Setup`, `Key Files`, `Established Conventions`, `DO NOT`) are **left untouched**. The PM never deletes or restructures them.

6. **If a prescribed concept has no semantic match in the existing handoff**, the PM:
   - Surfaces the gap (e.g., "No `Blockers` section found and nothing semantically matches.").
   - Asks whether to add a new section or fold blockers into an existing section.
   - Records the decision in the project memory.

## Required sections (prescribed template — new projects only)

> For existing projects with a different structure, use Format detection above. The PM adapts; it does not impose.


```markdown
# Handoff — <Project Name>

> Last updated: <YYYY-MM-DD>
> Last session: <one-line summary>

## Current phase

<Plan step number and name. Should match `plan/00.Plan.md` Status line for that step.>

## Last action

<One or two sentences. What did the most recent session accomplish? Reference files, commits, deliverables.>

## Open items

- [ ] <Item pending. Owner if known.>
- [ ] <…>

## Blockers

- ⚠ <Blocker: who or what is preventing progress.>
- ⚠ <…>

## Next step

<Explicit instruction: which skill to invoke, what input it needs, what artifact it should produce. The future-you reads this and knows exactly what to do.>

## History

<Append-only log of past sessions. Each session adds a dated entry.>

### YYYY-MM-DD — <one-line summary>
<2–4 bullet points of what was done, what was decided.>

### YYYY-MM-DD — <one-line summary>
<…>
```

## Section semantics

### `Current phase`

The plan-step pointer. Format: `Step N — <Phase Name>` matching `plan/00.Plan.md`.

If the project runs parallel workstreams, list each:

```markdown
## Current phase

- Copy track: Step 6 — Copywriting (In progress)
- Dev track: Step 9 — Homepage Generation (In progress)
```

### `Last action`

What the most recent session shipped. Should be specific:

- ✅ *"Applied Client-feedback-01 critical fixes to `copy/automotive.md` and `index.html`; deployed via push to main."*
- ❌ *"Worked on copy."*

### `Open items`

Things known to be pending. Use checkbox syntax so they can be ticked off as resolved. Each item should be actionable — vague "research more about X" items belong in plan files, not the handoff.

### `Blockers`

Things preventing the next step. Different from open items: a blocker stops you, an open item is just pending.

Each blocker should name a *who* or *what* and the resolution it needs:

- ✅ *"Audrey needs to send current LOI figure before S2/S9 stats can be finalized."*
- ✅ *"Netlify auth on staging URL — gate edge function deploy issue."*
- ❌ *"SEO stuff."*

### `Next step`

The single most important sentence in the handoff. Reads like:

> Run `seo-research` in `no-volumes` mode against the existing `copy/` corpus to generate retroactive briefs. Output to `seo/<project>_SEO.xlsx`.

> Run `<project>-copy` on the relevant page copy file to apply the deferred sweep.

> Wait for Audrey's LOI confirmation; nothing actionable until then.

When the next step is "wait," say so — don't fabricate work.

### `History`

Append-only. Each session-close adds a dated entry. The PM **never** rewrites or deletes history entries (except when the user explicitly asks for cleanup).

Entries are *summary*, not *transcript*. 2–4 bullets per session. The conversation transcript is not the PM's responsibility.

## Update protocol

### At session close (Flow 2)

The PM applies updates in this order:

1. **Read** the current handoff fully.
2. **Append** a new `### YYYY-MM-DD — <summary>` entry under `## History` summarizing this session.
3. **Update** `Last updated:` date in the header.
4. **Update** `Last session:` one-liner in the header.
5. **Replace** `## Last action` with the new most-recent action.
6. **Mutate** `## Open items` — tick off resolved, append new.
7. **Mutate** `## Blockers` — remove resolved, append new.
8. **Rewrite** `## Next step` with the new explicit instruction.
9. **Update** `## Current phase` if a gate was approved this session.

Write the file once at the end. Don't do incremental saves mid-update.

### At session start (Flow 1)

**Read-only.** The PM never writes to the handoff at session start. If state is incoherent, surface and ask; don't auto-fix.

### At phase transition (Flow 3)

The PM:

1. Updates `## Current phase` to the new phase.
2. Appends a `### YYYY-MM-DD — Phase transition` history entry naming the gate that was met.
3. Updates `## Next step` to the new phase's first action.
4. Other sections (Open items, Blockers, Last action) get updated only if the user signals they should.

### At status report (Flow 4)

**Read-only.** Status reports never mutate the handoff.

## History retention rules

- **Always preserve.** History is the project's memory across sessions; the PM never silently deletes.
- **Compress only if explicitly asked.** If the handoff grows beyond ~500 lines and the user wants compaction, propose: archive entries older than N months to `workflow/Handoff-archive.md`, keep recent in `Handoff.md`. Don't auto-archive.
- **Date format `YYYY-MM-DD`.** Always absolute, never relative ("last Tuesday"). The handoff outlives the session's relative-time context.

## Anti-patterns

- **Stale `Last updated:` date.** If the PM updates the file, the date moves. Always.
- **`Next step:` written as a vague suggestion.** *"Maybe think about SEO?"* doesn't help future-you. Be specific.
- **Open items that never close.** If an item has been open for ≥5 sessions, the PM should surface it during the next briefing — either it needs decomposition or it should move to a longer-term tracking file.
- **History entries that just say "worked on the project."** Empty entries dilute the log. If a session genuinely produced nothing, write that: *"No deliverables shipped; user reviewed sitemap, no decisions logged."*
- **Mixing transcript and state.** History entries are *what happened and what was decided*, not *what the user typed*.

## Example handoff

```markdown
# Handoff — <Project Name>

> Last updated: YYYY-MM-DD
> Last session: <One-line summary of what was done last session>.

## Current phase

Step 6 — Copywriting (In progress; per-vertical cleanup pending)

## Last action

Applied Client-feedback-01 critical + high redlines to `copy/automotive.md`, propagated to `index.html`, and pushed (commit `10d58dd`). Also refactored all 5 copy files to the new table-of-fields format and updated `_TEMPLATE.md`. SEO research skill `.claude/skills/seo-research/` created. PM skill `.claude/skills/project-manager/` created (this session).

## Open items

- [ ] Apply the same Onus.ai / loyalty / payment-processing sweep to `copy/entertainment.md`, `copy/sports.md`, `copy/pos.md` (deferred from automotive cleanup).
- [ ] Resolve LOI figure ⚠ pending Kendall / Audrey confirmation.
- [ ] CSEC / Calgary Flames logo + quote — ⚠ pending Alysia Olsen approval.
- [ ] Mockup sample rows: confirm public-use approval for PBS / Harley-Davidson Tampa / NMAX, or anonymize before launch.

## Blockers

- ⚠ Audrey / Kendall — need current LOI figure to replace `$500M+` in S2 / S9 / OG description.
- ⚠ Alysia Olsen / CSEC — need public-use approval before adding Flames logo + quote.

## Next step

Run `<project>-copy` to apply the deferred sweep to remaining copy files. After that, propagate to their HTML per the copy↔HTML sync rule.

## History

### YYYY-MM-DD — Example session entry
- Applied client feedback to `copy/<page>.md`, propagated to HTML, pushed to main.
- Refactored copy files to table-of-fields format.
- Created `seo-research` skill at `.claude/skills/seo-research/`.
```
