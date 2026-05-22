#!/usr/bin/env python3
"""
pytrends_compare.py — relative interest for up to 5 keywords via Google Trends.

Usage:
    python pytrends_compare.py "embedded credit" "value-back platform" --country US --timeframe "today 12-m"
    python pytrends_compare.py --keywords keywords.txt --out pytrends.csv

pytrends caps payloads at 5 keywords per request. Larger lists must be batched
externally (or call this script multiple times with overlapping anchor keywords).

Output:
    Single CSV with columns: keyword, mean_relative_interest, rising_queries, related_queries.

Limitations:
    - Relative interest is 0-100 WITHIN THE BATCH. Cross-batch comparison requires an anchor keyword.
    - Google Trends rate-limits aggressively. The script retries with exponential backoff on 429.

Dependencies: pytrends
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from typing import Optional

try:
    from pytrends.request import TrendReq
    from pytrends.exceptions import TooManyRequestsError
except ImportError as e:
    print(f"Missing dependency: {e.name}. Run: pip install pytrends", file=sys.stderr)
    sys.exit(1)


MAX_KEYWORDS_PER_BATCH = 5
INITIAL_BACKOFF_SECONDS = 5
MAX_RETRIES = 5


def fetch_batch(keywords: list[str], country: str, timeframe: str) -> dict:
    if len(keywords) > MAX_KEYWORDS_PER_BATCH:
        raise ValueError(f"Pytrends accepts max {MAX_KEYWORDS_PER_BATCH} keywords per batch; got {len(keywords)}.")

    pt = TrendReq(hl="en-US", tz=0, timeout=(10, 25))

    backoff = INITIAL_BACKOFF_SECONDS
    for attempt in range(MAX_RETRIES):
        try:
            pt.build_payload(kw_list=keywords, cat=0, timeframe=timeframe, geo=country, gprop="")
            interest_df = pt.interest_over_time()
            related = pt.related_queries() or {}
            break
        except TooManyRequestsError:
            if attempt == MAX_RETRIES - 1:
                raise
            print(f"  429 rate limited; backing off {backoff}s (attempt {attempt + 1}/{MAX_RETRIES})", file=sys.stderr)
            time.sleep(backoff)
            backoff *= 2
        except Exception as exc:
            if attempt == MAX_RETRIES - 1:
                raise
            print(f"  error {type(exc).__name__}: {exc}; retrying in {backoff}s", file=sys.stderr)
            time.sleep(backoff)
            backoff *= 2

    results: dict = {}
    for kw in keywords:
        mean = 0.0
        if not interest_df.empty and kw in interest_df.columns:
            try:
                mean = float(interest_df[kw].mean())
            except Exception:
                mean = 0.0

        rising_list: list[str] = []
        related_list: list[str] = []
        kw_block = related.get(kw, {}) if isinstance(related, dict) else {}
        rising_df = kw_block.get("rising") if isinstance(kw_block, dict) else None
        top_df = kw_block.get("top") if isinstance(kw_block, dict) else None
        if rising_df is not None and not rising_df.empty:
            rising_list = list(rising_df["query"].astype(str).head(10))
        if top_df is not None and not top_df.empty:
            related_list = list(top_df["query"].astype(str).head(10))

        results[kw] = {
            "mean_relative_interest": round(mean, 2),
            "rising_queries": " | ".join(rising_list),
            "related_queries": " | ".join(related_list),
        }
    return results


def read_keywords(args) -> list[str]:
    if args.keywords:
        with open(args.keywords, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()][:MAX_KEYWORDS_PER_BATCH]
    return list(args.terms)[:MAX_KEYWORDS_PER_BATCH]


def write_csv(rows: list[dict], path: Optional[str]) -> None:
    fieldnames = ["keyword", "mean_relative_interest", "rising_queries", "related_queries"]
    if path:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def main() -> int:
    parser = argparse.ArgumentParser(description="Pytrends relative interest for up to 5 keywords.")
    parser.add_argument("terms", nargs="*", help="Keywords to compare (up to 5).")
    parser.add_argument("--keywords", help="Path to a file with one keyword per line (up to 5 used).")
    parser.add_argument("--country", default="US", help="Two-letter country code (default: US).")
    parser.add_argument("--timeframe", default="today 12-m", help="Pytrends timeframe (default: 'today 12-m').")
    parser.add_argument("--out", help="Output CSV path (default: stdout).")
    args = parser.parse_args()

    keywords = read_keywords(args)
    if not keywords:
        print("No keywords provided.", file=sys.stderr)
        return 2

    try:
        results = fetch_batch(keywords, args.country, args.timeframe)
    except Exception as exc:
        print(f"Pytrends fetch failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    rows = [{"keyword": kw, **vals} for kw, vals in results.items()]
    write_csv(rows, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
