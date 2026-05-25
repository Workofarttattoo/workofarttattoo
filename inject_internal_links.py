#!/usr/bin/env python3
"""Inject sitewide internal links block into static HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARKER = 'data-woa-internal-links="1"'
SKIP_HOME = "home_work_of_art_tattoo_piercing"

BLOCK = f"""
<nav {MARKER} aria-label="Explore Work of Art" class="woa-internal-links py-12 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/10">
<div class="max-w-4xl mx-auto">
<h2 class="font-headline-md text-on-surface mb-4">Explore the studio</h2>
<ul class="font-body-md text-on-surface-variant space-y-2 sm:columns-2">
<li><a class="text-secondary underline hover:no-underline" href="/">Best tattoo and piercing shop Las Vegas</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/appointments/">Book an appointment</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/artists/">Our artists</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/artists/joshua-cole/">Joshua Cole — realism tattoo</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/artists/katelyn-cole/">Katelyn Cole — piercing</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/jay_jay_artist_portfolio_authentic_masterpieces/">Jay Jay — portfolio</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/realism_tattoos_las_vegas_master_authority_guide/">Realism tattoos guide</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/best_piercing_shop_las_vegas_updated_jewelry_standards/">Piercing shop guide</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/walk_in_tattoos_las_vegas_authority_guide/">Walk-in tattoos</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/tattoo_shop_near_the_strip_nap_corrected/">Directions &amp; hours</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/merchandise/">Merchandise</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/privacy-policy/">Privacy policy</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/cart/">Shopping cart</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/my-account/">My account</a></li>
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


def inject_block(html: str) -> str:
    if MARKER in html:
        return html
    if "</main>" in html:
        return html.replace("</main>", BLOCK + "\n</main>", 1)
    return html.replace("</body>", BLOCK + "\n</body>", 1)


def inject_nav(html: str) -> str:
    if 'href="/artists/">Artists Directory</a>' in html:
        return html
    if GALLERY_ANCHOR not in html:
        return html
    return html.replace(GALLERY_ANCHOR, ARTISTS_DIR_ANCHOR + GALLERY_ANCHOR, 1)


def main() -> None:
    n_block = n_nav = 0
    for path in sorted(set(FILES)):
        if SKIP_HOME in path.parts:
            html = path.read_text(encoding="utf-8")
            html2 = inject_nav(html)
            if html2 != html:
                path.write_text(html2, encoding="utf-8")
                n_nav += 1
            continue
        html = path.read_text(encoding="utf-8")
        orig = html
        html = inject_nav(html)
        html = inject_block(html)
        if html != orig:
            path.write_text(html, encoding="utf-8")
            if MARKER in html and MARKER not in orig:
                n_block += 1
            if 'href="/artists/">Artists Directory</a>' in html and ARTISTS_DIR_ANCHOR not in orig:
                n_nav += 1
            print(path.relative_to(ROOT))
    print(f"Nav updates: {n_nav}, internal link blocks: {n_block}")


if __name__ == "__main__":
    main()
