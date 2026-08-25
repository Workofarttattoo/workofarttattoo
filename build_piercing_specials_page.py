#!/usr/bin/env python3
"""Build the permanent Las Vegas piercing specials page."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_entity_schema import ID_KATELYN, guide_article_graph, schema_script
from woa_nav_config import STUDIO_ADDRESS_SINGLE_LINE, STUDIO_PHONE_DISPLAY, STUDIO_PHONE_TEL
from woa_piercing_promotions import (
    DIRECTIONS_URL,
    JEWELRY_URL,
    KATELYN_URL,
    SPECIALS_SLUG,
    current_promotion,
    render_current_piercing_special,
)

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"


def main_html() -> str:
    promo = current_promotion()
    eligible = "".join(
        f"<li>{html.escape(str(item))}</li>" for item in promo.get("eligiblePiercings", [])
    )
    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-[1.05fr_0.95fr] gap-10 items-start">
<div class="space-y-6">
<p class="font-label-caps text-secondary uppercase tracking-[0.2em] text-xs">This week at Work of Art</p>
<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">Piercing Specials in Las Vegas</h1>
<p class="font-body-lg text-on-surface-variant leading-relaxed">One permanent page for current Work of Art piercing offers, same-day availability, and booking links. We keep the URL stable so old weekly specials do not stay indexed after they expire.</p>
<div class="flex flex-col sm:flex-row gap-3">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center uppercase" href="/appointments/" data-woa-piercing-booking-start="1">Book piercing</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center uppercase hover:border-secondary" href="{STUDIO_PHONE_TEL.replace('tel:', 'sms:')}" data-woa-piercing-text-click="1">Text for today</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center uppercase hover:border-secondary" href="{DIRECTIONS_URL}" data-woa-piercing-directions-click="1">Directions</a>
</div>
</div>
{render_current_piercing_special(variant="hero", context="specials-page")}
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
<div class="space-y-4">
<p class="font-label-caps text-secondary uppercase tracking-[0.2em] text-xs">Professional piercer</p>
<h2 class="font-headline-md text-on-surface text-3xl">Katelyn Cole</h2>
<p class="font-body-md text-on-surface-variant">Katelyn is the Work of Art piercer clients book for anatomy-based placement, ear curation, jewelry-fit planning, aftercare questions, and downsizing timing.</p>
<a class="text-secondary underline font-body-md" href="{KATELYN_URL}" data-woa-katelyn-profile-click="1">See Katelyn's piercing portfolio</a>
</div>
<img alt="Katelyn Cole professional piercer at Work of Art Las Vegas" class="aspect-[4/5] w-full object-cover border border-outline-variant/30" decoding="async" loading="lazy" src="/artists/katelyn-cole/katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas.webp"/>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-12">
<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Piercings offered</h2>
<p class="font-body-md text-on-surface-variant">The weekly feature can change, but the consult process stays the same: anatomy first, clean placement marks, starter fit, and aftercare you can actually follow in Las Vegas.</p>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">{eligible}</ul>
</section>
<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Jewelry, anatomy, and placement</h2>
<p class="font-body-md text-on-surface-variant">Starter jewelry is selected in the room based on placement, swelling room, and your anatomy. Katelyn will tell you when a placement needs a different angle, a staged plan, or a no for long-term healing.</p>
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline" href="{JEWELRY_URL}" data-woa-piercing-jewelry-click="1">Read the piercing jewelry guide</a>.</p>
</section>
<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Same-day and walk-in availability</h2>
<p class="font-body-md text-on-surface-variant">Same-day openings happen, especially for single piercings, but texting first is the fastest way to confirm schedule room before driving across town or leaving the Strip.</p>
</section>
<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Healing and aftercare in Las Vegas</h2>
<p class="font-body-md text-on-surface-variant">Dry air, hotel pools, sunscreen, shows, flights, headphones, and sleep position all matter after a fresh piercing. Plan the piercing before alcohol, pool time, and long travel days.</p>
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline" href="/piercing_aftercare_desert_climate_las_vegas_expert_guide/">Read the desert piercing aftercare guide</a>.</p>
</section>
<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Location and parking</h2>
<p class="font-body-md text-on-surface-variant">{html.escape(STUDIO_ADDRESS_SINGLE_LINE)}. Text or call {html.escape(STUDIO_PHONE_DISPLAY)} for current openings; use the official location page for maps, parking, and contact details.</p>
</section>
<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Questions clients ask</h2>
<details class="border border-outline-variant/30 bg-surface-container-high p-5"><summary class="font-headline-md text-on-surface cursor-pointer">Is the weekly feature still professional piercing?</summary><p class="font-body-md text-on-surface-variant mt-4">Yes. The point is a current feature, not racing to the lowest price. Placement, sterile setup, jewelry fit, and aftercare time still matter.</p></details>
<details class="border border-outline-variant/30 bg-surface-container-high p-5"><summary class="font-headline-md text-on-surface cursor-pointer">Can I walk in for the weekly piercing special?</summary><p class="font-body-md text-on-surface-variant mt-4">Sometimes. Text first for today's availability so the studio can confirm Katelyn's schedule and whether the placement fits your anatomy.</p></details>
<details class="border border-outline-variant/30 bg-surface-container-high p-5"><summary class="font-headline-md text-on-surface cursor-pointer">Can I upgrade or change jewelry?</summary><p class="font-body-md text-on-surface-variant mt-4">Ask during the consult. Fresh-piercing jewelry choices depend on fit, swelling, placement, and what is appropriate for the stage of healing.</p></details>
</section>
<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Book this week's piercing feature</h2>
<div class="flex flex-col sm:flex-row gap-3">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center uppercase" href="/appointments/" data-woa-piercing-booking-start="1">Book piercing</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center uppercase hover:border-secondary" href="{STUDIO_PHONE_TEL.replace('tel:', 'sms:')}" data-woa-piercing-text-click="1">Text for today</a>
</div>
</section>
</div>
</section>
</main>"""


