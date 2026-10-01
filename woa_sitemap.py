"""Discover every indexable public URL for sitemap.xml.

Candidates follow the deploy folder rules, then each page is kept only when
its HTML canonical is that exact https://www URL and the page is not noindex.
Obsolete aliases, redirects, and pages that canonicalize elsewhere are omitted.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from woa_nav_config import HOME_SLUG, SITE_CANONICAL_HOST

SITE_ORIGIN = SITE_CANONICAL_HOST
GEO_SLUG = "geo_hub_ai_source_of_truth_work_of_art"

# Utility / legal pages — noindex, excluded from XML sitemap
NOINDEX_SITEMAP_SLUGS: frozenset[str] = frozenset(
    {"privacy-policy", "terms-of-service", "image-license"}
)

_CANONICAL_TAG_RE = re.compile(
    r'<link\b[^>]*\brel=["\']canonical["\'][^>]*>',
    re.IGNORECASE,
)
_ROBOTS_TAG_RE = re.compile(
    r'<meta\b[^>]*\bname=["\']robots["\'][^>]*>',
    re.IGNORECASE,
)
_HREF_RE = re.compile(r'\bhref=["\']([^"\']+)["\']', re.IGNORECASE)
_CONTENT_RE = re.compile(r'\bcontent=["\']([^"\']+)["\']', re.IGNORECASE)


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
    from woa_url_aliases import (
        ALIASES_BY_SOURCE,
        MUST_PUBLISH_ALIAS_SOURCES,
        NEVER_RETIRE_SOURCE_SLUGS,
    )

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

    # Alias sources normally 301 to a short URL and stay out of the sitemap.
    # MUST_PUBLISH_ALIAS_SOURCES (the GEO hub) must be listed at the live hub path.
    alias_sources = (
        frozenset(ALIASES_BY_SOURCE.keys())
        - NEVER_RETIRE_SOURCE_SLUGS
        - MUST_PUBLISH_ALIAS_SOURCES
    )

    for slug in sorted(merged.keys()):
        if slug == "artists_build":
            continue
        if slug == HOME_SLUG or (home_slug and slug == home_slug):
            continue
        if slug.startswith("home_work_of_art"):
            continue
        if slug not in MUST_PUBLISH_ALIAS_SOURCES and (
            slug in SKIP_DEPLOY_SLUGS or slug in RETIRE_OVERLAP_SLUGS or slug in alias_sources
        ):
            continue
        if slug in NOINDEX_SITEMAP_SLUGS:
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

    return [row for row in rows if _is_indexable_canonical(repo_root, row[0])]


def _html_source_for_path(repo_root: Path, path: str) -> Path | None:
    """Deploy source HTML for a public path. Homepage lives in the home export folder."""
    if path == "/":
        for candidate in (
            repo_root / HOME_SLUG / "code.html",
            repo_root / "code.html",
            repo_root / "index.html",
        ):
            if candidate.is_file():
                return candidate
        return None
    folder = repo_root / path.strip("/")
    for name in ("code.html", "index.html"):
        candidate = folder / name
        if candidate.is_file():
            return candidate
    return None


def _head_signals(html_path: Path) -> tuple[str | None, bool]:
    text = html_path.read_text(encoding="utf-8", errors="replace")[:120_000]
    canonical = None
    match = _CANONICAL_TAG_RE.search(text)
    if match:
        href = _HREF_RE.search(match.group(0))
        if href:
            canonical = href.group(1).strip()
    noindex = False
    robots = _ROBOTS_TAG_RE.search(text)
    if robots:
        content = _CONTENT_RE.search(robots.group(0))
        if content and "noindex" in content.group(1).lower():
            noindex = True
    return canonical, noindex


def _is_indexable_canonical(repo_root: Path, path: str) -> bool:
    """Keep a URL only when it is the page's own HTTPS-www canonical and is indexable."""
    if "?" in path or path.startswith("http"):
        return False
    source = _html_source_for_path(repo_root, path)
    if source is None:
        return False
    canonical, noindex = _head_signals(source)
    if noindex or not canonical or "?" in canonical:
        return False
    if not canonical.startswith(f"{SITE_ORIGIN}/") and canonical.rstrip("/") != SITE_ORIGIN:
        return False
    expected = SITE_ORIGIN if path == "/" else f"{SITE_ORIGIN}{path}"
    return canonical.rstrip("/") == expected.rstrip("/")


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
