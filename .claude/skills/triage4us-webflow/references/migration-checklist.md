# Migration Checklist — Phase 6 Execution Order

Step-by-step plan for recreating the Triage4US landing page in Webflow. Each step has a verification gate before moving on. Do NOT skip ahead.

## Prerequisites (before Phase 6 starts)

- [ ] Phase 4 signed off by user (local build approved on Netlify).
- [ ] Phase 5 doc reviewed (this skill's references are the Phase 5 doc).
- [ ] Webflow site created (manual step; MCP operates inside an existing site).
- [ ] `webflow_guide_tool` called once at session start to load current MCP capabilities.

## Step 0 — Connect

1. Authenticate the Webflow MCP if not already connected.
2. Use `data_sites_tool` to list sites; confirm the right site ID.
3. Save the site ID as project memory for the duration of Phase 6.

## Step 1 — Variables

Webflow Variables are the foundation. Recreate them BEFORE any structure.

1. Read [variables-map.md](variables-map.md) for the full mapping.
2. Use `variable_tool` to create variables in this order:
   - Color (10 swatches + semantic aliases)
   - Typography (font family, sizes, weights, line-heights, letter-spacing)
   - Radius (7 values)
   - Spacing (11 values, the 4-pt grid)
   - Containers (4 widths)
   - Elevation (3 shadow tokens — Webflow supports shadow variables since 2024)
   - Motion (3 durations + 1 easing curve)
3. **Gate:** every CSS custom property in `styles/tokens.css` has a corresponding Webflow Variable. No hard-coded hex values, no hard-coded px in spacing or radius.

## Step 2 — Font loading

1. Manrope (400, 500, 600, 700, 800) — load via Webflow's Google Fonts integration.
2. Set Manrope as the project's default font in Webflow Site Settings.
3. **Gate:** body text on a blank Webflow page renders in Manrope, not the Webflow default.

## Step 3 — Page shell

1. Create a single page: `index` (slug `/`).
2. Set page-level SEO metadata: title, meta description, OG image, Twitter card. Pull values from `index.html` `<head>`.
3. Add the LCP preload as a head custom code:
   ```html
   <link rel="preload" as="image" href="<webflow-asset-url>/hero.png" fetchpriority="high">
   ```
   (Wait until Step 7 to fill the asset URL — after upload.)
4. **Gate:** Webflow page exists, SEO metadata matches local build, preload tag staged.

## Step 4 — Layout primitives

Build the client-first layout primitives as Webflow Components.

1. `padding-global` — page inline padding wrapper (see [components.md](components.md)).
2. `container-large` — max-width 1280px wrapper.
3. `container-medium` — max-width 1024px wrapper (used in FAQ section).
4. `page-padding` utility — vertical section padding.
5. **Gate:** dropping these components into a blank page reproduces the local build's section rhythm.

## Step 5 — Header

1. Build `site-header` component with logo + nav + hamburger + CTA + mobile drawer.
2. The transparent-over-hero / frosted-on-scroll behavior is a **Webflow Interaction**: trigger on scroll past 40px, toggle a class. See [interactions.md](interactions.md).
3. Hamburger toggle + mobile drawer slide-down: Webflow native click interaction with two states. ESC key close: custom code embed.
4. **Gate:** at >768px the inline nav renders; <768px the hamburger renders. Toggle works. Logo + CTA always visible.

## Step 6 — Reusable components (buttons, cards)

In this order:

1. `.button` base + `.button.is-primary`, `.is-secondary`, `.is-tertiary`, `.is-on-dark` variants. Active scale, hover translate.
2. `.faq_item` — accordion item with trigger + answer.
3. `.stat_card` (informational) — 4 variants: `--metric`, `--widget`, `--gradient`, `--photo`.
4. `.services_card` (image-led) — full-bleed image, dark gradient overlay, content bottom-left.
5. `.donation_card` (action) — cursor: pointer, hover lift.

Build each as a true Webflow Component with editable text/image instances.

**Gate:** dropping each component renders correctly on a test page with placeholder content.

## Step 7 — Asset upload

1. Upload all 12 images from `assets/images/` to Webflow Assets (`asset_tool`). Get the Webflow asset URLs.
2. Upload all 27 icons from `assets/icons/` to Webflow Assets.
3. Update the head preload tag from Step 3 with the real Webflow URL for `hero.png`.
4. **Gate:** every image referenced in the local build has a corresponding Webflow asset URL.

## Step 8 — Sections (in DOM order)

For each section, see [section-tree.md](section-tree.md) for structure and [components.md](components.md) for which components plug in:

1. **Hero** — full-bleed image card + content overlay + dual CTAs.
2. **The Reality** — 4 stat cards in a bento grid (1fr 1fr 1fr 1.6fr at ≥1024px).
3. **Our Mission** — 6 services cards in 3-col grid (≥960px).
4. **Why It Matters** — split image + body + pull quote.
5. **Donation Impact** — 4 donation cards + CTA section.
6. **Final CTA** — hero-style card with sheen drift.
7. **FAQ** — 4 accordion items in container-medium.

**Gate after each section:** matches local build at desktop. Mobile + tablet checks happen in Step 11.

## Step 9 — Footer

Build `site-footer` component with tagline + legal + dynamic year.

The dynamic year (`<span id="year">`) becomes a custom code embed: `<script>document.getElementById('year').textContent=new Date().getFullYear();</script>` — or inline a static current year if the page is regenerated annually.

## Step 10 — Floating donate CTA

This is a separate component at the body root, not inside any section.

1. Pill-shaped link with heart icon (Heroicons fill SVG), positioned fixed bottom-right.
2. Visibility tied to hero scroll position — Webflow Interaction: when `.section_hero` exits viewport, set `data-visible="true"`.
3. Halo (sonar-ping ring) — pure CSS `@keyframes` in custom code (cannot be expressed natively because it loops with both transform AND opacity in a specific pattern; Webflow Interactions don't loop natively).

See [interactions.md](interactions.md) for the embed code.

## Step 11 — Motion + interactions pass

After all structure is in place, audit motion fidelity. See [interactions.md](interactions.md) for the full list. Critical ones:

- FAQ accordion expansion (grid-template-rows 0fr → 1fr) — custom code.
- Hero page-load orchestration — Webflow Interactions (stagger 4 elements).
- Below-fold image fade-in on load — custom code embed.
- Stat number scroll reveal — `animation-timeline: view()` custom code, gated by `@supports`.
- Final CTA sheen drift — `@property --sheen-x` custom code embed.
- Services-card image zoom 700ms — Webflow native or custom code.
- Mobile nav drawer slide.
- Hamburger morph.
- Button :active scale.

## Step 12 — Breakpoint verification

For each breakpoint — desktop (≥1200), tablet (768-991), mobile L (480-767), mobile P (<480) — compare side-by-side against the local Netlify build:

- Header layout (inline nav vs hamburger at the right cutoff)
- Hero card sizing and content padding
- Stat cards grid (1fr / 2-col / 1fr 1fr 1fr 1.6fr)
- Services cards (1 / 2 / 3 col)
- Donation cards
- Final CTA card sizing
- Floating donate position and font-size

## Step 13 — Accessibility pass

- All images have alt text matching `index.html` (none use em-dashes).
- Focus indicators visible on every interactive element.
- FAQ accordion uses `aria-expanded`, `aria-controls` correctly.
- Hamburger uses `aria-expanded`, `aria-controls`, `aria-label`.
- Heading hierarchy: H1 → H2 → H3, no skips.
- `prefers-reduced-motion` honored — Webflow doesn't always emit this; add custom code embed with the global `@media (prefers-reduced-motion: reduce)` rule from `base.css:25-32`.

## Step 14 — Final sign-off

- Webflow staging URL matches local build at all breakpoints.
- All interactions verified working.
- Accessibility checks pass.
- User reviews, signs off.
- **Gate to advance:** user confirms parity → publish to production domain.

## Step 15 — Post-launch

- Disable Netlify deployment (or keep as backup).
- Remove the `.gitignore` exclusion of `documents/` IF you want the Webflow site to live alongside its source-of-truth docs (decision for the team).
- Archive the local-build branch with a tag (e.g., `static-build-final`).
