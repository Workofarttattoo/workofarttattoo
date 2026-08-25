#!/usr/bin/env python3
"""Piercing SEO keywords + conversion copy — traffic intent without keyword stuffing."""

from __future__ import annotations

import html
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from woa_piercing_authority import PiercingGuide

from woa_nav_config import (
    STUDIO_ADDRESS_SINGLE_LINE,
    STUDIO_PHONE_PARENS,
    STUDIO_PHONE_TEL,
    STUDIO_STREET_ADDRESS,
)

BOOK = "/appointments/"
PIERCING_HUB = "/best_piercing_shop_las_vegas_updated_jewelry_standards/"
KATELYN_PAGE = "/artists/katelyn-cole/"
LOCATION_PAGE = "/official_location_hours_contact/"
PHONE_TEL = STUDIO_PHONE_TEL
PHONE_DISPLAY = STUDIO_PHONE_PARENS
STUDIO_LINE = f"Work of Art Tattoo & Piercing · {STUDIO_ADDRESS_SINGLE_LINE}"


def _trim_meta(text: str, limit: int = 155) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return cut + "…"


def piercing_label(name: str) -> str:
    """Display label: 'Helix Piercing', 'Lobe Piercing'."""
    low = name.lower()
    if low.endswith(" piercing") or low.endswith(" piercings"):
        return name
    return f"{name} Piercing"


def piercing_label_lower(name: str) -> str:
    return piercing_label(name).lower()


def page_title(guide: "PiercingGuide") -> str:
    from woa_piercing_complete_guides import complete_page_title

    return complete_page_title(guide)


def meta_description(guide: "PiercingGuide") -> str:
    from woa_expert_voice import katelyn_meta

    return katelyn_meta(guide)


def hub_title() -> str:
    return "Piercing Las Vegas | Complete Guide — Ear, Nose, Body & Book Online"


def hub_meta_description() -> str:
    return _trim_meta(
        "Every piercing placement Katelyn Cole offers at Work of Art — healing timelines, jewelry, "
        f"desert aftercare, and anatomy notes. {STUDIO_STREET_ADDRESS}. {PHONE_DISPLAY}."
    )


def pillar_title(pillar_title: str) -> str:
    base = pillar_title.split(" — ")[0]
    return f"{base} Las Vegas | Piercing Shop Near the Strip"


def pillar_meta(intro_keyword: str) -> str:
    return (
        f"{intro_keyword} in Las Vegas — Work of Art piercing studio on E. Tropicana, "
        f"anatomy-first placement with Katelyn Cole. Book online · {PHONE_DISPLAY}."
    )[:160]


def seo_lead_paragraph(guide: "PiercingGuide") -> str:
    from woa_expert_voice import katelyn_hero

    return katelyn_hero(guide)


def seo_faqs(guide: "PiercingGuide") -> tuple[tuple[str, str], ...]:
    label = piercing_label_lower(guide.name)
    article = "an" if label[:1] in {"a", "e", "i", "o", "u"} else "a"
    existing_q = {q.lower() for q, _ in guide.faqs}
    extras: list[tuple[str, str]] = []

    def add(q: str, a: str) -> None:
        if q.lower() not in existing_q:
            extras.append((q, a))
            existing_q.add(q.lower())

    if guide.offered:
        add(
            f"Where can I get {article} {label} in Las Vegas?",
            f"At Work of Art — {STUDIO_STREET_ADDRESS}. I book by appointment so we can mark anatomy "
            f"and pick starter length before we pierce. Online booking or {PHONE_DISPLAY}.",
        )
        add(
            f"Do I need an appointment for a {label}?",
            f"Yes. I need time to assess angle, swelling room, and jewelry length — same-day openings "
            f"do happen; call {PHONE_DISPLAY} or grab a slot online.",
        )
        add(
            f"How long until a {label} heals?",
            f"{guide.healing_time} Vegas dry air tightens crusties — saline mist, no picking, "
            f"and show up for your downsizing check when I schedule it.",
        )
        add(
            f"Does a {label} hurt?",
            f"Most clients rate this {guide.pain_score}/10 — {guide.pain_label}. "
            f"The poke is quick; sleep position and snagging matter more over the next months.",
        )
        add(
            f"What jewelry do you start with?",
            f"Starter jewelry is sized long enough for normal swelling. "
            f"I downsize at your check-in and wait on decorative upgrades until the piercing is stable.",
        )
    else:
        add(
            f"Does Work of Art offer {label}?",
            f"No — I do not perform {label} here. See our complete piercing guide for placements I do offer "
            f"and book one of those instead.",
        )

    return guide.faqs + tuple(extras)


def conversion_bar(guide: "PiercingGuide", *, compact: bool = False) -> str:
    from woa_expert_voice import katelyn_cta_blurb

    label = piercing_label(guide.name)
    if guide.offered:
        headline = f"Book {label.lower()} with Katelyn"
        sub = katelyn_cta_blurb(guide)
        primary = f"Book {label.lower()}"
    else:
        headline = "Book a piercing I do offer"
        sub = katelyn_cta_blurb(guide)
        primary = "See offered piercings"

    if compact:
        return f"""<div class="flex flex-wrap gap-3 pt-2">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase" href="{BOOK}">{html.escape(primary)}</a>
<a class="inline-flex border border-outline px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase hover:border-secondary" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
</div>"""

    return f"""<aside class="border border-secondary/50 bg-secondary/10 p-6 md:p-8 space-y-4 my-8" data-woa-piercing-cta="1">
<h2 class="font-headline-md text-on-surface text-xl md:text-2xl">{html.escape(headline)}</h2>
<p class="font-body-md text-on-surface-variant">{html.escape(sub)}</p>
<div class="flex flex-col sm:flex-row flex-wrap gap-3">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:bg-secondary-fixed transition-colors" href="{BOOK}">{html.escape(primary)}</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:border-secondary transition-colors" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:border-secondary transition-colors" href="{LOCATION_PAGE}">Directions</a>
</div>
</aside>"""


def sticky_book_label(slug: str) -> str | None:
    """Placement-specific sticky CTA label from page slug."""
    if not slug.endswith("_piercing_las_vegas_authority_guide"):
        return None
    sid = slug[: -len("_piercing_las_vegas_authority_guide")]
    names = {
        "ear_lobe": "Lobe",
        "upper_lobe": "Upper Lobe",
        "forward_helix": "Forward Helix",
        "anti_tragus": "Anti-Tragus",
        "ear_curation": "Ear Curation",
        "high_nostril": "High Nostril",
        "anti_eyebrow": "Anti-Eyebrow",
        "vertical_labret": "Vertical Labret",
        "snake_bites": "Snake Bites",
        "frog_eyes_tongue": "Frog Eyes",
    }
    name = names.get(sid, sid.replace("_", " ").title())
    return f"Book {name} Piercing"


def hub_conversion_block() -> str:
    return f"""<aside class="border border-secondary/50 bg-secondary/10 p-8 space-y-4 text-center my-8">
<h2 class="font-headline-md text-on-surface text-2xl">Ready to book?</h2>
<p class="font-body-md text-on-surface-variant max-w-2xl mx-auto">Ear curation, facial, oral, and body piercings with Katelyn Cole — anatomy-first placement, jewelry-fit planning, and desert aftercare at {STUDIO_STREET_ADDRESS}.</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center pt-2">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest" href="{BOOK}">Book piercing appointment</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:border-secondary" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
</div>
</aside>"""
