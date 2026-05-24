---
name: triage4us-webflow
description: Migrate the Triage4US static HTML/CSS landing page to Webflow. Use when the user asks to start Phase 5 (Webflow handoff doc) or Phase 6 (Webflow migration), wants to recreate the page in Webflow, asks how to map a token / component / interaction from the local build to Webflow, or invokes Webflow MCP tools in this project. Project-specific — do not load on other projects.
user-invocable: false
---

# Triage4US — Webflow migration skill

Owns the bridge between the static HTML/CSS build (this repo) and the Webflow recreation. Two phases:

- **Phase 5 — Webflow Handoff Doc:** before opening Webflow. Reads the live local build, produces a complete spec mapping every token / structure / interaction to its Webflow equivalent.
- **Phase 6 — Webflow Migration:** in-Webflow execution. Recreates the page using the handoff doc + the Webflow MCP server.

The local build at `E:\DZ\Triage4US` is the source of truth. Webflow recreation must match it visually and behaviorally. When the two disagree, the local build wins — surface the conflict, do not silently adjust either side.

## When to load

Load this skill when ANY of these are true:

- User asks about Webflow, Webflow Variables, Webflow Components, Webflow Interactions, Webflow Designer, client-first naming, or Phase 5/6 of the plan.
- User invokes any `mcp__claude_ai_Webflow__*` tool.
- The active task is to translate a CSS token, an HTML structure, or a JS interaction into its Webflow equivalent.

Do NOT load this skill for:
- General HTML/CSS work on the local build (other skills cover that — `impeccable`, `design-motion-principles`).
- SEO / copy work (locked inputs; see `documents/03. Copy/`).
- Initial Webflow account setup or project creation — that's the user's manual step (the MCP operates inside an existing site).

## Required reading order (don't load all upfront)

| Step | Reference | When |
|---|---|---|
| 1 | [references/migration-checklist.md](references/migration-checklist.md) | First — gives the ordered Phase 6 plan. |
| 2 | [references/section-tree.md](references/section-tree.md) | Before any markup recreation. Lists every section, its ID, and Webflow class names. |
| 3 | [references/variables-map.md](references/variables-map.md) | Before any styling. Maps CSS custom properties → Webflow Variables. |
| 4 | [references/components.md](references/components.md) | When building reusable elements (buttons, cards, FAQ items). |
| 5 | [references/interactions.md](references/interactions.md) | When recreating motion, hover states, scroll behaviors. |
| 6 | [references/assets.md](references/assets.md) | When uploading images / SVG icons. |

## Hard rules

- **Use the Webflow MCP, not manual instructions.** When in Phase 6, invoke `mcp__claude_ai_Webflow__*` tools instead of writing step-by-step Webflow Designer instructions for the user. Call `webflow_guide_tool` once at the start of the session to load current MCP capabilities.
- **Client-first naming is law.** Webflow class names follow the project's existing client-first convention (`hero_card`, `section_reality`, `stat_card`, etc). Do not rename to Webflow defaults.
- **Variables, not utility classes.** Every color/radius/font/spacing value in the local build is already tokenized in `styles/tokens.css`. Each token becomes a Webflow Variable. Do not hard-code values in Webflow style panels.
- **Components for repeated patterns only.** `.button`, `.faq_item`, `.stat_card`, `.services_card`, `.donation_card` are Webflow Components. One-off sections (`#hero`, `#final-cta`) are NOT components — recreate them as section-level structure.
- **Locked inputs are immutable.** Copy from `documents/03. Copy/`, visual rules from `documents/02. visual direction/`. Do not rewrite text or change palette during migration.
- **Interactions: native first, custom code last.** Try to recreate every motion as a Webflow Interaction. If the effect needs `@property`, `animation-timeline: view()`, `grid-template-rows: 0fr → 1fr`, or any modern CSS that Webflow Interactions can't express → use custom code embed and document the reason.
- **Mobile breakpoints match the local build.** Webflow's default breakpoints are Desktop (>991), Tablet (768-991), Mobile L (480-767), Mobile P (<480). The local build uses 640, 768, 960, 1024, 1200. Map the local breakpoints to the closest Webflow ones, NOT the other way around.
- **Don't deploy the Webflow staging URL publicly until parity is reviewed.** Phase 6 finishes when the Webflow preview matches the local build at all three breakpoints AND the user signs off.

## What this skill does NOT do

- Write static HTML/CSS for the local build (that's Phase 3 / 4 work, already done).
- Re-audit motion or design (use `impeccable` and `design-motion-principles` skills if needed).
- Manage the Webflow account, billing, or domain configuration.
- Run the Webflow MCP on a non-Triage4US project. This skill is project-scoped.

## Skill orchestration

This skill is **downstream** of:
- `project-manager` — confirms Phase 4 sign-off before Phase 5 can start.
- `impeccable` and `design-motion-principles` — their audits inform what motion needs to survive the migration.

This skill is **upstream** of:
- The Webflow MCP server (`mcp__claude_ai_Webflow__*`) — operationally, but conceptually the MCP is the executor and this skill is the spec.

## Honest limitations

- **Webflow Interactions ≠ CSS animations 1:1.** Some patterns (especially `animation-timeline: view()`, `@property`-driven custom properties, `grid-template-rows: 0fr → 1fr`) cannot be reproduced as native Interactions. The skill flags these explicitly and routes them to custom code blocks.
- **The Webflow MCP is the executor of last resort.** If the MCP can't perform an operation (e.g., the API doesn't expose a specific Designer feature), the skill surfaces the gap and instructs the user to do that one step manually in the Webflow Designer.
- **Variable scoping in Webflow is global.** The local build uses CSS custom properties scoped to `:root` — fine in Webflow Variables. If you ever scope a variable to a component (`.hero { --hero-card-inset: ... }`), that becomes a component-level Variable in Webflow, which behaves slightly differently. Document any scoped variables in `variables-map.md`.
