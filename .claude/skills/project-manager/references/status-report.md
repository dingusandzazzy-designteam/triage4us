# Status Report

> On-demand answer to a specific status question. The PM scopes the report to what the user asked — no broader, no narrower.

## Trigger phrases (examples)

- *"O que tá bloqueado?"* / *"What's blocked?"*
- *"Punch list before launch?"*
- *"Qual o status de SEO?"* / *"Status of SEO?"*
- *"Timeline?"* / *"Cronograma?"*
- *"O que falta no copy?"* / *"What's left in copy?"*
- *"Who owes us what?"*
- *"Quais decisões em aberto?"*
- *"What did we agree on about X?"*

The PM identifies the question's scope, then produces a tight, traceable answer.

## Report structure

```markdown
**<Direct answer to the question, 1–3 sentences.>**

<Optional: a bulleted list or table providing the supporting detail.>

**Sources:** <file:line citations for every non-trivial claim>

**Open questions:** <if any — things the PM couldn't determine from files alone>
```

Length: variable based on the question. A "what's blocked?" answer can be 30 words; a "punch list before launch" answer might be 300. **Match the answer length to the question's scope.**

## Scoping the question

Before reading any files, identify:

| Scope axis | Examples |
|---|---|
| **Topic** | Copy, SEO, design, deploy, motion, brand, all-of-the-above |
| **Workstream** | Single (just copy track) vs. all parallel workstreams |
| **Time horizon** | Current state, near-term (this week), full timeline |
| **Stakeholder** | What does Kendall owe? What does the dev team own? |
| **Phase** | Current phase only, or include past/future |

Don't read all the plan files if the question is "what does Audrey owe us?" — read only the handoff's `## Blockers` and `## Open items` for items naming Audrey.

## Source traceability

Every non-trivial claim in the report cites a source. Format:

- `workflow/Handoff.md:34` — line reference.
- `plan/02.Sitemap-Strategy.md` — full-file reference when the line isn't specific.
- `copy/automotive.md S9 Notes` — section reference inside a file.
- *"Per user statement 2026-05-18"* — when sourced from conversation, with date.

If a claim can't be sourced, say so:

> *"Believed to be true based on session context — not documented in the handoff or plan. Recommend confirming."*

Never make confident claims without traceable backing.

## Common question patterns

### "What's blocked?"

Read `workflow/Handoff.md` `## Blockers`. List each with owner and resolution path.

```markdown
**2 active blockers:**

1. ⚠ **LOI figure** — Audrey / Kendall need to confirm current number; affects S2 stats strip, S9 traction stat, OG description across automotive copy.
2. ⚠ **CSEC / Calgary Flames** — Alysia Olsen needs to clear public-use approval; affects S9 social proof on automotive.

**Sources:** `workflow/Handoff.md:18–22`, `copy/automotive.md S9 Notes`.

**Open questions:** None — blockers are well-documented; just need the human side to deliver.
```

### "Punch list before launch?"

Scope = all `Open items` + current `Blockers` + any phase still `In progress` with launch-blocking deliverables. Read handoff + relevant plan files.

```markdown
**Launch is blocked on 4 items:**

| Item | Owner | Where |
|---|---|---|
| Sweep remaining copy files | `<project>-copy` skill | `workflow/Handoff.md:12` |
| Resolve pending client data point | Client stakeholder | `workflow/Handoff.md:18` |
| Third-party approval | External contact | `workflow/Handoff.md:20` |
| Sample-row name approvals | PM / client | `copy/<page>.md Notes` |

**Sources:** handoff + automotive copy file flags.

**Open questions:** Are the 3 unbuilt vertical pages (entertainment/sports/pos HTML) in scope for this launch, or is automotive shipping alone? — Determines whether item #1 is launch-blocking.
```

### "Timeline?"

The PM **never invents timelines**. It reports:

- Phases marked `In progress` — these are happening now.
- Phases marked `Draft` — these are planned but not started.
- Gates that need to be approved.
- Any explicit deadlines documented in the plan or handoff.

If the user asks "when will we launch?" and no date is documented:

```markdown
**No launch date is documented.** The plan and handoff carry phase pointers but no committed dates.

**Current trajectory** (no dates implied):
- Step 6 — Copywriting: In progress.
- Step 9 — Homepage Generation: In progress.
- Step 11 — Localhost and Deploy: Draft (last in sequence).

**Open question:** Want me to draft a proposed timeline? — That's a planning conversation, not a status report. I'd need stakeholder constraints (Kendall's mandate, client commitments) before fabricating dates.
```

### "Status of SEO?"

Scope = SEO-related artifacts only. Read SEO-related plan steps (currently none documented) + skill state.

```markdown
**SEO is at Step 2.5 — SEO Research, but the slot isn't formalized in the plan yet.**

- `seo-research` skill exists at `.claude/skills/seo-research/` (created 2026-05-18).
- `seo-copy-sync` and `seo-validate` are pending future work.
- `seo/templates/SEO_Master_Template.xlsx` is the spreadsheet template.
- No SEO research has run yet against the project copy.

**Recommended next move:** Run `seo-research` in `no-volumes` mode to generate retroactive briefs against the existing copy — those briefs become the audit baseline for future `seo-validate`.

**Sources:** memory `project-seo-pipeline-slot.md`, `.claude/skills/seo-research/SKILL.md`.

**Open questions:** When do you want to formalize Step 2.5 in `plan/00.Plan.md`? Currently waiting for the other 2 SEO skills to exist.
```

### "Who owes us what?"

Scope = items naming external stakeholders. Read handoff `## Open items` and `## Blockers`; grep plan files for named owners.

```markdown
**External deliverables outstanding:**

| Owner | What they owe | Affects |
|---|---|---|
| Audrey / Kendall | Current LOI figure | S2 stats, S9 traction, OG description |
| Alysia Olsen / CSEC | Public-use approval for Flames logo + quote | S9 social proof |
| Kyle | PBS / Harley-Davidson Tampa / NMAX public-use confirmation | S1 mockup sample rows |

**Sources:** `workflow/Handoff.md:18–22`, `copy/automotive.md` S1 / S9 Notes.

**Open questions:** Want me to draft Slack / email pings to each owner? — That's a deliverable; happy to draft but the user sends.
```

## Anti-patterns

- **Reporting more than the question asked.** "What's blocked?" doesn't deserve a full project summary.
- **Reporting less than the question asked.** "Punch list before launch" needs *the punch list*, not a one-liner.
- **Inventing claims to fill gaps.** If the files don't have the answer, say so. Don't speculate.
- **Skipping source citations.** Every meaningful claim cites a file. Without sources, the report is just an opinion.
- **Refusing to answer because state is messy.** Surface the mess explicitly and recommend a path to clean it up.

## When the question is fundamentally unanswerable

Some questions require information the PM doesn't have:

- *"Will the client like this?"* — Not in the files. PM can't predict.
- *"How much will this cost?"* — Not in the files unless a budget doc exists.
- *"What's the competitor's pricing?"* — Different skill (`seo-research` does competitor analysis but on SEO, not pricing).

For these:

```markdown
**Can't answer from project files.** This needs <type of input: user judgment / external research / stakeholder confirmation>.

**Recommendation:** <how to get the answer — talk to X, run Y skill, look at Z external source>.
```

Don't fabricate. Don't guess. Surface the gap and recommend a path.
