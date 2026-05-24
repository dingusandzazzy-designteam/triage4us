---
name: seo-copy-sync
description: Bridge SEO research outputs and the project's copy skill — ensure every page's copy is written (or refined) honoring the locked SEO brief (Title ≤60, Meta 150–160, H1 ≤70) AND the 8 on-page SEO best practices (intent, PAA/FAQ, organized structure, descriptive subheadings, keywords in headlines, keyword placement, image support, metadata + alt text). Trigger when copy is being drafted, refined, or audited for a page that already has a locked SEO brief from `seo-research`; when the user asks to apply SEO briefs to existing copy; when reviewing copy against on-page SEO rules; or when validating that subheadings, alt text, or H2/H3 structure honor a page's keyword targeting. Generic skill, project-agnostic. Do NOT trigger for keyword research (use `seo-research`), post-build validation of rendered HTML (use `seo-validate`), or brand-voice review uncoupled from SEO (use the project's copy skill directly).
---

# SEO Copy Sync Skill

You are the **bridge** between locked SEO research outputs and the project's copy skill. Your job is to ensure every page of marketing copy is written (or refined) so that on-page SEO is honored by construction — not retrofitted after the fact.

You **do not write copy**. You read the locked SEO brief for a given page, surface the on-page SEO constraints, hand them to the project's copy skill (e.g., `triage4us-copy`), and verify the output before it ships.

This skill is **project-agnostic**: no vertical-specific vocabulary, no brand-specific rules. The project's copy skill owns voice, tone, and brand vocabulary; this skill owns SEO discipline.

## Position in the SEO pipeline

Three-skill chain:

1. **`seo-research`** → locked spreadsheet (Keyword Research / Page Map / SEO Briefs tabs) + `seo_research_report.md`.
2. **`seo-copy-sync`** *(this skill)* → wraps the project's copy skill so every page born or refined honors its locked brief.
3. **`seo-validate`** → post-build check of rendered HTML against locked briefs (catches drift introduced during HTML generation / motion expansion / late edits).

**Why this skill exists:** without it, the locked briefs from `seo-research` sit in a spreadsheet while the project's copy skill writes from voice/tone rules alone. The copy ends up brand-clean but SEO-inconsistent: vague subheadings, keywords stuffed late, alt text empty, no PAA-style FAQ phrasing, title/meta drifting from the brief. This skill is the connective tissue.

## Always do this first

1. **Identify which page is being worked on.** Ask the user if ambiguous. The page name must match a row in the Page Map tab of the locked spreadsheet (or the `Meta` block in a `copy/<page>.md` file if the project mirrors briefs into copy files).
2. **Read the locked brief for that page** from the source of truth (priority order):
   - `seo/<project>_SEO.xlsx` SEO Briefs tab (canonical).
   - `copy/<page>.md` Meta block (project-mirrored, may be slightly stale if just edited).
   - If both exist and disagree: the xlsx wins; surface the drift.
3. **Load the on-page SEO rules** from `references/on-page-seo.md`. The 8 practices are the checklist.
4. **Decide the operating mode** based on what the user is asking for:
   - **`apply`** — new copy is being drafted. Hand the brief + rules to the project's copy skill upfront so the copy is born compliant.
   - **`refine`** — existing copy needs SEO retrofit. Diff current copy against brief; produce a structured edit plan; hand the plan to the copy skill.
   - **`review`** — copy exists and the user wants an audit (no edits yet). Produce a violation report with severity and fix suggestions; do not edit.

## Prerequisites

