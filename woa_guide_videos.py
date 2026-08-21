#!/usr/bin/env python3
"""Map guide pages to studio video embeds — one question, one clip."""

from __future__ import annotations

import html
from dataclasses import dataclass


@dataclass(frozen=True)
class GuideVideo:
    question: str
    embed_url: str
    caption: str
    studio_href: str = "/studio_videos/"


# Instagram embeds from studio_videos/videos.json — swap IDs when new single-question reels ship.
GUIDE_VIDEOS: dict[str, GuideVideo] = {
    "daith_piercing_las_vegas_authority_guide": GuideVideo(
        question="Does a daith piercing hurt?",
        embed_url="https://www.instagram.com/reel/C78fY1quCVF/embed",
        caption="Katelyn Cole piercing in-studio — placement, angle, and jewelry sizing at the chair.",
        studio_href="/studio_videos/#katelyn-piercing",
    ),
    "helix_piercing_las_vegas_authority_guide": GuideVideo(
        question="Does a helix piercing hurt?",
        embed_url="https://www.instagram.com/reel/C78fY1quCVF/embed",
        caption="Cartilage piercing at the chair — angle, pressure, and what to expect with Katelyn Cole.",
        studio_href="/studio_videos/#katelyn-piercing",
    ),
    "katelyn_downsizing_jewelry_las_vegas_authority_guide": GuideVideo(
        question="When can I change my piercing jewelry?",
        embed_url="https://www.instagram.com/reel/C0nNwUkRHz6/embed",
        caption="Implant-grade jewelry and anatomical placement — why downsizing timing matters.",
        studio_href="/studio_videos/#katelyn-piercing",
    ),
    "piercing_jewelry_guide_las_vegas": GuideVideo(
        question="When can I change my piercing jewelry?",
        embed_url="https://www.instagram.com/reel/C0nNwUkRHz6/embed",
        caption="Starter length vs healed fit — Katelyn on jewelry and placement.",
        studio_href="/studio_videos/#katelyn-piercing",
    ),
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": GuideVideo(
        question="How long until I can swim after a tattoo in Vegas?",
        embed_url="https://www.instagram.com/reel/C8vPwacP1du/embed",
        caption="Joshua Cole on craft and long-term heal — desert sun changes the timeline.",
        studio_href="/studio_videos/#joshua-cole",
    ),
    "piercing_aftercare_desert_climate_las_vegas_expert_guide": GuideVideo(
        question="How long until I can swim with a fresh piercing?",
        embed_url="https://www.instagram.com/reel/C4fOsY7OSTq/embed",
        caption="Ear curation and aftercare in the studio — Katelyn Cole, Las Vegas.",
        studio_href="/studio_videos/#katelyn-piercing",
    ),
    "realism_tattoos_las_vegas_master_authority_guide": GuideVideo(
        question="Why did my tattoo get lighter as it healed?",
        embed_url="https://www.instagram.com/reel/Cpp18lXgU3P/embed",
        caption="Value range and aging — Joshua Cole on realism that holds in Vegas sun.",
        studio_href="/studio_videos/#joshua-cole",
    ),
}


def video_for_slug(slug: str) -> GuideVideo | None:
    return GUIDE_VIDEOS.get(slug)


def video_section(slug: str) -> str:
    clip = video_for_slug(slug)
    if not clip:
        return ""
    return f"""<section class="space-y-4 my-8" data-woa-guide-video="1" id="studio-video">
<h2 class="font-headline-md text-on-surface text-2xl">{html.escape(clip.question)}</h2>
<p class="font-body-md text-on-surface-variant text-sm">{html.escape(clip.caption)}</p>
<div class="aspect-[9/16] max-w-sm mx-auto border border-outline-variant/40 bg-surface-container-low overflow-hidden">
<iframe allowfullscreen="" class="w-full h-full min-h-[420px]" loading="lazy" src="{html.escape(clip.embed_url)}" title="{html.escape(clip.question)}"></iframe>
</div>
<p class="font-body-md text-on-surface-variant text-sm text-center pt-2">
<a class="text-secondary underline" href="{html.escape(clip.studio_href)}">More studio videos</a>
</p>
</section>"""
