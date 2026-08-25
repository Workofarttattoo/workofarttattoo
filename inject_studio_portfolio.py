#!/usr/bin/env python3
"""Wire studio gallery into artist pages — fix Katelyn portfolio, add gallery CTAs."""

from __future__ import annotations

import re
from pathlib import Path

from woa_studio_media_manifest import MediaCategory, manifest_items

ROOT = Path(__file__).resolve().parent
SLUG = "studio_gallery"
MARKER = 'data-woa-studio-gallery-strip="'
JOSHUA = ROOT / "artists_build" / "joshua-cole.html"
KATELYN = ROOT / "artists_build" / "katelyn-cole.html"


def picture(stem: str, alt: str) -> str:
    return (
        f'<picture><source srcset="/{SLUG}/{stem}.webp" type="image/webp"/>'
        f'<img alt="{alt}" class="w-full h-full object-cover object-center" decoding="async" '
        f'height="800" loading="lazy" src="/{SLUG}/{stem}.png" width="800"/></picture>'
    )


def strip_html(items: list, heading: str, blurb: str, artist_key: str, extra_link: tuple[str, str] | None = None) -> str:
    if not items:
        return ""
    cells = "".join(
        f'<div class="aspect-square overflow-hidden">{picture(i.stem, i.alt)}</div>'
        for i in items[:8]
    )
    extra = ""
    if extra_link:
        label, href = extra_link
        extra = f' <a class="inline-flex border border-outline text-on-surface px-10 py-3 font-label-caps text-label-caps uppercase tracking-widest hover:bg-on-surface hover:text-surface transition-colors ml-0 sm:ml-4 mt-4 sm:mt-0" href="{href}">{label}</a>'
    return f"""
<section class="py-16 px-margin-mobile md:px-margin-desktop bg-surface border-y border-outline-variant/20" {MARKER}{artist_key}">
<div class="max-w-6xl mx-auto space-y-8">
<div class="max-w-3xl space-y-3">
<h2 class="font-headline-lg text-on-surface">{heading}</h2>
<p class="font-body-md text-on-surface-variant">{blurb}</p>
</div>
<div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">{cells}</div>
<p class="text-center pt-4 flex flex-col sm:flex-row gap-4 justify-center items-center"><a class="inline-flex border border-secondary text-secondary px-10 py-3 font-label-caps text-label-caps uppercase tracking-widest hover:bg-secondary/10 transition-colors" href="/{SLUG}/">View full studio gallery</a>{extra}</p>
</div>
</section>
"""


def katelyn_portfolio_wall(piercing_items: list) -> str:
    cells = "".join(picture(i.stem, i.alt) for i in piercing_items[:12])
    return f"""<!-- HIGH DENSITY PORTFOLIO WALL -->
<section class="py-section-gap px-4 md:px-margin-desktop bg-background overflow-hidden">
<div class="text-center mb-20 max-w-4xl mx-auto">
<span class="text-label-caps font-label-caps text-secondary block mb-2 uppercase tracking-widest">Piercing Portfolio</span>
<h2 class="text-headline-lg font-headline-lg mb-6">Real piercing work — not tattoo stock</h2>
<p class="text-body-lg font-body-lg text-on-surface-variant">Documented ear curation, facial piercing, and jewelry styling by Katelyn Cole in our Las Vegas studio.</p>
</div>
<div class="portfolio-wall">
<div class="flex flex-col gap-4">
<div class="sticky top-24 z-20 bg-background/90 backdrop-blur-sm py-4 border-b border-secondary/30">
<h3 class="text-headline-md font-headline-md text-secondary uppercase tracking-tighter">Recent piercing work</h3>
<p class="text-label-caps text-on-surface-variant uppercase mt-1">Jewelry fit · anatomy-first</p>
</div>
<div class="dense-grid">{cells}</div>
</div>
</div>
<div class="mt-16 text-center">
<a class="inline-flex border border-secondary text-secondary px-12 py-4 text-label-caps hover:bg-secondary hover:text-on-secondary transition-all uppercase tracking-widest" href="/{SLUG}/#katelyn-piercing">Full piercing gallery</a>
</div>
</section>"""


def replace_katelyn_portfolio(html: str, piercing_items: list) -> str:
    pattern = r"<!-- HIGH DENSITY PORTFOLIO WALL -->.*?</section>\s*(?=<!-- SEO Rich Biography Section -->)"
    replacement = katelyn_portfolio_wall(piercing_items)
    if not re.search(pattern, html, flags=re.DOTALL):
        print("[warn] Katelyn portfolio wall block not found")
        return html
    return re.sub(pattern, replacement + "\n", html, count=1, flags=re.DOTALL)


def inject_strip(html: str, strip: str) -> str:
    html = re.sub(
        rf'<section[^>]*{re.escape(MARKER)}[^"]*"[^>]*>.*?</section>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    anchor = '<section class="py-16 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" data-woa-artist-eeat='
    if anchor in html:
        return html.replace(anchor, strip + "\n" + anchor, 1)
    for foot in ("<!-- Footer -->", "<footer"):
        if foot in html:
            return html.replace(foot, strip + "\n" + foot, 1)
    return html.replace("</body>", strip + "\n</body>", 1)


def main() -> int:
    items = manifest_items()
    by_cat: dict[MediaCategory, list] = {}
    for item in items:
        by_cat.setdefault(item.category, []).append(item)
    piercing = by_cat.get(MediaCategory.KATELYN_PIERCING, [])

    if KATELYN.is_file():
        raw = KATELYN.read_text(encoding="utf-8")
        updated = replace_katelyn_portfolio(raw, piercing)
        strip = strip_html(
            piercing,
            "From the piercing chair",
            "A sample of Katelyn’s documented piercing work — see the full gallery for more ear curation and facial placements.",
            "katelyn",
        )
        updated = inject_strip(updated, strip)
        if updated != raw:
            KATELYN.write_text(updated, encoding="utf-8")
            print(f"[ok] {KATELYN.relative_to(ROOT)} — portfolio + strip ({len(piercing)} piercing)")

    if JOSHUA.is_file():
        raw = JOSHUA.read_text(encoding="utf-8")
        tattooing = by_cat.get(MediaCategory.JOSHUA_TATTOOING, [])
        strip = strip_html(
            tattooing,
            "Joshua Cole · Tattooing in the studio",
            "Only real session photos of Joshua at the machine — custom black & grey work shot in our Las Vegas studio.",
            "joshua",
            extra_link=("Offsite bookings", "/offsite_bookings/#party-at-mike-tysons-house"),
        )
        updated = inject_strip(raw, strip)
        if updated != raw:
            JOSHUA.write_text(updated, encoding="utf-8")
            print(f"[ok] {JOSHUA.relative_to(ROOT)} — Joshua tattooing strip ({len(tattooing)} photos)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
