#!/usr/bin/env python3
"""Reusable piercing promotion data and rendering helpers."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from woa_nav_config import STUDIO_ADDRESS_SINGLE_LINE, STUDIO_PHONE_PARENS, STUDIO_PHONE_TEL

ROOT = Path(__file__).resolve().parent
PROMO_PATH = ROOT / "siteData" / "piercing_promotions.json"
SPECIALS_SLUG = "piercing-specials-las-vegas"
SPECIALS_URL = f"/{SPECIALS_SLUG}/"
KATELYN_URL = "/artists/katelyn-cole/"
JEWELRY_URL = "/piercing_jewelry_guide_las_vegas/"
DIRECTIONS_URL = "/official_location_hours_contact/"


def load_promotions() -> list[dict[str, Any]]:
    return json.loads(PROMO_PATH.read_text(encoding="utf-8"))


def current_promotion() -> dict[str, Any]:
    promos = load_promotions()
    for promo in promos:
        if str(promo.get("status", "")).upper() == "ACTIVE":
            return promo
    return promos[0]


def _attrs(promo: dict[str, Any]) -> str:
    return (
        f'data-woa-piercing-special="1" '
        f'data-woa-promo-id="{html.escape(str(promo["id"]))}" '
        f'data-woa-promo-campaign="{html.escape(str(promo["analyticsCampaign"]))}"'
    )


def _cta(href: str, label: str, *, primary: bool = False, extra: str = "") -> str:
    klass = (
        "inline-flex items-center justify-center bg-secondary text-on-secondary px-8 py-4 "
        "font-label-caps text-label-caps tracking-widest uppercase"
        if primary
        else "inline-flex items-center justify-center border border-outline px-8 py-4 "
        "font-label-caps text-label-caps tracking-widest uppercase hover:border-secondary transition-colors"
    )
    return f'<a class="{klass}" href="{html.escape(href)}" {extra}>{html.escape(label)}</a>'


def render_current_piercing_special(*, variant: str = "standard", context: str = "content") -> str:
    promo = current_promotion()
    price = str(promo.get("displayPrice") or "").strip()
    price_line = (
        f'<p class="font-headline-md text-secondary text-2xl">{html.escape(price)}</p>'
        if price
        else '<p class="font-label-caps text-secondary uppercase tracking-[0.2em] text-xs">Current weekly feature</p>'
    )
    eligible = ", ".join(str(item) for item in promo.get("eligiblePiercings", [])[:5])
    data = _attrs(promo)
    booking_extra = (
        'data-woa-piercing-booking-start="1" data-woa-promo-click="booking" '
        f'data-woa-promo-context="{html.escape(context)}"'
    )
    special_extra = (
        'data-woa-promo-click="special" '
        f'data-woa-promo-context="{html.escape(context)}"'
    )
    text_extra = (
        'data-woa-piercing-text-click="1" data-woa-promo-click="text" '
        f'data-woa-promo-context="{html.escape(context)}"'
    )

    if variant == "compact":
        return f"""<aside class="border border-secondary/40 bg-secondary/10 p-5 space-y-3" {data} data-woa-promo-variant="compact">
<p class="font-label-caps text-secondary uppercase tracking-[0.2em] text-[10px]">This week at Work of Art</p>
<h2 class="font-headline-md text-on-surface text-xl">Piercing in Las Vegas</h2>
<p class="font-body-md text-on-surface-variant">{html.escape(str(promo["description"]))}</p>
<div class="flex flex-col sm:flex-row gap-3">
{_cta(SPECIALS_URL, str(promo["ctaText"]), primary=True, extra=special_extra)}
{_cta(STUDIO_PHONE_TEL.replace("tel:", "sms:"), "Text for today", extra=text_extra)}
</div>
</aside>"""

    image = str(promo.get("image") or "")
    alt = str(promo.get("altText") or "Piercing work at Work of Art Tattoo and Piercing")
    image_html = (
        f'<img alt="{html.escape(alt)}" class="aspect-[4/5] w-full object-cover border border-outline-variant/30" '
        f'decoding="async" loading="lazy" src="{html.escape(image)}"/>'
        if image
        else ""
    )
    hero_class = "grid grid-cols-1 lg:grid-cols-[1.1fr_0.9fr] gap-8 items-center" if variant == "hero" else "space-y-6"
    return f"""<aside class="border border-secondary/40 bg-surface-container-low p-6 md:p-8 {hero_class}" {data} data-woa-promo-variant="{html.escape(variant)}">
