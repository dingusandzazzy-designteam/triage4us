# CLAUDE.md — Triage4US

> Project conventions for Triage4US. Scope-specific rules will be added once project scope is defined.

---

## Folder conventions

- All project folders lowercase: `assets/`, `copy/`, `documents/`, `workflow/`, `plan/`, `prompts/`.
- **Gitignored** (project-internal, never commit): `documents/`, `workflow/`, `plan/`, `prompts/`, `feedbacks/`. See `.gitignore`.
- **Tracked**: `assets/`, `copy/`, source code, `.claude/skills/`, top-level config files. Tracked folders are created on demand once scope is defined.

## Language

- All project documentation is written in **English**. Chat with the user can be in Portuguese; written artifacts stay in English so future-you and any collaborator can read them.

## Living documents

- `workflow/Handoff.md` — current project state. Read at session start, update at session end. Owned by the `project-manager` skill.
- `plan/00.Plan.md` — phase list with statuses + gates. Updated only on phase transitions.

## Skills

- `.claude/skills/seo-research/` — keyword research, page mapping, SEO briefs (project-agnostic).
- `.claude/skills/seo-copy-sync/` — bridge between SEO briefs and copy writing (project-agnostic).
- `.claude/skills/project-manager/` — handoff + plan coordination across sessions (project-agnostic).

When a project-specific skill is needed (e.g., a brand-voice copy skill), create it under `.claude/skills/triage4us-<name>/` following the SKILL.md frontmatter pattern.

## Auto-memory

- Auto-memory directory will live at `C:\Users\marco\.claude\projects\E--DZ-Triage4US\memory\` once the first memory write happens.
- Memory types: `user`, `feedback`, `project`, `reference` (see global memory rules in user prompt).

## Pending scope decisions

- Project type (marketing site / web app / Webflow build / other)
- Client / brand
- Platform / hosting target
- Whether to build a brand-specific copy skill

See `workflow/Handoff.md → Open Items` for the live list.
