#!/usr/bin/env python3
"""Compare live workofarttattoo.com signals to repo canonical NAP and SEO."""

from __future__ import annotations

import csv
import re
import ssl
import urllib.request
from pathlib import Path

from woa_nav_config import (
    HOME_SLUG,
    HOME_TITLE,
    ROOT_A,
    STUDIO_BOOKING_EMAIL,
    STUDIO_PHONE_DISPLAY,
    STUDIO_STREET_ADDRESS,
)
from woa_sitemap import discover_deploy_urls

SITE = "https://workofarttattoo.com"
ROOT = ROOT_A
OUT = ROOT / "live_vs_repo_checklist.csv"

CHECKS: tuple[tuple[str, str, str], ...] = (
    ("/", "Homepage title", HOME_TITLE),
    ("/", "Canonical phone", STUDIO_PHONE_DISPLAY),
    ("/", "Canonical address", STUDIO_STREET_ADDRESS),
    ("/", "Business email", STUDIO_BOOKING_EMAIL),
    ("/", "Grouped knowledge vault (woa-kb-group)", "present"),
    ("/", "No 'elite artistry' in FAQ", "absent"),
    ("/artists/joshua-cole/", "Joshua title contains 'Realism Tattoo Artist'", "present"),
    ("/artists/joshua-cole/", "No keyword-stuffed title (five star nose)", "absent"),
    ("/tattoo_shop_near_mgm_grand_las_vegas/", "Geo: Directions section", "present"),
    ("/helix_piercing_las_vegas_authority_guide/", "Guide video embed", "present"),
    ("/sitemap.xml", "Sitemap URL count vs repo", "match"),
)


def fetch(url: str) -> str:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "WorkOfArt-Audit/1.0"})
    with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="replace")


def title_of(html: str) -> str:
    m = re.search(r"<title>([^<]*)</title>", html, re.I)
    return m.group(1).strip() if m else ""


def evaluate(path: str, check: str, expected: str, html: str) -> tuple[str, str, str]:
    if check == "Homepage title":
        live = title_of(html)
        status = "PASS" if live == expected.replace("&", "&amp;") or live == expected else "FAIL"
        return status, live, expected
    if check == "Canonical phone":
        found = STUDIO_PHONE_DISPLAY in html or "(725) 224-1240" in html
        bad = any(x in html for x in ("224-2617", "960-9607", "5025"))
        status = "PASS" if found and not bad else "FAIL"
        return status, "725-224-1240 found" if found else "missing", expected
    if check == "Canonical address":
        bad = "5025" in html
        good = STUDIO_STREET_ADDRESS in html or "2375 E. Tropicana" in html
        status = "PASS" if good and not bad else "FAIL"
        return status, "2375 present" if good else "missing/wrong", expected
    if check == "Business email":
        bad = "gmail.com" in html.lower()
        good = STUDIO_BOOKING_EMAIL in html
        status = "PASS" if good and not bad else "FAIL"
        return status, STUDIO_BOOKING_EMAIL if good else "missing", expected
    if expected == "present":
        ok = check.split(" (")[0].lower() in html.lower() or (
            check == "Grouped knowledge vault (woa-kb-group)" and 'class="woa-kb-group"' in html
        ) or (
            check == "Joshua title contains 'Realism Tattoo Artist'"
            and "Realism Tattoo Artist" in title_of(html)
        ) or (
            check == "Geo: Directions section" and "Directions from" in html
        ) or (
            check == "Guide video embed" and 'data-woa-guide-video="1"' in html
        )
        status = "PASS" if ok else "FAIL"
        return status, "present" if ok else "missing", expected
    if expected == "absent":
        needles = {
            "No 'elite artistry' in FAQ": "elite artistry",
            "No keyword-stuffed title (five star nose)": "five star nose",
        }
        needle = needles.get(check, "")
        ok = needle.lower() not in html.lower()
        status = "PASS" if ok else "FAIL"
        return status, "absent" if ok else f"found '{needle}'", expected
    return "SKIP", "", expected


def main() -> int:
    repo_count = len(discover_deploy_urls(ROOT))
    cache: dict[str, str] = {}
    rows: list[dict[str, str]] = []

    for path, check, expected in CHECKS:
        if path == "/sitemap.xml":
            try:
                xml = fetch(f"{SITE}/sitemap.xml")
                live_count = xml.count("<loc>")
                status = "PASS" if live_count == repo_count else "WARN"
                rows.append(
                    {
                        "url": f"{SITE}/sitemap.xml",
                        "check": check,
                        "status": status,
                        "live_value": str(live_count),
                        "expected": str(repo_count),
                        "action": "OK" if status == "PASS" else "Re-deploy + resubmit sitemap",
                    }
                )
            except OSError as exc:
                rows.append(
                    {
                        "url": f"{SITE}/sitemap.xml",
                        "check": check,
                        "status": "ERROR",
                        "live_value": str(exc),
                        "expected": str(repo_count),
                        "action": "Retry fetch",
                    }
                )
            continue

        url = SITE + (path if path.endswith("/") else path + "/")
        if path not in cache:
            try:
                cache[path] = fetch(url)
            except OSError as exc:
                rows.append(
                    {
                        "url": url,
                        "check": check,
                        "status": "ERROR",
                        "live_value": str(exc),
                        "expected": expected,
                        "action": "Retry fetch",
                    }
                )
                continue
        html = cache[path]
        status, live_val, exp = evaluate(path, check, expected, html)
        action = "OK"
        if status == "FAIL":
            if "woa-kb-group" in check or "elite artistry" in check or "Guide video" in check:
                action = "Run prepare_seo.py + deploy"
            elif check == "Homepage title":
                action = "Run fix_homepage_seo.py + deploy"
            else:
                action = "Verify repo + deploy"
        rows.append(
            {
                "url": url,
                "check": check,
                "status": status,
                "live_value": live_val,
                "expected": exp,
                "action": action,
            }
        )

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["url", "check", "status", "live_value", "expected", "action"],
        )
        writer.writeheader()
        writer.writerows(rows)

    fails = sum(1 for r in rows if r["status"] == "FAIL")
    print(f"Wrote {OUT} ({len(rows)} checks, {fails} FAIL)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
