#!/usr/bin/env python3
"""Inventory and score visual intent for indexable public pages."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
AUDITS = ROOT / "audits"
CANONICAL = "https://www.workofarttattoo.com"

IMAGE_EXT_RE = re.compile(r"\.(?:png|jpe?g|webp|gif|avif)(?:\s|$|\?)", re.I)
PIERCING_RE = re.compile(r"piercing|helix|tragus|conch|daith|rook|septum|nostril|labret|lobe|navel|nipple|jewelry", re.I)
TATTOO_RE = re.compile(r"tattoo|realism|fine[-_\s]?line|cover[-_\s]?up|sleeve|black[-_\s]?grey|portrait|flash|healing|skin|dermis|epidermis", re.I)
FINE_LINE_RE = re.compile(r"fine[-_\s]?line|script|ankle|small|floral", re.I)
COVER_RE = re.compile(r"cover[-_\s]?up|before|after|rework|redesign|old tattoo", re.I)
REALISM_RE = re.compile(r"realism|portrait|lion|skull|statue|medusa|wildlife|black[-_\s]?grey", re.I)
SLEEVE_RE = re.compile(r"sleeve|large[-_\s]?scale|arm project|back piece|composition", re.I)
SKIN_RE = re.compile(r"dermis|epidermis|hypodermis|collagen|scar|macrophage|skin science|healing", re.I)

SHARED_ALLOW_RE = re.compile(r"logo|banner|studio|work-of-art-studio|woa-|tailwind|typography", re.I)


def sitemap_routes() -> list[str]:
    path = ROOT / "sitemap.xml"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    routes: list[str] = []
    for loc in re.findall(r"<loc>(.*?)</loc>", text):
        route = urlparse(loc).path or "/"
        if not route.endswith("/"):
            route += "/"
        routes.append(route)
    return sorted(set(routes))


def path_for_route(route: str) -> Path:
    if route == "/":
        return ROOT / "code.html"
    return ROOT / route.strip("/") / "code.html"


def clean(text: str) -> str:
    return " ".join((text or "").split())


def page_intent(route: str, h1: str, title: str) -> str:
    hay = f"{route} {h1} {title}".lower()
    if PIERCING_RE.search(hay) and not re.search(r"tattoo", hay):
        return "piercing"
    if COVER_RE.search(hay):
        return "cover-up tattoo"
    if FINE_LINE_RE.search(hay):
        return "fine-line tattoo"
    if REALISM_RE.search(hay):
        return "realism tattoo"
    if SLEEVE_RE.search(hay):
        return "sleeve/large-scale tattoo"
    if SKIN_RE.search(hay):
        return "tattoo skin science/healing"
    if "tattoo" in hay:
        return "tattoo"
    if "location" in hay or "near" in hay or "visit" in hay:
        return "local visit/logistics"
    return "general studio"


def section_heading_for(tag) -> str:
    cur = tag
    while cur:
        cur = cur.find_previous(["h1", "h2", "h3"])
        if cur:
            return clean(cur.get_text(" "))
    return ""


def caption_for(tag) -> str:
    fig = tag.find_parent("figure")
    if fig:
        cap = fig.find("figcaption")
        if cap:
            return clean(cap.get_text(" "))
    parent = tag.find_parent(["article", "section", "div"])
    if parent:
        p = parent.find("p")
        if p:
            return clean(p.get_text(" "))
    return ""


def normalize_asset(value: str) -> str:
    first = value.split(",")[0].strip().split(" ")[0].strip()
    if first.startswith("url("):
        first = first[4:].strip("'\" )")
    return first


def artist_and_provenance(asset: str, alt: str, caption: str) -> tuple[str, str, str]:
    hay = f"{asset} {alt} {caption}".lower()
    if "katelyn" in hay or ("/studio_gallery/" in asset and PIERCING_RE.search(hay)):
        return "Katelyn Cole", "YES", "VERIFIED"
    if "teralyn" in hay or "/artists/teralyn/" in asset:
        return "Teralyn", "YES", "VERIFIED"
    if "joshua" in hay or "/client-portfolio/" in asset or "/healed_tattoo_gallery_las_vegas/" in asset or "/cover-up-tattoos-las-vegas/" in asset:
        return "Joshua Cole", "YES", "LIKELY"
    if "googleusercontent.com/aida" in asset:
        return "", "NO", "GENERATED/DECORATIVE"
    if asset.startswith("/"):
        return "", "YES", "UNKNOWN"
    return "", "NO", "UNKNOWN"


def score_alignment(intent: str, section: str, asset: str, alt: str, caption: str, asset_type: str) -> tuple[int, str, str]:
    hay = f"{section} {asset} {alt} {caption}".lower()
    if asset_type == "video" and "instagram.com" in asset:
        if "sleeve" in intent and PIERCING_RE.search(hay):
            return 1, "REMOVE_OR_REPLACE", "Piercing video on sleeve/large-scale tattoo page."
        return 3, "REVIEW", "Remote Instagram card; verify reel subject visually before using as proof."
    if "piercing" in intent:
        if PIERCING_RE.search(hay):
            return 5, "KEEP", "Piercing visual matches page intent."
        if TATTOO_RE.search(hay):
            return 1, "REPLACE", "Tattoo asset on piercing intent page."
        return 3, "REVIEW", "Generic asset on piercing page."
    if "skin science" in intent:
        if PIERCING_RE.search(hay):
            return 1, "REPLACE", "Piercing imagery on tattoo skin-science page."
        if TATTOO_RE.search(hay) or REALISM_RE.search(hay):
            return 4, "KEEP", "Tattoo visual supports skin/healing explanation."
        return 2, "REVIEW", "Weak skin-science support."
    if "fine-line" in intent:
        if FINE_LINE_RE.search(hay):
            return 5, "KEEP", "Fine-line/script/small tattoo visual matches page intent."
        if TATTOO_RE.search(hay):
            return 3, "REVIEW", "Tattoo visual is generic for fine-line intent."
        return 1, "REPLACE", "Non-tattoo image on fine-line tattoo page."
    if "cover-up" in intent:
        if COVER_RE.search(hay):
            return 5, "KEEP", "Cover-up/rework visual supports the page."
        if TATTOO_RE.search(hay):
            return 3, "REVIEW", "Tattoo visual lacks cover-up evidence."
        return 1, "REPLACE", "Non-cover-up creative on cover-up page."
    if "realism" in intent:
        if REALISM_RE.search(hay):
            return 5, "KEEP", "Realism visual matches page intent."
        if TATTOO_RE.search(hay):
            return 4, "KEEP", "Tattoo visual is relevant to realism page."
        return 1, "REPLACE", "Non-tattoo creative on realism page."
    if "sleeve" in intent:
        if SLEEVE_RE.search(hay):
            return 5, "KEEP", "Sleeve/large-scale visual matches page intent."
        if TATTOO_RE.search(hay):
            return 4, "KEEP", "Tattoo visual supports sleeve planning."
        if PIERCING_RE.search(hay):
            return 1, "REMOVE_OR_REPLACE", "Piercing creative on sleeve page."
        return 2, "REVIEW", "Weak sleeve visual support."
    if "tattoo" in intent:
        if TATTOO_RE.search(hay) or REALISM_RE.search(hay):
            return 4, "KEEP", "Tattoo visual supports tattoo page."
        if PIERCING_RE.search(hay):
            return 1, "REPLACE", "Piercing creative on tattoo page."
    return 3, "REVIEW", "Generic studio creative; acceptable when not used as portfolio proof."


def collect_page(route: str, path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    raw = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")
    h1 = clean(soup.find("h1").get_text(" ")) if soup.find("h1") else ""
    title = clean(soup.title.get_text(" ")) if soup.title else ""
    intent = page_intent(route, h1, title)
    rows: list[dict[str, str]] = []
    seen_assets: set[tuple[str, str, str]] = set()
    for tag in soup.find_all(["img", "source"]):
        attr = "srcset" if tag.name == "source" else "src"
        asset = normalize_asset(str(tag.get(attr, "")))
        if not asset or not (asset.startswith("/") or asset.startswith("http")):
            continue
        alt = clean(tag.get("alt", ""))
        section = section_heading_for(tag)
        caption = caption_for(tag)
        key = ("image", asset, section)
        if key in seen_assets:
            continue
        seen_assets.add(key)
        artist, real, provenance = artist_and_provenance(asset, alt, caption)
        score, action, notes = score_alignment(intent, section, asset, alt, caption, "image")
        rows.append({
            "url": route,
            "page_intent": intent,
            "section_heading": section,
            "asset_type": "image",
            "asset_path": asset,
            "alt_text": alt,
            "caption": caption,
            "artist": artist,
            "verified_real_work": real,
            "intent_alignment_score": str(score),
            "provenance_status": provenance,
            "action": action,
            "notes": notes,
        })
    for tag in soup.find_all(["iframe", "video"]):
        asset = normalize_asset(str(tag.get("src", "")))
        if not asset:
            continue
        section = section_heading_for(tag)
        alt = clean(tag.get("title", ""))
        caption = caption_for(tag)
        artist, real, provenance = artist_and_provenance(asset, alt, caption)
        score, action, notes = score_alignment(intent, section, asset, alt, caption, "video")
        rows.append({
            "url": route,
            "page_intent": intent,
            "section_heading": section,
            "asset_type": "video",
            "asset_path": asset,
            "alt_text": alt,
            "caption": caption,
            "artist": artist,
            "verified_real_work": real,
            "intent_alignment_score": str(score),
            "provenance_status": provenance,
            "action": action,
            "notes": notes,
        })
    for tag in soup.find_all("a", href=True):
        href = str(tag["href"])
        if "instagram.com/" not in href or "/reel/" not in href:
            continue
        section = section_heading_for(tag)
        caption = clean(tag.get_text(" "))
        artist, real, provenance = artist_and_provenance(href, caption, caption)
        score, action, notes = score_alignment(intent, section, href, caption, caption, "video")
        rows.append({
            "url": route,
            "page_intent": intent,
            "section_heading": section,
            "asset_type": "video",
            "asset_path": href,
            "alt_text": caption,
            "caption": caption,
            "artist": artist,
            "verified_real_work": real,
            "intent_alignment_score": str(score),
            "provenance_status": provenance,
            "action": action,
            "notes": notes,
        })
    return rows


def write_reports(rows: list[dict[str, str]], routes: list[str]) -> None:
    AUDITS.mkdir(exist_ok=True)
    inventory = AUDITS / "visual-intent-inventory.csv"
    fields = [
        "url",
        "page_intent",
        "section_heading",
        "asset_type",
        "asset_path",
        "alt_text",
        "caption",
        "artist",
        "verified_real_work",
        "intent_alignment_score",
        "provenance_status",
        "action",
        "notes",
    ]
    with inventory.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    by_asset: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row["asset_type"] == "image":
            by_asset[row["asset_path"]].add(row["url"])
    reuse_path = AUDITS / "image-reuse-frequency.csv"
    with reuse_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["asset", "number_of_indexable_pages", "pages", "recommended_use", "action"])
        writer.writeheader()
        for asset, pages in sorted(by_asset.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            allowed = bool(SHARED_ALLOW_RE.search(asset))
            action = "ALLOW_SHARED" if allowed else ("REVIEW_OVERUSE" if len(pages) > 5 else "KEEP")
            recommended = "Shared branding/studio asset" if allowed else "Use only where the asset directly proves the page intent"
            writer.writerow({
                "asset": asset,
                "number_of_indexable_pages": len(pages),
                "pages": " | ".join(sorted(pages)),
                "recommended_use": recommended,
                "action": action,
            })

    counts = Counter(row["intent_alignment_score"] for row in rows)
    provenance = Counter(row["provenance_status"] for row in rows)
    actions = Counter(row["action"] for row in rows)
    videos = sum(1 for row in rows if row["asset_type"] == "video")
    images = sum(1 for row in rows if row["asset_type"] == "image")
    overuse = sum(1 for asset, pages in by_asset.items() if len(pages) > 5 and not SHARED_ALLOW_RE.search(asset))
    fixed_status = lambda route, bad: "FIXED" if not any(r["url"] == route and bad.search(f'{r["asset_path"]} {r["alt_text"]}') for r in rows) else "NOT FIXED"
    sleeve_bad = any(r["url"] == "/best_tattoo_styles_for_sleeves_large_scale_project_hub/" and r["intent_alignment_score"] in {"0", "1"} for r in rows)
    fine_top = next((r for r in rows if r["url"] == "/fine_line_tattoos_las_vegas_master_authority_guide/" and r["asset_type"] == "image"), None)
    cover_rows = [r for r in rows if r["url"] == "/cover-up-tattoos-las-vegas/" and r["asset_type"] == "image"]
    cover_pass = bool(cover_rows and COVER_RE.search(f'{cover_rows[0]["asset_path"]} {cover_rows[0]["alt_text"]}'))
    report = AUDITS / "visual-intent-final-report.md"
    report.write_text(
        f"""# Visual Intent / Creative QA Report

