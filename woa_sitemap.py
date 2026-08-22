"""Discover every deployable HTML URL for sitemap.xml (matches deploy_stitch_site_root.py)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from woa_nav_config import SITE_CANONICAL_HOST

SITE_ORIGIN = SITE_CANONICAL_HOST
GEO_SLUG = "geo_hub_ai_source_of_truth_work_of_art"


def _priority_for_slug(slug: str, home_slug: str | None) -> tuple[str, str]:
    """Return (priority, changefreq) for a deployed slug folder."""
    if slug == GEO_SLUG:
        return "0.95", "weekly"
    if home_slug and slug == home_slug:
        return "0.95", "weekly"
    if slug == "appointments":
        return "0.9", "monthly"
    if slug == "artists":
        return "0.9", "monthly"
    if slug == "knowledge":
        return "0.9", "weekly"
    return "0.8", "monthly"


def discover_deploy_urls(repo_root: Path) -> list[tuple[str, str, str]]:
    """
    Return sorted (path, priority, changefreq) for sitemap entries.
    path is site-root relative with leading slash and trailing slash for directories.

    Uses the same folder merge + SKIP_DEPLOY_SLUGS rules as deploy_stitch_site_root.py
    so every live HTML URL is listed (including short aliases, never-retire legacy paths,
    and pages excluded from the guides nav only).
    """
    from deploy_stitch_site_root import SKIP_DEPLOY_SLUGS, gather_folders, resolve_home_slug
    from woa_page_consolidation import RETIRE_OVERLAP_SLUGS

    repo_root = repo_root.resolve()
    merged = gather_folders()
    home_slug = resolve_home_slug(merged)

    rows: list[tuple[str, str, str]] = []
    seen: set[str] = set()

    def add(path: str, priority: str, changefreq: str) -> None:
        if not path.startswith("/"):
            path = "/" + path
        if not path.endswith("/"):
            path = path + "/"
        if path in seen:
            return
        seen.add(path)
        rows.append((path, priority, changefreq))

    add("/", "1.0", "weekly")

    for slug in sorted(merged.keys()):
        if slug == "artists_build":
            continue
        if home_slug and slug == home_slug:
            continue
        if slug in SKIP_DEPLOY_SLUGS or slug in RETIRE_OVERLAP_SLUGS:
            continue
        local_dir = merged[slug]
        if not (local_dir / "code.html").is_file():
            continue
        pri, freq = _priority_for_slug(slug, home_slug)
        add(f"/{slug}/", pri, freq)

    knowledge = merged.get("knowledge")
    if knowledge and knowledge.is_dir():
        for child in sorted(knowledge.iterdir()):
            if child.is_dir() and (child / "code.html").is_file():
                add(f"/knowledge/{child.name}/", "0.75", "monthly")

    artists_build = merged.get("artists_build") or repo_root / "artists_build"
    if artists_build.is_dir():
        for html in sorted(artists_build.glob("*.html")):
            add(f"/artists/{html.stem}/", "0.85", "monthly")

    return rows


def build_sitemap_xml(repo_root: Path) -> str:
    lastmod = date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, priority, changefreq in discover_deploy_urls(repo_root):
        loc = f"{SITE_ORIGIN}{path}"
        lines.extend(
            [
                "  <url>",
                f"    <loc>{loc}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                f"    <changefreq>{changefreq}</changefreq>",
                f"    <priority>{priority}</priority>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def url_count(repo_root: Path) -> int:
    return len(discover_deploy_urls(repo_root))
