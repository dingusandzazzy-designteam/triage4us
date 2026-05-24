# Variables Map — CSS tokens → Webflow Variables

Every value in `styles/tokens.css` becomes a Webflow Variable. The local CSS custom property names are preserved (without the leading `--`) so the Webflow Variables panel mirrors the design system 1:1.

Use `variable_tool` from the Webflow MCP to create these.

---

## Color (Webflow type: Color)

| Webflow Variable | Hex / Value | Notes |
|---|---|---|
| `color-white` | `#FFFFFF` | Pure white only for page surface |
| `color-background-soft` | `#F7F9FB` | Section bg (hero, reality) — slightly tinted near-white |
| `color-soft-blue` | `#E9F0FF` | Accent surface for impact / data |
| `color-bright-green` | `#00C44C` | Accent — pills, active states, floating donate icon |
| `color-deep-green` | `#016847` | Primary CTA, brand identity color |
| `color-deep-teal` | `#022F42` | Display text on light, dark gradient overlays |
| `color-muted-gray` | `#5B6B7A` | Secondary text, captions |
| `color-near-black` | `#0B0D11` | Body text — tinted near-black, not #000 |
| `color-stable-green` | `#7BB662` | Secondary accent, stat-card variants |
| `color-border-soft` | `#E6EBF0` | Hairlines, dividers |

### Semantic aliases (Webflow type: Color — referenced)

In Webflow, create these as **referenced** variables (pointing to the swatches above), not duplicates:

| Alias | Points to |
|---|---|
| `color-text-primary` | `color-near-black` |
| `color-text-deep` | `color-deep-teal` |
| `color-text-muted` | `color-muted-gray` |
| `color-text-on-dark` | `color-white` |
| `color-bg-page` | `color-white` |
| `color-bg-soft` | `color-background-soft` |
| `color-bg-accent-soft` | `color-soft-blue` |
| `color-cta-primary` | `color-deep-green` |
| `color-cta-primary-hover` | `#014f37` (no swatch; hard-code or add) |
| `color-accent-bright` | `color-bright-green` |
| `color-accent-stable` | `color-stable-green` |

---

## Typography

### Font family (Webflow Site Settings → Fonts)

- **Manrope** — load from Google Fonts. Weights: 400, 500, 600, 700, 800. Set as default font.

CSS source: `--font-primary: "Manrope", system-ui, -apple-system, "Segoe UI", sans-serif;`

### Font sizes (Webflow type: Size)

All use clamp() for fluid scaling. Webflow Variables support `clamp()` since 2024 — paste the full clamp expression.

| Webflow Variable | Value | Use |
|---|---|---|
| `fs-display` | `clamp(2.5rem, 5vw + 1rem, 4.5rem)` | Hero H1, final-CTA H2 |
| `fs-h1` | `clamp(2.25rem, 4vw + 0.5rem, 3.5rem)` | (unused currently — reserve) |
| `fs-h2` | `clamp(1.75rem, 2.5vw + 0.5rem, 2.75rem)` | Section H2 |
| `fs-h3` | `clamp(1.25rem, 1vw + 0.875rem, 1.5rem)` | Card titles |
| `fs-stat` | `clamp(2.75rem, 4vw + 1rem, 4rem)` | Big stat numbers (78%, 40%) |
| `fs-body-large` | `1.125rem` | Hero subtext, intro paragraphs |
| `fs-body` | `1rem` | Default body |
| `fs-small` | `0.875rem` | Trust lines, captions, footer |
| `fs-tiny` | `0.75rem` | Legal, eyebrow labels |

### Font weight (Webflow type: Number)

| Webflow Variable | Value |
|---|---|
| `fw-regular` | `400` |
| `fw-medium` | `500` |
| `fw-bold` | `700` |

### Line height (Webflow type: Number)

| Webflow Variable | Value |
|---|---|
| `lh-tight` | `1.1` |
| `lh-snug` | `1.25` |
| `lh-normal` | `1.5` |
| `lh-relaxed` | `1.65` |

### Letter spacing (Webflow type: Size)

| Webflow Variable | Value |
|---|---|
| `ls-tight` | `-0.02em` |
| `ls-normal` | `0` |

---

## Radius (Webflow type: Size)

| Webflow Variable | Value | Use |
|---|---|---|
| `radius-button` | `999px` | All pill buttons |
| `radius-small` | `12px` | Small chips, eyebrow pills |
| `radius-medium` | `20px` | FAQ items |
| `radius-card` | `24px` | Default card (stat, services, donation) |
| `radius-large` | `32px` | (reserved) |
| `radius-section` | `40px` | Hero card, final-CTA card |

