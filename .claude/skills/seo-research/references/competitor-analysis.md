# Competitor Analysis

> The first observable signal in any SEO project. What's already ranking tells you the niche's vocabulary, page-type expectations, and schema baseline. The goal is **not** to copy competitors — it's to know what the SERP rewards.

## Direct vs indirect competitors

| Type | Definition | Use |
|---|---|---|
| **Direct** | Same product/service, same audience, same geo. Will show up in the same SERPs you target. | Primary source — analyze 5–8. |
| **Adjacent** | Same audience, different angle (e.g., a content site in the same niche; a tool that solves a subset). | Secondary source — analyze 1–2 for vocabulary expansion. |
| **Indirect** | Different solution to the same problem (e.g., a SaaS competing with an in-house build). | Skip unless the audience seriously evaluates them — too noisy. |

Identify direct first. If the project has <3 direct competitors visible, the niche is either too narrow (good — low competition) or too vague (bad — keyword pool will be thin).

## Discovery method (when no competitors are supplied)

1. Web-search the niche's most likely seed term + audience + geo. Example: *"embedded credit platform B2B Canada"*.
2. Capture top 10 organic results. Discard aggregators (Capterra, G2, Wikipedia) on the first pass — useful for vocabulary, not for direct-competitor analysis.
3. Repeat with 2–3 variant seeds (different USP framings).
4. Take the union. Dedupe by domain. You should now have 5–10 direct candidates.
5. Log the exact search queries used. They go into `seo_research_report.md`.

## Which pages to inspect per competitor

Pick 3–8 high-signal pages per competitor. Priority:

1. **Homepage** — top-of-funnel vocabulary, headline strategy, primary keyword for the brand itself.
2. **Pricing** — commercial-intent keywords, comparison framing.
3. **Primary product / service page** — keyword the brand pins as its core offering.
4. **Comparison or alternatives pages** ("vs", "alternatives to") — commercial keywords and competitor-brand modifiers.
5. **Top blog posts** (only if they rank organically for niche seeds) — informational keyword targets.
6. **Solutions / use cases / industries pages** — long-tail commercial keywords.

Skip: blog tag pages, author pages, generic "About" pages unless they carry SEO weight.

## What to extract

Per page:

| Field | Why |
|---|---|
| URL | Traceability. |
| `<title>` | Primary keyword target + brand suffix pattern. |
| `<meta name="description">` | Value-prop framing, CTA language. |
| H1 | Primary keyword expressed for humans. May differ from `<title>`. |
| H2s (top 5) | Sub-topic clusters, secondary keyword targets. |
| H3s (top 5) | Granular intent signals. |
| Schema.org JSON-LD `@type` | What schema the competitor implements (`Organization`, `Product`, `FAQPage`, `Article`, etc.). |
| Breadcrumb structure | Information architecture clues. |

Run `scripts/analyze_competitors.py` to automate this. The script respects `robots.txt`, throttles at 2-second intervals, and falls back gracefully on broken URLs.

## Inferring SEO strategy from observable surface

Look for these patterns across competitors:

- **Cluster topics** — same domain has a hub page (broad keyword) plus 5–20 spoke pages (long-tail variations) linking back. Indicates a topical-authority strategy.
- **Title patterns** — `[Primary KW] | [Brand]` vs `[Brand] | [Tagline]`. The first is SEO-aggressive; the second is brand-driven (often consumer brands).
- **Schema density** — heavy `FAQPage` schema = aiming for PAA / FAQ snippets. `Product` + `AggregateRating` = chasing rich-result eligibility.
- **Anchor patterns** in internal linking — repeated anchor text across pages signals the keyword they're consolidating authority around.
- **Meta-description CTA language** — "Get started free," "Book a demo," "See pricing." Tells you the commercial intent the page is built for.

Document patterns per competitor in 1–2 sentences. Not a doctoral thesis.

## Rate limiting and ethics

- **2 seconds minimum between requests** per competitor (script enforces). Many sites have light WAFs that flag faster scraping.
- **Respect `robots.txt`.** The script reads it via `urllib.robotparser`. If a path is disallowed, skip it; surface it in the report.
- **No login-required content.** No "scrape behind paywall" tricks. Public surface only.
- **No mass paginated scraping.** This is per-page analysis, not site-wide crawling.
- **No competitive intelligence outside SEO.** Don't fetch their analytics, ad spend, employee directories, etc. Out of scope.

If a competitor's site blocks the script (403, 429, CAPTCHA challenge), note it as `BLOCKED` and move on. Don't escalate evasion tactics.

## Output format

After Phase 2 ends, the report should contain a table like:

| Competitor | URL inspected | Title pattern | Primary KW inferred | Schema observed | Notes |
|---|---|---|---|---|---|
| ExampleCo | example.com | `[KW] \| ExampleCo` | "embedded credit platform" | `Organization`, `FAQPage` | Heavy cluster on "[X] integration" |
| RivalCo | rival.com/pricing | `RivalCo \| [Tagline]` | "B2B fintech pricing" | `Product`, `Offer` | Brand-driven titles, weaker organic |

Plus a flat list of **niche vocabulary baseline** — every term that appeared in ≥2 competitors' titles or H1s. This list feeds directly into Phase 3.
