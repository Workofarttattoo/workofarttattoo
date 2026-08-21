#!/usr/bin/env python3
"""Trim footer link walls, update copyright year, rename GEO customer label."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup

from woa_nav_config import (
    GEO_HUB_CUSTOMER_LABEL,
    HREF_APPOINTMENTS,
    HREF_OFFICIAL_NAP,
    STUDIO_PHONE_PARENS,
    STUDIO_PHONE_TEL,
)

ROOT = Path(__file__).resolve().parent
YEAR = date.today().year

GEO_REPLACEMENTS = (
    ("GEO source of truth", GEO_HUB_CUSTOMER_LABEL),
    ("GEO Source of Truth", GEO_HUB_CUSTOMER_LABEL),
    ("GEO & AI Source of Truth", GEO_HUB_CUSTOMER_LABEL),
    ("GEO &amp; AI Source of Truth", GEO_HUB_CUSTOMER_LABEL),
)

COPYRIGHT_RE = re.compile(
    r"©\s*20\d{2}\s*Work of Art Tattoo\s*&(?:amp;)?\s*Piercing[^<]*",
    re.I,
)

SLIM_FOOTER_INNER = f"""
<div class="grid grid-cols-1 sm:grid-cols-3 gap-8">
<div class="space-y-3">
<h5 class="font-label-caps text-on-surface uppercase tracking-widest text-[11px]">Book</h5>
<ul class="space-y-2 text-on-surface-variant text-[13px] font-body-md">
<li><a class="hover:text-secondary transition-colors" href="{HREF_APPOINTMENTS}">Free consultation</a></li>
<li><a class="hover:text-secondary transition-colors" href="{STUDIO_PHONE_TEL}">Text {STUDIO_PHONE_PARENS}</a></li>
<li><a class="hover:text-secondary transition-colors" href="/reviews_vault_100_verified_masterpieces/">Client reviews</a></li>
</ul>
</div>
<div class="space-y-3">
<h5 class="font-label-caps text-on-surface uppercase tracking-widest text-[11px]">Studio</h5>
<ul class="space-y-2 text-on-surface-variant text-[13px] font-body-md">
<li><a class="hover:text-secondary transition-colors" href="/#gallery">Portfolio</a></li>
<li><a class="hover:text-secondary transition-colors" href="/artists/">Artists</a></li>
<li><a class="hover:text-secondary transition-colors" href="{HREF_OFFICIAL_NAP}">Hours &amp; location</a></li>
<li><a class="hover:text-secondary transition-colors" href="/geo_hub_ai_source_of_truth_work_of_art/">{GEO_HUB_CUSTOMER_LABEL}</a></li>
</ul>
</div>
<div class="space-y-3">
<h5 class="font-label-caps text-on-surface uppercase tracking-widest text-[11px]">Hours</h5>
<ul class="space-y-2 text-on-surface-variant text-[13px] font-body-md">
<li>Daily: 12pm - 12am</li>
<li class="pt-2">2375 E. Tropicana Ave, Suite 3<br/>Las Vegas, NV 89119</li>
</ul>
</div>
</div>
<div class="mt-12 pt-8 border-t border-outline-variant/10 flex flex-col md:flex-row justify-between items-center gap-4">
<p class="text-[12px] text-on-surface-variant font-body-md">© {YEAR} Work of Art Tattoo &amp; Piercing · Las Vegas</p>
</div>
"""


def patch_text(raw: str) -> str:
    out = raw
    for old, new in GEO_REPLACEMENTS:
        out = out.replace(old, new)
    out = COPYRIGHT_RE.sub(
        f"© {YEAR} Work of Art Tattoo &amp; Piercing · Las Vegas",
        out,
    )
    return out


def trim_footer(soup: BeautifulSoup) -> bool:
    marker = soup.find(string=lambda t: t and "Footer Links" in t)
    if not marker:
        return False
    parent = marker.parent
    if not parent:
        return False
    grid = parent.find_next("div", class_=lambda c: c and "grid" in c)
    if not grid:
        return False
    slim = BeautifulSoup(SLIM_FOOTER_INNER, "html.parser")
    grid.replace_with(slim)
    # Drop duplicate copyright row if still present above slim block
    for p in parent.find_all("p", class_=lambda c: c and "text-[12px]" in (c or [])):
        if p.get_text() and "©" in p.get_text():
            p.decompose()
    return True


def trim_internal_links(soup: BeautifulSoup) -> bool:
    nav = soup.find(attrs={"data-woa-internal-links": True})
    if not nav:
        return False
    nav.decompose()
    return True


def iter_html() -> list[Path]:
    paths = [p for p in ROOT.glob("*/code.html") if p.parent.name != "skipped_upload_build"]
    paths.append(ROOT / "code.html")
    paths.extend((ROOT / "artists_build").glob("*.html"))
    return sorted(set(paths))


def main() -> int:
    n = 0
    for path in iter_html():
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        updated = patch_text(raw)
        soup = BeautifulSoup(updated, "html.parser")
        changed = updated != raw
        if trim_footer(soup):
            changed = True
        if trim_internal_links(soup):
            changed = True
        if changed:
            path.write_text(str(soup), encoding="utf-8")
            print(f"[ok] {path.relative_to(ROOT)}")
            n += 1
    print(f"done — updated {n} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