- **Locked SEO brief** for the page being worked on. No brief = stop and run `seo-research` first (or point to the page's row in an existing spreadsheet).
- **Project copy skill exists** (e.g., `triage4us-copy`, or whatever name the project uses). Discover via `.claude/skills/<name>/SKILL.md` files. If no copy skill exists, surface that — this skill won't fabricate voice rules.
- **Page Map status** must be `Approved` or `Locked` for the page. If status is `Draft`, surface that the brief may shift and ask the user whether to proceed.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Page identifier | **Yes** | Slug or filename (e.g., `automotive`, `pricing`). Must resolve to a Page Map row. |
| Operating mode | **Yes** | `apply` / `refine` / `review`. Default `review` if ambiguous and ask the user. |
| Source of brief | Optional | Default: project's `seo/<project>_SEO.xlsx`. Override if the project mirrors into copy files. |
| Project copy skill name | Optional | Discovered automatically by scanning `.claude/skills/*/SKILL.md` for a copy-trigger description. If multiple, ask. |

## Workflow (5 phases)

### Phase 1 — Brief consumption

Read the page's locked SEO brief and stash these values:

- Primary keyword + secondary keywords.
- Search intent (Informational / Navigational / Transactional / Commercial).
- Locked Title (≤60 chars).
- Locked Meta description (150–160 chars).
- Locked H1 (≤70 chars).
- Suggested H2/H3 outline if the brief carries one (some `seo-research` outputs do, some don't).
- PAA / "People Also Ask" questions captured during research (often in the spreadsheet's Notes column or the `seo_research_report.md`).

If any of the above is missing, surface the gap before continuing. Don't invent values.

### Phase 2 — On-page rule load

Load the 8 practices from `references/on-page-seo.md`:

1. Write for user intent.
2. Address frequently asked questions (PAA targeting).
3. Make the content organized and easy to digest.
4. Write clear, descriptive subheadings.
5. Put keywords in all headlines.
6. Place keywords strategically throughout the page (beginning + end, long-tail naturally).
7. Support text with relevant images (and write alt text).
8. Optimize metadata and alt text (Title ≤60, Meta 150–160, alt text descriptive + keyword-aware when natural).

These are the audit dimensions. Every page-level edit will be checked against them.

### Phase 3 — Mode-specific work

#### `apply` (new copy being drafted)

1. Compose a **briefing packet** for the project's copy skill containing:
   - The full locked brief (Phase 1 output).
   - The 8 practices (Phase 2), expressed as concrete constraints — e.g., "H2/H3 must reference primary keyword or close variation," "FAQ block phrased as PAA questions if the brief lists any," "Place primary keyword in the first 100 words AND in the final CTA block".
   - The page's section list (from the project's sitemap / template).
2. Invoke the project's copy skill with the briefing packet. The copy skill writes copy that honors voice/tone + the SEO constraints.
3. Sanity-check the produced copy against the 8 practices before considering the work done. Surface any practice the copy missed.

#### `refine` (existing copy needs SEO retrofit)

1. Read the existing copy for the page (`copy/<page>.md`).
2. Diff against the locked brief:
   - Does the Meta block match (Title / Meta description / H1)? If not, flag a re-lock.
   - Do the H2/H3 subheadings carry the primary or secondary keywords? List each subheading + verdict.
   - Is the primary keyword present in the first 100 words? In the closing block? In the meta description?
   - Are FAQ questions PAA-style (full questions a user would type) or rewritten in marketing voice?
   - Do image references have alt text fields populated?
3. Produce a **structured edit plan** — a numbered list of concrete edits, each tagged with the practice number from `references/on-page-seo.md`.
4. Hand the edit plan to the project's copy skill, which executes the edits in voice.
5. Re-check the produced copy against the 8 practices.

#### `review` (audit only, no edits)

1. Read the existing copy.
2. Run the same diff as `refine` Phase 3.2.
3. Produce a **violation report** with severity:
   - **Critical** — brief fields mismatch (Title/Meta/H1 drift). Blocks deploy.
   - **High** — primary keyword absent from first 100 words OR from H1 OR from at least one H2/H3.
   - **Medium** — secondary keywords missing entirely; FAQ not PAA-aligned; image alt text missing.
   - **Low** — subheading could be more descriptive; long-tail variation opportunity missed.
4. Do **not** edit. The report is the deliverable. User decides whether to escalate to `refine`.

### Phase 4 — Handoff to project copy skill

For `apply` and `refine` modes, the actual writing is done by the project's copy skill — not this one. Construct the handoff message clearly:

> "I'm `seo-copy-sync` working on `<page>`. The locked SEO brief and on-page constraints are below. Please write/edit copy that honors voice, tone, and brand vocabulary [your domain], plus the SEO constraints [my domain]. If any voice rule conflicts with an SEO constraint, surface the conflict — do not silently break either side."

Then paste the briefing packet (Phase 3.`apply`.1) or edit plan (Phase 3.`refine`.3).

### Phase 5 — Verification

After the project copy skill produces output, run the audit again (Phase 3.`review`). Anything below severity `Medium` is acceptable for handoff. `Critical` or `High` violations require another pass.

## Outputs

| Mode | Output |
|---|---|
| `apply` | New copy in `copy/<page>.md`, written by the project's copy skill, audit-passing against the 8 practices. |
| `refine` | Edited `copy/<page>.md` + a one-page diff summary of which practices were retrofit and why. |
| `review` | Markdown violation report (no file edits). Suggested format: `seo/audits/<page>_<date>.md` if the project tracks audits; otherwise inline in the conversation. |

The skill **never** writes the rendered HTML — that's downstream (Phase 9+ in the typical project workflow). The skill always operates on `copy/*.md` (or equivalent) source files. HTML drift from copy is `seo-validate`'s problem.

## Hard rules (DO NOT)

- **Never write copy yourself.** This skill orchestrates; the project's copy skill writes. Even one sentence written by this skill bypasses the voice/tone discipline the project relies on.
- **Never relax the brief's budgets.** Title >60, Meta >160, H1 >70 are violations — do not "round up" or argue for exceptions. If the brief is wrong, re-run `seo-research` for that page; don't paper over.
- **Never silently overwrite a locked Title/Meta/H1.** The brief is the lock. Changes require re-running `seo-research` for that page and re-locking. Surface the need; don't act unilaterally.
- **Never invent PAA questions.** Use only the ones captured by `seo-research` (typically in the spreadsheet Notes column or the research report). If the brief lacks PAA data, flag it and proceed without that practice.
- **Never run when Page Map status is `Draft`.** The brief might shift. Stop and surface the gap. Exception: `review` mode is OK on Draft pages (read-only).
- **Never bypass the project's copy skill.** If the project has no copy skill, this one cannot operate. Surface the missing dependency.
- **Never operate on a page with no locked brief.** No brief = `seo-research` hasn't been run for that page. Run that first.
- **Never assume the project's status taxonomy.** Read it from the spreadsheet `Instructions` tab or the project's docs. Default to `Draft / Approved / Locked` if undocumented.

## What this skill does NOT do

- **Copy writing / wording / tone.** That's the project's copy skill.
- **Keyword research / volume resolution.** That's `seo-research`. If you need keywords, stop and run that first.
- **Post-build HTML validation.** That's `seo-validate` (Phase 10.5 in the typical project workflow). This skill works on source `copy/*.md`, not rendered HTML.
- **Schema markup / structured data (JSON-LD, FAQPage, Article, etc.).** Technical SEO — out of scope. Different toolchain.
- **Backlinks / internal-linking audit.** Off-page and site-architecture concerns — separate skill (not yet created).
- **Image generation.** Practice #7 (relevant images) is honored by *naming* the asset slot in the copy file; actual image generation belongs to the project's image-generation phase (e.g., Phase 10 in a typical workflow).
- **Multilingual SEO.** One locale per invocation. Localization is a wrapping concern.

## How this skill interacts with the project's copy skill

The contract is one-way: this skill provides constraints; the project's copy skill produces copy that honors them. The project's copy skill keeps full authority over voice, tone, brand vocabulary, "Never Say" tables, and audience tier.

If a voice rule conflicts with an SEO constraint:

- **Brand-guideline forbidden word that is also the primary keyword.** Real conflict. Surface to the user — they decide. Default recommendation: re-target the page on a secondary keyword from the same cluster, do not break brand.
- **Subheading descriptiveness (practice #4) vs voice's "punchy fragment" style.** Soft conflict. Resolve by writing subheadings that are *both* descriptive AND in voice — usually possible. Surface if not.
- **Title or H1 phrasing where the locked version sounds off-voice.** Re-open the brief, re-run `seo-research` for the page (lightweight — just the brief regeneration phase), produce a voice-aligned alternative within budget, re-lock. Don't silently rewrite.

The project's copy skill is **always** invoked. This skill never bypasses it, even for "small" edits.

## Index — references

| File | Covers |
|---|---|
| `references/on-page-seo.md` | The 8 best practices, expanded with project-agnostic examples and audit heuristics. |

## Extension points

- **Project-specific PAA capture.** If the project wants PAA stored somewhere other than the spreadsheet Notes column (e.g., a per-page `copy/<page>.md` "PAA" block), document that as a project memory.
- **Project-specific audit format.** Some projects want the violation report committed (`seo/audits/<page>_<date>.md`); others want it conversation-only. Default: conversation-only unless the project asks otherwise.
- **Custom severity overrides.** A project may decide that, say, missing alt text is `Critical` rather than `Medium`. Document overrides in a project memory.
- **Cross-page consistency.** This skill works one page at a time. For a multi-page sweep, invoke per page in sequence — the skill keeps no cross-page state.
