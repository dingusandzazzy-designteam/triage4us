# Components

Reusable elements built as Webflow Components. Each spec includes class name, structure, style notes, and which Variables to bind.

---

## Layout primitives (build first)

### `padding-global`

Wrapper that applies page inline padding. Always pair with a `container-*` inside.

- Tag: `div`
- Style: `padding-inline: var(--page-padding-inline)` → bind to `page-padding-inline` Variable.
- No max-width on this element — it spans the section.

### `container-large` / `container-medium` / `container-small`

- Tag: `div`
- Style: `width: 100%; max-width: var(--container-*); margin-inline: auto;`
- Bind max-width to the corresponding `container-large` / `container-medium` / `container-small` Variable.

### `padding-section-small/medium/large/huge`

These are utility classes, NOT components. Apply directly to section content blocks:

- `padding-section-small` → `padding-block: var(--section-padding-small)`
- `padding-section-medium` → `padding-block: var(--section-padding-medium)`
- `padding-section-large` → `padding-block: var(--section-padding-large)`
- `padding-section-huge` → `padding-block: var(--section-padding-huge)`

---

## Buttons (Webflow Component: `button`)

Base class `.button` with combo classes `.is-primary`, `.is-secondary`, `.is-tertiary`, `.is-on-dark`.

### Base `.button`

```
Tag: anchor (default) or button
Display: inline-flex
Align-items: center, justify-content: center
Gap: var(--space-2)  → 8px
Padding: var(--space-4) var(--space-6)  → 16px 32px (vertical horizontal)
Font: var(--fs-body), var(--fw-bold), line-height: 1
Border-radius: var(--radius-button)  → 999px
Transition: background-color, color, transform — all var(--duration-base) var(--ease-out-soft)
White-space: nowrap
```

### `.is-primary` combo

```
Background-color: var(--color-cta-primary)  → #016847
Color: var(--color-text-on-dark)  → white
:hover {
  background-color: var(--color-cta-primary-hover)  → #014f37
  transform: translateY(-1px)
}
```

### `.is-secondary` combo

```
Background-color: transparent
Color: var(--color-text-primary)
Box-shadow: inset 0 0 0 1.5px var(--color-text-primary)  (Webflow: use border 1.5px + transparent inset)
:hover {
  background-color: var(--color-text-primary)
  color: var(--color-text-on-dark)
}
```

### `.is-tertiary` combo

```
Background: transparent
Color: var(--color-cta-primary)
:hover { text-decoration: underline }
```

### `.is-on-dark` combo

Used over the hero photo and the final-CTA dark gradient. White outlined pill.

```
Background-color: transparent
Color: var(--color-white)
Border: 1.5px solid rgba(255, 255, 255, 0.7)
:hover {
  background-color: var(--color-white)
  color: var(--color-text-primary)
}
```

### Global `.button:active` (apply to all buttons)

```
:active {
  transform: scale(0.97)
  transition-duration: var(--duration-fast)
}
```

Webflow Interaction: trigger on mouse down → scale 0.97, on mouse up → scale 1. Custom-code fallback is the CSS above.

### `.site-header_cta` modifier (touch target)

When `.button.is-primary` is in the header, override padding/font:

```
padding-block: var(--space-4)  → 16px
font-size: var(--fs-body)  → 16px (not the previous small)
```

Total height stays ≥44px for WCAG.

---

## FAQ accordion item (Component: `faq-item`)

```
li.faq_item
├── button.faq_trigger (aria-expanded, aria-controls)
│   ├── span.faq_question
│   └── span.faq_icon (aria-hidden — two lines forming a +)
└── div.faq_panel (role="region", aria-labelledby, id="faq-panel-N")
    └── p.faq_answer
```

### `.faq_item` style

```
Border: 1px solid var(--color-border-soft)
Border-radius: var(--radius-medium)  → 20px
Background-color: var(--color-white)
Overflow: hidden
Transition: border-color var(--duration-base) var(--ease-out-soft)

When the trigger inside is aria-expanded="true":
  Border-color: var(--color-cta-primary)
```

Webflow: use a CSS combo class `.is-expanded` toggled by Interaction since Webflow Style panel can't target `:has(.faq_trigger[aria-expanded="true"])`.

### `.faq_trigger` style

```
Width: 100%
Display: flex
Align-items: center
Justify-content: space-between
Gap: var(--space-4)
Padding: var(--space-5) (24px all around)
Background: transparent
Border: 0
Cursor: pointer
Font: inherit
Text-align: left

:hover { background-color: var(--color-bg-soft) }
```

### `.faq_question`

```
Font-size: var(--fs-body-large)  → 18px
Font-weight: var(--fw-medium)
Color: var(--color-text-deep)
```

### `.faq_icon` (the + / × toggle)

A span with `::before` and `::after` forming two bars.

