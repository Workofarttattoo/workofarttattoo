#!/usr/bin/env python3
"""Inventory Work of Art piercing pages and produce a no-spam growth report."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
AUDITS = ROOT / "audits"
SITE = "https://www.workofarttattoo.com"

PIERCING_TERMS = re.compile(
    r"\b(pierc(?:e|ing|ings)|katelyn|helix|conch|tragus|daith|rook|septum|nostril|labret|philtrum|navel|nipple|industrial|ear curation|jewelry|downsizing|butterfly backs?)\b",
    re.I,
)
TATTOO_TERMS = re.compile(
    r"\b(tattoo|tattoos|realism|cover[-\s]?up|fine[-\s]?line|skull|lion|forearm|sleeve|portrait)\b",
    re.I,
)
PIERCING_IMAGE_TERMS = re.compile(
    r"(piercing|helix|conch|tragus|daith|rook|septum|nostril|labret|eyebrow|lobe|industrial|jewelry|ear-curation|cartilage)",
    re.I,
)
TATTOO_PROOF_IMAGE_TERMS = re.compile(
    r"(skull-hourglass|roaring-lion|all-seeing-eye|eagle-memorial|cover-up-tattoo|black-grey-lion|forearm-realism)",
    re.I,
)
COMMERCIAL_TERMS = re.compile(r"\b(book|appointment|call|text|price|cost|walk-in|same-day|consult|directions)\b", re.I)
LOCAL_TERMS = re.compile(r"\b(Las Vegas|Tropicana|Strip|MGM|airport|Sphere|UNLV|Fremont|Henderson|parking|rideshare)\b", re.I)


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel == Path("code.html"):
        return "/"
    return "/" + str(rel.parent).strip("/") + "/"


def visible_text(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return " ".join(soup.get_text(" ").split())


def canonical_url(soup: BeautifulSoup, route: str) -> str:
    tag = soup.find("link", rel="canonical")
    if tag and tag.get("href"):
        return str(tag["href"])
    return SITE + route


def intent_bucket(route: str, title: str, h1: str) -> str:
    hay = f"{route} {title} {h1}".lower()
    if "aftercare" in hay or "healing" in hay:
        return "piercing aftercare/healing"
    if "jewelry" in hay or "downsizing" in hay or "butterfly" in hay:
        return "piercing jewelry/downsizing"
    if any(x in hay for x in ("helix", "conch", "tragus", "rook", "daith", "industrial", "lobe", "ear_")):
        return "ear piercing placement"
    if any(x in hay for x in ("nostril", "septum", "eyebrow", "bridge")):
        return "facial piercing placement"
    if any(x in hay for x in ("labret", "philtrum", "tongue", "monroe")):
        return "oral piercing placement"
    if any(x in hay for x in ("navel", "nipple", "surface")):
        return "body piercing placement"
    if "katelyn" in hay:
        return "Katelyn piercing entity"
    if any(x in hay for x in ("near_", "serving_", "strip", "airport", "sphere", "unlv")):
        return "local visitor mixed tattoo/piercing"
    return "piercing commercial hub"


def indexable(soup: BeautifulSoup) -> bool:
    robots = soup.find("meta", attrs={"name": re.compile("^robots$", re.I)})
    if robots and "noindex" in str(robots.get("content", "")).lower():
        return False
    return True


def row_for(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")
    text = visible_text(BeautifulSoup(raw, "html.parser"))
    route = route_for(path)
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    h1 = soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else ""
    imgs = [str(img.get("src", "")) + " " + str(img.get("alt", "")) for img in soup.find_all("img")]
    piercing_imgs = [img for img in imgs if PIERCING_IMAGE_TERMS.search(img)]
    tattoo_imgs = [img for img in imgs if TATTOO_PROOF_IMAGE_TERMS.search(img)]
    links = [
        a.get("href", "")
        for a in soup.find_all("a", href=True)
        if str(a.get("href", "")).startswith("/")
    ]
    contamination = []
    if tattoo_imgs and "piercing" in route.lower():
        contamination.append("tattoo proof image")
    if re.search(r"send\s+a\s+reference\s+photo[^.]{0,100}timeline", text, re.I) and "piercing" in route.lower():
        contamination.append("tattoo reference-photo CTA")
    if re.search(r"professional piercer|medical-grade|APP-aligned|surgical steel|316L", text, re.I):
        contamination.append("unverified piercing credential/material wording")
    commercial = bool(COMMERCIAL_TERMS.search(text))
    local = bool(LOCAL_TERMS.search(text))
    intent = intent_bucket(route, title, h1)
    useful_without_google = "yes" if (piercing_imgs or "aftercare" in intent or "placement" in intent or local) else "partial"
    recommendation = "IMPROVE"
    if contamination:
        recommendation = "FIX"
    elif intent in {"piercing commercial hub", "piercing aftercare/healing", "piercing jewelry/downsizing"} and piercing_imgs:
        recommendation = "KEEP"
    elif intent.endswith("placement") and piercing_imgs and commercial:
        recommendation = "KEEP"
    elif not commercial and not local:
        recommendation = "IMPROVE"
    return {
        "url": SITE + route,
        "route": route,
        "title": title,
        "h1": h1,
        "indexable": "yes" if indexable(soup) else "no",
        "unique_search_intent": intent,
        "unique_firsthand_information": "yes" if "Katelyn" in text or "I " in text else "partial",
        "original_studio_imagery": "yes" if piercing_imgs else "no",
        "original_artist_commentary": "yes" if "Katelyn" in text and re.search(r"\bI\b|\bmy\b", text) else "partial",
        "unique_factual_information": "yes" if ("Pain" in text or "Healing" in text or local) else "partial",
        "inbound_internal_links_estimate": "pending graph pass",
        "overlap_bucket": intent,
        "commercial_usefulness": "yes" if commercial else "partial",
        "local_usefulness": "yes" if local else "partial",
        "deserves_to_exist_without_google": useful_without_google,
        "problems": "; ".join(contamination),
        "recommendation": recommendation,
        "canonical": canonical_url(soup, route),
        "internal_links_out": str(len(set(links))),
    }


def collect_rows() -> list[dict[str, str]]:
    rows = []
    for path in sorted(ROOT.rglob("code.html")):
        if ".git" in path.parts:
            continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        route = route_for(path)
        if PIERCING_TERMS.search(raw) or PIERCING_TERMS.search(route):
            rows.append(row_for(path))
    return rows


def write_inventory(rows: list[dict[str, str]]) -> None:
    AUDITS.mkdir(exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else [
        "url",
        "route",
        "title",
        "h1",
        "recommendation",
    ]
    with (AUDITS / "piercing-seo-inventory.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_cannibalization(rows: list[dict[str, str]]) -> None:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["overlap_bucket"]].append(row)
    with (AUDITS / "piercing-cannibalization-map.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["overlap_bucket", "page_count", "recommended_action", "urls"])
        writer.writeheader()
        for bucket, items in sorted(groups.items()):
            action = "Keep hub + strongest clusters; improve, do not multiply."
            if len(items) > 8 and "placement" not in bucket:
                action = "Consolidate weak variants into hub sections; no new pages."
            writer.writerow(
                {
                    "overlap_bucket": bucket,
                    "page_count": len(items),
                    "recommended_action": action,
                    "urls": " | ".join(item["url"] for item in items[:30]),
                }
            )


def write_report(rows: list[dict[str, str]]) -> None:
    counts = defaultdict(int)
    for row in rows:
        counts[row["recommendation"]] += 1
    missing = [
        "Piercing prices: improve only with owner-verified prices; otherwise explain quote factors.",
        "Same-day piercings: keep call/text-first language unless actual recurring availability is verified.",
        "Jewelry materials: publish specific metal/brand claims only after owner verification.",
        "Troubleshooting intent: strengthen bump, irritation, downsizing, sleeping, pool, and travel advice inside the existing aftercare/jewelry hubs.",
    ]
    improve = [r for r in rows if r["recommendation"] in {"FIX", "IMPROVE"}][:20]
    body = f"""# Piercing SEO Growth Inventory

