#!/usr/bin/env python3
"""Build piercing-type authority hub + per-placement guides (Katelyn Cole voice)."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_content_standards import expert_callout, katelyn_piercing_notes, reviewed_by_block, toc_nav
from woa_entity_schema import ID_KATELYN, guide_article_graph, schema_script
from woa_piercing_authority import (
    BOOK,
    CATEGORY_LABELS,
    HUB_INTRO,
    HUB_SLUG,
    HUB_TITLE,
    KATELYN_PAGE,
    PIERCING_CATALOG as _BASE_CATALOG,
    PIERCING_HUB,
    CategoryId,
    PiercingGuide,
    guide_by_id,
    meta_description,
    page_title,
    slug_for,
)
from woa_piercing_catalog_extra import PIERCING_CATALOG_EXTRA
from woa_expert_entity_blocks import katelyn_entity_block
from woa_piercing_complete_guides import complete_guide_h1, complete_sections_for
from woa_piercing_pillars import ORAL_SLUGS, PILLARS, SKIP_STANDALONE_CLUSTER, pillar_for_slug_id
from woa_piercing_profiles import sections_for
from woa_piercing_seo import (
    PHONE_TEL,
    STUDIO_LINE,
    conversion_bar,
    hub_conversion_block,
    hub_meta_description,
    hub_title,
    seo_faqs,
    seo_lead_paragraph,
)
from woa_piercing_promotions import render_current_piercing_special
from woa_guide_proof_strips import proof_strip_html

PIERCING_CATALOG: tuple[PiercingGuide, ...] = _BASE_CATALOG + PIERCING_CATALOG_EXTRA

DESERT_PIERCING_GUIDE = "/piercing_aftercare_desert_climate_las_vegas_expert_guide/"
HEALED_HUB = "/healed_tattoo_gallery_las_vegas/"
STUDIO_VIDEOS = "/studio_videos/#katelyn-piercing"
KATELYN_TOPICS_HUB = "/katelyn_cole_piercing_authority_hub_las_vegas/"
JEWELRY_PILLAR = "/piercing_jewelry_guide_las_vegas/"
HEALING_PILLAR = "/piercing_healing_guide_las_vegas/"
AFTERCARE_PILLAR = "/piercing_aftercare_guide_las_vegas/"

CATEGORY_PILLAR: dict[CategoryId, tuple[str, str]] = {
    "ear": ("Ear Piercing Guide", "/ear_piercing_guide_las_vegas/"),
    "facial": ("Facial Piercing Guide", "/facial_piercing_guide_las_vegas/"),
    "body": ("Body Piercing Guide", "/body_piercing_guide_las_vegas/"),
    "not_offered": ("Complete Piercing Guide", f"/{HUB_SLUG}/"),
}

# Oral placements link to oral pillar
ORAL_PILLAR = ("Oral Piercing Guide", "/oral_piercing_guide_las_vegas/")


def guides_for(category: CategoryId) -> list[PiercingGuide]:
    return [g for g in PIERCING_CATALOG if g.category == category]

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"
OG_DEFAULT = "/studio_gallery/ear-lobe-piercing-session-da19eec5"


def pain_meter(score: int) -> str:
    if score <= 0:
        return '<p class="font-body-md text-on-surface-variant">Not applicable — service not offered.</p>'
    filled = score
    empty = 10 - score
    blocks = "".join(
        '<span class="inline-block w-3 h-3 bg-secondary"></span>' if i < filled else
        '<span class="inline-block w-3 h-3 bg-outline-variant/40"></span>'
        for i in range(10)
    )
    return f"""<div class="flex items-center gap-3 flex-wrap">
