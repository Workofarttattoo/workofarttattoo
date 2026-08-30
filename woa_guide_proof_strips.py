#!/usr/bin/env python3
"""Five-frame heal proof strips for authority guides — close-up through swelling."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass

GALLERY = "studio_gallery"
PORTFOLIO = "home_work_of_art_tattoo_piercing/client-portfolio"
HUB = "healed_tattoo_gallery_las_vegas"
BEFORE_AFTER = "tattoo_healing_before_after_real_results"
COVER = "cover-up-tattoos-las-vegas"

# studio_gallery image stems (without extension)
IMG = {
    "helix_close": "helix-and-starburst-lobe-piercings-f002f0c4",
    "helix_curated": "curated-helix-tragus-lobe-piercings-88475d3e",
    "flat_conch_fresh": "flat-and-conch-cartilage-studs-c317138a",
    "industrial_fresh": "fresh-upper-cartilage-industrial-bar-2e41fc98",
    "industrial_healed": "industrial-bar-and-gold-hoop-a704b2d4",
    "ear_healed": "ear-piercing-healed-result-0f5998be",
    "jewelry_change": "jewelry-upgrade-86d3f26f",
    "ear_session": "ear-piercing-in-studio-69c261af",
    "ear_lobe_session": "ear-lobe-piercing-session-da19eec5",
    "ear_curation": "ear-curation-work-eb7d2939",
    "triple_flat_setup": "triple-flat-conch-lobe-ear-setup-f28e160a",
    "conch_smile": "conch-and-lobe-piercing-smile-f1da8b6f",
    "body_healed": "spiked-septum-and-chest-ornament-b09080b0",
    "lobe_fresh": "matching-bilateral-earlobe-piercings-2455fd61",
    "nostril": "nostril-stud-on-smiling-client-dd626b1d",
    "septum_session": "septum-piercing-session-in-studio-07aad378",
    "facial_curated": "curated-facial-piercing-jewelry-display-7d759759",
    "facial_work": "facial-piercing-work-c65aaed1",
    "labret_close": "labret-and-eyebrow-piercing-closeup-c6159742",
    "septum_client": "client-portrait-with-septum-piercings-3f1329cc",
    "body_work": "body-piercing-work-c611f77c",
    "piercing_prep": "piercing-session-prep-b525678d",
    "piercing_setup": "piercing-setup-in-studio-6ab88a11",
    "fine_line_ankle": "fine-line-ankle-tattoos-trio-ee57f2a6",
    "fine_line_werewolf": "fine-line-howling-werewolf-ankle-7ea2af20",
    "script_roses": "beauty-script-roses-inner-forearm-195a396a",
    "lion_healed": "black-grey-lion-thigh-realism-las-vegas",
    "lion_fresh": "fresh-roaring-lion-thigh-black-grey-joshua-cole-las-vegas",
    "lion_healed_3mo": "healed-3-month-roaring-lion-thigh-joshua-cole-las-vegas",
    "eye_fresh": "fresh-all-seeing-eye-triangle-forearm-joshua-cole-las-vegas",
    "cross_healed_1yr": "healed-1-year-cross-eye-skull-outer-forearm-joshua-cole-las-vegas",
    "eagle_fresh": "eagle-memorial-calf-fresh-tattoo-las-vegas",
    "eagle_comparison": "eagle-memorial-calf-fresh-vs-healed-comparison-las-vegas",
    "skull_fresh": "skull-hourglass-forearm-realism-fresh-las-vegas",
    "cover_sunflower_fresh": "cover-up-tattoo-sunflower-over-black-ink-las-vegas",
    "cover_before_hand": "cover-up-tattoo-faded-butterflies-hand-before",
    "cover_healed_chain": "healed-black-grey-chain-heart-tattoo",
    "cover_healed_wings": "healed-realism-seraphim-eye-wings-tattoo",
}


@dataclass(frozen=True)
class ProofFrame:
    label: str
    caption: str
    stem: str
    folder: str = GALLERY


@dataclass(frozen=True)
class GuideProofStrip:
    placement: str
    intro: str
    frames: tuple[ProofFrame, ProofFrame, ProofFrame, ProofFrame, ProofFrame]
    kind: str = "tattoo"


def _p(stem: str, folder: str = GALLERY) -> tuple[str, str]:
    return stem, folder


def piercing_strip(
    placement: str,
    *,
    close: tuple[str, str],
    week1: tuple[str, str],
    month2: tuple[str, str],
    jewelry: tuple[str, str] | None = None,
    swelling: tuple[str, str] | None = None,
    close_caption: str | None = None,
    week1_caption: str | None = None,
    month2_caption: str | None = None,
    jewelry_caption: str | None = None,
    swelling_caption: str | None = None,
) -> GuideProofStrip:
    jew = jewelry or _p(IMG["jewelry_change"])
    swell = swelling or week1
    return GuideProofStrip(
        placement=placement,
        intro=(
            f"Real {placement.lower()} work from our studio — not stock photos. "
            "Starter length, swelling room, downsizing, and healed angles documented in Vegas."
        ),
        kind="piercing",
        frames=(
            ProofFrame(
                f"{placement} close-up",
                close_caption
                or f"Placement and angle marked for your anatomy — starter jewelry sized for swelling.",
                close[0],
                close[1],
            ),
            ProofFrame(
                "Healing week 1",
                week1_caption
                or "Days 3–7: light crusties, tenderness, and a longer post on purpose — do not shorten jewelry at home.",
                week1[0],
                week1[1],
            ),
            ProofFrame(
                "Healing month 2",
                month2_caption
                or "Around 6–8 weeks swelling drops — this is when downsizing protects the angle and prevents bumps.",
                month2[0],
                month2[1],
            ),
            ProofFrame(
                "Jewelry change",
                jewelry_caption
                or "Downsize to a shorter post or swap ends once the fistula is stable — booked as a check-in, not a mall kiosk.",
                jew[0],
                jew[1],
            ),
            ProofFrame(
                "Swelling example",
                swelling_caption
                or "Starter jewelry sits long so tissue is not pulled inward — embedding happens when posts are too short too soon.",
                swell[0],
                swell[1],
            ),
        ),
    )


def tattoo_strip(
    style: str,
    *,
    close: tuple[str, str],
    week1: tuple[str, str],
    month2: tuple[str, str],
    settled: tuple[str, str],
    fresh_redness: tuple[str, str],
    close_caption: str | None = None,
    week1_caption: str | None = None,
    month2_caption: str | None = None,
    settled_caption: str | None = None,
    fresh_redness_caption: str | None = None,
) -> GuideProofStrip:
    return GuideProofStrip(
        placement=style,
        intro=(
            f"Real {style.lower()} from Joshua Cole's chair — fresh redness, peel stage, and settled heal "
            "photographed in-studio. Desert sun changes the timeline; these are honest reference frames."
        ),
        kind="tattoo",
        frames=(
            ProofFrame(
                f"{style} close-up",
                close_caption
                or "Detail at bandage-off — values and line weight before the epidermis sheds.",
                close[0],
                close[1],
            ),
            ProofFrame(
                "Healing week 1",
                week1_caption
                or "Days 4–10: light peel, tight skin, and redness at the edges — normal, not infection.",
                week1[0],
                week1[1],
            ),
            ProofFrame(
                "Healing month 2",
                month2_caption
                or "Weeks 6–8: surface looks closed while deeper layers still settle — contrast softens slightly.",
                month2[0],
                month2[1],
            ),
            ProofFrame(
                "Settled heal",
                settled_caption
                or "Months 3+ — readable at arm's length; blacks stay anchored, color mellows to a matte finish.",
                settled[0],
                settled[1],
            ),
            ProofFrame(
                "Fresh redness",
                fresh_redness_caption
                or "Day 0–3 inflammation and plasma sheen — colors read brightest before the skin rebuilds.",
                fresh_redness[0],
                fresh_redness[1],
            ),
        ),
    )


# Category defaults for ear / facial / oral / body piercings
_EAR = piercing_strip(
    "Ear piercing",
    close=_p(IMG["helix_curated"]),
    week1=_p(IMG["triple_flat_setup"]),
    month2=_p(IMG["ear_healed"]),
    swelling=_p(IMG["flat_conch_fresh"]),
    week1_caption="Fresh cartilage or lobe — starter studs with extra post length for swelling.",
    swelling_caption="Flat and conch starters sit long on purpose — shortening too soon causes embedding and bumps.",
)

_FACIAL = piercing_strip(
    "Facial piercing",
    close=_p(IMG["nostril"]),
    week1=_p(IMG["facial_work"]),
    month2=_p(IMG["facial_curated"]),
    jewelry=_p(IMG["facial_curated"]),
    swelling=_p(IMG["labret_close"]),
    week1_caption="Days 3–7: tenderness around nostril, eyebrow, or bridge — keep hands off and saline only.",
    month2_caption="Healed facial work — shorter posts and decorative ends once swelling is gone.",
)

_ORAL = piercing_strip(
    "Oral piercing",
    close=_p(IMG["labret_close"]),
    week1=_p(IMG["labret_close"]),
    month2=_p(IMG["facial_curated"]),
    jewelry=_p(IMG["facial_curated"]),
    swelling=_p(IMG["labret_close"]),
    week1_caption="Fresh labret, philtrum, or tongue — long flat-back post sized for oral swelling.",
    month2_caption="Downsizing window — shorter post once swelling drops, usually 2–6 weeks for oral piercings.",
    jewelry_caption="Decorative ends and shorter posts once healed — booked as a check-in, not a mall kiosk.",
    swelling_caption="Oral piercings swell fast — long starter posts protect teeth and gums until downsizing.",
)

_BODY = piercing_strip(
    "Body piercing",
    close=_p(IMG["body_work"]),
    week1=_p(IMG["piercing_prep"]),
    month2=_p(IMG["body_healed"]),
    jewelry=_p(IMG["body_work"]),
    swelling=_p(IMG["piercing_prep"]),
    week1_caption="Sterile prep and marking before navel, nipple, or surface work — longer bar on purpose.",
    month2_caption="Months in — jewelry stable and irritation resolved with proper aftercare and downsizing.",
    jewelry_caption="Bar length or decorative ends swapped once healed — navel and nipple need a booked check-in.",
    swelling_caption="Navel and nipple bars start long — embedding happens when jewelry is shortened too soon.",
)

# Placement-specific overrides (slug_id → strip)
PIERCING_STRIPS: dict[str, GuideProofStrip] = {
    "helix": piercing_strip(
        "Helix",
        close=_p(IMG["helix_close"]),
        week1=_p(IMG["helix_curated"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["flat_conch_fresh"]),
    ),
    "forward_helix": piercing_strip(
        "Forward helix",
        close=_p(IMG["helix_curated"]),
        week1=_p(IMG["flat_conch_fresh"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["industrial_fresh"]),
    ),
    "flat": piercing_strip(
        "Flat",
        close=_p(IMG["flat_conch_fresh"]),
        week1=_p(IMG["helix_curated"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["flat_conch_fresh"]),
    ),
    "conch": piercing_strip(
        "Conch",
        close=_p(IMG["flat_conch_fresh"]),
        week1=_p(IMG["helix_curated"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["industrial_fresh"]),
    ),
    "tragus": piercing_strip(
        "Tragus",
        close=_p(IMG["helix_curated"]),
        week1=_p(IMG["flat_conch_fresh"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["flat_conch_fresh"]),
    ),
    "daith": piercing_strip(
        "Daith",
        close=_p(IMG["helix_curated"]),
        week1=_p(IMG["flat_conch_fresh"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["industrial_fresh"]),
    ),
    "rook": piercing_strip(
        "Rook",
        close=_p(IMG["helix_curated"]),
        week1=_p(IMG["flat_conch_fresh"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["industrial_fresh"]),
    ),
    "snug": piercing_strip(
        "Snug",
        close=_p(IMG["helix_curated"]),
        week1=_p(IMG["flat_conch_fresh"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["industrial_fresh"]),
    ),
    "anti_tragus": piercing_strip(
        "Anti-tragus",
        close=_p(IMG["helix_curated"]),
        week1=_p(IMG["flat_conch_fresh"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["industrial_fresh"]),
    ),
    "industrial": piercing_strip(
        "Industrial",
        close=_p(IMG["industrial_fresh"]),
        week1=_p(IMG["industrial_fresh"]),
        month2=_p(IMG["industrial_healed"]),
        swelling=_p(IMG["industrial_fresh"]),
        swelling_caption="Industrial bars start long — both holes need swelling room before you shorten the bar.",
    ),
    "orbital": piercing_strip(
        "Orbital",
        close=_p(IMG["helix_curated"]),
        week1=_p(IMG["flat_conch_fresh"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["industrial_fresh"]),
    ),
    "ear_lobe": piercing_strip(
        "Lobe",
        close=_p(IMG["lobe_fresh"]),
        week1=_p(IMG["ear_lobe_session"]),
        month2=_p(IMG["conch_smile"]),
        swelling=_p(IMG["lobe_fresh"]),
        month2_caption="Healed lobes — studs sit flush once swelling drops, usually around 6–8 weeks.",
    ),
    "upper_lobe": piercing_strip(
        "Upper lobe",
        close=_p(IMG["lobe_fresh"]),
        week1=_p(IMG["ear_lobe_session"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["lobe_fresh"]),
    ),
    "ear_curation": piercing_strip(
        "Ear curation",
        close=_p(IMG["ear_curation"]),
        week1=_p(IMG["helix_curated"]),
        month2=_p(IMG["ear_healed"]),
        swelling=_p(IMG["flat_conch_fresh"]),
    ),
    "cartilage": _EAR,
    "ear": _EAR,
    "nostril": piercing_strip(
        "Nostril",
        close=_p(IMG["nostril"]),
        week1=_p(IMG["facial_work"]),
        month2=_p(IMG["facial_curated"]),
        swelling=_p(IMG["nostril"]),
    ),
    "high_nostril": piercing_strip(
        "High nostril",
        close=_p(IMG["nostril"]),
        week1=_p(IMG["facial_work"]),
        month2=_p(IMG["facial_curated"]),
        swelling=_p(IMG["nostril"]),
    ),
    "septum": piercing_strip(
        "Septum",
        close=_p(IMG["septum_session"]),
        week1=_p(IMG["septum_client"]),
        month2=_p(IMG["facial_curated"]),
        swelling=_p(IMG["septum_client"]),
    ),
    "bridge": piercing_strip(
        "Bridge",
        close=_p(IMG["facial_curated"]),
        week1=_p(IMG["facial_work"]),
        month2=_p(IMG["facial_curated"]),
        swelling=_p(IMG["labret_close"]),
    ),
    "eyebrow": piercing_strip(
        "Eyebrow",
        close=_p(IMG["labret_close"]),
        week1=_p(IMG["facial_work"]),
        month2=_p(IMG["facial_curated"]),
        swelling=_p(IMG["labret_close"]),
    ),
    "anti_eyebrow": _FACIAL,
    "labret": _ORAL,
    "philtrum": _ORAL,
    "vertical_labret": _ORAL,
    "monroe": _ORAL,
    "smiley": _ORAL,
    "tongue": _ORAL,
    "navel": _BODY,
    "nipple": _BODY,
    "surface": _BODY,
    "nose": _FACIAL,
}

# Tattoo proof strips — fresh/healed pairs from woa_healed_gallery catalog
_BG_TATTOO = tattoo_strip(
    "Realism",
    close=_p(IMG["skull_fresh"], PORTFOLIO),
    week1=_p(IMG["eye_fresh"], HUB),
    month2=_p(IMG["cross_healed_1yr"], HUB),
    settled=_p(IMG["lion_healed_3mo"], HUB),
    fresh_redness=_p(IMG["lion_fresh"], HUB),
)

_COLOR_HEAL = tattoo_strip(
    "Color heal",
    close=_p(IMG["eagle_fresh"], BEFORE_AFTER),
    week1=_p(IMG["eagle_fresh"], BEFORE_AFTER),
    month2=_p(IMG["eagle_comparison"], BEFORE_AFTER),
    settled=_p(IMG["eagle_comparison"], BEFORE_AFTER),
    fresh_redness=_p(IMG["eagle_fresh"], BEFORE_AFTER),
    month2_caption=(
        "Weeks 3–6: color looks dull while deeper layers settle — the healed calf in our comparison "
        "photo shows what stable saturation looks like months later."
    ),
    settled_caption=(
        "Months later — same memorial eagle calves from our fresh vs healed studio documentation; "
        "yellows and oranges mellow to a stable matte finish."
    ),
)

_SKIN_SCIENCE_TATTOO = tattoo_strip(
    "Tattoo skin science",
    close=_p(IMG["eye_fresh"], HUB),
    week1=_p(IMG["eagle_fresh"], BEFORE_AFTER),
    month2=_p(IMG["eagle_comparison"], BEFORE_AFTER),
    settled=_p(IMG["lion_healed_3mo"], HUB),
    fresh_redness=_p(IMG["skull_fresh"], PORTFOLIO),
    close_caption="Fresh tattoo surface detail — the epidermis is irritated while pigment is placed below it.",
    week1_caption="Early tattoo healing reference — surface shine, tightness, and light texture can change how value reads.",
    month2_caption="Fresh vs settled tattoo comparison — useful for explaining how the surface calms while pigment remains.",
    settled_caption="Settled black and grey tattoo detail — healed contrast is what matters for long-term readability.",
    fresh_redness_caption="Day-zero tattoo surface redness — shown as healing context, not as finished portfolio proof.",
)

SKIN_SCIENCE_SLUG_PARTS = (
    "dermis",
    "epidermis",
    "hypodermis",
    "collagen",
    "aging_skin",
    "scar_tissue",
    "macrophages",
    "tattoo_permanence",
    "why_tattoos_stay_forever",
    "eczema",
    "diabetes",
    "psoriasis",
    "stretch_marks",
    "skin_science",
)

# Page slug → strip for tattoo / service guides
PAGE_STRIPS: dict[str, GuideProofStrip] = {
    "realism_tattoos_las_vegas_master_authority_guide": _BG_TATTOO,
    "fine_line_tattoos_las_vegas_master_authority_guide": tattoo_strip(
        "Fine line",
        close=_p(IMG["fine_line_ankle"]),
        week1=_p(IMG["fine_line_werewolf"]),
        month2=_p(IMG["script_roses"]),
        settled=_p(IMG["cross_healed_1yr"], HUB),
        fresh_redness=_p(IMG["eye_fresh"], HUB),
        close_caption="Fine-line ankle tattoos from the studio gallery — scale and spacing are the proof here.",
        week1_caption="Small fine-line ankle work — readable subject matter without packing too much detail into the placement.",
        month2_caption="Script and rose detail — lettering needs enough spacing to stay readable after the skin settles.",
        settled_caption="Settled line-and-shade reference from healed studio documentation.",
        fresh_redness_caption="Fresh tattoo surface detail shown later as healing context, not as the lead fine-line proof.",
    ),
    "cover-up-tattoos-las-vegas": tattoo_strip(
        "Cover-up",
        close=_p(IMG["cover_before_hand"], COVER),
        week1=_p(IMG["cover_sunflower_fresh"], COVER),
        month2=_p(IMG["cover_healed_wings"], COVER),
        settled=_p(IMG["cover_healed_chain"], COVER),
        fresh_redness=_p(IMG["cover_sunflower_fresh"], COVER),
        close_caption="Before photo documented in-studio — faded old work we planned to redesign, not cover with a darker blob.",
        fresh_redness_caption="Fresh cover-up pass in progress — redness and plasma sheen on new color over old ink.",
    ),
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": _BG_TATTOO,
    "tattoo_healing_before_after_real_results": _COLOR_HEAL,
    "las-vegas-tattoo-healing-guide": _COLOR_HEAL,
    "dermis_skin_science_las_vegas_authority_guide": _SKIN_SCIENCE_TATTOO,
    "epidermis_skin_science_las_vegas_authority_guide": _SKIN_SCIENCE_TATTOO,
    "walk_in_tattoos_las_vegas_authority_guide": _BG_TATTOO,
    "best_piercing_shop_las_vegas_updated_jewelry_standards": _EAR,
    "piercing_types_las_vegas_authority_hub": _EAR,
    "ear_piercing_guide_las_vegas": _EAR,
    "facial_piercing_guide_las_vegas": _FACIAL,
    "oral_piercing_guide_las_vegas": _ORAL,
    "body_piercing_guide_las_vegas": _BODY,
    "piercing_jewelry_guide_las_vegas": piercing_strip(
        "Piercing jewelry",
        close=_p(IMG["facial_curated"]),
        week1=_p(IMG["flat_conch_fresh"]),
        month2=_p(IMG["jewelry_change"]),
        jewelry=_p(IMG["jewelry_change"]),
        swelling=_p(IMG["triple_flat_setup"]),
        close_caption="Threadless ends and jewelry options — what we discuss before fresh piercings.",
        week1_caption="Fresh piercings start with longer posts sized for swelling, not fashion length.",
        month2_caption="Healed upgrade — shorter posts and decorative ends once the fistula is stable.",
        jewelry_caption="Downsize and upgrade consult — shorter posts and decorative ends once healed.",
        swelling_caption="Starter length shown on flat and conch — downsizing too early is the most common jewelry mistake.",
    ),
    "piercing-guide-las-vegas": _EAR,
    "piercing_aftercare_desert_climate_las_vegas_expert_guide": _EAR,
}

# Katelyn topic pages — prefix match
KATELYN_TOPIC_DEFAULT = _EAR

SKIP_SLUGS = frozenset(
    {
        "home_work_of_art_tattoo_piercing",
        "artists",
        "appointments",
        "studio_gallery",
        "flash_art_deals_under_100",
        "healed_tattoo_gallery_las_vegas",
        "offsite_bookings",
        "studio_videos",
        "reviews_vault_100_verified_masterpieces",
        "geo_hub_ai_source_of_truth_work_of_art",
        "tattoo_shop_near_the_strip_nap_corrected",
    }
)


def _is_geo_landing(page_slug: str) -> bool:
    if page_slug.startswith("tattoo_shop_near_"):
        return True
    if page_slug.startswith("tattoo_shop_") and page_slug.endswith(
        ("_las_vegas", "_nevada", "_henderson")
    ):
        return True
    return False


def slug_id_from_page_slug(page_slug: str) -> str | None:
    if not page_slug.endswith("_las_vegas_authority_guide"):
        return None
    base = page_slug[: -len("_las_vegas_authority_guide")]
    if base.endswith("_piercing"):
        return base[: -len("_piercing")]
    return base


def strip_for_page(page_slug: str) -> GuideProofStrip | None:
    if page_slug in SKIP_SLUGS or _is_geo_landing(page_slug):
        return None
    if page_slug in PAGE_STRIPS:
        return PAGE_STRIPS[page_slug]
    if any(part in page_slug for part in SKIN_SCIENCE_SLUG_PARTS):
        return _SKIN_SCIENCE_TATTOO
    sid = slug_id_from_page_slug(page_slug)
    if sid and sid in PIERCING_STRIPS:
        return PIERCING_STRIPS[sid]
    if sid:
        return _EAR
    if page_slug.startswith("katelyn_") and page_slug.endswith("_las_vegas_authority_guide"):
        return KATELYN_TOPIC_DEFAULT
    if page_slug.startswith("knowledge_") or page_slug.startswith("knowledge/"):
        return None
    if page_slug.endswith("_authority_guide") or page_slug.endswith("_expert_guide"):
        if any(x in page_slug for x in ("tattoo", "realism", "cover", "fine_line", "walk_in", "sleeve")):
            return _BG_TATTOO
        if "piercing" in page_slug:
            return _EAR
    if page_slug.endswith("_guide") or "guide" in page_slug:
        if "piercing" in page_slug:
            return _EAR
        if "tattoo" in page_slug or "healing" in page_slug:
            return _COLOR_HEAL if "healing" in page_slug or "before_after" in page_slug else _BG_TATTOO
    return None


def picture(frame: ProofFrame, *, placement: str) -> str:
    webp = f"/{frame.folder}/{frame.stem}.webp"
    png = f"/{frame.folder}/{frame.stem}.png"
    alt = html.escape(f"{frame.label} — {placement} — Work of Art Las Vegas")
    return (
        f'<picture><source srcset="{webp}" type="image/webp"/>'
        f'<img alt="{alt}" class="w-full aspect-square object-cover" decoding="async" height="400" '
        f'loading="lazy" src="{png}" width="400"/></picture>'
    )


MARKER = 'data-woa-guide-proof-strip="1"'


def proof_strip_html(page_slug: str) -> str:
    strip = strip_for_page(page_slug)
    if not strip:
        return ""
    cards = []
    for i, frame in enumerate(strip.frames, 1):
        anchor = re.sub(r"[^a-z0-9]+", "-", frame.label.lower()).strip("-")
        cards.append(
            f"""<figure class="space-y-2" id="proof-{anchor}">
{picture(frame, placement=strip.placement)}
<figcaption class="px-1 space-y-1">
<span class="font-label-caps text-secondary text-[10px] uppercase tracking-widest block">{html.escape(frame.label)}</span>
<p class="font-body-md text-on-surface-variant text-sm leading-snug">{html.escape(frame.caption)}</p>
</figcaption>
</figure>"""
        )
    grid = "\n".join(cards)
    is_piercing_strip = strip.kind == "piercing"
    footer = (
        'Photos from Work of Art piercing clients — angles and jewelry length vary by anatomy. '
        '<a class="text-secondary underline" href="/studio_gallery/">Studio gallery</a> · '
        '<a class="text-secondary underline" href="/artists/katelyn-cole/">Katelyn\'s portfolio</a>'
        if is_piercing_strip
        else 'Photos from Work of Art tattoo clients — healing appearance varies by skin, placement, and aftercare. '
        '<a class="text-secondary underline" href="/healed_tattoo_gallery_las_vegas/">Healed tattoo proof</a> · '
        '<a class="text-secondary underline" href="/artists/joshua-cole/">Joshua\'s portfolio</a>'
    )
    return f"""<section class="space-y-6 py-4" {MARKER} id="photos">
<h2 class="font-headline-md text-on-surface text-2xl">Real heal documentation</h2>
<p class="font-body-md text-on-surface-variant">{html.escape(strip.intro)}</p>
<div class="grid grid-cols-2 md:grid-cols-5 gap-4 md:gap-5">
{grid}
</div>
<p class="font-body-md text-on-surface-variant text-sm">{footer}</p>
</section>"""
