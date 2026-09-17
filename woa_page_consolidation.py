"""Canonical URLs and retire/301 rules for overlapping content."""

from __future__ import annotations

# GSC Wizard obsolete URLs (2026-09) — Cloudflare one-hop 301 targets.
GSC_OBSOLETE_SLUG_REDIRECTS: tuple[tuple[str, str], ...] = (
    ("realism_tattoos_las_vegas_master_authority_guide", "/realism-tattoos-las-vegas/"),
    ("skin_science_tattoo_dermatology_authority_guide", "/tattoo-skin-science/"),
    ("walk_in_tattoos_las_vegas_authority_guide", "/walk-in-tattoos-las-vegas/"),
    (
        "tattoo_healing_in_desert_climate_expert_aftercare_guide",
        "/tattoo-aftercare-desert-climate/",
    ),
    ("piercing_types_las_vegas_authority_hub", "/piercing-guide-las-vegas/"),
    ("tattoo_healing_before_after_real_results", "/las-vegas-tattoo-healing-guide/"),
    (
        "vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison",
        "/vegas_tattoo_shop_vs_cheap_strip_tattoo_what_you_need_to_know/",
    ),
    ("review_funnel_google_authority_hub", "/reviews/"),
)

GSC_OBSOLETE_PATH_REDIRECTS: tuple[tuple[str, str], ...] = (
    (
        "/knowledge/implant-grade-titanium-vs-surgical-steel/",
        "/katelyn_implant_grade_titanium_las_vegas_authority_guide/",
    ),
)

# Complete GSC Wizard list (16 obsolete URLs → canonical targets).
GSC_WIZARD_OBSOLETE_REDIRECTS: tuple[tuple[str, str], ...] = (
    ("/realism_tattoos_las_vegas_master_authority_guide/", "/realism-tattoos-las-vegas/"),
    ("/skin_science_tattoo_dermatology_authority_guide/", "/tattoo-skin-science/"),
    ("/walk_in_tattoos_las_vegas_authority_guide/", "/walk-in-tattoos-las-vegas/"),
    (
        "/tattoo_healing_in_desert_climate_expert_aftercare_guide/",
        "/tattoo-aftercare-desert-climate/",
    ),
    ("/piercing_types_las_vegas_authority_hub/", "/piercing-guide-las-vegas/"),
    ("/tattoo_healing_before_after_real_results/", "/las-vegas-tattoo-healing-guide/"),
    ("/tattoo_shop_near_the_strip_geo_seo_optimized/", "/tattoo_shop_near_the_strip_nap_corrected/"),
    ("/how_to_choose_a_tattoo_artist_master_selection_guide_2/", "/how-to-choose-a-tattoo-artist/"),
    (
        "/vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison/",
        "/vegas_tattoo_shop_vs_cheap_strip_tattoo_what_you_need_to_know/",
    ),
    ("/cover_up_tattoos_las_vegas_master_authority_guide/", "/cover-up-tattoos-las-vegas/"),
    ("/tattoo_shop_near_las_vegas_convention_center/", "/tattoo_shop_near_the_strip_nap_corrected/"),
    (
        "/healing_database_tattoo_timeline_encyclopedia_las_vegas/",
        "/real_client_tattoo_timeline_las_vegas/",
    ),
    ("/tattoo_shop_enterprise_las_vegas/", "/official_location_hours_contact/"),
    ("/tattoo_shop_green_valley_henderson/", "/tattoo_shop_serving_henderson_nevada/"),
    GSC_OBSOLETE_PATH_REDIRECTS[0],
    ("/review_funnel_google_authority_hub/", "/reviews/"),
)


def gsc_obsolete_slug_redirects() -> dict[str, str]:
    return dict(GSC_OBSOLETE_SLUG_REDIRECTS)


def gsc_obsolete_paths() -> tuple[str, ...]:
    return tuple(src for src, _dest in GSC_WIZARD_OBSOLETE_REDIRECTS)


def gsc_wizard_redirect_map() -> dict[str, str]:
    return {src: dest for src, dest in GSC_WIZARD_OBSOLETE_REDIRECTS}


