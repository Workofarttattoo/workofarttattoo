#!/usr/bin/env python3
"""Piercing-type authority catalog — healing, pain, quirks, Katelyn Cole voice."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CategoryId = Literal["ear", "facial", "body", "not_offered"]

HUB_SLUG = "piercing_types_las_vegas_authority_hub"
HUB_TITLE = "Complete Piercing Guide — Las Vegas"
HUB_INTRO = (
    "One definitive guide per placement — not hundreds of thin pages. Pillars organize ear, facial, oral, "
    "and body work; every cluster page follows the same structure and is reviewed by Katelyn Cole."
)

PIERCING_HUB = "/best_piercing_shop_las_vegas_updated_jewelry_standards/"
KATELYN_PAGE = "/artists/katelyn-cole/"
BOOK = "/appointments/"


@dataclass(frozen=True)
class PiercingGuide:
    slug_id: str
    name: str
    category: CategoryId
    offered: bool
    offer_note: str
    healing_time: str
    pain_score: int
    pain_label: str
    intro: str
    quirks: tuple[str, ...]
    tips: tuple[str, ...]
    jewelry_notes: str
    aftercare_summary: str
    faqs: tuple[tuple[str, str], ...] = ()
    related: tuple[str, ...] = ()


def slug_for(guide: PiercingGuide) -> str:
    sid = guide.slug_id
    if sid.endswith("_piercing"):
        return f"{sid}_las_vegas_authority_guide"
    return f"{sid}_piercing_las_vegas_authority_guide"


def _piercing_phrase(name: str) -> str:
    """Avoid 'Ear Piercing Piercing' in titles and meta."""
    low = name.lower()
    if low.endswith(" piercing") or low.endswith(" piercings"):
        return name
    return f"{name} Piercing"


def page_title(guide: PiercingGuide) -> str:
    from woa_piercing_complete_guides import complete_page_title

    return complete_page_title(guide)


def meta_description(guide: PiercingGuide) -> str:
    from woa_piercing_seo import meta_description as seo_desc

    return seo_desc(guide)


# Shared voice fragments
VEGAS_DRY = (
    "Las Vegas is dry — your crusties will feel tighter than in humid climates. "
    "Do not pick them; let saline do the work."
)
DOWNSIZE = "I schedule a downsizing check around 6–8 weeks when swelling is gone — shorter posts prevent angle irritation."
IMPLANT = "Fresh piercings start with properly fitted starter jewelry — never mystery metal from a kiosk."


PIERCING_CATALOG: tuple[PiercingGuide, ...] = (
    PiercingGuide(
        slug_id="ear_lobe",
        name="Lobe Piercing",
        category="ear",
        offered=True,
        offer_note="Yes — walk-in friendly when the schedule allows; minors 14+ with guardian for ear work.",
        healing_time="6–8 weeks for initial heal; 3 months before heavy hoops or stretching",
        pain_score=2,
        pain_label="Quick pinch — most clients say it is easier than they expected",
        intro=(
            "Ear lobes are where most people start — and they should be done with a sterile needle, not a gun. "
            "I pierce lobes every week in-studio: symmetrical marks, well-fitted studs, and aftercare you can "
            "actually follow in Vegas heat."
        ),
        quirks=(
            "Sleeping on a fresh lobe causes bumps fast — keep pressure off for the first two weeks.",
            "Cheap butterfly-back earrings trap bacteria; I use flat-back labret-style posts for healing.",
            "Second holes need spacing planned if you are building toward a curated ear later.",
        ),
        tips=(
            "I mark both ears standing and sitting — your anatomy shifts, and symmetry matters.",
            "If you are planning multiple piercings, tell me now so we leave room for future conch or helix work.",
            "Spray sterile saline 1–2 times daily; no twisting the jewelry — that micro-tears the fistula.",
            DOWNSIZE,
        ),
        jewelry_notes=IMPLANT + " Starter studs are slightly long for swelling; we downsize once healed enough.",
        aftercare_summary=(
            "Saline mist, hands off, no pools or hot tubs for 4–6 weeks. "
            + VEGAS_DRY
        ),
        faqs=(
            (
                f"How long until I can change my ear lobe piercing jewelry?",
                "Wait until the fistula feels stable — usually 6–8 weeks minimum. "
                "Come in for a check if you want to swap to gold or a hoop; I will tell you if you are ready.",
            ),
            (
                "Can kids get ear piercings at Work of Art?",
                "Ear piercings for minors 14+ with a parent or guardian present — ID required. "
                "We focus on ear work for minors, not facial or body piercings.",
            ),
        ),
        related=("helix", "conch", "ear_curation"),
    ),
    PiercingGuide(
        slug_id="cartilage",
        name="Cartilage (Overview)",
        category="ear",
        offered=True,
        offer_note="Yes — helix, flat, conch, tragus, daith, rook, and industrial are all cartilage work we perform.",
        healing_time="6–12 months depending on placement; cartilage heals from the outside in",
        pain_score=5,
        pain_label="Moderate — sharp pressure, over in seconds",
        intro=(
            "Cartilage is not 'just another ear piercing.' It is thicker tissue, slower blood flow, and a longer "
            "healing clock. I treat every cartilage piercing as a 6–12 month project — not a weekend accessory."
        ),
        quirks=(
            "Cartilage bumps are usually irritation, not infection — wrong angle, sleeping on it, or harsh aftercare.",
            "One side of your ear may heal slower; do not compare timelines ear-to-ear.",
            "Helix, flat, and conch all share cartilage rules but heal at different speeds — see each guide.",
        ),
        tips=(
            "I pierce cartilage with a single-use needle and guide — never a piercing gun (guns shatter cartilage).",
            "Book one cartilage piercing at a time unless we are planning a staged curation map.",
            "No headphones pressed on fresh helix or conch work for at least 4 weeks.",
            "If a bump appears, come in before you start random tea-tree or aspirin paste from the internet.",
        ),
        jewelry_notes=(
            "Flat-back labret posts or barbells sized for your anatomy — never tight rings on fresh cartilage."
        ),
        aftercare_summary="Saline only, no rotation, protect from snags and pressure. " + VEGAS_DRY,
        faqs=(
            (
                "Why does cartilage take so long to heal?",
                "Cartilage has less blood supply than lobes. The fistula forms slowly from the entry outward — "
                "rush the timeline and you get bumps, migration, or scarring.",
            ),
        ),
        related=("helix", "conch", "daith", "industrial"),
    ),
    PiercingGuide(
        slug_id="helix",
        name="Helix",
        category="ear",
        offered=True,
        offer_note="Yes — outer rim helix and stacked helix work are common in my ear curation consults.",
        healing_time="6–9 months; up to 12 months for stacked or multiple helix points",
        pain_score=5,
        pain_label="Moderate pinch with brief pressure",
        intro=(
            "Helix piercings sit on the outer rim — one of the most popular cartilage placements I do. "
            "They photograph beautifully, but they hate pressure from headphones, glasses arms, and side-sleeping."
        ),
        quirks=(
            "The upper helix has less flesh — jewelry must sit flush or the post angles into the rim.",
            "Double helix stacks need vertical spacing so posts do not collide inside the ear.",
            "Hair caught around a helix stud is the number-one snag complaint I hear at downsizing.",
        ),
        tips=(
            "I mark helix piercings with you looking in the mirror — you live with the angle, not me.",
            "Tell me if you wear over-ear headphones daily; we may shift placement slightly.",
            "Downsize the post at 6–8 weeks — long starter jewelry is a helix bump factory.",
            "One helix at a time unless we are executing a planned multi-month curation.",
        ),
        jewelry_notes="Flat-back labret or ring after heal — rings too early cause migration on the rim.",
        aftercare_summary="Saline mist twice daily, no twisting, keep hair and headphones away. " + VEGAS_DRY,
        related=("tragus", "conch", "rook", "flat", "ear_curation"),
    ),
    PiercingGuide(
        slug_id="forward_helix",
        name="Forward Helix",
        category="ear",
        offered=True,
        offer_note="Yes — anatomy-dependent; I will tell you honestly if your forward helix has enough shelf.",
        healing_time="6–9 months",
        pain_score=6,
        pain_label="Moderate to sharp — thin cartilage at the front of the ear",
        intro=(
            "Forward helix sits on the small ridge facing your face — delicate, visible, and anatomy-specific. "
            "Not every ear has a safe shelf for this piercing, and I would rather say no than pierce into a bad angle."
        ),
        quirks=(
            "Very shallow anatomy leads to migration — I assess the ridge thickness before we commit.",
            "Glasses and mask loops rub this area constantly; plan accordingly.",
            "Often paired with tragus or conch in curated ears — spacing is everything.",
        ),
        tips=(
            "I use a fine labret post and mark from the side and front — dual views prevent a crooked forward helix.",
            "If the ridge is thin, I will suggest helix or flat instead — same aesthetic, safer heal.",
            "Sleep on the opposite side for at least 8 weeks; a travel pillow helps.",
        ),
        jewelry_notes="Tiny flat-back studs only for healing — decorative ends after the fistula is stable.",
        aftercare_summary="Minimal touch, saline spray, keep glasses clean where they contact the ear.",
        related=("helix", "tragus", "ear_curation"),
    ),
    PiercingGuide(
        slug_id="flat",
        name="Flat",
        category="ear",
        offered=True,
        offer_note="Yes — flat helix (scapha) piercings are a staple of curated ear designs in my chair.",
        healing_time="8–12 months",
        pain_score=6,
        pain_label="Moderate — firm cartilage on the flat plane of the ear",
        intro=(
            "Flat piercings sit on the wide plane between the helix and conch — perfect for a gem that faces outward "
            "in photos. They need precise angle and a post long enough for swelling without sticking out like a antenna."
        ),
        quirks=(
            "Wrong angle makes the flat look 'tilted' in every selfie — I take extra time on the mark.",
            "Multiple flats in one ear need horizontal spacing to avoid shared swelling channels.",
            "Bump risk rises if you sleep on the ear before downsizing.",
        ),
        tips=(
            "I pierce flats perpendicular to the tissue plane — not toward the head, not toward the rim.",
            "Plan your curation map before a flat goes in; moving it later leaves a scar.",
            "Come back for downsizing — flats look best with a snug post once swelling drops.",
        ),
        jewelry_notes="Flat-back labret with a low-profile end — no rings until fully healed.",
        aftercare_summary="Saline, no pressure, staged downsizing at 6–8 weeks.",
        related=("helix", "conch", "ear_curation"),
    ),
    PiercingGuide(
        slug_id="conch",
        name="Conch",
        category="ear",
        offered=True,
        offer_note="Yes — inner and outer conch, studs or (after heal) rings.",
        healing_time="6–12 months; outer conch often heals faster than inner",
        pain_score=7,
        pain_label="Moderate to firm — deep cartilage pressure",
        intro=(
            "Conch piercings go through the cup of the ear — inner or outer. They are bold, they heal slowly, "
            "and they are one of my favorite placements when the anatomy supports a clean 90-degree angle."
        ),
        quirks=(
            "Inner conch can interfere with earbuds — tell me about your daily headphones.",
            "Large decorative ends on a fresh conch add weight and delay healing.",
            "Outer conch rings are gorgeous healed but risky as starter jewelry.",
        ),
        tips=(
            "I distinguish inner vs outer conch on the mark — they heal differently and look different in curation.",
            "Starter jewelry is a labret, not a ring — rings twist and cause bumps on fresh conch work.",
            "If you want a conch ring eventually, we plan diameter at consult so you are not disappointed later.",
        ),
        jewelry_notes="Flat-back labret; gem size chosen for weight as well as look.",
        aftercare_summary="Strict no-touch, saline spray, no in-ear headphones on inner conch for 6+ weeks.",
        related=("flat", "daith", "ear_curation"),
    ),
    PiercingGuide(
        slug_id="tragus",
        name="Tragus",
        category="ear",
        offered=True,
        offer_note="Yes — anatomy check required; tiny tragus may need a smaller gauge or alternative placement.",
        healing_time="6–9 months",
        pain_score=6,
        pain_label="Moderate — short crunch, then done",
        intro=(
            "Tragus piercings frame the ear canal opening — subtle, elegant, and surprisingly fussy about earbuds "
            "and phone habits. I love them in curated ears paired with conch or forward helix."
        ),
        quirks=(
            "Bluetooth earbuds sit right on a healing tragus — expect irritation if you wear them daily.",
            "Very small tragus anatomy may not safely hold standard gauge — I size honestly.",
            "Hair behind the ear snags the post tail if jewelry is too long pre-downsize.",
        ),
        tips=(
            "I mark the tragus with your jaw relaxed — clenching changes the tissue position.",
            "Use over-ear headphones or one side only during early healing.",
            "Downsize early if the post sticks out — tragus bumps love long jewelry.",
        ),
        jewelry_notes="Micro flat-back labret; decorative ends after downsizing.",
        aftercare_summary="Saline mist, no earbuds in the canal side for 4–6 weeks minimum.",
        related=("daith", "forward_helix", "ear_curation"),
    ),
    PiercingGuide(
        slug_id="daith",
        name="Daith",
        category="ear",
        offered=True,
        offer_note="Yes — I perform daith piercings when the fold is deep enough for a safe angle.",
        healing_time="6–9 months; sometimes up to 12 months",
        pain_score=7,
        pain_label="Firm pressure — the fold is thick cartilage",
        intro=(
            "Daith piercings pass through the innermost cartilage fold. They are iconic for hoops and curated "
            "ears, but anatomy varies wildly — a shallow fold means I may recommend a different placement."
        ),
        quirks=(
            "Not every ear has a pierceable daith fold — I will decline rather than force it.",
            "Hoops as starter jewelry are a common mistake; I start with a curved bar or ring sized for swelling.",
            "Migraine claims are anecdotal — I pierce daith for anatomy and aesthetics, not medical promises.",
        ),
        tips=(
            "I use a receiving tube or precise clamp technique — daith requires control in a tight space.",
            "Keep shampoo and face wash residue off the fold; product buildup irritates daith piercings fast.",
            "Sleep with a donut pillow — daith and pillow pressure are enemies.",
        ),
        jewelry_notes="Curved barbell or ring sized for your fold depth — never tight captive rings on day one.",
        aftercare_summary="Saline, no picking crust in the fold, downsizing when swelling allows.",
        related=("conch", "rook", "ear_curation"),
    ),
    PiercingGuide(
        slug_id="rook",
        name="Rook",
        category="ear",
        offered=True,
        offer_note="Yes — one of the trickier cartilage placements; I assess fold depth before booking.",
        healing_time="9–12 months",
        pain_score=8,
        pain_label="Firm to sharp — dense fold cartilage",
        intro=(
            "Rook piercings sit in the antihelix fold above the daith — vertical, finicky, and worth the wait when "
            "healed. They are not for impatient healers or side-sleepers who will not change habits."
        ),
        quirks=(
            "Healing bumps on rook are common with sleeping pressure — plan a pillow strategy.",
            "Curved barbells fit the fold better than straight posts — I match jewelry to anatomy.",
            "Long healing means one rook project at a time per ear.",
        ),
        tips=(
            "I mark rook piercings lying down and upright — the fold moves.",
            "Do not change your own rook jewelry for at least 6 months unless I check it.",
            "If irritation starts, swap habits before swapping jewelry — pressure is usually the cause.",
        ),
        jewelry_notes="Curved barbell; decorative ends after heal.",
        aftercare_summary="Saline, strict side-sleeping avoidance, patience — rook rewards slow healers.",
        related=("daith", "flat", "ear_curation"),
    ),
    PiercingGuide(
        slug_id="industrial",
        name="Industrial",
        category="ear",
        offered=True,
        offer_note="Yes — custom bar length and angle; both holes pierced in one session when anatomy allows.",
        healing_time="9–12 months minimum; sometimes 12–18 months",
        pain_score=8,
        pain_label="Two piercings back-to-back — firm cartilage twice",
        intro=(
            "An industrial connects two cartilage points with one bar — helix-to-helix or variant angles. "
            "It is a statement piece and a commitment: two wounds, one bar, zero room for sloppy aftercare."
        ),
        quirks=(
            "Ear shape must allow a bar without tension — tension causes migration and scarring.",
            "Hair, hoodies, and car headrests snag industrials constantly during healing.",
            "One irritated hole affects the whole bar — you cannot heal them independently.",
        ),
        tips=(
            "I measure your ear for bar length and angle before we pierce — not all ears suit a classic industrial.",
            "Start with longer bar for swelling; downsize bar length at 8–12 weeks if swelling is gone.",
            "Clean both entry points equally; do not ignore the hole you cannot see in the mirror.",
            "No sleeping on the ear — non-negotiable for industrial healing.",
        ),
        jewelry_notes="Industrial bar fitted to your anatomy; decorative ends optional after initial heal.",
        aftercare_summary="Saline both holes, no twisting the bar, downsizing appointment required.",
        related=("helix", "cartilage", "ear_curation"),
    ),
    PiercingGuide(
        slug_id="ear_curation",
        name="Ear Curation",
        category="ear",
        offered=True,
        offer_note="Yes — this is my specialty: mapping multiple piercings, metal, and jewelry scale over time.",
        healing_time="Staged over months — each piercing follows its own timeline",
        pain_score=4,
        pain_label="Varies by placement — planning session is painless",
        intro=(
            "Ear curation is not 'as many holes as possible.' It is a plan: which piercings heal first, "
            "which jewelry metals match, how gem sizes balance on your ear, and when to downsize. "
            "That is how you get a cohesive ear instead of a random collection of bumps."
        ),
        quirks=(
            "Piercing everything at once slows every heal — I stage work intentionally.",
            "Mixing cheap jewelry with premium pieces causes metal reactions on fresh holes.",
            "Instagram ears often took years — not one appointment.",
        ),
        tips=(
            "Bring reference photos, but trust my anatomy read — your ear is not the same as the photo.",
            "We pick a 'hero' piercing first (often conch or helix), then build around it after downsizing.",
            "I document your curation map in consult notes — symmetry, metal, and order of work.",
            "Budget for quality jewelry upfront; swapping cheap studs later costs more in bump visits.",
        ),
        jewelry_notes="Properly fitted jewelry for fresh and healed piercings.",
        aftercare_summary="Follow each placement's guide; one irritated piercing can pause the whole curation plan.",
        faqs=(
            (
                "How many piercings can I get at once?",
                "Usually one or two cartilage piercings per session, depending on placement and your heal history. "
                "Lobes can sometimes pair with one cartilage if we plan sleep and aftercare carefully.",
            ),
        ),
        related=("helix", "conch", "flat", "daith"),
    ),
    PiercingGuide(
        slug_id="nostril",
        name="Nostril",
        category="facial",
        offered=True,
        offer_note="Yes — left, right, or both; high nostril available on anatomy consult.",
        healing_time="4–6 months",
        pain_score=4,
        pain_label="Quick sharp pinch — eyes may water",
        intro=(
            "Nostril piercings are classic for a reason — small, striking, and manageable when you respect the "
            "inside-of-the-nose healing zone. I mark for your nostril shape, not a generic dot."
        ),
        quirks=(
            "Makeup, sunscreen, and foundation migrate into fresh nostril piercings — clean around, not on.",
            "A stud that is too short embeds; too long snags on tissue — downsizing matters.",
            "Nostril piercings and colds are a bad combo — blow gently, do not rub.",
        ),
        tips=(
            "I pierce at a 90-degree angle to the tissue — not parallel to the face (that causes migration).",
            "Switch to a hoop only after full heal — premature rings cause bump scars at the rim.",
            "Tell me if you wear glasses or a CPAP mask — we adjust placement slightly if needed.",
        ),
        jewelry_notes="Flat-back labret or screw-back stud for healing; hoops after 4–6 months when stable.",
        aftercare_summary="Saline mist, no rotating, keep cosmetics away from the hole.",
        related=("septum", "philtrum", "labret"),
    ),
    PiercingGuide(
        slug_id="septum",
        name="Septum",
        category="facial",
        offered=True,
        offer_note="Yes — sweet spot technique; not everyone has ideal septum anatomy and I will tell you.",
        healing_time="6–8 weeks initial; 3–4 months for full stability",
        pain_score=5,
        pain_label="Eyes water — cartilage crunch then relief",
        intro=(
            "Septum piercings sit in the thin 'sweet spot' of soft tissue — not through hard cartilage when done "
            "correctly. You will tear up; that is normal. I use a clamp and guide for a straight channel."
        ),
        quirks=(
            "Hard septum cartilage piercing causes long heals and crooked jewelry — I avoid the bone.",
            "Flipping the ring up before heal irritates the fistula — leave it down or wear a retainer.",
            "Snot, colds, and dry Vegas air all irritate fresh septum work — saline helps.",
        ),
        tips=(
            "I find your sweet spot by feel — not every nose has the same soft spot depth.",
            "Circular barbells or retainers for healing — decorative clickers after downsizing.",
            "Do not flip or play with the jewelry during healing — movement delays the fistula.",
        ),
        jewelry_notes="Circular barbell sized for swelling; decorative options after healing.",
        aftercare_summary="Saline soak or mist, no flipping, no nose picking around the ring.",
        related=("nostril", "philtrum", "labret"),
    ),
    PiercingGuide(
        slug_id="eyebrow",
        name="Eyebrow",
        category="facial",
        offered=True,
        offer_note="Yes — surface-adjacent but standard eyebrow piercings are in my regular rotation.",
        healing_time="6–8 weeks initial; 3–4 months fully stable",
        pain_score=5,
        pain_label="Moderate pinch — thin tissue",
        intro=(
            "Eyebrow piercings sit through the supraorbital ridge area — vertical or angled depending on your brow "
            "shape. They migrate if the angle is wrong, so I mark with your natural brow hair growth in mind."
        ),
        quirks=(
            "Glasses and sunglasses rub the entry points — adjust wear during healing.",
            "Migration shows as the jewelry sliding toward the lash line — wrong angle from day one.",
            "One-sided sleeping can push the bar — try back sleeping early on.",
        ),
        tips=(
            "I pierce at an angle that follows your brow ridge — not straight vertical on every face.",
            "Curved barbells fit the anatomy better than straight barbells for most brows.",
            "Keep brow grooming gentle — waxing and threading wait until fully healed.",
        ),
        jewelry_notes="Curved barbell in titanium; shorter bar at downsizing to reduce snag.",
        aftercare_summary="Saline, no makeup on the entries, protect from helmet straps and glasses.",
        related=("anti_eyebrow", "bridge", "labret"),
    ),
    PiercingGuide(
        slug_id="anti_eyebrow",
        name="Anti-Eyebrow",
        category="facial",
        offered=True,
        offer_note="Yes — surface-style placement below the brow; anatomy and aftercare consult required.",
        healing_time="6–12 months — surface-adjacent with migration risk",
        pain_score=7,
        pain_label="Moderate to firm — shallow surface tension",
        intro=(
            "Anti-eyebrow piercings sit on the upper cheek below the brow — a surface aesthetic that looks like a "
            "brow piercing flipped. They are beautiful and unforgiving: angle, jewelry, and aftercare must be perfect."
        ),
        quirks=(
            "High migration and rejection risk compared to standard eyebrow piercings — I set honest expectations.",
            "Microdermals are sometimes a better choice for the same look — we discuss at consult.",
            "Makeup and skincare products migrate into the channel easily.",
        ),
        tips=(
            "I use surface bar or curved barbell techniques depending on your cheek anatomy — one size does not fit all.",
            "If I see thin tissue or high tension, I will recommend a different placement instead.",
            "Sleep on your back; pillow pressure is the main migration driver for anti-eyebrow work.",
            "Come in at the first sign of thinning skin at an entry — early removal beats a scar.",
        ),
        jewelry_notes="Surface bar or high-quality curved barbell — no mystery metal.",
        aftercare_summary="Strict saline, zero pressure, no playing with the bar — monitor for migration monthly.",
        related=("eyebrow", "bridge", "surface"),
    ),
    PiercingGuide(
        slug_id="labret",
        name="Labret",
        category="facial",
        offered=True,
        offer_note="Yes — standard and vertical labret variants on consult.",
        healing_time="2–4 months",
        pain_score=5,
        pain_label="Moderate — lip tissue swells noticeably",
        intro=(
            "Labret piercings sit below the lower lip — versatile for studs, rings, and stacked lip aesthetics. "
            "Swelling is real day one; I use longer posts and schedule downsizing when your lip returns to normal."
        ),
        quirks=(
            "Teeth and gum contact from wrong bar length cause enamel wear — downsizing prevents damage.",
            "Eating spicy or acidic food day one is miserable — plan soft food for 48 hours.",
            "Kissing and oral contact are off limits during early healing — bacteria transfer is real.",
        ),
        tips=(
            "I mark with your lip relaxed and check tooth clearance — your dentist will thank you.",
            "Flat-back disc inside the mouth must sit flush — not tilted into gum tissue.",
            "Rinse with saline after meals; mouthwash with alcohol is too harsh for fresh oral piercings.",
        ),
        jewelry_notes="Long flat-back labret for swell; shorter post at 4–6 week downsizing.",
        aftercare_summary="Saline inside and out, soft food, no oral contact, downsizing appointment required.",
        related=("philtrum", "nostril", "septum"),
    ),
    PiercingGuide(
        slug_id="philtrum",
        name="Medusa (Philtrum)",
        category="facial",
        offered=True,
        offer_note="Yes — centered philtrum piercings are a studio favorite when lip anatomy is suitable.",
        healing_time="2–4 months",
        pain_score=6,
        pain_label="Moderate to sharp — dense lip tissue",
        intro=(
            "Philtrum (Medusa) piercings sit in the center groove above the upper lip — symmetrical, striking, "
            "and sensitive to swelling. I mark from the front and profile so the stud sits truly centered."
        ),
        quirks=(
            "Swelling can make the stud look off-center for a week — that usually resolves before downsizing.",
            "Tooth contact on the inside disc causes gum irritation if the post is wrong length.",
            "Lipstick and lip products must stay away from the entry during healing.",
        ),
        tips=(
            "I check your smile line in the mirror before we pierce — philtrum is unforgiving of crooked marks.",
            "Downsize at 4–6 weeks — philtrum bumps often trace back to jewelry that is too long.",
            "No kissing or sharing drinks during initial heal — oral bacteria slows everything.",
        ),
        jewelry_notes="Flat-back labret with a low-profile gem; fitted for fresh and healed wear.",
        aftercare_summary="Saline rinse after eating, no lip products on the wound, downsizing required.",
        related=("labret", "nostril", "septum"),
    ),
    PiercingGuide(
        slug_id="bridge",
        name="Bridge",
        category="facial",
        offered=True,
        offer_note="Yes — horizontal bridge when brow ridge anatomy supports safe angle.",
        healing_time="8–12 months",
        pain_score=7,
        pain_label="Firm pressure across nasal bridge tissue",
        intro=(
            "Bridge piercings cross the skin between the eyes — bold, photogenic, and sensitive to glasses pressure. "
            "I assess whether your bridge has enough tissue for a stable bar and honest healing odds."
        ),
        quirks=(
            "Glasses sit exactly where bridge bars live — contacts or careful padding during heal.",
            "Migration shows as visible bar shadow under thin skin — anatomy thin? I may advise against it.",
            "Two entry points mean double the aftercare attention.",
        ),
        tips=(
            "I use straight barbells sized for swell — not tight custom lengths on day one.",
            "Keep sunscreen and skincare off the entries; product buildup causes bumps.",
            "If you wear heavy glasses, we talk alternatives before piercing day.",
        ),
        jewelry_notes="Straight barbell; shorter bar after downsizing.",
        aftercare_summary="Saline both sides, no glasses pressure if avoidable, monitor for migration.",
        related=("anti_eyebrow", "eyebrow", "nostril"),
    ),
    PiercingGuide(
        slug_id="navel",
        name="Navel",
        category="body",
        offered=True,
        offer_note="Yes — anatomy must have a defined lip; I decline inverted or flat navels honestly.",
        healing_time="6–12 months",
        pain_score=6,
        pain_label="Moderate — pinch at the lip, brief",
        intro=(
            "Navel piercings need a visible shelf of tissue — not every belly button can support one safely. "
            "I check your anatomy standing and sitting before we book; an honest no saves you a scar."
        ),
        quirks=(
            "Waistbands, high-waisted pants, and workout leggings rub navels constantly in Vegas gym culture.",
            "Inverted navels often reject — I will suggest alternatives instead of a doomed piercing.",
            "Summer pool season and fresh navel piercings do not mix — plan timing before vacation.",
        ),
        tips=(
            "I pierce from the bottom lip up for a cleaner angle on most anatomies.",
            "Wear low-rise or loose waistbands during healing — friction is the navel's enemy.",
            "No submerging in pools or hot tubs until fully healed — bacteria loves warm water.",
        ),
        jewelry_notes="Curved barbell with room for swell; decorative ends after heal.",
        aftercare_summary="Saline, loose clothing, no tanning beds on fresh navel work.",
        related=("surface", "labret"),
    ),
    PiercingGuide(
        slug_id="tongue",
        name="Tongue (Center)",
        category="body",
        offered=True,
        offer_note="Yes — standard center tongue piercings only; we do not offer frog eyes / venom bites.",
        healing_time="4–6 weeks initial; 2–3 months for full stability",
        pain_score=6,
        pain_label="Sharp then throbbing — swelling peaks day 2–3",
        intro=(
            "Center tongue piercings heal faster than cartilage but swell dramatically the first few days. "
            "I use long barbells for swell and downsize when you can speak normally again — usually 2–3 weeks."
        ),
        quirks=(
            "Day-two swelling is normal — ice chips and cold water help; panic is unnecessary if breathing is fine.",
            "Speech and eating are awkward for a week — plan work calls accordingly.",
            "We do not perform frog eyes (paired venom / surface tongue piercings) — see that guide for why.",
        ),
        tips=(
            "I mark the center line with you sticking your tongue out relaxed — not strained.",
            "Long barbell mandatory for swell — never start with a short bar on tongue work.",
            "Rinse with saline after every meal; smoking and alcohol slow heal significantly.",
            "Come in for downsizing on schedule — a long bar is a tooth chip risk once swelling drops.",
        ),
        jewelry_notes="Barbell long enough for healing; shorter bar at downsizing.",
        aftercare_summary="Cold fluids, saline rinses, soft food, no oral contact, mandatory downsizing visit.",
        related=("labret", "frog_eyes_tongue"),
    ),
    PiercingGuide(
        slug_id="surface",
        name="Surface",
        category="body",
        offered=True,
        offer_note="Yes — consult-only; not all surface placements are suitable for every body.",
        healing_time="6–12 months with elevated rejection risk",
        pain_score=7,
        pain_label="Moderate to firm — tissue pinching",
        intro=(
            "Surface piercings travel under a flat plane of skin — collarbone, nape, hip, and similar. "
            "They are consult-first because rejection is common industry-wide; I only pierce when tissue depth "
            "and lifestyle support a fair chance of success."
        ),
        quirks=(
            "Surface bars behave differently from standard piercings — migration often shows as thinning skin first.",
            "Bags, seatbelts, and bra straps destroy surface piercings — lifestyle must match placement.",
            "Sometimes a microdermal is the better tool for the same aesthetic — we decide at consult.",
        ),
        tips=(
            "I will say no if your tissue is too shallow — that is professionalism, not disappointment.",
            "Surface work requires check-ins at 4 and 8 weeks — do not ghost your piercer on these.",
            "If an entry looks angry, come in early — removal beats a split scar.",
        ),
        jewelry_notes="Surface bar with custom length per anatomy.",
        aftercare_summary="Saline, zero pressure on the bar, strict monitoring for rejection signs.",
        related=("anti_eyebrow", "navel"),
    ),
    PiercingGuide(
        slug_id="genital",
        name="Genital",
        category="not_offered",
        offered=False,
        offer_note="No — Work of Art does not perform genital piercings in-studio.",
        healing_time="N/A — service not offered",
        pain_score=0,
        pain_label="N/A",
        intro=(
            "Clients ask, so I answer clearly: we do not offer genital piercings at Work of Art. "
            "That is a scope choice for our studio — not a judgment on your body or preferences."
        ),
        quirks=(
            "Genital work requires specialized training, room setup, and aftercare protocols we do not provide.",
            "If you need a referral, search for an APP member piercer who lists genital work explicitly.",
            "We focus on ear curation, facial, and select body piercings where our training and setup excel.",
        ),
        tips=(
            "I would rather be honest here than take a piercing outside our competency — your safety comes first.",
            "For every other placement on this guide that we offer, book a consult and I will walk you through heal.",
            "Our jewelry standards page explains what we do perform and how we sterilize for those services.",
        ),
        jewelry_notes="N/A — not performed at Work of Art.",
        aftercare_summary="N/A — see APP resources for piercers who specialize in genital placements.",
        faqs=(
            (
                "Why does Work of Art not offer genital piercings?",
                "Scope and specialization — we focus on ear curation, facial, and select body piercings "
                "where our training, room setup, and aftercare protocols are built to excel.",
            ),
        ),
        related=("ear_lobe", "ear_curation"),
    ),
    PiercingGuide(
        slug_id="frog_eyes_tongue",
        name="Frog Eyes (Venom / Surface Tongue)",
        category="not_offered",
        offered=False,
        offer_note="No — we do not perform frog eyes, venom bites, or paired surface tongue piercings.",
        healing_time="N/A — service not offered",
        pain_score=0,
        pain_label="N/A",
        intro=(
            "Frog eyes — the paired piercings on the top surface of the tongue — are not something I perform. "
            "We do standard center tongue piercings; this specific placement stays off our menu for safety reasons."
        ),
        quirks=(
            "Surface tongue piercings have high complication rates — nerve, tooth, and speech risks rise sharply.",
            "Many studios that offered frog eyes have stopped — industry trend reflects heal data, not hype.",
            "Center tongue and standard oral piercings follow different anatomy rules than surface tongue work.",
        ),
        tips=(
            "If you wanted frog eyes for aesthetics, ask me about center tongue or other oral options we do offer.",
            "Never go to a piercer who minimizes tongue surface risks — your teeth and nerves are not negotiable.",
            "Read our center tongue guide for what we do perform and how we downsize safely.",
        ),
        jewelry_notes="N/A — not performed at Work of Art.",
        aftercare_summary="N/A — we offer center tongue piercing with structured downsizing instead.",
        faqs=(
            (
                "Do you do venom or frog eye tongue piercings?",
                "No. Work of Art does not perform frog eyes, venom bites, or paired surface tongue piercings. "
                "We do offer standard center tongue piercings with properly fitted jewelry and scheduled downsizing.",
            ),
        ),
        related=("tongue", "labret"),
    ),
)


def guide_by_id(slug_id: str) -> PiercingGuide | None:
    for g in PIERCING_CATALOG:
        if g.slug_id == slug_id:
            return g
    return None


def guides_for(category: CategoryId) -> list[PiercingGuide]:
    return [g for g in PIERCING_CATALOG if g.category == category]


def offered_guides() -> list[PiercingGuide]:
    return [g for g in PIERCING_CATALOG if g.offered]


CATEGORY_LABELS: dict[CategoryId, str] = {
    "ear": "Ear piercings",
    "facial": "Facial piercings",
    "body": "Body piercings",
    "not_offered": "Not offered at Work of Art",
}
