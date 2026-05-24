# Section Tree

The full DOM hierarchy of the Triage4US landing page. Each section's Webflow class names follow client-first conventions (already used in the local build — preserve verbatim).

## Page-level wrappers

```
body
└── .page_wrap (div, overflow-x: clip)
    ├── .site-header (HEADER tag)
    ├── main #main
    │   ├── #hero (SECTION)
    │   ├── #the-reality (SECTION)
    │   ├── #our-mission (SECTION)
    │   ├── #why-it-matters (SECTION)
    │   ├── #donation-impact (SECTION)
    │   ├── #final-cta (SECTION)
    │   └── #faq (SECTION)
    └── .site-footer (FOOTER tag)

After </body>:
└── .floating-donate (anchor, position: fixed)
```

The `Skip to main content` link (`.is-visually-hidden`, href="#main") goes at the very top of the body, before `.page_wrap`. Webflow embed it as a custom code block at body start.

---

## 1. `.site-header`

```
.site-header.is-over-hero (header role="banner", position: fixed)
├── .padding-global
│   └── .container-large
│       └── .site-header_inner (flex row, space-between)
│           ├── .site-header_logo (a, href="#hero") — "Triage4US"
│           ├── .site-header_nav (nav, hidden <768px)
│           │   ├── .site-header_nav-link → #our-mission "Our mission"
│           │   ├── .site-header_nav-link → #donation-impact "Donate"
│           │   └── .site-header_nav-link → #faq "FAQ"
│           ├── .site-header_menu-toggle (button, shown <768px)
│           │   └── .hamburger-icon (span, aria-hidden)
│           └── .site-header_cta (a.button.is-primary) → #donation-impact "Donate Today"
└── #mobile-nav (nav.site-header_mobile-nav, data-open="false", drawer below header)
    ├── a → #our-mission "Our mission"
    ├── a → #donation-impact "Donate"
    └── a → #faq "FAQ"
```

States toggled by Webflow Interaction on scroll:
- `.is-over-hero` (default at top, transparent bg)
- Removed past 40px scroll → frosted white bg + border-bottom

Notes:
- `.site-header` is `position: fixed`. Set in Webflow Style panel.
- `.site-header_inner` has `padding-block: var(--space-5)` (24px top/bottom).
- The mobile drawer `#mobile-nav` is a sibling of `.padding-global`, NOT nested inside it — it's `position: fixed` and slides down from top.

---

## 2. `#hero` — `.section_hero`

```
section#hero.section_hero (aria-labelledby="hero-heading")
└── .hero_card (display: flex, align-items: flex-end, border-radius: 40px, overflow: hidden)
    ├── img.hero_backdrop (assets/images/hero.png, position: absolute, inset: 0, object-fit: cover, fetchpriority="high")
    ├── ::after (CSS pseudo, dark dual-gradient overlay)
    └── .hero_content (max-width: 40rem, z-index: 2, bottom-left)
        ├── h1.heading-style-display.hero_heading "Stable Care.<br>Stronger Nurses.<br>Healthier Communities."
        ├── p.text-size-large.hero_subtext "Single mom nurses show up..."
        ├── .hero_cta-wrap (flex)
        │   ├── a.button.is-primary → #donation-impact "Donate Today"
        │   └── a.button.is-on-dark → #our-mission "Support a Nurse Family"
        └── p.text-size-small.hero_trust "Powered by Triage360 in partnership with Care.com"
```

