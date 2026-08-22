#!/usr/bin/env python3
"""Healing Database — timeline stages, style categories, photo mapping, hub metadata."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

StyleId = Literal[
    "black_grey",
    "color",
    "fine_line",
    "traditional",
    "neo_traditional",
    "cover_ups",
    "portraits",
]

StageId = Literal[
    "day_1",
    "day_2",
    "day_3",
    "day_4",
    "week_1",
    "week_2",
    "week_3",
    "month_1",
    "month_3",
    "month_6",
    "year_1",
]

SITE = "https://www.workofarttattoo.com"
HUB_SLUG = "healing_database_tattoo_timeline_encyclopedia_las_vegas"
GALLERY = "healed_tattoo_gallery_las_vegas"
CLIENT = "home_work_of_art_tattoo_piercing/client-portfolio"
COVER = "cover_up_tattoos_las_vegas_master_authority_guide"
BEFORE_AFTER = "tattoo_healing_before_after_real_results"
STUDIO = "studio_gallery"

AFTERCARE_GUIDE = "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"
HEALED_HUB = "/healed_tattoo_gallery_las_vegas/"
BOOK = "/appointments/"
REAL_CLIENT = "/real_client_tattoo_timeline_las_vegas/"


@dataclass(frozen=True)
class TimelineStage:
    stage_id: StageId
    label: str
    day_range: str
    headline: str
    intro: str
    whats_normal: tuple[str, ...]
    watch_for: tuple[str, ...]
    call_studio: tuple[str, ...]
    see_doctor: tuple[str, ...]
    vegas_notes: tuple[str, ...]
    prev_stage: StageId | None
    next_stage: StageId | None


@dataclass(frozen=True)
class StyleCategory:
    style_id: StyleId
    label: str
    short_label: str
    description: str
    healed_collection_slug: str | None
    style_guide_href: str | None
    normal_deltas: dict[StageId, tuple[str, ...]]
    watch_deltas: dict[StageId, tuple[str, ...]]
    vegas_deltas: dict[StageId, tuple[str, ...]]


@dataclass(frozen=True)
class PhotoSlot:
    """Honest studio photo mapped to one style + timeline stage."""

    stem: str
    folder: str
    style_id: StyleId
    stage_id: StageId
    piece_id: str
    caption: str
    alt: str


@dataclass(frozen=True)
class FaqItem:
    question: str
    answer: str


TIMELINE_STAGES: tuple[TimelineStage, ...] = (
    TimelineStage(
        "day_1",
        "Day 1",
        "Hours 0–24 after session",
        "Fresh tattoo — bandage-off to first full sleep",
        (
            "Your tattoo was just finished. Plasma, a thin clear fluid, may weep for several hours — "
            "that is normal wound healing, not infection. In Las Vegas low humidity, skin often feels "
            "tight faster than in humid climates."
        ),
        (
            "Redness and warmth around the tattoo for the first 24–48 hours.",
            "Ink looks slightly darker and more saturated than your healed reference photos will show.",
            "Mild tenderness when fabric brushes the area — expected on forearms, ribs, and feet.",
            "Second-skin or film wrap left on per artist instructions (typically 24–72 hours for large pieces).",
            "Light plasma weeping that dries as a thin shiny layer — blot, do not rub.",
        ),
        (
            "Increasing pain after day two instead of gradual easing.",
            "Spreading redness beyond the tattoo outline after 48 hours.",
            "Yellow or green discharge with foul odor.",
            "Fever, chills, or red streaks toward the heart.",
        ),
        (
            "Wrap feels too tight, fills with fluid, or lifts at edges — message us with a photo.",
            "Unsure whether your aftercare product is fragrance-free and tattoo-safe.",
            "Large piece with heavy plasma — we can walk you through second-skin timing.",
        ),
        (
            "Red streaking, fever over 100.4°F, or rapidly spreading hot redness.",
            "Signs of allergic reaction to adhesive (hives far from tattoo, trouble breathing).",
        ),
        (
            "Vegas AC dries air fast — keep hydration up; lotion comes after first wash, not on day-zero plasma.",
            "Do not sit poolside or hot-tub on day one even if the tattoo is covered — heat and bacteria risk.",
            "Carry SPF for healed skin only; fresh tattoos need shade, not sunscreen yet.",
        ),
        None,
        "day_2",
    ),
    TimelineStage(
        "day_2",
        "Day 2",
        "24–48 hours",
        "First wash, light lotion, plasma slowing down",
        (
            "Most collectors remove second-skin or switch to breathable aftercare on day two or three. "
            "The tattoo may look dull as plasma film builds — washing reveals true color underneath."
        ),
        (
            "Slight swelling still present on hands, feet, and ankles.",
            "Skin feels tight; fine grey tattoos may look slightly thicker until peel.",
            "Gentle wash with lukewarm water and fragrance-free soap — pat dry, air 5–10 minutes.",
            "Thin application of approved lotion once dry — Vegas dryness may need two light passes.",
        ),
        (
            "Heavy scabbing that cracks when you move (often from over-lotioning or picking).",
            "Blistering under second-skin — remove film and contact studio.",
        ),
        (
            "Second-skin traps fluid under the whole piece — send a photo before removing.",
            "Unsure if your wash routine matches what Joshua or Katelyn demonstrated in-studio.",
        ),
        (
            "Pus, fever, or pain that wakes you at night and worsens daily.",
        ),
        (
            "Desert heat + gym sweat: skip heavy workouts that soak the tattoo for 48–72 hours.",
            "Hotel rooms on the Strip run dry — a humidifier helps peel phase later, not day two alone.",
        ),
        "day_1",
        "day_3",
    ),
    TimelineStage(
        "day_3",
        "Day 3",
        "48–72 hours",
        "Peel phase begins on thin skin",
        (
            "Day three is when many pieces start the satin, flaky look people call 'milky.' "
            "Do not pick — the ink is setting under a regenerating layer."
        ),
        (
            "Light flaking like sunburn peel — white or greyish skin coming off in sheets.",
            "Itching that improves with clean hands and light lotion, not scratching.",
            "Color may look muted until dead skin sheds — especially on color and black & grey realism.",
        ),
        (
            "Thick hard scabs the size of coins — usually over-lotion or trauma.",
            "Ink blowout appearing as fuzzy halos beyond original lines (contact artist for photo review).",
        ),
        (
            "Peel looks uneven on a large thigh or back piece — we can confirm normal vs. trouble spots.",
            "Cover-up in progress — session spacing questions before your next pass.",
        ),
        (
            "Green discharge, red streaks, or fever.",
        ),
        (
            "Pool parties and day clubs: still off limits until fully closed — chlorine and sun combo is harsh.",
            "Outdoor workers: long sleeves or UPF fabric over healed-adjacent skin; keep fresh tattoo shaded.",
        ),
        "day_2",
        "day_4",
    ),
    TimelineStage(
        "day_4",
        "Day 4",
        "72–96 hours",
        "Active peeling — keep hands off",
        (
            "Peeling accelerates on day four for many clients. The tattoo often looks worst this week — "
            "that is normal, not a sign the artist failed."
        ),
        (
            "Flakes fall off during washing — do not force them.",
            "Mild itch; tattoo may look 'foggy' until fresh skin completes.",
            "Continue light lotion 2–3× daily in Vegas dry air.",
        ),
        (
            "Raw shiny patches that bleed when bumped.",
            "Lines that look completely gone (rare — usually just buried under peel; wait two weeks before panic).",
        ),
        (
            "Hand or foot tattoo with heavy peel and job requirements — we advise on gloves and downtime.",
        ),
        (
            "Spreading infection signs or allergic rash covering body beyond tattoo.",
        ),
        (
            "Hiking Red Rock or Valley of Fire: dust sticks to lotion — rinse gently if outdoor exposure happens.",
        ),
        "day_3",
        "week_1",
    ),
    TimelineStage(
        "week_1",
        "Week 1",
        "Days 5–7",
        "End of first week — peel finishing on small pieces",
        (
            "By end of week one, smaller tattoos often finish peeling. Large black & grey pieces may "
            "still flake on inner thighs or elbows where skin moves."
        ),
        (
            "Peel mostly complete on forearms and calves.",
            "Slight dryness and ashiness — normal until month one.",
            "Tattoo readable but not at final contrast yet.",
        ),
        (
            "Scabs pulled off early leaving pits or color loss.",
            "Persistent heavy swelling on extremities past day seven.",
        ),
        (
            "Planning second session on a multi-pass cover-up — confirm heal readiness.",
            "Fine line looks hairy during peel — photo review before worrying.",
        ),
        (
            "Medical emergency signs as above.",
        ),
        (
            "First weekend back at gym: avoid direct friction on the piece (bench press on fresh chest tattoo, etc.).",
        ),
        "day_4",
        "week_2",
    ),
    TimelineStage(
        "week_2",
        "Week 2",
        "Days 8–14",
        "Surface heal — still not sun-ready",
        (
            "Week two is when clients think they are 'healed' because peeling stopped. "
            "The dermis is still remodeling — treat the tattoo as fragile."
        ),
        (
            "Peeling complete on most placements.",
            "Mild itch and dry patches.",
            "Colors look slightly lighter than day zero — expected settling.",
        ),
        (
            "Bumpy scar tissue forming along lines (hypertrophic scarring — early intervention helps).",
            "Sections where scabs were picked show patchy saturation.",
        ),
        (
            "Touch-up timing questions — we prefer photos at 4–6 weeks minimum.",
            "Swimming pool trip planned — ask before submerging.",
        ),
        (
            "Infection signs; uncontrolled bleeding.",
        ),
        (
            "Vegas sun through car windows still UV-exposes forearms — keep covered until month one.",
            "SPF 30+ on fully closed skin only — not on open peel.",
        ),
        "week_1",
        "week_3",
    ),
    TimelineStage(
        "week_3",
        "Week 3",
        "Days 15–21",
        "Settling begins — contrast returns slowly",
        (
            "Grey steps and color blocks start separating again as skin normalizes. "
            "Fine line may look slightly softer — judge at month three, not week three."
        ),
        (
            "Reduced itch; skin texture smoothing.",
            "Black & grey mid-tones reappear after 'milky' phase.",
            "Light gym and normal showers OK if skin is fully closed.",
        ),
        (
            "Raised lines that stay red for weeks (possible blowout or irritation).",
            "Color patches that look completely blank — photo for artist review.",
        ),
        (
            "Traveling home from Vegas — need aftercare product recommendations on the road.",
        ),
        (
            "Medical concerns as above.",
        ),
        (
            "Desert hiking season: sweat + dust — rinse tattoo after outdoor activity, pat dry.",
        ),
        "week_2",
        "month_1",
    ),
    TimelineStage(
        "month_1",
        "Month 1",
        "Days 22–30",
        "Fully closed skin — SPF habit starts",
        (
            "At one month, the epidermis is typically closed. This is when we teach SPF as a daily "
            "habit in Las Vegas — UV is the main long-term enemy of tattoo clarity."
        ),
        (
            "Matte healed look; true contrast emerging.",
            "Safe for normal exercise if no open areas.",
            "Light touch-up consult OK if artist flagged thin spots during session.",
        ),
        (
            "Persistent redness in one zone only.",
            "Bumps or keloid-like growth (genetic tendency — dermatology referral).",
        ),
        (
            "Schedule touch-up or second session on large project.",
            "Healing check photos welcome — we keep files for our gallery updates.",
        ),
        (
            "Signs of infection (rare this late) or severe allergic reaction.",
        ),
        (
            "SPF 30–50 reapplied every two hours in direct sun — non-negotiable for color and portraits.",
            "Pool and hot tub generally OK if skin is fully closed and rinsed after.",
        ),
        "week_3",
        "month_3",
    ),
    TimelineStage(
        "month_3",
        "Month 3",
        "~90 days",
        "True healed appearance for most styles",
        (
            "Three months is our benchmark for judging black & grey realism, fine line longevity, "
            "and color saturation. This is when we publish many healed gallery comparisons."
        ),
        (
            "Blacks settled — not powdery grey unless designed that way.",
            "Fine lines stable without spread.",
            "Color mellowed slightly; detail still readable at conversational distance.",
        ),
        (
            "Significant blowout or fade in high-friction zones (palm, foot, inner lip — if applicable).",
            "Cover-up still showing old ink ghosting — may need planned pass.",
        ),
        (
            "Book touch-up if agreed during consult.",
            "Add healed photos to our documentation queue — same client only.",
        ),
        (
            "Skin disease symptoms unrelated to tattoo — see dermatologist.",
        ),
        (
            "Summer pool season in Vegas: SPF + rinse after chlorine.",
            "Outdoor workers: reapply SPF through shirt gaps on forearm pieces.",
        ),
        "month_1",
        "month_6",
    ),
    TimelineStage(
        "month_6",
        "Month 6",
        "~180 days",
        "Mid-term aging check",
        (
            "Six months shows how desert sun and lifestyle affect your piece. "
            "Compare to month three — slight lightening is normal; blotchy loss is not."
        ),
        (
            "Even grey transitions on portraits and wildlife.",
            "Color pieces stable if SPF used consistently.",
            "Cover-ups integrated — old ink no longer readable at distance.",
        ),
        (
            "Sharp fade bands on color (often sun exposure).",
            "Grey wash turned uniformly muddy — may indicate aftercare or design issue.",
        ),
        (
            "Second session on sleeve or back piece scheduling.",
            "Request in-studio healed photo for our gallery.",
        ),
        (
            "Dermatology for changing moles within tattoo.",
        ),
        (
            "Monsoon humidity spike — skin may look slightly different; hydration still matters.",
        ),
        "month_3",
        "year_1",
    ),
    TimelineStage(
        "year_1",
        "Year 1",
        "12 months",
        "Long-term proof — how Vegas wear treats ink",
        (
            "One year is the gold standard for healed portfolio documentation. "
            "We photograph the same client when possible — see our Real Client Timeline and style galleries."
        ),
        (
            "Linework and values readable at arm's length.",
            "Blacks still deep if SPF and aftercare followed.",
            "Fine line letterforms still legible on inner arm.",
            "Portraits retain likeness if values were planned for healing.",
        ),
        (
            "Major blur or fade in non-sun-exposed areas — unusual; consult artist.",
            "Touch-up need on high-detail realism after year — sometimes normal for hands.",
        ),
        (
            "Annual check-in photos for our Healing Database updates.",
            "Plan refresh or add-on work with healed skin as canvas.",
        ),
        (
            "Skin cancer screening if new pigment changes within tattoo.",
        ),
        (
            "Year-round Vegas UV: SPF remains daily on exposed tattoos.",
            "Compare to fresh photo — slight softening is art settling, not failure.",
        ),
        "month_6",
        None,
    ),
)

STYLE_CATEGORIES: tuple[StyleCategory, ...] = (
    StyleCategory(
        "black_grey",
        "Black & Grey",
        "Black & grey",
        (
            "Realism, soft shading, open skin highlights — how grey wash settles in desert heat. "
            "Joshua Cole documents most of our black & grey heal stages in-studio."
        ),
        "healed_black_grey_tattoos_las_vegas",
        "/realism_tattoos_las_vegas_master_authority_guide/",
        {
            "day_1": ("Deep blacks look wet and glossy under plasma — highlights stay open by design.",),
            "month_3": ("Mid-tone separation returns after milky phase — judge contrast now, not week one.",),
            "year_1": ("Saturated blacks without muddy grey wash in bend areas (thigh, elbow) = successful heal.",),
        },
        {
            "week_2": ("Grey realism can look 'washed out' during peel — do not assume blowout until month one.",),
        },
        {
            "month_1": ("Forearm commuters: SPF before driving — UV through windshield fades grey faster than body pieces.",),
        },
    ),
    StyleCategory(
        "color",
        "Color",
        "Color",
        (
            "Memorial eagles, saturated blocks, and layered color — how pigments mellow and stay readable "
            "months later in Las Vegas sun."
        ),
        "healed_color_tattoos_las_vegas",
        "/realism_tattoos_las_vegas_master_authority_guide/",
        {
            "day_1": ("Color reads brightest day zero — expect 10–20% softening as skin regenerates.",),
            "month_3": ("Yellows and oranges settle most; blues and greens usually hold if aftercare followed.",),
            "year_1": ("Memorial and portrait color judged at distance — detail should still read.",),
        },
        {
            "week_1": ("Patchy color during peel is normal — do not pick flakes off color blocks.",),
        },
        {
            "month_1": ("SPF is non-optional for color in Vegas — reapply every two hours outdoors.",),
        },
    ),
    StyleCategory(
        "fine_line",
        "Fine Line",
        "Fine line",
        (
            "Single-needle and micro-detail work — what stays crisp after peel and what softens slightly "
            "by month three."
        ),
        "healed_fine_line_tattoos_las_vegas",
        "/fine_line_tattoos_las_vegas_master_authority_guide/",
        {
            "day_3": ("Lines may look slightly thicker under peeling skin — wait before judging spread.",),
            "month_3": ("Hairline strokes either hold open or show micro-spread — our benchmark week.",),
        },
        {
            "week_2": ("Do not over-lotion fine line — thick scabs blur delicate strokes.",),
            "month_1": ("Inner arm fine line: fabric friction during peel causes more blur risk.",),
        },
        {
            "day_2": ("Lightest lotion layer of any style — Vegas dryness vs. line clarity balance.",),
        },
    ),
    StyleCategory(
        "traditional",
        "Traditional",
        "Traditional",
        (
            "Bold outlines and saturated fills — how whip shading and solid packs heal in low humidity. "
            "Studio traditional photos added to this database as we document new pieces."
        ),
        None,
        "/best_tattoo_styles_for_sleeves_large_scale_project_hub/",
        {
            "day_1": ("Bold black outlines swell slightly — lines look thicker for 48–72 hours.",),
            "month_3": ("Solid fills should read even — no patchy gaps if peel was protected.",),
        },
        {
            "week_1": ("Heavy black fill can scab thicker — avoid gym friction on fresh trad.",),
        },
        {
            "month_1": ("Traditional holds sun better than grey wash but still needs SPF in Vegas.",),
        },
    ),
    StyleCategory(
        "neo_traditional",
        "Neo-Traditional",
        "Neo-traditional",
        (
            "Illustrative color, bold lines, and decorative fills — healing sits between traditional "
            "saturation and realism grey transitions."
        ),
        None,
        "/best_tattoo_styles_for_sleeves_large_scale_project_hub/",
        {
            "day_1": ("Color blocks and black outlines heal on different timelines — peel may look patchy.",),
            "month_3": ("Decorative fills should look even; soft shading intentional, not muddy.",),
        },
        {
            "week_2": ("Mixed line weights — thin color separations need extra peel protection.",),
        },
        {},
    ),
    StyleCategory(
        "cover_ups",
        "Cover-Ups",
        "Cover-ups",
        (
            "Redesigns over old ink — multi-session spacing, hand and forearm challenges, "
            "and judging success at 90 days+, not day one."
        ),
        "healed_cover_up_tattoos_las_vegas",
        "/cover_up_tattoos_las_vegas_master_authority_guide/",
        {
            "day_1": ("Cover-ups often run longer sessions — expect more plasma and fatigue.",),
            "month_3": ("Old ink ghosting may still show faintly — planned passes are normal.",),
            "month_6": ("Finished redesign should read as new art, not a dark blob.",),
        },
        {
            "week_3": ("Do not panic if old color peeks through during peel — photo us before assuming failure.",),
        },
        {
            "month_1": ("Hand cover-ups: limit sun and friction longest — palms and knuckles heal slower.",),
        },
    ),
    StyleCategory(
        "portraits",
        "Portraits",
        "Portraits",
        (
            "Figurative and likeness work — values, skin texture, and eye detail judged after "
            "the milky phase clears."
        ),
        "healed_portrait_tattoos_las_vegas",
        "/realism_tattoos_las_vegas_master_authority_guide/",
        {
            "day_1": ("Portrait greys look harsh day zero — soft transitions return after peel.",),
            "month_3": ("Likeness and eye detail benchmark — tentacle fine lines, hair strands, etc.",),
            "year_1": ("Facial likeness and micro-detail documented at 12 months when possible.",),
        },
        {
            "week_2": ("Portrait pieces look worst mid-peel — do not judge likeness until month one.",),
        },
        {
            "month_1": ("Portrait on calf or arm: SPF protects value range that sells likeness.",),
        },
    ),
)

# Honest photo mapping only — stem must match documented heal age in filename or catalog.
PHOTO_SLOTS: tuple[PhotoSlot, ...] = (
    PhotoSlot(
        "fresh-roaring-lion-thigh-black-grey-joshua-cole-las-vegas",
        GALLERY,
        "black_grey",
        "day_1",
        "roaring-lion-thigh",
        "Roaring lion thigh — fresh (day 0), same client as 3-month healed photo",
        "Fresh black and grey roaring lion thigh tattoo by Joshua Cole, Work of Art Las Vegas",
    ),
    PhotoSlot(
        "healed-3-month-roaring-lion-thigh-joshua-cole-las-vegas",
        GALLERY,
        "black_grey",
        "month_3",
        "roaring-lion-thigh",
        "Same roaring lion thigh — documented at 3 months (not a different client)",
        "Three-month healed roaring lion thigh black and grey realism by Joshua Cole, Las Vegas",
    ),
    PhotoSlot(
        "fresh-all-seeing-eye-skull-elbow-joshua-cole-las-vegas",
        GALLERY,
        "black_grey",
        "day_1",
        "all-seeing-eye-elbow",
        "All-seeing eye & skull elbow — fresh documentation",
        "Fresh black and grey all-seeing eye skull elbow tattoo by Joshua Cole, Las Vegas",
    ),
    PhotoSlot(
        "fresh-all-seeing-eye-triangle-forearm-joshua-cole-las-vegas",
        GALLERY,
        "black_grey",
        "day_1",
        "all-seeing-eye-triangle",
        "All-seeing eye in triangle — fresh (healed follow-up pending)",
        "Fresh all-seeing eye triangle forearm tattoo by Joshua Cole, Work of Art Las Vegas",
    ),
    PhotoSlot(
        "cross-eye-skull-forearm-stack-5bc3d948",
        STUDIO,
        "black_grey",
        "day_1",
        "cross-eye-skull-forearm",
        "Cross, eye & skull forearm — fresh session (see Real Client Timeline for 1-year heal)",
        "Fresh cross eye skull forearm black and grey tattoo by Joshua Cole, Las Vegas",
    ),
    PhotoSlot(
        "healed-1-year-cross-eye-skull-outer-forearm-joshua-cole-las-vegas",
        GALLERY,
        "black_grey",
        "year_1",
        "cross-eye-skull-forearm",
        "Same cross/eye/skull client — 1 year healed (outer forearm)",
        "One-year healed cross eye skull outer forearm tattoo by Joshua Cole, Las Vegas",
    ),
    PhotoSlot(
        "healed-1-year-cross-eye-skull-forearm-portrait-joshua-cole-las-vegas",
        GALLERY,
        "portraits",
        "year_1",
        "cross-eye-skull-forearm",
        "Same client — portrait angle at 1 year (realistic eye detail)",
        "One-year healed realistic eye forearm portrait tattoo by Joshua Cole, Las Vegas",
    ),
    PhotoSlot(
        "skull-hourglass-forearm-realism-fresh-las-vegas",
        CLIENT,
        "black_grey",
        "day_1",
        "skull-hourglass-forearm",
        "Skull & hourglass forearm — fresh at bandage-off",
        "Fresh skull hourglass forearm black and grey realism by Joshua Cole, Las Vegas",
    ),
    PhotoSlot(
        "fresh-eagle-memorial-calf-tattoo-las-vegas",
        GALLERY,
        "color",
        "day_1",
        "eagle-memorial-calf",
        "Color memorial eagle calf — fresh (day 0)",
        "Fresh color eagle memorial calf tattoo by Joshua Cole, Work of Art Las Vegas",
    ),
    PhotoSlot(
        "eagle-memorial-calf-healed-tattoo-las-vegas",
        GALLERY,
        "color",
        "month_3",
        "eagle-memorial-calf",
        "Same memorial eagle calf — healed months later (settled color)",
        "Healed color eagle memorial calf tattoo months later, Work of Art Las Vegas",
    ),
    PhotoSlot(
        "fresh-dog-portrait-chest-realism-joshua-cole-las-vegas",
        GALLERY,
        "portraits",
        "day_1",
        "dog-portrait-chest",
        "Dog portrait chest — fresh realism session",
        "Fresh dog portrait chest realism tattoo by Joshua Cole, Las Vegas",
    ),
    PhotoSlot(
        "healed-davy-jones-pirates-calf-portrait-joshua-cole-las-vegas",
        GALLERY,
        "portraits",
        "month_3",
        "davy-jones-calf",
        "Davy Jones calf portrait — healed documentation (3–12 month range)",
        "Healed Davy Jones Pirates calf portrait tattoo by Joshua Cole, Las Vegas",
    ),
    PhotoSlot(
        "cover-up-tattoo-phoenix-hand-las-vegas-after",
        COVER,
        "cover_ups",
        "month_6",
        "phoenix-hand-cover-up",
        "Phoenix hand & forearm cover-up — finished healed piece",
        "Healed phoenix hand and forearm cover-up tattoo by Joshua Cole, Las Vegas",
    ),
    PhotoSlot(
        "healed-realism-seraphim-eye-wings-tattoo",
        COVER,
        "cover_ups",
        "month_3",
        "seraphim-cover-up",
        "Seraphim eye & wings cover-up — healed black & grey",
        "Healed seraphim eye wings cover-up realism tattoo, Work of Art Las Vegas",
    ),
    PhotoSlot(
        "fine-line-howling-werewolf-ankle-7ea2af20",
        STUDIO,
        "fine_line",
        "month_3",
        "werewolf-ankle",
        "Fine-line werewolf ankle — healed documentation",
        "Healed fine line werewolf ankle tattoo by Joshua Cole, Las Vegas",
    ),
    PhotoSlot(
        "beauty-script-roses-inner-forearm-195a396a",
        STUDIO,
        "fine_line",
        "month_3",
        "beauty-script-roses",
        "Beauty script with roses — healed fine line inner forearm",
        "Healed fine line beauty script roses inner forearm tattoo, Las Vegas",
    ),
)

HUB_FAQS: tuple[FaqItem, ...] = (
    FaqItem(
        "What is the Healing Database?",
        (
            "A stage-by-stage encyclopedia of tattoo healing — day 1 through year 1 — organized by style "
            "(black & grey, color, fine line, traditional, neo-traditional, cover-ups, portraits). "
            "We pair education with honest studio photos where we have documented the same client at that heal age."
        ),
    ),
    FaqItem(
        "Why does my tattoo look worse during week one?",
        (
            "Peeling skin creates a milky, flaky layer that hides contrast. This is normal wound healing — "
            "not a sign your artist did poor work. Judge black & grey and portraits at month three; "
            "fine line at month three minimum."
        ),
    ),
    FaqItem(
        "Is Las Vegas desert climate harder on healing tattoos?",
        (
            "Low humidity dries skin faster — you may need lighter, more frequent lotion than humid-climate guides suggest. "
            "UV is intense year-round: keep fresh tattoos shaded; use SPF on fully closed skin from month one onward."
        ),
    ),
    FaqItem(
        "When should I call Work of Art vs. see a doctor?",
        (
            "Call us for aftercare timing, second-skin questions, peel photos, and touch-up scheduling. "
            "See a doctor for fever, red streaking, pus, spreading hot redness, or allergic reactions with breathing difficulty. "
            "We share studio practice — not medical diagnosis."
        ),
    ),
    FaqItem(
        "Do you use stock healing photos?",
        (
            "No. Photos in this database come from Work of Art client documentation. When we show a timeline pair "
            "(fresh and healed), it is the same piece and client — labeled explicitly."
        ),
    ),
)


def stage_by_id(stage_id: StageId) -> TimelineStage:
    for s in TIMELINE_STAGES:
        if s.stage_id == stage_id:
            return s
    raise KeyError(stage_id)


def style_by_id(style_id: StyleId) -> StyleCategory:
    for c in STYLE_CATEGORIES:
        if c.style_id == style_id:
            return c
    raise KeyError(style_id)


def style_hub_slug(style_id: StyleId) -> str:
    return f"healing_database_{style_id}_tattoos_las_vegas"


def universal_timeline_slug(stage_id: StageId) -> str:
    return f"healing_database_tattoo_{stage_id}_las_vegas"


def leaf_slug(style_id: StyleId, stage_id: StageId) -> str:
    return f"healing_database_{style_id}_{stage_id}_las_vegas"


def photos_for(style_id: StyleId | None, stage_id: StageId) -> list[PhotoSlot]:
    out: list[PhotoSlot] = []
    for p in PHOTO_SLOTS:
        if p.stage_id != stage_id:
            continue
        if style_id is not None and p.style_id != style_id:
            continue
        out.append(p)
    return out


def all_leaf_slugs() -> list[tuple[StyleId, StageId, str]]:
    rows: list[tuple[StyleId, StageId, str]] = []
    for style in STYLE_CATEGORIES:
        for stage in TIMELINE_STAGES:
            rows.append((style.style_id, stage.stage_id, leaf_slug(style.style_id, stage.stage_id)))
    return rows


def all_page_slugs() -> list[str]:
    slugs = [HUB_SLUG]
    slugs.extend(style_hub_slug(s.style_id) for s in STYLE_CATEGORIES)
    slugs.extend(universal_timeline_slug(s.stage_id) for s in TIMELINE_STAGES)
    slugs.extend(slug for _sty, _stg, slug in all_leaf_slugs())
    return slugs


def image_path(stem: str, folder: str, *, webp: bool = True) -> str:
    ext = "webp" if webp else "png"
    return f"/{folder}/{stem}.{ext}"


def merge_stage_style_copy(
    stage: TimelineStage,
    style: StyleCategory | None,
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    normal = stage.whats_normal
    watch = stage.watch_for
    vegas = stage.vegas_notes
    if style:
        normal = normal + style.normal_deltas.get(stage.stage_id, ())
        watch = watch + style.watch_deltas.get(stage.stage_id, ())
        vegas = vegas + style.vegas_deltas.get(stage.stage_id, ())
    return normal, watch, vegas
