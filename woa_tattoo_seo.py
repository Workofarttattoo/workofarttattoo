#!/usr/bin/env python3
"""Tattoo SEO keywords + conversion copy — Joshua Cole voice, book-appointment intent."""

from __future__ import annotations

import html
from dataclasses import dataclass

from woa_nav_config import (
    STUDIO_ADDRESS_SINGLE_LINE,
    STUDIO_PHONE_PARENS,
    STUDIO_PHONE_TEL,
    STUDIO_STREET_ADDRESS,
)

BOOK = "/appointments/"
JOSHUA_PAGE = "/artists/joshua-cole/"
LOCATION_PAGE = "/tattoo_shop_near_the_strip_nap_corrected/"
REALISM_GUIDE = "/realism_tattoos_las_vegas_master_authority_guide/"
DESERT_AFTERCARE = "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"
PHONE_TEL = STUDIO_PHONE_TEL
PHONE_DISPLAY = STUDIO_PHONE_PARENS
STUDIO_LINE = f"Work of Art Tattoo & Piercing · {STUDIO_ADDRESS_SINGLE_LINE}"


def _trim_meta(text: str, limit: int = 155) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return cut + "…"


@dataclass(frozen=True)
class TattooGuideSEO:
    slug: str
    keyword: str  # primary phrase: "realism tattoo"
    style_label: str  # display: "Black & Grey Realism"
    joshua_note: str
    hero_lead: str  # first-person opening — only used when page lacks one
    book_primary: str
    book_headline: str
    extra_keywords: tuple[str, ...] = ()


def _lead(keyword: str, style: str, *, book_verb: str = "book a consult") -> str:
    return (
        f"I run {style.lower()} at Work of Art on {STUDIO_STREET_ADDRESS} — consult-first, "
        f"healed photos, desert aftercare coaching. {book_verb.capitalize()} online or call {PHONE_DISPLAY}."
    )


def _location_answer(style: str = "") -> str:
    tail = f" Joshua Cole specializes in {style.lower()}." if style else ""
    return (
        f"Work of Art Tattoo & Piercing at {STUDIO_STREET_ADDRESS} — minutes from the Strip.{tail} "
        f"Book at workofarttattoo.com/appointments/ or call {PHONE_DISPLAY}."
    )


def _service_faqs(keyword: str, style: str) -> tuple[tuple[str, str], ...]:
    return (
        (
            f"Where can I get a {keyword} in Las Vegas?",
            _location_answer(style),
        ),
        (
            f"How much does a {keyword} cost in Las Vegas?",
            f"{style} pricing depends on size, placement, and session count. Work of Art quotes after a consult — "
            f"transparent pricing before you sit in the chair. See our tattoo pricing guide for ranges.",
        ),
        (
            f"How do I book a {keyword} appointment?",
            f"Book online at workofarttattoo.com/appointments/ or call {PHONE_DISPLAY}. "
            f"Custom {keyword} work starts with a consult and healed-photo goals, not a walk-in flash sheet.",
        ),
        (
            "Is Work of Art near the Las Vegas Strip?",
            f"Yes — {STUDIO_STREET_ADDRESS}, roughly 10 minutes from major Strip resorts in light traffic. "
            f"Private parking, licensed studio, desert-climate aftercare coaching included.",
        ),
        (
            f"Who should I see for {keyword} at Work of Art?",
            (
                "For fine line, fineline floral work, script, custom drawings by commission, and high-detail "
                "smaller tattoos, see Teralyn at /artists/teralyn/. For larger custom realism, blackwork, "
                "sleeves, and cover-ups, see Joshua Cole at /artists/joshua-cole/."
                if "fine line" in keyword.lower()
                else f"Joshua Cole leads {style.lower()} at Work of Art — oil-painting background, "
                f"black & grey realism, sleeves, cover-ups, and seminar-trained resident artists. "
                f"Portfolio at /artists/joshua-cole/."
            ),
        ),
    )


