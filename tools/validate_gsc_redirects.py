#!/usr/bin/env python3
"""Validate GSC obsolete URL redirects and internal link cleanup."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install requests and beautifulsoup4", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from woa_canonical import CANONICAL_ORIGIN
from woa_page_consolidation import GSC_WIZARD_OBSOLETE_REDIRECTS, gsc_obsolete_paths, gsc_wizard_redirect_map
from woa_sitemap import discover_deploy_urls

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

HOST_VARIANTS = (
    "http://workofarttattoo.com",
    "http://www.workofarttattoo.com",
    "https://workofarttattoo.com",
    CANONICAL_ORIGIN,
)

SKIP_SCAN = {".git", ".github", "audits", "skipped_upload_build", "tools", "artists_raw", "config"}


def expected_target(path: str) -> str:
    path = path if path.startswith("/") else f"/{path}"
    if not path.endswith("/"):
        path = f"{path}/"
    redirect_map = gsc_wizard_redirect_map()
    if path in redirect_map:
        return f"{CANONICAL_ORIGIN}{redirect_map[path]}"
    bare = path.rstrip("/")
    for old, new in redirect_map.items():
        if old.rstrip("/") == bare:
            return f"{CANONICAL_ORIGIN}{new}"
    raise KeyError(path)


def trace_url(url: str, timeout: float = 20.0) -> dict:
    session = requests.Session()
    session.headers.update({"User-Agent": "WOA-GSC-Redirect-Validator/1.0"})
    hops: list[dict] = []
    current = url
    for _ in range(8):
        resp = session.get(current, allow_redirects=False, timeout=timeout)
        hop = {
            "url": current,
            "status": resp.status_code,
            "location": resp.headers.get("Location", ""),
        }
        hops.append(hop)
        if resp.status_code not in (301, 302, 303, 307, 308):
            break
        location = hop["location"]
        if not location:
            break
        current = urljoin(current, location)
    final = hops[-1]
    canonical = ""
    if final["status"] == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
        link = soup.find("link", rel="canonical")
        if link and link.get("href"):
            canonical = link["href"].strip()
    redirect_hops = len(hops) - 1 if final["status"] == 200 else len(hops)
    return {
        "hops": redirect_hops,
        "chain": hops,
        "final_url": current,
        "final_status": final["status"],
        "final_canonical": canonical,
    }


def obsolete_source_dir(old_fragment: str) -> Path | None:
    rel = old_fragment.strip("/")
    if not rel:
        return None
    parts = rel.split("/")
    if parts[0] == "knowledge" and len(parts) == 2:
        return ROOT / "knowledge" / parts[1]
    return ROOT / parts[0]


def count_internal_links(old_fragment: str) -> int:
    count = 0
    patterns = (old_fragment, old_fragment.rstrip("/"))
    exclude_dir = obsolete_source_dir(old_fragment)
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_SCAN for part in path.parts):
            continue
        if exclude_dir is not None:
            try:
                path.relative_to(exclude_dir)
                continue
            except ValueError:
                pass
        if path.suffix not in {".html", ".txt", ".xml"}:
            continue
        if path.name not in {
            "code.html",
            "index.html",
            "llms.txt",
            "ai.txt",
            "robots.txt",
            "sitemap.xml",
            "sitemap-static-pages.xml",
        } and path.suffix != ".html":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in patterns:
            count += text.count(needle)
    return count


def sitemap_contains(path: str) -> bool:
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.is_file():
        return False
    tree = ET.parse(sitemap)
    locs = [el.text.strip() for el in tree.findall(".//sm:loc", NS) if el.text]
    needle = f"{CANONICAL_ORIGIN}{path}" if path.startswith("/") else path
    return any(loc.rstrip("/") + "/" == needle.rstrip("/") + "/" for loc in locs)


def crawl_sitemap_404s(live: bool) -> list[tuple[str, str]]:
    broken: list[tuple[str, str]] = []
    if not live:
        return broken
    session = requests.Session()
    session.headers.update({"User-Agent": "WOA-GSC-Redirect-Validator/1.0"})
    for _path, _prio, _freq in discover_deploy_urls(ROOT):
        page_url = f"{CANONICAL_ORIGIN}{_path}"
        try:
            html = session.get(page_url, timeout=25).text
        except Exception as exc:
            broken.append((page_url, f"fetch failed: {exc}"))
            continue
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            href = (a.get("href") or "").strip()
            if not href.startswith("/") or href.startswith("//"):
                continue
            target = urljoin(page_url, href)
            parsed = urlparse(target)
            if parsed.netloc not in ("www.workofarttattoo.com", "workofarttattoo.com"):
                continue
            check = f"{CANONICAL_ORIGIN}{parsed.path}"
            if not check.endswith("/") and "." not in parsed.path.split("/")[-1]:
                check = check + "/"
            try:
                head = session.head(check, allow_redirects=True, timeout=20)
                if head.status_code >= 400:
                    broken.append((page_url, f"{href} -> HTTP {head.status_code}"))
            except Exception as exc:
                broken.append((page_url, f"{href} -> {exc}"))
    return broken


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GSC obsolete URL redirects")
    parser.add_argument("--live", action="store_true", help="Probe production URLs")
    parser.add_argument("--crawl-sitemap", action="store_true", help="Check internal links on sitemap URLs")
    args = parser.parse_args()

    obsolete_paths = gsc_obsolete_paths()
    print(
        "| Old URL | Initial | Location | Hops | Final URL | Final | Canonical | Internal links | Pass |"
    )
    print("|---|---|---|---|---|---|---|---|---|")

    failures = 0
    for path in obsolete_paths:
        expected = expected_target(path)
        internal_count = count_internal_links(path)
        if args.live:
            probe = f"{CANONICAL_ORIGIN}{path}"
            result = trace_url(probe)
            initial = result["chain"][0]["status"]
            location = result["chain"][0]["location"] if len(result["chain"]) > 1 else ""
            hops = result["hops"]
            final_url = result["final_url"]
            final_status = result["final_status"]
            canonical = result["final_canonical"] or final_url
            ok = (
                initial in (301, 308)
                and hops == 1
                and final_status == 200
                and canonical.rstrip("/") + "/" == expected.rstrip("/") + "/"
                and internal_count == 0
                and not sitemap_contains(path)
            )
        else:
            initial = location = hops = final_status = canonical = "n/a"
            final_url = expected
            ok = internal_count == 0 and not sitemap_contains(path)

        if not ok:
            failures += 1
        pass_cell = "yes" if ok else "**no**"
        print(
            f"| `{CANONICAL_ORIGIN}{path}` | {initial} | `{location}` | {hops} | "
            f"`{final_url}` | {final_status} | `{canonical}` | {internal_count} | {pass_cell} |"
        )

    if args.crawl_sitemap and args.live:
        broken = crawl_sitemap_404s(True)
        print(f"\nSitemap crawl: {len(broken)} broken internal link(s)")
        for src, detail in broken[:50]:
            print(f"  - {src}: {detail}")
        if broken:
            failures += 1

    print(f"\n{len(obsolete_paths) - failures}/{len(obsolete_paths)} paths passed checks")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