<div class="flex gap-1" aria-hidden="true">{blocks}</div>
<span class="font-headline-md text-on-surface text-xl">{score}<span class="text-on-surface-variant text-base">/10</span></span>
</div>"""


def offered_badge(guide: PiercingGuide) -> str:
    if guide.offered:
        return (
            '<span class="inline-flex items-center gap-2 px-4 py-2 bg-secondary/15 border border-secondary/40 '
            'font-label-caps text-[11px] uppercase tracking-widest text-secondary">'
            "✓ We offer this piercing</span>"
        )
    return (
        '<span class="inline-flex items-center gap-2 px-4 py-2 bg-surface-container-high border '
        'border-outline-variant/50 font-label-caps text-[11px] uppercase tracking-widest text-on-surface-variant">'
        "Not offered at Work of Art</span>"
    )


def list_items(items: tuple[str, ...]) -> str:
    return "".join(f"<li>{html.escape(s)}</li>" for s in items)


def link_list(items: tuple[tuple[str, str], ...]) -> str:
    if not items:
        return ""
    return "".join(
        f'<li><a class="text-secondary underline hover:no-underline" href="{html.escape(href)}">'
        f"{html.escape(label)}</a></li>"
        for label, href in items
    )


def section_block(title: str, items: tuple[str, ...], anchor: str = "") -> str:
    if not items or items == ("N/A",) or items == ("N/A — not performed at Work of Art.",):
        return ""
    aid = f' id="{html.escape(anchor)}"' if anchor else ""
    return f"""<section class="space-y-4"{aid}>
<h2 class="font-headline-md text-on-surface text-2xl">{html.escape(title)}</h2>
<ul class="font-body-md text-on-surface-variant space-y-3 list-disc pl-5">{list_items(items)}</ul>
</section>"""


def prose_section(title: str, text: str, anchor: str) -> str:
    return f"""<section class="space-y-4" id="{html.escape(anchor)}">
<h2 class="font-headline-md text-on-surface text-2xl">{html.escape(title)}</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">{html.escape(text)}</p>
</section>"""


def pillar_breadcrumb(guide: PiercingGuide) -> str:
    pillar = pillar_for_slug_id(guide.slug_id)
    return (
        f'<a class="text-secondary underline" href="/{HUB_SLUG}/">Complete piercing guide</a>'
        f' · <a class="text-secondary underline" href="/{pillar.slug}/">{html.escape(pillar.title.split(" — ")[0])}</a>'
    )


PILLAR_LINKS = "".join(
    f"""<a class="block border border-outline-variant/30 bg-surface-container-high p-5 hover:border-secondary transition-colors" href="/{html.escape(p.slug)}/">
<h3 class="font-headline-md text-on-surface text-base">{html.escape(p.title.split(" — ")[0])}</h3>
<p class="font-body-md text-on-surface-variant text-sm mt-2 line-clamp-2">{html.escape(p.intro[:120])}…</p>
</a>"""
    for p in PILLARS
    if p.slug != HUB_SLUG
)


def encyclopedia_graph_links() -> str:
    return f"""<section class="space-y-4 border border-outline-variant/30 bg-surface-container-low p-6">
