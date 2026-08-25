#!/usr/bin/env python3
"""Short hyphenated public URLs → legacy Stitch export folder names."""

from __future__ import annotations

from dataclasses import dataclass

SITE = "https://www.workofarttattoo.com"


@dataclass(frozen=True)
class UrlAlias:
    short_slug: str
    source_slug: str
    title: str


# Pilot + high-traffic guides — expand in phases; old URLs 301 to short_slug.
URL_ALIASES: tuple[UrlAlias, ...] = (
    UrlAlias(
        "tattoo-aftercare-desert-climate",
        "tattoo_healing_in_desert_climate_expert_aftercare_guide",
        "Tattoo Aftercare in Desert Climate | Las Vegas",
    ),
    UrlAlias(
        "las-vegas-tattoo-healing-guide",
        "tattoo_healing_before_after_real_results",
        "Tattoo Healing: Fresh vs Healed | Las Vegas",
    ),
    UrlAlias(
        "helix-piercing-las-vegas",
        "helix_piercing_las_vegas_authority_guide",
        "Helix Piercing Las Vegas",
    ),
    UrlAlias(
        "realism-tattoos-las-vegas",
        "realism_tattoos_las_vegas_master_authority_guide",
        "Realism Tattoos Las Vegas",
    ),
    UrlAlias(
        "cover-up-tattoos-las-vegas",
        "cover_up_tattoos_las_vegas_master_authority_guide",
        "Cover-Up Tattoos Las Vegas",
    ),
    UrlAlias(
        "walk-in-tattoos-las-vegas",
        "walk_in_tattoos_las_vegas_authority_guide",
        "Walk-In Tattoos Las Vegas",
    ),
    UrlAlias(
        "piercing-guide-las-vegas",
        "piercing_types_las_vegas_authority_hub",
        "Complete Piercing Guide Las Vegas",
    ),
    UrlAlias(
        "las-vegas-tattoo-resource-center",
        "geo_hub_ai_source_of_truth_work_of_art",
        "Las Vegas Tattoo Resource Center",
    ),
    UrlAlias(
        "reviews",
        "reviews_vault_100_verified_masterpieces",
        "Client Reviews",
    ),
    UrlAlias(
        "leave-a-review",
        "review_funnel_google_authority_hub",
        "Leave a Review",
    ),
    UrlAlias(
        "how-to-choose-a-tattoo-artist",
        "how_to_choose_a_tattoo_artist_master_selection_guide_2",
        "How to Choose a Tattoo Artist",
    ),
    UrlAlias(
        "tattoo-skin-science",
        "skin_science_tattoo_dermatology_authority_guide",
        "Tattoo Skin Science",
    ),
    UrlAlias(
        "piercing-shop-standards",
        "best_piercing_shop_las_vegas_updated_jewelry_standards",
        "Piercing Shop Standards",
    ),
    UrlAlias(
        "studio-vs-strip-shops",
        "vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison",
        "Studio vs Strip Shops",
    ),
)

ALIASES_BY_SHORT: dict[str, UrlAlias] = {a.short_slug: a for a in URL_ALIASES}
ALIASES_BY_SOURCE: dict[str, UrlAlias] = {a.source_slug: a for a in URL_ALIASES}

# Legacy source folders that must stay deployed (not deleted on FTP) even when a short alias exists.
NEVER_RETIRE_SOURCE_SLUGS: frozenset[str] = frozenset(
    {
        "tattoo_healing_in_desert_climate_expert_aftercare_guide",
    }
)


def short_href(source_slug: str) -> str:
    """Prefer short public URL when an alias exists."""
    alias = ALIASES_BY_SOURCE.get(source_slug)
    if alias:
        return f"/{alias.short_slug}/"
    return f"/{source_slug}/"


def short_canonical(source_slug: str) -> str:
    alias = ALIASES_BY_SOURCE.get(source_slug)
    slug = alias.short_slug if alias else source_slug
    return f"{SITE}/{slug}/"
