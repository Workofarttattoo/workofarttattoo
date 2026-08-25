#!/usr/bin/env python3
"""Heal-profile templates for piercing encyclopedia sections (Katelyn Cole voice)."""

from __future__ import annotations

from dataclasses import dataclass

HealProfile = str  # lobe | cartilage | nasal | oral | facial | body | surface | overview | not_offered

DESERT_BASE = (
    "Vegas air is dry — crusties tighten faster than at the coast. Saline mist, not picking.",
    "Skip hotel pools, day-club hot tubs, and dusty outdoor festivals until your piercer clears you.",
    "SPF on healed piercings only; never on fresh work. Sweat from summer gym sessions — rinse with saline after.",
)


@dataclass(frozen=True)
class EncyclopediaSections:
    who_its_good_for: tuple[str, ...]
    downsizing: tuple[str, ...]
    swimming: tuple[str, ...]
    exercise: tuple[str, ...]
    sleeping: tuple[str, ...]
    cleaning: tuple[str, ...]
    changing_jewelry: tuple[str, ...]
    swelling: tuple[str, ...]
    migration: tuple[str, ...]
    rejection: tuple[str, ...]
    common_mistakes: tuple[str, ...]
    desert_healing: tuple[str, ...]
    when_to_call: tuple[str, ...]
    who_should_avoid: tuple[str, ...]
    katelyn_recommendations: tuple[str, ...]
    video_links: tuple[tuple[str, str], ...] = ()
    photo_links: tuple[tuple[str, str], ...] = ()
    anatomy_requirements: tuple[str, ...] = ()
    jewelry_sizing: tuple[str, ...] = ()
    swelling_expectations: tuple[str, ...] = ()
    headphones: tuple[str, ...] = ()
    helmets: tuple[str, ...] = ()
    keloids_vs_bumps: tuple[str, ...] = ()


def _extras(profile: HealProfile) -> dict[str, tuple[str, ...]]:
    """Profile-level sections for the 16-part template."""
    shared_swim = (
        "No pools, hot tubs, or open water until your piercer clears you — chlorine and bacteria both set you back.",
        "Lake Mead and hotel pools are everywhere in Vegas; plan heal before pool season.",
    )
    shared_gym = (
        "Light gym is usually fine after the first few days if you rinse with saline after sweat.",
        "Avoid contact sports, grappling, and anything that snags fresh jewelry.",
    )
    by_profile: dict[str, dict[str, tuple[str, ...]]] = {
        "lobe": {
            "who_its_good_for": (
                "First-time piercees wanting low pain and predictable heal.",
                "Clients planning stacked lobes or a curated ear who can attend a downsizing check.",
            ),
            "downsizing": (
                "Downsize post length at 8–10 weeks if swelling is gone — shorter jewelry prevents angle irritation.",
                "Stacked lobes need spacing planned before shortening ends.",
            ),
            "swimming": shared_swim + ("Lobes: usually 8+ weeks before swimming in Vegas pools.",),
            "exercise": shared_gym,
        },
        "cartilage": {
            "who_its_good_for": (
                "Clients who can sleep on their back or use a donut pillow for months.",
                "Anyone willing to wait 6–12 months before hoops and decorative ends.",
            ),
            "downsizing": (
                "Mandatory downsizing at 6–8 weeks — long posts are the number-one cause of helix and conch bumps.",
                "Industrial and orbital bars get checked as a unit; do not skip the appointment.",
            ),
            "swimming": shared_swim + ("Cartilage: plan on 6+ months before submerging the ear.",),
            "exercise": shared_gym + ("Headphones and hat brims add friction — plan around them.",),
        },
        "nasal": {
            "who_its_good_for": (
                "Clients with stable sinuses and realistic heal timelines for studs before hoops.",
                "Bridge candidates who can reduce glasses pressure during heal.",
            ),
            "downsizing": (
                "Nostril: shorter post at 6–8 weeks once tip swelling drops.",
                "Septum: smaller ring diameter at 6–8 weeks after sweet-spot swelling resolves.",
            ),
            "swimming": shared_swim + ("Facial entries and pool chemicals do not mix — nostril work needs extra caution.",),
            "exercise": shared_gym,
        },
        "oral": {
            "who_its_good_for": (
                "Clients who can commit to downsizing appointments and no oral contact during heal.",
                "Anyone willing to pause smoking for the heal window.",
            ),
            "downsizing": (
                "Tongue: mandatory downsizing at 2–3 weeks — non-negotiable for tooth safety.",
                "Labret and philtrum: shorter post at 4–6 weeks to protect gums and teeth.",
            ),
            "swimming": shared_swim,
            "exercise": shared_gym + ("Rinse with saline after meals and workouts.",),
        },
        "body": {
            "who_its_good_for": (
                "Clients with anatomy that supports a fair heal — consult first for navel lip and nipple depth.",
                "Anyone who can avoid waistband compression and pool season until cleared.",
            ),
            "downsizing": (
                "Navel and nipple: shorter bar once swelling resolves — usually 6–8 weeks.",
                "Decorative dangling navel jewelry waits until 6–12 months.",
            ),
            "swimming": shared_swim + ("Body piercings and Vegas pool season are a bad combination — wait for full clear.",),
            "exercise": shared_gym + ("Loose clothing; no compression on fresh navel or nipple work.",),
        },
        "surface": {
            "who_its_good_for": (
                "Clients who accept higher migration risk and zero pressure on the bar during heal.",
            ),
            "downsizing": ("Surface bars stay until fully stable — 9–12 months minimum.",),
            "swimming": shared_swim,
            "exercise": shared_gym,
        },
        "overview": {
            "who_its_good_for": ("Use the pillar page for your area, then open the specific placement guide.",),
            "downsizing": ("Downsizing schedules vary — see your placement guide.",),
            "swimming": shared_swim,
            "exercise": shared_gym,
        },
        "not_offered": {
            "who_its_good_for": ("N/A — not performed at Work of Art.",),
            "downsizing": ("N/A",),
            "swimming": ("N/A",),
            "exercise": ("N/A",),
        },
    }
    return by_profile.get(profile, by_profile["cartilage"])


