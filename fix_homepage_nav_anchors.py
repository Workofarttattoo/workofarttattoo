#!/usr/bin/env python3
"""Fix broken homepage anchor targets and top-nav deep links."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
ROOT_HOME = ROOT / "code.html"

REVIEWS_HREF = "/reviews_vault_100_verified_masterpieces/"
STUDIO_VIDEOS_HREF = "/studio_videos/"


def patch_homepage(html: str) -> str:
    html = html.replace(
        '<div class="space-y-8 pt-12 border-t border-outline-variant/20" id="gallery-expanded">',
        '<div class="space-y-8 pt-12 border-t border-outline-variant/20 scroll-mt-28" id="portfolio">',
        1,
    )
    if 'id="gallery"' not in html:
        html = html.replace(
            '<div class="woa-gallery-masonry" id="home-gallery-masonry">',
            '<span class="block scroll-mt-28" id="gallery" aria-hidden="true"></span>\n<div class="woa-gallery-masonry" id="home-gallery-masonry">',
            1,
        )

    html = html.replace(
        'href="#studio-interview">Interview</a>',
        f'href="{STUDIO_VIDEOS_HREF}">Interview</a>',
        1,
    )

    html = html.replace('href="/#reviews">Reviews</a>', f'href="{REVIEWS_HREF}">Reviews</a>')
    html = html.replace(
        'href="/#reviews">Client Reviews</a>',
        f'href="{REVIEWS_HREF}">Client Reviews</a>',
    )
    return html


def patch_all_html(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    updated = raw
    updated = updated.replace('href="/#reviews">Reviews</a>', f'href="{REVIEWS_HREF}">Reviews</a>')
    updated = updated.replace(
        'href="/#reviews">Client Reviews</a>',
        f'href="{REVIEWS_HREF}">Client Reviews</a>',
    )
    if updated != raw:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> int:
    for path in (HOME, ROOT_HOME):
        if path.is_file():
            html = path.read_text(encoding="utf-8")
            new_html = patch_homepage(html)
            if new_html != html:
                path.write_text(new_html, encoding="utf-8")
                print(f"[anchors] {path.relative_to(ROOT)}")

    count = 0
    for path in ROOT.rglob("code.html"):
        if "artists_raw" in str(path) or "skipped_upload_build" in str(path):
            continue
        if patch_all_html(path):
            count += 1
    print(f"[nav] reviews link → {REVIEWS_HREF} on {count} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
