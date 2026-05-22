---
name: seo-research
description: Run keyword research, competitor analysis, and produce a locked SEO spreadsheet (keyword research + page map + SEO briefs) at the start of any web project. Trigger when the user asks for SEO research, keyword research, competitor SEO teardown, SERP analysis, page mapping, or populating an SEO master spreadsheet — typically before any copy is written. Generic skill, not tied to any single project. Do NOT trigger for technical SEO (sitemap, redirects, schema implementation), link-building, on-page audits of already-published pages, or copy writing — those are downstream of this skill.
---

# SEO Research Skill

You run **the first SEO phase of a web project** — *before* a single line of marketing copy is written. The output is a locked spreadsheet (3 tabs: Keyword Research, Page Map, SEO Briefs) plus a short research report. Downstream skills consume these artifacts; this skill never writes the marketing copy itself.

This skill is **project-agnostic**: no vertical-specific vocabulary, no brand-specific rules. The project's brand voice belongs to whatever copy skill the project ships with (e.g., `triage4us-copy`). This skill produces *the SEO constraints* that copy skill will honor.

## Position in the SEO pipeline

This skill is the **first** of three SEO skills. The full pipeline:

1. **`seo-research`** (this) → research, decide target keywords per page, generate locked SEO Briefs → populate the master spreadsheet.
2. **`seo-copy-sync`** (available) → read the locked briefs, invoke the project's copy skill to write copy that honors every SEO decision (title, meta, H1, primary/secondary keywords) + 8 on-page SEO best practices. 3 modes: `apply` / `refine` / `review`.
3. **`seo-validate`** (future) → after copy is written and the page is built, validate that the rendered page still honors the original briefs (no keyword drift, no length overflow, no missing H1).

**Why SEO before copy:** copy needs to be born already knowing which keyword the page is targeting, which title/meta is locked, which intent it serves. Writing copy first and trying to retrofit SEO produces keyword stuffing, awkward rewrites, and silent keyword cannibalization between pages.

**When to run this skill:** at the start of a project, *before* any new copy is produced. If the project already has copy in flight, run it anyway — the briefs become the retroactive baseline that `seo-validate` will check against.

## Always do this first

1. **Ask the user which operating mode to use** — the skill never assumes:
   - **"with volumes"** (recommended for serious launches) — skill drafts the candidate keyword list, pauses, asks user to export real volumes from Google Keyword Planner, then prioritizes on real data.
   - **"no volumes"** (zero-friction) — skill prioritizes on heuristics (competitor frequency, pytrends relative interest, SERP signals, modifier shape). Priority is **inferred**, not measured.
2. **Read the sources of truth** before producing anything (priority order):
   - `references/workflow.md` — the 7 ordered phases of an `seo-research` run.
   - `references/xlsx-schema.md` — exact cell mapping of the master spreadsheet. **Never** write to formula columns.
   - `references/keyword-planner-handoff.md` (with-volumes mode) or `references/heuristic-prioritization.md` (no-volumes mode).
3. **Verify the project brief is on file.** No brief = no research. Stop and ask the user for: project name, niche, audience (B2B/B2C), target countries, primary USPs, known competitors (if any), existing site URL (if any).
4. **Verify the spreadsheet template exists.** Per-project default — the project owns the template. For the current project: `seo/templates/SEO_Master_Template.xlsx`. For new projects, ask the user where the template lives or where they want the populated copy written. If absent, surface the gap before doing any other work.

## Prerequisites

