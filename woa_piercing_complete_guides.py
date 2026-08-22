#!/usr/bin/env python3
"""Complete piercing guide titles + placement-specific deep sections."""

from __future__ import annotations

from dataclasses import replace

from woa_piercing_authority import PiercingGuide, _piercing_phrase
from woa_piercing_profiles import EncyclopediaSections, sections_for


def complete_guide_h1(guide: PiercingGuide) -> str:
    label = _piercing_phrase(guide.name)
    return f"The Complete {label} Guide"


def complete_page_title(guide: PiercingGuide) -> str:
    label = _piercing_phrase(guide.name)
    return f"{label} — Katelyn Cole | Work of Art Las Vegas"


def _industrial(name: str, base: EncyclopediaSections) -> EncyclopediaSections:
    return replace(
        base,
        anatomy_requirements=(
            "Two stable cartilage points with enough tissue for a 90-degree angle — classic helix-to-helix or custom angles.",
            "The ridge between points must allow a bar that does not torque tissue — I measure standing and lying down.",
            "Ears with shallow helix rims or extreme folds often cannot support a fair industrial heal.",
        ),
        who_should_avoid=(
            "Not enough cartilage shelf on one or both points — I decline rather than pierce a migrating industrial.",
            "Cannot sleep on your back for 6–12 months or remove over-ear headphones during heal.",
            "Active outer-ear infection, recent cartilage work on the same ear without a staged plan.",
        ),
        jewelry_sizing=(
            "Starter industrial bar is long for swelling — typically 1.5–2\" depending on ear width; never guess at a mall kiosk.",
            "Implant-grade titanium (ASTM F136); gauge usually 14G for initial heal.",
            "Bar length must clear both entries without pulling tissue inward — custom measure every ear.",
        ),
        swelling_expectations=(
            "Both holes swell independently days 1–7 — the bar can look slightly bowed until downsizing.",
            "One side more swollen than the other is common; embedding on either end means come in immediately.",
        ),
        headphones=(
            "Over-ear headphones and gaming headsets add constant pressure — plan around them for 6+ months or shift placement.",
            "On-ear and in-ear buds are usually safer once swelling drops; wipe with saline after gym use.",
        ),
        helmets=(
            "Motorcycle, skate, and climbing helmets contact the industrial bar directly — skip contact sports until cleared.",
            "If you ride daily, tell me at consult — we may stage one helix first instead of a connected bar.",
        ),
        keloids_vs_bumps=(
            "Irritation bumps on industrials are usually pressure or long jewelry — fix angle, downsize, stop sleeping on the ear.",
            "Keloids are rare but genetic — family history matters; hypertrophic scars can look similar; see a clinician if tissue grows beyond the piercing.",
            "A bump on only one hole often means that angle is wrong — both entries need assessment, not just one.",
        ),
        migration=(
            "Industrial migration shows as the bar tilting toward one rim over weeks — wrong angle from day one is the usual cause.",
            "Sleeping pressure makes one hole heal at an angle while the other stays straight — the bar wins the fight and migrates.",
        ),
        rejection=(
            "Rejection looks like thinning skin at an entry and the bar sitting closer to the surface — early removal preserves better scar than waiting.",
            "Surface-style industrials on shallow anatomy reject faster — honest anatomy assessment prevents this.",
        ),
        desert_healing=base.desert_healing
        + (
            "Vegas dry air tightens crusties on both holes — saline both entries; do not rotate the bar.",
            "Summer car headrests and AC vents dry the ear — travel pillow for side-sleepers.",
        ),
    )


def _default_complete(slug_id: str, name: str, base: EncyclopediaSections) -> EncyclopediaSections:
    low = name.lower()
    anatomy = (
        f"I assess {low} anatomy before marking — tissue depth, angle, and lifestyle (sleep, headphones, helmets).",
        "I decline when anatomy cannot support a safe 90-degree piercing — not every trend placement fits every body.",
    )
    jewelry = (
        "Starter length accounts for swelling — implant-grade titanium flat-back or bar sized at consult.",
        "Gauge and length are chosen for your anatomy, not copied from a photo on Pinterest.",
    )
    if not base.swelling:
        swelling_exp = ("Mild swelling days 1–5 is normal; embedding is not.",)
    else:
        swelling_exp = base.swelling

    headphones: tuple[str, ...] = ()
    helmets: tuple[str, ...] = ()
    profile = slug_id
    ear_cartilage = {
        "helix", "forward_helix", "flat", "conch", "tragus", "anti_tragus",
        "daith", "rook", "snug", "orbital", "industrial",
    }
    if profile in ear_cartilage or slug_id in ear_cartilage:
        headphones = (
            "Over-ear headphones add pressure on cartilage — limit use early heal or switch to on-ear/in-ear after downsizing.",
        )
        helmets = (
            "Sports and motorcycle helmets contact the ear — avoid direct pressure until your piercer clears you.",
        )

    keloids = (
        "Irritation bumps: fluid-filled, tied to pressure, long jewelry, or sleeping — usually fixable with downsizing and saline.",
        "Keloids: raised scar tissue that grows beyond the piercing, often genetic — see a dermatologist; do not self-diagnose online.",
        "If a bump grows for two weeks after fixing sleep and jewelry, book a check-in — do not stack home remedies.",
    )

    return replace(
        base,
        anatomy_requirements=anatomy if not base.anatomy_requirements else base.anatomy_requirements,
        jewelry_sizing=jewelry if not base.jewelry_sizing else base.jewelry_sizing,
        swelling_expectations=swelling_exp if not base.swelling_expectations else base.swelling_expectations,
        headphones=headphones if not base.headphones else base.headphones,
        helmets=helmets if not base.helmets else base.helmets,
        keloids_vs_bumps=keloids if not base.keloids_vs_bumps else base.keloids_vs_bumps,
    )


def complete_sections_for(slug_id: str, name: str) -> EncyclopediaSections:
    base = sections_for(slug_id, name)
    if slug_id == "industrial":
        return _industrial(name, base)
    return _default_complete(slug_id, name, base)