PROFILE_MAP: dict[str, HealProfile] = {
    "ear": "overview",
    "ear_lobe": "lobe",
    "upper_lobe": "lobe",
    "cartilage": "overview",
    "helix": "cartilage",
    "forward_helix": "cartilage",
    "flat": "cartilage",
    "conch": "cartilage",
    "tragus": "cartilage",
    "anti_tragus": "cartilage",
    "daith": "cartilage",
    "rook": "cartilage",
    "snug": "cartilage",
    "industrial": "cartilage",
    "orbital": "cartilage",
    "ear_curation": "overview",
    "nose": "overview",
    "nostril": "nasal",
    "high_nostril": "nasal",
    "septum": "nasal",
    "bridge": "nasal",
    "eyebrow": "facial",
    "anti_eyebrow": "surface",
    "lip": "overview",
    "labret": "oral",
    "vertical_labret": "oral",
    "philtrum": "oral",
    "monroe": "oral",
    "snake_bites": "oral",
    "tongue": "oral",
    "navel": "body",
    "nipple": "body",
    "surface": "surface",
    "genital": "not_offered",
    "frog_eyes_tongue": "not_offered",
}


def _lobe(name: str) -> EncyclopediaSections:
    ex = _extras("lobe")
    return EncyclopediaSections(
        who_its_good_for=ex["who_its_good_for"],
        downsizing=ex["downsizing"],
        swimming=ex["swimming"],
        exercise=ex["exercise"],
        sleeping=(
            f"Sleep on the opposite side for the first two weeks — pillow pressure on a fresh {name.lower()} is the fastest route to a bump.",
            "A travel pillow with a ear hole helps if you are a side sleeper.",
        ),
        cleaning=(
            "Sterile saline mist 1–2 times daily — spray, let it sit 30 seconds, pat dry with clean paper towel.",
            "No alcohol, peroxide, or tea tree oil unless I tell you otherwise in a check-in.",
            "Wash hands before touching anywhere near the piercing.",
        ),
        changing_jewelry=(
            "Wait until the fistula feels stable — usually 6–8 weeks for lobes, longer if you stretch or stack holes.",
            "Come in for a jewelry change so I can confirm you are ready — DIY swaps with blunt posts cause tears.",
        ),
        swelling=(
            "Mild swelling day 1–3 is normal; a long flat-back post accounts for it.",
            "If the post embeds or skin swells over the backing, come in — do not wait.",
        ),
        migration=(
            "True migration is rare on lobes with correct angle — crooked gun piercings are the usual cause.",
            "If the hole looks oval instead of round, book a consult before it worsens.",
        ),
        rejection=(
            "Lobe rejection is uncommon with needle technique and properly fitted jewelry.",
            "Red flags: thinning skin at the exit, jewelry hanging lower over weeks.",
        ),
        common_mistakes=(
            "Twisting the stud — that micro-tears the fistula every time.",
            "Butterfly backs that trap hair, sweat, and bacteria.",
            "Swimming in Vegas pools before the fistula closes.",
        ),
        desert_healing=DESERT_BASE,
        when_to_call=(
            "Spreading redness, pus, red streaks, fever, or pain that worsens after day 3.",
            "Jewelry embedding, sudden asymmetry, or a bump that grows for two weeks straight.",
        ),
        who_should_avoid=(
            "Active outer-ear infection — see a clinician first, pierce after it clears.",
            "Unrealistic timeline for multiple cartilage piercings on the same ear in one trip.",
        ),
        katelyn_recommendations=(
            f"I mark {name.lower()} piercings standing and sitting — your anatomy shifts.",
            "Plan spacing now if you want a curated ear later.",
            "Fresh jewelry must be fitted and documented in-studio.",
        ),
        video_links=(
            ("Katelyn piercing in the studio", "/studio_videos/#katelyn-piercing"),
            ("Minor ear piercing — how we do it", "/artists/katelyn-cole/#minors"),
        ),
        photo_links=(
            ("Ear piercing portfolio", "/studio_gallery/#katelyn-piercing"),
            ("Katelyn Cole — artist page", "/artists/katelyn-cole/"),
        ),
    )