- **SEO master spreadsheet template** — `SEO_Master_Template.xlsx` at a project-owned path (this project: `seo/templates/SEO_Master_Template.xlsx`). The skill copies the template to a working file (e.g., `<project>_SEO.xlsx`) before populating, so the template stays clean. The template must contain six tabs: `Instructions`, `Keyword Research`, `Page Map`, `SEO Briefs`, `Alt Text`, `Dashboard`. Schema is locked — see `references/xlsx-schema.md`.
- **Operating mode** — `with-volumes` or `no-volumes`, decided in the first turn.
- **Project briefing** — a short paragraph (or doc reference) covering project name, niche, audience, geo, USPs, known competitors.
- **Python 3.10+** with: `requests`, `beautifulsoup4`, `lxml`, `pytrends`, `openpyxl`. Install with `pip install requests beautifulsoup4 lxml pytrends openpyxl`.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Project briefing | **Yes** | Free-form text. Used to seed competitor discovery, keyword brainstorming, and intent decisions. |
| Operating mode | **Yes** | `with-volumes` or `no-volumes`. Decides phase 4 path. |
| Known competitors | Optional | If absent, skill identifies 5–10 via web search in phase 2. |
| Existing site URL | Optional | If present, scraped as a competitor-to-self to find canibalization risks and current rankings. |
| Keyword Planner CSV | Optional, **required if mode = with-volumes** | Supplied by the user mid-flow after the skill exports a candidate list. |

## Workflow (7 phases)

Detail in `references/workflow.md`. Summary:

1. **Discovery** — collect inputs above.
2. **Competitor analysis** — extract titles, H1s, metas, headings from 5–10 competitors. See `references/competitor-analysis.md`.
3. **Keyword discovery** — generate 50–150 candidates from competitor terms, sector brainstorm, long-tail variations, PAA / forum questions. Classify each by intent and funnel stage. See `references/keyword-research-methodology.md`, `references/intent-classification.md`.
4. **Volume / priority resolution** — mode-dependent. `with-volumes`: handoff to Keyword Planner, parse returned CSV, prioritize by volume × intent weight. `no-volumes`: run `pytrends_compare.py` + `serp_inspect.py`, score heuristically. See `references/keyword-planner-handoff.md` or `references/heuristic-prioritization.md`.
5. **Page mapping** — decide structure (1 primary keyword per page, no cannibalization). Populate the Page Map tab. See `references/page-mapping.md`.
6. **Brief generation** — for each page, draft title tag, meta description, H1. These are **drafts** — `seo-copy-sync` may refine when invoking the project's copy skill. Populate the SEO Briefs tab. See `references/seo-brief-generation.md`.
7. **Report & handoff** — generate `seo_research_report.md` at project root summarizing keywords found, top-20 by priority, page map, key decisions, next steps. Set Page Map status to `Draft`. Tell the user to review the spreadsheet and run `seo-copy-sync` when satisfied.

## Outputs

All SEO artifacts live under the project's `seo/` directory (or whatever path the project owns — ask the user for new projects). The skill never scatters outputs across the repo root.

```
seo/
├── templates/                      ← clean templates, NEVER write here
│   ├── SEO_Master_Template.xlsx
│   └── …
├── <project>_SEO.xlsx              ← working copy populated by the skill
├── seo_research_report.md          ← final markdown summary
└── raw/                            ← intermediate artifacts (CSVs, JSONs)
    ├── competitors_<date>.csv
    ├── pytrends_batch_<n>.csv
    └── serp_<keyword>.json
```

| Artifact | Path (this project) | Content |
|---|---|---|
| Populated working xlsx | `seo/<project>_SEO.xlsx` | 3 tabs filled: Keyword Research (≤100 keywords), Page Map (≤50 pages), SEO Briefs (≤50 briefs). Formula columns preserved. Templates stay untouched. |
| Research report | `seo/seo_research_report.md` | Discovery summary, top-20 priorities, page map, methodology, mode used, limitations. |
| Updated status flags | In-spreadsheet | Page Map rows marked `Draft` so `seo-copy-sync` knows what to consume. |
| Candidate keyword list | `seo/raw/keyword_candidates_<date>.csv` | Phase 3 output. **Format:** CSV with single `Keyword` header column, one keyword per row — matches Google Ads upload format. Template at `seo/templates/keywords-template.csv`. |
| Competitor surface | `seo/raw/competitors_<date>.csv` | Output of `scripts/analyze_competitors.py` from Phase 2. |
| Pytrends snapshots | `seo/raw/pytrends_batch_<n>.csv` | Output of `scripts/pytrends_compare.py` (no-volumes mode). |
| SERP snapshots | `seo/raw/serp_<keyword>.json` | Output of `scripts/serp_inspect.py`. |

