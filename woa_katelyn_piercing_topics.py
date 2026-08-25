#!/usr/bin/env python3
"""Katelyn Cole piercing authority topic catalog."""

from __future__ import annotations

from dataclasses import dataclass

HUB_SLUG = "katelyn_cole_piercing_authority_hub_las_vegas"
HUB_TITLE = "Katelyn Cole — Piercing Topics"
HUB_INTRO = (
    "Professional piercer Katelyn Cole on jewelry fit, ear curation, anatomy, and aftercare — "
    "the topics clients search before they sit in my chair."
)

BOOK = "/appointments/"
ENCYCLOPEDIA = "/piercing_types_las_vegas_authority_hub/"
DESERT = "/piercing_aftercare_desert_climate_las_vegas_expert_guide/"
KATELYN_PAGE = "/artists/katelyn-cole/"


@dataclass(frozen=True)
class KatelynTopic:
    slug_id: str
    title: str
    intro: str
    sections: tuple[tuple[str, tuple[str, ...]], ...]
    faqs: tuple[tuple[str, str], ...] = ()
    related: tuple[str, ...] = ()


def slug_for(topic: KatelynTopic) -> str:
    return f"{topic.slug_id}_las_vegas_authority_guide"


KATELYN_TOPICS: tuple[KatelynTopic, ...] = (
    KatelynTopic(
        slug_id="katelyn_implant_grade_titanium",
        title="How I Choose Starter Jewelry",
        intro=(
            "Fresh piercings deserve jewelry selected for anatomy, swelling, and sensitivity. "
            "This page keeps material claims general until the studio owner verifies current jewelry documentation."
        ),
        sections=(
            ("What I check before choosing jewelry", (
                "Post length needs room for expected swelling without leaving enough leverage to snag constantly.",
                "Ends should sit comfortably against the anatomy and stay practical during cleaning.",
                "Metal sensitivity history matters, so tell me about reactions before we choose a starter piece.",
            )),
            ("What I will not use on day one", (
                "Mystery jewelry from online retailers with no reliable documentation.",
                "Gold-plated fashion studs — plating is not a good plan for fresh work.",
                "Butterfly backs on fresh cartilage — see my butterfly back guide.",
            )),
            ("Katelyn's recommendation", (
                "Start with properly fitted starter jewelry and save decorative upgrades for a stable piercing.",
                "Keep every starter piece on file at the studio so downsizing is a swap, not a guess.",
            )),
        ),
        faqs=(("Can I bring my own jewelry for a fresh piercing?", "Usually no. Bring photos or packaging and I can review it, but fresh jewelry needs to fit the anatomy, swelling, and safety requirements for that placement."),),
        related=("katelyn_implant_grade_titanium", "katelyn_threadless_jewelry"),
    ),
    KatelynTopic(
        slug_id="katelyn_butterfly_backs_truth",
        title="The Truth About Butterfly Backs",
        intro=(
            "Butterfly backs are everywhere at the mall — and they cause more bumps in my chair than almost any other jewelry choice."
        ),
        sections=(
            ("Why I avoid them on fresh work", (
                "They trap hair, dead skin, and bacteria against the entry.",
                "They are hard to clean — you cannot see the post threading inside.",
                "Tightening them embeds the back into swelling — a common emergency visit.",
            )),
            ("What I use instead", (
                "Flat-back labret posts — clean profile, easy saline access, secure threadless or internal thread.",
                "Long enough for swell, then downsized on schedule.",
            )),
            ("When butterfly backs appear", (
                "Healed lobe piercings with occasional short-term wear — still not my favorite.",
                "Never on fresh cartilage, nostril, or conch work in my studio.",
            )),
        ),
        related=("katelyn_implant_grade_titanium", "katelyn_downsizing_jewelry"),
    ),
    KatelynTopic(
        slug_id="katelyn_anatomy_matters",
        title="Why Anatomy Matters",
        intro=(
            "A piercing photo on Instagram is not your ear. I mark every piercing for your tissue — angle, depth, and jewelry length."
        ),
        sections=(
            ("What I assess before we pierce", (
                "Tissue thickness and blood supply — shallow anti-tragus or snug anatomy gets a honest no.",
                "Sleeping habits — side sleepers need different planning for industrial and rook.",
                "Existing piercings and scarring — we map around old holes, not through them blindly.",
            )),
            ("Angles are not cosmetic", (
                "A nostril pierced parallel to the face migrates — I pierce perpendicular to tissue.",
                "Industrial bars need custom length and angle or both holes reject together.",
            )),
            ("Katelyn's recommendation", (
                "Bring reference photos, but trust the mark I show you in the mirror — you wear it for years.",
            )),
        ),
        related=("katelyn_ear_curation", "katelyn_why_piercings_reject"),
    ),
    KatelynTopic(
        slug_id="katelyn_ear_curation",
        title="How I Curate Ears",
        intro=(
            "Ear curation is a plan — not a spontaneous stack of holes. I map jewelry scale, metal, order of work, and downsizing timelines."
        ),
        sections=(
            ("The consult map", (
                "We pick a hero piercing first — often conch or helix — then build around it after downsizing.",
                "Gem size and metal match across the ear so it reads as one composition.",
                "We stage work over months — piercing everything at once slows every heal.",
            )),
            ("What clients get wrong", (
                "Copying a Pinterest ear on incompatible anatomy.",
                "Mixing cheap healed jewelry with fresh work — irritation can ripple across the ear.",
                "Skipping downsizing because the long post 'does not hurt.'",
            )),
            ("Book an ear curation consult", (
                "Walk-ins can do single piercings; full curation starts with a planning appointment.",
            )),
        ),
        related=("katelyn_anatomy_matters", "katelyn_downsizing_jewelry"),
    ),
    KatelynTopic(
        slug_id="katelyn_why_piercings_reject",
        title="Why Some Piercings Reject",
        intro=(
            "Rejection is not bad luck — it is physics. Surface area, tension, pressure, and wrong anatomy predict outcomes before we pierce."
        ),
        sections=(
            ("Migration vs rejection", (
                "Migration: jewelry shifts angle over weeks — often sleeping or wrong length.",
                "Rejection: body pushes jewelry out — common on surface, navel, and anti-eyebrow when anatomy is wrong.",
            )),
            ("What I do about it", (
                "I say no when tissue is too shallow — a scar beats a year of fighting a doomed piercing.",
                "Early removal preserves better skin for a future attempt or different placement.",
            )),
            ("Warning signs", (
                "Thinning skin at an entry, increasing redness only on one side of the bar, jewelry sitting closer to the surface.",
            )),
        ),
        related=("katelyn_anatomy_matters", "katelyn_sleeping_on_helix"),
    ),
    KatelynTopic(
        slug_id="katelyn_gold_vs_titanium",
        title="Gold vs Titanium",
        intro=(
            "Both can be excellent — timing matters. Titanium for fresh work and titanium-based upgrades when you want a decorative healed look."
        ),
        sections=(
            ("Fresh piercings", ("Starter jewelry needs proper length, polish, and fit for swelling; material specifics should be verified at the consult.",)),
            ("Healed upgrades", (
                "Reputable piercing jewelry makers — not plated fashion jewelry.",
                "Gold is heavier — I check cartilage healed enough to support decorative ends.",
            )),
            ("Allergies", (
                "Nickel sensitivity clients stay on titanium longer; gold alloys still contain trace metals — disclose allergies at consult.",
            )),
        ),
        related=("katelyn_implant_grade_titanium", "katelyn_threadless_jewelry"),
    ),
    KatelynTopic(
        slug_id="katelyn_threadless_jewelry",
        title="Threadless Jewelry Explained",
        intro=(
            "Threadless ends pin into a post with tension — no screwing through a fresh fistula during downsizing."
        ),
        sections=(
            ("Why I love threadless for downsizing", (
                "Swap decorative ends without twisting the post inside the channel.",
                "Fewer threads means fewer bacteria traps on labret and cartilage posts.",
            )),
            ("How it works", (
                "Post has a slight bend; end pins in with hand pressure — I adjust tension in-studio.",
                "Comes from reputable piercing jewelry makers and is fitted in-studio.",
            )),
        ),
        related=("katelyn_downsizing_jewelry", "katelyn_implant_grade_titanium"),
    ),
    KatelynTopic(
        slug_id="katelyn_downsizing_jewelry",
        title="Downsizing Jewelry",
        intro=(
            "Long starter posts are intentional — short jewelry on day one causes embedding, bumps, and angle irritation."
        ),
        sections=(
            ("Typical timeline", (
                "Cartilage and nostril: 6–8 weeks for first downsize if swelling is gone.",
                "Tongue: 2–3 weeks — mandatory, not optional.",
                "Labret and philtrum: 4–6 weeks to protect teeth and gums.",
            )),
            ("What happens if you skip it", (
                "Helix bumps from posts that stick out and get slept on.",
                "Tooth chips from tongue bars still at swell length after week 3.",
            )),
            ("Book the downsize", (
                "Downsizing is a quick appointment — often walk-in when you are an existing client.",
            )),
        ),
        related=("katelyn_butterfly_backs_truth", "katelyn_sleeping_on_helix"),
    ),
    KatelynTopic(
        slug_id="katelyn_sleeping_on_helix",
        title="Sleeping on a Helix",
        intro=(
            "The helix bump epidemic is mostly a pillow problem — not an infection problem."
        ),
        sections=(
            ("What pressure does", (
                "Forces the post to angle into the rim — irritation bump forms within days.",
                "Repeats every night until you change sleep position or use a donut pillow.",
            )),
            ("My client protocol", (
                "Back sleep or opposite side for minimum 8 weeks on helix, flat, and conch.",
                "Clean pillowcase — bacteria from hair products transfers to fresh entries.",
            )),
            ("If a bump appears", (
                "Come in before you buy random online 'bump solutions' — usually pressure or length, not infection.",
            )),
        ),
        related=("katelyn_why_piercings_reject", "katelyn_downsizing_jewelry"),
    ),
    KatelynTopic(
        slug_id="katelyn_piercing_minors",
        title="How I Pierce Minors",
        intro=(
            "Ear piercing for minors 14+ with a parent or guardian present — ID required. Facial and body piercings are adults only in my chair."
        ),
        sections=(
            ("What we require", (
                "Guardian present for the full appointment — not just drop-off.",
                "Valid ID for minor and guardian; ear work only.",
                "Aftercare taught to both minor and guardian — healing is a team effort.",
            )),
            ("What we use", (
                "Sterile needle technique — never a piercing gun.",
                "Properly fitted starter studs with flat backs.",
            )),
            ("Why standards matter", (
                "Mall guns cannot be sterilized between clients the way our setup is.",
                "I would rather turn away a rushed guardian than pierce without consent and aftercare understanding.",
            )),
        ),
        faqs=(("What age do you start?", "Ear piercings for minors 14+ with guardian present at Work of Art Las Vegas."),),
        related=("katelyn_implant_grade_titanium", "katelyn_ear_curation"),
    ),
)


def topic_by_id(slug_id: str) -> KatelynTopic | None:
    for t in KATELYN_TOPICS:
        if t.slug_id == slug_id:
            return t
    return None
