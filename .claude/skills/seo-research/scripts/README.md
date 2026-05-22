# Scripts — `seo-research`

Helper scripts the skill calls during phases 2, 4, and 6/7. Each is invocable standalone for debugging.

## Dependencies

```bash
pip install requests beautifulsoup4 lxml pytrends openpyxl
```

Python 3.10+. Install in a venv if the project doesn't already have one.

## Scripts

### `analyze_competitors.py`

Fetch a list of competitor URLs and extract observable SEO surface (title, meta, H1, H2/H3, schema.org JSON-LD types).

```bash
# single URL
python analyze_competitors.py --url https://example.com/pricing --out out.csv

# list of URLs
python analyze_competitors.py --urls urls.txt --out competitors.csv

# stdin
cat urls.txt | python analyze_competitors.py --out competitors.csv
```

Behavior:

- Respects `robots.txt` via `urllib.robotparser`.
- 2-second rate limit between requests (hardcoded).
- Failed URLs are written with `status` column = `FAILED` / `ROBOTS_DISALLOWED` / `PARSE_ERROR:*`; the script continues.
- Output CSV columns: `url, title, meta_description, h1, h2_concatenated, h3_concatenated, schema_types, status`.

Consumed by: Phase 2 of the skill workflow. Output feeds the niche vocabulary baseline.

### `pytrends_compare.py`

Pull relative-interest data from Google Trends for up to 5 keywords per call.

```bash
# inline keywords
python pytrends_compare.py "embedded credit" "value-back platform" --country US

# from file
python pytrends_compare.py --keywords keywords.txt --out pytrends.csv

# different timeframe
python pytrends_compare.py "term1" "term2" --timeframe "today 5-y"
```

Behavior:

- Pytrends caps at 5 keywords per request — larger lists must be batched externally.
- Exponential backoff on 429 (5s, 10s, 20s, 40s, 80s — 5 retries).
- Output CSV columns: `keyword, mean_relative_interest, rising_queries, related_queries`.
- `mean_relative_interest` is **relative within the batch** (0–100), not absolute volume.

Consumed by: Phase 4 of the skill workflow in `no-volumes` mode.

**Known limitations:**

- Google Trends aggressively rate-limits unauthenticated requests. Long runs may hit 429 even with backoff.
- Cross-batch comparison is unreliable. Include an anchor keyword in every batch when comparing across batches.

### `serp_inspect.py`

Read top-10 organic results plus SERP features (featured snippet, PAA, ads count) for a single keyword.

```bash
python serp_inspect.py "embedded credit platform" --country US --out serp.json
python serp_inspect.py "embedded credit platform" --country US      # JSON to stdout
```

Behavior:

- Single HTTP request to `google.com/search`. No login. No proxy.
- Detects CAPTCHA / consent wall / 429 and fails gracefully with `status` set.
- Output JSON shape:
  ```json
  {
    "keyword": "...",
    "country": "...",
    "results": [{"position": 1, "url": "...", "title": "...", "snippet": "..."}, ...],
    "featured_snippet": {"text": "...", "source_url": "..."} | null,
    "people_also_ask": [...],
    "ads_count": int,
    "status": "OK | CAPTCHA | CONSENT_WALL | BLOCKED | ERROR:*"
  }
  ```

Consumed by: Phase 4 of the skill workflow (top 20–30 candidates in `no-volumes` mode) and Phase 5 sanity checks.

**Known limitations:**

- Google may serve different DOM markup over time; selectors may need updates.
- Heavy use from the same IP triggers CAPTCHA quickly. For >10 queries in a session, expect failures.
- Fallback path documented in `references/serp-analysis.md`: SerpAPI free tier (100 queries/month) or manual incognito SERP check.

### `populate_xlsx.py`

Write the three data tabs (Keyword Research, Page Map, SEO Briefs) of `SEO_Master.xlsx` from a JSON payload.

```bash
python populate_xlsx.py --xlsx SEO_Master.xlsx --payload payload.json
python populate_xlsx.py --xlsx SEO_Master.xlsx --payload payload.json --no-backup
```

Payload JSON shape: see the script's module docstring or `references/xlsx-schema.md`.

Behavior:

- `data_only=False` — formulas are preserved on save.
- Writes a `SEO_Master.xlsx.bak` before mutating (disable with `--no-backup`).
- Validates schema before writing: tab presence, header row integrity, cross-tab references.
- **Refuses to overwrite formula columns** (`SEO Briefs` D, F, H).
- **Refuses to write to protected tabs** (Instructions, Alt Text, Dashboard).
- Detects cannibalization (same Primary keyword on two pages) and aborts the save.

Consumed by: Phase 7 of the skill workflow.

**Known limitations:**

- The header-row check requires the user's template headers to match the canonical strings in `references/xlsx-schema.md` exactly. If a user renames a header, the script aborts and surfaces the diff.
- If the template uses additional formula columns beyond D/F/H, document the deviation and adjust the script's `BRIEF_FORMULA_COLS` set.

## Composing the scripts

Typical Phase 2 → Phase 4 → Phase 7 flow:

```bash
# Phase 2: competitor surface
python analyze_competitors.py --urls phase2_urls.txt --out phase2_competitors.csv

# Phase 4 (no-volumes mode): pytrends in batches of 5
python pytrends_compare.py --keywords batch1.txt --out pytrends_batch1.csv
python pytrends_compare.py --keywords batch2.txt --out pytrends_batch2.csv
# ... combine pytrends CSVs externally

# Phase 4 sanity: SERP check on top candidates
for kw in $(cat top_candidates.txt); do
  python serp_inspect.py "$kw" --country US --out "serp_$(echo "$kw" | tr ' ' '_').json"
  sleep 5   # rate-limit ourselves to avoid CAPTCHA
done

# Phase 7: populate the spreadsheet
python populate_xlsx.py --xlsx SEO_Master.xlsx --payload final_payload.json
```

The skill itself orchestrates these calls. The standalone usage is for debugging or for users who want to override individual phases.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `analyze_competitors.py` returns `ROBOTS_DISALLOWED` | Site's robots.txt blocks scrapers | Honor it; skip the page or do manual check. |
| `pytrends_compare.py` 429s after a few calls | Google Trends rate limit | Wait 10–15 minutes between sessions; reduce batch frequency. |
| `serp_inspect.py` returns `CAPTCHA` | Google challenged the script | Wait, use SerpAPI free tier, or manual SERP. Do not escalate evasion. |
| `populate_xlsx.py` aborts with "header mismatch" | User edited the template headers | Restore canonical headers or update `references/xlsx-schema.md` and the script's header constants. |
| `populate_xlsx.py` "cannibalization detected" | Two pages share a Primary keyword | Fix the Page Map (Phase 5) before retrying. |