<h2 class="font-headline-md text-on-surface text-xl">Explore the piercing knowledge graph</h2>
<p class="font-body-md text-on-surface-variant">Videos, aftercare, healing proof, portfolio, and booking — connected so you can go deep on one topic.</p>
<ul class="font-body-md text-on-surface-variant space-y-2">
<li><a class="text-secondary underline" href="{STUDIO_VIDEOS}">Studio videos — Katelyn piercing</a></li>
<li><a class="text-secondary underline" href="{DESERT_PIERCING_GUIDE}">Desert climate piercing aftercare</a></li>
<li><a class="text-secondary underline" href="{HEALED_HUB}">Healed tattoo gallery (client heal proof)</a></li>
<li><a class="text-secondary underline" href="/studio_gallery/#katelyn-piercing">Piercing portfolio</a></li>
<li><a class="text-secondary underline" href="{KATELYN_PAGE}">Katelyn Cole — artist page</a></li>
<li><a class="text-secondary underline" href="{KATELYN_TOPICS_HUB}">Katelyn's piercing authority topics</a></li>
<li><a class="text-secondary underline" href="{BOOK}">Book a piercing</a></li>
</ul>
</section>"""


def guide_web_section(guide: PiercingGuide) -> str:
    """Pillar + related links — site as a web, not isolated documents."""
    items: list[str] = []
    seen_hrefs: set[str] = set()

    def add(label: str, href: str) -> None:
        if href in seen_hrefs:
            return
        seen_hrefs.add(href)
        items.append(
            f'<li><a class="text-secondary underline hover:no-underline" href="{html.escape(href)}">'
            f"{html.escape(label)}</a></li>"
        )

    add("Complete Piercing Guide", f"/{HUB_SLUG}/")
    if guide.slug_id in ORAL_SLUGS:
        add(*ORAL_PILLAR)
    elif guide.category in CATEGORY_PILLAR:
        add(*CATEGORY_PILLAR[guide.category])
    add("Piercing Jewelry Guide", JEWELRY_PILLAR)
    add("Piercing Healing Guide", HEALING_PILLAR)
    add("Desert Piercing Aftercare", DESERT_PIERCING_GUIDE)
    add("Katelyn Cole — Piercing Authority", KATELYN_TOPICS_HUB)

    for rid in guide.related:
        rel = guide_by_id(rid)
        if rel:
            add(f"{rel.name} piercing guide", f"/{slug_for(rel)}/")

    links = "\n".join(items)
    return f"""<nav aria-label="Related piercing guides" class="border border-outline-variant/30 bg-surface-container-low p-5 space-y-3">
<p class="font-label-caps text-[10px] uppercase tracking-widest text-secondary">Part of this guide</p>
<ul class="font-body-md text-on-surface-variant space-y-2">{links}</ul>
</nav>"""


def related_links(guide: PiercingGuide) -> str:
    """Footer related list — placement neighbors only (pillars are in guide_web_section)."""
    links: list[str] = []
    for rid in guide.related:
        rel = guide_by_id(rid)
        if not rel:
            continue
        links.append(
            f'<li><a class="text-secondary underline hover:no-underline" href="/{slug_for(rel)}/">'
            f"{html.escape(rel.name)} piercing guide</a></li>"
        )
    if not links:
        links.append(
            f'<li><a class="text-secondary underline hover:no-underline" href="/{HUB_SLUG}/">'
            "Browse all piercing guides</a></li>"
        )
    return "\n".join(links)


def guide_card(guide: PiercingGuide) -> str:
    status = "Offered" if guide.offered else "Not offered"
    pain = f"Pain {guide.pain_score}/10" if guide.pain_score else "N/A"
    return f"""<a class="block border border-outline-variant/30 bg-surface-container-high p-6 hover:border-secondary transition-colors group" href="/{slug_for(guide)}/">
<div class="flex justify-between items-start gap-4">
<h3 class="font-headline-md text-on-surface text-lg group-hover:text-secondary transition-colors">{html.escape(guide.name)}</h3>
<span class="font-label-caps text-[10px] uppercase tracking-widest text-on-surface-variant shrink-0">{status}</span>
</div>
<p class="font-body-md text-on-surface-variant mt-2 text-sm">{html.escape(guide.healing_time.split(";")[0])} · {pain}</p>
<p class="font-body-md text-on-surface-variant mt-3 line-clamp-2">{html.escape(guide.intro[:140])}…</p>
<span class="inline-block mt-4 font-label-caps text-[11px] uppercase tracking-widest text-secondary">Read guide →</span>
</a>"""


def hub_main() -> str:
    sections: list[str] = []
    category_blocks = (
        ("ear", "ear", None),
        ("facial", "facial", ORAL_SLUGS),
        ("oral", None, ORAL_SLUGS),
        ("body", "body", None),
        ("not_offered", "not_offered", None),
    )
    for label_key, cat, slug_filter in category_blocks:
        if cat:
            items = [g for g in guides_for(cat) if g.slug_id not in SKIP_STANDALONE_CLUSTER]
            if slug_filter is not None and label_key == "facial":
                items = [g for g in items if g.slug_id not in slug_filter]
        else:
            items = [
                g
                for g in PIERCING_CATALOG
                if g.slug_id in slug_filter and g.slug_id not in SKIP_STANDALONE_CLUSTER
            ]
        if not items:
            continue
        heading = {
            "ear": CATEGORY_LABELS["ear"],
            "facial": CATEGORY_LABELS["facial"],
            "oral": "Oral piercings",
            "body": CATEGORY_LABELS["body"],
            "not_offered": CATEGORY_LABELS["not_offered"],
        }[label_key]
        cards = "\n".join(guide_card(g) for g in items)
        sections.append(
            f"""<div class="space-y-6">