The `seo/raw/` directory is optional to gitignore — keep if you want a frozen record of the research, ignore if you prefer to regenerate. Templates and outputs (xlsx, report) should be tracked.

## Hybrid mode

The skill has **two operating modes**, decided per invocation:

### with-volumes

- Used when the project has time/budget to validate keyword volumes against real data.
- Skill drafts the candidate list (phase 3), pauses, and asks the user to export volumes via one of the supported tools:
  - **Google Keyword Planner** (free; requires Google Ads account; volumes in ranges; 10-keyword cap per "Discover new keywords" request) — handoff: `references/keyword-planner-handoff.md`.
  - **SEMrush / Ahrefs / Moz / SE Ranking** (paid; exact volumes; bulk uploads; also returns Keyword Difficulty + SERP features + Intent classification) — handoff is simpler: upload the candidate CSV to the tool's "Bulk Analysis" / "Keyword Magic" feature, export, send back.
- Skill parses the returned CSV (auto-detects format: Google Ads UTF-16 vs SEMrush UTF-8; columns may include extras like KD / CPC / SERP Features), joins on the candidate list, drops rows with volume `<10` or `Low search volume` flag.
- Final priority = `volume × intent_weight` where `commercial > transactional > informational > navigational`. When KD is available (paid-tool path), apply a secondary tiebreaker: lower KD → higher priority within the same volume band.
- Honest note: paid-tool exports are the gold standard. Free Keyword Planner gives bucketed ranges only and is unreliable for accounts with no billing history.

### no-volumes

- Used for fast / exploratory work, or when the user doesn't have a Google Ads account.
- Skill runs `scripts/pytrends_compare.py` in groups of 5 keywords (pytrends API limit).
- Skill runs `scripts/serp_inspect.py` on the top candidates to read competition shape.
- Score formula: `(competitor_frequency × 2) + (pytrends_relative / 10) + commercial_intent_bonus − long_tail_penalty`.
- Final priority is **inferred** and labeled as such in the spreadsheet `Notes` column.
- Full methodology: `references/heuristic-prioritization.md`.

The skill **never** silently picks a mode. Phase 1 always opens with the question.

## Hard rules (DO NOT)

- **Never write copy.** Title / meta / H1 *drafts* are SEO scaffolding, not finished copy. The project's copy skill owns voice, tone, and brand vocabulary. `seo-copy-sync` is the handoff.
- **Never fabricate volumes.** In `no-volumes` mode, priority is inferred — the spreadsheet must say so. Don't write made-up numbers in the volume column.
- **Never write to formula columns** in `SEO Briefs` (columns D `Title length`, F `Meta length`, H `H1 length`). They are auto-calculated. See `references/xlsx-schema.md`.
- **Never touch hidden / structural tabs** (`Instructions`, `Alt Text`, `Dashboard`). The skill only writes to the three data tabs.
- **Never scrape aggressively.** 2-second rate limit per competitor in `analyze_competitors.py`. Respect `robots.txt`. No login-required content. No mass paginated scraping.
- **Never assign more than one primary keyword to a page.** Cannibalization defense — see `references/page-mapping.md`.
- **Never recommend a target where the SERP shape mismatches the page type.** If the top 10 for keyword X is all editorial blog posts, do not map it to a landing page without flagging the mismatch. See `references/serp-analysis.md`.
- **Never claim difficulty scores.** This skill has no real KD data (which is paid, Ahrefs/Semrush). When asked about difficulty, infer from SERP and say it's inferred.
- **Never run the skill against a project that has no brief.** Stop and ask for one. Bad inputs produce bad keyword maps that look authoritative.

## What this skill does NOT do