def _cartilage(name: str) -> EncyclopediaSections:
    ex = _extras("cartilage")
    return EncyclopediaSections(
        who_its_good_for=ex["who_its_good_for"],
        downsizing=ex["downsizing"],
        swimming=ex["swimming"],
        exercise=ex["exercise"],
        sleeping=(
            f"A fresh {name.lower()} and your pillow are enemies — back sleeping or a donut pillow for 8+ weeks.",
            "Headphones, glasses arms, and mask loops all add pressure — plan around them.",
        ),
        cleaning=(
            "Saline mist twice daily; no rotating the jewelry.",
            "Rinse after gym sweat — salt and friction irritate cartilage fast in desert heat.",
            "Keep hair tied back so it does not wrap around the post.",
        ),
        changing_jewelry=(
            "Cartilage: 6–12 months before a casual jewelry swap — I will tell you at downsizing if you are on track.",
            "Hoops too early are the number-one cause of bumps on conch and helix work.",
        ),
        swelling=(
            "Cartilage swells less than lobes but lasts longer — expect a tender bump around the post for 1–2 weeks.",
            "Downsize at 6–8 weeks when swelling drops — long posts cause angle irritation.",
        ),
        migration=(
            "Wrong angle or sleeping pressure makes cartilage migrate — the post tilts toward the rim over weeks.",
            "Industrial and orbital piercings migrate as a unit if bar tension is wrong.",
        ),
        rejection=(
            "Cartilage does not reject like surface work, but bumps and delayed healing mimic it.",
            "If the entry looks shallow or skin thins, come in — early removal beats a scar.",
        ),
        common_mistakes=(
            "Piercing guns on cartilage — never in my studio.",
            "Changing to a hoop because it 'looks healed' at week 4.",
            "Ignoring downsizing appointments.",
        ),
        desert_healing=DESERT_BASE + (
            "Dry crusties — do not pick; saline softens them.",
            "Helix piercings under baseball caps in summer — add friction you do not need.",
        ),
        when_to_call=(
            "Bump growing 2+ weeks, jewelry embedding, hot swelling after week 1, or fluid that smells.",
            "Industrial: if one hole heals and the other stays angry — both need attention.",
        ),
        who_should_avoid=(
            "Anatomy too shallow for safe angle — I will say no rather than force a trendy placement.",
            "Cannot commit to side-sleeping changes for rook, daith, or industrial heal.",
        ),
        katelyn_recommendations=(
            f"I pierce {name.lower()} with clean technique and flat-back posts sized for your swelling.",
            "One cartilage project at a time unless we map a staged curation plan.",
            "Threadless titanium lets us downsize ends without twisting the fistula.",
        ),
        video_links=(("Piercing in the studio — Katelyn Cole", "/studio_videos/#katelyn-piercing"),),
        photo_links=(("Curated ear portfolio", "/studio_gallery/#katelyn-piercing"),),
    )


