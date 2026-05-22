# Skill Orchestration

> The PM doesn't invoke skills — it tells the user which skill to invoke and why. The routing logic comes from reading each skill's own `SKILL.md`.

## How to discover skills in a project

1. Look in `.claude/skills/` (this convention) — every subdirectory is a skill.
2. For each skill, read `<skill-name>/SKILL.md`:
   - **`name`** in the frontmatter — the skill's identifier.
   - **`description`** in the frontmatter — when to trigger, scope, and what *not* to use it for.
   - **First H1 + opening paragraph** — what the skill is for in plain language.
   - **Prerequisites section** — what inputs it expects to exist.
   - **What this skill does NOT do** — explicit out-of-scope.

The PM builds a mental routing table from these. It does **not** invent skills, infer skills from filenames, or use skill capabilities the docs don't claim.

## Routing decision — the basic algorithm

When the user (or the current plan phase) needs a deliverable:

1. **Identify the deliverable type** — copy, design, SEO research, animation code, deploy artifact, etc.
2. **Scan skill descriptions** — find the skill whose `description` includes that deliverable type and whose triggers match the project context.
3. **Check prerequisites** — read the skill's `Prerequisites` and `Inputs` sections. Are those artifacts present in the project?
   - Yes → recommend invoking the skill.
   - No → identify which *other* skill produces the missing inputs. Route to that one first.
4. **Surface to the user** as: *"Next move is `<skill-name>`. It needs `<input>` which is `<present | missing>`. If missing, run `<upstream-skill>` first to produce it."*

## Dependency rules

Skills declare their own dependencies in their `SKILL.md`. The PM reads those declarations; it does not enforce dependencies the skills don't declare.

Common patterns:

### Linear pipeline

Skill A produces an artifact that skill B consumes. B's `SKILL.md` lists A's output in `Prerequisites`.

Example:

> `seo-research` produces `seo/<project>_SEO.xlsx` with locked briefs.
> `seo-copy-sync` lists `seo/<project>_SEO.xlsx` with `Page Map` rows marked `Draft` as a prerequisite.

PM routing: when copy is needed and locked briefs don't exist, route to `seo-research` first.

### Parallel-independent

Two skills produce different artifacts that don't depend on each other. Project may run them in any order.

Example:

> `<project>-copy` writes copy.
> `<project>-animation` writes motion code.
> Neither depends on the other; the page just needs both before launch.

PM routing: ask the user which is the priority; route accordingly. Both will be needed eventually.

### Feedback loop

Skill A produces a draft; skill B reviews/validates; skill A re-runs with feedback.

Example:

> `seo-research` drafts briefs.
> `seo-validate` (future) audits the rendered page against the briefs.
> If validation fails, `seo-research` may need re-running with corrections.

PM routing: read the validation output; if failures, route back to the producing skill with the specific failure as input.

### Co-located orchestration

One skill orchestrates the invocation of another.

Example:

> `seo-copy-sync` (future) is a meta-skill that reads SEO briefs and invokes the project's copy skill (e.g., `<project>-copy`) to write copy honoring those briefs.

PM routing: invoke the orchestrator; trust it to invoke the inner skill.

## What the PM is responsible for

- **Knowing the current phase** and which deliverable that phase produces.
- **Matching deliverable type to skill** via the skills' `description` text.
- **Checking prerequisites** — does the skill have what it needs?
- **Surfacing the routing decision** to the user with reasoning.
- **Flagging dependency violations** if the user tries to invoke a skill whose inputs aren't ready.

## What the PM is NOT responsible for

- **Invoking skills.** The user does that explicitly.
- **Inferring undocumented dependencies.** If skill B doesn't say it needs skill A's output, the PM doesn't fabricate the link.
- **Validating skill output quality.** If a copy skill produces copy and the copy is bad, that's not the PM's call. The user (or `seo-validate`) judges.
- **Resolving ambiguity about which skill to use.** If two skills both plausibly handle the deliverable, the PM lists both and asks the user to pick.

## Building the routing table — concrete example

For a typical marketing-site project, the PM would read these skills:

| Skill | Produces | Prerequisites | Triggers |
|---|---|---|---|
| `<project>-copy` | Copy in `copy/*.md` | Brand analysis + sitemap; the copy skill's docs reference `plan/01`, `plan/03`. | When user asks to draft/refine copy. |
| `<project>-animation` | Motion code in `script.js` / `snippets/` | Markup exists in `index.html`; `plan/04` motion scope locked. | When user asks about animations / scroll effects. |
| `seo-research` | `seo/<project>_SEO.xlsx` + `seo/seo_research_report.md` | Project brief, spreadsheet template, operating mode chosen. | When user asks for keyword research / SEO setup. |
| `project-manager` | Updated handoff + plan status | Plan dir + handoff file. | Session start/end, phase transition, status request. |

From this table, the PM can answer "what's next?" by:

1. Reading the handoff's `Current phase` — say, `Step 6 — Copywriting`.
2. Identifying the deliverable — copy in `copy/*.md`.
3. Matching to skill — `<project>-copy`.
4. Checking prerequisites — does brand analysis exist? Does sitemap exist? Yes / no.
5. Recommending: *"Invoke `<project>-copy` on the relevant copy file. Brand analysis (plan/01) is approved; sitemap (plan/03) is approved; the skill's inputs are ready."*

## When skills are missing or undocumented

If the current phase needs a deliverable type with no matching skill:

- The PM says so. *"No skill in this project handles `<deliverable>`. Options: (1) do it manually, (2) create a new skill, (3) extend an existing skill."*
- The PM does **not** suggest the wrong skill just because something has to be picked.

If a skill exists but its `SKILL.md` is empty or incoherent:

- The PM surfaces the gap: *"`<skill>` exists but its description is incomplete; can't route confidently. Recommend reviewing the skill's docs."*

## Cross-project skills

Some skills are generic (work in any project) and some are project-specific (named with project prefix like `triage4us-*`). The PM treats both as routing options as long as they're discoverable in `.claude/skills/`. The skill itself enforces its scope via its `description` field.

When the user is in a different project context, project-specific skills shouldn't trigger — but if they do, the PM defers to the skill's own self-gating. PM doesn't override skill triggers.