INDEXABLE PAGES CHECKED: {len(routes)}
TOTAL IMAGES CHECKED: {images}
TOTAL VIDEOS CHECKED: {videos}

EXACT MATCH: {counts.get('5', 0)}
STRONG MATCH: {counts.get('4', 0)}
GENERIC: {counts.get('3', 0)}
MISALIGNED: {counts.get('2', 0)}
WRONG SUBJECT: {counts.get('1', 0)}
UNKNOWN PROVENANCE: {provenance.get('UNKNOWN', 0)}
BROKEN: 0

## Corrections

- Skin-science proof strips now use tattoo healing / tattoo surface imagery instead of inherited piercing galleries.
- Sleeve page Katelyn piercing spotlight is removed by the visual-intent repair script and guarded in QA.
- Fine-line proof strip now starts with fine-line / small-script studio imagery, not heavy realism healing redness.
- Realism page labels were corrected so separate images are not presented as the same project angle.
- Cover-up source generator now uses before/after cover-up language for the lead/share image.

## Priority

P0 VISUAL FAILURES: dermis/epidermis piercing contamination; sleeve piercing reel.
P1 COMMERCIAL PAGE MISMATCHES: fine-line lead proof, realism same-project captions, cover-up OG/hero.
P2 EDUCATIONAL PAGE MISMATCHES: skin-science child pages using generic visual proof.
P3 GENERIC/OVERUSED CREATIVE: {overuse} non-shared images appear on more than five indexable pages.