---

## Spacing — 4-pt grid (Webflow type: Size)

| Webflow Variable | rem | px |
|---|---|---|
| `space-0` | `0` | 0 |
| `space-1` | `0.25rem` | 4 |
| `space-2` | `0.5rem` | 8 |
| `space-3` | `0.75rem` | 12 |
| `space-4` | `1rem` | 16 |
| `space-5` | `1.5rem` | 24 |
| `space-6` | `2rem` | 32 |
| `space-7` | `3rem` | 48 |
| `space-8` | `4rem` | 64 |
| `space-9` | `6rem` | 96 |
| `space-10` | `8rem` | 128 |

### Section vertical padding (referenced from space scale)

| Webflow Variable | Points to | px |
|---|---|---|
| `section-padding-small` | `space-7` | 48 |
| `section-padding-medium` | `space-8` | 64 |
| `section-padding-large` | `space-9` | 96 |
| `section-padding-huge` | `space-10` | 128 |

---

## Container widths (Webflow type: Size)

| Webflow Variable | Value | Used by |
|---|---|---|
| `container-small` | `48rem` (768px) | (reserved) |
| `container-medium` | `64rem` (1024px) | FAQ section, intro blocks |
| `container-large` | `80rem` (1280px) | All standard sections |
| `container-full` | `90rem` (1440px) | (reserved) |

---

## Elevation — Shadows (Webflow type: Shadow)

Webflow supports Shadow Variables since 2024. Paste the full shadow expression.

| Webflow Variable | Value |
|---|---|
| `shadow-soft` | `0 1px 2px rgba(11, 13, 17, 0.04), 0 4px 16px rgba(11, 13, 17, 0.04)` |
| `shadow-card` | `0 2px 4px rgba(11, 13, 17, 0.04), 0 12px 32px rgba(11, 13, 17, 0.06)` |
| `shadow-lift` | `0 4px 12px rgba(11, 13, 17, 0.08), 0 24px 48px rgba(11, 13, 17, 0.10)` |

Note: the floating donate CTA uses a custom shadow with green tint that should be a separate Variable:
- `shadow-floating-donate-idle` = `0 8px 24px rgba(1, 104, 71, 0.32), 0 2px 6px rgba(0, 0, 0, 0.12)`
- `shadow-floating-donate-hover` = `0 12px 32px rgba(1, 104, 71, 0.4), 0 3px 10px rgba(0, 0, 0, 0.15)`

---

## Motion (Webflow type: Number — for durations / String — for easings)

| Webflow Variable | Value |
|---|---|
| `duration-fast` | `150ms` |
| `duration-base` | `250ms` |
| `duration-slow` | `400ms` |
| `ease-out-soft` | `cubic-bezier(0.22, 1, 0.36, 1)` |

Note: Webflow Interactions use Webflow's own easing UI; the variable here is for custom code embeds (FAQ reveal, sheen drift, etc.).

For the services-card image zoom, the custom curve is `cubic-bezier(0.33, 1, 0.68, 1)` (ease-out-quart). Add as `ease-out-quart` if you want it tokenized; otherwise inline in the custom code.

---

## Layout helpers (Webflow type: Size)

| Webflow Variable | Value |
|---|---|
| `page-padding-inline` | `clamp(1.25rem, 4vw, 2.5rem)` |

Used by `.padding-global`.

---

## Component-scoped variables (do NOT create globally)

These exist inside a single component's CSS and should be set as **local variables** in the relevant Webflow component's settings, not global Variables:

- `--hero-card-inset` — defined on `.section_hero`, value `space-5` on mobile, `space-6` ≥768, `space-7` ≥1200.
- `--header-offset` — defined on `.section_hero`, value `4.5rem`.

In Webflow these would be inline custom properties on the section element, or part of a per-breakpoint component setting.

---

## Verification

After creating all Variables in Webflow:

- [ ] Open the Webflow Variables panel — 10 color swatches + 11 semantic color aliases visible.
- [ ] Open the Style panel of any text element — Manrope appears as the active font.
- [ ] Inspect the rendered HTML on Webflow's staging — `font-family` resolves to `"Manrope", ...`.
- [ ] No hard-coded hex values appear anywhere in the Webflow style classes (verify by inspecting CSS).
