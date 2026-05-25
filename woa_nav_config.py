"""
Shared URLs and guide discovery for Work of Art static HTML navigation.

Deployed paths match stitch_work_of_art_digital_overhaul/*/folder_name/
(except HOME_SLUG maps to site root).

Adjust MERCH_HREF only if merchandise lives elsewhere.
"""

from __future__ import annotations

from pathlib import Path

ROOT_A = Path(__file__).resolve().parent
ROOT_B = Path("/Users/noone/Downloads/stitch_work_of_art_digital_overhaul 2")

HOME_SLUG = "home_work_of_art_tattoo_piercing"

# Primary links (sitewide; use root-relative anchors that work across pages)
HREF_ARTISTS = "/#gallery"
HREF_PIERCING = "/#piercing"
MERCH_HREF = "/merchandise/"
HREF_REVIEWS = "/#faq"
HREF_APPOINTMENTS = "/appointments/"

# Exclude from "Guides" mega-list — home is duplicated as index; uploads often WP mirrors
SKIP_GUIDE_SLUGS = frozenset(
    {
        HOME_SLUG,
        "skipped_upload_build",
        "skipped_pages_clipboard.html",
        "skipped_pages_clipboard",
        "appointments",
    }
)


def merged_export_roots() -> dict[str, Path]:
    """Prefer later roots (ROOT_B overrides ROOT_A slug path for deploy merges)."""
    merged: dict[str, Path] = {}
    for base in (ROOT_A, ROOT_B):
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir()):
            if not child.is_dir():
                continue
            if child.name.startswith("."):
                continue
            if (child / "code.html").is_file():
                merged[child.name] = child
    return merged


def slug_to_guide_label(slug: str, max_len: int = 46) -> str:
    readable = slug.replace("_", " ").strip()
    if len(readable) > max_len:
        readable = readable[: max_len - 1].rstrip() + "…"
    return readable


def discover_guide_pairs() -> list[tuple[str, str]]:
    """
    Returns sorted (label, href) for every export folder containing code.html
    minus SKIP_GUIDE_SLUGS (home, upload staging, etc.).
    """
    out: dict[str, tuple[str, str]] = {}
    for slug, folder in merged_export_roots().items():
        if slug in SKIP_GUIDE_SLUGS:
            continue
        href = f"/{slug}/"
        label = slug_to_guide_label(slug)
        out[href] = (label, href)
    pairs = sorted(out.values(), key=lambda t: t[0].lower())
    return pairs
