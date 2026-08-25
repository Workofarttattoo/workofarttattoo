#!/usr/bin/env python3
"""Warm, conversion-focused CTA blocks — text-first booking prompts."""

from __future__ import annotations

import html

from woa_nav_config import (
    HREF_APPOINTMENTS,
    HREF_BOOKING_MAILTO,
    STUDIO_PHONE_PARENS,
    STUDIO_PHONE_TEL,
)

MARKER = 'data-woa-sitewide-cta="1"'


def sitewide_conversion_block(*, compact: bool = False, service: str = "tattoo") -> str:
    """Text us · service-specific booking prompt · walk-in policy."""
    if service == "piercing":
        if compact:
            return f"""<div class="flex flex-wrap gap-3 pt-2" {MARKER}>
<a class="inline-flex bg-secondary text-on-secondary px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase" href="{STUDIO_PHONE_TEL}">Text us: {html.escape(STUDIO_PHONE_PARENS)}</a>
<a class="inline-flex border border-outline px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase hover:border-secondary" href="{HREF_APPOINTMENTS}">Book piercing</a>
<a class="inline-flex border border-outline px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase hover:border-secondary" href="/artists/katelyn-cole/">Katelyn portfolio</a>
</div>"""

        return f"""<aside class="border border-secondary/40 bg-surface-container-low p-6 md:p-8 space-y-4 my-8" {MARKER}>
<h2 class="font-headline-md text-on-surface text-xl md:text-2xl">Questions before a piercing?</h2>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">
<li><strong class="text-on-surface">Text us now:</strong> <a class="text-secondary underline hover:no-underline" href="{STUDIO_PHONE_TEL}">{html.escape(STUDIO_PHONE_PARENS)}</a> — fastest answer for same-day openings, jewelry questions, and downsizing checks.</li>
<li><strong class="text-on-surface">Tell us the piercing you want</strong>, any current piercings nearby, and whether you have irritation, swelling, or a jewelry-fit question.</li>
<li><strong class="text-on-surface">Walk-ins welcome</strong> when the schedule allows — text first so we can tell you if a piercing slot is open today.</li>
</ul>
<div class="flex flex-col sm:flex-row flex-wrap gap-3 pt-2">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:bg-secondary-fixed transition-colors" href="{STUDIO_PHONE_TEL}">Text {html.escape(STUDIO_PHONE_PARENS)}</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:border-secondary transition-colors" href="{HREF_APPOINTMENTS}">Book piercing</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:border-secondary transition-colors" href="/artists/katelyn-cole/">Katelyn portfolio</a>
</div>
</aside>"""

    if compact:
        return f"""<div class="flex flex-wrap gap-3 pt-2" {MARKER}>
<a class="inline-flex bg-secondary text-on-secondary px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase" href="{STUDIO_PHONE_TEL}">Text us: {html.escape(STUDIO_PHONE_PARENS)}</a>
<a class="inline-flex border border-outline px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase hover:border-secondary" href="{HREF_BOOKING_MAILTO}">Send reference photo</a>
<a class="inline-flex border border-outline px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase hover:border-secondary" href="{HREF_APPOINTMENTS}">Book consult</a>
</div>"""

    return f"""<aside class="border border-secondary/40 bg-surface-container-low p-6 md:p-8 space-y-4 my-8" {MARKER}>
<h2 class="font-headline-md text-on-surface text-xl md:text-2xl">Questions before you book?</h2>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">
<li><strong class="text-on-surface">Text us now:</strong> <a class="text-secondary underline hover:no-underline" href="{STUDIO_PHONE_TEL}">{html.escape(STUDIO_PHONE_PARENS)}</a> — fastest answer for walk-in slots and same-day piercing.</li>
<li><strong class="text-on-surface">Send a reference photo</strong> to <a class="text-secondary underline hover:no-underline" href="{HREF_BOOKING_MAILTO}">thewhiteknight702@gmail.com</a> with placement, size, and timeline.</li>
<li><strong class="text-on-surface">Walk-ins welcome</strong> when the schedule allows — text first so we can tell you if a chair is open today.</li>
</ul>
<div class="flex flex-col sm:flex-row flex-wrap gap-3 pt-2">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:bg-secondary-fixed transition-colors" href="{STUDIO_PHONE_TEL}">Text {html.escape(STUDIO_PHONE_PARENS)}</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:border-secondary transition-colors" href="{HREF_BOOKING_MAILTO}">Email reference photo</a>
<a class="inline-flex border border-outline px-8 py-4 font-label-caps text-label-caps tracking-widest justify-center hover:border-secondary transition-colors" href="{HREF_APPOINTMENTS}">Book online</a>
</div>
</aside>"""
