# Page Mapping

> The bridge between the prioritized keyword list and the site's information architecture. Get this right and every page has one clear job; get it wrong and pages cannibalize each other in the SERP.

## Principles

### One primary keyword per page

**Hard rule.** Each page targets exactly one primary keyword. Secondary keywords (2–3 allowed) must be near-variations of the primary, not new intents.

Why this is non-negotiable:

- Google picks one URL per query. If two of your URLs target the same primary, it picks one — usually arbitrarily — and the other never recovers.
- Internal linking gets confused when anchor text has to serve two pages.
- Conversion paths fork when the same intent maps to two pages.

### Same intent per page

A page targeting *"best embedded credit platform"* (commercial) cannot also target *"how does embedded credit work"* (informational). The first wants a curated comparison; the second wants an educational guide. Forcing both produces a confused page that ranks for neither.

### Cluster topics

Related secondary keywords can become a *cluster*: one **hub page** (broad primary keyword, MOFU framing) + multiple **spoke pages** (long-tail variations, TOFU/MOFU framing) that internal-link back to the hub. The hub builds topical authority; the spokes capture long-tail traffic.

Only build a cluster if there are ≥3 spoke-worthy long-tail variations *and* the volume / score justifies the effort.

### Every page traces to a keyword

Don't invent pages without keyword backing. If a page exists for brand reasons (About, Team, Press), it doesn't need SEO targeting — leave the SEO Brief minimal and don't compete for SERP. But don't *invent* SEO targets for brand pages either.

## Common structures by project type

### B2B SaaS / fintech

| Page | Intent | Primary KW shape |
|---|---|---|
| Homepage | Branded + broad commercial | `[category] platform` |
| Pricing | Transactional | `[product] pricing`, `[product] cost` |
| Solution / use-case page (1 per audience segment) | Commercial | `[product] for [audience]` |
| Comparison page (1 per major competitor) | Commercial | `[product] vs [competitor]` |
| Industries / verticals (1 per vertical) | Commercial | `[product] for [industry]` |
| Blog hub | Informational (TOFU) | `[category] guide` |
| Demo / contact | Transactional | `[product] demo` |

### E-commerce

| Page | Intent | Primary KW shape |
|---|---|---|
| Homepage | Branded + broad | `[brand]` |
| Category page | Commercial | `[category]`, `best [category]` |
| Product page (1 per SKU) | Transactional | `[product name]`, `buy [product]` |
| Comparison / "alternatives" pages | Commercial | `[product] vs [competitor]` |
| Buying guides | Informational (TOFU) | `how to choose [category]`, `[category] guide` |
| Cart / checkout | Navigational (own) | n/a (no SEO target) |

### Agency / service business

| Page | Intent | Primary KW shape |
|---|---|---|
| Homepage | Branded + broad commercial | `[service] agency` |
| Service pages (1 per service) | Commercial | `[specific service]` |
| Case-study pages | Commercial (proof) | `[service] case study`, `[client industry] [service]` |
| Local landing (1 per geo) | Local commercial | `[service] in [city]` |
| Blog | Informational | mixed |
| Contact | Navigational + transactional | n/a |

### Multi-vertical landing site (e.g., one brand, four audience segments)

| Page | Intent | Primary KW shape |
|---|---|---|
| Brand homepage | Branded | `[brand]` |
| Vertical page (1 per audience) | Commercial | `[product] for [audience]` |
| Cross-vertical comparison or hub | Optional. Use only if there's volume for *"[product] for businesses"*-style queries. |

## Multi-vertical projects

When the project has multiple audience segments, each gets its own page (or sub-site). Rules:

- **Don't merge verticals.** A single page trying to address dealers, venues, and sports teams will rank for none of them.
- **Each vertical's primary keyword is `[product] for [vertical]`** or close to it. Confirm the SERP supports it.
- **Cross-link verticals through the brand's homepage**, not through each other (avoids internal-link cycles that confuse Google's prioritization).
- **Shared content (FAQ, methodology, founder story)** lives in a global / about page. Each vertical links to the shared page once.

## Cannibalization defense

Cannibalization happens when two pages target the same primary keyword (or close variants).

**Detection (during Phase 5):**

- After mapping, sort the Page Map by `Primary keyword`. Duplicates = cannibalization.
- For each primary keyword, ensure secondary keywords don't appear as primary on a different page.

**Resolution:**

- Pick the page that better matches the SERP shape and intent.
- Demote the other page's primary to a secondary on the kept page (or drop entirely).
- If both pages are essential for business reasons, differentiate the keywords (one becomes the hub, the other a spoke with a more specific long-tail primary).

## Secondary keyword rules

A page can carry 2–3 secondary keywords if:

- They share the same intent as the primary.
- They are linguistic variations / synonyms / longer-tail versions.
- They appear in PAA blocks adjacent to the primary's SERP.

A page **cannot** carry secondaries that:

- Are different intents (TOFU + BOFU on same page).
- Are different audiences (would split the page's messaging).
- Have stronger volume than the primary (then they should *be* the primary).

## Page Map output (Phase 5)

Populate the `Page Map` tab with one row per page. Columns:

| Column | Content | Example |
|---|---|---|
| Page name | Human label | "Automotive landing" |
| URL slug | Kebab-case, no trailing slash | `/for-automotive` |
| Page type | `Landing` / `Product` / `Pricing` / `Comparison` / `Blog` / `Hub` / `Spoke` / `Other` | `Landing` |
| Primary keyword | One from prioritized list | `embedded credit for dealerships` |
| Secondary keyword 1–3 | Variations of primary | `dealership credit platform`, `auto F&I credit` |
| Status | `Draft` after Phase 5 | `Draft` |

Cross-check before exiting Phase 5:

- No primary keyword appears on two rows.
- No keyword is a primary on one row and a secondary on another.
- Every `High` priority keyword from Phase 4 is either a primary, a secondary, or explicitly deferred with a note.
