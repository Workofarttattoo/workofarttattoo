#!/usr/bin/env python3
"""Official NAP source-of-truth page for citations and directory cleanup."""

from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

from woa_entity_schema import faq_page_graph, schema_script
from woa_nav_config import (
    STUDIO_ADDRESS_HTML,
    STUDIO_ADDRESS_SINGLE_LINE,
    STUDIO_BOOKING_EMAIL,
    STUDIO_LEGAL_NAME,
    STUDIO_PHONE_DISPLAY,
    STUDIO_PHONE_PARENS,
    STUDIO_PHONE_SCHEMA,
    STUDIO_PHONE_TEL,
    SITE_CANONICAL_HOST,
    SITE_CANONICAL_URL,
    STUDIO_ROSTER_BLURB,
    STUDIO_STREET_ADDRESS,
)
from woa_studio_conversion import sitewide_conversion_block

ROOT = Path(__file__).resolve().parent
SLUG = "official_location_hours_contact"
OUT = ROOT / SLUG / "code.html"
TEMPLATE = ROOT / "appointments" / "code.html"
SITE = SITE_CANONICAL_HOST
CANON = f"{SITE}/{SLUG}/"
TITLE = "Work of Art Tattoo & Piercing — Official Location, Hours & Contact"
DESCRIPTION = (
    "Official NAP for Work of Art Tattoo & Piercing — 2375 E. Tropicana Ave, Suite 3, Las Vegas. "
    f"Phone {STUDIO_PHONE_PARENS}. Address, parking, walk-ins, and booking contact."
)

MAP_QUERY = "2375+E+Tropicana+Suite+3+Las+Vegas+NV+89119"
MAP_LINK = f"https://www.google.com/maps/search/?api=1&query={MAP_QUERY}"
MAP_EMBED = f"https://maps.google.com/maps?q={MAP_QUERY}&output=embed"

FAQS: list[tuple[str, str]] = [
    (
        "What is the official phone number for Work of Art Tattoo & Piercing?",
        f"The studio line is {STUDIO_PHONE_PARENS}. Use this number for walk-in checks, booking questions, and directions — not artist personal mobiles. Update any outdated directory listings to match.",
    ),
    (
        "What are your hours?",
        "Hours should be confirmed before you drive over, especially around holidays, shows, conventions, and event traffic. Call or text the studio for the current schedule.",
    ),
    (
        "Do you take walk-ins?",
        "Walk-ins welcome when the schedule allows — palm-size flash and simple piercings when a chair is open. Text or call first for the fastest answer.",
    ),
    (
        "What is your address for GPS and directories?",
        STUDIO_ADDRESS_SINGLE_LINE,
    ),
    (
        "Do you pierce minors?",
        "Minor piercing rules remain an owner-verification item. Call or text before visiting so the studio can confirm the current age, consent, and ID requirements.",
    ),
]


def main_html() -> str:
    nap_table = f"""<dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-5 font-body-md">
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-1">Business name</dt><dd class="text-on-surface">{html_lib.escape(STUDIO_LEGAL_NAME)}</dd></div>
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-1">Phone</dt><dd><a class="text-secondary underline hover:no-underline" href="{STUDIO_PHONE_TEL}">{html_lib.escape(STUDIO_PHONE_PARENS)}</a></dd></div>
<div class="sm:col-span-2"><dt class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-1">Address</dt><dd class="text-on-surface">{STUDIO_ADDRESS_HTML}</dd></div>
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-1">Email</dt><dd><a class="text-secondary underline hover:no-underline" href="mailto:{STUDIO_BOOKING_EMAIL}">{html_lib.escape(STUDIO_BOOKING_EMAIL)}</a></dd></div>
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-1">Website</dt><dd><a class="text-secondary underline hover:no-underline" href="{SITE_CANONICAL_URL}">www.workofarttattoo.com</a></dd></div>
</dl>"""

    faq_rows = "".join(
        f"""<details class="border border-outline-variant/30 bg-surface-container-high p-5 group">
<summary class="font-headline-md text-on-surface cursor-pointer list-none flex justify-between gap-4">
<span>{html_lib.escape(q)}</span>
<span class="text-secondary font-label-caps text-xs">+</span>
</summary>
<p class="font-body-md text-on-surface-variant mt-4">{html_lib.escape(a)}</p>
</details>"""
        for q, a in FAQS
    )

    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background border-b border-outline-variant/20">