<h2 class="font-headline-md text-on-surface text-2xl">{html.escape(heading)}</h2>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
{cards}
</div>
</div>"""
        )
    grid = "\n\n".join(sections)
    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-4xl space-y-6">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Piercing knowledge base · Katelyn Cole</span>
<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">{html.escape(hub_title())}</h1>
{reviewed_by_block(expert="katelyn")}
<p class="font-body-lg text-on-surface-variant max-w-2xl">{html.escape(HUB_INTRO)}</p>
<p class="font-body-md text-on-surface-variant">Quality over quantity — one definitive page per topic. Same structure on every guide so you know what to expect.</p>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-6xl mx-auto space-y-8">
<h2 class="font-headline-md text-on-surface text-2xl">Pillar guides</h2>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
{PILLAR_LINKS}
</div>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-6xl mx-auto space-y-14">
<h2 class="font-headline-md text-on-surface text-2xl">Every placement — definitive guides</h2>
{grid}
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low text-center">
{hub_conversion_block()}
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background text-center">
<div class="max-w-2xl mx-auto space-y-6">
<h2 class="font-headline-md text-on-surface">Ready to book?</h2>
<p class="font-body-md text-on-surface-variant">Ear curation consults and single piercings — anatomy-first placement, starter jewelry sized for swelling, and follow-up planning on Tropicana.</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest" href="{BOOK}">Book piercing</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:border-secondary transition-colors" href="{PIERCING_HUB}">Jewelry standards</a>
</div>
</div>
</section>
</main>"""