```
Flex-shrink: 0
Width: 1.5rem  → 24px
Height: 1.5rem
Position: relative

::before {
  position: absolute, top: 50%, left: 50%
  width: 1rem, height: 2px
  background-color: var(--color-cta-primary)
  transform: translate(-50%, -50%)
}

::after {
  position: absolute, top: 50%, left: 50%
  width: 2px, height: 1rem
  background-color: var(--color-cta-primary)
  transform: translate(-50%, -50%)
  transition: transform var(--duration-base) var(--ease-out-soft)
}

When parent .faq_trigger is aria-expanded="true":
  ::after { transform: translate(-50%, -50%) rotate(90deg) }
```

**Webflow note:** pseudo-elements with rotation need custom code embed. Alternative: use two separate `div` lines stacked + an Interaction that rotates the vertical one.

### `.faq_panel` — the modern accordion reveal

```
display: grid
grid-template-rows: 0fr
transition: grid-template-rows 360ms var(--ease-out-soft)

When parent .faq_item has .is-open class:
  grid-template-rows: 1fr
```

This pattern ANIMATES auto-height — `grid-template-rows: 0fr → 1fr` is a modern CSS trick that has no Webflow Interaction equivalent. Use custom code embed for this rule.

### `.faq_answer` (the panel's inner grid item)

```
min-height: 0
overflow: hidden
padding: 0 var(--space-5) 0
color: var(--color-text-muted)
line-height: var(--lh-relaxed)
max-width: 64ch

Initial state:
  opacity: 0
  transform: translateY(-6px)
  filter: blur(2px)
  transition: opacity 280ms, transform 280ms, filter 280ms, padding-bottom 360ms (all ease-out-soft)

When .faq_item has .is-open:
  opacity: 1
  transform: translateY(0)
  filter: blur(0)
  padding-bottom: var(--space-5)
```

---

## Stat card variants (Component: `stat-card`)

All 4 variants share the base + a `--variant` combo class. Bento layout (1fr 1fr 1fr 1.6fr at ≥1024px).

### Base `.stat_card`

```
Position: relative
Display: flex
Flex-direction: column
Gap: var(--space-4)
Border-radius: var(--radius-card)  → 24px
Padding: var(--space-6)  → 32px
Min-height: 22rem
Overflow: hidden
Isolation: isolate
Transition: transform, box-shadow — both var(--duration-base) var(--ease-out-soft)

:hover {
  transform: translateY(-3px)
  box-shadow: var(--shadow-card)
}
```

**Important:** Do NOT differentiate hover per variant. See [feedback_card_hover_consistency.md](../../../../C:/Users/marco/.claude/projects/E--DZ-Triage4US/memory/feedback_card_hover_consistency.md) — uniform translateY(-3px) is the validated treatment.

### Variants

| Combo | Background | Notes |
|---|---|---|
| `.stat_card--metric` | `var(--color-white)` | Border: 1px solid var(--color-border-soft). Big number + label + supporting text. |
| `.stat_card--widget` | `var(--color-white)` | Border 1px. Big number + label + a CSS bar widget. |
| `.stat_card--gradient` | linear-gradient deep-green → deep-teal | Light text (`.stat_card--gradient .stat_number` is white). Includes 2 `.gradient_blob` decorative spans. |
| `.stat_card--photo` | `assets/images/reality-portrait.png` as background + dark overlay | Light text. The "featured" wider card at desktop (1.6fr). |

### Card internals (shared)

```
.stat_pill — eyebrow chip, small uppercase tracked label
.stat_card_body — flex column gap small
.stat_number — clamp 2.75rem → 4rem, fw-bold, lh-tight, color: var(--color-deep-green)
  EXCEPT --gradient and --photo variants: color is white
.stat_label — body text, color: text-deep
.stat_supporting — small text, muted

Stat-number scroll reveal: see interactions.md (animation-timeline: view() custom code)
```

---

## Services card (Component: `services-card`)

6 instances in `#our-mission`. Aspect-ratio 3/4, image-led.

```
.services_card
├── img.services_image (absolute, inset: 0, object-fit: cover)
├── ::after (dark vertical gradient overlay)
└── .services_content (z-index: 2, bottom-anchored)
    ├── h3.heading-style-h3.services_heading (color: white)
    └── p.text-size-small.services_copy (color: rgba(255,255,255,0.88))
```

### `.services_card` base

```
Position: relative
Overflow: hidden
Isolation: isolate
Border-radius: var(--radius-card)
Aspect-ratio: 3 / 4
Display: flex, flex-direction: column, justify-content: flex-end
Background-color: transparent  ← critical, NOT a fallback color (corner-leak issue)
Transition: transform, box-shadow — both var(--duration-base) var(--ease-out-soft)

:hover {
  transform: translateY(-3px)
  box-shadow: var(--shadow-lift)
}
```

### `.services_card .services_image` (specificity bumped)

The `.services_card` qualifier is REQUIRED in the selector. See interactions.md for why.

```
Position: absolute
Inset: 0
Width: 100%, height: 100%
Object-fit: cover
Z-index: 0
Border-radius: inherit  ← critical, keeps corners during GPU-composited scale
Transition: transform 700ms cubic-bezier(0.33, 1, 0.68, 1), opacity 320ms var(--ease-out-soft)

:hover { transform: scale(1.06) }
```

