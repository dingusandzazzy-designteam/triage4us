# Workflow — `seo-research`

> 7 ordered phases. Each phase has an exit criterion. **Never skip phases.** Skipping discovery or competitor analysis produces a keyword map that looks authoritative and is wrong.

The flow is linear with one branch in Phase 4 based on the operating mode chosen at the start.

---

## Phase 1 — Discovery (input gathering)

**Purpose:** collect everything the skill needs before doing any research.

**Collect from the user:**

| Field | Required | Notes |
|---|---|---|
| Project name | Yes | Used in `seo_research_report.md` and the report's filename. |
| Niche / industry | Yes | One sentence. "B2B fintech for community lenders," "DTC sneaker subscription," etc. |
| Audience | Yes | B2B / B2C / both. If both, ask which is primary. |
| Target countries | Yes | ISO codes preferred. Default `US` if user doesn't specify. |
| Languages | Yes | Default `en`. Multi-locale = one run per locale. |
| Primary USPs | Yes | 2–5 bullets. Used to bias keyword brainstorm toward differentiated modifiers. |
| Known competitors | Optional | If absent, Phase 2 discovers 5–10 via web search. |
| Existing site URL | Optional | If present, treated as a "self-competitor" to surface canibalization risk and current ranking signals. |
| Operating mode | Yes | `with-volumes` or `no-volumes`. Decides the Phase 4 branch. |

**Exit criterion:** every "Yes" row above is filled. If anything is missing, **stop** and ask. Do not invent.

---

## Phase 2 — Competitor analysis

**Purpose:** observe what's already ranking and what vocabulary the niche uses.

**Steps:**

1. If competitors weren't supplied, web-search the niche + audience + geo to identify 5–10 direct competitors. Document the search queries used in the report.
2. For each competitor, identify 3–8 high-signal pages: homepage, pricing, primary product/service pages, comparison pages, top blog posts (if surfacing in organic search).
3. Run `scripts/analyze_competitors.py` against the URL list. Output: CSV with `title`, `meta_description`, `h1`, `h2_concatenated`, `h3_concatenated`, `schema_types`.
4. Manually inspect the CSV for repeated terms across competitors. Repetition = niche vocabulary baseline.
5. Document for each competitor: URL list inspected, top 3 inferred keyword targets per page, schema strategy observed.

**Detail:** `competitor-analysis.md`.

**Exit criterion:** 5–10 competitors fully analyzed, niche vocabulary list (≥30 terms) extracted, schema patterns noted.

---

## Phase 3 — Keyword discovery

**Purpose:** expand from observed niche vocabulary into a candidate list of 50–150 keywords.

**Sources to combine:**

- **Competitor vocabulary** from Phase 2 (titles, H1s, repeated terms).
- **Seed brainstorming** from the project brief (USPs, product / service names, target persona vocabulary).
- **Long-tail variations** — apply common modifier sets (best / top / how to / what is / X vs Y / pricing / alternatives / for [use case]).
- **People Also Ask + forum questions** — web-search the top seeds and capture PAA blocks; search Reddit, Stack Overflow, Quora, niche forums for natural-language questions.

**For each candidate, classify:**

- **Intent:** Informational / Commercial / Transactional / Navigational (see `intent-classification.md`).
- **Funnel stage:** TOFU / MOFU / BOFU.
- **Source:** which Phase 2/3 source produced it (traceability).

**Discard rules (apply before Phase 4):**

- Brand keywords of unrelated companies.
- Internal jargon with no observable demand (no competitor uses it, no PAA, no pytrends signal).
- Pure navigational queries for *other* brands (e.g., "Stripe login" for a Stripe competitor — useless).

**Detail:** `keyword-research-methodology.md` and `intent-classification.md`.

**Exit criterion:** 50–150 candidates with intent + funnel + source filled in. List sorted alphabetically for handoff.

---

## Phase 4 — Volume / priority resolution

**Branch on the operating mode chosen in Phase 1.**

### 4a — with-volumes

1. Export the candidate list (Phase 3 output) to a plain-text or CSV file the user can paste.
2. **Pause execution.** Show the user this message verbatim:

   > Por favor, abra o Google Keyword Planner (ads.google.com/aw/keywordplanner), cole essa lista de keywords, exporte o CSV com volumes, e me envie. Aguardando...

   See `keyword-planner-handoff.md` for the step-by-step the user will follow.

3. When the user returns the CSV, parse it with `pandas` or `csv` stdlib. Join on the candidate list.
4. **Drop** any row with:
   - Volume `< 10` average monthly searches, or
   - Flag `Low search volume` in the export.
5. Compute final priority per keyword:
   ```
   priority_score = volume_midpoint * intent_weight
   intent_weight: commercial=1.5, transactional=1.3, informational=1.0, navigational=0.4
   ```
   Volume midpoint reads ranges like `1K-10K` → 5,000; `10-100` → 55.
6. Sort descending. Top N (default 30–50) flagged `High`; next band `Medium`; remainder `Low`.

**Exit criterion:** every surviving keyword has a numeric volume estimate, intent, funnel, source, and priority bucket.

### 4b — no-volumes