def _nasal(name: str) -> EncyclopediaSections:
    ex = _extras("nasal")
    return EncyclopediaSections(
        who_its_good_for=ex["who_its_good_for"],
        downsizing=ex["downsizing"],
        swimming=ex["swimming"],
        exercise=ex["exercise"],
        sleeping=(
            "Sleep on your back when possible — side pressure shifts nostril and septum jewelry.",
            "Fresh septum: avoid flipping the ring up before heal — it irritates the sweet spot.",
        ),
        cleaning=(
            "Saline mist on entries; for septum, a quick saline rinse in the shower helps.",
            "Keep makeup, sunscreen, and foundation off nostril entries until healed.",
        ),
        changing_jewelry=(
            "Nostril: 4–6 months before a hoop — studs heal more predictably.",
            "Septum: downsizing ring diameter at 6–8 weeks once swelling is gone.",
        ),
        swelling=(
            "Eyes water during the piercing — normal. Nostril tip may swell slightly for days.",
            "Septum swelling can make the ring feel tight — we size for it.",
        ),
        migration=(
            "Nostril migration shows as the stud sitting at a visible angle — usually wrong angle from day one.",
            "Bridge work migrates if glasses pressure is constant during heal.",
        ),
        rejection=(
            "Bridge and high nostril have higher migration risk than standard nostril.",
            "Thinning skin at an entry means come in immediately.",
        ),
        common_mistakes=(
            "Rotating nostril studs with dirty fingers.",
            "Switching to a hoop for 'aesthetic' at week 2.",
            "Blowing nose aggressively during a cold on fresh septum work.",
        ),
        desert_healing=DESERT_BASE + (
            "Dry nose from AC and desert air — saline helps, do not over-moisturize entries.",
        ),
        when_to_call=(
            "Nostril ring of redness expanding past the piercing, yellow discharge, or jewelry sinking in.",
            "Septum: hard cartilage crunch pain after week 1 — may have been pierced too high.",
        ),
        who_should_avoid=(
            "Active sinus infection or severe allergies you cannot control during heal.",
            "Bridge: cannot avoid glasses contact on the bar.",
        ),
        katelyn_recommendations=(
            f"I mark {name.lower()} at 90 degrees to tissue — not parallel to the face.",
            "Starter jewelry sized for swelling; decorative options after the fistula stabilizes.",
        ),
        video_links=(("Studio piercing reels", "/studio_videos/"),),
        photo_links=(("Facial piercing portfolio", "/studio_gallery/#katelyn-piercing"),),
    )


