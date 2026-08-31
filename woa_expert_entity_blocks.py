#!/usr/bin/env python3
"""Semantic expert-entity blocks — reinforce Katelyn Cole & Joshua Cole knowledge graphs."""

from __future__ import annotations

import html

KATELYN_LINKS: tuple[tuple[str, str], ...] = (
    ("Katelyn Cole", "/artists/katelyn-cole/"),
    ("Ear curation", "/katelyn_ear_curation_las_vegas_authority_guide/"),
    ("Starter jewelry fit", "/katelyn_implant_grade_titanium_las_vegas_authority_guide/"),
    ("Luxury jewelry", "/piercing_jewelry_guide_las_vegas/"),
    ("Piercing healing", "/piercing_healing_guide_las_vegas/"),
    ("Anatomy", "/katelyn_anatomy_matters_las_vegas_authority_guide/"),
    ("Las Vegas piercing", "/piercing_types_las_vegas_authority_hub/"),
)

JOSHUA_LINKS: tuple[tuple[str, str], ...] = (
    ("Joshua Cole", "/artists/joshua-cole/"),
    ("Oil painter", "/artists/joshua-cole/#oil-painting"),
    ("Realism", "/realism_tattoos_las_vegas_master_authority_guide/"),
    ("Black & grey", "/realism_tattoos_las_vegas_master_authority_guide/"),
    ("Portraiture", "/healed_portrait_tattoos_las_vegas/"),
    ("Composition", "/best_tattoo_styles_for_sleeves_large_scale_project_hub/"),
    ("Fine art", "/realism_tattoos_las_vegas_master_authority_guide/"),
    ("Tattoo educator", "/artists/joshua-cole/#seminars"),
    ("Skin science", "/skin_science_tattoo_dermatology_authority_guide/"),
    ("Las Vegas", "/tattoo-shop-near-las-vegas-strip/"),
)


def _graph_block(title: str, links: tuple[tuple[str, str], ...], marker: str) -> str:
    items = "".join(
        f"""<li class="flex items-center gap-2 flex-wrap">
<a class="text-secondary underline hover:no-underline font-body-md" href="{html.escape(href)}">{html.escape(label)}</a>
<span class="text-on-surface-variant" aria-hidden="true">→</span>
</li>"""
        for label, href in links[:-1]
    )
    last_label, last_href = links[-1]
    items += (
        f'<li><a class="text-secondary underline hover:no-underline font-body-md" '
        f'href="{html.escape(last_href)}">{html.escape(last_label)}</a></li>'
    )
    return f"""<nav aria-label="{html.escape(title)}" class="border border-outline-variant/30 bg-surface-container-low p-5 my-6" {marker}>
<p class="font-label-caps text-[10px] uppercase tracking-widest text-secondary mb-3">{html.escape(title)}</p>
<ol class="flex flex-col gap-1 list-none pl-0">{items}</ol>
</nav>"""


def katelyn_entity_block() -> str:
    return _graph_block(
        "Katelyn Cole — piercing topics",
        KATELYN_LINKS,
        'data-woa-katelyn-entity="1"',
    )


def joshua_entity_block() -> str:
    return _graph_block(
        "Joshua Cole — fine art & realism",
        JOSHUA_LINKS,
        'data-woa-joshua-entity="1"',
    )