Generated from local repository HTML after the source audit. This sprint should improve existing hubs and clusters rather than create dozens of new pages.

## Inventory Summary

- Piercing-related pages found: {len(rows)}
- KEEP/FIX/IMPROVE counts: {dict(sorted(counts.items()))}
- New large-scale page creation recommended: no
- Recommended new pages: none until pricing, jewelry-material, and same-day availability facts are owner-verified

## Missing Intents To Strengthen In Existing Pages

{chr(10).join(f"- {item}" for item in missing)}

## Pages To Improve First

{chr(10).join(f"- {r['route']} — {r['recommendation']} — {r['problems'] or r['unique_search_intent']}" for r in improve)}

## Pages Worth Creating

- No new pages in this pass. Use the existing piercing hub, Katelyn topic hub, aftercare guide, jewelry guide, and placement clusters.

## Pages Not Worth Creating

- Separate “piercing near [every neighborhood]” pages.
- Duplicate helix/conch/nostril pages for “near me,” “walk-in,” “cheap,” or “best” variants.
- Jewelry-brand or material pages until the shop owner verifies current inventory/material claims.
- Price pages with exact dollar amounts until prices are verified.

## Implementation Direction

- Replace tattoo proof strips on piercing pages with real piercing imagery.
- Route piercing commercial pages to piercing-specific CTAs.
- Keep Katelyn central as the piercer entity without unsupported credential claims.
- Add concise piercing-planning blocks to useful local pages instead of doorway pages.
- Use QA to fail if tattoo images or tattoo CTAs return to piercing routes.
"""
    (AUDITS / "piercing-seo-growth-report.md").write_text(body, encoding="utf-8")


def main() -> int:
    rows = collect_rows()
    write_inventory(rows)
    write_cannibalization(rows)
    write_report(rows)
    print(f"[ok] piercing inventory pages: {len(rows)}")
    print("[ok] audits/piercing-seo-inventory.csv")
    print("[ok] audits/piercing-cannibalization-map.csv")
    print("[ok] audits/piercing-seo-growth-report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