def _aftercare_faqs() -> tuple[tuple[str, str], ...]:
    return (
        (
            "Do you give aftercare instructions after my tattoo?",
            f"Yes — Joshua walks you through wash, moisture, sun, and gym rules before you leave. "
            f"Vegas dry heat changes healing; we coach for desert climate, not a generic aftercare card.",
        ),
        (
            "How does desert heat affect tattoo healing in Las Vegas?",
            "Low humidity pulls moisture from fresh skin faster than coastal clients expect. "
            "We emphasize short showers, thin aftercare layers, sun avoidance, and no pools until the skin closes.",
        ),
        (
            "When can I swim or tan after a tattoo in Vegas?",
            "No pools, hot tubs, or direct sun until the outer layer has fully closed — usually several weeks, "
            "longer for large pieces. Joshua gives placement-specific timing at your session.",
        ),
        (
            "Where is Work of Art Tattoo & Piercing?",
            f"{STUDIO_ADDRESS_SINGLE_LINE}. Private parking, licensed studio, about 10 minutes from the Strip. "
            f"Directions and hours on our location page.",
        ),
        (
            "How do I book my tattoo session?",
            f"Book online at workofarttattoo.com/appointments/ or call {PHONE_DISPLAY}. "
            f"Bring reference photos and questions — we plan for healed results in Vegas sun.",
        ),
    )


def _pricing_faqs() -> tuple[tuple[str, str], ...]:
    return (
        (
            "How much do tattoos cost at Work of Art?",
            "We quote by project after a consult — size, detail, placement, and session count. "
            "No surprise day-of pricing; cheap Strip shops often skip consult and aftercare, and that shows up later.",
        ),
        (
            "Do you charge a shop minimum?",
            "Small pieces have a studio minimum that covers setup, sterile supplies, and artist time. "
            "Teralyn's fineline floral work, script, custom drawings by commission, and high-detail "
            "smaller tattoos are quoted by size, placement, and detail — book a consult for a real quote.",
        ),
        (
            "Where is the studio?",
            _location_answer(),
        ),
        (
            "How do I get an accurate quote before booking?",
            f"Book a consult online or call {PHONE_DISPLAY}. Bring reference photos, placement ideas, "
            f"and any artist notes. Joshua quotes color realistic imagery, blackwork, sleeves, and cover-ups "
            f"by healed goals; Teralyn quotes fineline floral work, script, detailed small tattoos, "
            f"and custom drawings by commission by size and detail.",
        ),
        (
            "Is Work of Art near the Las Vegas Strip?",
            f"Yes — {STUDIO_STREET_ADDRESS}, roughly 10 minutes from major Strip resorts in light traffic with private parking.",
        ),
    )


def _walk_in_faqs() -> tuple[tuple[str, str], ...]:
    return (
        (
            "Do you take walk-in tattoos in Las Vegas?",
            "Sometimes — palm-size flash and simple designs when the schedule allows. "
            "Large realism, cover-ups, and sleeves need a consult; we would rather say no than rush a permanent mistake.",
        ),
        (
            "What tattoo sizes work as walk-ins?",
            "Small flash, simple script, fineline floral pieces, and designs that fit a single session block. "
            "Teralyn is a strong fit for script, detailed smaller tattoos, and custom drawings by commission; "
            "anything larger or multi-session should be booked ahead.",
        ),
        (
            "Where is Work of Art Tattoo & Piercing?",
            _location_answer("Walk-In & Same-Day Tattoos"),
        ),
        (
            "How do I check same-day availability?",
            f"Call {PHONE_DISPLAY} before you drive over — walk-in slots depend on artist chairs that day. "
            f"You can also book online for the next open session.",
        ),
        (
            "Is Work of Art near the Las Vegas Strip?",
            f"Yes — {STUDIO_STREET_ADDRESS}, roughly 10 minutes from major Strip resorts in light traffic.",
        ),
    )


def _choose_artist_faqs() -> tuple[tuple[str, str], ...]:
    return (
        (
            "How do I choose a tattoo artist in Las Vegas?",
            "Start with healed photos in your style, not fresh Instagram shots. "
            "Ask about consult process, licensing, and how they plan for Vegas sun on your placement.",
        ),
        (
            "What should I look for in a portfolio?",
            "Healed work at 6–12 months, consistent line weight or value range in your style, "
            "and pieces similar to what you want — not unrelated award shots.",
        ),
        (
            "Who are the tattoo artists at Work of Art?",
            f"Joshua Cole leads tattoo and piercing at {STUDIO_STREET_ADDRESS} — black & grey realism, "
            f"color realistic imagery, blackwork, sleeves, cover-ups, and artist training. Teralyn handles "
            f"fineline floral work, script, custom drawings by commission, and high-detail smaller tattoos. "
            f"See /artists/joshua-cole/ and /artists/teralyn/.",
        ),
        (
            "Where is Work of Art Tattoo & Piercing?",
            _location_answer(),
        ),
        (
            "How do I book a consult?",
            f"Book online at workofarttattoo.com/appointments/ or call {PHONE_DISPLAY}. "
            f"Bring references, placement ideas, and questions about healing in the desert.",
        ),
    )


