#!/usr/bin/env python3
"""Shared content standards — expert attribution, revision dates, section helpers."""

from __future__ import annotations

import html

LAST_UPDATED = "June 2026"
LAST_UPDATED_ISO = "2026-06-01"

KATELYN_REVIEW = "Katelyn Morgen Cole, Professional Piercer"
JOSHUA_REVIEW = "Joshua Cole, Tattoo Artist"


def reviewed_by_block(
    *,
    expert: str = "katelyn",
    updated: str = LAST_UPDATED,
) -> str:
    """E-E-A-T line for guide pages — maintained, named expert."""
    if expert == "joshua":
        name = JOSHUA_REVIEW
        label = "Joshua's Studio Notes"
    elif expert == "both":
        return f"""<p class="font-body-md text-on-surface-variant border border-outline-variant/30 bg-surface-container-low px-5 py-4 rounded-sm">
<span class="font-label-caps text-[10px] uppercase tracking-widest text-secondary block mb-1">Reviewed &amp; maintained</span>
Reviewed by {html.escape(JOSHUA_REVIEW)} and {html.escape(KATELYN_REVIEW)} · Last updated: {html.escape(updated)}
</p>"""
    else:
        name = KATELYN_REVIEW
        label = "Katelyn's Piercing Tips"
    return f"""<p class="font-body-md text-on-surface-variant border border-outline-variant/30 bg-surface-container-low px-5 py-4 rounded-sm">
<span class="font-label-caps text-[10px] uppercase tracking-widest text-secondary block mb-1">Reviewed &amp; maintained</span>
Reviewed by {html.escape(name)} · Last updated: {html.escape(updated)}
<span class="sr-only">Expert section label: {html.escape(label)}</span>
</p>"""


def katelyn_piercing_notes(
    tips: tuple[str, ...],
    recommendations: tuple[str, ...],
    *,
    placement: str = "",
) -> str:
    """Multi-tip expert section — distinct from the single-quote callout."""
    seen: set[str] = set()
    items: list[str] = []
    for line in tips + recommendations:
        key = line.strip().lower()
        if key and key not in seen:
            seen.add(key)
            items.append(line.strip())
    if not items:
        return ""
    bullets = "".join(
        f"<li class=\"font-body-md text-on-surface-variant\">{html.escape(line)}</li>"
        for line in items[:6]
    )
    subtitle = (
        f" — what I tell clients about {html.escape(placement)}" if placement else ""
    )
    return f"""<section class="space-y-4 my-8" id="katelyn-notes">
<h2 class="font-headline-md text-on-surface text-2xl">Katelyn's Piercing Notes{subtitle}</h2>
<ul class="space-y-3 list-disc pl-5 marker:text-secondary">{bullets}</ul>
</section>"""


def expert_callout(title: str, quote: str, *, expert: str = "katelyn") -> str:
    """Recurring expert insight block — not generic SEO filler."""
    if expert == "joshua":
        heading = "Joshua's Studio Notes"
    else:
        heading = "Katelyn's Piercing Tips"
    return f"""<aside class="border-l-4 border-secondary pl-6 py-3 space-y-2 my-8 bg-surface-container-low/50">
<p class="font-label-caps text-secondary uppercase tracking-widest text-[10px]">{html.escape(heading)}</p>
<p class="font-body-lg text-on-surface leading-relaxed">{html.escape(quote)}</p>
</aside>"""


def toc_nav(items: tuple[tuple[str, str], ...]) -> str:
    """Jump links for consistent page structure — helps users and AI parsers."""
    links = "".join(
        f'<a class="text-secondary underline hover:no-underline text-sm" href="#{html.escape(aid)}">{html.escape(label)}</a>'
        for label, aid in items
    )
    return f"""<nav aria-label="On this page" class="flex flex-wrap gap-x-4 gap-y-2 py-4 border-y border-outline-variant/20">
<span class="font-label-caps text-[10px] uppercase tracking-widest text-on-surface-variant w-full mb-1">On this page</span>
{links}
</nav>"""