### `.services_card::after` overlay

```
Position: absolute, inset: 0
Background: linear-gradient(180deg,
  rgba(2, 47, 66, 0) 0%,
  rgba(2, 47, 66, 0) 40%,
  rgba(2, 47, 66, 0.55) 70%,
  rgba(2, 47, 66, 0.92) 100%)
Border-radius: inherit  ← critical for corner clip
Z-index: 1
Pointer-events: none
```

### `.services_content`

```
Position: relative
Z-index: 2
Padding: var(--space-6)
Display: flex, flex-direction: column, gap: var(--space-2)
Color: var(--color-white)
```

---

## Donation card (Component: `donation-card`)

4 instances in `#donation-impact`. Action-oriented — keeps the canonical lift.

```
.donation_card
├── .donation_amount (big number)
├── h3.donation_label
└── p.donation_copy
```

Style:

```
Background: var(--color-white)
Border: 1px solid var(--color-border-soft)
Border-radius: var(--radius-card)
Padding: var(--space-6) var(--space-5)
Display: flex, flex-direction: column, gap: var(--space-3)
Text-align: center
Cursor: pointer
Transition: transform, background-color, box-shadow — all var(--duration-base) var(--ease-out-soft)

:hover {
  transform: translateY(-3px)
  background-color: var(--color-soft-blue)
  box-shadow: var(--shadow-card)
}
```

---

## Floating donate (Component: `floating-donate`)

Single instance at the body root, not nested in any section.

```
a.floating-donate (data-visible="false")
├── span.floating-donate__halo
├── span.floating-donate__icon
│   └── svg (Heroicons heart fill)
└── span.floating-donate__label "Donate"
```

### `.floating-donate` base

```
Position: fixed
Bottom: clamp(1rem, 3vw, 1.5rem)
Right: clamp(1rem, 3vw, 1.5rem)
Z-index: 80
Display: inline-flex, align-items: center, gap: 0.625rem
Padding: 0.75rem 1.25rem 0.75rem 0.625rem
Border-radius: var(--radius-button)
Background: var(--color-cta-primary)
Color: var(--color-white)
Font: var(--font-primary), var(--fs-body), var(--fw-bold)
Box-shadow: 0 8px 24px rgba(1, 104, 71, 0.32), 0 2px 6px rgba(0, 0, 0, 0.12)

Initial hidden state:
  transform: translateY(140%)
  opacity: 0
  pointer-events: none
  transition: transform 520ms cubic-bezier(0.33, 1, 0.68, 1), opacity 360ms

When data-visible="true":
  transform: translateY(0)
  opacity: 1
  pointer-events: auto

:hover {
  background: var(--color-cta-primary-hover)
  transform: translateY(-2px)
  box-shadow: 0 12px 32px rgba(1, 104, 71, 0.4), 0 3px 10px rgba(0, 0, 0, 0.15)
}

:active {
  transform: translateY(0) scale(0.97)
  transition-duration: var(--duration-fast)
}
```

### `.floating-donate__icon`

```
Display: inline-flex
Width: 28px, height: 28px
Align-items: center, justify-content: center
Border-radius: 999px
Background: var(--color-accent-bright)  → bright-green
Color: var(--color-cta-primary)  → deep-green for the heart fill
Flex-shrink: 0
```

### `.floating-donate__halo`

The sonar-ping ring. Custom code. See interactions.md.

```
Position: absolute, inset: 0
Border-radius: inherit
Border: 2px solid var(--color-cta-primary)
Pointer-events: none
Opacity: 0  (default)

When parent has data-visible="true" AND prefers-reduced-motion is no-preference:
  animation: floating-donate-halo 3.8s cubic-bezier(0.33, 1, 0.68, 1) infinite
  (keyframes in interactions.md)
```

### Mobile (<480px)

```
Bottom: 0.75rem
Right: 0.75rem
Padding: 0.625rem 1rem 0.625rem 0.5rem
Font-size: var(--fs-small)
Gap: 0.5rem
Icon: 24×24, svg 12×12
```

---

## Header (Component: `site-header`)

Already detailed in section-tree.md. Key styling notes:

- `.site-header` is `position: fixed`, full width, z-index: 50.
- `.site-header.is-over-hero` (default at scroll 0) has transparent bg.
- After scroll past 40px, remove `.is-over-hero` → frosted-white bg `rgba(255,255,255,0.85)` + `backdrop-filter: saturate(140%) blur(12px)` + `border-bottom: 1px solid var(--color-border-soft)`.
- `.site-header_logo` and `.site-header_nav-link` use `--duration-fast` (150ms) for color transitions, not the default `--duration-base`.
- Hamburger morph: see interactions.md.

---

## Footer (Component: `site-footer`)

```
.site-footer
└── .site-footer_inner (flex column < 768, row ≥ 768 with space-between)
    ├── p.site-footer_tagline
    └── p.site-footer_legal
```

Style: small text, muted color, simple layout. Footer year is dynamic — custom code embed.
