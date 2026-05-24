# Heuristic Prioritization

> Used only in `no-volumes` operating mode. The skill cannot access real search volumes, so it builds a *score* from observable signals: competitor coverage, pytrends relative interest, SERP shape, intent class, and modifier shape. The output is **inferred priority**, not measured demand. Every priority cell carries an explicit `(inferred)` flag in the spreadsheet `Notes` column.

## When to use this mode

- The project doesn't have a Google Ads account and won't create one.
- The project is exploratory / pre-budget and needs a directional map fast.
- A first pass before a `with-volumes` run, to narrow the list before paying the human cost of the Keyword Planner handoff.

## When NOT to use this mode

- The project is a serious launch with a budget for paid traffic. Heuristic priority is too noisy to drive paid-keyword bidding decisions.
- The niche is bilingual or multi-locale — pytrends gets unreliable across locale combinations.
- Volumes are non-negotiable for stakeholder reporting. In that case, switch to `with-volumes`.

## The score formula

```
score = (competitor_frequency * 2)
      + (pytrends_relative / 10)
      + commercial_intent_bonus
      − long_tail_penalty
```

Components:

### `competitor_frequency` — integer 0–10

Count of competitors (from Phase 2) that use the term in their title, H1, or H2s.

- 0 = no competitor touches the term. Pytrends or PAA must carry the signal alone.
- 1 = barely emerging. Risky unless it's strongly long-tail with clear intent.
- 2–4 = niche vocabulary baseline. Solid signal.
- 5+ = saturated. High competition; organic is uphill but volume is real.

Weighted ×2 because competitor coverage is the most reliable signal available without volumes.

### `pytrends_relative` — integer 0–100

From `scripts/pytrends_compare.py`. The score is *relative within the batch of 5 keywords* compared. To make cross-batch comparison less noisy:

- Always include 1 "anchor" keyword (a known high-volume term from the niche) in every batch.
- Normalize the batch's pytrends scores against the anchor.

If pytrends is unavailable (429 backoff exhausted), set to 0 and document in `Notes`.

Divided by 10 to keep the score in the same magnitude band as competitor frequency.

### `commercial_intent_bonus` — integer 0/2/3

| Intent | Bonus |
|---|---|
| Commercial | +3 |
| Transactional | +2 |
| Informational | 0 |
| Navigational | 0 |

Commercial > transactional because, in the no-volumes mode, transactional keywords usually have small absolute volumes that real volumes (if measured later) would penalize. Commercial keywords have broader volume profiles.

### `long_tail_penalty` — integer 0/2

| Word count | Penalty |
|---|---|
| 1–6 words | 0 |
| 7+ words | 2 |

Hyper-long-tail keywords (8+ words) often have negligible volume *and* low SERP competition, so they look attractive but rarely convert at meaningful scale. The penalty pushes them down the priority list unless the rest of the signals are strong.

## Worked example

Candidate: *"embedded credit platform for car dealerships"* (6 words)

- `competitor_frequency = 4` (4 of 8 competitors use it or close variants) → `4 × 2 = 8`
- `pytrends_relative = 35` (moderate interest vs anchor) → `35 / 10 = 3.5`
- Intent = commercial → `+3`
- Word count = 6 → `−0`

**Score = 8 + 3.5 + 3 − 0 = 14.5**

Compare to: *"how to lower interchange fees for sports venues"* (8 words)

- `competitor_frequency = 1` → `1 × 2 = 2`
- `pytrends_relative = 12` → `12 / 10 = 1.2`
- Intent = informational → `+0`
- Word count = 8 → `−2`

**Score = 2 + 1.2 + 0 − 2 = 1.2**

The first ranks much higher. Sanity check matches intuition.

## Priority buckets

After scoring all candidates:

| Bucket | Rule of thumb |
|---|---|
| `High` | Top ~30% by score. Map to landing / hub pages. |
| `Medium` | Next ~40%. Map to secondary keywords or spoke pages if the cluster supports it. |
| `Low` | Bottom ~30%. Park in `Notes`; revisit after launch with real Google Search Console data. |

These percentages are heuristic. In a long-tail-rich project, the `High` band may need to shrink to 15–20% because most candidates are weak.

## Sanity-check signals

### Positive signals (push a candidate up regardless of raw score)

- Appears in ≥3 competitors' titles or H1s.
- Pytrends relative ≥ 30.
- Commercial intent.
- Word count 3–5 (sweet spot for tail length).
- Appeared in a PAA block for a higher-priority term.
- Has a featured snippet opportunity (SERP shows no current snippet).

### Negative signals (push down or drop)

- Appears in only 1 competitor, no pytrends signal.
- Pytrends < 10 across multiple batches.
- Brand-specific to a *different* player (e.g., your candidate includes a competitor's product name in a way that doesn't make sense for your site).
- 8+ words and no competitor uses it.
- SERP shape mismatches the page type you'd want to build (see `serp-analysis.md`).
- Ad density = 0 and the term has commercial framing — usually means commercial value is weak.

## Limitations of the heuristic

- **No real volume data.** A high-score keyword might still get 20 searches/month. You'll only know post-launch via Google Search Console.
- **Pytrends is relative, not absolute.** A 100 in pytrends doesn't mean "many searches" — it means "more than the others in this batch."
- **Competitor frequency is biased toward established players.** New entrants in a niche may be targeting better long-tail terms that established competitors haven't caught up to.
- **The score is a starting point.** Manual judgment, especially around SERP shape and brand voice fit, should override the score in obvious cases. Document the override in `Notes`.

## Post-launch correction loop

The heuristic score is a *predictive* model. After the project launches:

1. Connect Google Search Console.
2. After 60–90 days, pull the actual impressions and clicks per keyword.
3. Compare against the heuristic priority. Where they diverge:
   - High heuristic / low actual = the heuristic over-weighted competitor frequency for that term. Demote in the next iteration.
   - Low heuristic / high actual = a sleeper hit. Promote in the next iteration.
4. Update the weights in the formula if patterns emerge. Document overrides in `seo_research_report.md`.

This loop is the real correction mechanism for the no-volumes mode. Treat the initial scoring as a hypothesis, not a verdict.
