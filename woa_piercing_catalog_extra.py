#!/usr/bin/env python3
"""Additional piercing encyclopedia entries — compact specs expanded at build time."""

from __future__ import annotations

from woa_piercing_authority import (
    DOWNSIZE,
    IMPLANT,
    VEGAS_DRY,
    PiercingGuide,
)

_EXTRA: list[tuple] = [
    (
        "ear",
        "Ear Piercing",
        "ear",
        True,
        "Varies by placement — lobe 6–8 weeks, cartilage 6–12 months",
        3,
        "Varies — lobe is mild, cartilage is moderate",
        (
            "Ear piercing is an umbrella term — lobe, helix, conch, tragus, and daith all heal differently. "
            "I built separate guides for each placement because ear piercing aftercare is not one-size-fits-all."
        ),
        ("ear_lobe", "helix", "ear_curation"),
    ),
    (
        "upper_lobe",
        "Upper Lobe",
        "ear",
        True,
        "8–10 weeks; wait 3 months before heavy hoops",
        3,
        "Similar to standard lobe — quick pinch",
        (
            "Upper lobe sits above the standard lobe hole — popular for stacked lobe looks and curated ears. "
            "Spacing from your first lobe hole matters if you plan a full constellation later."
        ),
        ("ear_lobe", "helix", "ear_curation"),
    ),
    (
        "anti_tragus",
        "Anti-Tragus",
        "ear",
        True,
        "9–12 months",
        7,
        "Firm — thick cartilage opposite the tragus",
        (
            "Anti-tragus sits on the cartilage ridge opposite the tragus — anatomy-dependent and not every ear "
            "has enough tissue. I assess the ridge before we commit."
        ),
        ("tragus", "conch", "helix"),
    ),
    (
        "snug",
        "Snug",
        "ear",
        True,
        "9–12 months — anatomy consult required",
        8,
        "Firm — inner rim cartilage",
        (
            "The snug runs along the inner rim of the ear — one of the more advanced cartilage placements. "
            "Curved barbells fit the fold; shallow anatomy means I may recommend an alternative."
        ),
        ("rook", "daith", "helix"),
    ),
    (
        "orbital",
        "Orbital",
        "ear",
        True,
        "9–12 months",
        7,
        "Two piercings connected by one ring",
        (
            "An orbital connects two holes with one ring — often conch-to-helix or lobe-to-helix. "
            "Both holes must heal together; I pierce with a ring sized for swelling or use a bar first."
        ),
        ("conch", "helix", "industrial"),
    ),
    (
        "nose",
        "Nose Piercing",
        "facial",
        True,
        "Varies — nostril 4–6 months, septum 6–8 weeks initial",
        4,
        "Varies by placement — nostril pinch, septum eyes water",
        (
            "Nose piercing covers nostril, high nostril, and septum — each has its own anatomy and heal clock. "
            "Read the specific guide for the placement you want before booking."
        ),
        ("nostril", "septum", "high_nostril"),
    ),
    (
        "high_nostril",
        "High Nostril",
        "facial",
        True,
        "6–9 months",
        5,
        "Moderate — higher on the nostril curve",
        (
            "High nostril sits above the standard nostril sweet spot — subtle and anatomy-specific. "
            "I mark for your nostril shape and check symmetry with standard nostril piercings if you have them."
        ),
        ("nostril", "septum", "nose"),
    ),
    (
        "lip",
        "Lip Piercing",
        "facial",
        True,
        "Varies — labret 2–4 months, vertical labret longer",
        5,
        "Moderate — lip tissue swells",
        (
            "Lip piercing includes labret, vertical labret, Monroe, and snake bites — oral-adjacent work with "
            "tooth and gum considerations. Each variant has its own guide."
        ),
        ("labret", "philtrum", "monroe"),
    ),
    (
        "vertical_labret",
        "Vertical Labret",
        "facial",
        True,
        "3–4 months",
        6,
        "Moderate to sharp — exits through lip surface",
        (
            "Vertical labret enters and exits on the lip without contacting teeth — different heal than standard labret. "
            "I check lip thickness and tooth clearance at consult."
        ),
        ("labret", "philtrum", "snake_bites"),
    ),
    (
        "monroe",
        "Monroe",
        "facial",
        True,
        "2–4 months",
        5,
        "Moderate pinch on upper lip area",
        (
            "Monroe piercings sit off-center above the upper lip — named for the beauty mark look. "
            "Makeup and skincare must stay off the entry during heal."
        ),
        ("philtrum", "labret", "lip"),
    ),
    (
        "snake_bites",
        "Snake Bites",
        "facial",
        True,
        "2–4 months per side; staged or paired on consult",
        5,
        "Moderate — two labret-style piercings",
        (
            "Snake bites are paired lower-lip piercings — symmetry and spacing matter. "
            "I often pierce one side first so you can eat and heal, then add the second."
        ),
        ("labret", "vertical_labret", "lip"),
    ),
    (
        "nipple",
        "Nipple",
        "body",
        True,
        "6–12 months; consult required",
        7,
        "Firm — sensitive tissue",
        (
            "Nipple piercings are appointment-first with a private consult — anatomy, bar length, and aftercare "
            "are discussed before we schedule. Proper jewelry fit is required."
        ),
        ("navel", "surface"),
    ),
]


def _make(spec: tuple) -> PiercingGuide:
    slug_id, name, cat, offered, heal, pain, pain_label, intro, related = spec
    return PiercingGuide(
        slug_id=slug_id,
        name=name,
        category=cat,
        offered=offered,
        offer_note="Yes — book with Katelyn Cole" if offered else "No",
        healing_time=heal,
        pain_score=pain,
        pain_label=pain_label,
        intro=intro,
        quirks=(
            f"{name} has placement-specific quirks — see sleeping, migration, and desert sections below.",
            "Anatomy-first marking — I decline when tissue cannot support a safe angle.",
        ),
        tips=(
            f"I use clean technique and properly fitted starter jewelry for every {name.lower()}.",
            DOWNSIZE,
            "Saline mist — no twisting the jewelry during heal.",
        ),
        jewelry_notes=IMPLANT,
        aftercare_summary=f"Saline cleaning, downsizing on schedule, desert-climate awareness. {VEGAS_DRY}",
        faqs=(
            (
                f"Does Work of Art offer {name.lower()} piercing in Las Vegas?",
                f"Yes — Katelyn Cole performs {name.lower()} piercings at our Tropicana studio by appointment.",
            ),
        ),
        related=related,
    )


PIERCING_CATALOG_EXTRA: tuple[PiercingGuide, ...] = tuple(_make(s) for s in _EXTRA)
