#!/usr/bin/env python3
"""Skin Science authority catalog — tattoo-focused dermatology education (Joshua Cole voice)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CategoryId = Literal["layers", "permanence", "conditions"]

HUB_SLUG = "skin_science_tattoo_dermatology_authority_guide"
HUB_TITLE = "Skin Science for Tattoo Collectors"
HUB_INTRO = (
    "Your skin is the canvas — not just the surface we tattoo on, but the living tissue that "
    "holds ink for decades. These guides explain how skin layers work, why tattoos stay permanent, "
    "and how common conditions change what we can safely tattoo. Written from a studio perspective "
    "by Joshua Cole — not medical advice; when in doubt, consult a dermatologist before you book."
)

BOOK = "/appointments/"
JOSHUA_PAGE = "/artists/joshua-cole/"
DESERT_AFTERCARE = "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"
HEALED_HUB = "/healed_tattoo_gallery_las_vegas/"
HEALING_PROOF = "/tattoo_healing_before_after_real_results/"
FINE_LINE = "/fine_line_tattoos_las_vegas_master_authority_guide/"
COVER_UP = "/cover_up_tattoos_las_vegas_master_authority_guide/"

CATEGORY_LABELS: dict[CategoryId, str] = {
    "layers": "Skin layers — where ink lives",
    "permanence": "Why tattoos stay permanent",
    "conditions": "Skin conditions & tattoo planning",
}

MEDICAL_DISCLAIMER = (
    "This page is studio education — how tattoo artists think about skin — not a diagnosis or "
    "treatment plan. If you have a medical skin condition, talk to a licensed dermatologist "
    "before booking tattoo work. We can often tattoo safely with clearance and a adjusted plan, "
    "but your clinician knows your history better than any guide."
)


@dataclass(frozen=True)
class SkinScienceTopic:
    slug_id: str
    title: str
    intro: str
    meta_description: str
    category: CategoryId
    sections: tuple[tuple[str, tuple[str, ...]], ...]
    faqs: tuple[tuple[str, str], ...] = ()
    related: tuple[str, ...] = ()
    joshua_quote: str = ""
    medical: bool = False
    desert_bullets: tuple[str, ...] = ()


def slug_for(topic: SkinScienceTopic) -> str:
    return f"{topic.slug_id}_skin_science_las_vegas_authority_guide"


def topic_by_id(slug_id: str) -> SkinScienceTopic | None:
    for t in SKIN_SCIENCE_TOPICS:
        if t.slug_id == slug_id:
            return t
    return None


def hub_meta_description() -> str:
    return (
        "How skin layers, immune cells, and collagen hold tattoo ink — plus scar tissue, eczema, "
        "psoriasis, diabetes, and aging skin from a Las Vegas tattoo studio perspective. "
        "Work of Art Tattoo & Piercing."
    )


def page_title(topic: SkinScienceTopic) -> str:
    return topic.title


SKIN_SCIENCE_TOPICS: tuple[SkinScienceTopic, ...] = (
    SkinScienceTopic(
        slug_id="epidermis",
        title="The Epidermis — Your Skin's Outer Shield",
        intro=(
            "The epidermis is the thin, constantly renewing layer you see and touch. Tattoo needles "
            "pass through it on the way to the dermis — and understanding that turnover explains peeling, "
            "why surface ink washes away, and why aftercare protects more than the art itself."
        ),
        meta_description=(
            "What the epidermis does for tattoo healing — turnover, barrier function, peeling, and "
            "why surface ink does not stay. Joshua Cole, Work of Art Las Vegas."
        ),
        category="layers",
        joshua_quote=(
            "When clients panic during peeling, I remind them: the epidermis replaces itself every few weeks. "
            "We are not tattooing the epidermis to hold color — we are crossing it to deposit ink where it "
            "belongs, then letting this layer heal shut like a door over the vault."
        ),
        sections=(
            ("What the epidermis is", (
                "Outermost skin layer — roughly 0.05–1.5 mm thick depending on body site.",
                "Made mostly of keratinocytes that mature as they rise toward the surface.",
                "No blood vessels — nutrients diffuse up from the dermis below.",
                "Melanocytes live here — pigment that gives skin tone and some UV protection.",
            )),
            ("Turnover and the tattoo session", (
                "Basal layer stem cells push new cells upward; the surface sheds as dead stratum corneum.",
                "Needles pierce the full epidermis in milliseconds — you feel it, then ink passes deeper.",
                "Ink trapped only in the epidermis sheds with normal skin renewal within weeks.",
                "That is why wipe-away 'scratch' tattoos and stick-and-poke on the surface fade fast.",
            )),
            ("Healing — what you see day by day", (
                "Days 1–3: plasma, redness, tightness — the barrier is open and vulnerable.",
                "Days 4–14: peeling and flaking as the epidermis rebuilds over the wound.",
                "Weeks 3–6: matte finish replaces the glossy fresh look; color reads softer.",
                "Picking scabs pulls ink out of the dermis through the same holes we made — avoid it.",
            )),
            ("Barrier function after tattooing", (
                "Intact epidermis blocks bacteria and limits water loss — critical in desert climates.",
                "Over-washing or harsh scrubbing delays barrier recovery and can lighten ink.",
                "Fragrance-free moisturizer supports the lipid barrier without suffocating the tattoo.",
            )),
            ("Studio perspective — what we watch for", (
                "Rashes or open eczema on the planned site — we reschedule until skin is calm.",
                "Sunburned epidermis tattoos unevenly and heals poorly — book after it clears.",
                "Heavy exfoliation habits (retinol, glycolic) near fresh work can pull color early.",
            )),
        ),
        desert_bullets=(
            "Las Vegas low humidity pulls water through a healing epidermis faster — light lotion beats heavy occlusive balms.",
            "Pool chlorine and hot-tub chemicals strip lipids from renewing epidermis — keep fresh tattoos out until closed.",
            "SPF on healed epidermis slows UV breakdown of pigment sitting below — daily on exposed work.",
        ),
        faqs=(
            ("Is peeling normal on a new tattoo?", "Yes. Peeling is the epidermis shedding damaged surface cells. Do not pick — let it flake off naturally."),
            ("Why did my tattoo look faded right after peeling?", "The most saturated cells peeled away. Color in the dermis re-emerges as the new epidermis matures over several weeks."),
            ("Can I exfoliate a healed tattoo?", "Gentle exfoliation on fully healed skin is fine occasionally. Avoid aggressive scrubs on fine line or light color until the piece is months settled."),
        ),
        related=("dermis", "why_tattoos_stay_forever", "aging_skin"),
    ),
    SkinScienceTopic(
        slug_id="dermis",
        title="The Dermis — Where Tattoo Ink Lives",
        intro=(
            "The dermis is the connective-tissue layer beneath the epidermis — thick enough to hold "
            "pigment for life, vascular enough to heal, and structured enough that needle depth "
            "matters on every pass."
        ),
        meta_description=(
            "Tattoo ink sits in the dermis — collagen, blood supply, needle depth, and why too shallow "
            "or Too deep: pigment can spread beyond the intended line, increasing the risk of blurred edges or tattoo blowout and causing unnecessary tissue trauma.
        ),
        category="layers",
        joshua_quote=(
            "I am listening for the skin through the machine — a slight change in resistance tells me "
            "when I am in the dermis versus riding too shallow or punching into fat. That feel is years "
            "of repetition, not guesswork."
        ),
        sections=(
            ("Structure of the dermis", (
                "Two zones: papillary dermis (upper, finer collagen) and reticular dermis (deeper, denser bundles).",
                "Hair follicles, sweat glands, nerves, and blood vessels run through this layer.",
                "Collagen and elastin give skin strength and snap — they also trap ink particles.",
                "Thickness varies — eyelid dermis is paper-thin; upper back dermis is much deeper.",
            )),
            ("Target depth for tattooing", (
                "Stable pigment lands roughly the dermis, with exact working depth varying by body site, skin thickness, technique, and individual anatomy below the surface — the dermis, with exact working depth varying by body site, skin thickness, technique, and individual anatomy.",
                "Too shallow: pigment may heal faint, patchy, or fall out because too much ink was placed in tissue that continually renews.",
                "Too deep: pigment can spread beyond the intended line, increasing the risk of blurred edges or tattoo blowout and causing unnecessary tissue trauma.
                "Skin type, age, and body site change the sweet spot — artists adjust on the fly.",
            )),
            ("Ink dispersion in dermal tissue", (
                "Needles create micro-channels; ink suspension flows into the wound track.",
                "Fibroblasts and macrophages respond within hours — beginning the permanence process.",
                "Line work needs tighter packing; soft shading spreads more with the same depth.",
            )),
            ("Healing inside the dermis", (
                "Inflammation peaks in the first 72 hours — swelling and warmth are normal within limits.",
                "Fibroblasts lay new collagen to repair needle tracks — slight texture change is common.",
                "Excess ink that never bound to tissue clears via lymph — why colors soften slightly.",
                "Full dermal remodeling continues months — the tattoo 'settles' into its long-term look.",
            )),
            ("What artists adjust by anatomy", (
                "Thin skin ( wrists, inner bicep): lighter hand, fewer passes.",
                "Thick skin ( upper back, outer thigh): slightly deeper, more room for saturation.",
                "Scarred dermis: unpredictable pockets — see our scar tissue guide before cover-ups.",
            )),
        ),
        faqs=(
            ("Can you tattoo Too deep: pigment can spread beyond the intended line, increasing the risk of blurred edges or tattoo blowout and causing unnecessary tissue trauma.
            ("Why do lines spread over years?", "Collagen remodeling and UV exposure change how light scatters through skin — not always 'blown out' from day one."),
            ("Does the dermis grow back after tattooing?", "It repairs — it does not replace untouched dermis. Ink sits among permanent structural change."),
        ),
        related=("epidermis", "hypodermis", "collagen", "macrophages"),
    ),
    SkinScienceTopic(
        slug_id="hypodermis",
        title="The Hypodermis — Fat Layer & Tattoo Limits",
        intro=(
            "The hypodermis — subcutaneous fat — sits below the dermis. We avoid depositing ink here "
            "on purpose. When pigment lands in fat, lines blur, color migrates, and healing gets "
            "unpredictable."
        ),
        meta_description=(
            "Why tattoo artists avoid the hypodermis (fat layer) — blowouts, migration, and anatomy "
            "limits by body area. Skin science from Work of Art Las Vegas."
        ),
        category="layers",
        joshua_quote=(
            "A blowout is often a depth problem — ink where fat can move. I would rather build a line "
            "with two controlled passes in the dermis than one heavy pass that drops into the hypodermis."
        ),
        sections=(
            ("What the hypodermis does", (
                "Primarily adipose (fat) tissue with loose connective fibers.",
                "Insulates, cushions, and anchors skin to underlying muscle and fascia.",
                "Major blood vessels and nerves pass through on their way to the dermis.",
                "Thickness swings with body composition and site — belly vs shin is night and day.",
            )),
            ("Why ink in fat misbehaves", (
                "Fat lobules move with weight change, pressure, and time — ink drifts from original placement.",
                "Lower cell density means less trapping — pigment spreads in a feathered halo.",
                "Healing is slower and more inflammatory when trauma reaches deep subcutaneous tissue.",
            )),
            ("Blowouts — artist and anatomy factors", (
                "Over-travel on a liner, dull needles, or excessive speed can drive ink past the dermis.",
                "Very thin skin over bone ( spine, ankle) offers little margin for error.",
                "Client movement during a pass increases depth inconsistency.",
            )),
            ("Body areas with less dermal margin", (
                "Fingers, toes, tops of feet — thin dermis over minimal fat; high fade and blowout risk.",
                "Inner wrist and elbow ditch — tendons and thin skin need conservative depth.",
                "We may decline or simplify designs on high-risk sites after an honest consult.",
            )),
            ("Weight fluctuation and old tattoos", (
                "Significant fat gain or loss reshapes hypodermis volume — large pieces can distort slightly.",
                "Stretch marks form when dermis tears faster than it can repair — different issue, related stress.",
                "Stable weight during healing helps ink settle evenly in the dermis above.",
            )),
        ),
        faqs=(
            ("Can a blowout be fixed?", "Sometimes a cover-up or laser lightening first — small halos may soften over years but rarely disappear fully."),
            ("Is finger tattoo fading because of fat?", "Thin dermis and constant use matter more — but any ink driven Too deep: pigment can spread beyond the intended line, increasing the risk of blurred edges or tattoo blowout and causing unnecessary tissue trauma.
            ("Do weight-loss injections affect tattoos?", "Medications that shrink fat under tattooed skin may change how the area looks — ask your prescriber and wait until treatment is stable."),
        ),
        related=("dermis", "stretch_marks", "why_tattoos_stay_forever"),
    ),
    SkinScienceTopic(
        slug_id="why_tattoos_stay_forever",
        title="Why Tattoos Stay Forever",
        intro=(
            "Tattoo permanence is not magic — it is physics and biology. Pigment particles too large "
            "for lymph to carry away get locked in the dermis, wrapped by immune cells and woven into "
            "collagen. That is the whole reason tattoos outlast skin surface renewal."
        ),
        meta_description=(
            "Why tattoos are permanent — dermal ink trapping, immune response, particle size, and what "
            "can still fade over decades. Joshua Cole, Work of Art Las Vegas."
        ),
        category="permanence",
        joshua_quote=(
            "Clients ask if we 'inject' ink like a vaccine — we deposit insoluble particles the body "
            "cannot fully remove. Your immune system learns to wall them off instead of clearing them. "
            "That standoff is what you wear for life."
        ),
        sections=(
            ("Surface skin vs permanent ink", (
                "Epidermis replaces itself continuously — anything only in that layer disappears.",
                "Dermis has no equivalent full shed — repairs in place around foreign material.",
                "Laser removal works by shattering particles small enough for lymph to finally flush.",
            )),
            ("Particle size and pigment chemistry", (
                "Modern tattoo inks use insoluble pigments suspended in carriers — not dye that dissolves.",
                "Particles range roughly 0.02–2 microns — above the threshold easy lymph clearance.",
                "Carbon black and iron-based pigments are especially stable; some organics fade faster in UV.",
            )),
            ("The immune system's role", (
                "Macrophages engulf ink at the wound — see our dedicated macrophage guide.",
                "Fibroblasts lay collagen through the tattooed matrix — locking particles in place.",
                "Decades of sun and aging change how ink looks without necessarily removing it.",
            )),
            ("What still changes over time", (
                "UV breaks down some pigment bonds — yellows and pastels often lighten first.",
                "Skin loses collagen and elasticity — lines soften, contrast drops slightly.",
                "Weight change, pregnancy, and surgery move skin — design edges shift with anatomy.",
            )),
            ("Not actually forever — exceptions", (
                "Cosmetic tattooing (microblading) uses smaller particles in shallower planes — intentional fade.",
                "Bad placement in epidermis-only scratch work fades in weeks.",
                "Laser, dermabrasion, and certain medical treatments can remove or lighten ink.",
            )),
        ),
        faqs=(
            ("Why don't tattoos heal away like cuts?", "Cuts close with new collagen and no large foreign particles. Tattoos deposit material the body cannot fully degrade."),
            ("Do white tattoos disappear?", "White ink uses titanium dioxide — it can yellow, fade in UV, or look like scar tissue; it is not invisible long-term."),
            ("Can my body 'reject' a tattoo like an piercing?", "True rejection is rare — more often ink was too shallow, infection damaged tissue, or allergic reaction to a specific pigment."),
        ),
        related=("macrophages", "collagen", "dermis", "aging_skin"),
    ),
    SkinScienceTopic(
        slug_id="macrophages",
        title="Macrophages — The Immune Cells That Lock Ink In",
        intro=(
            "Macrophages are the cleanup crew of your immune system — and with tattoo ink, they "
            "become the long-term storage crew. They swallow pigment, sit in the dermis for years, "
            "and pass particles to successors when they die. That cycle is central to tattoo permanence."
        ),
        meta_description=(
            "How macrophages trap tattoo pigment in the dermis — immune response, ink permanence, and "
            "what it means for healing. Skin science guide, Work of Art Las Vegas."
        ),
        category="permanence",
        joshua_quote=(
            "Every tattoo is a controlled wound. Macrophages show up because they should — we rely on "
            "them to wall off pigment in the right layer. Healing well means giving those cells a clean "
            "job site, not picking scabs and not soaking in dirty water."
        ),
        sections=(
            ("What macrophages normally do", (
                "White blood cells that engulf pathogens, debris, and foreign particles.",
                "Present in acute inflammation within minutes of needle trauma.",
                "Coordinate with fibroblasts to transition from inflammation to repair.",
            )),
            ("Macrophages meet tattoo ink", (
                "Needling releases ink particles into interstitial fluid — macrophages phagocytose them.",
                "Some pigment travels to lymph nodes — especially carbon — visible on scans in heavy collectors.",
                "Remaining ink sits in dermal macrophages and extracellular matrix indefinitely.",
            )),
            ("The 'pass the baton' model", (
                "Macrophages live months to years — not forever.",
                "When one dies, another can inherit engulfed pigment — continuity of color.",
                "Research using fluorescent tracing in mice confirmed this handoff — human data aligns.",
            )),
            ("Healing implications for clients", (
                "Infection redirects macrophages to bacteria — ink settlement suffers, scarring rises.",
                "Overworked skin in one session creates excess debris — more inflammation, slower clarity.",
                "Good aftercare reduces unnecessary immune escalation — gentle wash, breathable healing.",
            )),
            ("Allergies and pigment reactions", (
                "Rare hypersensitivity to specific colors (often red) can activate macrophages differently.",
                "Granulomatous bumps may form — see a dermatologist; we may patch-test or avoid a pigment.",
                "Not the same as normal healing bumps — timing and distribution differ.",
            )),
        ),
        faqs=(
            ("Do tattoos show up in lymph nodes?", "Carbon and some pigments migrate to regional nodes — usually harmless but documented in imaging studies."),
            ("Does a strong immune system fade tattoos faster?", "Not in a meaningful way for healed work — clearance of large particles is structurally limited."),
            ("Why does my tattoo itch months later?", "Histamine and dry skin often cause itch — not always immune activity. Persistent raised areas warrant a derm check."),
        ),
        related=("why_tattoos_stay_forever", "collagen", "dermis"),
    ),
    SkinScienceTopic(
        slug_id="collagen",
        title="Collagen — Structure That Holds Your Tattoo Together",
        intro=(
            "Collagen is the scaffold of the dermis — rope-like proteins that give skin strength. "
            "When we tattoo, we disrupt collagen bundles and trigger new formation around ink. "
            "That remodeled matrix is part of why your design stays put — and why scar tissue tattoos differently."
        ),
        meta_description=(
            "Collagen and tattoos — dermal scaffold, healing, scarring, and how structure affects "
            "line clarity over time. Work of Art Las Vegas skin science."
        ),
        category="permanence",
        joshua_quote=(
            "I think about collagen like canvas weave — tight and even holds fine detail; damaged or "
            "cross-hatched scar tissue drinks ink unpredictably. That is why I map scars before any cover-up consult."
        ),
        sections=(
            ("Collagen basics", (
                "Most abundant protein in skin — Types I and III dominate the dermis.",
                "Organized in parallel bundles in healthy skin; cross-linked for tensile strength.",
                "Production slows with age — skin thins, elasticity drops, tattoo contrast shifts.",
            )),
            ("Tattooing disrupts and rebuilds collagen", (
                "Needles shear through existing fibers — controlled micro-injury.",
                "Fibroblasts deposit new collagen over 6–12+ months — maturation parallels tattoo settle.",
                "Ink particles sit among fibers and cells — mechanically locked in the matrix.",
            )),
            ("Collagen quality and line clarity", (
                "Dense, healthy dermis holds crisp edges — why placement on firm skin ages well.",
                "Sun damage breaks collagen ( photoaging) — tattoos on sun-leathered chests blur faster.",
                "Hydration and SPF support collagen long-term — desert clients need both.",
            )),
            ("Scar collagen vs normal collagen", (
                "Scars lay Type III collagen first — disorganized, dense, poor elasticity.",
                "Ink in scar tissue follows fracture lines — patchy saturation, color shift.",
                "See our scar tissue tattoo guide for consult requirements.",
            )),
            ("Supplements and skincare — realistic expectations", (
                "Oral collagen supplements have mixed evidence for skin — not a tattoo cure-all.",
                "Topical retinoids thicken epidermis and increase cell turnover — avoid on fresh tattoos.",
                "Microneedling on tattooed skin is a medical decision — can disturb pigment.",
            )),
        ),
        faqs=(
            ("Does collagen cream help healed tattoos?", "Moisturizing helps appearance; collagen molecules in creams do not rebuild dermis meaningfully."),
            ("Why did my fine lines blur after weightlifting gains?", "Rapid dermal stretch can redistribute ink slightly — slow bulk/cut cycles are gentler on large pieces."),
            ("Can building muscle distort a tattoo?", "Muscle growth moves skin — designs on outer deltoid or thigh can shift subtly; plan large work accordingly."),
        ),
        related=("scar_tissue_tattoo", "dermis", "aging_skin", "macrophages"),
    ),
    SkinScienceTopic(
        slug_id="scar_tissue_tattoo",
        title="Why Scar Tissue Tattoos Differently",
        intro=(
            "Scar tissue is remodeled dermis — collagen laid down fast after injury, not the organized "
            "matrix of untouched skin. Tattooing scars is often possible and beautiful, but saturation, "
            "texture, and pain differ. We plan accordingly."
        ),
        meta_description=(
            "Tattooing over scar tissue — collagen structure, ink retention, timing, and cover-up "
            "planning at Work of Art Las Vegas. Studio education, not medical advice."
        ),
        category="conditions",
        medical=True,
        joshua_quote=(
            "I have covered surgical scars and self-harm scars with dignity — but only when the tissue "
            "is mature, flat, and stable. Rushing a tattoo on a fresh scar is how you get a third problem "
            "on top of the first two."
        ),
        sections=(
            ("How scar tissue differs from normal skin", (
                "Disorganized collagen bundles — denser, less elastic, often lighter or pinker.",
                "Reduced blood flow in some scars — slower heal, uneven ink uptake.",
                "Texture may be raised ( hypertrophic) or sunken ( atrophic) — each behaves differently.",
            )),
            ("When we will tattoo a scar", (
                "Generally wait 12–24 months after injury or surgery — surgeon clearance if applicable.",
                "Scar should be fully matured: no active redness, no widening, no frequent breakdown.",
                "Client understands touch-ups are likely — scar tissue rarely takes ink in one pass.",
            )),
            ("Technique adjustments in the chair", (
                "Multiple light passes instead of one heavy saturation.",
                "Test spot or small section first on large or unpredictable scars.",
                "Soft shading and botanicals often outperform tight realism on heavy texture.",
            )),
            ("Cover-ups on scarred skin", (
                "Scars add another variable to opacity planning — we need more room than on smooth skin.",
                "Stretching from weight change can reopen texture — stable weight helps.",
                "See our cover-up authority guide for session mapping.",
            )),
            ("When we refer out", (
                "Keloid-prone history with new raised growth — dermatology before any tattoo.",
                "Active inflammatory scars or ongoing treatment — wait.",
                "Scars over implants or radiation fields — physician clearance required.",
            )),
        ),
        faqs=(
            ("Will tattooing hide scar texture?", "Ink adds color — not always flatness. Microneedling and medical scar treatment may help texture first."),
            ("Does it hurt more on scars?", "Often yes — fewer nerve endings in dense scar, but some clients report sharp sensitivity; others feel less."),
            ("Can you tattoo over self-harm scars?", "Often yes, with compassion and a consult — we discuss readiness, design, and aftercare without judgment."),
        ),
        related=("collagen", "stretch_marks", "why_tattoos_stay_forever"),
    ),
    SkinScienceTopic(
        slug_id="stretch_marks",
        title="Stretch Marks & Tattoo Planning",
        intro=(
            "Stretch marks ( striae) are dermal tears — collagen and elastin rupture faster than skin "
            "can repair. They are not scars exactly, but they tattoo differently: ink may sit unevenly "
            "across thinned, textured bands."
        ),
        meta_description=(
            "Tattooing over stretch marks — striae anatomy, timing after pregnancy or weight change, "
            "and design strategies. Work of Art Las Vegas."
        ),
        category="conditions",
        medical=True,
        joshua_quote=(
            "I have wrapped stretch marks into larger compositions — florals, geometry, black and grey "
            "flow — so the skin reads as one piece instead of a patch job. Honest expectations beat "
            "promising invisibility."
        ),
        sections=(
            ("What stretch marks are", (
                "Rupture of dermis with intact epidermis — often start red/purple ( striae rubra), fade white ( striae alba).",
                "Common on abdomen, hips, thighs, upper arms after growth spurts, pregnancy, or rapid weight change.",
                "Texture is lower than surrounding skin — ink absorption varies across the mark.",
            )),
            ("Timing a tattoo", (
                "Wait until marks have faded to pale/white and skin volume is stable.",
                "Post-pregnancy: often 12+ months after delivery and after breastfeeding if applicable.",
                "Recent weight loss: maintain stable weight several months before large abdominal work.",
            )),
            ("Design strategies that work", (
                "Incorporate marks into the design flow — not just tattooing 'over' them like a band-aid.",
                "Soft gradients and organic shapes hide edge transitions better than hard geometric lines.",
                "Color may look patchy inside striae — test spots or desaturated palettes help.",
            )),
            ("Pregnancy and future changes", (
                "A belly piece may distort with another pregnancy — plan with that in mind.",
                "Fine line over striae is higher risk for blur — bolder values hold better.",
            )),
            ("Las Vegas climate note", (
                "Dry heat can emphasize skin texture — moisturized healed skin reads smoother.",
                "Sun darkens surrounding skin while striae stay lighter — SPF evens appearance around work.",
            )),
        ),
        faqs=(
            ("Can tattoos prevent stretch marks?", "No — tattoos do not strengthen dermis. Hydration and gradual weight change help prevention, not ink."),
            ("Will color look even across stretch marks?", "Often slightly uneven — we build that into the design and may touch up after heal."),
            ("Are red stretch marks safe to tattoo?", "Better to wait until they mature — active striae rubra heal slower and unpredictably."),
        ),
        related=("scar_tissue_tattoo", "collagen", "hypodermis"),
    ),
    SkinScienceTopic(
        slug_id="eczema",
        title="Eczema (Atopic Dermatitis) & Tattoos",
        intro=(
            "Eczema is chronic inflammation of the skin barrier — flares, itch, and patches that cycle "
            "unpredictably. Tattooing during a flare is a bad idea; tattooing on well-controlled skin "
            "may be possible with dermatologist input and extra aftercare planning."
        ),
        meta_description=(
            "Eczema and tattoos — flares, barrier repair, when to wait, and studio safety. Consult "
            "your dermatologist; Work of Art Las Vegas education guide."
        ),
        category="conditions",
        medical=True,
        joshua_quote=(
            "I will not tattoo active eczema — the barrier is compromised and healing fights itself. "
            "When a client is clear for months and their derm agrees, we pick placement away from "
            "usual flare zones and baby the aftercare."
        ),
        sections=(
            ("What eczema does to skin", (
                "Impaired epidermal barrier — water loss, allergen entry, itch-scratch cycles.",
                "Inflammation thickens or thins skin depending on chronicity and scratching.",
                "Common sites: inner elbows, knees, hands, neck — high-friction tattoo areas.",
            )),
            ("Risks of tattooing with eczema", (
                "Koebner phenomenon — new trauma can trigger eczema in new locations.",
                "Flare during heal mimics infection — redness, oozing, itch — harder to manage.",
                "Patchy ink if skin sheds excessively during heal.",
            )),
            ("When we may proceed", (
                "No active flare on or near the tattoo site for several months.",
                "Written or verbal clearance from treating dermatologist for invasive procedures.",
                "Client has a rescue plan ( prescribed cream) if post-tattoo irritation starts.",
            )),
            ("Aftercare modifications", (
                "Avoid fragranced products entirely — use derm-approved bland moisturizer.",
                "Short showers, lukewarm water — long hot showers trigger many eczema clients.",
                "Loose breathable clothing — wool and synthetic heat against fresh work.",
            )),
            ("Desert climate considerations", (
                "Las Vegas dry air worsens barrier dryness — humidifier at home during heal helps.",
                "Air conditioning strips moisture — lotion more often than generic aftercare cards suggest.",
            )),
        ),
        faqs=(
            ("Will tattoo ink cause eczema?", "Rare pigment allergy is possible — unrelated to atopic eczema but worth knowing. Patch testing exists for high-risk clients."),
            ("Can I use steroid cream on a healing tattoo?", "Only if your dermatologist directs — steroids suppress heal and can affect ink. Never self-prescribe on fresh work."),
            ("Is black ink safer for eczema skin?", "No guaranteed safe color — barrier health matters more than pigment hue."),
        ),
        related=("psoriasis", "epidermis", "dermis"),
    ),
    SkinScienceTopic(
        slug_id="psoriasis",
        title="Psoriasis & Tattoo Safety",
        intro=(
            "Psoriasis is an immune-mediated condition — rapid skin cell turnover, plaques, and Koebner "
            "response where trauma triggers new lesions. Tattooing requires dermatologist clearance, "
            "stable disease, and acceptance of unique risks."
        ),
        meta_description=(
            "Psoriasis and tattoos — Koebner phenomenon, flares, biologics, and when tattooing may "
            "be considered. Not medical advice — Work of Art Las Vegas."
        ),
        category="conditions",
        medical=True,
        joshua_quote=(
            "Psoriasis clients deserve honesty: a tattoo is trauma, and trauma can seed plaques. "
            "If your skin has been quiet a long time and your rheumatologist or derm says go — we "
            "plan small, watch heal closely, and stop if anything spreads."
        ),
        sections=(
            ("Psoriasis basics for tattoo planning", (
                "Accelerated keratinocyte turnover — plaques with silvery scale on elbows, knees, scalp, lower back.",
                "Koebner phenomenon — cuts, piercings, and tattoos can trigger lesions along the injury line.",
                "Systemic treatments ( biologics, methotrexate) affect immune heal — timing matters.",
            )),
            ("Medications and timing", (
                "Biologic immunosuppressants — surgeon/derm often require holding for elective procedures; follow prescriber rules.",
                "Topical steroids on planned site — stop before tattoo per derm instruction.",
                "Recent phototherapy — skin sensitivity elevated; wait until derm clears.",
            )),
            ("Studio criteria", (
                "Stable psoriasis without new plaques for 6–12+ months.",
                "No active lesions on tattoo site or within likely Koebner spread zone.",
                "Written clearance when on systemic therapy.",
            )),
            ("Healing watchpoints", (
                "Plaque forming along tattoo outline — contact dermatology promptly.",
                "Do not pick scales on or near fresh tattoo — increases scarring and ink loss.",
                "Aftercare stays gentle — no aggressive scrubbing or alcohol-based products.",
            )),
            ("Design and placement", (
                "Avoid known plaque-prone areas if possible — inner elbow tattoos on elbow psoriasis history is high risk.",
                "Smaller initial work tests Koebner response before committing to a back piece.",
            )),
        ),
        faqs=(
            ("Will tattoos make psoriasis spread?", "They can trigger Koebner lesions in susceptible people — not guaranteed, but risk is real."),
            ("Can I tattoo if I am on Humira or Stelara?", "Only with prescriber clearance — holding medication may be required."),
            ("Does psoriasis ruin existing tattoos?", "Plaques over ink can alter texture and color; treating psoriasis helps preserve the art."),
        ),
        related=("eczema", "macrophages", "scar_tissue_tattoo"),
    ),
    SkinScienceTopic(
        slug_id="diabetes",
        title="Diabetes — Skin Healing & Tattoo Considerations",
        intro=(
            "Diabetes affects blood flow, nerve sensation, and infection risk — all relevant to tattoo "
            "healing. Well-controlled diabetes is not an automatic no, but it demands clinician "
            "clearance, realistic timelines, and stricter aftercare."
        ),
        meta_description=(
            "Diabetes and tattoos — healing risk, blood sugar control, neuropathy, and studio "
            "requirements. Consult your doctor; Work of Art Las Vegas guide."
        ),
        category="conditions",
        medical=True,
        joshua_quote=(
            "I ask every client with diabetes about A1C, foot neuropathy, and who manages their care. "
            "Tattooing feet or shins with numbness is how small infections become emergencies — "
            "we decline those placements when sensation is gone."
        ),
        sections=(
            ("How diabetes affects skin heal", (
                "Elevated glucose impairs white blood cell function — slower fight against bacteria.",
                "Peripheral vascular disease reduces blood flow to extremities — lower leg and foot heal worst.",
                "Neuropathy hides pain from early infection — client may not feel warning signs.",
            )),
            ("When tattooing may be considered", (
                "Stable, well-controlled blood sugar — many studios ask A1C under 8% with derm/PCP OK.",
                "No active ulcers, open wounds, or infections on or near the site.",
                "Client monitors glucose during heal and knows sick-day rules.",
            )),
            ("High-risk placements we avoid", (
                "Feet, toes, and lower legs with neuropathy or poor circulation.",
                "Injection sites that bruise easily without sensation feedback.",
                "Areas with diabetic dermopathy spots — tattooing may mask skin cancer surveillance.",
            )),
            ("Aftercare for diabetic clients", (
                "Strict hygiene — wash hands before touching tattoo, clean bedding.",
                "Watch for infection signs daily — redness spreading, odor, fever — doctor same day.",
                "Avoid soaking — pools, hot tubs, long baths until fully healed.",
            )),
            ("Las Vegas lifestyle factors", (
                "Heat and dehydration can swing glucose — hydrate and monitor during heal weeks.",
                "Long casino nights can disrupt sleep and glucose — plan heal when routine is stable.",
            )),
        ),
        faqs=(
            ("Do I need a doctor's note?", "Often yes for Type 1, insulin pumps, or history of heal complications — we decide case by case."),
            ("Does diabetes make tattoos fade faster?", "Poor heal can affect ink retention — control matters more than the diagnosis itself."),
            ("Can I get a CGM sensor area tattooed?", "Avoid — needs clear skin for adhesion and sensor accuracy."),
        ),
        related=("epidermis", "macrophages", "eczema"),
    ),
    SkinScienceTopic(
        slug_id="aging_skin",
        title="Aging Skin & Long-Term Tattoo Clarity",
        intro=(
            "Skin ages — collagen thins, elastin fails, sun damage accumulates. Tattoos age with it: "
            "lines soften, contrast drops, and placement that looked perfect at 25 reads different at "
            "55. Planning ahead beats chasing youth later."
        ),
        meta_description=(
            "How aging skin affects tattoos — collagen loss, sun damage, placement, and design choices "
            "for longevity. Joshua Cole, Work of Art Las Vegas skin science."
        ),
        category="permanence",
        joshua_quote=(
            "I design for the body you will have in twenty years — not just the mirror today. Bold "
            "hierarchy, generous spacing, and sun discipline beat ultra-micro detail that cannot "
            "survive thin, sun-exposed skin."
        ),
        sections=(
            ("Structural changes over decades", (
                "Collagen production drops ~1% per year after mid-20s — dermis thins gradually.",
                "Elastin loss — skin sags and stretches; large pieces move with gravity.",
                "Sebaceous glands reduce output — dry skin, more visible texture.",
            )),
            ("Photoaging and tattoos", (
                "UV breaks collagen and fades pigment — Nevada sun is relentless on chest, shoulders, forearms.",
                "Freckles and solar lentigines appear around — not through — older ink.",
                "Daily SPF 30+ on exposed tattoos is the cheapest anti-aging tool.",
            )),
            ("Design choices that age well", (
                "Slightly bolder line weight than Instagram micro-trends — readable at social distance for life.",
                "High-contrast black and grey realism holds value structure when color mellows.",
                "Avoid crowding finger spaces and paper-thin inner-wrist bands on mature skin.",
            )),
            ("Placement by decade", (
                "20s–30s: most sites viable — still plan for pregnancy, career, and sun habits.",
                "40s–50s: prefer areas with stable dermis ( outer upper arm, thigh, upper back).",
                "60s+: thinner skin needs lighter hand, possibly fewer sessions — consult honestly.",
            )),
            ("Skincare interactions", (
                "Retinoids increase turnover — can brighten surrounding skin and alter contrast near tattoos.",
                "Cosmetic procedures ( lasers, peels) can affect pigment — tell your provider about ink.",
            )),
        ),
        desert_bullets=(
            "Year-round UV in Las Vegas accelerates photoaging on driver-side arm and chest — SPF every day.",
            "Desert dryness emphasizes fine lines — hydrated skin shows tattoos cleaner at every age.",
        ),
        faqs=(
            ("Will my tattoo look bad when I am old?", "It will look different — like any art on a living surface. Good design, depth, and sun care keep it dignified."),
            ("Should older clients avoid color?", "Not necessarily — expect softer saturation long-term; black and grey may need fewer touch-ups."),
            ("Can I get my first tattoo at 60?", "Yes — heal may be slightly slower; we adjust session length and aftercare. Medical clearance if on blood thinners."),
        ),
        related=("collagen", "epidermis", "why_tattoos_stay_forever"),
    ),
)