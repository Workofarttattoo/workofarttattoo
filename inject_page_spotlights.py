#!/usr/bin/env python3
"""Inject a single Instagram studio clip on static pages (deterministic by slug).

Skips the homepage, full video library page, and pages that already host many embeds.
Idempotent: replaces WOA_PAGE_SPOTLIGHT markers when re-run.

  python3 inject_page_spotlights.py

Run after:  python3 refresh_videos_catalog.py
           python3 inject_client_videos.py
"""

from __future__ import annotations

import re
import hashlib
from pathlib import Path

from client_videos import (
    KATELYN_VIDEOS,
    PAGE_SPOTLIGHT_MARKER_END,
    PAGE_SPOTLIGHT_MARKER_START,
    load_spotlight_pool,
    render_page_spotlight_strip,
)
from woa_nav_config import HOME_SLUG

ROOT = Path(__file__).resolve().parent
GITHUB = Path("/Users/noone/Downloads/GitHub/workofarttattoo")

SPOTLIGHT_RE = re.compile(
    rf"{re.escape(PAGE_SPOTLIGHT_MARKER_START)}[\s\S]*?{re.escape(PAGE_SPOTLIGHT_MARKER_END)}",
    re.MULTILINE,
)

IGNORE_SLUGS = frozenset(
    {
        HOME_SLUG,
        "studio_videos",
        "skipped_upload_build",
        "skipped_pages_clipboard",
        "skipped_pages_clipboard.html",
        "artists_build",
    }
)
SKIP_HEAVY_SLUGS = frozenset(
    {
        # Already has a full multi-embed client stories grid
        "artists",
    }
)

MAX_EXISTING_INSTAGRAM_EMBEDS = 5

PIERCING_SLUG_RE = re.compile(
    r"(piercing|katelyn|helix|conch|tragus|daith|rook|septum|nostril|labret|philtrum|navel|nipple|industrial|cartilage|lobe|tongue|monroe|eyebrow)",
    re.I,
)


def embed_count(html: str) -> int:
    return len(re.findall(r'instagram\.com/[^"\s>]+/embed', html))


def pick_video(slug: str, pool: list) -> object | None:
    if not pool:
        return None
    h = int(hashlib.sha256(slug.encode("utf-8")).hexdigest(), 16)
    return pool[h % len(pool)]


def spotlight_pool_for_slug(slug: str, default_pool: list) -> list:
    if PIERCING_SLUG_RE.search(slug):
        piercing_pool = [v for v in default_pool if getattr(v, "media_id", "") in {row["media_id"] for row in KATELYN_VIDEOS}]
        return piercing_pool or default_pool
    return default_pool


def inject_block(html: str, slug: str, pool: list) -> tuple[str, bool]:
    v = pick_video(slug, pool)
    if not v:
        return html, False

    block = render_page_spotlight_strip(v)

    if PAGE_SPOTLIGHT_MARKER_START in html:
        new_html, n = SPOTLIGHT_RE.subn(block, html, count=1)
        return new_html, n > 0

    if embed_count(html) > MAX_EXISTING_INSTAGRAM_EMBEDS:
        return html, False

    m = re.search(r"\n(<footer\s)", html)
    if not m:
        return html, False

    insert_at = m.start(0)
    return html[:insert_at] + "\n" + block + html[insert_at:], True


def process_file(path: Path, slug: str, pool: list) -> bool:
    raw = path.read_text(encoding="utf-8")
    new_html, ok = inject_block(raw, slug, pool)
    if ok:
        path.write_text(new_html, encoding="utf-8")
        print(f"spotlight {path}")
    return ok


def mirror_rel(rel: Path) -> Path | None:
    cand = GITHUB / rel
    return cand if cand.is_file() else None


def main() -> None:
    pool = load_spotlight_pool()
    if not pool:
        print("empty spotlight pool — run refresh_videos_catalog.py first")
        return

    for folder in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        name = folder.name
        if name.startswith("."):
            continue
        if name in IGNORE_SLUGS:
            continue
        if name in SKIP_HEAVY_SLUGS:
            continue
        code = folder / "code.html"
        if not code.is_file():
            continue
        page_pool = spotlight_pool_for_slug(name, pool)
        ok = process_file(code, name, page_pool)
        mir = mirror_rel(code.relative_to(ROOT))
        if mir:
            mraw = mir.read_text(encoding="utf-8")
            mh, mok = inject_block(mraw, name, page_pool)
            if mok:
                mir.write_text(mh, encoding="utf-8")
                print(f"mirror {mir}")

    artists = ROOT / "artists_build"
    if artists.is_dir():
        for path in sorted(artists.glob("*.html")):
            slug = path.stem.replace("_", "-")
            key = f"artist-{slug}"
            raw = path.read_text(encoding="utf-8")
            if embed_count(raw) > MAX_EXISTING_INSTAGRAM_EMBEDS and PAGE_SPOTLIGHT_MARKER_START not in raw:
                continue
            page_pool = spotlight_pool_for_slug(key, pool)
            new_html, ok = inject_block(raw, key, page_pool)
            if ok:
                path.write_text(new_html, encoding="utf-8")
                print(f"spotlight {path}")
                mir = mirror_rel(Path("artists_build") / path.name)
                if mir:
                    mh, mok = inject_block(mir.read_text(encoding="utf-8"), key, page_pool)
                    if mok:
                        mir.write_text(mh, encoding="utf-8")
                        print(f"mirror {mir}")


if __name__ == "__main__":
    main()
