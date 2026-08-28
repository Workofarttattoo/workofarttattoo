#!/usr/bin/env python3
"""Catalog of Joshua Cole actively tattooing — for artist-at-work sections only."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"

# UUID prefixes where Joshua is visibly tattooing (machine on skin).
JOSHUA_TATTOOING_UUIDS: frozenset[str] = frozenset(
    {
        "70837687",  # tattoo session in progress
        "67F63F8A",  # tattooing lyric piece
        "F39790C4",  # studio session in progress
        "55A4538D",  # fine-line ankle work
        "7AC4181A",  # tattooing client forearm
        "83BE4284",  # geometric forearm stencil
        "F76AEEF5",  # head tattoo session
    }
)

# Self-hosted close-up used on homepage Experience section.
HOMEPAGE_AT_WORK_STEM = "las-vegas-tattoo-artist-working-closeup"
HOMEPAGE_AT_WORK_WEBP = f"/{HOME.name}/{HOMEPAGE_AT_WORK_STEM}.webp"
HOMEPAGE_AT_WORK_PNG = f"/{HOME.name}/{HOMEPAGE_AT_WORK_STEM}.png"
HOMEPAGE_AT_WORK_ALT = (
    "Joshua Cole tattooing a client at Work of Art Tattoo &amp; Piercing, Las Vegas"
)


def is_joshua_tattooing_uuid(uuid_prefix: str) -> bool:
    return uuid_prefix.upper() in JOSHUA_TATTOOING_UUIDS


def homepage_at_work_picture(*, eager: bool = False) -> str:
    loading = "eager" if eager else "lazy"
    fetch = ' fetchpriority="high"' if eager else ""
    return (
        f'<picture><source srcset="{HOMEPAGE_AT_WORK_WEBP}" type="image/webp"/>'
        f'<img alt="{HOMEPAGE_AT_WORK_ALT}" class="w-full h-full object-cover object-center" '
        f'decoding="async" loading="{loading}"{fetch} src="{HOMEPAGE_AT_WORK_PNG}"/></picture>'
    )
