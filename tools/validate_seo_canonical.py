#!/usr/bin/env python3
"""Fail CI when canonical URLs, sitemap entries, or JSON-LD drift from SEO rules."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from deploy_stitch_site_root import SKIP_DEPLOY_SLUGS, gather_folders, resolve_home_slug
from generate_gh_pages_excludes import gh_pages_exclude_slugs
from woa_canonical import CANONICAL_ORIGIN, canonical_url, normalize_path
from woa_page_consolidation import RETIRE_OVERLAP_SLUGS
from woa_url_aliases import ALIASES_BY_SOURCE, short_canonical

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
CANONICAL_NETLOC = urlparse(CANONICAL_ORIGIN).netloc


def slug_for(path: Path) -> str:
    if path.name == "code.html":
        return path.parent.name
    return path.parent.name


def route_for(path: Path) -> str:
    slug = slug_for(path)
    if slug == "code.html" or path.parent == ROOT:
        return "/"
    if slug.startswith("home_work_of_art"):
        return "/"
    from woa_url_aliases import short_href

    return short_href(slug)


def indexable_code_files() -> list[Path]:
    exclude = gh_pages_exclude_slugs()
    paths: list[Path] = []
    for path in sorted(ROOT.glob("*/code.html")):
        slug = path.parent.name
        if slug.startswith(".") or slug in exclude:
            continue
        if slug in RETIRE_OVERLAP_SLUGS:
            continue
        paths.append(path)
    # Root code.html mirrors home export — validate via home_work_of_art only.
    return paths


def assert_canonical_host(url: str, ctx: str, failures: list[str]) -> None:
    if not url:
        failures.append(f"{ctx}: empty URL")
        return
    parsed = urlparse(url)
    if parsed.scheme != "https":
        failures.append(f"{ctx}: must use https ({url})")
    if parsed.netloc != CANONICAL_NETLOC:
        failures.append(f"{ctx}: must use www host ({url})")


def validate_page(path: Path, failures: list[str], canonicals: dict[str, str]) -> None:
    slug = slug_for(path)
    expected = canonical_url("/") if slug.startswith("home_work_of_art") or path == ROOT / "code.html" else short_canonical(slug)
    expected_path = urlparse(expected).path
    rel = str(path.relative_to(ROOT))
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")

    robots = soup.find("meta", attrs={"name": "robots"})
    robots_content = (robots.get("content", "") if robots else "").lower()
    if "noindex" in robots_content:
        return

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    if not title:
        failures.append(f"{rel}: missing <title>")

    desc = soup.find("meta", attrs={"name": "description"})
    if not desc or not (desc.get("content") or "").strip():
        failures.append(f"{rel}: missing meta description")

    canonical = soup.find("link", rel="canonical")
    if not canonical or not canonical.get("href"):
        failures.append(f"{rel}: missing canonical link")
    else:
        href = canonical.get("href", "").strip()
        assert_canonical_host(href, f"{rel} canonical", failures)
        if normalize_path(urlparse(href).path) != normalize_path(expected_path):
            failures.append(f"{rel}: canonical {href} != expected {expected}")
        if href in canonicals and canonicals[href] != rel:
            failures.append(f"{rel}: duplicate canonical {href} (also {canonicals[href]})")
        canonicals[href] = rel

    og_url = soup.find("meta", property="og:url")
    if og_url and og_url.get("content"):
        assert_canonical_host(og_url["content"], f"{rel} og:url", failures)

    for script in soup.find_all("script", type="application/ld+json"):
        block = (script.string or script.get_text() or "").strip()
        if not block:
            continue
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            failures.append(f"{rel}: invalid JSON-LD: {exc}")
            continue
        nodes = data if isinstance(data, list) else data.get("@graph", [data])
        if not isinstance(nodes, list):
            nodes = [nodes]
        ids_seen: set[str] = set()
        for node in nodes:
            if not isinstance(node, dict):
                continue
            node_id = node.get("@id")
            if node_id:
                if node_id in ids_seen:
                    failures.append(f"{rel}: duplicate JSON-LD @id {node_id}")
                ids_seen.add(node_id)
            for key in ("url", "mainEntityOfPage"):
                val = node.get(key)
                if isinstance(val, str) and val.startswith("http"):
                    assert_canonical_host(val, f"{rel} JSON-LD {key}", failures)

    for m in re.finditer(r'href="(https?://[^"]+)"', raw):
        href = m.group(1)
        parsed = urlparse(href)
        if parsed.netloc.endswith("workofarttattoo.com"):
            assert_canonical_host(href, f"{rel} internal absolute href", failures)
            if parsed.netloc == "workofarttattoo.com":
                failures.append(f"{rel}: non-www internal link {href}")


def validate_sitemap(failures: list[str]) -> int:
    from woa_ai_crawl import SITEMAP_STATIC_NAME

    sitemap = ROOT / SITEMAP_STATIC_NAME
    if not sitemap.is_file():
        failures.append(f"missing {SITEMAP_STATIC_NAME}")
        return 0
    try:
        root_el = ElementTree.parse(sitemap).getroot()
    except ElementTree.ParseError as exc:
        failures.append(f"{SITEMAP_STATIC_NAME} parse error: {exc}")
        return 0
    locs = [el.text.strip() for el in root_el.findall(".//sm:loc", NS) if el.text]
    issues = 0
    for loc in locs:
        assert_canonical_host(loc, "sitemap loc", failures)
        path = urlparse(loc).path
        if path != "/" and not path.endswith("/"):
            failures.append(f"sitemap: non-trailing-slash URL {loc}")
        slug = path.strip("/").split("/")[0]
        if slug in RETIRE_OVERLAP_SLUGS or slug in ALIASES_BY_SOURCE:
            failures.append(f"sitemap: legacy/alias source URL {loc}")
        folder = ROOT / slug
        index = folder / "index.html"
        code = folder / "code.html"
        if slug and not index.is_file() and not code.is_file() and path != "/":
            failures.append(f"sitemap: URL has no local page {loc}")
        issues += len(failures)
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8", errors="replace") if (ROOT / "robots.txt").is_file() else ""
    sitemap_lines = [ln for ln in robots.splitlines() if ln.lower().startswith("sitemap:")]
    if len(sitemap_lines) != 1:
        failures.append(f"robots.txt must list exactly one Sitemap (found {len(sitemap_lines)})")
    elif SITEMAP_STATIC_NAME not in sitemap_lines[0]:
        failures.append(f"robots.txt Sitemap must advertise /{SITEMAP_STATIC_NAME}")
    elif CANONICAL_ORIGIN not in sitemap_lines[0]:
        failures.append("robots.txt Sitemap must use canonical https://www host")
    if locs.count(f"{CANONICAL_ORIGIN}/") != 1:
        failures.append("sitemap must list homepage exactly once")
    if any("/home_work_of_art_tattoo_piercing/" in loc for loc in locs):
        failures.append("sitemap must not list duplicate homepage path")
    return len(locs)


def main() -> int:
    failures: list[str] = []
    canonicals: dict[str, str] = {}
    pages = indexable_code_files()
    for path in pages:
        validate_page(path, failures, canonicals)

    sitemap_count = validate_sitemap(failures)

    print(f"Checked {len(pages)} indexable page(s), {sitemap_count} sitemap URL(s)")
    if failures:
        print(f"\nSEO canonical validation FAILED ({len(failures)} issue(s)):")
        for item in failures[:80]:
            print(f"  - {item}")
        if len(failures) > 80:
            print(f"  ... and {len(failures) - 80} more")
        return 1
    print("SEO canonical validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
