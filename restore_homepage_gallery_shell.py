#!/usr/bin/env python3
"""Restore missing homepage gallery/portfolio sections and remove corrupted banner junk."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODE = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
ROOT_CODE = ROOT / "code.html"

CORRUPT_BANNER_RE = re.compile(
    r"<!-- WOA_HERO_BANNER_START -->\s*"
    r'<div aria-hidden="false" class="woa-hero-banner[\s\S]*?'
    r'<div class="absolute -bottom-6 -left-6 w-32 h-32 border-b-2 border-l-2 border-secondary"></div>\s*',
    re.MULTILINE,
)

GALLERY_SHELL = """<!-- Portfolio Showcase Section -->
<section class="py-16 md:py-section-gap px-margin-mobile md:px-margin-desktop space-y-10 md:space-y-section-gap" id="gallery">
<div class="text-center space-y-4 mb-16 max-w-3xl mx-auto">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Las Vegas Tattoo &amp; Piercing</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Meet Our Artists</h2>
<p class="font-body-lg text-body-lg text-on-surface-variant">Joshua Cole — black &amp; grey realism. Katelyn Cole — master body piercer &amp; ear curation.</p>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-gutter max-w-3xl mx-auto">
<a class="group text-center" href="/artists/joshua-cole/">
<div class="aspect-[3/4] bg-surface-container mb-4 overflow-hidden relative border border-outline-variant/30">
<picture><source srcset="/artists/joshua-cole/joshua-cole-tattooing-portrait-las-vegas.webp" type="image/webp"/><img width="800" height="1067" alt="Joshua Cole — Work of Art Las Vegas" class="w-full h-full object-cover object-top" decoding="async" loading="lazy" src="/artists/joshua-cole/joshua-cole-tattooing-portrait-las-vegas.png"/></picture>
</div>
<span class="font-label-caps text-label-caps text-on-surface">Joshua Cole</span>
</a>
<a class="group text-center" href="/artists/katelyn-cole/">
<div class="aspect-[3/4] bg-surface-container mb-4 overflow-hidden relative border border-outline-variant/30">
<picture><source srcset="/artists/katelyn-cole/katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas.webp" type="image/webp"/><img width="800" height="1067" alt="Katelyn Cole — Work of Art Las Vegas" class="w-full h-full object-cover object-top" decoding="async" loading="lazy" src="/artists/katelyn-cole/katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas.jpg"/></picture>
</div>
<span class="font-label-caps text-label-caps text-on-surface">Katelyn Cole</span>
</a>
</div>
<div aria-label="Gallery category filter" class="mt-8 mb-12 flex flex-wrap gap-3" id="gallery-filters">
<button class="px-6 py-2.5 bg-secondary text-on-secondary font-label-caps text-[11px] uppercase tracking-[0.15em] border border-secondary transition-all active:scale-95" data-filter="all" type="button">All</button>
<button class="px-6 py-2.5 bg-surface-container-high text-on-surface-variant font-label-caps text-[11px] uppercase tracking-[0.15em] border border-outline-variant/30 hover:border-secondary transition-all active:scale-95" data-filter="black-grey" type="button">Realism</button>
<button class="px-6 py-2.5 bg-surface-container-high text-on-surface-variant font-label-caps text-[11px] uppercase tracking-[0.15em] border border-outline-variant/30 hover:border-secondary transition-all active:scale-95" data-filter="sleeves" type="button">Sleeves</button>
<button class="px-6 py-2.5 bg-surface-container-high text-on-surface-variant font-label-caps text-[11px] uppercase tracking-[0.15em] border border-outline-variant/30 hover:border-secondary transition-all active:scale-95" data-filter="color-realism" type="button">Color</button>
</div>
<div class="grid grid-cols-1 md:grid-cols-12 gap-gutter" id="showcase-grid">
<div class="md:col-span-8 group relative aspect-[3/4] md:aspect-[4/5] min-h-[320px] bg-surface-container overflow-hidden" data-category="black-grey">
<img alt="Portfolio placeholder" class="w-full h-full object-cover" loading="eager" src="/home_work_of_art_tattoo_piercing/client-portfolio/norse-odin-viking-ship-sleeve-realism-las-vegas.png" width="800" height="800"/>
</div>
<div class="md:col-span-4 space-y-gutter">
<div class="group relative aspect-square bg-surface-container overflow-hidden" data-category="black-grey">
<img alt="Portfolio placeholder" class="w-full h-full object-cover" loading="lazy" src="/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-warrior-profile-shoulder-realism-las-vegas.png" width="800" height="800"/>
</div>
<div class="group relative aspect-square bg-surface-container overflow-hidden" data-category="black-grey">
<img alt="Portfolio placeholder" class="w-full h-full object-cover" loading="lazy" src="/home_work_of_art_tattoo_piercing/client-portfolio/veiled-woman-statue-black-grey-realism-las-vegas.png" width="800" height="800"/>
</div>
<div class="group relative aspect-square bg-surface-container overflow-hidden hidden md:block" data-category="black-grey">
<img alt="Portfolio placeholder" class="w-full h-full object-cover" loading="lazy" src="/home_work_of_art_tattoo_piercing/client-portfolio/all-seeing-eye-triangle-forearm-realism-las-vegas.png" width="800" height="800"/>
</div>
</div>
</div>
<!-- WOA_HOME_MASONRY_START -->
<!-- WOA_HOME_MASONRY_END -->
<div class="flex justify-center pt-8">
<a class="bg-transparent text-on-surface px-12 py-5 font-label-caps text-label-caps uppercase tracking-widest border-2 border-outline-variant hover:border-secondary transition-all text-center min-h-[52px] flex items-center justify-center" href="/studio_gallery/">View full studio gallery</a>
</div>
</section>
<section class="py-16 md:py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/10 space-y-16" id="portfolio">
<div class="text-center space-y-4 max-w-2xl mx-auto">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Custom Work</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Tattoo Portfolio</h2>
<p class="font-body-lg text-body-lg text-on-surface-variant">Real client photos from Joshua Cole — black &amp; grey realism, color memorial pieces, and original art.</p>
</div>
</section>
<!-- Piercing Section -->
<section class="py-16 md:py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container border-y border-outline-variant/10" id="piercing">
<div class="max-w-3xl mx-auto text-center space-y-4">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Professional Piercer</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Ear Curation &amp; Body Piercing</h2>
<p class="font-body-lg text-body-lg text-on-surface-variant">Katelyn Cole — jewelry fit, anatomical placement, and styling.</p>
<a class="inline-flex bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest" href="/artists/katelyn-cole/">Meet Katelyn</a>
</div>
</section>
"""


def patch_html(html: str) -> tuple[str, dict[str, int]]:
    stats = {"corrupt_banner_removed": 0, "gallery_shell_inserted": 0}
    html, n = CORRUPT_BANNER_RE.subn("", html)
    stats["corrupt_banner_removed"] = n

    if 'id="gallery"' not in html:
        anchor = "<!-- FAQ Section -->"
        if anchor in html:
            html = html.replace(anchor, GALLERY_SHELL + "\n" + anchor, 1)
            stats["gallery_shell_inserted"] = 1
        elif 'id="knowledge-base"' in html:
            html = re.sub(
                r'(<section class="py-16[^"]*" id="knowledge-base")',
                GALLERY_SHELL + r"\n\1",
                html,
                count=1,
            )
            stats["gallery_shell_inserted"] = 1
    return html, stats


def main() -> int:
    for path in (CODE, ROOT_CODE):
        if not path.is_file():
            continue
        html, stats = patch_html(path.read_text(encoding="utf-8"))
        path.write_text(html, encoding="utf-8")
        print(f"[restore] {path.relative_to(ROOT)} {stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