def patch_meta(page: str) -> str:
    title = "Piercing Specials in Las Vegas"
    desc = "Current piercing specials at Work of Art Las Vegas with Katelyn Cole, same-day availability, booking, jewelry-fit planning, aftercare, and directions."
    canon = f"{SITE}/{SPECIALS_SLUG}/"
    page = re.sub(r"<title>.*?</title>", f"<title>{title} | Work of Art</title>", page, count=1)
    page = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{desc}" name="description"/>', page, count=1)
    page = re.sub(r'<link href="https://www.workofarttattoo.com/[^"]*" rel="canonical"/>', f'<link href="{canon}" rel="canonical"/>', page, count=1)
    page = re.sub(r'<meta content="https://www.workofarttattoo.com/[^"]*" property="og:url"/>', f'<meta content="{canon}" property="og:url"/>', page, count=1)
    page = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{title} | Work of Art" property="og:title"/>', page, count=1)
    page = re.sub(r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{desc}" property="og:description"/>', page, count=1)
    page = re.sub(r'<meta content="[^"]*" name="twitter:title"/>', f'<meta content="{title} | Work of Art" name="twitter:title"/>', page, count=1)
    page = re.sub(r'<meta content="[^"]*" name="twitter:description"/>', f'<meta content="{desc}" name="twitter:description"/>', page, count=1)
    return page


def main() -> int:
    page = TEMPLATE.read_text(encoding="utf-8")
    page = patch_meta(page)
    page = re.sub(r'<main class="relative pt-20">.*?</main>', main_html(), page, count=1, flags=re.DOTALL)
    page = re.sub(r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*', "", page, flags=re.DOTALL)
    graph = guide_article_graph(
        slug=SPECIALS_SLUG,
        title="Piercing Specials in Las Vegas",
        description="Permanent Work of Art page for current piercing specials, booking, same-day availability, Katelyn Cole, aftercare, and location details.",
        author_id=ID_KATELYN,
    )
    page = page.replace("</head>", schema_script(graph) + "\n</head>", 1)
    out = ROOT / SPECIALS_SLUG
    out.mkdir(parents=True, exist_ok=True)
    (out / "code.html").write_text(page, encoding="utf-8")
    print(f"[ok] {SPECIALS_SLUG}/code.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
