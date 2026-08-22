#!/usr/bin/env python3
"""Piercing pillar + cluster architecture — one maintained page per topic."""

from __future__ import annotations

from dataclasses import dataclass

from woa_piercing_authority import HUB_SLUG

# Overview slugs are index-only — content lives on pillars and placement guides.
SKIP_STANDALONE_CLUSTER = frozenset({"ear", "nose", "lip", "cartilage"})

ORAL_SLUGS = frozenset(
    {
        "lip",
        "labret",
        "vertical_labret",
        "philtrum",
        "monroe",
        "snake_bites",
        "tongue",
    }
)

FACIAL_SLUGS = frozenset(
    {
        "nostril",
        "high_nostril",
        "septum",
        "bridge",
        "eyebrow",
        "anti_eyebrow",
        "nose",
    }
)

EAR_SLUGS = frozenset(
    {
        "ear",
        "ear_lobe",
        "upper_lobe",
        "helix",
        "forward_helix",
        "flat",
        "conch",
        "tragus",
        "anti_tragus",
        "daith",
        "rook",
        "snug",
        "industrial",
        "orbital",
        "ear_curation",
        "cartilage",
    }
)

BODY_SLUGS = frozenset({"navel", "nipple", "surface"})


@dataclass(frozen=True)
class PiercingPillar:
    slug: str
    title: str
    meta_description: str
    intro: str
    body_paragraphs: tuple[str, ...]
    cluster_filter: str  # ear | facial | oral | body | all | none
    related_pillars: tuple[tuple[str, str], ...]  # label, path


