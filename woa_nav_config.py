"""
Shared URLs and guide discovery for Work of Art static HTML navigation.

Deployed paths match stitch_work_of_art_digital_overhaul/*/folder_name/
(except HOME_SLUG maps to site root).

Adjust MERCH_HREF only if merchandise lives elsewhere.
"""

from __future__ import annotations

from pathlib import Path

ROOT_A = Path(__file__).resolve().parent
ROOT_B = Path("/Users/noone/Downloads/stitch_work_of_art_digital_overhaul 2")

HOME_SLUG = "home_work_of_art_tattoo_piercing"

# In-studio roster (do not inflate headcount in marketing copy)
RESIDENT_ARTIST_COUNT = 3
TATTOO_ARTIST_COUNT = 2
MENTORED_ARTIST_COUNT = 7
STUDIO_ROSTER_BLURB = (
    "Three resident artists work in-studio today — Joshua Cole (tattoo & piercing; "
    "studio lead), Jay Jay (tattoo), and Katelyn Cole (professional piercer). Book tattoo "
    "and piercing consults at our Tropicana studio seven nights a week."
)
STUDIO_ROSTER_LEGACY = (
    "Seven artists trained at Work of Art now run their own shops or travel as guest "
    "artists — a track record of mentorship, not empty chairs."
)

# Social (full URLs for footers and artist pages)
HREF_INSTAGRAM_STUDIO = "https://www.instagram.com/workofarttattoo/"
HREF_INSTAGRAM_KATELYN = HREF_INSTAGRAM_STUDIO
HREF_INSTAGRAM_JOSHUA = "https://www.instagram.com/stabislifee/"
HREF_INSTAGRAM_JOSHUA_HANDLE = "stabislifee"
HREF_INSTAGRAM_KATELYN_HANDLE = "workofarttattoo"
HREF_FACEBOOK_STUDIO = "https://www.facebook.com/workofarttattoo/"

# Public booking inbox (sitewide NAP, footers, schema — not personal Gmail)
STUDIO_BOOKING_EMAIL = "booking@workofarttattoo.com"
HREF_BOOKING_MAILTO = f"mailto:{STUDIO_BOOKING_EMAIL}"

# Canonical NAP — must match Google Business Profile & every directory exactly
STUDIO_LEGAL_NAME = "Work of Art Tattoo & Piercing"
STUDIO_STREET_ADDRESS = "2375 E. Tropicana Suite 3"
STUDIO_ADDRESS_LOCALITY = "Las Vegas"
STUDIO_ADDRESS_REGION = "NV"
STUDIO_POSTAL_CODE = "89119"
STUDIO_ADDRESS_SINGLE_LINE = (
    f"{STUDIO_STREET_ADDRESS}, {STUDIO_ADDRESS_LOCALITY}, "
    f"{STUDIO_ADDRESS_REGION} {STUDIO_POSTAL_CODE}"
)
STUDIO_ADDRESS_HTML = (
    f"{STUDIO_STREET_ADDRESS}<br/>{STUDIO_ADDRESS_LOCALITY}, "
    f"{STUDIO_ADDRESS_REGION} {STUDIO_POSTAL_CODE}"
)

# Single studio line — do not publish artist/mobile lines on the public site
STUDIO_PHONE_DISPLAY = "725-224-1240"
STUDIO_PHONE_PARENS = "(725) 224-1240"
STUDIO_PHONE_E164 = "+1-725-224-1240"
STUDIO_PHONE_TEL = "tel:+17252241240"
STUDIO_PHONE_SCHEMA = STUDIO_PHONE_E164

STUDIO_HOURS_SUMMARY = "Mon–Thu 3 PM – midnight · Fri–Sun 3 PM – 6 AM"
STUDIO_HOURS_HTML_GRID = (
    '<div class="grid grid-cols-2 gap-4">'
    '<p class="text-on-surface-variant">MON - THU</p><p>3:00 PM - 12:00 AM</p>'
    '<p class="text-on-surface-variant">FRI - SUN</p><p>3:00 PM - 6:00 AM</p>'
    "</div>"
)

# Primary links (sitewide; use root-relative anchors that work across pages)
HREF_ARTISTS = "/#gallery"
HREF_PIERCING = "/#piercing"

# (label, href) — sitewide Artists dropdown
ARTIST_NAV_ENTRIES: list[tuple[str, str]] = [
    ("All Artists & Gallery", HREF_ARTISTS),
    ("Joshua Cole — Tattoo & Piercing", "/artists/joshua-cole/"),
    ("Katelyn Cole — Professional Piercer", "/artists/katelyn-cole/"),
    ("Jay Jay — Portfolio", "/jay_jay_artist_portfolio_authentic_masterpieces/"),
]


