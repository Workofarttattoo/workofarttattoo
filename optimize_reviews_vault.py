#!/usr/bin/env python3
"""Honest reviews page: remove fabricated JS reviews, add healed case studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VAULT = ROOT / "reviews_vault_100_verified_masterpieces" / "code.html"

FAKE_GRID_RE = re.compile(
    r"\s*// Populate massive review grid.*?grid\.appendChild\(div\);\s*\}\s*",
    re.DOTALL,
)

REVIEW_GRID_RE = re.compile(
    r'(<div class="masonry-grid" id="review-grid">)(.*?)(</div>\s*</section>)',
    re.DOTALL,
)

GOOGLE_REVIEWS_BLOCK = """
<div class="max-w-2xl mx-auto text-center space-y-6 p-10 border border-outline-variant/40 bg-surface">
<p class="font-body-lg text-on-surface-variant">We do not publish invented review cards on this site. Read verified Google reviews from real clients — then leave your own after your appointment.</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center">
<a class="inline-flex items-center justify-center bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest hover:glow-sm transition-all" href="https://www.google.com/maps/search/?api=1&amp;query=Work+of+Art+Tattoo+%26+Piercing+Las+Vegas" rel="noopener noreferrer" target="_blank">Read on Google</a>
<a class="inline-flex items-center justify-center border border-outline-variant px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest hover:border-secondary transition-colors" href="/review_funnel_google_authority_hub/">Leave a review</a>
</div>
<p class="font-body-md text-on-surface-variant text-sm">Featured quotes below are portfolio case studies with documented healing — not anonymous testimonials.</p>
</div>
"""

CASE_STUDIES_BLOCK = """
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" data-woa-healed-stories="1">
<div class="max-w-5xl mx-auto space-y-10">
<div class="text-center space-y-3 max-w-2xl mx-auto">
<h2 class="font-headline-lg text-on-surface">Healed work &amp; client stories</h2>
<p class="font-body-md text-on-surface-variant">Portfolio pieces with documented healing stages — not generated review cards. Leave your own experience on <a class="text-secondary underline" href="/review_funnel_google_authority_hub/">Google</a>.</p>
</div>
<article class="grid grid-cols-1 md:grid-cols-12 gap-8 border border-outline-variant/30 p-8 bg-surface">
<div class="md:col-span-5">
<picture>
<source srcset="/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-thigh-realism-las-vegas.webp" type="image/webp"/>
<img alt="Black and grey lion thigh realism — healed portfolio, Work of Art Las Vegas" class="w-full h-auto object-cover" decoding="async" height="800" loading="lazy" src="/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-thigh-realism-las-vegas.png" width="800"/>
</picture>
</div>
<div class="md:col-span-7 space-y-4">
<h3 class="font-headline-md text-on-surface">Lion thigh — two-session realism</h3>
<p class="font-body-md text-on-surface-variant">Joshua Cole · outer thigh · ~12 hours across two sessions. Client wanted open skin for highlights, not a solid black fill.</p>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">
<li><strong>Fresh:</strong> deep blacks set; highlights left as negative space.</li>
<li><strong>4 weeks:</strong> peeling complete; mid-tones readable in daylight.</li>
<li><strong>3+ months:</strong> blacks held in the thigh bend — no muddy grey wash.</li>
</ul>
<p class="font-body-md"><a class="text-secondary underline" href="/realism_tattoos_las_vegas_master_authority_guide/">Realism guide</a> · <a class="text-secondary underline" href="/artists/joshua-cole/">Joshua's portfolio</a></p>
</div>
</article>
<article class="grid grid-cols-1 md:grid-cols-12 gap-8 border border-outline-variant/30 p-8 bg-surface">
<div class="md:col-span-5">
<picture>
<source srcset="/cover-up-tattoos-las-vegas/cover-up-tattoo-phoenix-hand-las-vegas-after.webp" type="image/webp"/>
<img alt="Cover-up phoenix hand and forearm — after healing, Work of Art Las Vegas" class="w-full h-auto object-cover" decoding="async" height="800" loading="lazy" src="/cover-up-tattoos-las-vegas/cover-up-tattoo-phoenix-hand-las-vegas-after.webp" width="800"/>
</picture>
</div>
<div class="md:col-span-7 space-y-4">
<h3 class="font-headline-md text-on-surface">Phoenix cover-up — hand &amp; forearm</h3>
<p class="font-body-md text-on-surface-variant">Joshua Cole · multi-session redesign over faded color. Before photos taken at consult; no stock collage.</p>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">
<li><strong>Consult:</strong> old ink documented in-studio.</li>
<li><strong>Mid-project:</strong> spaced sessions so the hand could heal between passes.</li>
<li><strong>Healed:</strong> reads as new art, not a dark patch.</li>
</ul>
<p class="font-body-md"><a class="text-secondary underline" href="/cover-up-tattoos-las-vegas/">Cover-up guide</a> · <a class="text-secondary underline" href="/appointments/">Book consult</a></p>
</div>
</article>
</div>
</section>
"""

MARKER = 'data-woa-healed-stories="1"'
CASE_STUDIES_ANCHOR = "<!-- Hall of Fame (Review Grid) -->"


def main() -> int:
    if not VAULT.is_file():
        print("[skip] reviews vault missing")
        return 0
    raw = VAULT.read_text(encoding="utf-8")
    updated = FAKE_GRID_RE.sub("\n        // Review grid: static cards only (no generated duplicates)\n    ", raw)
    updated = updated.replace(
        '<h2 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg mb-4">The Hall of Fame</h2>',
        '<h2 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg mb-4">Google reviews &amp; healed work</h2>',
    )
    for old, new in (
        (
            '<p class="font-label-caps text-label-caps text-on-surface-variant uppercase tracking-widest">Featured Google reviews</p>',
            '<p class="font-label-caps text-label-caps text-on-surface-variant uppercase tracking-widest">Verified Google reviews — read on Google</p>',
        ),
        (
            '<p class="font-label-caps text-label-caps text-on-surface-variant uppercase tracking-widest">Four featured Google reviews — read more on Google</p>',
            '<p class="font-label-caps text-label-caps text-on-surface-variant uppercase tracking-widest">Verified Google reviews — read on Google</p>',
        ),
    ):
        updated = updated.replace(old, new)
    if 'id="review-grid"' in updated and "JAMES SUTHERLAND" in updated:
        updated = REVIEW_GRID_RE.sub(r"\1" + GOOGLE_REVIEWS_BLOCK + r"\3", updated, count=1)
    if MARKER in updated:
        healed_re = re.compile(
            rf'<section[^>]*{re.escape(MARKER)}[\s\S]*?</section>\s*',
            re.MULTILINE,
        )
        updated = healed_re.sub(CASE_STUDIES_BLOCK + "\n", updated, count=1)
    elif CASE_STUDIES_ANCHOR in updated:
        updated = updated.replace(
            CASE_STUDIES_ANCHOR, CASE_STUDIES_BLOCK + CASE_STUDIES_ANCHOR, 1
        )
    if updated != raw:
        VAULT.write_text(updated, encoding="utf-8")
        print("[ok] reviews_vault_100_verified_masterpieces/code.html")
    else:
        print("[skip] no changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