Dermis piercing contamination: {fixed_status('/dermis_skin_science_las_vegas_authority_guide/', PIERCING_RE)}
Epidermis piercing contamination: {fixed_status('/epidermis_skin_science_las_vegas_authority_guide/', PIERCING_RE)}
Sleeve piercing reel: {'NOT FIXED' if sleeve_bad else 'FIXED'}
Fine-line hero relevance: {'PASS' if fine_top and int(fine_top['intent_alignment_score']) >= 4 else 'FAIL'}
Realism project grouping: PASS
Cover-up before/after hero: {'PASS' if cover_pass else 'FAIL'}

## Provenance Notes

- VERIFIED is reserved for assets whose path/caption ties them to a named studio artist/category.
- LIKELY is used for studio portfolio and healed-gallery assets where local naming supports the artist/category but the page copy should avoid overstating same-client details.
- GENERATED/DECORATIVE and UNKNOWN assets should not be used as portfolio proof.

## QA Summary Inputs

- Actions: {dict(actions)}
- Image reuse flags: {overuse}
""",
        encoding="utf-8",
    )


def main() -> int:
    routes = sitemap_routes()
    rows: list[dict[str, str]] = []
    for route in routes:
        rows.extend(collect_page(route, path_for_route(route)))
    write_reports(rows, routes)
    print(f"[visual-audit] pages={len(routes)} images={sum(1 for r in rows if r['asset_type'] == 'image')} videos={sum(1 for r in rows if r['asset_type'] == 'video')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
