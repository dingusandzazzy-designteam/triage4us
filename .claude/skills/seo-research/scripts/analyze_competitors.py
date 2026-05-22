#!/usr/bin/env python3
"""
analyze_competitors.py — fetch competitor URLs and extract observable SEO surface.

Usage:
    python analyze_competitors.py --urls urls.txt --out competitors.csv
    python analyze_competitors.py --url https://example.com/pricing --out out.csv
    cat urls.txt | python analyze_competitors.py --out out.csv

Output CSV columns:
    url, title, meta_description, h1, h2_concatenated, h3_concatenated, schema_types, status

Respects robots.txt. Rate-limited to 2 seconds between requests.
Dependencies: requests, beautifulsoup4, lxml
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from typing import Optional
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Missing dependency: {e.name}. Run: pip install requests beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(1)


USER_AGENT = "seo-research-skill/1.0 (+https://example.com/bot)"
REQUEST_TIMEOUT = 15
RATE_LIMIT_SECONDS = 2.0


def can_fetch(url: str) -> bool:
    """Check robots.txt for the URL's host. Returns True if disallowed lookup fails (fail-open)."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception:
        return True
    try:
        return rp.can_fetch(USER_AGENT, url)
    except Exception:
        return True


def fetch_html(url: str) -> Optional[str]:
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
    except requests.RequestException:
        return None
    if resp.status_code != 200:
        return None
    content_type = resp.headers.get("Content-Type", "")
    if "html" not in content_type.lower():
        return None
    return resp.text


def extract_schema_types(soup: BeautifulSoup) -> list[str]:
    types: list[str] = []
    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = tag.string or tag.get_text() or ""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        nodes = data if isinstance(data, list) else [data]
        for node in nodes:
            if isinstance(node, dict):
                t = node.get("@type")
                if isinstance(t, str):
                    types.append(t)
                elif isinstance(t, list):
                    types.extend(x for x in t if isinstance(x, str))
    return sorted(set(types))


def extract_page(url: str, html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta = meta_tag.get("content", "").strip() if meta_tag else ""

    h1_tag = soup.find("h1")
    h1 = h1_tag.get_text(" ", strip=True) if h1_tag else ""

    h2_list = [h.get_text(" ", strip=True) for h in soup.find_all("h2")][:10]
    h3_list = [h.get_text(" ", strip=True) for h in soup.find_all("h3")][:10]

    schema_types = extract_schema_types(soup)

    return {
        "url": url,
        "title": title,
        "meta_description": meta,
        "h1": h1,
        "h2_concatenated": " | ".join(h2_list),
        "h3_concatenated": " | ".join(h3_list),
        "schema_types": ",".join(schema_types),
        "status": "OK",
    }


def analyze_urls(urls: list[str]) -> list[dict]:
    rows: list[dict] = []
    for i, url in enumerate(urls):
        if i > 0:
            time.sleep(RATE_LIMIT_SECONDS)
        url = url.strip()
        if not url:
            continue
        if not can_fetch(url):
            rows.append({
                "url": url, "title": "", "meta_description": "", "h1": "",
                "h2_concatenated": "", "h3_concatenated": "", "schema_types": "",
                "status": "ROBOTS_DISALLOWED",
            })
            continue
        html = fetch_html(url)
        if html is None:
            rows.append({
                "url": url, "title": "", "meta_description": "", "h1": "",
                "h2_concatenated": "", "h3_concatenated": "", "schema_types": "",
                "status": "FAILED",
            })
            continue
        try:
            rows.append(extract_page(url, html))
        except Exception as exc:
            rows.append({
                "url": url, "title": "", "meta_description": "", "h1": "",
                "h2_concatenated": "", "h3_concatenated": "", "schema_types": "",
                "status": f"PARSE_ERROR:{type(exc).__name__}",
            })
    return rows


def write_csv(rows: list[dict], path: str) -> None:
    fieldnames = ["url", "title", "meta_description", "h1", "h2_concatenated", "h3_concatenated", "schema_types", "status"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def read_urls_from_args(args) -> list[str]:
    if args.url:
        return [args.url]
    if args.urls:
        with open(args.urls, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    if not sys.stdin.isatty():
        return [line.strip() for line in sys.stdin if line.strip()]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch competitor URLs and extract SEO surface.")
    parser.add_argument("--url", help="Single URL to analyze.")
    parser.add_argument("--urls", help="Path to a file with one URL per line.")
    parser.add_argument("--out", default="competitors.csv", help="Output CSV path (default: competitors.csv).")
    args = parser.parse_args()

    urls = read_urls_from_args(args)
    if not urls:
        print("No URLs provided. Use --url, --urls, or pipe URLs via stdin.", file=sys.stderr)
        return 2

    rows = analyze_urls(urls)
    write_csv(rows, args.out)

    ok = sum(1 for r in rows if r["status"] == "OK")
    print(f"Analyzed {len(rows)} URLs ({ok} OK). Output: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
