#!/usr/bin/env python3
"""Inject slim sitewide internal links — guides use topic clusters only."""

from __future__ import annotations

import re
from pathlib import Path

from woa_nav_config import GUIDE_META, HOME_SLUG, SKIP_GUIDE_SLUGS

ROOT = Path(__file__).resolve().parent
MARKER = 'data-woa-internal-links="1"'
TOPIC_MARKER = 'data-woa-topic-cluster="1"'

CONVERSION_SLUGS = frozenset(
    {
        HOME_SLUG,
        "appointments",
        "artists",
        "merchandise",
        "cart",
        "my-account",
        "privacy-policy",
        "terms-of-service",
        "__root__",
    }
)

NAV_RE = re.compile(
    rf'<nav[^>]*{re.escape(MARKER)}[^>]*>.*?</nav>\s*',
    re.DOTALL,
)

SLIM_BLOCK = f"""
<nav {MARKER} aria-label="Explore Work of Art" class="woa-internal-links py-10 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/10">
<div class="max-w-4xl mx-auto">
<h2 class="font-headline-md text-on-surface mb-4">Explore the studio</h2>
<ul class="font-body-md text-on-surface-variant space-y-2 sm:columns-2">
<li><a class="text-secondary underline hover:no-underline" href="/">Work of Art — Las Vegas studio</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/appointments/">Book an appointment</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/artists/">Our artists</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/knowledge/">Tattoo &amp; piercing Q&amp;A</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/tattoo-shop-near-las-vegas-strip/">Directions &amp; hours</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/privacy-policy/">Privacy policy</a></li>
</ul>
</div>
</nav>
"""

GALLERY_ANCHOR = (
    '<a class="block px-3 py-2 text-[13px] leading-snug text-on-surface hover:text-secondary transition-colors" '
    'href="/#gallery">All Artists &amp; Gallery</a>'
)
ARTISTS_DIR_ANCHOR = (
    '<a class="block px-3 py-2 text-[13px] leading-snug text-on-surface hover:text-secondary transition-colors" '
    'href="/artists/">Artists Directory</a>'
)

FILES: list[Path] = []
for p in ROOT.rglob("code.html"):
    if "skipped" in p.parts:
        continue
    FILES.append(p)
for p in (ROOT / "artists_build").glob("*.html"):
    FILES.append(p)
if (ROOT / "artists" / "code.html").is_file():
    FILES.append(ROOT / "artists" / "code.html")


def page_slug(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel == Path("code.html"):
        return "__root__"
    if rel.parts[0] == "artists_build":
        return rel.stem
    if rel.name == "code.html" and len(rel.parts) >= 2:
        if rel.parts[0] == "knowledge" and len(rel.parts) >= 3:
            return rel.parts[1]
        return rel.parts[0]
    return ""


def is_guide_page(path: Path, html: str) -> bool:
    slug = page_slug(path)
    if slug in CONVERSION_SLUGS:
        return False
    if path.parent.name == "artists_build":
        return False
    if path.parent.parent.name == "knowledge" or slug == "knowledge":
        return True
    if slug in GUIDE_META:
        return True
    if slug in SKIP_GUIDE_SLUGS:
        return False
    if TOPIC_MARKER in html or 'data-woa-guide-hub-bar="1"' in html:
        return True
    if slug.startswith("tattoo_shop_"):
        return True
    return False


def inject_block(html: str, path: Path) -> str:
    html = NAV_RE.sub("", html)
    return html


def inject_nav(html: str) -> str:
    if 'href="/artists/">Artists Directory</a>' in html:
        return html
    if GALLERY_ANCHOR not in html:
        return html
    return html.replace(GALLERY_ANCHOR, ARTISTS_DIR_ANCHOR + GALLERY_ANCHOR, 1)


def main() -> None:
    n_block = n_nav = 0
    for path in sorted(set(FILES)):
        html = path.read_text(encoding="utf-8")
        orig = html
        html = inject_nav(html)
        html = inject_block(html, path)
        if html != orig:
            path.write_text(html, encoding="utf-8")
            if MARKER in html:
                n_block += 1
            if 'href="/artists/">Artists Directory</a>' in html and ARTISTS_DIR_ANCHOR not in orig:
                n_nav += 1
            print(path.relative_to(ROOT))
    print(f"Nav updates: {n_nav}, internal link blocks: {n_block}")


if __name__ == "__main__":
    main()
