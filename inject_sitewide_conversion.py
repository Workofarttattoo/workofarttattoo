#!/usr/bin/env python3
"""Inject warm text-first conversion blocks on high-traffic pages."""

from __future__ import annotations

import re
from pathlib import Path

from woa_studio_conversion import MARKER, sitewide_conversion_block

ROOT = Path(__file__).resolve().parent

MAJOR_SLUGS: tuple[str, ...] = (
    "home_work_of_art_tattoo_piercing",
    "appointments",
    "official_location_hours_contact",
    "walk-in-tattoos-las-vegas",
    "walk_in_tattoos_las_vegas_authority_guide",
    "tattoo-aftercare-desert-climate",
    "tattoo_healing_in_desert_climate_expert_aftercare_guide",
    "realism_tattoos_las_vegas_master_authority_guide",
    "fine_line_tattoos_las_vegas_master_authority_guide",
    "cover_up_tattoos_las_vegas_master_authority_guide",
    "best_piercing_shop_las_vegas_updated_jewelry_standards",
    "tattoo_shop_near_the_strip_nap_corrected",
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide",
    "how_to_choose_a_tattoo_artist_master_selection_guide_2",
    "reviews_vault_100_verified_masterpieces",
)

BLOCK_RE = re.compile(
    rf'<aside[^>]*{re.escape(MARKER)}[\s\S]*?</aside>\s*',
    re.MULTILINE,
)


def inject(html: str) -> str:
    block = sitewide_conversion_block()
    if MARKER in html:
        return BLOCK_RE.sub(block + "\n", html, count=1)

    for anchor in (
        '<footer class="w-full',
        "</main>",
    ):
        if anchor in html:
            return html.replace(anchor, block + "\n" + anchor, 1)
    return html


def main() -> int:
    n = 0
    for slug in MAJOR_SLUGS:
        path = ROOT / slug / "code.html"
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated = inject(raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {slug}")
            n += 1
    print(f"Done: conversion blocks on {n} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
