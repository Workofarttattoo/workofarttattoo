"""Discover every deployable HTML URL for sitemap.xml (matches deploy_stitch_site_root.py)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from woa_nav_config import HOME_SLUG, SKIP_GUIDE_SLUGS

SITE_ORIGIN = "https://workofarttattoo.com"
GEO_SLUG = "geo_hub_ai_source_of_truth_work_of_art"


def discover_deploy_urls(repo_root: Path) -> list[tuple[str, str, str]]:
    """
    Return sorted (path, priority, changefreq) for sitemap entries.
    path is site-root relative with leading slash and trailing slash for directories.
    """
    repo_root = repo_root.resolve()
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
    add(f"/{GEO_SLUG}/", "0.95", "weekly")
    add("/appointments/", "0.9", "monthly")

    for slug_dir in sorted(repo_root.iterdir()):
        if not slug_dir.is_dir() or slug_dir.name.startswith("."):
            continue
        slug = slug_dir.name
        if slug in SKIP_GUIDE_SLUGS or slug == "artists_build":
            continue
        if slug == HOME_SLUG:
            continue
        if (slug_dir / "code.html").is_file():
            pri = "0.95" if slug == GEO_SLUG else "0.8"
            add(f"/{slug}/", pri, "weekly" if slug == GEO_SLUG else "monthly")

    artists = repo_root / "artists_build"
    if artists.is_dir():
        for html in sorted(artists.glob("*.html")):
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
