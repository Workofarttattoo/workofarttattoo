#!/usr/bin/env python3
"""Inject reusable piercing promotion modules into selected high-value pages."""

from __future__ import annotations

import re
from pathlib import Path

from woa_piercing_promotions import render_current_piercing_special, render_piercing_decision_module

ROOT = Path(__file__).resolve().parent
MARKER_START = "<!-- WOA_PIERCING_PROMO_START -->"
MARKER_END = "<!-- WOA_PIERCING_PROMO_END -->"
BLOCK_RE = re.compile(r"<!-- WOA_PIERCING_PROMO_START -->[\s\S]*?<!-- WOA_PIERCING_PROMO_END -->\s*")

PROMO_TARGETS: dict[str, tuple[str, str]] = {
    "home_work_of_art_tattoo_piercing": ("compact", "homepage"),
    "artists/katelyn-cole": ("standard", "katelyn-artist"),
    "ear_piercing_guide_las_vegas": ("compact", "ear-guide"),
    "tattoo_shop_near_the_strip_nap_corrected": ("compact", "near-strip"),
    "tattoo_piercing_shop_near_unlv": ("compact", "unlv"),
    "tattoo_shop_near_paradise_las_vegas": ("compact", "paradise"),
    "tattoo_shop_near_las_vegas_airport": ("compact", "airport"),
    "tattoo_shop_near_mgm_grand_las_vegas": ("compact", "mgm-grand"),
    "tattoo_shop_paradise_nevada": ("compact", "paradise"),
}

PROMO_FILE_TARGETS: dict[str, tuple[str, str]] = {
    "artists_build/katelyn-cole.html": ("standard", "katelyn-artist"),
}


def wrapped(block: str) -> str:
    return f"{MARKER_START}\n{block}\n{MARKER_END}\n"


def inject_after_first_section(raw: str, block: str) -> str:
    replacement = wrapped(block)
    raw = BLOCK_RE.sub("", raw)
    match = re.search(r"</section>", raw)
    if match:
        pos = match.end()
        return raw[:pos] + "\n" + replacement + raw[pos:]
    return raw


def inject_before_second_section(raw: str, block: str) -> str:
    replacement = wrapped(block)
    raw = BLOCK_RE.sub("", raw)
    matches = list(re.finditer(r"<section\b", raw))
    if len(matches) >= 2:
        pos = matches[1].start()
        return raw[:pos] + replacement + raw[pos:]
    return inject_after_first_section(raw, block)


def patch_main_piercing(raw: str) -> str:
    marker = 'data-woa-piercing-decision="1"'
    raw = re.sub(r'<section[^>]*data-woa-piercing-decision="1"[\s\S]*?</section>\s*', "", raw, count=1)
    if marker in raw:
        return raw
    main = render_piercing_decision_module()
    return inject_before_second_section(raw, main)


def main() -> int:
    updated = 0
    main_path = ROOT / "best_piercing_shop_las_vegas_updated_jewelry_standards" / "code.html"
    if main_path.is_file():
        raw = main_path.read_text(encoding="utf-8")
        new = patch_main_piercing(raw)
        if new != raw:
            main_path.write_text(new, encoding="utf-8")
            print("[ok] best_piercing_shop_las_vegas_updated_jewelry_standards")
            updated += 1

    for slug, (variant, context) in PROMO_TARGETS.items():
        path = ROOT / slug / "code.html"
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        block = render_current_piercing_special(variant=variant, context=context)
        new = inject_after_first_section(raw, block)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            print(f"[ok] {slug}")
            updated += 1

    for file_name, (variant, context) in PROMO_FILE_TARGETS.items():
        path = ROOT / file_name
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        block = render_current_piercing_special(variant=variant, context=context)
        new = inject_after_first_section(raw, block)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            print(f"[ok] {file_name}")
            updated += 1

    print(f"Done: piercing promotion modules on {updated} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