Layout key:
- `.section_hero` is `height: 100svh` exactly. Padding accounts for header offset + inset.
- `.section_hero` background: `var(--color-bg-soft)` (#F7F9FB).
- `.hero_card` is `flex: 1, min-height: 0` — fills available space.
- Hero text animations: page-load stagger (see interactions.md).

---

## 3. `#the-reality` — `.section_reality`

```
section#the-reality.section_reality
└── .padding-global
    └── .container-large.padding-section-large
        ├── .reality_intro (text-align: center, max-width: container-medium)
        │   ├── h2.heading-style-h2 #reality-heading "Behind every shift is a family depending on them."
        │   └── p.text-size-large.text-color-muted.reality_intro-copy "Nurses work long hours..."
        └── ul.reality_stats-grid (role="list", bento grid)
            ├── li.stat_card.stat_card--metric (78% women)
            ├── li.stat_card.stat_card--widget (40% mothers + bar widget)
            ├── li.stat_card.stat_card--gradient (gradient bg + blobs)
            └── li.stat_card.stat_card--photo (full-bleed photo of reality-portrait.png)
```

Grid:
- `<640px`: 1 column
- `≥640px`: `repeat(2, 1fr)`
- `≥1024px`: `1fr 1fr 1fr 1.6fr` (last card is featured wider)

Background: `var(--color-bg-soft)` (#F7F9FB).

See [components.md](components.md) for each card variant's internal structure.

---

## 4. `#our-mission` — `.section_mission`

```
section#our-mission.section_mission
└── .padding-global
    └── .container-large.padding-section-large
        ├── .mission_intro
        │   ├── h2.heading-style-h2 #mission-heading "How we help"
        │   └── p.text-size-large.text-color-muted.mission_intro-copy "..."
        └── ul.services_grid (role="list")
            ├── li.services_card × 6
            │   (1) On-Demand Childcare — service-1-childcare.png
            │   (2) Homework & Tutoring Support — service-2-tutoring.png
            │   (3) Meal & Nutrition Assistance — service-3-meals.png
            │   (4) Wellness & Mentorship — service-4-wellness.png
            │   (5) Sports & Activity Support — service-5-activity.png
            │   (6) Future Readiness Programs — service-6-future-readiness.png
```

Grid:
- `<640px`: 1 column
- `≥640px`: 2 columns
- `≥960px`: 3 columns

Background: `var(--color-bg-page)` (#FFFFFF).

Each `.services_card` aspect-ratio 3/4, full-bleed image + dark gradient overlay + bottom-anchored text. See components.md.

---

## 5. `#why-it-matters` — `.section_why`

```
section#why-it-matters.section_why
└── .padding-global
    └── .container-large.padding-section-large
        └── .why_layout (split layout)
            ├── img (assets/images/why-it-matters.png, why_image)
            └── .why_content
                ├── h2.heading-style-h2 #why-heading "..."
                ├── p.text-size-large.text-color-muted "..."
                ├── .why_quote (blockquote w/ left accent border)
                │   ├── p (the quote)
                │   └── cite
                └── ... (additional paragraphs as needed)
```

Background: `var(--color-bg-page)`.

Image is the locked photographic asset (no zoom/hover, this is a portrait moment).

---

## 6. `#donation-impact` — `.section_donation`

```
section#donation-impact.section_donation
└── .padding-global
    └── .container-large.padding-section-large
        ├── .donation_intro (centered)
        │   ├── h2.heading-style-h2 #donation-heading "..."
        │   └── p.text-size-large.text-color-muted "..."
        ├── ul.donation_grid (role="list", 4 columns at desktop)
        │   └── li.donation_card × 4 (each is cursor: pointer, hover lift -3px + bg-soft tint)
        │       ├── .donation_amount (big number)
        │       ├── h3.donation_label
        │       └── p.donation_copy
        └── .donation_cta (centered CTA below grid)
            └── a.button.is-primary → external "Donate Today"
```

Background: `var(--color-bg-page)`.

This is the **action section** — the donation cards keep their `translateY(-3px)` hover (preserved by user decision after motion audit).

---

## 7. `#final-cta` — `.section_final-cta`

```
section#final-cta.section_final-cta
└── .padding-global
    └── .container-large
        └── .final-cta_card (border-radius: 40px, overflow: hidden, isolation: isolate)
            ├── img.final-cta_backdrop (assets/images/final-cta-2.png, position: absolute, inset: 0)
            ├── ::before (CSS pseudo — @property sheen drift, z-index: 2)
            ├── ::after (CSS pseudo — dark dual-gradient overlay, z-index: 1)
            └── .final-cta_content (z-index: 3, bottom-left)
                ├── span.final-cta_pill "Join the movement"
                ├── h2.heading-style-display.final-cta_heading "Together, we can cover what matters."
                ├── p.text-size-large.final-cta_copy "..."
                └── .final-cta_cta-wrap
                    ├── a.button.is-primary → #donation-impact "Donate Today"
                    └── a.button.is-on-dark → #our-mission "Become a Partner"
```

Background: `var(--color-bg-page)` (#FFFFFF).

Card sizing: `min-height: clamp(28rem, 60svh, 34rem)`.

The `::before` sheen drift is custom CSS code (@property + keyframes). See interactions.md.

---

## 8. `#faq` — `.section_faq`

```
section#faq.section_faq
└── .padding-global
    └── .container-medium.padding-section-large
        ├── h2.heading-style-h2.faq_heading #faq-heading "Frequently asked questions"
        └── ul.faq_list (role="list")
            └── li.faq_item × 4
                ├── button.faq_trigger (aria-expanded, aria-controls)
                │   ├── span.faq_question
                │   └── span.faq_icon (aria-hidden, ::before + ::after lines form a +)
                └── div.faq_panel (id=faq-panel-N, role="region", aria-labelledby)
                    └── p.faq_answer (text)
```

The 4 FAQ items (preserve copy from `index.html`):
1. "What is Triage4US?"
2. "Who does Triage4US support?"
3. "How do donations help nurse families?"
4. "Can organizations partner with Triage4US?"

Background: `var(--color-bg-page)`.

FAQ panel reveal is grid-template-rows 0fr→1fr — custom code. See interactions.md.

---

## 9. `.site-footer`

```
footer.site-footer (role="contentinfo")
└── .padding-global
    └── .container-large.padding-section-medium
        └── .site-footer_inner (column <768px, row ≥768px)
            ├── p.site-footer_tagline "Powered by Triage360 in partnership with Care.com."
            └── p.site-footer_legal "© <span id='year'>2026</span> Triage4US. All rights reserved."
```

Dynamic year: custom code embed (`document.getElementById('year').textContent = new Date().getFullYear()`).

---

## 10. `.floating-donate`

```
a.floating-donate (data-visible="false", position: fixed, bottom-right)
├── span.floating-donate__halo (aria-hidden, sonar-ping ring)
├── span.floating-donate__icon (aria-hidden, bright-green circle bg)
│   └── svg (Heroicons heart fill, viewBox 20×20)
└── span.floating-donate__label "Donate"
```

Placement: `position: fixed`, `bottom: clamp(1rem, 3vw, 1.5rem)`, `right: clamp(1rem, 3vw, 1.5rem)`, `z-index: 80`.

Visibility: data-visible toggled by IntersectionObserver on `.section_hero`. Reproduce as Webflow Interaction or custom code (see interactions.md).
