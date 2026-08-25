#!/usr/bin/env python3
"""Intent paths for the Start Here visitor hub."""

from __future__ import annotations

from dataclasses import dataclass

START_HERE_SLUG = "start_here"
HREF_START_HERE = f"/{START_HERE_SLUG}/"

START_HERE_TITLE = "Start Here"
START_HERE_META = (
    "Not sure where to begin? Pick your situation — first tattoo, Vegas visit, piercing, "
    "cover-up, healed proof, pricing, or meeting our artists. Work of Art Las Vegas."
)


@dataclass(frozen=True)
class StartHerePath:
    anchor: str
    title: str
    summary: str
    primary_label: str
    primary_href: str
    links: tuple[tuple[str, str], ...]


START_HERE_PATHS: tuple[StartHerePath, ...] = (
    StartHerePath(
        anchor="first-tattoo",
        title="I want my first tattoo",
        summary=(
            "Start with how to read a portfolio, what placement feels like, and what "
            "tattoos cost in Las Vegas before you book."
        ),
        primary_label="How to choose a tattoo artist",
        primary_href="/how_to_choose_a_tattoo_artist_master_selection_guide_2/",
        links=(
            ("Tattoo pain by placement", "/tattoo_pain_chart_placement_sensitivity_guide/"),
            ("Tattoo pricing in Vegas", "/how_much_do_tattoos_cost_in_las_vegas_authority_guide/"),
            ("Desert aftercare basics", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
            ("Skin science — how skin holds ink", "/skin_science_tattoo_dermatology_authority_guide/"),
        ),
    ),
    StartHerePath(
        anchor="visiting-vegas",
        title="I'm visiting Las Vegas",
        summary=(
            "Short drive from the Strip and airport. Walk-ins when chairs are open — "
            "consult-first for custom work."
        ),
        primary_label="Tattoo shop near the Strip",
        primary_href="/tattoo_shop_near_the_strip_nap_corrected/",
        links=(
            ("Walk-in tattoos", "/walk_in_tattoos_las_vegas_authority_guide/"),
            ("Near the airport", "/tattoo_shop_near_las_vegas_airport/"),
            ("Hours & directions", "/official_location_hours_contact/"),
        ),
    ),
    StartHerePath(
        anchor="piercing",
        title="I want a piercing",
        summary=(
            "Placement guides, jewelry-fit planning, and desert aftercare from "
            "Katelyn Cole — ear, facial, oral, and body."
        ),
        primary_label="Complete piercing guide",
        primary_href="/piercing-guide-las-vegas/",
        links=(
            ("Ear piercing guide", "/ear_piercing_guide_las_vegas/"),
            ("Jewelry standards", "/piercing_jewelry_guide_las_vegas/"),
            ("Piercing shop & booking", "/best_piercing_shop_las_vegas_updated_jewelry_standards/"),
        ),
    ),
    StartHerePath(
        anchor="cover-up",
        title="I need a cover-up",
        summary=(
            "Old ink, faded color, or a Strip regret — cover-ups start with a consult "
            "and a realistic plan for sessions and healing."
        ),
        primary_label="Cover-up tattoo guide",
        primary_href="/cover_up_tattoos_las_vegas_master_authority_guide/",
        links=(
            ("Healed cover-up gallery", "/healed_cover_up_tattoos_las_vegas/"),
            ("How to choose an artist", "/how_to_choose_a_tattoo_artist_master_selection_guide_2/"),
            ("Book a consult", "/appointments/"),
        ),
    ),
    StartHerePath(
        anchor="healed-results",
        title="I care about healed results",
        summary=(
            "Fresh photos are easy. We publish healed work at 6–12 months so you can "
            "see how ink holds in Vegas sun."
        ),
        primary_label="Healed tattoo gallery",
        primary_href="/healed_tattoo_gallery_las_vegas/",
        links=(
            ("Healing Database — day 1 to year 1", "/healing_database_tattoo_timeline_encyclopedia_las_vegas/"),
            ("Real client timeline (fresh → 1 year)", "/real_client_tattoo_timeline_las_vegas/"),
            ("Healed black & grey", "/healed_black_grey_tattoos_las_vegas/"),
            ("Studio gallery", "/studio_gallery/"),
        ),
    ),
    StartHerePath(
        anchor="pricing",
        title="I need pricing",
        summary=(
            "Shop minimums, session rates, and what changes your quote — transparent "
            "ranges before you commit."
        ),
        primary_label="Tattoo pricing in Las Vegas",
        primary_href="/how_much_do_tattoos_cost_in_las_vegas_authority_guide/",
        links=(
            ("Flash under $100", "/flash_art_deals_under_100/"),
            ("Walk-in availability", "/walk_in_tattoos_las_vegas_authority_guide/"),
            ("Book a consult", "/appointments/"),
        ),
    ),
    StartHerePath(
        anchor="meet-artists",
        title="I want to meet the artists",
        summary=(
            "Three resident artists in-studio — Joshua Cole (tattoo artist, studio lead, and "
            "piercing trainer), Katelyn Cole (professional piercer), and Teralyn (tattoo artist "
            "and piercer; fineline floral work, script, custom drawings by commission, and "
            "detailed smaller tattoos). Portfolios, videos, and booking."
        ),
        primary_label="Meet our artists",
        primary_href="/artists/",
        links=(
            ("Joshua Cole — tattoo", "/artists/joshua-cole/"),
            ("Teralyn — tattoos & piercing", "/artists/teralyn/"),
            ("Katelyn Cole — piercing", "/artists/katelyn-cole/"),
            ("Client videos", "/studio_videos/"),
        ),
    ),
)
