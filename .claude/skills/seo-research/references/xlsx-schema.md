# XLSX Schema

> Exact cell-level mapping of `SEO_Master_Template.xlsx`. **The schema is the contract.** Writing outside these ranges, or writing to formula columns, breaks the template's dashboards and validation logic.
>
> **Template location.** The skill does **not** ship its own copy of the template — each project owns one. For the current project the canonical template lives at `seo/templates/SEO_Master_Template.xlsx`. For new projects, ask the user. The skill always copies the template to a working file (e.g., `<project>_SEO.xlsx`) before populating, so the template stays clean and reusable.

## Reading the template

- Use `openpyxl` with `data_only=False` to preserve formulas.
- Open the file once at the start of `scripts/populate_xlsx.py`, write all changes, save once at the end.
- Do **not** call `wb.save()` between writes — partial saves can leave the file in an inconsistent state if the script errors mid-flow.

```python
from openpyxl import load_workbook

wb = load_workbook('SEO_Master.xlsx', data_only=False)
# write to sheets here
wb.save('SEO_Master.xlsx')
```

## Tabs the skill writes to

Three tabs only: `Keyword Research`, `Page Map`, `SEO Briefs`.

## Tabs the skill NEVER touches

- `Instructions` — the human-readable template guide. Static content; users may add notes but the skill must not overwrite.
- `Alt Text` — accessibility scaffolding for the dashboard. Static.
- `Dashboard` — pivot / formula-driven summary. Reads from the data tabs; do not write directly to it.

If any of these tabs are missing from the user's template, **stop and surface the gap**. Don't try to recreate them — the user's template may have customizations the skill doesn't know about.

## Tab: `Keyword Research`

### Layout

| Row | Content |
|---|---|
| 1 | Sheet title (e.g., "Keyword Research"). Frozen / styled. **Do not overwrite.** |
| 2 | Subtitle / description. **Do not overwrite.** |
| 3 | Empty / styled separator. **Do not overwrite.** |
| 4 | Column headers. **Do not overwrite.** |
| 5 to 104 | Data rows — the skill writes here. Up to 100 keywords. |
| 105+ | Reserved for future expansion. Leave empty. |

### Column headers (row 4)

| Col | Header | Skill writes? |
|---|---|---|
| A | Keyword | Yes |
| B | Avg. monthly searches | Yes |
| C | Intent | Yes |
| D | Funnel stage | Yes |
| E | Target page | Yes (filled after Phase 5) |
| F | Priority | Yes |
| G | CPC (USD) | Yes (only in `with-volumes` mode) |
| H | SERP Features | Yes (only in `with-volumes` mode) |
| I | Notes | Yes |

### Value rules

- **Keyword (A):** lowercase, exactly as it will appear in the candidate list.
- **Avg. monthly searches (B):** in `with-volumes` mode, the volume midpoint (numeric) — store the range string in `Notes` for traceability. In `no-volumes` mode, write the heuristic score (numeric) and add `(score, inferred)` to `Notes`.
- **Intent (C):** one of `Informational` / `Commercial` / `Transactional` / `Navigational`. Multi-intent keywords use comma-separated values (e.g., `Informational, Commercial`).
- **Funnel stage (D):** one of `TOFU` / `MOFU` / `BOFU` (or empty for navigational).
- **Target page (E):** must match a Page name from the `Page Map` tab. Empty until Phase 5 assigns.
- **Priority (F):** one of `High` / `Medium` / `Low`. In `no-volumes` mode, append ` (inferred)` to the cell value or document inline in `Notes`.
- **CPC (USD) (G):** numeric (e.g., `4.62`). The average cost-per-click paid by advertisers for this keyword in Google Ads — used as a proxy for commercial intent and clicks' economic value. `0` means no advertisers bid (almost always pure-informational). Empty in `no-volumes` mode.
- **SERP Features (H):** comma-separated list of features Google injects on the SERP for this keyword. Common values: `AI Overview`, `People Also Ask`, `Featured Snippet`, `Local Pack`, `Video`, `Video Carousel`, `Image Pack`, `Sitelinks`, `Discussions and Forums`, `Things to Know`, `Jobs`, `Reviews`, `Short videos`, `Related searches`, `Ads top`, `Ads middle`, `Ads bottom`. Copy verbatim from the SEMrush export. Empty in `no-volumes` mode.
- **Notes (I):** source codes (`comp:N`, `paa`, `forum:reddit`, etc.) + any decisions (intent ambiguity calls, mode flag).

### Why CPC + SERP Features

Volume + KD answers *how much demand and how hard*. CPC + SERP Features answers *how valuable each click is and what format the SERP rewards*. Without these two columns, briefs are written blind to the real competitive surface — see `seo-brief-generation.md` §Decision matrix.

### Template migration (existing projects)

Projects whose `SEO_Master_Template.xlsx` predates the CPC + SERP Features columns must extend the `Keyword Research` tab row 4 headers from 7 columns (A–G) to 9 columns (A–I) before the populate script can run:

