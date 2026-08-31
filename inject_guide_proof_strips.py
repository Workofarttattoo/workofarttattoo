#!/usr/bin/env python3
"""Inject five-frame heal proof strips on every authority guide."""

from __future__ import annotations

import re
from pathlib import Path

from woa_guide_proof_strips import MARKER, SKIP_SLUGS, proof_strip_html, strip_for_page
from woa_nav_config import discover_guide_entries

ROOT = Path(__file__).resolve().parent

STRIP_RE = re.compile(
    rf'<section[^>]*{re.escape(MARKER)}[\s\S]*?</section>\s*',
    re.MULTILINE,
)

# Legacy photos section (link list only) from piercing builder
LEGACY_PHOTOS_RE = re.compile(
    r'<section class="space-y-4" id="photos">\s*'
    r'<h2 class="font-headline-md text-on-surface text-2xl">Photos</h2>\s*'
    r'<ul class="font-body-md text-on-surface-variant space-y-2">.*?</ul>\s*'
    r"</section>\s*",
    re.DOTALL,
)

# Older pipeline runs injected a proof block without the current idempotent marker.
LEGACY_PROOF_BLOCK_RE = re.compile(
    r'<section[^>]*data-woa-proof-block="1"[\s\S]*?</section>\s*',
    re.DOTALL,
)


def inject(html_text: str, slug: str) -> str:
    html_text = LEGACY_PROOF_BLOCK_RE.sub("", html_text)
    block = proof_strip_html(slug)
    if not block:
        if MARKER in html_text:
            return STRIP_RE.sub("", html_text, count=1)
        return html_text

    if MARKER in html_text:
        return STRIP_RE.sub(block + "\n", html_text, count=1)

    if LEGACY_PHOTOS_RE.search(html_text):
        return LEGACY_PHOTOS_RE.sub(block + "\n", html_text, count=1)

    for pattern in (
        r'(<section[^>]*\bid="faq"[^>]*>)',
        r'(<section[^>]*\bid="videos"[^>]*>)',
        r'(<section[^>]*\bid="book"[^>]*>)',
    ):
        match = re.search(pattern, html_text)
        if match:
            pos = match.start()
            return html_text[:pos] + block + "\n" + html_text[pos:]

    if "</main>" in html_text:
        return html_text.replace("</main>", block + "\n</main>", 1)
    return html_text


def main() -> int:
    slugs = {row[0] for row in discover_guide_entries()} - SKIP_SLUGS
    n = 0
    for slug in sorted(slugs):
        path = ROOT / slug / "code.html"
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated = inject(raw, slug)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {slug}")
            n += 1
    print(f"Done: proof strips on {n} guide(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