def _oral(name: str) -> EncyclopediaSections:
    ex = _extras("oral")
    return EncyclopediaSections(
        who_its_good_for=ex["who_its_good_for"],
        downsizing=ex["downsizing"],
        swimming=ex["swimming"],
        exercise=ex["exercise"],
        sleeping=(
            "Elevate your head slightly the first few nights — oral piercings swell with gravity.",
            "Tongue: expect day-2 swelling peak; keep breathing unobstructed.",
        ),
        cleaning=(
            "Saline rinse after meals and before bed — no alcohol mouthwash on fresh oral work.",
            "Labret and philtrum: saline on outside entries; avoid spicy food 48 hours.",
        ),
        changing_jewelry=(
            "Tongue: mandatory downsizing at 2–3 weeks — long bars chip teeth once swelling drops.",
            "Labret: shorter post at 4–6 weeks to protect gums and teeth.",
        ),
        swelling=(
            "Oral piercings swell predictably — tongue day 2–3, lip piercings day 1–4.",
            "Ice chips and cold water help; panic is unnecessary if you can breathe and swallow.",
        ),
        migration=(
            "Vertical labret and philtrum migrate if angle fights lip movement — rare with correct mark.",
            "Snake bites need symmetrical spacing or one side heals angry.",
        ),
        rejection=(
            "Surface oral work (frog eyes) is not offered here — high rejection and tooth damage risk.",
            "Gum recession from wrong labret length looks like rejection — fix jewelry, not placement.",
        ),
        common_mistakes=(
            "Kissing and oral contact during heal — bacteria transfer is real.",
            "Playing with tongue barbells.",
            "Smoking slows every oral heal in Vegas dry air.",
        ),
        desert_healing=DESERT_BASE + (
            "Dehydration from heat makes oral crusties worse — drink water, rinse with saline.",
        ),
        when_to_call=(
            "Teeth chips from tongue bar, gum pain from labret disc, white patches that spread, or fever.",
        ),
        who_should_avoid=(
            "Active cold sores or oral infection — heal first, pierce second.",
            "Cannot commit to downsizing appointment for tongue work.",
        ),
        katelyn_recommendations=(
            f"I check tooth clearance and gum line before every {name.lower()} piercing.",
            "Long starter jewelry on purpose — short jewelry on day one damages teeth.",
        ),
        video_links=(("Katelyn Cole — piercing portfolio", "/artists/katelyn-cole/"),),
        photo_links=(("Labret and facial work", "/studio_gallery/#katelyn-piercing"),),
    )


def _body(name: str) -> EncyclopediaSections:
    ex = _extras("body")
    return EncyclopediaSections(
        who_its_good_for=ex["who_its_good_for"],
        downsizing=ex["downsizing"],
        swimming=ex["swimming"],
        exercise=ex["exercise"],
        sleeping=(
            "Loose waistbands for navel — tight leggings and fresh navel piercings do not mix.",
            "Nipple: loose shirts, no compression sports bras on fresh work until I clear you.",
        ),
        cleaning=(
            "Saline mist on entries; pat dry — no heavy ointment layers that trap sweat.",
            "Navel: rinse after sweat; keep lint out of the wound.",
        ),
        changing_jewelry=(
            "Navel: 6–12 months before decorative dangling jewelry.",
            "Nipple: downsizing bar length once swelling resolves — usually 6–8 weeks.",
        ),
        swelling=(
            "Navel and nipple swell moderately day 1–5 — starter bars are long for a reason.",
        ),
        migration=(
            "Navel migration happens when anatomy lacks a lip — I assess before we pierce.",
            "Shallow nipple anatomy may not support safe piercing — consult required.",
        ),
        rejection=(
            "Navel rejection is common industry-wide on inverted navels — I decline when anatomy is wrong.",
            "Watch for thinning skin at top or bottom entry.",
        ),
        common_mistakes=(
            "Swimming in Vegas pools before heal completes.",
            "Waistband friction on navel; backpack straps on nipple work.",
            "Changing jewelry because it 'looks fine' at 6 weeks.",
        ),
        desert_healing=DESERT_BASE + (
            "Sweat under bandages or tight clothes — change to dry fabric after gym.",
        ),
        when_to_call=(
            "Bar half out, green discharge, spreading redness, or jewelry embedding.",
        ),
        who_should_avoid=(
            "Inverted or flat navel with no pierceable lip.",
            "Pregnancy planning within heal window for nipple work — book a consult.",
        ),
        katelyn_recommendations=(
            f"I only pierce {name.lower()} when anatomy and lifestyle support a fair heal.",
            "Private consult room available — body piercings are appointment-first.",
        ),
        video_links=(("Book a consult", "/appointments/"),),
        photo_links=(("Piercing standards", "/best_piercing_shop_las_vegas_updated_jewelry_standards/"),),
    )


