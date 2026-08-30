#!/usr/bin/env python3
"""Link high-traffic geo and footer blocks to the official NAP source page."""

from __future__ import annotations

import re
from pathlib import Path

from woa_nav_config import HREF_OFFICIAL_NAP

ROOT = Path(__file__).resolve().parent
MARKER = 'data-woa-official-nap-link="1"'

STRIP_SLUGS: tuple[str, ...] = (
    "tattoo_shop_near_the_strip_nap_corrected",
    "tattoo_shop_near_the_strip_geo_seo_optimized",
)

CALLOUT = f"""<p class="font-body-md text-on-surface-variant text-sm mt-6" {MARKER}>
<a class="text-secondary underline hover:no-underline" href="{HREF_OFFICIAL_NAP}">Official location, hours &amp; contact</a>
 — canonical NAP for Google, Yelp, and directory listings.
</p>"""

CALLOUT_RE = re.compile(
    rf'<p class="font-body-md text-on-surface-variant text-sm mt-6" {re.escape(MARKER)}>[\s\S]*?</p>\s*',
    re.MULTILINE,
)

ADDRESS_LINK = (
    f'<a class="text-secondary underline hover:no-underline" href="{HREF_OFFICIAL_NAP}">'
    "2375 E. Tropicana Ave, Suite 3</a>"
)


def inject_strip_page(html: str) -> str:
    if MARKER in html:
        html = CALLOUT_RE.sub(CALLOUT + "\n", html, count=1)
    elif "2375 E. Tropicana Ave, Suite 3 is a short drive" in html:
        html = html.replace(
            "2375 E. Tropicana Ave, Suite 3 is a short drive",
            f"{ADDRESS_LINK} is a short drive",
            1,
        )
        html = html.replace(
            "2375 E. Tropicana Ave, Suite 3 — about five minutes",
            f"{ADDRESS_LINK} — about five minutes",
            1,
        )
        html = html.replace(
            "</section>\n<!-- Proximity Bento Grid -->",
            CALLOUT + "\n</section>\n<!-- Proximity Bento Grid -->",
            1,
        )
    elif "2375 E. Tropicana — about five minutes" in html:
        html = html.replace(
            "on E. Tropicana — about five minutes",
            f"at {ADDRESS_LINK} — about five minutes",
            1,
        )
        if MARKER not in html and "</section>" in html:
            html = html.replace(
                "</section>\n<!-- Proximity Bento Grid -->",
                CALLOUT + "\n</section>\n<!-- Proximity Bento Grid -->",
                1,
            )

    footer_needle = '<h5 class="font-label-caps text-label-caps text-primary mb-4">CONTACT</h5>'
    footer_link = (
        f'{footer_needle}\n<ul class="space-y-2 font-body-md text-on-surface-variant">\n'
        f'<li><a class="hover:text-primary transition-colors" href="{HREF_OFFICIAL_NAP}">'
        "Official hours &amp; location</a></li>"
    )
    if footer_needle in html and "Official hours &amp; location" not in html:
        html = html.replace(footer_needle, footer_link, 1)

    return html


def main() -> int:
    n = 0
    for slug in STRIP_SLUGS:
        path = ROOT / slug / "code.html"
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated = inject_strip_page(raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {slug}")
            n += 1
    print(f"Done: official NAP links on {n} strip page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