- **Copy writing / wording / tone** → handed to the project's copy skill via `seo-copy-sync` (future).
- **Technical SEO** (sitemap.xml, robots.txt, redirects, structured data implementation, Core Web Vitals fixes) → out of scope.
- **Real keyword difficulty scores / live rankings** → those require Ahrefs / Semrush / Moz / SE Ranking subscriptions. If the user has one of those tools, the skill consumes the export and uses the KD scores natively (paid-tool path under `with-volumes`). If the user doesn't, the skill produces *qualitative* difficulty signals only (SERP shape, competitor count, paid ad density).
- **Volumes without the handoff.** Pytrends gives *relative* interest 0–100, not absolute volume. The skill never invents a search-volume number.
- **Off-page analysis** (backlink profiles, domain authority, referring domains). Different toolchain.
- **Localization beyond country/language toggles in Keyword Planner.** Multilingual SEO needs a localization pass per language; this skill scaffolds one locale at a time.
- **Continuous monitoring / rank tracking.** One-shot research at project start. Re-run quarterly if needed, but that's a separate invocation.

## Honest limitations

- **Volumes from Keyword Planner are ranges**, not exact counts. `1K–10K` is treated as ~5,000 in the score; the spreadsheet stores the range string and the midpoint. Tools that promise exact volumes are extrapolating from clickstream data and are not authoritative either.
- **Pytrends is rate-limited and relative.** A 429 forces backoff; relative interest 0–100 means "vs the most popular term in this batch," not absolute search volume. Cross-batch comparisons are unreliable.
- **SERP scraping fails when Google challenges with CAPTCHA.** `serp_inspect.py` degrades gracefully and tells the user to swap in SerpAPI free tier or a manual SERP check.
- **No real-time ranking data.** Use Google Search Console after launch to validate the priority model retroactively — that's the feedback loop, not this skill.
- **Competitor analysis is observable surface only.** Title / meta / H1s / visible schema. Doesn't reveal their internal keyword strategy, ad bidding, or analytics — only what they ship.
- **Intent classification is heuristic.** Hard cases (e.g., "X review") split between informational and commercial depending on whether the searcher is comparing or learning. Document the call in `Notes`.

## Index — references

| File | Covers |
|---|---|
| `references/workflow.md` | 7 ordered phases with hand-offs and exit criteria per phase |
| `references/competitor-analysis.md` | How to pick competitors, what to extract, rate limits |
| `references/keyword-research-methodology.md` | Seed → expand → variations → long-tail framework, filtering rules |
| `references/intent-classification.md` | Informational / Commercial / Transactional / Navigational + funnel mapping |
| `references/serp-analysis.md` | Reading the SERP: page-type signals, PAA, ads, snippets |
| `references/page-mapping.md` | 1 primary KW per page, cluster topics, multi-vertical projects |
| `references/seo-brief-generation.md` | Title / Meta / H1 / OG templates with good and bad examples |
| `references/keyword-planner-handoff.md` | Step-by-step user handoff for `with-volumes` mode |
| `references/heuristic-prioritization.md` | Score formula for `no-volumes` mode + signal table |
| `references/xlsx-schema.md` | Exact cell-level mapping of the master spreadsheet |

## Index — scripts

| Script | Purpose |
|---|---|
| `scripts/analyze_competitors.py` | Fetch competitor URLs, extract title/meta/H1/H2s/H3s/schema, output CSV |
| `scripts/pytrends_compare.py` | Pytrends relative interest in batches of 5 keywords |
| `scripts/serp_inspect.py` | Read top-10 + SERP features for a keyword (no login) |
| `scripts/populate_xlsx.py` | Write Keyword Research / Page Map / SEO Briefs tabs from a JSON payload |
| `scripts/README.md` | Dependencies, usage, known limits |

## Extension points

- **Multi-locale work.** When the project ships in N languages, run the skill once per locale and produce one spreadsheet per locale. Don't merge — language ambiguity destroys page mapping.
- **Custom score weights.** The heuristic formula in `references/heuristic-prioritization.md` has documented knobs (`α`, `β`, etc.). Override per-invocation if the niche demands it (e.g., highly commercial niches weight `commercial_intent_bonus` higher).
- **Larger competitor sets.** Default cap is 10. Raise via CLI flag if the project is in a fragmented vertical.
- **Custom intent taxonomy.** Some niches need finer categories (e.g., "comparison" split from "commercial"). Document the extension inline in the `Notes` column for traceability.