1. Group candidates in batches of 5 (pytrends API limit).
2. Run `scripts/pytrends_compare.py <kw1> <kw2> <kw3> <kw4> <kw5>` per batch. Output: CSV with relative interest (0–100), rising queries, related queries.
3. For the top 20–30 candidates from Phase 3 (by competitor frequency), run `scripts/serp_inspect.py <kw>` to capture top 10, featured snippet presence, PAA, ad count.
4. Compute heuristic score per keyword:
   ```
   score = (competitor_frequency * 2)
         + (pytrends_relative / 10)
         + commercial_intent_bonus      # +3 if commercial, +2 if transactional, 0 else
         - long_tail_penalty            # -2 if word count > 6
   ```
5. Sort descending. Buckets: `High` (top 30%), `Medium` (next 40%), `Low` (rest).
6. **Mark every priority cell with `(inferred)`** in the spreadsheet `Notes` column. Honest about the methodology.

**Detail:** `heuristic-prioritization.md`.

**Exit criterion:** every keyword has heuristic score, intent, funnel, source, priority bucket, and explicit `(inferred)` flag.

---

## Phase 5 — Page mapping

**Purpose:** turn the prioritized keyword list into a page structure.

**Rules:**

- **1 primary keyword per page.** Hard rule — cannibalization defense.
- **2–3 secondary keywords per page** allowed, but they must be variations / synonyms of the primary, not new intents.
- **Same intent per page.** Don't mix informational and transactional intents under one URL.
- **Cluster topics.** Group related secondary keywords; that cluster maps to one hub page + N spoke pages if the volume justifies it.
- **Don't invent pages without keyword backing.** Every row in Page Map points to ≥1 candidate from the prioritized list.

**Output structure to write to the `Page Map` tab:**

| Column | Content |
|---|---|
| Page name | Human label (e.g., "Pricing", "Automotive landing", "How to X guide") |
| URL slug | Kebab-case, no trailing slash |
| Page type | `Landing` / `Product` / `Pricing` / `Comparison` / `Blog` / `Hub` / `Spoke` / `Other` |
| Primary keyword | One from the prioritized list. Must trace. |
| Secondary keyword 1–3 | Variations only. Optional. |
| Status | `Draft` after Phase 5 completes. |

**Detail:** `page-mapping.md`.

**Exit criterion:** every `High` and `Medium` priority keyword is either assigned to a page or explicitly deferred with a note. No keyword is assigned to two pages.

---

## Phase 6 — Brief generation

**Purpose:** draft the locked SEO scaffolding each page must honor.

For each page in the Page Map, draft:

- **Title tag** — `[Primary keyword] [optional modifier] | [Brand]`. Keyword in first 30 chars. Total ≤ 60 chars.
- **Meta description** — open with problem/value-prop using the primary keyword, follow with differentiator, end with soft CTA. Avoid "Welcome to…". 150–160 chars total.
- **H1** — sentence case ending with a period, primary keyword used naturally, ≤ 70 chars.
- **OG Title / OG Description** — only fill if they differ from Title / Meta. Often left empty so they inherit.

**These are drafts.** The copy skill (via `seo-copy-sync`) may refine wording to honor brand voice, as long as the SEO constraints survive (keyword presence, length budget, sentence case).

Write to the `SEO Briefs` tab. **Never** write to formula columns (`Title length` D, `Meta length` F, `H1 length` H). See `xlsx-schema.md`.

**Detail:** `seo-brief-generation.md`.

**Exit criterion:** every page in the Page Map has Title, Meta, H1 drafts. Lengths fit budgets (the formula columns will validate on save).

---

## Phase 7 — Report & handoff

**Purpose:** produce a human-readable summary the user can review before invoking the next skill.

Write `seo/seo_research_report.md` (or `<project>/seo/seo_research_report.md` if running from a parent dir) with:

- **Run metadata:** date, project name, operating mode used, locale.
- **Discovery summary:** niche, audience, geo, USPs, competitors analyzed.
- **Methodology note:** sources, sample sizes, mode-specific caveats (especially the `(inferred)` flag in no-volumes mode).
- **Top 20 keywords by priority** with intent, funnel stage, target page.
- **Page map** as a markdown table.
- **Key decisions logged:** what was discarded and why; ambiguous intent calls; any keyword the SERP suggested mismatches the page type.
- **Next step:** "Review `SEO_Master.xlsx`. When satisfied, invoke `seo-copy-sync` to draft copy that honors these briefs."

Set Page Map row statuses to `Draft`. The next skill will move them to `Copy-Ready` once it consumes them.

**Exit criterion:** report file exists, spreadsheet is saved, user has been told what to do next.

---

## Failure recovery

| Failure | Recovery |
|---|---|
| User can't access Keyword Planner | Switch mode to `no-volumes`. Don't fake volumes. |
| Pytrends 429s repeatedly | Wait, backoff, batch slower. If persistent, mark affected keywords as `pytrends: unavailable` in `Notes` and skip that signal in the score. |
| `serp_inspect.py` hits CAPTCHA | Tell the user. Suggest SerpAPI free tier (100 queries/month) or manual SERP check. Don't fake SERP data. |
| Spreadsheet template missing | Stop. Ask the user where to put it. Don't generate a stub template — schema must match. |
| Project brief is too thin | Surface the gaps. Don't proceed with Phase 2 until the user fills them. |