def type_main(guide: PiercingGuide) -> str:
    h1 = complete_guide_h1(guide)
    if guide.slug_id == "helix":
        h1 = "Helix Piercing in Las Vegas"
    title = page_title(guide)
    sec = complete_sections_for(guide.slug_id, guide.name)
    breadcrumb = pillar_breadcrumb(guide)
    all_faqs = seo_faqs(guide)

    tip_quote = guide.tips[0] if guide.tips else (
        sec.katelyn_recommendations[0] if sec.katelyn_recommendations else guide.intro
    )
    expert_box = expert_callout(guide.name, tip_quote, expert="katelyn")
    katelyn_notes = katelyn_piercing_notes(
        guide.tips,
        sec.katelyn_recommendations,
        placement=guide.name,
    )
    seo_lead = seo_lead_paragraph(guide)
    cta_top = conversion_bar(guide)
    cta_mid = conversion_bar(guide, compact=True)
    helix_fast_start = ""
    if guide.slug_id == "helix":
        helix_fast_start = f"""<div class="border border-outline-variant/30 bg-surface-container-low p-5 space-y-4">
<p class="font-label-caps text-secondary uppercase tracking-[0.2em] text-[10px]">Helix quick start</p>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 font-body-md text-sm text-on-surface-variant">
<p><strong class="text-on-surface">Healing:</strong> {html.escape(guide.healing_time)}</p>
<p><strong class="text-on-surface">Starter jewelry:</strong> sized for normal swelling</p>
<p><strong class="text-on-surface">Anatomy:</strong> outer-rim angle and spacing matter</p>
<p><strong class="text-on-surface">Downsizing:</strong> usually discussed at the check-in</p>
<p><strong class="text-on-surface">Location:</strong> {html.escape(STUDIO_LINE)}</p>
</div>
<div class="flex flex-col sm:flex-row gap-3">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase justify-center" href="{BOOK}" data-woa-piercing-booking-start="1">Book helix</a>
<a class="inline-flex border border-outline px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase justify-center hover:border-secondary" href="{PHONE_TEL.replace('tel:', 'sms:')}" data-woa-piercing-text-click="1">Text for today</a>
<a class="inline-flex border border-outline px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase justify-center hover:border-secondary" href="/studio_gallery/#katelyn-piercing" data-woa-katelyn-profile-click="1">See helix work</a>
</div>
<img alt="Helix and curated ear piercing work by Katelyn Cole at Work of Art Las Vegas" class="aspect-[16/10] w-full object-cover border border-outline-variant/30" decoding="async" loading="lazy" src="/studio_gallery/curated-helix-tragus-lobe-piercings-88475d3e.webp"/>
</div>
{render_current_piercing_special(variant="compact", context="helix-top")}"""

    toc = toc_nav(
        (
            ("Anatomy", "anatomy"),
            ("Who is not a candidate", "not-a-candidate"),
            ("Pain level", "pain-level"),
            ("Healing timeline", "healing-time"),
            ("Jewelry sizing", "jewelry-sizing"),
            ("Downsizing", "downsizing"),
            ("Swelling", "swelling"),
            ("Sleeping", "sleeping"),
            ("Exercise", "exercise"),
            ("Headphones", "headphones"),
            ("Helmets", "helmets"),
            ("Migration", "migration"),
            ("Rejection", "rejection"),
            ("Keloids vs bumps", "keloids-bumps"),
            ("Desert climate", "desert-climate"),
            ("Katelyn's notes", "katelyn-notes"),
            ("Cleaning", "cleaning"),
            ("Swimming", "swimming"),
            ("FAQ", "faq"),
            ("Photos", "photos"),
            ("Videos", "videos"),
            ("Book", "book"),
        )
    )

    pain_section = f"""<section class="space-y-4" id="pain-level">
<h2 class="font-headline-md text-on-surface text-2xl">Pain level</h2>
{pain_meter(guide.pain_score)}
<p class="font-body-md text-on-surface-variant">{html.escape(guide.pain_label)}</p>
</section>"""

    healing_section = f"""<section class="space-y-4" id="healing-time">
<h2 class="font-headline-md text-on-surface text-2xl">Healing timeline</h2>
<p class="font-body-md text-on-surface-variant">{html.escape(guide.healing_time)}</p>
<p class="font-body-md text-on-surface-variant text-sm">{html.escape(guide.aftercare_summary)}</p>
</section>"""

    swelling_section = section_block(
        "Swelling expectations",
        sec.swelling_expectations or sec.swelling,
        "swelling",
    )

    faq_block = ""
    if all_faqs:
        rows = "".join(
            f"""<details class="border border-outline-variant/30 bg-surface-container-high p-5 group">
<summary class="font-headline-md text-on-surface cursor-pointer list-none flex justify-between items-center gap-4">
<span>{html.escape(q)}</span>
<span class="text-secondary font-label-caps text-xs">+</span>
</summary>
<p class="font-body-md text-on-surface-variant mt-4">{html.escape(a)}</p>
</details>"""
            for q, a in all_faqs
        )
        faq_block = f"""<section class="space-y-4" id="faq">
<h2 class="font-headline-md text-on-surface text-2xl">Questions clients ask</h2>
{rows}
</section>"""

    photos_block = proof_strip_html(slug_for(guide)) or ""
    if not photos_block and sec.photo_links:
        photos_block = f"""<section class="space-y-4" id="photos">
<h2 class="font-headline-md text-on-surface text-2xl">Photos</h2>
<ul class="font-body-md text-on-surface-variant space-y-2">{link_list(sec.photo_links)}</ul>
</section>"""

    videos_block = ""
    if sec.video_links:
        videos_block = f"""<section class="space-y-4" id="videos">
<h2 class="font-headline-md text-on-surface text-2xl">Videos</h2>
<ul class="font-body-md text-on-surface-variant space-y-2">{link_list(sec.video_links)}</ul>
</section>"""

    book_section = ""
    if guide.offered:
        book_section = f"""<section class="space-y-4 pt-4" id="book">
<h2 class="font-headline-md text-on-surface text-2xl">Book appointment</h2>
<p class="font-body-md text-on-surface-variant">{html.escape(guide.offer_note)}</p>
<div class="flex flex-col sm:flex-row gap-4 pt-2">
<a class="inline-flex bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest justify-center" href="{BOOK}" data-woa-piercing-booking-start="1">Book {html.escape(guide.name.lower())}</a>
<a class="inline-flex border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:border-secondary transition-colors justify-center" href="{KATELYN_PAGE}" data-woa-katelyn-profile-click="1">Katelyn's portfolio</a>
</div>
</section>"""
    else:
        book_section = f"""<section class="space-y-4 pt-4" id="book">
<h2 class="font-headline-md text-on-surface text-2xl">Book a piercing we offer</h2>
<p class="font-body-md text-on-surface-variant">{html.escape(guide.offer_note)}</p>
<div class="flex flex-col sm:flex-row gap-4 pt-2">
<a class="inline-flex bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest justify-center" href="/{HUB_SLUG}/">Browse offered piercings</a>
<a class="inline-flex border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:border-secondary transition-colors justify-center" href="{BOOK}" data-woa-piercing-booking-start="1">Book appointment</a>
</div>
</section>"""

    quirks_block = section_block("Placement quirks", guide.quirks) if guide.quirks else ""

    body_sections = "\n".join(
        s
        for s in (
            section_block("Anatomy requirements", sec.anatomy_requirements, "anatomy"),
            section_block("Who is NOT a candidate", sec.who_should_avoid, "not-a-candidate"),
            section_block("Who it's good for", sec.who_its_good_for, "who-its-good-for"),
            pain_section,
            healing_section,
            cta_top,
            section_block("Jewelry sizing", sec.jewelry_sizing or ((guide.jewelry_notes,) if guide.jewelry_notes else ()), "jewelry-sizing"),
            section_block("Downsizing", sec.downsizing, "downsizing"),
            swelling_section,
            section_block("Sleeping", sec.sleeping, "sleeping"),
            section_block("Exercise", sec.exercise, "exercise"),
            section_block("Headphones", sec.headphones, "headphones"),
            section_block("Helmets", sec.helmets, "helmets"),
            section_block("Migration", sec.migration, "migration"),
            section_block("Rejection", sec.rejection, "rejection"),
            section_block("Keloids vs irritation bumps", sec.keloids_vs_bumps, "keloids-bumps"),
            section_block("Desert climate — Las Vegas", sec.desert_healing, "desert-climate"),
            katelyn_notes,
            section_block("Cleaning", sec.cleaning, "cleaning"),
            section_block("Swimming", sec.swimming, "swimming"),
            section_block("Common mistakes", sec.common_mistakes),
            section_block("When to contact your piercer", sec.when_to_call, "when-to-call"),
            quirks_block,
            faq_block,
            photos_block,
            videos_block,
            book_section,
            encyclopedia_graph_links(),
        )
        if s
    )

    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-6">