<div class="space-y-5">
<p class="font-label-caps text-secondary uppercase tracking-[0.2em] text-xs">This week at Work of Art</p>
<h2 class="font-headline-md text-on-surface text-2xl md:text-3xl">{html.escape(str(promo["headline"]))}</h2>
{price_line}
<p class="font-body-md text-on-surface-variant leading-relaxed">{html.escape(str(promo["description"]))}</p>
<dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 font-body-md text-sm">
<div><dt class="text-secondary font-label-caps uppercase tracking-widest text-[10px]">Piercer</dt><dd class="text-on-surface">Katelyn Cole</dd></div>
<div><dt class="text-secondary font-label-caps uppercase tracking-widest text-[10px]">Eligible work</dt><dd class="text-on-surface">{html.escape(eligible)}</dd></div>
<div><dt class="text-secondary font-label-caps uppercase tracking-widest text-[10px]">Jewelry</dt><dd class="text-on-surface">{html.escape(str(promo["jewelryTerms"]))}</dd></div>
<div><dt class="text-secondary font-label-caps uppercase tracking-widest text-[10px]">Studio</dt><dd class="text-on-surface">{html.escape(STUDIO_ADDRESS_SINGLE_LINE)}</dd></div>
</dl>
<p class="font-body-sm text-on-surface-variant">{html.escape(str(promo["exclusions"]))}</p>
<div class="flex flex-col sm:flex-row flex-wrap gap-3">
{_cta(str(promo["bookingUrl"]), "Book piercing", primary=True, extra=booking_extra)}
{_cta(SPECIALS_URL, str(promo["ctaText"]), extra=special_extra)}
{_cta(STUDIO_PHONE_TEL.replace("tel:", "sms:"), "Text for today", extra=text_extra)}
</div>
</div>
{image_html}
</aside>"""


def render_meet_your_piercer(*, context: str = "content") -> str:
    return f"""<aside class="border border-outline-variant/30 bg-background p-5 md:p-6 space-y-4" data-woa-meet-your-piercer="katelyn" data-woa-piercing-context="{html.escape(context)}">
<div class="space-y-2">
<p class="font-label-caps text-secondary uppercase tracking-[0.2em] text-[10px]">Meet your piercer</p>
<h2 class="font-headline-md text-on-surface text-xl">Katelyn Cole at Work of Art</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">Katelyn handles professional piercing consults, anatomy checks, jewelry planning, and follow-up questions at our Tropicana studio. Start with her portfolio, current piercing specials, or a direct booking request.</p>
</div>
<div class="flex flex-col sm:flex-row gap-3">
{_cta(KATELYN_URL, "Katelyn's portfolio", primary=True, extra='data-woa-katelyn-profile-click="1"')}
{_cta("/appointments/", "Book piercing", extra='data-woa-piercing-booking-start="1"')}
{_cta(STUDIO_PHONE_TEL.replace("tel:", "sms:"), "Text for today", extra='data-woa-piercing-text-click="1"')}
</div>
</aside>"""


def render_piercing_decision_module() -> str:
    return f"""<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" data-woa-piercing-decision="1">
<div class="max-w-5xl mx-auto space-y-6">
<p class="font-label-caps text-secondary uppercase tracking-[0.2em] text-xs">Piercing in Las Vegas</p>
<h2 class="font-headline-md text-on-surface text-3xl">Professional piercing with Katelyn Cole</h2>
<p class="font-body-lg text-on-surface-variant max-w-3xl">Start with the current weekly piercing feature, then choose booking, same-day availability, portfolio proof, or jewelry education based on what you need before you commit.</p>
{render_meet_your_piercer(context="decision-module")}
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
{_cta(SPECIALS_URL, "This week's special", primary=True, extra='data-woa-promo-click="main-page-special"')}
{_cta("/appointments/", "Book piercing", extra='data-woa-piercing-booking-start="1"')}
{_cta(STUDIO_PHONE_TEL.replace("tel:", "sms:"), "Text for today", extra='data-woa-piercing-text-click="1"')}
{_cta(KATELYN_URL, "See real work", extra='data-woa-katelyn-profile-click="1"')}
{_cta(JEWELRY_URL, "See jewelry", extra='data-woa-piercing-jewelry-click="1"')}
</div>
</div>
</section>"""
