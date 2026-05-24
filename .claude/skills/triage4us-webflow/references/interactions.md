# Interactions

Every motion, hover state, and JS-driven behavior in the local build, with a "Webflow strategy" for each: native Interaction, custom code embed, or hybrid.

## Decision rule

For each interaction, prefer in this order:

1. **Webflow native Interaction** if the effect uses only `transform`, `opacity`, `color`, `background`, `box-shadow`, `display`, `width`, `height`, and timing/easing within Webflow's UI.
2. **Webflow Interaction + a single class toggle** if the effect needs state coordination (e.g., `aria-expanded` ⇄ a visual class).
3. **Custom code embed** when the effect uses any of: `grid-template-rows: 0fr → 1fr`, `@property`, `animation-timeline: view()`, `mix-blend-mode`, `clip-path` animation, `filter: blur()` transitions, or pseudo-element animation. These are the local build's modern-CSS moments — Webflow Interactions can't express them.

---

## 1. Header — transparent over hero, frosted on scroll

**Effect:** `.site-header` starts transparent over the hero. When scroll > 40px, gains white-frosted bg + bottom border.

**Local build:** `scripts/main.js:19-40` toggles `.is-over-hero` class. CSS handles the visual.

**Webflow strategy:** Native Interaction.

- Trigger: page scroll, threshold 40px.
- Action set 1 (scroll > 40px): remove class `is-over-hero` from `.site-header`.
- Action set 2 (scroll ≤ 40px): add class `is-over-hero`.

Style up both states in the Style panel — transparent (with `is-over-hero`) and frosted (without).

---

## 2. Mobile hamburger toggle

**Effect:** Hamburger button click → mobile drawer slides down from top, hamburger icon morphs into an X.

**Local build:** `scripts/main.js:43-67`. Toggles `aria-expanded` on the button and `data-open` on the drawer.

**Webflow strategy:** Native Interaction + custom code for the morph keyframes.

- Element: `.site-header_menu-toggle`
- Trigger: click
- State A → B: toggle `data-open` attribute on `#mobile-nav` between "false" and "true"
- State A → B: toggle `aria-expanded` between "false" and "true" on the button
- Drawer CSS handles the slide via `transform: translateY(-110% → 0)` with 250ms transition

The hamburger icon morph (three lines → X) uses CSS `::before` and `::after` rotations. Webflow Interactions can't target pseudo-elements with CSS — embed as custom code.

```html
<style>
/* hamburger morph — paste in head custom code or component-scoped embed */
.site-header_menu-toggle[aria-expanded="true"] .hamburger-icon { background-color: transparent; }
.site-header_menu-toggle[aria-expanded="true"] .hamburger-icon::before { transform: translateY(7px) rotate(45deg); }
.site-header_menu-toggle[aria-expanded="true"] .hamburger-icon::after { transform: translateY(-7px) rotate(-45deg); }
</style>
```

The ESC-to-close + click-outside-link-to-close need a small JS embed:

```html
<script>
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    var toggle = document.querySelector('.site-header_menu-toggle[aria-expanded="true"]');
    if (toggle) toggle.click();
  }
});
document.querySelectorAll('#mobile-nav a').forEach(function(a) {
  a.addEventListener('click', function() {
    var toggle = document.querySelector('.site-header_menu-toggle');
    if (toggle && toggle.getAttribute('aria-expanded') === 'true') toggle.click();
  });
});
</script>
```

---

## 3. FAQ accordion expansion

**Effect:** Click trigger → panel reveals with `grid-template-rows: 0fr → 1fr` + inner answer fades in with `opacity + translateY(-6px → 0) + blur(2px → 0)`.

**Local build:** `scripts/main.js:42-79` toggles `aria-expanded` + `.is-open` class on `.faq_panel`.

**Webflow strategy:** Native Interaction for state toggle + custom code for the grid transition.