<div class="max-w-3xl mx-auto space-y-6">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Official studio information</span>
<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">{html_lib.escape(TITLE)}</h1>
<p class="font-body-lg text-on-surface-variant leading-relaxed">Use this page as the source of truth when updating Google Business Profile, Yelp, Apple Maps, Fresha, and other directories. If a listing shows an old phone number or address, replace it with the details below.</p>
<p class="font-body-md text-on-surface-variant border-l-4 border-secondary pl-4"><strong class="text-on-surface">Canonical phone:</strong> {html_lib.escape(STUDIO_PHONE_PARENS)} only. Remove any legacy listing numbers that do not forward to this line.</p>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-b border-outline-variant/20">
<div class="max-w-4xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">
<div class="space-y-6">
<h2 class="font-headline-md text-on-surface text-2xl">Name, address &amp; phone (NAP)</h2>
{nap_table}
<p class="font-body-md text-on-surface-variant text-sm">Copy for citations: {html_lib.escape(STUDIO_LEGAL_NAME)} · {html_lib.escape(STUDIO_ADDRESS_SINGLE_LINE)} · {html_lib.escape(STUDIO_PHONE_DISPLAY)} · {html_lib.escape(STUDIO_BOOKING_EMAIL)}</p>
</div>
<div class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Current schedule</h2>
<p class="font-body-md text-on-surface-variant">Call or text the studio before you drive over, especially around holidays, shows, conventions, or event traffic.</p>
<p class="font-body-md text-on-surface-variant text-sm">Exact public hours remain an owner-verification item before they should be used in structured data or directories.</p>
</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background border-b border-outline-variant/20">
<div class="max-w-4xl mx-auto space-y-6">
<h2 class="font-headline-md text-on-surface text-2xl">Map &amp; parking</h2>
<p class="font-body-md text-on-surface-variant">We are on E. Tropicana east of the Strip and near Harry Reid Airport. Suite 3 is inside the retail plaza at {html_lib.escape(STUDIO_STREET_ADDRESS)}.</p>
<div class="aspect-video w-full border border-outline-variant/40 overflow-hidden bg-surface-container">
<iframe allowfullscreen="" height="100%" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{MAP_EMBED}" style="border:0;" title="Work of Art Tattoo &amp; Piercing on Google Maps" width="100%"></iframe>
</div>
<p class="font-body-md"><a class="text-secondary underline hover:no-underline" href="{MAP_LINK}" rel="noopener noreferrer" target="_blank">Open directions in Google Maps</a> · <a class="text-secondary underline hover:no-underline" href="/tattoo-shop-near-las-vegas-strip/">Strip-area driving guide</a></p>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-b border-outline-variant/20">
<div class="max-w-3xl mx-auto space-y-8">
<h2 class="font-headline-md text-on-surface text-2xl">Walk-ins, booking &amp; piercing policy</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-8 font-body-md text-on-surface-variant">
<div class="space-y-3">
<h3 class="font-headline-md text-on-surface text-lg">Walk-ins</h3>
<p>Walk-ins welcome when artists have open chairs — text {html_lib.escape(STUDIO_PHONE_PARENS)} first for the fastest answer. Large realism, cover-ups, and multi-session work start with a consult.</p>
<p><a class="text-secondary underline hover:no-underline" href="/walk-in-tattoos-las-vegas/">Walk-in tattoo guide</a></p>
</div>
<div class="space-y-3">
<h3 class="font-headline-md text-on-surface text-lg">Booking</h3>
<p>Free consultations for custom tattoos. Send reference photos to {html_lib.escape(STUDIO_BOOKING_EMAIL)} with placement and size ideas.</p>
<p><a class="text-secondary underline hover:no-underline" href="/appointments/">Book online</a></p>
</div>
<div class="space-y-3">
<h3 class="font-headline-md text-on-surface text-lg">In-studio artists</h3>
<p>{html_lib.escape(STUDIO_ROSTER_BLURB)}</p>
<p><a class="text-secondary underline hover:no-underline" href="/artists/joshua-cole/">Joshua</a> · <a class="text-secondary underline hover:no-underline" href="/artists/katelyn-cole/">Katelyn</a> · <a class="text-secondary underline hover:no-underline" href="/artists/teralyn/">Teralyn</a></p>
</div>
<div class="space-y-3">
<h3 class="font-headline-md text-on-surface text-lg">Minor piercing questions</h3>
<p>Minor piercing rules should be confirmed before visiting. Call or text the studio for the current age, consent, and ID requirements.</p>
<p><a class="text-secondary underline hover:no-underline" href="/katelyn_piercing_minors_las_vegas_authority_guide/">Minor piercing guide</a></p>
</div>
</div>
{sitewide_conversion_block(service="neutral")}
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background" data-woa-tattoo-faq="1">
<div class="max-w-3xl mx-auto space-y-6">
<h2 class="font-headline-md text-on-surface text-2xl">Directory &amp; citation FAQ</h2>
<p class="font-body-md text-on-surface-variant">Questions from Google, Yelp, and third-party listing sites.</p>
{faq_rows}
</div>
</section>
</main>"""


def patch_meta(page_html: str) -> str:
    page_html = re.sub(r"<title>.*?</title>", f"<title>{html_lib.escape(TITLE)} | Work of Art</title>", page_html, count=1)
    page_html = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{html_lib.escape(DESCRIPTION)}" name="description"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<link href="https://www.workofarttattoo.com/[^"]*" rel="canonical"/>',
        f'<link href="{CANON}" rel="canonical"/>',
        page_html,
        count=1,
    )
    for prop, val in (
        ("og:url", CANON),
        ("og:title", f"{TITLE} | Work of Art"),
        ("og:description", DESCRIPTION),
    ):
        page_html = re.sub(
            rf'<meta content="[^"]*" property="{prop}"/>',
            f'<meta content="{html_lib.escape(val)}" property="{prop}"/>',
            page_html,
            count=1,
        )
    for name, val in (
        ("twitter:title", f"{TITLE} | Work of Art"),
        ("twitter:description", DESCRIPTION),
    ):
        page_html = re.sub(
            rf'<meta content="[^"]*" name="{name}"/>',
            f'<meta content="{html_lib.escape(val)}" name="{name}"/>',
            page_html,
            count=1,
        )
    return page_html


def patch_main(page_html: str, main: str) -> str:
    page_html = re.sub(
        r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*',
        "",
        page_html,
        flags=re.DOTALL,
    )
    page_html = re.sub(
        r"<main[^>]*>.*?</main>",
        main.strip(),
        page_html,
        count=1,
        flags=re.DOTALL,
    )
    graph = faq_page_graph(slug=SLUG, title=TITLE, faqs=FAQS)
    page_html = page_html.replace("</head>", schema_script(graph) + "\n</head>", 1)
    return page_html


def main() -> int:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    page_html = TEMPLATE.read_text(encoding="utf-8")
    page_html = patch_meta(page_html)
    page_html = patch_main(page_html, main_html())
    OUT.write_text(page_html, encoding="utf-8")
    print(f"[ok] {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