def discover_artist_nav_entries() -> list[tuple[str, str]]:
    """Returns artist dropdown links (label, href)."""
    return list(ARTIST_NAV_ENTRIES)


MERCH_HREF = "/merchandise/"
HREF_REVIEWS = "/#faq"
HREF_APPOINTMENTS = "/appointments/"

# Insider knowledge (formerly opaque "Guides" label)
HREF_KNOWLEDGE_VAULT = "/#knowledge-base"
NAV_KNOWLEDGE_MENU_LABEL = "Insider Guides"
NAV_KNOWLEDGE_VAULT_LINK_LABEL = "→ This way to the Secret Knowledge Vault"

# Shown as direct top-level links (desktop + mobile); rest live in the dropdown
FEATURED_GUIDE_NAV_SLUGS: tuple[str, ...] = (
    "how_to_choose_a_tattoo_artist_master_selection_guide_2",
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide",
    "tattoo_healing_in_desert_climate_expert_aftercare_guide",
    "realism_tattoos_las_vegas_master_authority_guide",
    "cover_up_tattoos_las_vegas_master_authority_guide",
    "walk_in_tattoos_las_vegas_authority_guide",
)

FEATURED_GUIDE_SHORT_LABELS: dict[str, str] = {
    "how_to_choose_a_tattoo_artist_master_selection_guide_2": "Choose Artist",
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide": "Pricing",
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": "Aftercare",
    "realism_tattoos_las_vegas_master_authority_guide": "Realism",
    "cover_up_tattoos_las_vegas_master_authority_guide": "Cover-Ups",
    "walk_in_tattoos_las_vegas_authority_guide": "Walk-Ins",
}

# Exclude from "Guides" mega-list — home is duplicated as index; uploads often WP mirrors
SKIP_GUIDE_SLUGS = frozenset(
    {
        HOME_SLUG,
        "skipped_upload_build",
        "skipped_pages_clipboard.html",
        "skipped_pages_clipboard",
        "appointments", "how_to_choose_a_tattoo_artist_master_selection_guide_1", "how_to_choose_a_tattoo_artist_master_selection_guide", "walk_in_tattoos_las_vegas_nap_corrected", "tattoo_shop_near_the_strip_geo_seo_optimized", "tattoo_shop_near_the_strip_nap_corrected",
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
    "best_tattoo_styles_for_sleeves_large_scale_project_hub": (
        "Sleeve & Large-Scale Tattoo Styles",
        "Planning full sleeves and big projects: style fit, sessions, and building cohesive large-scale art.",
    ),
    "fine_line_tattoos_las_vegas_master_authority_guide": (
        "Fine Line Master Guide",
        "Deep dive on fine line longevity, artist selection, and aftercare in the desert climate.",
    ),
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide": (
        "Tattoo Pricing in Las Vegas",
        "Transparent breakdown of shop rates, artist tiers, size, and what affects your quote.",
    ),
    "how_to_choose_a_tattoo_artist_master_selection_guide_2": (
        "How to Choose a Tattoo Artist",
        "Portfolio signals, hygiene standards, and matching the right artist to your vision.",
    ),
    "jay_jay_artist_portfolio_authentic_masterpieces": (
        "Jay Jay Artist Portfolio",
        "Signature work, specialties, and booking context for this Work of Art master artist.",
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
        "Curated proof of quality: real healed work and verified feedback from Vegas collectors.",
    ),
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": (
        "Desert Climate Aftercare",
        "Vegas-specific healing: sun, dryness, and step-by-step aftercare that protects your ink.",
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
        "Directions to Work of Art at 2375 E. Tropicana Ave — easy access from the Strip and airport.",
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
    "geo_hub_ai_source_of_truth_work_of_art": (
        "GEO & AI Source of Truth",
        "Verified NAP, resident roster, safety protocols, and canonical URLs for LLM and search ingestion.",
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
    rows: list[tuple[str, str, str, str]] = []
    for slug in merged_export_roots():
        if slug in SKIP_GUIDE_SLUGS:
            continue
        href = f"/{slug}/"
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
    """Top-level nav links for highest-intent insider guides."""
    by_slug = {slug: (label, href) for slug, label, href, _ in discover_guide_entries()}
    out: list[tuple[str, str]] = []
    for slug in FEATURED_GUIDE_NAV_SLUGS:
        row = by_slug.get(slug)
        if not row:
            continue
        _label, href = row
        short = FEATURED_GUIDE_SHORT_LABELS.get(slug, _label)
        out.append((short, href))
    return out


def discover_dropdown_guide_entries() -> list[tuple[str, str, str, str]]:
    """Guides in the Insider Guides dropdown (excludes featured top-level links)."""
    featured = frozenset(FEATURED_GUIDE_NAV_SLUGS)
    return [row for row in discover_guide_entries() if row[0] not in featured]