# Legacy slug -> canonical public path (301 on deploy)
CONSOLIDATION_REDIRECTS: tuple[tuple[str, str], ...] = (
    ("tattoo_shop_near_the_strip_geo_seo_optimized", "/tattoo_shop_near_the_strip_nap_corrected/"),
    ("tattoo_shop_serving_summerlin_las_vegas", "/tattoo_shop_spring_valley_las_vegas/"),
    ("tattoo_shop_serving_downtown_las_vegas", "/tattoo_shop_near_the_strip_nap_corrected/"),
    ("tattoo_piercing_shop_near_unlv", "/tattoo_shop_paradise_nevada/"),
    ("tattoo_shop_enterprise_las_vegas", "/official_location_hours_contact/"),
    ("tattoo_shop_green_valley_henderson", "/tattoo_shop_serving_henderson_nevada/"),
    ("tattoo_shop_serving_north_las_vegas", "/tattoo_shop_near_the_strip_nap_corrected/"),
    ("tattoo_shop_near_las_vegas_convention_center", "/tattoo_shop_near_the_strip_nap_corrected/"),
    ("tattoo_shop_near_mandalay_bay_las_vegas", "/tattoo_shop_near_allegiant_stadium_las_vegas/"),
    ("tattoo_shop_near_t_mobile_arena_las_vegas", "/tattoo_shop_near_mgm_grand_las_vegas/"),
    ("tattoo_shop_near_fashion_show_las_vegas", "/tattoo_shop_near_the_sphere_las_vegas/"),
    ("tattoo_shop_near_fremont_street_las_vegas", "/tattoo_shop_near_the_strip_nap_corrected/"),
    ("how_to_choose_a_tattoo_artist_master_selection_guide", "/how-to-choose-a-tattoo-artist/"),
    ("how_to_choose_a_tattoo_artist_master_selection_guide_2", "/how-to-choose-a-tattoo-artist/"),
    ("walk_in_tattoos_las_vegas_nap_corrected", "/walk-in-tattoos-las-vegas/"),
    ("cover_up_tattoos_las_vegas_master_authority_guide", "/cover-up-tattoos-las-vegas/"),
    ("healing_database_black_grey_day_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_day_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_day_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_day_4_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_month_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_month_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_month_6_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_tattoos_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_week_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_week_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_week_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_black_grey_year_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_day_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_day_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_day_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_day_4_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_month_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_month_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_month_6_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_tattoos_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_week_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_week_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_week_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_color_year_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_day_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_day_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_day_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_day_4_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_month_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_month_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_month_6_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_tattoos_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_week_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_week_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_week_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_cover_ups_year_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_day_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_day_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_day_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_day_4_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_month_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_month_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_month_6_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_tattoos_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_week_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_week_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_week_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_fine_line_year_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_day_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_day_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_day_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_day_4_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_month_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_month_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_month_6_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_tattoos_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_week_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_week_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_week_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_neo_traditional_year_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_day_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_day_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_day_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_day_4_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_month_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_month_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_month_6_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_tattoos_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_week_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_week_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_week_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_portraits_year_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_day_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_day_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_day_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_day_4_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_month_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_month_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_month_6_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_timeline_encyclopedia_las_vegas", "/real_client_tattoo_timeline_las_vegas/"),
    ("healing_database_tattoo_week_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_week_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_week_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_tattoo_year_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_day_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_day_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_day_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_day_4_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_month_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_month_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_month_6_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_tattoos_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_week_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_week_2_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_week_3_las_vegas", "/las-vegas-tattoo-healing-guide/"),
    ("healing_database_traditional_year_1_las_vegas", "/las-vegas-tattoo-healing-guide/"),
)

RETIRE_OVERLAP_SLUGS: frozenset[str] = frozenset(
    src for src, _dest in CONSOLIDATION_REDIRECTS
) | frozenset(gsc_obsolete_slug_redirects())

CANONICAL_STRIP_DIRECTIONS = "/tattoo_shop_near_the_strip_nap_corrected/"
CANONICAL_OFFICIAL_NAP = "/official_location_hours_contact/"

# Sitewide href replacements (old path fragment -> canonical)
_slug_href_map: dict[str, str] = dict(CONSOLIDATION_REDIRECTS)
_slug_href_map.update(gsc_obsolete_slug_redirects())
HREF_REPLACEMENTS: tuple[tuple[str, str], ...] = tuple(
    (f"/{src}/", dest) for src, dest in sorted(_slug_href_map.items())
)
ALL_HREF_REPLACEMENTS: tuple[tuple[str, str], ...] = HREF_REPLACEMENTS + GSC_OBSOLETE_PATH_REDIRECTS