- Webflow Interaction on `.faq_trigger` click:
  - Toggle `aria-expanded` between "false" / "true" on self.
  - Toggle `.is-open` class on the next sibling `.faq_panel`.
- Single-open behavior (only one panel open at a time): Webflow Interactions don't natively support "close others" — add a small custom code snippet:

```html
<script>
document.querySelectorAll('.faq_trigger').forEach(function(trigger) {
  trigger.addEventListener('click', function() {
    var others = document.querySelectorAll('.faq_trigger');
    others.forEach(function(other) {
      if (other !== trigger && other.getAttribute('aria-expanded') === 'true') {
        other.click();
      }
    });
  });
});
</script>
```

- CSS for grid-template-rows transition (custom code):

```html
<style>
.faq_panel {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 360ms cubic-bezier(0.22, 1, 0.36, 1);
}
.faq_panel.is-open { grid-template-rows: 1fr; }

.faq_answer {
  min-height: 0;
  overflow: hidden;
  opacity: 0;
  transform: translateY(-6px);
  filter: blur(2px);
  transition:
    opacity 280ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 280ms cubic-bezier(0.22, 1, 0.36, 1),
    filter 280ms cubic-bezier(0.22, 1, 0.36, 1),
    padding-bottom 360ms cubic-bezier(0.22, 1, 0.36, 1);
}
.faq_panel.is-open .faq_answer {
  opacity: 1;
  transform: translateY(0);
  filter: blur(0);
  padding-bottom: 1.5rem; /* var(--space-5) */
}
</style>
```

---

## 4. Hero page-load orchestration

**Effect:** When the page loads, hero heading → subtext → CTA-wrap → trust line stagger-in with `opacity + translateY(12px → 0) + blur(4px → 0)` over 700ms, delayed 120/260/400/540ms respectively.

**Local build:** CSS `@keyframes hero-element-enter` in `main.css`, gated by `prefers-reduced-motion: no-preference`.

**Webflow strategy:** Custom code embed (cleaner) OR 4 native Interactions on Page Load (more setup).

Recommended: custom code, because Webflow's load Interaction doesn't fluidly support the `filter: blur()` transition.

```html
<style>
@media (prefers-reduced-motion: no-preference) {
  @keyframes hero-element-enter {
    from { opacity: 0; transform: translateY(12px); filter: blur(4px); }
    to   { opacity: 1; transform: translateY(0); filter: blur(0); }
  }
  .hero_heading  { animation: hero-element-enter 700ms cubic-bezier(0.22, 1, 0.36, 1) 120ms backwards; }
  .hero_subtext  { animation: hero-element-enter 700ms cubic-bezier(0.22, 1, 0.36, 1) 260ms backwards; }
  .hero_cta-wrap { animation: hero-element-enter 700ms cubic-bezier(0.22, 1, 0.36, 1) 400ms backwards; }
  .hero_trust    { animation: hero-element-enter 700ms cubic-bezier(0.22, 1, 0.36, 1) 540ms backwards; }
}
</style>
```

`animation-fill-mode: backwards` keeps elements invisible during their delay (no flash-then-fade).

---

## 5. Below-fold image fade-in on load event

**Effect:** Every `<img loading="lazy">` starts at `opacity: 0` and fades to 1 over 320ms once decoded.

**Local build:** `scripts/main.js:42-58` adds `.is-loaded` class. CSS handles the transition.

**Webflow strategy:** Custom code embed (lightweight).

```html
<style>
@media (prefers-reduced-motion: no-preference) {
  img[loading="lazy"] {
    opacity: 0;
    transition: opacity 320ms cubic-bezier(0.22, 1, 0.36, 1);
  }
  img[loading="lazy"].is-loaded { opacity: 1; }
}
</style>
<script>
document.querySelectorAll('img[loading="lazy"]').forEach(function(img) {
  if (img.complete && img.naturalHeight !== 0) {
    img.classList.add('is-loaded');
  } else {
    img.addEventListener('load',  function() { img.classList.add('is-loaded'); }, { once: true });
    img.addEventListener('error', function() { img.classList.add('is-loaded'); }, { once: true });
  }
});
</script>
```

