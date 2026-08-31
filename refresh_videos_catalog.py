#!/usr/bin/env python3
"""
Rebuild videos_catalog_merged.json from:
  1) Curated entries in client_videos (FEATURED_HOME, CLIENT_VIDEOS, KATELYN_VIDEOS,
     JOSHUA_EDUCATION_REEL_ID, KATELYN_MINORS_REEL_ID).
  2) Every Instagram shortcode found in *.html under this repo (reel, p, tv).
  3) Manual extras: instagram_reels_inventory.json (never gitignored).
  4) Optional Instagram Graph (user media): set env INSTAGRAM_ACCESS_TOKEN and run
     with --fetch-api  (uses graph.instagram.com — token must have instagram_graph_user_media).

  Then run:  python3 build_studio_videos_page.py && python3 inject_client_videos.py
  and:      python3 inject_page_spotlights.py
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
CATALOG_OUT = ROOT / "videos_catalog_merged.json"
INVENTORY = ROOT / "instagram_reels_inventory.json"

IG_URL_RE = re.compile(
    r"https://www\.instagram\.com/(?:reel|p|tv)/([A-Za-z0-9_-]+)/?",
    re.IGNORECASE,
)


def _entry(kind: str, media_id: str, title: str, blurb: str = "") -> dict[str, str]:
    return {"kind": kind, "media_id": media_id, "title": title, "blurb": blurb}


def curated_ordered() -> list[dict[str, str]]:
    from client_videos import (
        CLIENT_VIDEOS,
        FEATURED_HOME,
        KATELYN_MINORS_REEL_ID,
        KATELYN_VIDEOS,
        JOSHUA_EDUCATION_REEL_ID,
    )

    out: list[dict[str, str]] = []
    seen: set[str] = set()

    def push(raw: dict[str, str], title_fallback: str) -> None:
        mid = raw.get("media_id") or raw.get("post_id") or ""
        if not mid or mid in seen:
            return
        seen.add(mid)
        out.append(
            _entry(
                raw.get("kind", "post"),
                mid,
                raw.get("title") or title_fallback,
                raw.get("blurb", ""),
            )
        )

    push(FEATURED_HOME, "Studio interview")

    for row in CLIENT_VIDEOS:
        push(row, "Work of Art reel")

    push(
        {
            "kind": "reel",
            "media_id": JOSHUA_EDUCATION_REEL_ID,
            "title": "Joshua Cole — seminars & advanced training",
            "blurb": "Continuing education reel from Joshua’s artist page.",
        },
        "Joshua Cole — seminars & advanced training",
    )

    push(
        {
            "kind": "reel",
            "media_id": KATELYN_MINORS_REEL_ID,
            "title": "Minor ear piercing — how Katelyn does it",
            "blurb": "Families & guardians — reel from piercing minors section.",
        },
        "Minor ear piercing — how Katelyn does it",
    )

    for row in KATELYN_VIDEOS:
        push(row, "Katelyn Cole — studio reel")

    return out


def scan_html_for_shortcodes() -> list[tuple[str, str]]:
    """Return (kind_guess, media_id) pairs in discovery order."""
    found: list[tuple[str, str]] = []

    def kind_for_url(fragment: str) -> str:
        low = fragment.lower()
        return "post" if "/p/" in low else "reel"

    for path in sorted(ROOT.rglob("*.html")):
        if any(
            skip in path.parts
            for skip in (
                ".git",
                "skipped_upload_build",
                "node_modules",
            )
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in IG_URL_RE.finditer(text):
            full = m.group(0)
            mid = m.group(1)
            found.append((kind_for_url(full), mid))

    return found


def load_inventory_file() -> list[dict[str, str]]:
    if not INVENTORY.is_file():
        return []
    try:
        data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    items = data.get("items") if isinstance(data, dict) else data
    if not isinstance(items, list):
        return []
    rows: list[dict[str, str]] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        mid = it.get("media_id") or it.get("shortcode") or ""
        if not mid:
            continue
        rows.append(
            _entry(
                str(it.get("kind", "reel")),
                str(mid),
                str(it.get("title", "Instagram clip")),
                str(it.get("blurb", "")),
            )
        )
    return rows


def fetch_instagram_graph_media(token: str) -> list[tuple[str, str]]:
    """
    Basic Display / IG User: GET graph.instagram.com/me/media
    Requires token with appropriate scopes; may return empty on error.
    """
    rows: list[tuple[str, str]] = []
    q = urllib.parse.urlencode(
        {
            "fields": "id,media_type,permalink,thumbnail_url",
            "limit": "50",
            "access_token": token,
        }
    )
    next_url: str | None = f"https://graph.instagram.com/me/media?{q}"
    while next_url:
        req = urllib.request.Request(
            next_url,
            headers={"User-Agent": "Mozilla/5.0 WOA-catalog-refresh"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
            break

        for item in payload.get("data") or []:
            link = item.get("permalink") or ""
            m = IG_URL_RE.search(link)
            if not m:
                continue
            mid = m.group(1)
            mt = (item.get("media_type") or "").upper()
            kind = "reel" if mt == "REELS" else "post"
            rows.append((kind, mid))

        paging = payload.get("paging") or {}
        next_url = paging.get("next")

    return rows


def merge_catalog(fetch_api: bool) -> list[dict[str, Any]]:
    from client_videos import is_site_video_allowed

    seen: set[str] = set()
    merged: list[dict[str, Any]] = []

    def add(kind: str, mid: str, title: str, blurb: str = "") -> None:
        if not mid or mid in seen or not is_site_video_allowed(mid):
            return
        seen.add(mid)
        merged.append({"kind": kind, "media_id": mid, "title": title, "blurb": blurb})

    for row in curated_ordered():
        add(row["kind"], row["media_id"], row["title"], row["blurb"])

    if fetch_api:
        tok = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "").strip()
        if tok:
            for kind, mid in fetch_instagram_graph_media(tok):
                add(kind, mid, "Instagram — fetched media", "")
        else:
            print("warning: --fetch-api set but INSTAGRAM_ACCESS_TOKEN is empty")

    for kind_guess, mid in scan_html_for_shortcodes():
        add(kind_guess, mid, "Work of Art — Instagram clip", "")

    for row in load_inventory_file():
        add(row["kind"], row["media_id"], row["title"], row["blurb"])

    return merged


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--fetch-api",
        action="store_true",
        help="Also call Instagram Graph me/media using INSTAGRAM_ACCESS_TOKEN",
    )
    args = ap.parse_args()

    merged = merge_catalog(fetch_api=args.fetch_api)
    CATALOG_OUT.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {CATALOG_OUT} ({len(merged)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
