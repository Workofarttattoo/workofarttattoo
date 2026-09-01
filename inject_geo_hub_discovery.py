#!/usr/bin/env python3
"""Inject AI crawl / search-discovery blocks into the GEO source-of-truth page."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from woa_ai_crawl import (
    GEO_SLUG,
    ai_crawl_endpoints_html,
    authoritative_canonical_links_html,
    resident_artist_credentials_html,
    search_ai_discovery_html,
    tattoo_piercing_truth_hub_html,
)

ROOT = Path(__file__).resolve().parent
GEO_CODE = ROOT / GEO_SLUG / "code.html"

_SECTION_RE = re.compile(
    r'<section[^>]*\bid="(?P<id>[^"]+)"[^>]*>.*?</section>',
    re.DOTALL | re.IGNORECASE,
)

_RESIDENT_ARTIST_LEGACY_RE = re.compile(
    r'<section(?:\s[^>]*)?>\s*<div class="border-b border-surface-variant pb-4 mb-8">\s*'
    r'<h2[^>]*>\s*<span[^>]*>badge</span>\s*&lt;Resident Artist Credentials&gt;'
    r"[\s\S]*?</section>",
    re.IGNORECASE,
)


def _replace_section(html: str, section_id: str, new_block: str) -> str:
    pattern = re.compile(
        rf'<section[^>]*\bid="{re.escape(section_id)}"[^>]*>.*?</section>',
        re.DOTALL | re.IGNORECASE,
    )
    if not pattern.search(html):
        raise ValueError(f"Missing section #{section_id} in GEO hub HTML")
    return pattern.sub(new_block, html, count=1)


def _insert_after_section(html: str, after_id: str, new_block: str) -> str:
    pattern = re.compile(
        rf'(<section[^>]*\bid="{re.escape(after_id)}"[^>]*>.*?</section>)',
        re.DOTALL | re.IGNORECASE,
    )
    match = pattern.search(html)
    if not match:
        raise ValueError(f"Missing anchor section #{after_id} in GEO hub HTML")
    start, end = match.span()
    inserted = html[:end] + "\n" + new_block + html[end:]
    if f'id="{after_id}"' in new_block:
        return inserted
    return inserted


def inject_geo_hub_discovery(html: str) -> str:
    html = _replace_section(html, "ai-crawl-endpoints", ai_crawl_endpoints_html())
    if 'id="search-ai-discovery"' in html:
        html = _replace_section(html, "search-ai-discovery", search_ai_discovery_html())
    else:
        html = _insert_after_section(html, "ai-crawl-endpoints", search_ai_discovery_html())
    if 'id="tattoo-piercing-truth-hub"' in html:
        html = _replace_section(
            html, "tattoo-piercing-truth-hub", tattoo_piercing_truth_hub_html()
        )
    else:
        html = _insert_after_section(
            html, "search-ai-discovery", tattoo_piercing_truth_hub_html()
        )
    if 'id="authoritative-canonical-pages"' in html:
        html = _replace_section(
            html, "authoritative-canonical-pages", authoritative_canonical_links_html()
        )
    else:
        html = _insert_after_section(
            html, "search-ai-discovery", authoritative_canonical_links_html()
        )
    if 'id="resident-artist-credentials"' in html:
        html = _replace_section(
            html, "resident-artist-credentials", resident_artist_credentials_html()
        )
    elif _RESIDENT_ARTIST_LEGACY_RE.search(html):
        html = _RESIDENT_ARTIST_LEGACY_RE.sub(
            resident_artist_credentials_html(), html, count=1
        )
    return html


def main() -> int:
    if not GEO_CODE.is_file():
        print(f"Missing {GEO_CODE}", file=sys.stderr)
        return 1
    original = GEO_CODE.read_text(encoding="utf-8")
    updated = inject_geo_hub_discovery(original)
    if updated != original:
        GEO_CODE.write_text(updated, encoding="utf-8")
        print(f"Updated {GEO_CODE}")
    else:
        print(f"No changes needed for {GEO_CODE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
