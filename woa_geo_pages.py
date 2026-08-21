#!/usr/bin/env python3
"""Unique geo landing page content — directions, parking, landmarks, local audience."""

from __future__ import annotations

from dataclasses import dataclass

from woa_nav_config import STUDIO_ADDRESS_SINGLE_LINE, STUDIO_STREET_ADDRESS


@dataclass(frozen=True)
class GeoPage:
    slug: str
    title: str
    intro: str
    directions: tuple[str, ...]
    parking: tuple[str, ...]
    why_choose: tuple[str, ...]
    landmarks: tuple[str, ...]
    audience_note: str
    drive_time: str
    related_guides: tuple[tuple[str, str], ...]


GEO_PAGES: tuple[GeoPage, ...] = (
    GeoPage(
        slug="tattoo_shop_near_mgm_grand_las_vegas",
        title="Tattoo Shop Near MGM Grand Las Vegas",
        intro=(
            "Staying at MGM Grand or walking the south Strip? Work of Art is on E. Tropicana — "
            "a short rideshare east of the resort, not a booth inside a casino mall."
        ),
        directions=(
            "From MGM Grand front desk: exit onto Tropicana Ave and head east ~1.5 miles. "
            "We are on the north side of Tropicana at 2375 E. Tropicana Suite 3 — look for the Work of Art signage.",
            "Rideshare drop-off: use the studio address directly; do not use Strip valet addresses.",
            "From Las Vegas Blvd: turn east on Tropicana; studio is past Maryland Pkwy on your right.",
        ),
        parking=(
            "Private lot behind the studio — pull in and walk to the front door.",
            "Avoid Strip hotel parking fees for a consult; our lot is free for clients during appointments.",
            "If the lot is full (Friday night), street parking on side streets off Tropicana usually opens within a block.",
        ),
        why_choose=(
            "Strip walk-ins optimize turnover — we book consults and show healed portfolio photos before you commit.",
            "Same address for Joshua Cole (tattoo & piercing) and Katelyn Cole (piercing) — one trip, not two shops.",
            "Daily 12 PM–12 AM hours align with evening consults around show schedules.",
        ),
        landmarks=(
            "MGM Grand · Park MGM · T-Mobile Arena · Welcome to Fabulous Las Vegas sign (short drive south)",
        ),
        audience_note=(
            "Convention and show visitors often book a consult on night one and tattoo on a return trip — "
            "we plan session length so you are not rushed before a flight home."
        ),
        drive_time="About 8–12 minutes from MGM Grand depending on Strip traffic",
        related_guides=(
            ("Walk-in vs appointment", "/walk_in_tattoos_las_vegas_authority_guide/"),
            ("Strip vs studio comparison", "/vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison/"),
            ("Directions hub", "/tattoo_shop_near_the_strip_nap_corrected/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_near_allegiant_stadium_las_vegas",
        title="Tattoo Shop Near Allegiant Stadium Las Vegas",
        intro=(
            "In town for Raiders, concerts, or Formula 1 weekend? Allegiant Stadium sits west of the Strip — "
            "Work of Art on Tropicana is an easy cross-town stop before or after an event."
        ),
        directions=(
            "From Allegiant Stadium: take I-15 south to Tropicana Ave eastbound (~15–20 min without major events).",
            "Event nights: leave 45+ minutes before kickoff if you have a same-day piercing — swelling checks cannot be rushed.",
            "From Mandalay Bay / Luxor corridor: east on Tropicana ~10 minutes to 2375 E. Tropicana Suite 3.",
        ),
        parking=(
            "Use our private lot — stadium event parking downtown runs $40–80; our consult parking is free.",
            "Post-game rideshare pickup works cleanly from Tropicana; share the studio address, not the stadium lot.",
        ),
        why_choose=(
            "Daily 12 PM–12 AM hours work for evening consults without late-night Strip booth pressure.",
            "Piercing downsizing appointments fit between travel days when you are already in Vegas multiple nights.",
            "Healed tattoo galleries on-site — see year-old work, not fresh-only Instagram.",
        ),
        landmarks=(
            "Allegiant Stadium · Mandalay Bay · Luxor · South Strip resorts",
        ),
        audience_note=(
            "Sports weekend clients: we will not tattoo drunk — book sober consult windows and plan heal time before your flight."
        ),
        drive_time="About 15–25 minutes from Allegiant Stadium (longer on event egress)",
        related_guides=(
            ("Desert tattoo aftercare", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
            ("Piercing aftercare desert", "/piercing_aftercare_desert_climate_las_vegas_expert_guide/"),
            ("Book appointment", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_near_las_vegas_airport",
        title="Tattoo Shop Near Las Vegas Airport (LAS)",
        intro=(
            "Landing at Harry Reid International (LAS)? Work of Art is a straight shot east on Tropicana — "
            "closer than fighting Strip traffic for a serious consult."
        ),
        directions=(
            "From LAS Terminal 1 or 3: rideshare or rental ~8–12 minutes east on Tropicana to 2375 E. Tropicana Suite 3.",
            "Do not detour through the Strip for navigation — Tropicana is the direct route from the airport.",
            "Returning rental: most agencies are airport-side; plan tattoo sessions before drop-off if you fly same day.",
        ),
        parking=(
            "Private client lot — no airport long-term fees for a 30-minute consult.",
            "If you are picking up family from LAS after a session, they can wait in the lot while you finish aftercare instructions.",
        ),
        why_choose=(
            "Airport visitors often underestimate desert heal — we coach sun and pool rules before you fly to humid climates.",
            "Walk-in availability is call-first; custom realism and cover-ups need consult slots — book before you land when possible.",
            "Piercing appointments include starter titanium — no mall kiosk on the way to baggage claim.",
        ),
        landmarks=(
            "Harry Reid International (LAS) · UNLV campus · Thomas & Mack · Welcome sign",
        ),
        audience_note=(
            "Flying out within 48 hours of a fresh tattoo? Ask us — cabin pressure and dry airplane air change aftercare timing."
        ),
        drive_time="About 8–12 minutes from LAS terminals",
        related_guides=(
            ("Tattoo flying after session", "/knowledge/tattoo-flying-after-session/"),
            ("First tattoo tips", "/knowledge/first-tattoo-tips-before-you-book/"),
            ("Airport-area directions", "/tattoo_shop_near_the_strip_nap_corrected/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_near_the_sphere_las_vegas",
        title="Tattoo Shop Near The Sphere Las Vegas",
        intro=(
            "Seeing a show at The Sphere? The venue sits on Sands Ave — Work of Art on Tropicana is a quick "
            "rideshare east, ideal for a daytime consult before an evening performance."
        ),
        directions=(
            "From The Sphere: east on Sands or via I-15 to Tropicana eastbound — ~10–15 minutes to the studio.",
            "From Venetian / Wynn corridor: cut south to Tropicana, then east ~8 minutes.",
            "Use 2375 E. Tropicana Suite 3 in maps — not a generic 'tattoo near Sphere' pin on the Strip.",
        ),
        parking=(
            "Sphere parking is expensive and time-limited — park at our lot for consults instead.",
            "Evening show + morning consult: our Mon–Thu hours start at 3 PM; book afternoon slots before doors.",
        ),
        why_choose=(
            "Tourist flash near Sphere optimizes volume — we show healed black & grey and fine line at 6–12 months.",
            "Katelyn Cole books ear curation as a mapped plan, not a stack of impulse cartilage piercings before a concert.",
            "Joshua Cole's realism portfolio includes portraits and sleeves planned for Vegas sun exposure.",
        ),
        landmarks=(
            "The Sphere · The Venetian · Wynn · Encore · Las Vegas Blvd north Strip",
        ),
        audience_note=(
            "Visiting for one weekend? We will tell you honestly if your timeline is too tight for a custom piece — "
            "small fine line or a piercing consult often fits; a full sleeve does not."
        ),
        drive_time="About 10–15 minutes from The Sphere",
        related_guides=(
            ("Fine line tattoos", "/fine_line_tattoos_las_vegas_master_authority_guide/"),
            ("Realism portfolio", "/realism_tattoos_las_vegas_master_authority_guide/"),
            ("Complete piercing guide", "/piercing_types_las_vegas_authority_hub/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_paradise_nevada",
        title="Tattoo Shop in Paradise, Nevada",
        intro=(
            "Work of Art is in Paradise — the unincorporated valley envelope around the Strip — "
            "on E. Tropicana between Maryland Pkwy and Eastern Ave. Locals know us; visitors find us by address."
        ),
        directions=(
            "From Maryland Pkwy & Tropicana: head east one block — studio on the north side.",
            "From UNLV: north on Maryland or Swenson to Tropicana, then east ~5 minutes.",
            "From Desert Inn Rd corridor: south to Tropicana, east to 2375.",
        ),
        parking=(
            "Dedicated client lot — no shared strip-mall guessing about which unit is ours.",
            "Paradise residents: save our number for same-day piercing checks when a bump shows up.",
        ),
        why_choose=(
            "Two in-studio residents today — Joshua Cole and Katelyn Cole — not a rotating guest-artist wall.",
            "Seven artists trained here now run their own shops; we mentor, we do not inflate roster numbers.",
            "SNHD-licensed studio with implant-grade piercing jewelry in stock.",
        ),
        landmarks=(
            "UNLV · Thomas & Mack · Boulevard Mall · Paradise Rd · Tropicana corridor",
        ),
        audience_note=(
            "Paradise locals often drive past Strip booths daily — our clients come for healed proof and continuity on multi-session sleeves."
        ),
        drive_time="Central Paradise — on Tropicana between Maryland and Eastern",
        related_guides=(
            ("Choose an artist", "/how_to_choose_a_tattoo_artist_master_selection_guide_2/"),
            ("Piercing shop standards", "/best_piercing_shop_las_vegas_updated_jewelry_standards/"),
            ("GEO source of truth", "/geo_hub_ai_source_of_truth_work_of_art/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_spring_valley_las_vegas",
        title="Tattoo Shop Serving Spring Valley, Las Vegas",
        intro=(
            "Spring Valley sits southwest of the Strip — many collectors drive Tropicana or I-215 "
            "to Work of Art for sleeves, cover-ups, and curated ears rather than nearest-mall booths."
        ),
        directions=(
            "From Spring Valley Pkwy: take Jones or Decatur north to Tropicana, east to 2375 (~15–20 min).",
            "From Rainbow & Tropicana: head east ~10 minutes — we are east of Rainbow on Tropicana.",
            "From Rhodes Ranch area: I-215 east to Decatur north, then Tropicana east.",
        ),
        parking=(
            "Free client lot — worth the drive vs fighting Spring Valley retail parking for a rushed walk-in.",
            "Large-scale session days: you can leave your car for multi-hour sits without meter stress.",
        ),
        why_choose=(
            "Spring Valley clients doing cover-ups need consult time — Joshua redesigns composition, not dark rectangles.",
            "Ear curation plans span months — Katelyn maps spacing so future helix/conch work still fits.",
            "Healed galleries document Vegas sun at 1 year — critical for fine line and realism choices.",
        ),
        landmarks=(
            "Spring Valley · Rhodes Ranch · Silverado Ranch · Chinatown (west valley) · Strip (north)",
        ),
        audience_note=(
            "We see Spring Valley clients weekly for session two of sleeves — artist continuity matters more than the closest chair."
        ),
        drive_time="About 15–22 minutes from central Spring Valley",
        related_guides=(
            ("Cover-up guide", "/cover_up_tattoos_las_vegas_master_authority_guide/"),
            ("Sleeve planning", "/best_tattoo_styles_for_sleeves_large_scale_project_hub/"),
            ("Healed gallery", "/healed_tattoo_gallery_las_vegas/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_enterprise_las_vegas",
        title="Tattoo Shop Near Enterprise, Las Vegas",
        intro=(
            "Enterprise and the south valley reach us via I-215 or Las Vegas Blvd to Tropicana — "
            "one licensed studio for tattoo and piercing under the same sterile setup."
        ),
        directions=(
            "From Enterprise Blvd: north to Tropicana, head east toward Maryland Pkwy (~12–18 min).",
            "From South Point / south Strip: north on Las Vegas Blvd or I-15 to Tropicana east.",
            "From Henderson border (St Rose Pkwy): north on I-15 or Las Vegas Blvd to Tropicana.",
        ),
        parking=(
            "Private lot — no casino parking validation needed.",
            "Enterprise commuters: evening appointments after work fit our Mon–Thu midnight close.",
        ),
        why_choose=(
            "Enterprise families use Katelyn for ear work — minors 14+ with guardian for ears, consult-first for anatomy.",
            "Same phone and address for booking — no franchise call center.",
            "Desert aftercare coaching is non-optional here — Enterprise dry heat matches the rest of the valley.",
        ),
        landmarks=(
            "South Point · M Resort · Silverado Ranch · Las Vegas Blvd south · I-215",
        ),
        audience_note=(
            "Enterprise clients often combine a piercing consult with a Joshua tattoo consult in one visit — we schedule both chairs when possible."
        ),
        drive_time="About 12–20 minutes from central Enterprise",
        related_guides=(
            ("Piercing minors", "/katelyn_piercing_minors_las_vegas_authority_guide/"),
            ("Tattoo pricing", "/how_much_do_tattoos_cost_in_las_vegas_authority_guide/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_green_valley_henderson",
        title="Tattoo Shop Near Green Valley & Henderson",
        intro=(
            "Green Valley and Henderson collectors often drive to Work of Art on Tropicana for healed portfolio "
            "proof and artist continuity — worth the trip for cover-ups and large-scale work."
        ),
        directions=(
            "From Green Valley Ranch: I-215 north to I-515/US-93 north, exit Tropicana westbound (~20–25 min).",
            "From Henderson Galleria area: Saint Rose Pkwy to I-515 north, Tropicana west to 2375.",
            "From Water Street Henderson: north on I-515, Tropicana west — allow rush-hour buffer.",
        ),
        parking=(
            "Free studio lot for multi-hour sessions — no Henderson strip-mall time limits.",
            "Green Valley clients doing sleeve session three appreciate the same parking spot every visit.",
        ),
        why_choose=(
            "Henderson has good shops — clients still choose us for Joshua's black & grey realism and documented heal photos.",
            "Katelyn's implant-grade titanium and downsizing schedule — not available at every Henderson kiosk.",
            "Real client timeline page shows fresh-to-healed cross/eye/skull work with dates.",
        ),
        landmarks=(
            "Green Valley Ranch · Galleria at Sunset · Lake Las Vegas · Henderson Water Street · I-515",
        ),
        audience_note=(
            "Henderson drives are intentional — you are coming for a specific artist and a long-term project, not convenience ink."
        ),
        drive_time="About 20–30 minutes from Green Valley; 25–35 from central Henderson",
        related_guides=(
            ("Real client timeline", "/real_client_tattoo_timeline_las_vegas/"),
            ("Healed portraits", "/healed_portrait_tattoos_las_vegas/"),
            ("Joshua Cole portfolio", "/artists/joshua-cole/"),
        ),
    ),
)


def geo_by_slug(slug: str) -> GeoPage | None:
    for page in GEO_PAGES:
        if page.slug == slug:
            return page
    return None