def _surface(name: str) -> EncyclopediaSections:
    ex = _extras("surface")
    sec = _cartilage(name)
    return EncyclopediaSections(
        who_its_good_for=ex["who_its_good_for"],
        downsizing=ex["downsizing"],
        swimming=ex["swimming"],
        exercise=ex["exercise"],
        sleeping=sec.sleeping + ("Zero pressure on the bar — ever, during heal.",),
        cleaning=sec.cleaning,
        changing_jewelry=("Surface bars stay until fully stable — 9–12 months minimum.",),
        swelling=sec.swelling,
        migration=(
            "Migration is the main risk — skin thins at an entry before the bar exits.",
            "Anti-eyebrow and surface nape need lifestyle buy-in or they will not last.",
        ),
        rejection=(
            "Rejection and migration overlap — early removal preserves better scar than waiting.",
        ),
        common_mistakes=sec.common_mistakes + ("Sleeping on surface work.",),
        desert_healing=sec.desert_healing,
        when_to_call=sec.when_to_call,
        who_should_avoid=sec.who_should_avoid,
        katelyn_recommendations=sec.katelyn_recommendations,
        video_links=sec.video_links,
        photo_links=sec.photo_links,
    )


def _overview(name: str) -> EncyclopediaSections:
    ex = _extras("overview")
    return EncyclopediaSections(
        who_its_good_for=ex["who_its_good_for"],
        downsizing=ex["downsizing"],
        swimming=ex["swimming"],
        exercise=ex["exercise"],
        sleeping=("Follow the specific placement guide for sleep rules — they vary by piercing.",),
        cleaning=("Sterile saline, hands off, no harsh chemicals — details in each placement guide.",),
        changing_jewelry=("Do not change jewelry until your piercer confirms the timeline for that placement.",),
        swelling=("Some swelling every placement is normal day 1–5; embedding is not.",),
        migration=("Migration risk depends on placement — surface and bridge highest, lobe lowest.",),
        rejection=("Rejection signs: thinning skin, jewelry sitting closer to the surface over weeks.",),
        common_mistakes=("Mall kiosks, mystery metal, twisting jewelry, and skipping downsizing.",),
        desert_healing=DESERT_BASE,
        when_to_call=("Spreading infection signs, embedding, or a bump that will not calm after two weeks.",),
        who_should_avoid=("Active infection at the site; anatomy that cannot support safe angle.",),
        katelyn_recommendations=(
            f"Use this {name} overview to pick a placement, then read the specific guide before booking.",
            "Ear curation clients start with a consult map — not a walk-in stack of holes.",
        ),
        video_links=(("Piercing encyclopedia hub", "/piercing_types_las_vegas_authority_hub/"),),
        photo_links=(("Studio gallery — piercing", "/studio_gallery/#katelyn-piercing"),),
    )


def _not_offered(name: str) -> EncyclopediaSections:
    ex = _extras("not_offered")
    return EncyclopediaSections(
        who_its_good_for=ex["who_its_good_for"],
        downsizing=ex["downsizing"],
        swimming=ex["swimming"],
        exercise=ex["exercise"],
        sleeping=("N/A — not performed at Work of Art.",),
        cleaning=("N/A",),
        changing_jewelry=("N/A",),
        swelling=("N/A",),
        migration=("N/A",),
        rejection=("N/A",),
        common_mistakes=("Going to an unqualified provider for placements outside our scope.",),
        desert_healing=("See our desert piercing aftercare guide for piercings we do perform.",),
        when_to_call=("N/A",),
        who_should_avoid=("N/A",),
        katelyn_recommendations=(
            "Browse piercings we offer in the encyclopedia hub — I would rather redirect you honestly.",
        ),
        video_links=(("Piercing types we offer", "/piercing_types_las_vegas_authority_hub/"),),
        photo_links=(),
    )


_BUILDERS = {
    "lobe": _lobe,
    "cartilage": _cartilage,
    "nasal": _nasal,
    "oral": _oral,
    "facial": _nasal,
    "body": _body,
    "surface": _surface,
    "overview": _overview,
    "not_offered": _not_offered,
}


def sections_for(slug_id: str, name: str) -> EncyclopediaSections:
    profile = PROFILE_MAP.get(slug_id, "cartilage")
    builder = _BUILDERS.get(profile, _cartilage)
    return builder(name)