PILLARS: tuple[PiercingPillar, ...] = (
    PiercingPillar(
        slug=HUB_SLUG,
        title="Complete Piercing Guide — Las Vegas",
        meta_description=(
            "Work of Art piercing guide — every placement, healing timeline, "
            "jewelry standards, desert aftercare, and advice from Katelyn Cole."
        ),
        intro=(
            "This is our piercing guide hub for Las Vegas — not a keyword list. "
            "Every placement has its own page. Pillars below organize ear, facial, oral, "
            "and body work; aftercare, healing, and jewelry each have a maintained guide."
        ),
        body_paragraphs=(
            "We built this because a helix piercing and a tongue piercing do not heal the same way — "
            "and Vegas dry air changes both. Generic mall advice fails here.",
            "Start with the pillar that matches your placement, then read the specific guide before you book. "
            "Each page follows the same structure so you know exactly what to expect.",
        ),
        cluster_filter="all",
        related_pillars=(
            ("Ear piercing guide", "/ear_piercing_guide_las_vegas/"),
            ("Piercing aftercare", "/piercing_aftercare_guide_las_vegas/"),
            ("Jewelry guide", "/piercing_jewelry_guide_las_vegas/"),
        ),
    ),
    PiercingPillar(
        slug="ear_piercing_guide_las_vegas",
        title="Ear Piercing Guide — Las Vegas",
        meta_description=(
            "Ear piercing guide — lobe, helix, conch, tragus, daith, industrial, "
            "and curated ears. Healing, pain, jewelry, and desert aftercare from Katelyn Cole."
        ),
        intro=(
            "Ear piercing is not one procedure — lobe, upper lobe, helix, conch, tragus, daith, rook, "
            "snug, industrial, and orbital each heal on different timelines with different sleep rules. "
            "This pillar links every ear placement guide we publish."
        ),
        body_paragraphs=(
            "The most common mistake I see is stacking cartilage before the first hole downsizes — "
            "that is how bumps happen in Vegas heat when long posts catch on pillows.",
            "Curated ears start with a consult map, not a walk-in stack. We mark standing and sitting "
            "because your anatomy shifts; spacing decided now saves migration later.",
        ),
        cluster_filter="ear",
        related_pillars=(
            ("Complete piercing guide", f"/{HUB_SLUG}/"),
            ("Piercing healing guide", "/piercing_healing_guide_las_vegas/"),
            ("Ear curation consult", "/appointments/"),
        ),
    ),
    PiercingPillar(
        slug="facial_piercing_guide_las_vegas",
        title="Facial Piercing Guide — Las Vegas",
        meta_description=(
            "Nostril, high nostril, septum, bridge, and eyebrow piercing guides — "
            "healing, pain, jewelry, and anatomy-first marking in Las Vegas."
        ),
        intro=(
            "Facial piercings live where you wash, apply sunscreen, and sleep on your side. "
            "Angle and jewelry length matter more than the trend photo you saved."
        ),
        body_paragraphs=(
            "I mark nostril work at 90 degrees to tissue — not parallel to the face. "
            "Bridge and high nostril carry higher migration risk; I decline when anatomy cannot support a fair heal.",
            "Keep makeup and SPF off fresh entries. Desert AC dries nasal crusties — saline mist, never picking.",
        ),
        cluster_filter="facial",
        related_pillars=(
            ("Complete piercing guide", f"/{HUB_SLUG}/"),
            ("Oral piercing guide", "/oral_piercing_guide_las_vegas/"),
            ("Desert aftercare", "/piercing_aftercare_desert_climate_las_vegas_expert_guide/"),
        ),
    ),
    PiercingPillar(
        slug="oral_piercing_guide_las_vegas",
        title="Oral Piercing Guide — Las Vegas",
        meta_description=(
            "Tongue, labret, philtrum, monroe, and lip piercing guides — downsizing timelines, "
            "swelling, and tooth-safe jewelry from master piercer Katelyn Cole."
        ),
        intro=(
            "Oral piercings swell predictably — tongue peaks day two, lips day one through four. "
            "Starter jewelry is long on purpose; downsizing is not optional."
        ),
        body_paragraphs=(
            "The most common mistake with tongue piercings is skipping the downsizing appointment — "
            "long bars chip teeth once swelling drops.",
            "No kissing, no oral contact, no smoking during heal. Dehydration from Vegas heat makes "
            "oral crusties worse — water and saline rinse after meals.",
        ),
        cluster_filter="oral",
        related_pillars=(
            ("Complete piercing guide", f"/{HUB_SLUG}/"),
            ("Facial piercing guide", "/facial_piercing_guide_las_vegas/"),
            ("Piercing healing guide", "/piercing_healing_guide_las_vegas/"),
        ),
    ),
    PiercingPillar(
        slug="body_piercing_guide_las_vegas",
        title="Body Piercing Guide — Las Vegas",
        meta_description=(
            "Navel and nipple piercing guides — anatomy assessment, healing, rejection signs, "
            "and private consults at Work of Art Las Vegas."
        ),
        intro=(
            "Body piercings need anatomy that can support a fair heal — inverted navels and shallow "
            "nipple tissue are consult-first, not walk-in."
        ),
        body_paragraphs=(
            "Navel rejection is common industry-wide when the lip is wrong — I would rather say no "
            "than leave you with a scar.",
            "Loose waistbands, compression bras, and pool season in Vegas all fight fresh body work. "
            "Plan heal before Mandalay Bay season.",
        ),
        cluster_filter="body",
        related_pillars=(
            ("Complete piercing guide", f"/{HUB_SLUG}/"),
            ("Piercing aftercare", "/piercing_aftercare_guide_las_vegas/"),
            ("Book private consult", "/appointments/"),
        ),
    ),
    PiercingPillar(
        slug="piercing_aftercare_guide_las_vegas",
        title="Piercing Aftercare Guide — Las Vegas",
        meta_description=(
            "How to clean, sleep, swim, and gym with a fresh piercing in Las Vegas — "
            "saline protocol, desert climate, and when to call your piercer."
        ),
        intro=(
            "Aftercare is not one list for every placement — but the principles are the same: "
            "sterile saline, hands off, downsizing on schedule, and desert-aware choices."
        ),
        body_paragraphs=(
            "Clean with sterile saline mist 1–2 times daily. No alcohol, peroxide, or tea tree oil unless "
            "your piercer tells you otherwise in a check-in.",
            "Vegas adds pool season, dust storms, and dry crusties that tighten overnight. "
            "Our desert piercing aftercare guide goes deeper on swimming, hot tubs, and sunscreen.",
        ),
        cluster_filter="none",
        related_pillars=(
            ("Desert climate aftercare", "/piercing_aftercare_desert_climate_las_vegas_expert_guide/"),
            ("Complete piercing guide", f"/{HUB_SLUG}/"),
            ("Piercing healing timelines", "/piercing_healing_guide_las_vegas/"),
        ),
    ),
    PiercingPillar(
        slug="piercing_jewelry_guide_las_vegas",
        title="Piercing Jewelry Guide — Las Vegas",
        meta_description=(
            "Implant-grade titanium, threadless ends, downsizing, gold vs titanium — "
            "jewelry standards at Work of Art Las Vegas from Katelyn Cole."
        ),
        intro=(
            "Fresh piercings start in implant-grade titanium (ASTM F136) or 316L steel — never mystery metal. "
            "Jewelry length accounts for swelling; downsizing protects the fistula."
        ),
        body_paragraphs=(
            "Butterfly backs trap hair, sweat, and bacteria — flat-back threadless posts heal cleaner on ears.",
            "Gold upgrades come after the fistula stabilizes. Anodized titanium gives color without mystery plating.",
        ),
        cluster_filter="none",
        related_pillars=(
            ("Why I only use implant-grade titanium", "/katelyn_implant_grade_titanium_las_vegas_authority_guide/"),
            ("Threadless jewelry explained", "/katelyn_threadless_jewelry_las_vegas_authority_guide/"),
            ("Gold vs titanium", "/katelyn_gold_vs_titanium_las_vegas_authority_guide/"),
            ("Studio jewelry standards", "/best_piercing_shop_las_vegas_updated_jewelry_standards/"),
        ),
    ),
    PiercingPillar(
        slug="piercing_healing_guide_las_vegas",
        title="Piercing Healing Guide — Las Vegas",
        meta_description=(
            "Piercing healing times by placement — lobe vs cartilage vs oral vs body, "
            "downsizing schedules, and what healed actually looks like."
        ),
        intro=(
            "Healed means the fistula is stable — not just when it looks fine in the mirror. "
            "Timelines below are honest ranges from my chair, not mall-kiosk promises."
        ),
        body_paragraphs=(
            "Lobe: 6–8 weeks baseline. Upper lobe: 8–10 weeks. Cartilage: 6–12 months. "
            "Oral: downsizing at 2–6 weeks, full heal 2–4 months. Navel/nipple: 6–12 months.",
            "Swelling, bumps, and migration are different problems — the placement guide for your piercing "
            "explains which is which and when to call me.",
        ),
        cluster_filter="none",
        related_pillars=(
            ("Complete piercing guide", f"/{HUB_SLUG}/"),
            ("Desert aftercare", "/piercing_aftercare_desert_climate_las_vegas_expert_guide/"),
            ("Downsizing jewelry", "/katelyn_downsizing_jewelry_las_vegas_authority_guide/"),
        ),
    ),
)


def pillar_for_slug_id(slug_id: str) -> PiercingPillar:
    if slug_id in EAR_SLUGS:
        return next(p for p in PILLARS if p.slug == "ear_piercing_guide_las_vegas")
    if slug_id in ORAL_SLUGS:
        return next(p for p in PILLARS if p.slug == "oral_piercing_guide_las_vegas")
    if slug_id in FACIAL_SLUGS:
        return next(p for p in PILLARS if p.slug == "facial_piercing_guide_las_vegas")
    if slug_id in BODY_SLUGS:
        return next(p for p in PILLARS if p.slug == "body_piercing_guide_las_vegas")
    return next(p for p in PILLARS if p.slug == HUB_SLUG)


def pillar_by_slug(slug: str) -> PiercingPillar | None:
    for p in PILLARS:
        if p.slug == slug:
            return p
    return None
