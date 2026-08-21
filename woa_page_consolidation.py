"""Canonical URLs and retire/301 rules for overlapping content."""

from __future__ import annotations

# Legacy slug → canonical public path (301 on deploy)
CONSOLIDATION_REDIRECTS: tuple[tuple[str, str], ...] = (
    (
        "tattoo_shop_near_the_strip_geo_seo_optimized",
        "/tattoo_shop_near_the_strip_nap_corrected/",
    ),
    (
        "how_to_choose_a_tattoo_artist_master_selection_guide",
        "/how_to_choose_a_tattoo_artist_master_selection_guide_2/",
    ),
    (
        "walk_in_tattoos_las_vegas_nap_corrected",
        "/walk-in-tattoos-las-vegas/",
    ),
)

RETIRE_OVERLAP_SLUGS: frozenset[str] = frozenset(
    src for src, _dest in CONSOLIDATION_REDIRECTS
)

CANONICAL_STRIP_DIRECTIONS = "/tattoo_shop_near_the_strip_nap_corrected/"
CANONICAL_OFFICIAL_NAP = "/official_location_hours_contact/"

# Sitewide href replacements (old path fragment → canonical)
HREF_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("/tattoo_shop_near_the_strip_geo_seo_optimized/", CANONICAL_STRIP_DIRECTIONS),
    ("/how_to_choose_a_tattoo_artist_master_selection_guide/", "/how_to_choose_a_tattoo_artist_master_selection_guide_2/"),
    ("/walk_in_tattoos_las_vegas_nap_corrected/", "/walk-in-tattoos-las-vegas/"),
)
