"""
Shared URLs and guide discovery for Work of Art static HTML navigation.

Deployed paths match stitch_work_of_art_digital_overhaul/*/folder_name/
(except HOME_SLUG maps to site root).

Adjust MERCH_HREF only if merchandise lives elsewhere.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT_A = Path(__file__).resolve().parent
ROOT_B = Path("/Users/noone/Downloads/stitch_work_of_art_digital_overhaul 2")


def _load_site_data(filename: str) -> dict:
    path = ROOT_A / "siteData" / filename
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


_BUSINESS = _load_site_data("business.json")
_SOCIAL = _load_site_data("social.json")

HOME_SLUG = "home_work_of_art_tattoo_piercing"

# In-studio roster (do not inflate headcount in marketing copy)
RESIDENT_ARTIST_COUNT = int(_BUSINESS.get("residentArtistCount", 3))
TATTOO_ARTIST_COUNT = 2
MENTORED_ARTIST_COUNT = 7
STUDIO_ROSTER_BLURB = (
    "Three resident artists work in-studio today — Joshua Cole (tattoo & piercing; "
    "studio lead), Katelyn Cole (master piercer), and Teralyn (fineline floral, script, "
    "custom drawings by commission, and high-detail small tattoos). Book tattoo "
    "and piercing consults at our Tropicana studio seven nights a week."
)
STUDIO_ROSTER_LEGACY = (
    "Seven artists trained at Work of Art now run their own shops or travel as guest "
    "artists — a track record of mentorship, not empty chairs."
)

# Social (full URLs for footers and artist pages)
HREF_INSTAGRAM_STUDIO = _SOCIAL.get("studioInstagram", "https://www.instagram.com/workofarttattoo/")
HREF_INSTAGRAM_KATELYN = _SOCIAL.get("katelynInstagram", "https://www.instagram.com/stabislifee/")
HREF_INSTAGRAM_JOSHUA = _SOCIAL.get("joshuaInstagram", HREF_INSTAGRAM_STUDIO)
HREF_INSTAGRAM_TERALYN = _SOCIAL.get("teralynInstagram", "https://www.instagram.com/mischiefmodifies/")
HREF_INSTAGRAM_JOSHUA_HANDLE = "workofarttattoo"
HREF_INSTAGRAM_KATELYN_HANDLE = "stabislifee"
HREF_INSTAGRAM_TERALYN_HANDLE = "mischiefmodifies"
HREF_FACEBOOK_STUDIO = _SOCIAL.get("facebook", "https://www.facebook.com/workofarttattoo/")

# Public booking inbox (sitewide NAP, footers, schema — not personal Gmail)
STUDIO_BOOKING_EMAIL = _BUSINESS.get("bookingEmail", "booking@workofarttattoo.com")
HREF_BOOKING_MAILTO = f"mailto:{STUDIO_BOOKING_EMAIL}"

# Canonical NAP — must match Google Business Profile & every directory exactly
SITE_CANONICAL_HOST = _BUSINESS.get("canonicalHost", "https://www.workofarttattoo.com")
SITE_CANONICAL_URL = _BUSINESS.get("url", f"{SITE_CANONICAL_HOST}/")
STUDIO_LEGAL_NAME = _BUSINESS.get("name", "Work of Art Tattoo & Piercing")
_ADDRESS = _BUSINESS.get("address", {})
STUDIO_STREET_ADDRESS = _ADDRESS.get("streetAddress", "2375 E. Tropicana Ave, Suite 3")
# Same physical location — Fresha, Apple Maps, and some directories use Ave + unit number
STUDIO_ADDRESS_DIRECTORY = "2375 E. Tropicana Ave, Suite 3"
STUDIO_ADDRESS_ALIASES: tuple[str, ...] = (
    STUDIO_STREET_ADDRESS,
    STUDIO_ADDRESS_DIRECTORY,
    "2375 E. Tropicana Ave, Suite 3",
)
STUDIO_ADDRESS_LOCALITY = _ADDRESS.get("addressLocality", "Las Vegas")
STUDIO_ADDRESS_REGION = _ADDRESS.get("addressRegion", "NV")
STUDIO_POSTAL_CODE = _ADDRESS.get("postalCode", "89119")
STUDIO_ADDRESS_SINGLE_LINE = (
    f"{STUDIO_STREET_ADDRESS}, {STUDIO_ADDRESS_LOCALITY}, "
    f"{STUDIO_ADDRESS_REGION} {STUDIO_POSTAL_CODE}"
)
STUDIO_ADDRESS_HTML = (
    f"{STUDIO_STREET_ADDRESS}<br/>{STUDIO_ADDRESS_LOCALITY}, "
    f"{STUDIO_ADDRESS_REGION} {STUDIO_POSTAL_CODE}"
)

# Single studio line — do not publish artist/mobile lines on the public site
STUDIO_PHONE_DISPLAY = _BUSINESS.get("phoneDisplay", "725-224-1240")
STUDIO_PHONE_PARENS = f"({STUDIO_PHONE_DISPLAY[:3]}) {STUDIO_PHONE_DISPLAY[4:]}" if re.match(r"^\d{3}-\d{3}-\d{4}$", STUDIO_PHONE_DISPLAY) else "(725) 224-1240"
STUDIO_PHONE_E164 = _BUSINESS.get("phoneE164", "+17252241240").replace("+1", "+1-")
STUDIO_PHONE_TEL = f"tel:{_BUSINESS.get('phoneE164', '+17252241240')}"
STUDIO_PHONE_SCHEMA = STUDIO_PHONE_E164

# Homepage SEO — evidence-led, not "Best Tattoo Shop" superlative stacking
HOME_TITLE = "Work of Art Tattoo & Piercing | Las Vegas | Walk-Ins on E. Tropicana"
HOME_META_DESCRIPTION = (
    "Warm, no-attitude tattoo & piercing on E. Tropicana — free consultations, walk-ins welcome. "
    f"Joshua, Katelyn & Teralyn in-studio. Questions encouraged. {STUDIO_PHONE_PARENS}."
)

STUDIO_HOURS_SUMMARY = "Daily 12 PM - 12 AM"
STUDIO_HOURS_HTML_GRID = (
    '<div class="grid grid-cols-2 gap-4">'
    '<p class="text-on-surface-variant">DAILY</p><p>12:00 PM - 12:00 AM</p>'
    "</div>"
)

# Primary links (sitewide; use root-relative anchors that work across pages)
HREF_ARTISTS = "/#gallery"
HREF_PIERCING = "/best_piercing_shop_las_vegas_updated_jewelry_standards/"

# (label, href) — sitewide Artists dropdown
ARTIST_NAV_ENTRIES: list[tuple[str, str]] = [
    ("All Artists & Gallery", HREF_ARTISTS),
    ("Joshua Cole — Tattoo & Piercing", "/artists/joshua-cole/"),
    ("Katelyn Cole — Master Piercer", "/artists/katelyn-cole/"),
    ("Teralyn — Fineline Floral & Script", "/artists/teralyn/"),
]


def discover_artist_nav_entries() -> list[tuple[str, str]]:
    """Returns artist dropdown links (label, href)."""
    return list(ARTIST_NAV_ENTRIES)


MERCH_HREF = "/merchandise/"
HREF_REVIEWS = "/reviews_vault_100_verified_masterpieces/"
HREF_APPOINTMENTS = "/appointments/"
HREF_OFFICIAL_NAP = "/official_location_hours_contact/"

# Visitor hub — intent-based entry to the guide library
from woa_start_here import HREF_START_HERE  # noqa: E402

HREF_KNOWLEDGE_VAULT = HREF_START_HERE
HREF_GUIDES_INDEX = "/piercing-guide-las-vegas/"
NAV_KNOWLEDGE_MENU_LABEL = "Start Here"
NAV_KNOWLEDGE_VAULT_LINK_LABEL = "Start here"
GEO_HUB_CUSTOMER_LABEL = "Las Vegas Tattoo Resource Center"

# Top-level nav: no flat featured guide links (nested dropdowns only)
FEATURED_GUIDE_NAV_SLUGS: tuple[str, ...] = ()

FEATURED_GUIDE_SHORT_LABELS: dict[str, str] = {}

NAV_PORTFOLIO: list[tuple[str, str]] = [
    ("Gallery & portfolio", "/#gallery"),
    ("Studio gallery", "/studio_gallery/"),
    ("Healed tattoo proof", "/healed_tattoo_gallery_las_vegas/"),
    ("Client videos", "/studio_videos/"),
]

NAV_TATTOO_GUIDE_SLUGS: tuple[str, ...] = (
    "how_to_choose_a_tattoo_artist_master_selection_guide_2",
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide",
    "realism_tattoos_las_vegas_master_authority_guide",
    "cover_up_tattoos_las_vegas_master_authority_guide",
    "walk_in_tattoos_las_vegas_authority_guide",
    "tattoo_healing_in_desert_climate_expert_aftercare_guide",
    "skin_science_tattoo_dermatology_authority_guide",
    "healing_database_tattoo_timeline_encyclopedia_las_vegas",
    "healed_tattoo_gallery_las_vegas",
    "real_client_tattoo_timeline_las_vegas",
    "best_tattoo_styles_for_sleeves_large_scale_project_hub",
    "vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison",
)

NAV_PIERCING_GUIDE_SLUGS: tuple[str, ...] = (
    "piercing_types_las_vegas_authority_hub",
    "ear_piercing_guide_las_vegas",
    "facial_piercing_guide_las_vegas",
    "body_piercing_guide_las_vegas",
    "piercing_jewelry_guide_las_vegas",
    "piercing_aftercare_guide_las_vegas",
    "helix_piercing_las_vegas_authority_guide",
    "best_piercing_shop_las_vegas_updated_jewelry_standards",
    "katelyn_cole_piercing_authority_hub_las_vegas",
)

NAV_LOCATION_SLUGS: tuple[str, ...] = (
    "official_location_hours_contact",
    "tattoo_shop_near_the_strip_nap_corrected",
    "tattoo_shop_near_mgm_grand_las_vegas",
    "tattoo_shop_near_allegiant_stadium_las_vegas",
    "tattoo_shop_near_las_vegas_airport",
    "tattoo_shop_near_the_sphere_las_vegas",
    "tattoo_shop_paradise_nevada",
    "tattoo_shop_spring_valley_las_vegas",
    "tattoo_shop_enterprise_las_vegas",
    "tattoo_shop_green_valley_henderson",
    "geo_hub_ai_source_of_truth_work_of_art",
)

# Exclude from "Guides" mega-list — home is duplicated as index; uploads often WP mirrors
SKIP_GUIDE_SLUGS = frozenset(
    {
        HOME_SLUG,
        "start_here",
        "skipped_upload_build",
        "skipped_pages_clipboard.html",
        "skipped_pages_clipboard",
        "appointments", "how_to_choose_a_tattoo_artist_master_selection_guide_1", "how_to_choose_a_tattoo_artist_master_selection_guide", "walk_in_tattoos_las_vegas_nap_corrected", "tattoo_shop_near_the_strip_geo_seo_optimized", "tattoo_shop_near_the_strip_nap_corrected", "jay_jay_artist_portfolio_authentic_masterpieces",
    }
)


def merged_export_roots() -> dict[str, Path]:
    """Prefer later roots (ROOT_B overrides ROOT_A slug path for deploy merges)."""
    merged: dict[str, Path] = {}
    for base in (ROOT_A, ROOT_B):
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir()):
            if not child.is_dir():
                continue
            if child.name.startswith("."):
                continue
            if (child / "code.html").is_file():
                merged[child.name] = child
    return merged


def slug_to_guide_label(slug: str, max_len: int = 46) -> str:
    readable = slug.replace("_", " ").replace("authority guide", "").replace("master selection guide", "").replace("ultimate authority guide", "").strip()
    if len(readable) > max_len:
        readable = readable[: max_len - 1].rstrip() + "…"
    return readable


# Short titles + blurbs for nav, guide hub bar, and homepage knowledge base
GUIDE_META: dict[str, tuple[str, str]] = {
    "start_here": (
        "Start Here",
        "Pick your situation — first tattoo, Vegas visit, piercing, cover-up, healed proof, pricing, or meet the artists.",
    ),
    "best_fine_line_tattoos_in_vegas_ultimate_authority_guide": (
        "Fine Line Tattoos in Vegas",
        "Needle-light linework, healed clarity, and how to pick an artist for delicate script and micro-detail.",
    ),
    "cover_up_tattoos_las_vegas_master_authority_guide": (
        "Cover-Up Tattoos in Vegas",
        "Tattoo cover up, scar camouflage, real studio portfolio photos, pricing, and free consult — minutes from the Strip.",
    ),
    "best_piercing_shop_las_vegas_updated_jewelry_standards": (
        "Piercing Shop & Jewelry Standards",
        "Implant-grade jewelry, sterile technique, and what separates a premium Vegas piercing studio.",
    ),
    "piercing_types_las_vegas_authority_hub": (
        "Complete Piercing Guide",
        "Piercing placement guides, jewelry tips, and aftercare from Katelyn Cole.",
    ),
    "ear_piercing_guide_las_vegas": (
        "Ear Piercing Guide",
        "Helix, conch, tragus, daith, industrial, and curated ears — placement guides by area.",
    ),
    "facial_piercing_guide_las_vegas": (
        "Facial Piercing Guide",
        "Nostril, septum, bridge, and eyebrow piercing — anatomy-first marking in Las Vegas.",
    ),
    "oral_piercing_guide_las_vegas": (
        "Oral Piercing Guide",
        "Tongue, labret, philtrum, and lip piercing — downsizing, swelling, and tooth-safe jewelry.",
    ),
    "body_piercing_guide_las_vegas": (
        "Body Piercing Guide",
        "Navel and nipple piercing guides with anatomy assessment and private consults.",
    ),
    "piercing_aftercare_guide_las_vegas": (
        "Piercing Aftercare Guide",
        "How to clean, sleep, swim, and gym with a fresh piercing in Las Vegas.",
    ),
    "piercing_jewelry_guide_las_vegas": (
        "Piercing Jewelry Guide",
        "Implant-grade titanium, threadless ends, downsizing, and gold vs titanium.",
    ),
    "piercing_healing_guide_las_vegas": (
        "Piercing Healing Guide",
        "Healing timelines by placement — lobe, cartilage, oral, and body piercings.",
    ),
    "katelyn_cole_piercing_authority_hub_las_vegas": (
        "Katelyn Cole Piercing Authority",
        "Implant-grade titanium, ear curation, anatomy, downsizing, and piercing expertise from Katelyn Cole.",
    ),
    "piercing_aftercare_desert_climate_las_vegas_expert_guide": (
        "Desert Piercing Aftercare",
        "Las Vegas piercing aftercare — dry heat, pools, dust, gym sweat, and saline routines by Katelyn Cole.",
    ),
    "best_tattoo_styles_for_sleeves_large_scale_project_hub": (
        "Sleeve & Large-Scale Tattoo Styles",
        "Planning full sleeves and big projects: style fit, sessions, and building cohesive large-scale art.",
    ),
    "fine_line_tattoos_las_vegas_master_authority_guide": (
        "Fine Line Tattoo Guide",
        "Needle depth, ink load, artist selection, and aftercare for fine line work in desert heat.",
    ),
    "real_client_tattoo_timeline_las_vegas": (
        "Real Client Tattoo Timeline",
        "One tattoo documented fresh to 1 year — cross, eye & skull forearm by Joshua Cole. Honest heal stages.",
    ),
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide": (
        "Tattoo Pricing in Las Vegas",
        "Transparent breakdown of shop rates, artist tiers, size, and what affects your quote.",
    ),
    "how_to_choose_a_tattoo_artist_master_selection_guide_2": (
        "How to Choose a Tattoo Artist",
        "Portfolio signals, hygiene standards, and matching the right artist to your vision.",
    ),
    "large_scale_projects_variant_a_authentic_art_rotation": (
        "Large-Scale Project Planning",
        "Multi-session roadmaps, reference prep, and timelines for ambitious tattoo projects.",
    ),
    "realism_tattoos_las_vegas_master_authority_guide": (
        "Realism Tattoos in Vegas",
        "Black-and-grey and color realism: what to expect, healing, and artist fit near the Strip.",
    ),
    "review_funnel_google_authority_hub": (
        "Leave a Google Review",
        "Scan our in-studio QR or NFC sign to share your experience and support our artists.",
    ),
    "reviews_vault_100_verified_masterpieces": (
        "Verified Client Reviews",
        "Real healed work and Google feedback from clients who booked with the studio.",
    ),
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": (
        "Desert Climate Aftercare",
        "Vegas-specific healing: sun, dryness, and step-by-step aftercare that protects your ink.",
    ),
    "healing_database_tattoo_timeline_encyclopedia_las_vegas": (
        "Tattoo Healing Database",
        "Day 1 through year 1 encyclopedia by style — what's normal, desert notes, and honest studio photos.",
    ),
    "skin_science_tattoo_dermatology_authority_guide": (
        "Skin Science for Tattoo Collectors",
        "How skin layers, immune cells, and collagen hold ink — plus conditions that change tattoo planning.",
    ),
    "epidermis_skin_science_las_vegas_authority_guide": (
        "Epidermis & Tattoo Healing",
        "Outer skin layer turnover, peeling, and why surface ink does not stay.",
    ),
    "dermis_skin_science_las_vegas_authority_guide": (
        "Dermis — Where Ink Lives",
        "Needle depth, collagen matrix, and why the dermis holds pigment for life.",
    ),
    "hypodermis_skin_science_las_vegas_authority_guide": (
        "Hypodermis & Blowouts",
        "Fat layer anatomy and why ink in subcutaneous tissue blurs.",
    ),
    "why_tattoos_stay_forever_skin_science_las_vegas_authority_guide": (
        "Why Tattoos Stay Forever",
        "Particle size, dermal trapping, and what still fades over decades.",
    ),
    "macrophages_skin_science_las_vegas_authority_guide": (
        "Macrophages & Tattoo Ink",
        "Immune cells that engulf pigment and lock color in the dermis.",
    ),
    "collagen_skin_science_las_vegas_authority_guide": (
        "Collagen & Tattoos",
        "Dermal scaffold, healing, and how structure affects line clarity.",
    ),
    "scar_tissue_tattoo_skin_science_las_vegas_authority_guide": (
        "Scar Tissue & Tattoos",
        "Why scars tattoo differently — timing, technique, and cover-ups.",
    ),
    "stretch_marks_skin_science_las_vegas_authority_guide": (
        "Stretch Marks & Tattoos",
        "Striae anatomy, pregnancy timing, and design strategies.",
    ),
    "eczema_skin_science_las_vegas_authority_guide": (
        "Eczema & Tattoos",
        "Barrier flares, Koebner risk, and when to wait — consult your dermatologist.",
    ),
    "psoriasis_skin_science_las_vegas_authority_guide": (
        "Psoriasis & Tattoos",
        "Koebner phenomenon, biologics, and dermatologist clearance.",
    ),
    "diabetes_skin_science_las_vegas_authority_guide": (
        "Diabetes & Tattoo Healing",
        "Blood sugar, neuropathy, and studio requirements for safe healing.",
    ),
    "aging_skin_skin_science_las_vegas_authority_guide": (
        "Aging Skin & Tattoos",
        "Collagen loss, sun damage, and design choices that age well.",
    ),
    "tattoo_healing_before_after_real_results": (
        "Fresh vs Healed Healing",
        "Real studio photos — same color memorial tattoos fresh and months later. Why ink lightens and what is normal.",
    ),
    "healed_tattoo_gallery_las_vegas": (
        "Healed Tattoo Gallery",
        "Fresh and healed documentation by style — black and grey, fine line, color, cover-ups, sleeves, and portraits.",
    ),
    "healed_black_grey_tattoos_las_vegas": (
        "Healed Black & Grey Tattoos",
        "How black and grey realism settles over months — contrast, open skin, and readability in desert sun.",
    ),
    "healed_fine_line_tattoos_las_vegas": (
        "Healed Fine Line Tattoos",
        "Delicate linework after healing — what stays crisp and how we plan fine line for longevity.",
    ),
    "healed_color_tattoos_las_vegas": (
        "Healed Color Tattoos",
        "Same clients photographed fresh and healed — realistic color saturation over time.",
    ),
    "healed_cover_up_tattoos_las_vegas": (
        "Healed Cover-Up Tattoos",
        "Cover-up redesigns judged at 90 days and beyond — not day-one studio lighting.",
    ),
    "healed_sleeve_tattoos_las_vegas": (
        "Healed Sleeve Tattoos",
        "Large-scale sleeves with session notes, touch-ups, and healed clarity.",
    ),
    "healed_portrait_tattoos_las_vegas": (
        "Healed Portrait Tattoos",
        "Portrait and figurative work after skin settles — values, likeness, and aftercare.",
    ),
    "joshua_oil_painting_black_grey_tattoo_aging_las_vegas": (
        "Oil Painting & Tattoo Aging",
        "How Joshua Cole's classical painting training shapes black and grey design for long-term healing.",
    ),
    "tattoo_pain_chart_placement_sensitivity_guide": (
        "Tattoo Pain & Placement Chart",
        "Body-area sensitivity guide so you can plan size, placement, and session comfort.",
    ),
    "tattoo_shop_near_the_strip_geo_seo_optimized": (
        "Tattoo Shop Near the Strip",
        "Location, parking, and why locals and tourists choose us minutes from the Las Vegas Strip.",
    ),
    "tattoo_shop_near_the_strip_nap_corrected": (
        "Studio Location & Hours",
        "Directions to Work of Art at 2375 E. Tropicana Ave, Suite 3 — easy access from the Strip and airport.",
    ),
    "vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison": (
        "Premium Studio vs. Cheap Strip Shops",
        "Side-by-side comparison of hygiene, artistry, and long-term value before you book.",
    ),
    "vegas_tattoo_shop_vs_cheap_strip_tattoo_what_you_need_to_know": (
        "What to Know Before You Ink",
        "Red flags, pricing traps, and how to avoid regret on vacation tattoos in Vegas.",
    ),
    "walk_in_tattoos_las_vegas_authority_guide": (
        "Walk-In Tattoos in Las Vegas",
        "Same-day availability, sizing limits, and how walk-ins work at our Tropicana studio.",
    ),
    "helix-piercing-las-vegas": (
        "Helix Piercing Las Vegas",
        "Placement, jewelry, healing timeline, and ear curation from Katelyn Cole.",
    ),
    "helix_piercing_las_vegas_authority_guide": (
        "Helix Piercing Guide",
        "Placement, jewelry, healing timeline, and ear curation from Katelyn Cole.",
    ),
    "official_location_hours_contact": (
        "Official Location & Hours",
        "Verified studio address, phone, hours, and contact details.",
    ),
    "tattoo_shop_near_mgm_grand_las_vegas": (
        "Near MGM Grand",
        "Directions from MGM Grand to Work of Art on E. Tropicana.",
    ),
    "tattoo_shop_near_allegiant_stadium_las_vegas": (
        "Near Allegiant Stadium",
        "Directions from Allegiant Stadium to Work of Art on E. Tropicana.",
    ),
    "tattoo_shop_near_las_vegas_airport": (
        "Near Las Vegas Airport",
        "Directions from Harry Reid airport to Work of Art on E. Tropicana.",
    ),
    "tattoo_shop_near_the_sphere_las_vegas": (
        "Near the Sphere",
        "Directions from the Sphere to Work of Art on E. Tropicana.",
    ),
    "tattoo_shop_paradise_nevada": (
        "Paradise, NV",
        "Local route and studio details for Paradise visitors.",
    ),
    "tattoo_shop_spring_valley_las_vegas": (
        "Spring Valley",
        "Local route and studio details for Spring Valley visitors.",
    ),
    "tattoo_shop_enterprise_las_vegas": (
        "Enterprise",
        "Local route and studio details for Enterprise visitors.",
    ),
    "tattoo_shop_green_valley_henderson": (
        "Green Valley / Henderson",
        "Local route and studio details for Green Valley and Henderson visitors.",
    ),
    "realism-tattoos-las-vegas": (
        "Realism Tattoos Las Vegas",
        "Black-and-grey and color realism — portfolio, healing, and artist fit near the Strip.",
    ),
    "cover-up-tattoos-las-vegas": (
        "Cover-Up Tattoos Las Vegas",
        "Scar camouflage, redesign consults, and healed cover-up proof from the studio.",
    ),
    "walk-in-tattoos-las-vegas": (
        "Walk-In Tattoos Las Vegas",
        "Same-day chairs when available — text first for today's openings.",
    ),
    "piercing-guide-las-vegas": (
        "Complete Piercing Guide Las Vegas",
        "All placement guides, jewelry standards, and Katelyn Cole's piercing hub.",
    ),
    "tattoo-aftercare-desert-climate": (
        "Desert Tattoo Aftercare",
        "Vegas-specific healing — sun, dryness, and step-by-step aftercare.",
    ),
    "las-vegas-tattoo-healing-guide": (
        "Fresh vs Healed Healing",
        "Real studio photos — same tattoos fresh and months later.",
    ),
    "flash_art_deals_under_100": (
        "Flash Under $100",
        "Palm-size flash tattoos from our studio sheets — under one hour, from $100. Walk-in friendly.",
    ),
    "studio_gallery": (
        "Studio Gallery",
        "Completed tattoos, original art, designs to book, and piercing work from Joshua and Katelyn Cole at Work of Art Las Vegas.",
    ),
    "offsite_bookings": (
        "Offsite Bookings",
        "Joshua Cole mobile tattoo studio for VIP private events — documented offsite work including Party at Mike Tyson's House.",
    ),
    "geo_hub_ai_source_of_truth_work_of_art": (
        GEO_HUB_CUSTOMER_LABEL,
        "Verified studio address, hours, resident artists, safety standards, and local tattoo & piercing guides.",
    ),
}


def guide_nav_label(slug: str, max_len: int = 40) -> str:
    if slug in GUIDE_META:
        title = GUIDE_META[slug][0]
        if len(title) <= max_len:
            return title
        return title[: max_len - 1].rstrip() + "…"
    return slug_to_guide_label(slug, max_len)


def guide_blurb(slug: str) -> str:
    if slug in GUIDE_META:
        return GUIDE_META[slug][1]
    return f"Expert guide from Work of Art Tattoo & Piercing — {slug_to_guide_label(slug, 120)}."


def discover_guide_entries() -> list[tuple[str, str, str, str]]:
    """Sorted (slug, label, href, blurb) for every informational guide page."""
    from woa_url_aliases import ALIASES_BY_SOURCE, NEVER_RETIRE_SOURCE_SLUGS, short_href

    rows: list[tuple[str, str, str, str]] = []
    for slug in merged_export_roots():
        if slug in SKIP_GUIDE_SLUGS:
            continue
        if slug in ALIASES_BY_SOURCE and slug not in NEVER_RETIRE_SOURCE_SLUGS:
            continue
        href = short_href(slug)
        rows.append((slug, guide_nav_label(slug), href, guide_blurb(slug)))
    rows.sort(key=lambda r: r[1].lower())
    return rows


def discover_guide_pairs() -> list[tuple[str, str]]:
    """
    Returns sorted (label, href) for every export folder containing code.html
    minus SKIP_GUIDE_SLUGS (home, upload staging, etc.).
    """
    return [(label, href) for _slug, label, href, _blurb in discover_guide_entries()]


def discover_featured_guide_nav() -> list[tuple[str, str]]:
    """Top-level nav links for highest-intent insider guides (empty — use dropdowns)."""
    return []


def nav_entries_for_slugs(slugs: tuple[str, ...]) -> list[tuple[str, str]]:
    """Resolve curated slug lists to (label, public href) for nav dropdowns."""
    from woa_url_aliases import ALIASES_BY_SOURCE, short_href

    merged = merged_export_roots()
    out: list[tuple[str, str]] = []
    for slug in slugs:
        alias = ALIASES_BY_SOURCE.get(slug)
        public_slug = alias.short_slug if alias else slug
        if public_slug not in merged and slug not in merged:
            continue
        label = (
            GEO_HUB_CUSTOMER_LABEL
            if slug == "geo_hub_ai_source_of_truth_work_of_art"
            else guide_nav_label(slug)
        )
        out.append((label, short_href(slug)))
    return out


def discover_nav_tattoo_guides() -> list[tuple[str, str]]:
    return nav_entries_for_slugs(NAV_TATTOO_GUIDE_SLUGS)


def discover_nav_piercing_guides() -> list[tuple[str, str]]:
    return nav_entries_for_slugs(NAV_PIERCING_GUIDE_SLUGS)


def discover_nav_locations() -> list[tuple[str, str]]:
    return nav_entries_for_slugs(NAV_LOCATION_SLUGS)


def discover_dropdown_guide_entries() -> list[tuple[str, str, str, str]]:
    """Legacy — full guide list (prefer categorized nav dropdowns)."""
    return discover_guide_entries()
