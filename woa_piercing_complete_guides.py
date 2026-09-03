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
            "Starter jewelry fitted to anatomy; gauge usually 14G for initial heal.",
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
        "I decline when anatomy cannot support stable placement — not every trend placement fits every body.",
    )
    jewelry = (
        "Starter length accounts for swelling — flat-back or bar jewelry sized at consult.",
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


# Studio-education notes from Katelyn's apprenticeship workbook — gaps only, no duplicate heal/jewelry copy.
_WORKBOOK_SUPPLEMENTS: dict[str, dict[str, object]] = {
    "ear_lobe": {
        "extra_sections": (
            (
                "stretching-healed-lobes",
                "Stretching healed lobes",
                (
                    "Start only after your initial lobe heal is stable — no tenderness, no crust cycles — usually at least 3 months out.",
                    "Tape method: wrap a few layers of non-adhesive stretching tape around your jewelry, reinsert, and let the tissue settle for about a week before adding more. Stop if skin gets angry.",
                    "Full gauge jumps: one size at a time is fine if you stay patient — allow about 1.5× the time your original piercing took to heal before each increase.",
                    "Burning, bleeding, or a ring of thin skin means the jump was too fast — come in before you tear the fistula.",
                ),
            ),
        ),
    },
    "helix": {
        "history": (
            "Helix and other cartilage piercings appear across Indigenous and tribal body-art traditions; "
            "today they are just as often a curated-ear or fashion choice.",
        ),
        "extra_sections": (
            (
                "cartilage-angle",
                "Why cartilage angle matters",
                (
                    "Cartilage has less blood flow than lobe tissue — it heals slower and bumps more easily when jewelry fights the ear's curve.",
                    "I pierce perpendicular to the tissue at the contact point so pressure stays even along the fistula, not straight through on a guess.",
                ),
            ),
        ),
    },
    "nostril": {
        "history": (
            "Nostril piercings carry long roots in South Asia, the Middle East, and North Africa — "
            "often tied to marriage, status, and tradition long before they became a Western fashion staple.",
        ),
        "extra_sections": (
            (
                "nostril-curve",
                "Along the nostril curve",
                (
                    "The nostril is soft tissue over cartilage — too shallow and the stud migrates; too deep and jewelry sits wrong against the natural crease.",
                    "I mark where your nostril curve supports a clean exit, not a generic dot from a photo.",
                ),
            ),
        ),
    },
    "eyebrow": {
        "history": (
            "The eyebrow piercing is newer than most facial work — it emerged in 1970s punk subculture, "
            "crossed into mainstream pop style in the 1990s, and today reads as a unisex accent rather than a counterculture signal.",
        ),
        "extra_sections": (
            (
                "eyebrow-placement",
                "Placement along the brow",
                (
                    "Vertical placements along the brow ridge are the most common — one stud or a deliberate series when anatomy and hair line allow.",
                    "Horizontal placements above, below, or through the brow line are an option when we can mark safely around superficial veins.",
                    "You do not need to shave or trim brows — I pierce through whatever hair you have. Thicker hair at the center can mean more drainage during heal, so extra saline patience there.",
                ),
            ),
        ),
    },
    "labret": {
        "extra_sections": (
            (
                "needle-vs-punch",
                "Needle vs larger gauge vs dermal punch",
                (
                    "Standard needle piercings part the skin — tissue stays in place, which makes downsizing easier if you change your mind about a large look.",
                    "A larger-gauge needle for the initial piercing is an option with an experienced piercer; expect a longer heal than a standard 14G or 16G start.",
                    "Dermal punches remove a circle of flesh outright — instant size, but more scarring if you retire the piercing and harder to scale down later. I recommend needle technique unless we discuss a specific medical or aesthetic plan at consult.",
                ),
            ),
            (
                "labret-jewelry-styles",
                "Which lip jewelry fits your goal",
                (
                    "Flat-back labret studs are the default starter — long enough for swelling, then downsized to protect teeth and gums.",
                    "Captive rings and circular barbells are usually a healed-jewelry choice; a ring large enough to clear day-one swelling tends to stick straight out and snag.",
                    "Tell me if you want a ring aesthetic long-term — we can mark placement and gauge with that end goal in mind.",
                ),
            ),
        ),
    },
}


def _apply_workbook_supplements(slug_id: str, base: EncyclopediaSections) -> EncyclopediaSections:
    patch = _WORKBOOK_SUPPLEMENTS.get(slug_id)
    if not patch:
        return base
    return replace(
        base,
        history=tuple(patch.get("history", ())) or base.history,
        extra_sections=tuple(patch.get("extra_sections", ())) or base.extra_sections,
    )


def complete_sections_for(slug_id: str, name: str) -> EncyclopediaSections:
    base = sections_for(slug_id, name)
    if slug_id == "industrial":
        base = _industrial(name, base)
    else:
        base = _default_complete(slug_id, name, base)
    return _apply_workbook_supplements(slug_id, base)