def _sleeve_faqs() -> tuple[tuple[str, str], ...]:
    return (
        (
            "How many sessions does a sleeve tattoo take?",
            "A full realism sleeve is usually multiple sessions over months or years — we map flow, "
            "negative space, and session order so the arm reads as one piece.",
        ),
        (
            "How do I plan a sleeve at Work of Art?",
            f"Book a sleeve consult with Joshua Cole online or call {PHONE_DISPLAY}. "
            f"Bring reference photos and be honest about budget and timeline.",
        ),
        (
            "Where can I get a sleeve tattoo in Las Vegas?",
            _location_answer("Sleeve & Large-Scale Tattoos"),
        ),
        (
            "What styles work best for large arm pieces?",
            "Black & grey realism, illustrative blackwork, and cohesive traditional flow — "
            "styles that age with clear contrast in Vegas sun.",
        ),
        (
            "Is Work of Art near the Las Vegas Strip?",
            f"Yes — {STUDIO_STREET_ADDRESS}, roughly 10 minutes from major Strip resorts in light traffic.",
        ),
    )


TATTOO_GUIDES: dict[str, TattooGuideSEO] = {
    "realism_tattoos_las_vegas_master_authority_guide": TattooGuideSEO(
        slug="realism_tattoos_las_vegas_master_authority_guide",
        keyword="realism tattoo",
        style_label="Black & Grey Realism",
        joshua_note=(
            "One thing I always watch for with black & grey sleeves is value range — without deep blacks "
            "and real skin left for highlights, realism turns muddy in Vegas sun within a few years."
        ),
        hero_lead=(
            "Black and grey realism is how I spend most of my chair time — portraits, wildlife, sleeves, "
            "and cover-ups planned for how skin ages in Vegas sun. Every project starts with a consult "
            "and healed-photo goals, not a flash sheet."
        ),
        book_primary="Book realism consult",
        book_headline="Book Black & Grey Realism in Las Vegas",
        extra_keywords=("portrait tattoo", "black and grey tattoo", "color realism tattoo"),
    ),
    "fine_line_tattoos_las_vegas_master_authority_guide": TattooGuideSEO(
        slug="fine_line_tattoos_las_vegas_master_authority_guide",
        keyword="fine line tattoo",
        style_label="Fine Line Tattoos",
        joshua_note=(
            "Fine line work fails when an artist chases hair-thin lines without planning for how skin "
            "spreads during heal — I design for how it looks at six months, not just day one."
        ),
        hero_lead=(
            "Fine line is not about the thinnest needle on day zero — it is about spacing, depth, and "
            "aftercare in dry heat so the piece still reads a year later."
        ),
        book_primary="Book fine line consult",
        book_headline="Book Fine Line Tattoo in Las Vegas",
        extra_keywords=("single needle tattoo", "delicate tattoo", "micro tattoo"),
    ),
    "best_fine_line_tattoos_in_vegas_ultimate_authority_guide": TattooGuideSEO(
        slug="best_fine_line_tattoos_in_vegas_ultimate_authority_guide",
        keyword="fine line tattoo",
        style_label="Fine Line Tattoos in Vegas",
        joshua_note=(
            "The best fine line tattoos in Vegas are the ones still readable a year later — "
            "needle weight, spacing, and aftercare in dry heat matter more than Instagram day-zero photos."
        ),
        hero_lead=(
            "When people ask me about fine line in Vegas, I show healed work at six and twelve months — "
            "that is the only timeline that matters in this climate."
        ),
        book_primary="Book fine line tattoo",
        book_headline="Best Fine Line Tattoos Las Vegas — Book Online",
        extra_keywords=("best fine line tattoo vegas", "fine line tattoo shop"),
    ),
    "cover_up_tattoos_las_vegas_master_authority_guide": TattooGuideSEO(
        slug="cover_up_tattoos_las_vegas_master_authority_guide",
        keyword="cover up tattoo",
        style_label="Tattoo Cover-Ups",
        joshua_note=(
            "Cover-ups fail when someone promises a dark rectangle over old ink — I redesign the composition "
            "so the new piece owns the space and heals as one story, not a patch."
        ),
        hero_lead=(
            "Cover-ups are redesign projects — I need photos of the old work, your skin tone, and honest "
            "time for multiple sessions. A consult beats a same-day guess every time."
        ),
        book_primary="Book cover-up consult",
        book_headline="Cover Up Tattoo Las Vegas — Free Consult",
        extra_keywords=("tattoo cover up artist", "scar cover tattoo", "laser cover up tattoo"),
    ),
    "walk_in_tattoos_las_vegas_authority_guide": TattooGuideSEO(
        slug="walk_in_tattoos_las_vegas_authority_guide",
        keyword="walk in tattoo",
        style_label="Walk-In & Same-Day Tattoos",
        joshua_note=(
            "Walk-ins work when the piece fits the day — palm-size flash and simple designs. "
            "Large realism or cover-ups need a consult; I would rather say no than rush a permanent mistake."
        ),
        hero_lead=(
            "Walk-ins happen when the schedule allows — small flash and simple pieces. "
            "Call before you drive over; large work always starts with a consult."
        ),
        book_primary="Check walk-in availability",
        book_headline="Walk-In Tattoos Las Vegas — Call or Book",
        extra_keywords=("tattoo shop near me", "same day tattoo las vegas", "walk in tattoo shop"),
    ),
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide": TattooGuideSEO(
        slug="how_much_do_tattoos_cost_in_las_vegas_authority_guide",
        keyword="tattoo cost",
        style_label="Tattoo Pricing",
        joshua_note=(
            "I quote by project, not by surprise — size, detail, placement, and how many sessions "
            "a sleeve or cover-up needs. Cheap Strip pricing often skips consult and aftercare; that cost shows up later."
        ),
        hero_lead=(
            "Tattoo pricing here is a consult conversation — size, detail, sessions, and placement. "
            "We would rather give you a real number after we talk than a menu board that lies."
        ),
        book_primary="Book consult for quote",
        book_headline="Tattoo Pricing Las Vegas — Get a Real Quote",
        extra_keywords=("how much do tattoos cost", "tattoo prices las vegas", "tattoo shop prices"),
    ),
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": TattooGuideSEO(
        slug="tattoo_healing_in_desert_climate_expert_aftercare_guide",
        keyword="tattoo aftercare",
        style_label="Desert Tattoo Healing",
        joshua_note=(
            "Vegas dries fresh tattoos faster than coastal clients expect — I coach sun, pool, and gym rules "
            "before you leave because desert heal is different from generic aftercare cards."
        ),
        hero_lead=(
            "Desert aftercare is different — low humidity, brutal sun, and tourists who want pools on day three. "
            "This is what I tell every client before they leave the chair."
        ),
        book_primary="Book tattoo appointment",
        book_headline="Tattoo Aftercare Las Vegas — Then Book Your Session",
        extra_keywords=("tattoo healing las vegas", "tattoo healing desert climate", "tattoo sun protection"),
    ),
    "best_tattoo_styles_for_sleeves_large_scale_project_hub": TattooGuideSEO(
        slug="best_tattoo_styles_for_sleeves_large_scale_project_hub",
        keyword="sleeve tattoo",
        style_label="Sleeve & Large-Scale Tattoos",
        joshua_note=(
            "A realism sleeve is a multi-year collaboration — we map flow, negative space, and session order "
            "so the arm reads as one piece, not a stack of random photos."
        ),
        hero_lead=(
            "Sleeves and large-scale work are mapped over months — flow, negative space, and session order "
            "so the arm or back reads as one composition, not a collage."
        ),
        book_primary="Book sleeve consult",
        book_headline="Sleeve Tattoo Las Vegas — Plan Your Project",
        extra_keywords=("full sleeve tattoo", "half sleeve tattoo las vegas", "black and grey sleeve"),
    ),
    "how_to_choose_a_tattoo_artist_master_selection_guide_2": TattooGuideSEO(
        slug="how_to_choose_a_tattoo_artist_master_selection_guide_2",
        keyword="tattoo artist",
        style_label="Choosing a Tattoo Artist",
        joshua_note=(
            "Choose an artist by healed photos in your style, not Instagram fresh shots — "
            "ask about consult process, licensing, and how they plan for Vegas sun on your placement."
        ),
        hero_lead=(
            "Choosing an artist means asking for healed photos in your style, not fresh Instagram shots — "
            "and understanding how they plan for Vegas sun on your placement."
        ),
        book_primary="Book Joshua Cole consult",
        book_headline="Las Vegas Tattoo Artist — Book Work of Art",
        extra_keywords=("best tattoo artist las vegas", "how to choose tattoo artist", "tattoo shop las vegas"),
    ),
}


