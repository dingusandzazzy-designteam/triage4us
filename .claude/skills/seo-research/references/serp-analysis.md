# SERP Analysis

> The SERP for a keyword is a *binding signal* of what Google believes the searcher wants. Map a landing page to a keyword whose SERP is dominated by blog posts and the page will struggle to rank — not because the page is bad, but because it's the wrong shape. Read the SERP before committing the keyword to a page.

## What a SERP tells you

Per keyword, scan the top 10 organic results plus SERP features:

| Signal | What it means |
|---|---|
| **Top 10 is all blog posts / editorial** | Informational intent. Map to a guide / blog, not a landing page. |
| **Top 10 is all vendor landing / product pages** | Commercial / transactional intent. Map to a landing page. |
| **Top 10 is mixed (vendor + aggregator + blog)** | Ambiguous intent. Use the dominant type as primary signal; consider a hybrid page (long-form landing with educational sections). |
| **Featured snippet** present | One answer dominates. Hard to displace without authority. Aim to be the source it would pull from. |
| **People Also Ask** (PAA) block | Adjacent queries Google has data for. Goldmine for sub-headings and secondary keywords. |
| **Video carousel** | YouTube-first SERP. Text content alone will struggle; consider whether the project ships video. |
| **Image carousel** | Visual intent. Implies the searcher wants to *see*. Text landing page is poor fit. |
| **Local pack / map** | Local intent. National landing pages won't rank without local schema and GBP presence. |
| **Shopping ads** | Product purchase intent. B2B landing pages won't compete here. |
| **Many text ads (≥4)** | High commercial competition. Organic is uphill but the volume is real. |
| **Zero ads** | Low commercial value or very specific. Investigate before deprioritizing — might be high-quality informational. |

## SERP shape vs page type — the mismatch test

For each `High` priority keyword, before mapping to a page:

1. Run `scripts/serp_inspect.py <kw>` (or do it manually in a fresh incognito browser).
2. Look at the top 10 page types.
3. Match against your intended page type for the keyword.
4. If they disagree (e.g., you want a landing page, SERP shows blog posts), do **one** of:
   - Reclassify the keyword's intent and re-map.
   - Note the mismatch in the page brief and accept the uphill battle.
   - Drop the keyword from the priority set.

This is the single most common reason mid-quality SEO research produces pages that don't rank. The SERP shape is destiny.

## How to collect SERP data

### Automated (degrades gracefully)

`scripts/serp_inspect.py <keyword> --country US` fetches a SERP via the public Google Search interface (no login, single request per query) and parses the top 10 + SERP features.

Google may challenge with CAPTCHA after several queries. The script:

1. Detects CAPTCHA / 429 / consent walls.
2. Fails gracefully with an explicit message.
3. Suggests the user either:
   - Use SerpAPI free tier (100 searches/month, https://serpapi.com).
   - Do manual SERP checks in incognito.

Never escalate evasion — fingerprint changes, proxies, residential IPs. Out of scope.

### Manual (when automation fails)

1. Open Google in a fresh incognito tab (no logged-in account).
2. Set the country / language via Google search settings.
3. Search the keyword.
4. Capture: top 10 URLs, top 10 titles, presence of PAA / featured snippet / video carousel / ads count.
5. Paste into a markdown table for the report.

This is slow but reliable. For 5–20 priority keywords, manual is fine.

## Reading paid-ad density

Number of paid text ads above the organic results is a fast proxy for commercial value:

| Ads visible | Implication |
|---|---|
| 0 | Low commercial value, or extremely specific. Check whether it's worth organic optimization. |
| 1–2 | Moderate commercial value. Organic is reachable. |
| 3–4 (the typical max above the fold) | High commercial competition. Organic top 3 is hard but worth pursuing if volume justifies. |
| Also ads in the right rail / bottom | Saturation. Volume is real; organic SEO needs strong authority to compete. |

## Featured snippets — strategy

If the top result is a featured snippet:

- **Don't ignore it.** It eats the #1 click-through-rate.
- **Aim to be the snippet's source** — structure your page's answer in 40–60 words right under an H2 that mirrors the query. Lists become bulleted lists; comparisons become tables.
- **If the snippet is owned by a dominant authority** (Wikipedia, government site), pivot to a long-tail variant where the snippet is up for grabs.

## People Also Ask — strategy

PAA blocks are free keyword research:

1. Capture every PAA question for your top priority terms.
2. They become **H2 candidates** on the page targeting the primary keyword.
3. They become **secondary keyword candidates** in their own right.
4. If a PAA question is significantly different in intent from the primary keyword, it's a separate page candidate.

## Output format

Phase 4 (no-volumes) should produce a SERP snapshot per priority keyword:

| Keyword | Top result type | Featured snippet | PAA count | Ads | Inferred competitiveness |
|---|---|---|---|---|---|
| embedded credit platform | Vendor landing | No | 4 | 3 | High |
| how does interchange work | Editorial | Yes (owned by Investopedia) | 6 | 0 | Snippet hard to displace; PAA opportunity |
| best credit platform for dealerships | Listicle blogs | No | 4 | 2 | Mixed; lean MOFU comparison page |

This table goes into `seo_research_report.md`.