---

## 6. Stat number scroll reveal

**Effect:** As the user scrolls and the stat number enters viewport, it animates from `opacity: 0, translateY(12px), blur(2px)` to its rest state.

**Local build:** CSS `@supports (animation-timeline: view())` + `animation-range: entry 10% entry 60%`.

**Webflow strategy:** Custom code embed (scroll-driven animations are a modern CSS spec; Webflow Interactions use a different scroll model and don't reproduce this cleanly).

```html
<style>
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    @keyframes stat-reveal {
      from { opacity: 0; transform: translateY(12px); filter: blur(2px); }
      to   { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    .stat_number {
      animation: stat-reveal linear both;
      animation-timeline: view();
      animation-range: entry 10% entry 60%;
    }
  }
}
</style>
```

The `@supports` gate means older browsers (Firefox without flag, Safari pre-26) simply render the static number. No fallback work needed.

---

## 7. Final-CTA gradient sheen drift

**Effect:** A slow, ambient bright-green sheen drifts horizontally across the final-CTA card every 22s, using `@property --sheen-x` for percentage interpolation + `mix-blend-mode: soft-light`.

**Local build:** CSS `@property` + keyframes on `.final-cta_card::before`.

**Webflow strategy:** Custom code embed only. `@property` and `mix-blend-mode` can't be expressed in Webflow Interactions.

```html
<style>
@property --sheen-x {
  syntax: "<percentage>";
  inherits: false;
  initial-value: -20%;
}

.final-cta_card::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 2;
  background: radial-gradient(
    ellipse 50% 70% at var(--sheen-x, -20%) 40%,
    rgba(0, 196, 76, 0.22) 0%,
    transparent 55%
  );
  pointer-events: none;
  mix-blend-mode: soft-light;
}

@media (prefers-reduced-motion: no-preference) {
  @keyframes sheen-drift {
    from { --sheen-x: -20%; }
    to   { --sheen-x: 120%; }
  }
  .final-cta_card::before {
    animation: sheen-drift 22s linear infinite alternate;
  }
}
</style>
```

**Important:** the `.final-cta_card` needs `position: relative` and `isolation: isolate` (already in its base style) for the pseudo to anchor correctly and the blend mode to scope to the card.

---

## 8. Services card image zoom (photo breathing)

**Effect:** Card hover → card lifts `translateY(-3px)` in 250ms. Image inside scales 1 → 1.06 in 700ms with `cubic-bezier(0.33, 1, 0.68, 1)`. Layered timing creates a "photo breathing" feel.

**Local build:** CSS hover rules.

**Webflow strategy:** Native Interaction (mouse over / out on `.services_card`).

- Mouse over → card transform translateY -3px (250ms ease-out-soft), image scale 1.06 (700ms ease-out-quart).
- Mouse out → reverse both at the same durations.

**Critical:** the image element's CSS must also include:
- `border-radius: inherit` (corners survive GPU-composited scale)
- specificity bumped via `.services_card .services_image` selector (otherwise the lazy-load opacity rule clobbers the transform transition due to specificity)
- card background-color MUST be `transparent` (not a fallback color) — eliminates corner sliver leak during scale

If Webflow's native Interaction won't honor `border-radius: inherit`, fall back to custom code:

```html
<style>
.services_card .services_image {
  border-radius: inherit;
  transition:
    transform 700ms cubic-bezier(0.33, 1, 0.68, 1),
    opacity 320ms cubic-bezier(0.22, 1, 0.36, 1);
}
.services_card:hover .services_image { transform: scale(1.06); }
.services_card::after { border-radius: inherit; }
.services_card { background-color: transparent; }
</style>
```

---

## 9. Button hover + active

**Hover** (`.button.is-primary:hover` translateY -1px + bg darker): Webflow native Interaction (mouse over/out).

**Active** (any `.button:active` scale 0.97): Webflow native Interaction (mouse down/up) with 120ms duration.

Card-level hovers (`.stat_card`, `.services_card`, `.donation_card`) all use uniform `translateY(-3px)` — preserve this. Do NOT differentiate per card type. See [feedback memory](../../../../C:/Users/marco/.claude/projects/E--DZ-Triage4US/memory/feedback_card_hover_consistency.md).

---

## 10. Smooth scroll for in-page anchors

**Effect:** Anchor links (`<a href="#section">`) scroll smoothly to target. Reduced-motion users get instant jump. Keyboard users get focus moved to the target.

**Local build:** `scripts/main.js:104-122`.

**Webflow strategy:** Built-in. Webflow's anchor links have smooth scroll by default. The reduced-motion fallback is honored if the user has it enabled at the OS level (Webflow respects `scroll-behavior: smooth` + `@media (prefers-reduced-motion)` from custom code in `base.css`).

Add this to the head custom code if Webflow's default doesn't include it:

```html
<style>
html { scroll-behavior: smooth; scroll-padding-top: 5rem; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
```

---

## 11. Floating donate CTA visibility + halo

**Effect:** Hidden while hero is in view. Slides up + fades in when hero leaves viewport. Sonar-ping halo loops while visible.

**Local build:** `scripts/main.js` IntersectionObserver on `.section_hero` + CSS animation.

**Webflow strategy:** Native Interaction (Scroll Out trigger on the hero section) + custom code for the halo.

- Webflow Interaction on `.section_hero`:
  - Trigger: scroll out of view (top of viewport).
  - Action: set `data-visible="true"` on `.floating-donate`.
  - Reverse trigger (scroll back into view): set `data-visible="false"`.

Custom code for the halo:

```html
<style>
@media (prefers-reduced-motion: no-preference) {
  @keyframes floating-donate-halo {
    0%   { transform: scale(1);    opacity: 0.55; border-width: 2px; }
    60%  { transform: scale(1.35); opacity: 0;    border-width: 1px; }
    100% { transform: scale(1.35); opacity: 0;    border-width: 1px; }
  }
  .floating-donate[data-visible="true"] .floating-donate__halo {
    animation: floating-donate-halo 3.8s cubic-bezier(0.33, 1, 0.68, 1) infinite;
  }
}
</style>
```

The 60% / 100% split is intentional — the ring expands and fades over 60% of the 3.8s cycle, then holds invisible for the remaining 40%. This is a "sonar ping" with rest between propagations, NOT a continuous pulse. The audit's anti-checklist permits this as a documented single-brand-element exception.

---

## 12. Reduced-motion global guard

**Effect:** All animations + transitions collapse to ~0ms for users who prefer reduced motion.

**Local build:** `styles/base.css:25-32`.

**Webflow strategy:** Custom code in head. Webflow doesn't automatically emit this guard.

```html
<style>
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
</style>
```

Add this to the page-level head custom code so it covers everything — Webflow Interactions, custom code embeds, and any motion the team adds later.

---

## Summary — what's native vs custom

| Interaction | Webflow approach |
|---|---|
| Header transparent / frosted | Native |
| Mobile hamburger toggle | Native + small custom for ESC/click-outside + pseudo morph |
| FAQ accordion | Native toggle + custom CSS for grid-template-rows + single-open script |
| Hero page-load stagger | Custom CSS (blur transitions) |
| Image fade-in on load | Custom CSS + script |
| Stat number scroll reveal | Custom CSS (animation-timeline) |
| Final-CTA sheen drift | Custom CSS (@property + mix-blend-mode) |
| Services card hover zoom | Native + custom CSS for border-radius inherit |
| Button hover + active | Native |
| Smooth scroll | Built-in |
| Floating donate visibility | Native + custom CSS for halo keyframes |
| Reduced-motion guard | Custom CSS in head |
