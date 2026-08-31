#!/usr/bin/env python3
"""
Validate the static sitemap and print Google Search Console steps to recrawl the site.

Google deprecated the anonymous sitemap ping endpoint; use Search Console instead.
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from woa_ai_crawl import SITEMAP_STATIC_NAME, SITE_ORIGIN, write_ai_crawl_assets
from woa_sitemap import url_count

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def main() -> int:
    root = Path(__file__).resolve().parent
    write_ai_crawl_assets(root)
    sitemap_path = root / SITEMAP_STATIC_NAME
    if not sitemap_path.is_file():
        print(f"Missing {sitemap_path}", file=sys.stderr)
        return 1

    tree = ET.parse(sitemap_path)
    locs = [el.text.strip() for el in tree.findall(".//sm:loc", NS) if el.text]
    print(f"Sitemap: {SITE_ORIGIN}/{SITEMAP_STATIC_NAME}")
    print(f"URLs listed: {len(locs)} (expected deploy set: {url_count(root)})")
    print()
    for loc in locs:
        print(f"  {loc}")
    print()
    print("Submit in Google Search Console (required for recrawl):")
    print("  1. Open https://search.google.com/search-console")
    print("  2. Property: https://www.workofarttattoo.com/")
    print(f"  3. Sitemaps → Add: {SITEMAP_STATIC_NAME}")
    print("  4. URL Inspection → enter homepage → Request indexing")
    print(f"  5. Repeat URL Inspection for: {SITE_ORIGIN}/geo_hub_ai_source_of_truth_work_of_art/")
    print()
    print("Note: sitemap.xml is a sitemap index; page URLs live in sitemap-static-pages.xml.")
    print("robots.txt points crawlers to /sitemap.xml only (no duplicate sitemap entries).")
    print("After deploy, verify:")
    print(f"  curl -sI {SITE_ORIGIN}/{SITEMAP_STATIC_NAME} | head -5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
