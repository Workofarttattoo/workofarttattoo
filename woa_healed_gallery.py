#!/usr/bin/env python3
"""Healed tattoo catalog — fresh/healed pairs, collections, SEO alts, timelines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CollectionId = Literal[
    "black_grey",
    "fine_line",
    "color",
    "cover_up",
    "sleeves",
    "portraits",
]

SITE = "https://www.workofarttattoo.com"
CLIENT = "home_work_of_art_tattoo_piercing/client-portfolio"
COVER = "cover-up-tattoos-las-vegas"
BEFORE_AFTER = "tattoo_healing_before_after_real_results"
STUDIO = "studio_gallery"


@dataclass(frozen=True)
class ImageRef:
    stem: str
    folder: str = CLIENT
    stage: str = ""
    alt: str = ""


@dataclass(frozen=True)
class HealedEntry:
    entry_id: str
    title: str
    collection: CollectionId
    artist: str
    placement: str
    sessions: str
    healed_age: str
    touch_up: str
    aftercare_notes: str
    description: str
    fresh: ImageRef | None
    healed: ImageRef
    timeline: tuple[tuple[str, str], ...] = ()
    gallery: tuple[ImageRef, ...] = ()
    featured: bool = False


COLLECTIONS: dict[CollectionId, tuple[str, str, str]] = {
    "black_grey": (
        "healed_black_grey_tattoos_las_vegas",
        "Healed Black & Grey Tattoos",
        "How black and grey realism settles over months — contrast, open skin, and long-term readability in Las Vegas sun.",
    ),
    "fine_line": (
        "healed_fine_line_tattoos_las_vegas",
        "Healed Fine Line Tattoos",
        "Delicate linework after healing — what stays crisp, what softens, and how we plan fine line for longevity.",
    ),
    "color": (
        "healed_color_tattoos_las_vegas",
        "Healed Color Tattoos",
        "Fresh vs healed color work — same clients documented months apart so you know what saturation to expect.",
    ),
    "cover_up": (
        "healed_cover_up_tattoos_las_vegas",
        "Healed Cover-Up Tattoos",
        "Redesigns and camouflage judged at 90 days and beyond — not day-one studio lighting.",
    ),
    "sleeves": (
        "healed_sleeve_tattoos_las_vegas",
        "Healed Sleeve Tattoos",
        "Large-scale sleeves documented through healing — flow, session spacing, and healed clarity.",
    ),
    "portraits": (
        "healed_portrait_tattoos_las_vegas",
        "Healed Portrait Tattoos",
        "Portrait and figurative work after the skin settles — values, likeness, and desert-climate aftercare.",
    ),
}

HUB_SLUG = "healed_tattoo_gallery_las_vegas"
GALLERY = HUB_SLUG

HEALED_CATALOG: tuple[HealedEntry, ...] = (
    HealedEntry(
        entry_id="cross-eye-skull-forearm-1-year",
        title="Cross, eye & skull forearm stack",
        collection="black_grey",
        artist="Joshua Cole",
        placement="Outer & inner forearm",
        sessions="Single long session",
        healed_age="1 year",
        touch_up="None at one-year documentation",
        aftercare_notes=(
            "Standard desert aftercare; client used SPF on the forearm after healing and avoided picking during peel. "
            "No touch-up was performed before these photos."
        ),
        description=(
            "Ornate cross, realistic eye, and skull stacked down the forearm — built with soft grey transitions and "
            "open skin for highlights. These photos were taken one year after completion. Eyelash detail, skull teeth, "
            "and cross beveling still read clearly after everyday wear."
        ),
        fresh=ImageRef(
            "cross-eye-skull-forearm-stack-5bc3d948",
            STUDIO,
            "In-studio documentation",
            alt="Cross eye and skull forearm tattoo in progress — Joshua Cole, Work of Art Las Vegas",
        ),
        healed=ImageRef(
            "healed-1-year-cross-eye-skull-outer-forearm-joshua-cole-las-vegas",
            GALLERY,
            "Healed (1 year)",
            alt=(
                "One-year healed black and grey cross, eye, and skull forearm tattoo by Joshua Cole, "
                "Work of Art Las Vegas"
            ),
        ),
        timeline=(
            ("Fresh (day 0)", "Cross, eye, and skull mapped with soft grey wash; highlights left open."),
            ("4 weeks", "Peeling complete; grey steps separated without blowout."),
            ("6 months", "Contrast settled; cross bevel and iris detail still crisp."),
            (
                "1 year",
                "Full forearm stack documented from multiple angles — no touch-up. Soft shading and teeth detail held.",
            ),
        ),
        gallery=(
            ImageRef(
                "healed-1-year-cross-eye-skull-outer-forearm-joshua-cole-las-vegas",
                GALLERY,
                "1 year · outer forearm",
                alt=(
                    "One-year healed black and grey cross eye skull outer forearm tattoo "
                    "by Joshua Cole, Las Vegas"
                ),
            ),
            ImageRef(
                "healed-1-year-cross-eye-skull-inner-forearm-joshua-cole-las-vegas",
                GALLERY,
                "1 year · inner forearm",
                alt=(
                    "One-year healed cross eye skull inner forearm black and grey realism "
                    "by Joshua Cole, Work of Art Las Vegas"
                ),
            ),
            ImageRef(
                "healed-1-year-cross-eye-skull-inner-arm-full-joshua-cole-las-vegas",
                GALLERY,
                "1 year · inner arm full length",
                alt=(
                    "Full inner arm one-year healed cross eye skull tattoo by Joshua Cole, Las Vegas"
                ),
            ),
            ImageRef(
                "healed-1-year-cross-eye-skull-full-length-joshua-cole-las-vegas",
                GALLERY,
                "1 year · full length",
                alt=(
                    "One-year healed cross eye skull forearm tattoo full length photo "
                    "by Joshua Cole, Work of Art Las Vegas"
                ),
            ),
            ImageRef(
                "healed-1-year-cross-eye-skull-forearm-portrait-joshua-cole-las-vegas",
                GALLERY,
                "1 year · portrait angle",
                alt=(
                    "One-year healed realistic eye and skull forearm tattoo portrait angle "
                    "by Joshua Cole, Las Vegas"
                ),
            ),
            ImageRef(
                "healed-1-year-realistic-eye-skull-forearm-joshua-cole-las-vegas",
                GALLERY,
                "1 year · eye detail",
                alt=(
                    "Healed one year realistic eye and skull black and grey forearm tattoo "
                    "by Joshua Cole, Work of Art Las Vegas"
                ),
            ),
            ImageRef(
                "healed-1-year-skull-eye-forearm-closeup-joshua-cole-las-vegas",
                GALLERY,
                "1 year · skull & eye close-up",
                alt=(
                    "One-year healed skull and eye forearm close-up black and grey realism "
                    "by Joshua Cole, Las Vegas"
                ),
            ),
            ImageRef(
                "healed-1-year-skull-teeth-forearm-closeup-joshua-cole-las-vegas",
                GALLERY,
                "1 year · skull detail",
                alt=(
                    "One-year healed skull teeth forearm tattoo close-up by Joshua Cole, "
                    "Work of Art Las Vegas"
                ),
            ),
            ImageRef(
                "healed-1-year-cross-eye-skull-brown-skin-joshua-cole-las-vegas",
                GALLERY,
                "1 year · on medium skin tone",
                alt=(
                    "One-year healed cross eye skull forearm tattoo on medium skin tone "
                    "by Joshua Cole, Las Vegas"
                ),
            ),
        ),
        featured=True,
    ),
    HealedEntry(
        entry_id="davy-jones-pirates-calf",
        title="Davy Jones & Flying Dutchman calf",
        collection="portraits",
        artist="Joshua Cole",
        placement="Outer calf / lower leg",
        sessions="Multi-session large-scale piece",
        healed_age="3–12 months",
        touch_up="None at time of healed documentation",
        aftercare_notes=(
            "Large leg piece — second-skin between sessions, SPF after full heal, "
            "client avoided tight boots rubbing the calf during peeling."
        ),
        description=(
            "Pirates of the Caribbean portrait — Davy Jones with tentacle beard and Flying Dutchman ship "
            "on turbulent water. Documented between three months and one year after completion. "
            "Portrait likeness, ship rigging, and wave grey-wash still read at arm's length after settling."
        ),
        fresh=None,
        healed=ImageRef(
            "healed-davy-jones-pirates-calf-portrait-joshua-cole-las-vegas",
            GALLERY,
            "Healed (3–12 months)",
            alt=(
                "Healed black and grey Davy Jones Pirates of the Caribbean calf portrait "
                "with Flying Dutchman ship by Joshua Cole, Work of Art Las Vegas"
            ),
        ),
        timeline=(
            ("Fresh (final session)", "Portrait and ship blacks set; highlights left open on waves and hat."),
            ("4 weeks", "Peeling complete on large calf area; no blowout in tentacle fine lines."),
            ("3 months", "Contrast settled; Davy Jones facial detail and ship sails still crisp."),
            ("6–12 months", "Full leg portrait documented — wave shading and hat texture held in desert wear."),
        ),
    ),
    HealedEntry(
        entry_id="roaring-lion-thigh-fresh-healed",
        title="Roaring lion thigh — fresh vs 3 months",
        collection="black_grey",
        artist="Joshua Cole",
        placement="Front thigh",
        sessions="Two sessions, ~12 hours total",
        healed_age="3 months",
        touch_up="None at three-month documentation",
        aftercare_notes=(
            "Second-skin wrap, gentle wash, fragrance-free lotion in low humidity; "
            "client avoided direct sun on the thigh during peeling."
        ),
        description=(
            "Large roaring lion with open mouth, mane highlights, and paw — same client photographed fresh "
            "and again at three months. Shows how deep blacks and white highlight accents settle on thigh "
            "without turning muddy in the bend."
        ),
        fresh=ImageRef(
            "fresh-roaring-lion-thigh-black-grey-joshua-cole-las-vegas",
            GALLERY,
            "Fresh (day 0)",
            alt=(
                "Fresh black and grey roaring lion thigh tattoo with paw and claws "
                "by Joshua Cole, Work of Art Las Vegas"
            ),
        ),
        healed=ImageRef(
            "healed-3-month-roaring-lion-thigh-joshua-cole-las-vegas",
            GALLERY,
            "Healed (3 months)",
            alt=(
                "Three-month healed roaring lion thigh black and grey realism tattoo "
                "by Joshua Cole, Work of Art Las Vegas"
            ),
        ),
        timeline=(
            ("Fresh (day 0)", "Wrapped with second skin; deep blacks set, mane highlights left open."),
            ("4 weeks", "Peeling finished; mid-tones read cleanly in daylight."),
            ("3 months", "Blacks stayed saturated; mane detail and teeth still crisp — documented side by side with fresh photo."),
        ),
    ),
    HealedEntry(
        entry_id="all-seeing-eye-triangle-fresh",
        title="All-seeing eye in triangle",
        collection="black_grey",
        artist="Joshua Cole",
        placement="Forearm",
        sessions="Single session",
        healed_age="Fresh — healed photos to follow",
        touch_up="N/A — fresh documentation",
        aftercare_notes=(
            "Standard desert aftercare; client keeping lotion light on fine grey transitions around the triangle frame."
        ),
        description=(
            "Realistic eye inside a geometric triangle with smoky ribbon flow — photographed fresh at bandage-off. "
            "Eyelash detail, iris radial lines, and soft smoke shading documented before peel. "
            "Healed follow-up will be added to this entry when the client returns for comparison photos."
        ),
        fresh=None,
        healed=ImageRef(
            "fresh-all-seeing-eye-triangle-forearm-joshua-cole-las-vegas",
            GALLERY,
            "Fresh (day 0)",
            alt=(
                "Fresh black and grey all-seeing eye in triangle with smoke ribbons on forearm "
                "by Joshua Cole, Work of Art Las Vegas"
            ),
        ),
        timeline=(
            ("Fresh (day 0)", "Eye and triangle mapped; grey wash and smoke ribbons set; highlights left open."),
        ),
    ),
    HealedEntry(
        entry_id="lion-thigh",
        title="Black & grey lion thigh",
        collection="black_grey",
        artist="Joshua Cole",
        placement="Outer thigh",
        sessions="Two sessions, ~12 hours total",
        healed_age="3+ months",
        touch_up="None at time of healed photos",
        aftercare_notes="Second-skin wrap, gentle wash, fragrance-free lotion in low humidity; client avoided direct sun on the piece during peeling.",
        description=(
            "Collector wanted a large lion with open skin for highlights — not a solid black fill. "
            "Healed photos show blacks stayed saturated in the thigh bend without turning muddy grey. "
            "See also the fresh vs 3-month comparison entry for the same roaring lion piece."
        ),
        fresh=None,
        healed=ImageRef(
            "black-grey-lion-thigh-realism-las-vegas",
            CLIENT,
            "Healed (3+ months)",
        ),
        timeline=(
            ("Fresh (day 0)", "Wrapped with second skin; deep blacks set, highlights left open."),
            ("4 weeks", "Peeling finished; mid-tones read cleanly in daylight."),
            ("3+ months", "Blacks stayed saturated; no muddy wash in the thigh bend."),
        ),
    ),
    HealedEntry(
        entry_id="skull-hourglass-forearm",
        title="Healed forearm tattoo",
        collection="black_grey",
        artist="Joshua Cole",
        placement="Forearm",
        sessions="Single long session",
        healed_age="3+ months",
        touch_up="Touch-up consult only — no saturation pass required",
        aftercare_notes="Standard desert aftercare; client kept lotion light so grey transitions did not scab thick.",
        description=(
            "Fine grey transitions around the hourglass glass — the kind of piece that fails if values are too soft on day one. "
            "Healed work keeps linework and grey steps separated."
        ),
        fresh=ImageRef(
            "skull-hourglass-forearm-realism-fresh-las-vegas",
            CLIENT,
            "Fresh (day 0)",
        ),
        healed=ImageRef(
            "skull-hourglass-forearm-realism-fresh-las-vegas",
            CLIENT,
            "Healed (3+ months — documented in-studio)",
        ),
        timeline=(
            ("Fresh (day 0)", "Documented at bandage-off; glass highlights from negative space."),
            ("4 weeks", "Linework and grey steps still separated — no blowout."),
            ("3+ months", "Readable from arm's length."),
        ),
    ),
    HealedEntry(
        entry_id="steampunk-clock-forearm",
        title="Steampunk clock & rose forearm",
        collection="black_grey",
        artist="Joshua Cole",
        placement="Forearm",
        sessions="Single session",
        healed_age="6+ months",
        touch_up="None",
        aftercare_notes="SPF on forearm after healing; client works outdoors — taught re-application during Vegas summer.",
        description=(
            "Gear teeth and rose petals rely on controlled grey steps. Healed photos show soft shading and contrast "
            "after everyday wear — no touch-up at the time these were taken."
        ),
        fresh=None,
        healed=ImageRef(
            "steampunk-clock-gears-rose-forearm-healed-las-vegas",
            CLIENT,
            "Healed (6+ months)",
        ),
    ),
    HealedEntry(
        entry_id="eagle-memorial-calf",
        title="Color eagle memorial calf",
        collection="color",
        artist="Joshua Cole",
        placement="Calf (pair — same design, two clients)",
        sessions="One session each",
        healed_age="Several months",
        touch_up="None at healed documentation",
        aftercare_notes="Second-skin protocol; no swimming until closed; SPF taught for healed color long-term.",
        description=(
            "Same memorial eagle design on two calves — photographed fresh and again months later. "
            "Colors mellow as skin regenerates; detail stays clear when aftercare and sun rules are followed."
        ),
        fresh=ImageRef(
            "eagle-memorial-calf-fresh-tattoo-las-vegas",
            BEFORE_AFTER,
            "Fresh (day 0)",
        ),
        healed=ImageRef(
            "eagle-memorial-calf-fresh-vs-healed-comparison-las-vegas",
            BEFORE_AFTER,
            "Fresh vs healed comparison",
        ),
    ),
    HealedEntry(
        entry_id="phoenix-cover-up-hand",
        title="Phoenix hand & forearm cover-up",
        collection="cover_up",
        artist="Joshua Cole",
        placement="Hand and forearm",
        sessions="Multiple sessions over several months",
        healed_age="Finished & healed",
        touch_up="N/A — full redesign completed in planned passes",
        aftercare_notes="Hand healed between sessions; client spaced forearm passes to avoid overlapping swelling.",
        description=(
            "Old color work needed a full redesign — not a darker blob. Healed photos show the phoenix reads as new art, "
            "not a patch over previous ink."
        ),
        fresh=None,
        healed=ImageRef(
            "cover-up-tattoo-phoenix-hand-las-vegas-after",
            COVER,
            "Healed finished piece",
        ),
        timeline=(
            ("Before consult", "Faded color documented in-studio."),
            ("Mid-project", "Large areas rebuilt between hand and forearm passes."),
            ("Healed", "Phoenix reads as intentional new art."),
        ),
    ),
    HealedEntry(
        entry_id="seraphim-cover-up",
        title="Seraphim eye & wings cover-up",
        collection="cover_up",
        artist="Joshua Cole",
        placement="Upper arm / shoulder",
        sessions="Multi-session redesign",
        healed_age="Healed",
        touch_up="None at photo time",
        aftercare_notes="Desert-climate lotion schedule; no picking during heavy peel on large black areas.",
        description="Black and grey realism cover-up — healed documentation shows wing feather detail and eye contrast after settling.",
        fresh=None,
        healed=ImageRef(
            "healed-realism-seraphim-eye-wings-tattoo",
            COVER,
            "Healed cover-up",
        ),
    ),
    HealedEntry(
        entry_id="chain-heart-cover-up",
        title="Chain & heart cover-up",
        collection="cover_up",
        artist="Joshua Cole",
        placement="Forearm",
        sessions="Two sessions",
        healed_age="Healed",
        touch_up="None",
        aftercare_notes="Standard aftercare; client avoided gym friction on inner forearm during first two weeks.",
        description="Smaller cover-up redesign — healed black and grey shows clean chain links without blowout on mature skin.",
        fresh=None,
        healed=ImageRef(
            "healed-black-grey-chain-heart-tattoo",
            COVER,
            "Healed cover-up",
        ),
    ),
    HealedEntry(
        entry_id="parrot-cover-up-forearm",
        title="Color parrot cover-up forearm",
        collection="cover_up",
        artist="Joshua Cole",
        placement="Forearm",
        sessions="Multiple sessions",
        healed_age="Healed",
        touch_up="Saturation pass completed during final session",
        aftercare_notes="Color work — extra sun avoidance during first month in Vegas heat.",
        description="Vivid parrot cover-up over older work — healed color still reads at conversational distance.",
        fresh=None,
        healed=ImageRef(
            "color-parrot-cover-up-forearm-las-vegas",
            CLIENT,
            "Healed color cover-up",
        ),
    ),
    HealedEntry(
        entry_id="werewolf-ankle-fine-line",
        title="Fine-line howling werewolf ankle",
        collection="fine_line",
        artist="Joshua Cole",
        placement="Ankle / lower leg",
        sessions="Single session",
        healed_age="Healed",
        touch_up="None",
        aftercare_notes="Thin lines — no heavy lotion layers; client wore loose socks during peel.",
        description="Single-needle style outline work — healed photo shows lines stayed open without spreading.",
        fresh=None,
        healed=ImageRef(
            "fine-line-howling-werewolf-ankle-7ea2af20",
            STUDIO,
            "Healed fine line",
        ),
    ),
    HealedEntry(
        entry_id="beauty-script-roses",
        title="Beauty script with roses",
        collection="fine_line",
        artist="Joshua Cole",
        placement="Inner forearm",
        sessions="Single session",
        healed_age="Healed",
        touch_up="None",
        aftercare_notes="Inner arm — kept fabric loose; no scrubbing during wash.",
        description="Script and floral fine line — healed work shows readable letterforms and delicate petal edges.",
        fresh=None,
        healed=ImageRef(
            "beauty-script-roses-inner-forearm-195a396a",
            STUDIO,
            "Healed fine line",
        ),
    ),
    HealedEntry(
        entry_id="geometric-portrait-sleeve",
        title="Geometric portrait sleeve",
        collection="sleeves",
        artist="Joshua Cole",
        placement="Full arm sleeve",
        sessions="Multiple sessions over months",
        healed_age="Healed",
        touch_up="Minor fill pass on outer bicep only",
        aftercare_notes="Large area — staged healing between inner and outer arm sessions.",
        description=(
            "Portrait and geometry flow around the elbow. Healed documentation shows the sleeve reads as one composition "
            "after all passes completed."
        ),
        fresh=None,
        healed=ImageRef(
            "geometric-portrait-realism-sleeve-client-las-vegas",
            CLIENT,
            "Healed sleeve",
        ),
    ),
    HealedEntry(
        entry_id="medusa-portrait-forearm",
        title="Medusa portrait forearm",
        collection="portraits",
        artist="Joshua Cole",
        placement="Forearm",
        sessions="Single long session",
        healed_age="Healed",
        touch_up="None",
        aftercare_notes="Forearm exposed often — SPF taught from first healed month.",
        description="Snake-hair portrait realism — healed photo shows scale detail and face values after settling.",
        fresh=None,
        healed=ImageRef(
            "black-grey-medusa-snakehair-realism-las-vegas",
            CLIENT,
            "Healed portrait",
        ),
    ),
    HealedEntry(
        entry_id="statue-bust-portrait",
        title="Statue bust with cloth drape",
        collection="portraits",
        artist="Joshua Cole",
        placement="Upper arm",
        sessions="Single session",
        healed_age="Healed",
        touch_up="None",
        aftercare_notes="Standard desert aftercare; client avoided gym shoulder straps during peel.",
        description="Classical bust realism — healed work shows cloth folds and marble-like grey transitions.",
        fresh=None,
        healed=ImageRef(
            "black-grey-statue-bust-cloth-drape-las-vegas",
            CLIENT,
            "Healed portrait",
        ),
    ),
)


def entries_for(collection: CollectionId) -> list[HealedEntry]:
    return [e for e in HEALED_CATALOG if e.collection == collection]


def image_url(ref: ImageRef, *, webp: bool = True) -> str:
    ext = "webp" if webp else "png"
    return f"/{ref.folder}/{ref.stem}.{ext}"


def seo_alt(entry: HealedEntry, ref: ImageRef) -> str:
    if ref.alt:
        return ref.alt
    stage = ref.stage or "Healed"
    slug_part = entry.title.lower().replace("&", "and")
    return (
        f"{stage} {slug_part} tattoo by {entry.artist}, "
        f"{entry.placement.lower()} — Work of Art Las Vegas"
    )


def featured_entry() -> HealedEntry | None:
    for entry in HEALED_CATALOG:
        if entry.featured:
            return entry
    return None


def collection_count(collection: CollectionId) -> int:
    return len(entries_for(collection))
