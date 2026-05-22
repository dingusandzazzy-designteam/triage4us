#!/usr/bin/env python3
"""
serp_inspect.py — read the top-10 organic results plus SERP features for a keyword.

Usage:
    python serp_inspect.py "embedded credit platform" --country US --out serp.json
    python serp_inspect.py "embedded credit platform" --country US      # prints JSON to stdout

Output JSON shape:
    {
        "keyword": str,
        "country": str,
        "results": [
            {"position": int, "url": str, "title": str, "snippet": str}, ...
        ],
        "featured_snippet": {"text": str, "source_url": str} | null,
        "people_also_ask": [str, ...],
        "ads_count": int,
        "status": "OK" | "CAPTCHA" | "BLOCKED" | "ERROR:..."
    }

Limitations:
    - Single request per call. Google may challenge with CAPTCHA after a handful of queries from the same IP.
    - On CAPTCHA / consent wall / 429, the script fails with status set and a hint to use SerpAPI free tier.
    - No login. No proxy chaining. No evasion. Public surface only.

Dependencies: requests, beautifulsoup4, lxml
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Missing dependency: {e.name}. Run: pip install requests beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(1)


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
REQUEST_TIMEOUT = 20


def build_url(keyword: str, country: str) -> str:
    q = quote_plus(keyword)
    gl = country.lower()
    return f"https://www.google.com/search?q={q}&gl={gl}&hl=en&num=20"


def detect_block(html: str) -> Optional[str]:
    lower = html.lower()
    if "captcha" in lower or "/sorry/" in lower:
        return "CAPTCHA"
    if "consent.google.com" in lower:
        return "CONSENT_WALL"
    if "unusual traffic" in lower:
        return "BLOCKED"
    return None


def parse_results(soup: BeautifulSoup) -> list[dict]:
    results: list[dict] = []
    seen_urls: set[str] = set()
    for block in soup.select("div.g, div.tF2Cxc, div.yuRUbf"):
        a = block.find("a", href=True)
        if not a:
            continue
        href = a["href"]
        if not href.startswith("http"):
            continue
        if href in seen_urls:
            continue
        h3 = block.find("h3")
        title = h3.get_text(" ", strip=True) if h3 else ""
        snippet_tag = block.select_one("div.VwiC3b, span.aCOpRe, div.IsZvec")
        snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""
        results.append({
            "position": len(results) + 1,
            "url": href,
            "title": title,
            "snippet": snippet,
        })
        seen_urls.add(href)
        if len(results) >= 10:
            break
    return results


def parse_featured_snippet(soup: BeautifulSoup) -> Optional[dict]:
    fs = soup.select_one("div.kp-blk, div.c2xzTb, div.xpdopen")
    if not fs:
        return None
    text_tag = fs.select_one("span, div.hgKElc, div.kno-rdesc")
    source_tag = fs.find("a", href=True)
    if not text_tag and not source_tag:
        return None
    return {
        "text": text_tag.get_text(" ", strip=True) if text_tag else "",
        "source_url": source_tag["href"] if source_tag else "",
    }


def parse_paa(soup: BeautifulSoup) -> list[str]:
    questions: list[str] = []
    for q in soup.select("div.related-question-pair, div[jsname='Cpkphb']"):
        text = q.get_text(" ", strip=True)
        if text and text not in questions:
            questions.append(text)
        if len(questions) >= 10:
            break
    return questions


def count_ads(soup: BeautifulSoup) -> int:
    ad_blocks = soup.select("div[data-text-ad], div.uEierd, div.commercial-unit-desktop-top")
    return len(ad_blocks)


def inspect(keyword: str, country: str) -> dict:
    url = build_url(keyword, country)
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        return {
            "keyword": keyword, "country": country, "results": [],
            "featured_snippet": None, "people_also_ask": [], "ads_count": 0,
            "status": f"ERROR:{type(exc).__name__}",
        }

    if resp.status_code == 429:
        return {
            "keyword": keyword, "country": country, "results": [],
            "featured_snippet": None, "people_also_ask": [], "ads_count": 0,
            "status": "BLOCKED",
        }
    if resp.status_code != 200:
        return {
            "keyword": keyword, "country": country, "results": [],
            "featured_snippet": None, "people_also_ask": [], "ads_count": 0,
            "status": f"ERROR:HTTP_{resp.status_code}",
        }

    block = detect_block(resp.text)
    if block:
        return {
            "keyword": keyword, "country": country, "results": [],
            "featured_snippet": None, "people_also_ask": [], "ads_count": 0,
            "status": block,
        }

    soup = BeautifulSoup(resp.text, "lxml")
    return {
        "keyword": keyword,
        "country": country,
        "results": parse_results(soup),
        "featured_snippet": parse_featured_snippet(soup),
        "people_also_ask": parse_paa(soup),
        "ads_count": count_ads(soup),
        "status": "OK",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect Google SERP for a keyword.")
    parser.add_argument("keyword", help="Keyword to inspect.")
    parser.add_argument("--country", default="US", help="Two-letter country code (default: US).")
    parser.add_argument("--out", help="Write JSON to this path (default: stdout).")
    args = parser.parse_args()

    data = inspect(args.keyword, args.country)

    if data["status"] != "OK":
        msg = (
            f"SERP inspection status: {data['status']}.\n"
            "Google may be challenging this client. Options:\n"
            "  1. Try again after a delay.\n"
            "  2. Use SerpAPI free tier (100 queries/month): https://serpapi.com\n"
            "  3. Do a manual SERP check in a fresh incognito browser."
        )
        print(msg, file=sys.stderr)

    payload = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
    else:
        print(payload)

    return 0 if data["status"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