<p class="font-body-md text-on-surface-variant">{breadcrumb}</p>
{guide_web_section(guide)}
{reviewed_by_block(expert="katelyn")}
{katelyn_entity_block()}
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">From Katelyn Cole</span>
<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">{html.escape(h1)}</h1>
{offered_badge(guide)}
<p class="font-body-lg text-on-surface-variant leading-relaxed">{html.escape(seo_lead)}</p>
{helix_fast_start}
{toc}
{expert_box}
{cta_mid}
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-12">
{body_sections}
<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Related piercing guides</h2>
<ul class="font-body-md text-on-surface-variant space-y-2">{related_links(guide)}</ul>
<p class="font-body-md text-on-surface-variant text-sm pt-2"><a class="text-secondary underline" href="{BOOK}">Book a piercing</a> · <a class="text-secondary underline" href="{KATELYN_PAGE}">Katelyn's portfolio</a></p>
</section>
</div>
</section>
</main>"""


def patch_meta(page_html: str, slug: str, title: str, description: str, og_path: str) -> str:
    canon = f"{SITE}/{slug}/"
    page_html = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} | Work of Art</title>", page_html, count=1)
    page_html = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{html.escape(description)}" name="description"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<link href="https://www.workofarttattoo.com/[^"]*" rel="canonical"/>',
        f'<link href="{canon}" rel="canonical"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="https://www.workofarttattoo.com/tattoo_healing[^"]*" property="og:url"/>',
        f'<meta content="{canon}" property="og:url"/>',
        page_html,
        count=1,
    )
    og_img = f"{SITE}{og_path}.webp"
    page_html = re.sub(
        r'<meta content="https://www.workofarttattoo.com/how_much[^"]*" property="og:image"/>',
        f'<meta content="{og_img}" property="og:image"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="Tattoo &amp; Piercing Aftercare in Desert Climate \| Work of Art" property="og:title"/>',
        f'<meta content="{html.escape(title)} | Work of Art" property="og:title"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="Vegas-specific healing:[^"]*" property="og:description"/>',
        f'<meta content="{html.escape(description)}" property="og:description"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="https://www.workofarttattoo.com/how_much[^"]*" name="twitter:image"/>',
        f'<meta content="{og_img}" name="twitter:image"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="Tattoo &amp; Piercing Aftercare in Desert Climate \| Work of Art" name="twitter:title"/>',
        f'<meta content="{html.escape(title)} | Work of Art" name="twitter:title"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="Vegas-specific healing:[^"]*" name="twitter:description"/>',
        f'<meta content="{html.escape(description)}" name="twitter:description"/>',
        page_html,
        count=1,
    )
    return page_html


def patch_main(page_html: str, main: str) -> str:
    return re.sub(
        r'<main class="relative pt-20">.*?</main>',
        main.strip(),
        page_html,
        count=1,
        flags=re.DOTALL,
    )


def inject_schema(
    page_html: str,
    slug: str,
    title: str,
    description: str,
    guide: PiercingGuide | None = None,
) -> str:
    page_html = re.sub(
        r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*',
        "",
        page_html,
        flags=re.DOTALL,
    )
    faqs = list(seo_faqs(guide)) if guide else None
    graph = guide_article_graph(
        slug=slug,
        title=title,
        description=description,
        author_id=ID_KATELYN,
        faqs=faqs,
    )
    return page_html.replace("</head>", schema_script(graph) + "\n</head>", 1)


def write_page(
    slug: str,
    main: str,
    title: str,
    description: str,
    og_path: str,
    guide: PiercingGuide | None = None,
) -> None:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    out_dir = ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    page = TEMPLATE.read_text(encoding="utf-8")
    page = patch_meta(page, slug, title, description, og_path)
    page = patch_main(page, main)
    page = inject_schema(page, slug, title, description, guide)
    (out_dir / "code.html").write_text(page, encoding="utf-8")
    print(f"[ok] {slug}/code.html")


def main() -> int:
    hub_desc = hub_meta_description()
    write_page(HUB_SLUG, hub_main(), hub_title(), hub_desc, OG_DEFAULT)

    for guide in PIERCING_CATALOG:
        if guide.slug_id in SKIP_STANDALONE_CLUSTER:
            continue
        slug = slug_for(guide)
        title = page_title(guide)
        desc = meta_description(guide)
        write_page(slug, type_main(guide), title, desc, OG_DEFAULT, guide)

    print(f"Done: hub + {len(PIERCING_CATALOG) - len(SKIP_STANDALONE_CLUSTER)} cluster guide(s) ({len(SKIP_STANDALONE_CLUSTER)} thin overviews merged into pillars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
