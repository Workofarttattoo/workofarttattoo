#!/usr/bin/env python3
"""Inject topic-cluster internal links into guide pages (semantic content graph)."""

from __future__ import annotations

import re
from pathlib import Path

from woa_nav_config import HOME_SLUG

ROOT = Path(__file__).resolve().parent
MARKER = 'data-woa-topic-cluster="1"'

# slug fragment -> (heading, list of (label, href))
CLUSTERS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "healing": (
        "Aftercare & healing cluster",
        [
            ("Skin Science hub — how skin holds ink", "/skin_science_tattoo_dermatology_authority_guide/"),
            ("Healing Database — day 1 to year 1 encyclopedia", "/healing_database_tattoo_timeline_encyclopedia_las_vegas/"),
            ("Fresh vs healed — real studio photos", "/tattoo_healing_before_after_real_results/"),
            ("Healed tattoo gallery by style", "/healed_tattoo_gallery_las_vegas/"),
            ("Joshua Cole — oil painting & aging", "/joshua_oil_painting_black_grey_tattoo_aging_las_vegas/"),
            ("Desert climate aftercare guide", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
            ("Tattoo pain & placement chart", "/tattoo_pain_chart_placement_sensitivity_guide/"),
            ("How tattoos age over time", "/knowledge/tattoo-aging-and-fading-over-time/"),
            ("Book a healing check-in", "/appointments/"),
        ],
    ),
    "skin_science": (
        "Skin science cluster",
        [
            ("Skin Science hub", "/skin_science_tattoo_dermatology_authority_guide/"),
            ("Tattoo healing — fresh to healed", "/tattoo_healing_before_after_real_results/"),
            ("Desert climate aftercare", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
            ("Why tattoos stay forever", "/why_tattoos_stay_forever_skin_science_las_vegas_authority_guide/"),
            ("Joshua Cole — artist page", "/artists/joshua-cole/"),
            ("Book tattoo consult", "/appointments/"),
        ],
    ),
    "pain": (
        "Placement & comfort cluster",
        [
            ("Desert climate aftercare", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
            ("Realism tattoos guide", "/realism_tattoos_las_vegas_master_authority_guide/"),
            ("Fine line master guide", "/fine_line_tattoos_las_vegas_master_authority_guide/"),
            ("Tattoo pricing in Las Vegas", "/how_much_do_tattoos_cost_in_las_vegas_authority_guide/"),
            ("Book consult", "/appointments/"),
        ],
    ),
    "realism": (
        "Realism & portfolio cluster",
        [
            ("Studio gallery — tattoos & original art", "/studio_gallery/"),
            ("Offsite bookings — VIP events", "/offsite_bookings/"),
            ("Designs to book — custom concepts", "/studio_gallery/#joshua-designs"),
            ("Joshua Cole — realism artist", "/artists/joshua-cole/"),
            ("Cover-up tattoos Las Vegas", "/cover-up-tattoos-las-vegas/"),
            ("Large-scale project planning", "/large_scale_projects_variant_a_authentic_art_rotation/"),
            ("Choose a tattoo artist", "/how_to_choose_a_tattoo_artist_master_selection_guide_2/"),
            ("Verified client reviews", "/reviews_vault_100_verified_masterpieces/"),
        ],
    ),
    "fine_line": (
        "Fine line cluster",
        [
            ("Fine line tattoos in Vegas", "/best_fine_line_tattoos_in_vegas_ultimate_authority_guide/"),
            ("Healing in desert climate", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
            ("Pain & placement chart", "/tattoo_pain_chart_placement_sensitivity_guide/"),
            ("Joshua Cole portfolio", "/artists/joshua-cole/"),
            ("Book appointment", "/appointments/"),
        ],
    ),
    "cover_up": (
        "Cover-up cluster",
        [
            ("Cover-up tattoo guide", "/cover-up-tattoos-las-vegas/"),
            ("Joshua Cole — cover-up consults", "/artists/joshua-cole/"),
            ("Healed cover-up gallery", "/healed_cover_up_tattoos_las_vegas/"),
            ("Realism tattoos guide", "/realism-tattoos-las-vegas/"),
            ("Ask about a cover-up", "/appointments/"),
        ],
    ),
    "piercing": (
        "Piercing knowledge graph",
        [
            ("Complete piercing guide", "/piercing-guide-las-vegas/"),
            ("Ear piercing guide", "/ear_piercing_guide_las_vegas/"),
            ("Katelyn Cole — piercer", "/artists/katelyn-cole/"),
            ("Piercing shop & jewelry standards", "/best_piercing_shop_las_vegas_updated_jewelry_standards/"),
            ("Piercing aftercare", "/piercing_aftercare_guide_las_vegas/"),
            ("Piercing healing timelines", "/piercing_healing_guide_las_vegas/"),
            ("Jewelry guide", "/piercing_jewelry_guide_las_vegas/"),
            ("Helix piercing guide", "/helix-piercing-las-vegas/"),
            ("Book your piercing", "/appointments/"),
        ],
    ),
    "walk_in": (
        "Walk-in & booking cluster",
        [
            ("Flash deals under $100", "/flash_art_deals_under_100/"),
            ("Studio location near the Strip", "/tattoo_shop_near_the_strip_nap_corrected/"),
            ("What to know before you ink", "/vegas_tattoo_shop_vs_cheap_strip_tattoo_what_you_need_to_know/"),
            ("Tattoo pricing guide", "/how_much_do_tattoos_cost_in_las_vegas_authority_guide/"),
            ("Book ahead", "/appointments/"),
        ],
    ),
    "cost": (
        "Pricing & planning cluster",
        [
            ("How to choose a tattoo artist", "/how_to_choose_a_tattoo_artist_master_selection_guide_2/"),
            ("Large-scale project planning", "/large_scale_projects_variant_a_authentic_art_rotation/"),
            ("Realism guide", "/realism_tattoos_las_vegas_master_authority_guide/"),
            ("Walk-in tattoos guide", "/walk_in_tattoos_las_vegas_authority_guide/"),
            ("Request a quote", "/appointments/"),
        ],
    ),
    "strip": (
        "Las Vegas location cluster",
        [
            ("Official hours & location", "/official_location_hours_contact/"),
            ("Directions from the Strip", "/tattoo_shop_near_the_strip_nap_corrected/"),
            ("Walk-in tattoos", "/walk-in-tattoos-las-vegas/"),
            ("Book appointment", "/appointments/"),
        ],
    ),
}

DEFAULT_CLUSTER = (
    "Explore related studio guides",
    [
        ("Artists directory", "/artists/"),
        ("Realism tattoos", "/realism_tattoos_las_vegas_master_authority_guide/"),
        ("Piercing standards", "/best_piercing_shop_las_vegas_updated_jewelry_standards/"),
        ("Aftercare in desert climate", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
        ("Book appointment", "/appointments/"),
    ],
)


def cluster_for_slug(slug: str) -> tuple[str, list[tuple[str, str]]]:
    low = slug.lower()
    if (
        "best_piercing" in low
        or "_piercing_las_vegas" in low
        or low.startswith("piercing")
        or "titanium" in low
        or "ear-curation" in low
        or low.startswith("katelyn_")
        or "katelyn_cole_piercing" in low
        or low.endswith("_piercing_guide_las_vegas")
        or low.endswith("_piercing_las_vegas_authority_guide")
    ):
        return CLUSTERS["piercing"]
    if "skin_science" in low or low.endswith("_skin_science_las_vegas_authority_guide"):
        return CLUSTERS["skin_science"]
    if low.startswith("tattoo-healing") or low.startswith("how-often") or "aftercare" in low or "second-skin" in low or "scabbing" in low or "infection" in low or "healing_database" in low:
        return CLUSTERS["healing"]
    if "cover-up" in low or "cover_up" in low:
        return CLUSTERS["cover_up"]
    if "cost" in low or "tip" in low or "deposit" in low or "walk-in" in low or "consultation" in low or "session" in low:
        return CLUSTERS["cost"]
    if "pain" in low or "ribs" in low or "placement" in low:
        return CLUSTERS["pain"]
    if "realism" in low or "fine-line" in low or "sleeve" in low or "style" in low or "first-tattoo" in low:
        return CLUSTERS["realism"]
    if "strip" in low or "compare" in low or "luxury" in low or "vegas" in low:
        return CLUSTERS["strip"]
    for key, value in CLUSTERS.items():
        if key in low:
            return value
    return DEFAULT_CLUSTER


def block_for_slug(slug: str, html: str) -> str:
    if 'data-woa-guide-hub-bar="1"' in html:
        return ""
    heading, links = cluster_for_slug(slug)
    existing = set(re.findall(r'href="(/[^"#?]*/?)"', html))
    filtered: list[tuple[str, str]] = []
    for label, href in links:
        if href in existing and href != f"/{slug}/":
            continue
        filtered.append((label, href))
    if len(filtered) < 2:
        return ""
    items = "\n".join(
        f'<li><a class="text-secondary underline hover:no-underline" href="{href}">{label}</a></li>'
        for label, href in filtered[:3]
    )
    return f"""
<nav {MARKER} aria-label="Related topics" class="woa-topic-cluster py-10 px-margin-mobile md:px-margin-desktop bg-surface-container border border-outline-variant/20 my-12">
<div class="max-w-4xl mx-auto">
<h2 class="font-headline-md text-on-surface mb-4">{heading}</h2>
<ul class="font-body-md text-on-surface-variant space-y-2 sm:columns-2">{items}</ul>
</div>
</nav>
"""


def inject(html: str, slug: str) -> str:
    if MARKER in html:
        html = re.sub(
            r'<nav[^>]*data-woa-topic-cluster="1"[^>]*>.*?</nav>\s*',
            "",
            html,
            flags=re.DOTALL,
        )
    block = block_for_slug(slug, html)
    if not block.strip():
        return html
    if 'data-woa-internal-links="1"' in html:
        return html.replace(
            f'<nav data-woa-internal-links="1"',
            block + f'\n<nav data-woa-internal-links="1"',
            1,
        )
    if "</main>" in html:
        return html.replace("</main>", block + "\n</main>", 1)
    return html.replace("</body>", block + "\n</body>", 1)


def main() -> int:
    changed = 0
    for path in sorted(ROOT.rglob("code.html")):
        if "skipped" in path.parts or path.parent.name == HOME_SLUG:
            continue
        slug = path.parent.name
        if slug == "knowledge":
            continue
        if path.parent.parent.name == "knowledge":
            slug = path.parent.name
        raw = path.read_text(encoding="utf-8")
        updated = inject(raw, slug)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ok] {slug}")
    print(f"Done: {changed} guide page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