def guide_for(slug: str) -> TattooGuideSEO | None:
    return TATTOO_GUIDES.get(slug)


def page_title(guide: TattooGuideSEO) -> str:
    from woa_expert_voice import joshua_page_title

    return joshua_page_title(guide)


def meta_description(guide: TattooGuideSEO) -> str:
    from woa_expert_voice import joshua_meta

    return joshua_meta(guide)


def seo_lead(guide: TattooGuideSEO) -> str:
    return guide.hero_lead


def seo_faqs(guide: TattooGuideSEO) -> tuple[tuple[str, str], ...]:
    if guide.slug == "tattoo_healing_in_desert_climate_expert_aftercare_guide":
        return _aftercare_faqs()
    if guide.slug == "how_much_do_tattoos_cost_in_las_vegas_authority_guide":
        return _pricing_faqs()
    if guide.slug == "walk_in_tattoos_las_vegas_authority_guide":
        return _walk_in_faqs()
    if guide.slug == "how_to_choose_a_tattoo_artist_master_selection_guide_2":
        return _choose_artist_faqs()
    if guide.slug == "best_tattoo_styles_for_sleeves_large_scale_project_hub":
        return _sleeve_faqs()
    return _service_faqs(guide.keyword, guide.style_label)


def conversion_bar(guide: TattooGuideSEO, *, compact: bool = False) -> str:
    from woa_expert_voice import joshua_cta_blurb

    if compact:
        return f"""<div class="flex flex-wrap gap-3 pt-2">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase" href="{BOOK}">{html.escape(guide.book_primary)}</a>
<a class="inline-flex border border-outline px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase hover:border-secondary" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
</div>"""

    return f"""<aside class="border border-secondary/50 bg-secondary/10 p-6 md:p-8 space-y-4 my-8" data-woa-tattoo-cta="1">
<h2 class="font-headline-md text-on-surface text-xl md:text-2xl">{html.escape(guide.book_headline)}</h2>
<p class="font-body-md text-on-surface-variant">{html.escape(joshua_cta_blurb(guide))}</p>
<div class="flex flex-col sm:flex-row flex-wrap gap-3">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:bg-secondary-fixed transition-colors" href="{BOOK}">{html.escape(guide.book_primary)}</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:border-secondary transition-colors" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:border-secondary transition-colors" href="{JOSHUA_PAGE}">Portfolio</a>
</div>
</aside>"""


def sticky_book_label(slug: str) -> str | None:
    guide = guide_for(slug)
    if not guide:
        if slug == "tattoo_healing_in_desert_climate_expert_aftercare_guide":
            return "Book Tattoo Appointment"
        if "tattoo" in slug and "authority" in slug:
            return "Book Tattoo Consult"
        return None
    short = {
        "realism_tattoos_las_vegas_master_authority_guide": "Book Realism Consult",
        "cover_up_tattoos_las_vegas_master_authority_guide": "Book Cover-Up Consult",
        "walk_in_tattoos_las_vegas_authority_guide": "Walk-In Availability",
        "how_much_do_tattoos_cost_in_las_vegas_authority_guide": "Get Tattoo Quote",
        "fine_line_tattoos_las_vegas_master_authority_guide": "Book Fine Line Tattoo",
        "best_tattoo_styles_for_sleeves_large_scale_project_hub": "Book Sleeve Consult",
    }
    return short.get(slug, guide.book_primary.title())