- Insert two columns between current column F (`Priority`) and current column G (`Notes`).
- New G header: `CPC (USD)`. New H header: `SERP Features`. Old G (`Notes`) becomes I.
- The `Notes` column ends up at I instead of G — update any conditional formatting or dashboard references that point to the old G coordinate.

If the populate script aborts with `Tab 'Keyword Research' header row 4 mismatch`, the template still has the old 7-column layout and needs the migration above.

## Tab: `Page Map`

### Layout

| Row | Content |
|---|---|
| 1–3 | Title / subtitle / separator. **Do not overwrite.** |
| 4 | Column headers. **Do not overwrite.** |
| 5 to 54 | Data rows — up to 50 pages. |
| 55+ | Reserved. |

### Column headers (row 4)

| Col | Header | Skill writes? |
|---|---|---|
| A | Page name | Yes |
| B | URL slug | Yes |
| C | Page type | Yes |
| D | Primary keyword | Yes |
| E | Secondary keyword 1 | Yes |
| F | Secondary keyword 2 | Yes |
| G | Secondary keyword 3 | Yes |
| H | Status | Yes |

### Value rules

- **Page name (A):** human-readable; must be unique within the tab.
- **URL slug (B):** kebab-case, leading `/`, no trailing slash. E.g., `/for-automotive`.
- **Page type (C):** one of `Landing` / `Product` / `Pricing` / `Comparison` / `Blog` / `Hub` / `Spoke` / `Other`.
- **Primary keyword (D):** must match a row in `Keyword Research` tab (column A). Cannibalization guard.
- **Secondary keyword 1–3 (E–G):** must match rows in `Keyword Research` tab. Cannot duplicate the Primary or another page's Primary.
- **Status (H):** `Draft` after Phase 5; advanced by downstream skills (`Copy-Ready`, `Copy-Done`, `Validated`).

### Cannibalization check before save

Run programmatically: collect all Primary keyword values from column D. If any appear more than once, **abort the save** and surface the duplicates to the user.

## Tab: `SEO Briefs`

### Layout

| Row | Content |
|---|---|
| 1–3 | Title / subtitle / separator. **Do not overwrite.** |
| 4 | Column headers. **Do not overwrite.** |
| 5 to 54 | Data rows — one row per page in `Page Map`. Up to 50 briefs. |
| 55+ | Reserved. |

### Column headers (row 4)

| Col | Header | Skill writes? |
|---|---|---|
| A | Page | Yes |
| B | URL slug | Yes |
| C | Title tag | Yes |
| D | Title length | **NO — formula** |
| E | Meta description | Yes |
| F | Meta length | **NO — formula** |
| G | H1 | Yes |
| H | H1 length | **NO — formula** |

### Formula columns

Columns **D, F, H** are auto-calculated by the template:

- `D` (Title length) = `=LEN(C5)` etc.
- `F` (Meta length) = `=LEN(E5)` etc.
- `H` (H1 length) = `=LEN(G5)` etc.

**The skill must not write to these cells.** If `populate_xlsx.py` writes a value into D/F/H, it overwrites the formula and the dashboard breaks. The script asserts this.

### Value rules

- **Page (A):** must match `Page Map` column A exactly.
- **URL slug (B):** copied from `Page Map` column B.
- **Title tag (C):** draft from Phase 6. ≤ 60 chars; the formula in D will flag violations.
- **Meta description (E):** draft from Phase 6. 150–160 chars target; the formula in F will flag.
- **H1 (G):** draft from Phase 6. ≤ 70 chars; the formula in H will flag.

If the user's template uses different formula columns (e.g., row 4 in column I has a status column), document the deviation in `seo_research_report.md` and adapt — but always keep the rule: *never overwrite a column that contains a formula.*

## Validation before save

`scripts/populate_xlsx.py` runs these checks before writing to disk:

1. **Tab presence:** all three writable tabs exist; the three protected tabs exist.
2. **Header row integrity:** row 4 in each writable tab matches the expected header strings. If a header has been renamed in the user's template, abort and surface.
3. **Formula column protection:** assert that no D5:D54, F5:F54, H5:H54 cell in `SEO Briefs` has been targeted for write.
4. **Primary keyword uniqueness:** scan `Page Map` column D for duplicates; abort on conflict.
5. **Cross-tab references:** every Primary keyword in `Page Map` exists in `Keyword Research`; every Page in `SEO Briefs` exists in `Page Map`.

If any check fails, the script raises a clear error before touching the file.

## Edge case: openpyxl strips formulas if mis-saved

`openpyxl` with `data_only=True` (the **wrong** flag) reads cached values and discards formulas on save. **Always use `data_only=False`.** Document this at the top of `populate_xlsx.py`.

## Backup before write

Optional but recommended: the script can write a `.bak` copy of the spreadsheet before mutating it. Easy to recover if something goes wrong.

```python
import shutil

shutil.copy('SEO_Master.xlsx', 'SEO_Master.xlsx.bak')
# ... then write
```
