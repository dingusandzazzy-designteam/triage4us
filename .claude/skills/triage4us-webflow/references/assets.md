# Assets Inventory

Every image + icon used in the local build. Upload to Webflow Assets in Phase 6 Step 7 using `asset_tool` (Webflow MCP).

---

## Images — `assets/images/` (12 files, all PNG)

| File | Used in | Alt text | Loading | Notes |
|---|---|---|---|---|
| `hero.png` | `#hero` `.hero_backdrop` | "Single mom nurse spending time with her child before work" | eager + `fetchpriority="high"` + preload | LCP image. Aspect 4:3 (1600×1200). |
| `og-card.png` | `<meta property="og:image">` + `<meta name="twitter:image">` | n/a (social) | n/a | Social share card. Aspect 1.91:1 typical. |
| `reality-portrait.png` | `#the-reality` 4th stat card `.stat_card--photo` | "A single mom nurse at home: a moment of quiet strength" | lazy | The "featured wider" stat card photo. NOT decorative — has alt. |
| `service-1-childcare.png` | `#our-mission` services_card 1 | "Childcare support for healthcare workers and nurses" | lazy | Aspect 3:4 (portrait). |
| `service-2-tutoring.png` | services_card 2 | "Student receiving tutoring support through Triage4US" | lazy | 3:4 |
| `service-3-meals.png` | services_card 3 | "Healthy meal support for nurse families" | lazy | 3:4 |
| `service-4-wellness.png` | services_card 4 | "Nurse family wellness and emotional support resources" | lazy | 3:4 |
| `service-5-activity.png` | services_card 5 | "Children participating in community activities and sports" | lazy | 3:4 |
| `service-6-future-readiness.png` | services_card 6 | "Mentorship and future readiness support for children" | lazy | 3:4 |
| `why-it-matters.png` | `#why-it-matters` `.why_image` | "A single mom nurse and her family supporting each other at home" | lazy | Split-layout image. |
| `final-cta.png` | (legacy — replaced by final-cta-2.png) | n/a | n/a | Keep in assets for fallback; can be deleted pre-Webflow upload. |
| `final-cta-2.png` | `#final-cta` `.final-cta_backdrop` | `alt=""` (decorative — heading carries the content) | lazy | Aspect 3:2 (1800×1200). Subject in right third, lower-left negative space for the gradient + white text overlay. |

### Upload order

1. `hero.png` first (LCP — also needed for the head preload tag).
2. `final-cta-2.png` (large, page-finale image).
3. All 6 service images.
4. `reality-portrait.png` + `why-it-matters.png`.
5. `og-card.png` (social share — connect to page-level SEO settings, not the body).

### Pre-upload optimization (recommended)

The motion audit (impeccable) flagged WebP/AVIF conversion as P2 not-done. Before uploading to Webflow:

1. Convert each PNG → AVIF (smallest, modern browsers) + WebP (universal fallback).
2. Tools: `cwebp` (CLI), `sharp` (Node), or any online converter like Squoosh.
3. Webflow accepts WebP and AVIF uploads as of 2024.
4. If converting, upload BOTH formats and use Webflow's auto-selection (or a `<picture>` element via custom code embed).

Target file sizes:
- `hero.png` — currently ~1.2-1.8MB PNG. Target: ~120-200KB AVIF or 300-400KB WebP.
- Service images — currently ~500KB-1MB each. Target: ~80-150KB AVIF.
- Total page weight after conversion: drop from ~10MB to ~1.5-2.5MB.

### Filename cleanup decision

Open item in handoff: rename `final-cta-2.png` → `final-cta.png` for cleaner Webflow URLs. Decide before upload:

- **If renaming:** delete the legacy `final-cta.png`, rename `final-cta-2.png` to `final-cta.png`, then upload.
- **If keeping:** upload `final-cta-2.png` as-is. The Webflow asset URL will carry the `-2` suffix.

---

## Icons — `assets/icons/` (27 SVG, Lucide style)

27 Lucide-style SVG icons. **NOT ALL are used in the live build** — the original build referenced some that got removed during iteration. Audit which are actually rendered before uploading.

| File | Likely use | Status |
|---|---|---|
| `arrow-right.svg` | Inline in services links / CTAs | Check usage |
| `arrow-up-right.svg` | External link indicator | Check usage |
| `car.svg` | Service icon (transportation?) | Check usage |
| `chart-bar.svg` | Stat widget | Check usage |
| `chevron-down.svg` | FAQ trigger / dropdown | Likely yes (FAQ icon replacement?) |
| `circle-arrow-right.svg` | Decorative CTA arrow | Check usage |
| `circle-dollar-sign.svg` | Donation icon | Check usage |
| `circle-x.svg` | Close button (modals?) | Check usage |
| `clipboard-check.svg` | Trust indicator | Check usage |
| `credit-card.svg` | Donation icon | Check usage |
| `crown.svg` | Premium tier marker | Check usage |
| `file-check.svg` | Verification badge | Check usage |
| `hand-coins.svg` | Donation icon | Check usage |
| `handshake.svg` | Partnership icon (Care.com)? | Check usage |
| `info.svg` | Tooltip / disclosure | Check usage |
| `landmark.svg` | Nonprofit / institution | Check usage |
| `linkedin.svg` | Social link | Likely footer |
| `mail.svg` | Contact icon | Likely footer |
| `medal.svg` | Recognition / award | Check usage |
| `menu.svg` | Hamburger icon | NOT USED — local build uses CSS bars |
| `phone.svg` | Contact icon | Check usage |
| `qr-code.svg` | Donation QR (mobile)? | Check usage |
| `shield-check.svg` | Trust / safety | Check usage |
| `target.svg` | Mission / goal | Check usage |
| `trending-up.svg` | Stat / growth | Check usage |
| `user-round.svg` | Profile | Check usage |
| `users.svg` | Community / nurses | Check usage |
| `zap.svg` | Speed / urgency | Check usage |

### Action before upload

Grep the local `index.html` for icon references:

```bash
grep -o 'assets/icons/[a-z-]*\.svg' index.html | sort -u
```

Upload ONLY the icons that grep returns. The unused SVGs stay in the local repo for future Webflow Component expansion (or for the Webflow site asset library as a reserve set).

### How to render in Webflow

Two options per icon:

1. **Webflow Asset (Image element):** simplest. Upload as SVG, drop as `<img>` in the design. Cannot recolor via CSS.
2. **Inline SVG via Embed:** paste the SVG markup into an Embed element. Allows `fill: currentColor` for theming.

For the heart icon in `.floating-donate__icon` — this is INLINE SVG, not from `/icons/`. It's a Heroicons "heart fill" with `viewBox="0 0 20 20"`. Preserve as embed code (already in `index.html:550-553`).

---

## Inventory checklist

- [ ] Confirm which icons are actually used in the live `index.html` (grep).
- [ ] Decide: convert PNGs to WebP/AVIF before upload? (Recommended; needs cwebp or sharp.)
- [ ] Decide: rename `final-cta-2.png` to `final-cta.png`?
- [ ] Upload images via `asset_tool` in Phase 6 Step 7.
- [ ] Capture Webflow asset URL for `hero.png` and inject into the head preload tag.
- [ ] Update `og:image` and `twitter:image` meta tags to Webflow URLs.
- [ ] Verify alt text for every uploaded image matches `index.html`.
- [ ] Verify the decorative `.final-cta_backdrop` has empty alt (`alt=""`) since the H2 carries the content.
