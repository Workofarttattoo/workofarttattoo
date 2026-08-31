#!/usr/bin/env python3
"""Final human copy pass: repair casing damage, remove SEO jargon from visible
copy, humanize breadcrumb labels, and fix truncated TOC labels sitewide.

Run from repo root: python3 humanize_final_edit_pass.py
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXCLUDE_PARTS = {"skipped_upload_build", "artists_raw", "obsidian_gold", ".git", "node_modules"}
EXCLUDE_NAMES = {"skipped_pages_clipboard.html"}


def target_files() -> list[Path]:
    files = []
    for p in sorted(ROOT.rglob("*.html")):
        if any(part in EXCLUDE_PARTS for part in p.parts):
            continue
        if p.name in EXCLUDE_NAMES:
            continue
        files.append(p)
    return files


# ---------------------------------------------------------------------------
# 1. Casing repair: a bad lowercase pass turned "Piercing" into "piercing" in
#    headings, nav labels, page titles, and the brand name.
# ---------------------------------------------------------------------------
TITLE_WORDS = (
    "Guide", "Guides", "Jewelry", "Aftercare", "Healing", "Shop", "Tips",
    "Topics", "Authority", "Services", "Minors", "Specials", "Hub", "Standards",
)
CASING_RULES: list[tuple[str, str]] = []
for w in TITLE_WORDS:
    CASING_RULES.append((f"piercing {w}", f"Piercing {w}"))
CASING_RULES += [
    ("piercing Las Vegas |", "Piercing Las Vegas |"),
    ("Tattoo &amp; piercing", "Tattoo &amp; Piercing"),
    ("Tattoo & piercing", "Tattoo & Piercing"),
    ("Tattoos &amp; piercing", "Tattoos &amp; Piercing"),
    ("Tattoos & piercing", "Tattoos & Piercing"),
    (">piercing ", ">Piercing "),
    ('current-label">forward Helix', 'current-label">Forward Helix'),
    (">piercing,", ">Piercing,"),
    ('content="piercing ', 'content="Piercing '),
]

# ---------------------------------------------------------------------------
# 2. Visible SEO jargon, leaked internal notes, and robotic copy.
# ---------------------------------------------------------------------------
COPY_RULES: list[tuple[str, str]] = [
    # Geo pages: "NAP" is directory-listing jargon, not reader language.
    (">Studio NAP</p>", ">Studio address &amp; contact</p>"),
    # Henderson page spoke to Google, not to the reader.
    (
        "This page stays indexed because Henderson clients often plan larger tattoos around artist fit and repeat sessions.",
        "Most of our Henderson clients are planning bigger work — sleeves, cover-ups, multi-session projects — where picking the right artist matters more than picking the closest chair.",
    ),
    (
        "Green Valley is consolidated here so Henderson searchers get one stronger page instead of thin neighborhood duplicates.",
        "If you're coming from Green Valley, this is your page too — same studio, same team, one honest set of directions.",
    ),
    # Paradise page.
    (
        "This page exists to clarify the real studio location, not to claim a second storefront.",
        "To be clear: this is not a second storefront. Paradise is simply the real locality around our E. Tropicana address.",
    ),
    (
        "This is the exact city/locality context for the studio address, not a doorway page pretending to be another branch.",
        "Same studio, same rooms, same team — Paradise just happens to be the locality our address technically sits in.",
    ),
    # Near-the-Strip hub page.
    (
        "This hub helps Strip visitors plan a real tattoo or piercing appointment at Work of Art without relying on thin neighborhood doorway pages.",
        "This page helps Strip visitors plan a real tattoo or piercing appointment at Work of Art — honest directions, honest timing, no gimmicks.",
    ),
    (
        "Use the canonical studio address:",
        "Use the exact studio address:",
    ),
    # Official location page: internal directory-cleanup directive shown to readers.
    (
        "(725) 224-1240 only. Remove any legacy listing numbers that do not forward to this line.",
        "(725) 224-1240 — this is the only number that reaches the studio. Older numbers still floating around on directory sites do not forward to us.",
    ),
    # Strip-vs-studio comparison: self-praising framing.
    (
        "This authoritative comparison breaks down the systemic differences between a premier Las Vegas tattoo and piercing shop and the high-volume, low-cost storefronts lining the Strip.",
        "Here is an honest breakdown of how a dedicated Las Vegas studio differs from the high-volume storefronts lining the Strip \u2014 and why that difference shows up on your skin years later.",
    ),
    # Pain chart intro: "authoritative analysis ... for the modern collector".
    (
        "An authoritative analysis of dermal sensitivity, nerve density, and pain management strategies for the modern collector. Precision artistry meets biological understanding.",
        "A straight answer to the question every client asks: where does it hurt most, why, and what we do in the chair to make the tougher spots manageable.",
    ),
    # Walk-in page footer tagline.
    (
        "Elevating the Vegas tattoo experience through clinical precision and healed portfolio work.",
        "Custom tattoos and piercings, a consult-first approach, and healed work to back it up.",
    ),
    # Pricing page badge.
    ("5.0 Star Rated Excellence", "5.0-Star Google Rating"),
    # Typos.
    ("with clearance and a adjusted plan", "with clearance and an adjusted plan"),
    ("rescue plan ( prescribed cream)", "rescue plan (a prescribed cream)"),
]


# ---------------------------------------------------------------------------
# 2b. Hand-edit replacement pairs replayed on every build (idempotent).
# ---------------------------------------------------------------------------
REPLAY_PAIRS: list[tuple[str, str]] = [('<p class="text-body-md text-on-surface-variant">Patents, Material Design systems work, and additional project gems can be layered here as you publish the canonical links.</p>', ''),
 ('Joshua Cole is widely recognized as the best black and grey realism artist in Las Vegas. With over 20 years of dedicated practice and a focus on high-fidelity anatomical precision, his work at '
  'Work of Art Tattoo &amp; Piercing delivers anatomical precision and long-term healed clarity in the valley.',
  'Joshua Cole was named Best of Las Vegas in 2025 and 2026 by BusinessRate.com, and he has spent over 20 years focused almost entirely on black and grey realism. Still, the honest way to judge any '
  'artist is their healed work — look for contrast and detail that still read clearly years later. His portfolio at Work of Art Tattoo &amp; Piercing is built for exactly that comparison.'),
 ('Best of Vegas 2025 &amp; 2026', 'Best of Las Vegas 2025 &amp; 2026 · BusinessRate.com'),
 ('<!-- INSERT ISSUING BEST OF VEGAS PUBLICATION HERE ONCE CONFIRMED FROM PLAQUE -->', ''),
 ('To choose a tattoo artist is to choose a legacy. In the upper echelons of the industry, the distinction between a "tattooist" and an "artist" is defined by a deep-seated understanding of '
  'classical art principles. At Work of Art, we believe that the skin is merely a substrate, and the rules of the Old Masters—Rembrandt, Caravaggio, and Sargent—apply as much to ink as they do to '
  'oil.',
  'Choosing a tattoo artist means choosing who you trust with something permanent, so it deserves more care than scrolling a feed. The difference between a tattooist and an artist usually comes down '
  'to fundamentals. At Work of Art we lean on the same rules the Old Masters used — Rembrandt, Caravaggio, Sargent — because value, light, and composition matter on skin just as much as they do in '
  'oil.'),
 ('The technical bridge from canvas to skin requires more than just steady hands; it requires an artist who can mentally translate the viscosity of paint to the fluid dynamics of pigment under the '
  'dermis. This "fine art lens" allows an artist to predict how a tattoo will settle over decades, ensuring that the integrity of the composition remains as striking in twenty years as it was on day '
  'one.',
  'Moving a design from canvas to skin takes more than steady hands. Skin stretches, ages, and softens detail over time, and a good artist plans for that from the first sketch. That is what fine art '
  'training buys you: the ability to predict how a piece will settle so it still reads clearly in twenty years — not just on day one.'),
 ("A portfolio is a curated window into an artist's soul, but to the untrained eye, it can be deceptive. High-contrast filters and strategic lighting can mask technical flaws. To spot strong "
  'portfolio work, look for the **integrity of the line** and the **purity of the saturation**.',
  'A portfolio only tells the truth if you know what to look for. High-contrast filters and clever lighting can hide technical flaws. Two things are very hard to fake: clean, confident linework and '
  'even, fully saturated pigment.'),
 ('Fresh ink is vibrant and forgiving. Demand to see "healed and settled" photos from 1-2 years post-procedure. This proves the artist knows how to pack pigment so it stays sharp.',
  'Fresh ink is vibrant and forgiving. Ask to see healed, settled photos from one to two years out — that is the real proof an artist knows how to place pigment so it stays sharp.'),
 ('If the portfolio looks "muddy" or lacks clear highlights, the artist hasn\'t mastered the physics of light.',
  'If the portfolio looks "muddy" or lacks clear highlights, the work will only get softer as it ages.'),
 ('Premium Tattoo &amp; Piercing Studio. Defining the standard of Las Vegas artistry through classical fine art training.',
  'Custom tattoos and professional piercing in Las Vegas, grounded in classical fine art training.'),
 ('See /artists/joshua-cole/ and /artists/teralyn/.',
  'See <a class="text-secondary underline" href="/artists/joshua-cole/">Joshua’s page</a> and <a class="text-secondary underline" href="/artists/teralyn/">Teralyn’s page</a>.'),
 ('Portfolio at /artists/joshua-cole/.', 'See <a class="text-secondary underline" href="/artists/joshua-cole/">Joshua’s portfolio</a>.'),
 ('see Teralyn at /artists/teralyn/.', 'see <a class="text-secondary underline" href="/artists/teralyn/">Teralyn’s page</a>.'),
 ('see Joshua Cole at /artists/joshua-cole/.', 'see <a class="text-secondary underline" href="/artists/joshua-cole/">Joshua Cole’s page</a>.'),
 ('Our approach utilizes the "three-tone" methodology: high-contrast blacks for longevity, mid-tone greys for texture, and precise highlights for that final \'pop\' of life.',
  'We work in three tones: high-contrast blacks for longevity, mid greys for texture, and precise highlights for that final pop of life.'),
 ('This is the strongest true before-and-after evidence in the supplied set. The old tattoo is visibly present in the top frame, and the floral design in the lower frame shows how color, leaf '
  'shapes, and movement can pull attention away from the original mark.',
  'This is a true before-and-after. The old tattoo is clearly visible in the top frame, and the floral design below it shows how color, leaf shapes, and movement pull the eye away from the original '
  'mark.'),
 ('Large reworks often work better when the artist treats the entire area as one composition instead of trying to hide individual marks one at a time. These two photos are grouped as one arm project '
  'so the page does not overstate the number of finished projects.',
  'Large reworks often turn out better when the artist treats the entire area as one composition instead of hiding individual marks one at a time. Both photos below are from the same arm — one '
  'project, two angles.'),
 ('These are supplied studio examples for the cover-up and rework page. Where the original tattoo is not visible, captions describe the visible strategy without calling it a confirmed cover-up.',
  'All photos here are from our studio. Where the original tattoo is not visible in the shot, the caption describes the design strategy instead of claiming a confirmed cover-up — we would rather '
  'undersell than overstate.'),
 ('If it goes a fraction of a millimeter Too deep: pigment can spread beyond the intended line, increasing the risk of blurred edges or tattoo blowout and causing unnecessary tissue trauma.el the '
  'resistance of the dermal layer, a tactile skill that takes years to master.',
  'If it goes a fraction of a millimeter too deep, pigment can spread beyond the intended line — blurred edges, blowout, and unnecessary tissue trauma. The artist has to feel the resistance of the '
  'dermal layer through the machine, a tactile skill that takes years to develop.'),
 ('EXPLORE FINE ART &amp; ORIGINAL OILS /#gallery', 'EXPLORE FINE ART &amp; ORIGINAL OILS'),
 ('Fine line tattooing is often misunderstood as merely a stylistic choice. In reality, it is a high-stakes engineering challenge where the medium is living tissue and the instrument is a singular '
  'point of steel.',
  'Fine line tattooing gets treated like a purely aesthetic choice. In practice it is a technical discipline where the medium is living skin and the tool is a single point of steel — there is '
  'nowhere for a mistake to hide.'),
 ('CERTIFIED SINGLE-NEEDLE MASTERS', 'SINGLE-NEEDLE SPECIALISTS'),
 ("The Las Vegas sun isn't just bright; it's predatory. UV rays penetrate the skin and break down the pigment particles. For a fresh tattoo, sun exposure is catastrophic.",
  "The Las Vegas sun isn't just bright — it's relentless. UV rays penetrate the skin and break down pigment particles, and for a fresh tattoo, direct sun is one of the fastest ways to lose detail "
  'you paid for.'),
 ('With average humidity often dropping below 10%, your skin becomes a battleground. Without proper intervention, the desert air will pull moisture directly from your healing dermis, leading to '
  'heavy scabbing, cracking, and eventual ink loss.',
  'With humidity often below 10%, your skin is fighting the climate the whole time it heals. Left unprotected, desert air pulls moisture straight out of healing skin — heavy scabbing, cracking, and '
  'lost ink follow.'),
 ('Master Artist — Tattoo &amp; Piercing — Black &amp; Grey Realism', 'Tattoo Artist &amp; Studio Lead — Black &amp; Grey Realism'),
 ('HOSPITAL-GRADE STERILIZATION', 'STERILE, SINGLE-USE SETUP'),
 ('Hospital-grade sterilization, single-use needles, and a fully aseptic procedure environment.', 'Autoclave sterilization, single-use needles, and a fully aseptic procedure environment.'),
 ('Hospital-grade sterilization and single-use equipment are our baseline. We maintain the cleanest environment in Las Vegas.',
  'Single-use needles, autoclave sterilization, and a spotless setup are our baseline — every client, every session, no exceptions.'),
 ('Medical-grade sterilization protocol', 'Strict sterilization protocol — autoclave plus single-use needles'),
 ('>Medical Grade Precision</p>', '>Sterile, Precise Technique</p>'),
 ('>Medical Grade Safety</p>', '>Sterile, Single-Use Setup</p>'),
 ('Hospital-level sterilization', 'Autoclave sterilization and single-use needles'),
 ('>Clinically Informed<', '>Anatomy-Informed<'),
 ('>Elite Cleanliness</h3>', '>Sterile, Always</h3>'),
 ('Fresh piercings deserve jewelry selected for anatomy, swelling, and sensitivity. This page keeps material claims general until the studio owner verifies current jewelry documentation.',
  'Fresh piercings deserve jewelry selected for your anatomy, expected swelling, and skin sensitivity — not whatever happens to be in the display case. Here is how I actually choose what goes in on '
  'day one.'),
 ('Fresh piercings deserve jewelry selected for anatomy, swelling, and sensitivity. This page keeps material claims general until the studio ow…',
  'Fresh piercings deserve jewelry selected for your anatomy, expected swelling, and skin sensitivity — not whatever happens to be in the display case.…'),
 (' We keep the language factual until owner-verified credential and material documentation is added.', ''),
 ('No placeholder roster slots: everyone listed below books real sessions.', 'Everyone listed below actually works here and books real sessions — no padded roster.'),
 ('Use this page as the source of truth when updating Google Business Profile, Yelp, Apple Maps, Fresha, and other directories. If a listing shows an old phone number or address, replace it with the '
  'details below.',
  'This page is the official studio information — the details we confirm ourselves. If you spot a listing on Google, Yelp, Apple Maps, or Fresha showing an old phone number or address, the details '
  'below are the correct ones.'),
 ('Exact public hours remain an owner-verification item before they should be used in structured data or directories.',
  'Hours can shift around holidays and big event weeks, so we would rather you text us than trust a stale listing.'),
 ('Minor piercing rules remain an owner-verification item. Call or text before visiting so the studio can confirm the current age, consent, and ID requirements.',
  'Rules for piercing minors can change, so call or text before visiting and we will confirm the current age, consent, and ID requirements.'),
 ('Use this number for walk-in checks, booking questions, and directions — not artist personal mobiles. Update any outdated directory listings to match.',
  'Use this number for walk-in checks, booking questions, and directions. If you see a different number on an older listing somewhere, it does not reach us.'),
 ('(725) 224-1240 only. Remove any legacy listing numbers that do not forward to this line.',
  '(725) 224-1240 — this is the only number that reaches the studio. Older numbers still floating around on directory sites do not forward to us.'),
 ('leading-tight">Piercing Las Vegas | Complete Guide — Ear, Nose, Body &amp; Book Online</h1>', 'leading-tight">Piercing in Las Vegas — the Complete Guide to Ear, Nose &amp; Body Work</h1>'),
 ('current-label">Best Piercing Shop Las Vegas Updated Jewelry Standards</span>', 'current-label">Piercing Shop &amp; Jewelry Standards</span>'),
 ('Often considered the gold standard for sleeve tattoos in Las Vegas, large-scale black and grey realism offers a timeless elegance. This style relies on soft gradients, high contrast, and '
  'photographic detail.',
  'Large-scale black and grey realism is the backbone of most sleeves we build. The style relies on soft gradients, high contrast, and photographic detail.'),
 ('black and grey work ages exceptionally well and maintains its prestige over decades.', 'black and grey work ages exceptionally well and stays readable for decades.'),
 ('The flow of a Japanese sleeve is unparalleled, as the background elements are designed specifically to flow around the joints and curves of the limb.',
  'Japanese sleeves flow like almost nothing else because the background elements are designed to wrap around the joints and curves of the limb.'),
 ('For clients who want a darker high-impact aesthetic, Biomechanical sleeves are unrivaled.', 'For clients who want a darker, high-impact look, biomechanical sleeves are hard to beat.'),
 ('>Ready to Start Your Journey?<', '>Ready to Start Your Sleeve?<'),
 ('This authoritative comparison breaks down the systemic differences between a premier Las Vegas tattoo and piercing shop and the high-volume, low-cost storefronts lining the Strip.',
  'Here is an honest breakdown of how a dedicated Las Vegas studio differs from the high-volume storefronts lining the Strip — and why that difference shows up on your skin years later.'),
 ('An authoritative analysis of dermal sensitivity, nerve density, and pain management strategies for the modern collector. Precision artistry meets biological understanding.',
  'A straight answer to the question every client asks: where does it hurt most, why, and what we do in the chair to make the tougher spots manageable.'),
 ('Elevating the Vegas tattoo experience through clinical precision and healed portfolio work.', 'Custom tattoos and piercings, a consult-first approach, and healed work to back it up.'),
 ('5.0 Star Rated Excellence', '5.0-Star Google Rating'),
 ('>Studio NAP</p>', '>Studio address &amp; contact</p>'),
 ('This page stays indexed because Henderson clients often plan larger tattoos around artist fit and repeat sessions.',
  'Most of our Henderson clients are planning bigger work — sleeves, cover-ups, multi-session projects — where picking the right artist matters more than picking the closest chair.'),
 ('Green Valley is consolidated here so Henderson searchers get one stronger page instead of thin neighborhood duplicates.',
  "If you're coming from Green Valley, this is your page too — same studio, same team, one honest set of directions."),
 ('This page exists to clarify the real studio location, not to claim a second storefront.',
  'To be clear: this is not a second storefront. Paradise is simply the real locality around our E. Tropicana address.'),
 ('This is the exact city/locality context for the studio address, not a doorway page pretending to be another branch.',
  'Same studio, same rooms, same team — Paradise just happens to be the locality our address technically sits in.'),
 ('This hub helps Strip visitors plan a real tattoo or piercing appointment at Work of Art without relying on thin neighborhood doorway pages.',
  'This page helps Strip visitors plan a real tattoo or piercing appointment at Work of Art — honest directions, honest timing, no gimmicks.'),
 ('Use the canonical studio address:', 'Use the exact studio address:'),
 ('with clearance and a adjusted plan', 'with clearance and an adjusted plan'),
 ('rescue plan ( prescribed cream)', 'rescue plan (a prescribed cream)'),
 ('>ear and body piercing at Work of Art — Ear &amp; Helix</h2>', '>Ear &amp; Body Piercing, Done Right</h2>'),
 ('Looking for a ear and body piercing at Work of Art or helix body piercing in Las Vegas? Katelyn Cole leads calm ear piercing — lobe, helix body piercing, conch, daith, and full ear curation — '
  'with starter jewelry and luxury gold. Our studio on E. Tropicana Ave uses a clean studio process for every piercing on the ear and select facial/body placements.',
  'Katelyn Cole leads calm, unhurried piercing — lobes, helix, conch, daith, and full ear curation — with starter jewelry sized for healing and gold options once you are healed. Every piercing at '
  'our E. Tropicana studio is done with single-use needles and sterile technique, and jewelry is fit to your anatomy, not just to a trend.'),
 ('>starter jewelry &amp; 14k gold jewelry<', '>Starter jewelry &amp; 14k gold options<'),
 ('>Piercing studio on E. Tropicana — Work of Art standards</a>', '>our piercing &amp; jewelry standards</a>'),
 ('>Piercing at Work of Art</span>', '>Tattoos + Piercing</span>'),
 ('>tattoo and piercing at Work of Art — Las Vegas</h2>', '>Tattoos and Piercing Under One Roof</h2>'),
 ('Work of Art is the tattoo and piercing studio in Las Vegas and tattoo and body piercing studio locals use on one stop — 2375 E. Tropicana, minutes from the Strip. A tattoo and piercing studio on '
  'E. Tropicana Ave means sterile body piercing with Katelyn Cole and custom tattoo work with Joshua Cole under the same roof.',
  'Work of Art is the studio Las Vegas locals use for both — tattoos and piercing at 2375 E. Tropicana, minutes from the Strip. Katelyn Cole handles piercing, Joshua Cole handles tattoos, and '
  'everything happens under one licensed roof with the same sterile standards.'),
 ('<strong>Helix body piercing</strong>, ear piercing, and <strong>body piercings at Work of Art</strong> services:', 'Start with these guides:'),
 ('>Why Locals Choose This Tattoo and Piercing Studio</h2>', '>Why Locals Choose Work of Art</h2>'),
 ('Work of Art is the local tattoo and piercing studio collectors use for custom tattoo work without strip-shop shortcuts. Joshua Cole leads tattoo work and also offers piercing; Katelyn Cole is our '
  'professional piercer; Teralyn tattoos and pierces, including fine line, floral, script, and detailed smaller tattoos.',
  'Locals come to us for careful, custom work without strip-shop shortcuts. Joshua Cole leads tattooing and also offers piercing; Katelyn Cole is our professional piercer; Teralyn tattoos and '
  'pierces — fine line, floral, script, and detailed smaller pieces. Every project starts with a real conversation.'),
 ('Look for licensed tattoo and piercing studios in Las Vegas with healed portfolios, sterile setup, and artists who consult before they ink. Work of Art is a tattoo and piercing studio in Las Vegas '
  'collectors use for black &amp; grey realism, fine line, and piercing — custom tattoo work and piercing consultations at 2375 E. Tropicana Ave, Suite 3, minutes from the Strip.',
  'Look for a licensed studio with healed portfolios (not just fresh photos), a sterile setup you can actually see, and artists who consult before they ink. That is the standard we hold ourselves to '
  'at Work of Art — black &amp; grey realism, fine line, and professional piercing at 2375 E. Tropicana, minutes from the Strip.'),
 ('Work of Art Tattoo &amp; Piercing is the <strong>tattoo and piercing studio in Las Vegas</strong> and <strong>tattoo studio in Las Vegas</strong> answer for east Strip and UNLV-area searches — '
  'same team for east-Strip and UNLV-area visits, with one-studio convenience for piercing and ink in one visit.',
  'We are just east of the Strip on Tropicana, a few minutes from UNLV. One visit covers both: tattoos and piercing from the same team, in the same licensed studio.'),
 ('Work of Art Tattoo &amp; Piercing at 2375 E. Tropicana Suite 3 is the nearby tattoo and piercing studio for many major Strip resorts — typically about five minutes by car. We are the tattoo and '
  'piercing studio in Las Vegas locals book for black &amp; grey realism, fine line, and piercing under one roof.',
  'From most major Strip resorts, Work of Art at 2375 E. Tropicana Suite 3 is about five minutes by car. Locals and visitors book us for black &amp; grey realism, fine line, and piercing under one '
  'roof.'),
 ('Skip shops that rush vacation flash. Work of Art is a tattoo and piercing studio in Las Vegas option with licensed artists, sterile setup, and portfolios you can review before you commit — '
  'portfolios you can review before you book, without strip-mall shortcuts.',
  'Skip anywhere that rushes vacation flash. A shop earns your trust with licensed artists, a sterile setup, and portfolios you can review before you commit. That is exactly how we run Work of Art — '
  'no strip-mall shortcuts.'),
 ('Work of Art Tattoo &amp; Piercing is the tattoo and piercing studio near the Las Vegas Strip at 2375 E. Tropicana — experienced artists and studio sanitation for tourists and locals.',
  'We are minutes from the Strip at 2375 E. Tropicana — close enough for a short rideshare, far enough to skip the tourist-floor rush. Tourists and locals get the same careful setup and the same '
  'unhurried consult.'),
 ('Work of Art Tattoo &amp; Piercing at 2375 E. Tropicana Suite 3 is the black and grey tattoo artist in Las Vegas choice for locals and Strip visitors — book a consult for black and grey tattoo '
  'ideas, sleeves, or single-session realism.',
  'Joshua Cole works out of Work of Art at 2375 E. Tropicana Suite 3. Book a consult to talk through black and grey ideas, sleeves, or single-session realism — bring references and we will give you '
  'an honest read on size, placement, and budget.'),
 ('>Where is tattoo and piercing at Work of Art in Las Vegas?</h3>', '>Can I get a tattoo and a piercing in the same visit?</h3>'),
 ('Work of Art Tattoo &amp; Piercing at 2375 E. Tropicana Suite 3 — one address for tattoo and piercing at Work of Art, tattoos and piercings in one studio, and helix body piercing. Tattoo artists '
  'and Katelyn Cole (piercing) share the same clean studio practices.',
  'Yes — one address covers both: Work of Art Tattoo &amp; Piercing at 2375 E. Tropicana Suite 3. Our tattoo artists and Katelyn Cole (piercing) share the same sterile setup and the same standards.'),
 ('Choose a licensed piercing studio in Las Vegas with single-use needles, autoclave sterilization, and piercers who explain piercing aftercare. Work of Art is a piercing studio on E. Tropicana for '
  'locals that also welcomes tourists — book ahead for curated ear work.',
  'A safe piercing studio uses single-use needles and autoclave sterilization, and takes real time to explain aftercare. That is our baseline at Work of Art. Locals book ahead for curated ear '
  'projects; visitors are always welcome.'),
 ('Katelyn Cole is our professional piercer — ear piercing, anatomical ear curation, and luxury jewelry styling with careful placement.',
  'Katelyn Cole is our professional piercer — ear piercing, anatomy-first ear curation, and jewelry styling with a careful, unhurried approach.'),
 ('Katelyn Cole is our professional piercer — ear piercing, anatomical ear curation, and luxury jewelry styling with clinical precision.',
  'Katelyn Cole is our professional piercer — ear piercing, anatomy-first ear curation, and jewelry styling with a careful, unhurried approach.'),
 ('While we recommend appointments for custom large-scale work, Work of Art provides same-day walk-in availability for both tattoos and piercings to accommodate the fast pace of Las Vegas.',
  'We recommend appointments for custom large-scale work, but we take same-day walk-ins for tattoos and piercings when chairs are open. Text first and we will tell you honestly whether today works.'),
 ('Joshua Cole leads <strong>realism tattoo</strong> and <strong>black and grey realism tattoo</strong> at Work of Art — portraits, <strong>realism tattoos</strong>, and custom sleeves. See our',
  'Joshua Cole was named Best of Las Vegas in 2025 and 2026 by BusinessRate.com, after 20+ years focused on black and grey realism — portraits, statues, and full sleeves. Judge for yourself by the '
  'healed results in our'),
 ('>artists</h3><p class="font-body-md text-on-surface-variant">Expert guide from Work of Art Tattoo &amp; Piercing — artists.</p>',
  '>Meet the Artists</h3><p class="font-body-md text-on-surface-variant">Portfolios, specialties, and booking for Joshua, Katelyn, and Teralyn.</p>'),
 ('>studio videos</h3><p class="font-body-md text-on-surface-variant">Expert guide from Work of Art Tattoo &amp; Piercing — studio videos.</p>',
  '>Studio Videos</h3><p class="font-body-md text-on-surface-variant">Real sessions and studio life — see the space and the process before you book.</p>')]
COPY_RULES.extend(REPLAY_PAIRS)

STUB_LABELS = {'/cover-up-tattoos-las-vegas/': 'our cover-up tattoos guide',
 '/official_location_hours_contact/': 'our official location & hours page',
 '/tattoo_piercing_shop_near_unlv/': 'our UNLV-area guide',
 '/tattoo_shop_near_allegiant_stadium_las_vegas/': 'our Allegiant Stadium visitor guide',
 '/tattoo_shop_near_las_vegas_airport/': 'our airport visitor guide',
 '/tattoo_shop_near_mgm_grand_las_vegas/': 'our MGM Grand visitor guide',
 '/tattoo_shop_near_the_sphere_las_vegas/': 'our Sphere visitor guide',
 '/tattoo_shop_near_the_strip_nap_corrected/': 'our Las Vegas Strip guide',
 '/tattoo_shop_paradise_nevada/': 'our Paradise, NV guide',
 '/tattoo_shop_serving_henderson_nevada/': 'our Henderson guide',
 '/tattoo_shop_spring_valley_las_vegas/': 'our Spring Valley guide',
 '/walk-in-tattoos-las-vegas/': 'our walk-in tattoos guide'}
STUB_RE = re.compile(r'This (?:location guide|page|guide) has been consolidated\. Continue to <a href="([^"]+)">[^<]+</a>\.')

KNOWLEDGE_LABELS = {'Best Piercing Shop Las Vegas Updated Jewelry Standards': 'Our Piercing & Jewelry Standards',
 'Best Tattoo Styles For Sleeves Large Scale Project Hub': 'Sleeve & Large-Scale Tattoo Styles',
 'Cover Up Tattoos Las Vegas Master': 'Cover-Up Tattoos in Las Vegas',
 'Fine Line Tattoos Las Vegas Master': 'Fine Line Tattoos in Las Vegas',
 'How Much Do Tattoos Cost In Las Vegas': 'Tattoo Pricing in Las Vegas',
 'How To Choose A Tattoo Artist Master Selection Guide 2': 'How to Choose a Tattoo Artist',
 'Realism Tattoos Las Vegas Master': 'Realism Tattoos in Las Vegas',
 'Tattoo Healing In Desert Climate Expert Aftercare Guide': 'Desert Climate Tattoo Aftercare',
 'Tattoo Pain Chart Placement Sensitivity Guide': 'Tattoo Pain & Placement Chart',
 'Tattoo Shop Near The Strip Nap Corrected': 'Tattoo Shop Near the Strip',
 'Vegas Tattoo Shop Vs Cheap Strip Tattoo Ultimate Comparison': 'Studio vs. Strip Shop Comparison',
 'Walk In Tattoos Las Vegas': 'Walk-In Tattoos in Las Vegas'}


# ---------------------------------------------------------------------------
# 3. Breadcrumb pill labels: raw slugs like "eczema skin science las vegas"
#    become readable titles derived from the page's own directory.
# ---------------------------------------------------------------------------
PILL_RE = re.compile(r'(<span class="woa-guide-pill-current-label">)([^<]*)(</span>)')
SMALL_WORDS = {"a", "an", "and", "the", "of", "vs", "in", "for", "to", "on", "with", "near", "at", "by", "or"}
SPECIAL = {
    "unlv": "UNLV", "mgm": "MGM", "nv": "NV", "faq": "FAQ", "llc": "LLC",
    "tmobile": "T-Mobile", "ai": "AI", "geo": "GEO", "nap": "NAP", "qa": "Q&A",
}
TRAILING_NOISE = [
    "las vegas authority guide", "master authority guide", "ultimate authority guide",
    "authority guide", "authority hub", "nap corrected", "geo seo optimized",
    "las vegas", "las", "vegas",
]


def human_label(dirname: str) -> str:
    words = dirname.replace("_", " ").replace("-", " ").strip().lower()
    changed = True
    while changed:
        changed = False
        for noise in TRAILING_NOISE:
            if words.endswith(" " + noise):
                words = words[: -len(noise) - 1].rstrip()
                changed = True
    out = []
    for i, w in enumerate(words.split()):
        if w in SPECIAL:
            out.append(SPECIAL[w])
        elif w in SMALL_WORDS and i != 0:
            out.append(w)
        else:
            out.append(w.capitalize())
    return " ".join(out)


def fix_pill(path: Path, text: str, counts: Counter) -> str:
    if path.parent == ROOT or path.parent.name == "artists_build":
        return text

    def repl(m: re.Match) -> str:
        current = m.group(2).strip()
        # Only replace labels that are raw slug text (all lowercase).
        if current and current != current.lower():
            return m.group(0)
        label = human_label(path.parent.name)
        if not label:
            return m.group(0)
        counts["breadcrumb"] += 1
        return m.group(1) + label + m.group(3)

    return PILL_RE.sub(repl, text)


# ---------------------------------------------------------------------------
# 4. TOC labels truncated mid-word by an old [:28] slice.
# ---------------------------------------------------------------------------
TOC_LINK_RE = re.compile(r'(<a class="text-secondary underline hover:no-underline text-sm" href="#([a-z0-9-]+)">)([^<]+)(</a>)')
HEADING_ID_RE = r'id="{aid}"[^>]*>\s*(?:<h[23][^>]*>)?([^<]+)<'


def fix_toc(text: str, counts: Counter) -> str:
    def repl(m: re.Match) -> str:
        aid, label = m.group(2), m.group(3)
        hm = re.search(HEADING_ID_RE.format(aid=re.escape(aid)), text, re.S)
        if not hm:
            return m.group(0)
        full = hm.group(1).split("\u2014")[0].strip()
        if full and full != label and full[:28].strip() == label.strip() and len(full) <= 60:
            counts["toc"] += 1
            return m.group(1) + full + m.group(4)
        return m.group(0)

    return TOC_LINK_RE.sub(repl, text)


def main() -> None:
    counts: Counter = Counter()
    touched = 0
    for path in target_files():
        original = path.read_text(encoding="utf-8")
        text = original
        for old, new in CASING_RULES:
            n = text.count(old)
            if n:
                counts[f"casing: {old[:40]}"] += n
                text = text.replace(old, new)
        for old, new in COPY_RULES:
            n = text.count(old)
            if n:
                counts[f"copy: {old[:50]}"] += n
                text = text.replace(old, new)
        def _stub_repl(m: re.Match) -> str:
            href = m.group(1)
            label = STUB_LABELS.get(href, "our main guide")
            counts["stub"] += 1
            return (
                f"We\u2019ve folded this page into {label} so everything lives in one place. "
                f'<a href="{href}">Continue there for directions, timing, and booking</a>.'
            )

        text = STUB_RE.sub(_stub_repl, text)
        if path.parts and path.parent.parent.name == "knowledge":
            for _old, _new in KNOWLEDGE_LABELS.items():
                if ">" + _old + "</a>" in text:
                    counts["kb-label"] += 1
                    text = text.replace(">" + _old + "</a>", ">" + _new + "</a>")
        text = fix_pill(path, text, counts)
        text = fix_toc(text, counts)
        if text != original:
            path.write_text(text, encoding="utf-8")
            touched += 1
    print(f"Touched {touched} files")
    for key, n in sorted(counts.items()):
        print(f"{n:6d}  {key}")


if __name__ == "__main__":
    main()
