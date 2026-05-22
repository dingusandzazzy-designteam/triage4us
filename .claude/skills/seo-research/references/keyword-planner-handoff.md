# Keyword Planner Handoff

> Used only in `with-volumes` operating mode. The skill cannot access Google Ads programmatically without a billing-capable account and OAuth credentials, so it hands off to the user mid-flow.

## Why the handoff exists

Google Keyword Planner is the only free source of search-volume data that comes directly from Google. Third-party tools (Ahrefs, Semrush, Moz, KWFinder) estimate from clickstream and serve volumes that disagree with each other and with Keyword Planner. For a research baseline that downstream tooling can audit against, Keyword Planner is the source of truth — but it requires a Google Ads account and a human in the loop.

The user, not the skill, performs the export. The skill pauses, waits, parses what comes back.

## Prerequisites for the user

- A Google Ads account (free to create at ads.google.com — no campaign or spend required to access Keyword Planner).
- Browser access to ads.google.com.
- The skill's exported candidate list. **Format: CSV with a single column header `Keyword`, one keyword per row.** This matches Google Ads' upload-supported format — see `seo/templates/keywords-template.csv` for the canonical empty template (one column: `Keyword`).

## Step-by-step procedure (give this to the user verbatim)

1. **Open Google Keyword Planner** — go to `ads.google.com/aw/keywordplanner`. Sign in with the Google account tied to your Ads account.

2. **Choose "Discover new keywords"** — the second of the two big cards on the Keyword Planner home.

3. **Select "Start with keywords"** — the tab on the left of the input panel.

4. **Provide the candidate list — preferred method is CSV upload:**
   - **Recommended (single shot):** click the upload icon in the input panel and upload the skill's exported `seo/raw/keyword_candidates_<date>.csv` directly. Google Ads accepts CSVs with `Keyword` as the single column header. No batching needed for typical lists (50–150 keywords).
   - **Fallback:** paste keywords manually. Google's UI caps each paste at ~10 terms; for longer lists, split into batches and combine the resulting CSVs after.

5. **Set targeting** — match the project's target country and language. Default `United States` / `English` if the project didn't specify.

6. **Set the date range** — default is "Last 12 months." Keep it unless the project has a seasonality reason to widen the window.

7. **Click "Get results."** Keyword Planner returns a table with: Keyword, Avg. monthly searches, Competition, Competition (indexed value), Top of page bid (low range), Top of page bid (high range).

8. **Download CSV** — top-right of the results panel, "Download keyword ideas" → "Plan historical metrics (.csv)" or just "Keyword ideas (.csv)." The "Keyword ideas" CSV is sufficient.

9. **Repeat for additional batches** if the candidate list exceeded the single-submission cap. Save each as a separate CSV.

10. **Send the CSV(s) back to the skill.** Drop them in the chat or save to a known path and point the skill at it.

## What the CSV contains

Columns typically include (Keyword Planner varies UI to UI):

| Column | Meaning |
|---|---|
| Keyword | The exact term you submitted (sometimes the auto-deduped form). |
| Avg. monthly searches | Volume **range** like `1K - 10K` or a numeric estimate. |
| Three month change | Recent trend, % delta. |
| YoY change | Year-over-year delta. |
| Competition | `Low` / `Medium` / `High` — paid competition, NOT organic SEO difficulty. |
| Competition (indexed value) | 0–100 numeric version of Competition. |
| Top of page bid (low range) | $ value — paid commercial intent proxy. |
| Top of page bid (high range) | $ value — same. |

**Note:** `Competition` measures *paid ad bidding density*, not organic difficulty. Use it as a *signal* of commercial intent (high competition = many advertisers want this traffic = high commercial value), not as a difficulty score.

## How to read volume ranges

Keyword Planner reports volumes in buckets, not exact numbers:

| Range | Midpoint to use in scoring |
|---|---|
| `10 - 100` | 55 |
| `100 - 1K` | 550 |
| `1K - 10K` | 5,500 |
| `10K - 100K` | 55,000 |
| `100K - 1M` | 550,000 |
| `1M - 10M` | 5,500,000 |

If the row is flagged `Low search volume` or shows `–`, treat as effectively zero and drop the keyword unless the project specifically wants to chase ultra-long-tail.

If `Avg. monthly searches` is a number (rare — happens for Ads customers with billing history on the account), use it directly.

## Parsing in the skill

`scripts/populate_xlsx.py` reads the CSV with `pandas` (or `csv` stdlib) and joins on the candidate list. Pseudocode:

```python
import csv

def parse_kp_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        # Keyword Planner exports a 2-line header sometimes; skip until column row
        reader = csv.DictReader(f)
        for r in reader:
            kw = r.get('Keyword', '').strip().lower()
            vol_str = r.get('Avg. monthly searches', '').strip()
            comp = r.get('Competition', '').strip()
            rows.append({'keyword': kw, 'volume_raw': vol_str, 'competition': comp})
    return rows


RANGE_MIDPOINTS = {
    '10 - 100': 55,
    '100 - 1K': 550,
    '1K - 10K': 5500,
    '10K - 100K': 55000,
    '100K - 1M': 550000,
    '1M - 10M': 5500000,
}


def midpoint(vol_str):
    if not vol_str or vol_str in ('-', '–'):
        return 0
    if vol_str in RANGE_MIDPOINTS:
        return RANGE_MIDPOINTS[vol_str]
    try:
        return int(vol_str.replace(',', ''))
    except ValueError:
        return 0
```

## Edge cases

| Situation | Handling |
|---|---|
| Upload rejected with *"Keywords cannot contain non-standard characters like: ! @ % , *"* | Strip forbidden characters before upload: `!`, `@`, `%`, `,`, `*`, `$`, `&`. Replace `&` with `and` (e.g. `F&I` → `F and I`). Drop currency / percent / superlative-specific keywords (`$30K`, `0.5%`) — they have near-zero search volume in Keyword Planner anyway. Document drops in Notes. |
| User pastes <10 keywords per batch | Fine — Keyword Planner accepts any length up to the cap. |
| User exports multiple CSVs | Concatenate before parsing. Dedupe by keyword string. |
| Keyword in the export differs slightly from candidate (lowercasing, plural, etc.) | Fuzzy-match by lowercased exact string; if no match, mark as `(unmatched)` in `Notes` and use the candidate's original form for the spreadsheet row. |
| User can't reach Keyword Planner (account issues, geo restrictions) | Switch the run to `no-volumes` mode. Document the mode switch in the report. |
| User exports with billing-history account showing exact numbers | Use the exact numbers directly; don't bucket. |
| Export shows `Low search volume` flag | Drop the keyword from the priority set. Note it in `Notes` for future reconsideration. |

## What this skill does NOT do with Keyword Planner

- Does not log into Google Ads itself.
- Does not access Google Ads API.
- Does not bid, create campaigns, or read account spend.
- Does not save the user's Google account credentials.

The handoff is intentional: the human owns the account.
