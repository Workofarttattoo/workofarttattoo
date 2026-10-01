#!/usr/bin/env python3
"""Expert voice helpers — Joshua & Katelyn copy that reads hand-written, not templated."""

from __future__ import annotations

from typing import TYPE_CHECKING

from woa_nav_config import STUDIO_PHONE_PARENS, STUDIO_STREET_ADDRESS

if TYPE_CHECKING:
    from woa_piercing_authority import PiercingGuide
    from woa_tattoo_seo import TattooGuideSEO


def _trim(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return cut + "…"


def katelyn_hero(guide: "PiercingGuide") -> str:
    """Lead with catalog intro — already first-person. Add one natural booking line."""
    if guide.offered:
        tail = (
            f" I pierce this placement by appointment at {STUDIO_STREET_ADDRESS} — "
            f"book online or call {STUDIO_PHONE_PARENS}."
        )
        return guide.intro + tail
    return (
        f"{guide.intro} We do not offer this placement at Work of Art — "
        f"this page explains why and points you to piercings I do perform."
    )


def katelyn_meta(guide: "PiercingGuide") -> str:
    from woa_piercing_authority import _piercing_phrase

    label = _piercing_phrase(guide.name)
    heal = guide.healing_time.split(";")[0].strip()
    if guide.offered:
        return _trim(
            f"{label} with Katelyn Cole at Work of Art, Las Vegas — anatomy-first, "
            f"starter jewelry sized for swelling, desert aftercare. Typical heal: {heal}. "
            f"Book: {STUDIO_PHONE_PARENS}.",
            155,
        )
    return _trim(
        f"Honest scope on {label.lower()} from Katelyn Cole — what we do and do not pierce "
        f"at Work of Art Las Vegas.",
        155,
    )


def katelyn_cta_blurb(guide: "PiercingGuide") -> str:
    from woa_piercing_authority import _piercing_phrase

    label = _piercing_phrase(guide.name)
    if guide.offered:
        return (
            f"I size starter jewelry for swelling, schedule your downsizing check, and walk you through "
            f"desert aftercare before you leave. {label} appointments at {STUDIO_STREET_ADDRESS}."
        )
    return (
        f"Browse piercings we actually perform — same clean setup and placement-first standards, "
        f"reviewed by me at {STUDIO_STREET_ADDRESS}."
    )


PRICING_SLUG = "how_much_do_tattoos_cost_in_las_vegas_authority_guide"
PRICING_TITLE = "Tattoo Prices in Las Vegas | Rates & Quotes | Work of Art"
PRICING_DESCRIPTION = (
    "What do tattoos cost in Las Vegas? See what affects tattoo pricing, session length and deposits, "
    "then request a personalized quote from Work of Art."
)


def joshua_page_title(guide: "TattooGuideSEO") -> str:
    if guide.slug == PRICING_SLUG:
        return PRICING_TITLE
    return f"{guide.style_label} — Joshua Cole | Work of Art Las Vegas"


def joshua_meta(guide: "TattooGuideSEO") -> str:
    if guide.slug == PRICING_SLUG:
        return PRICING_DESCRIPTION
    return _trim(
        f"{guide.style_label} with Joshua Cole at Work of Art on E. Tropicana — consult-first, "
        f"healed portfolio, desert aftercare coaching. {STUDIO_PHONE_PARENS}.",
        155,
    )


def joshua_cta_blurb(guide: "TattooGuideSEO") -> str:
    return (
        f"Custom {guide.keyword} work starts with a consult and healed-photo goals — "
        f"my studio is at {STUDIO_STREET_ADDRESS}, a short drive from the Strip."
    )
