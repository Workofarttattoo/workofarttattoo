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
        slug="tattoo_shop_serving_summerlin_las_vegas",
        title="Tattoo Shop Serving Summerlin, Las Vegas",
        intro=(
            "Work of Art is not in Summerlin. It is a destination studio on E. Tropicana for Summerlin "
            "collectors who would rather choose by artist fit, healed work, and consultation quality than by the closest chair."
        ),
        directions=(
            "From Summerlin, most clients come across the valley using Summerlin Parkway, I-215, Charleston, Flamingo, or Tropicana depending on where they start.",
            "Use the studio address directly in maps: 2375 E. Tropicana Ave, Suite 3. Vegas traffic changes quickly around Strip events, so check the route before leaving.",
            "For large tattoo sessions, plan the drive like an appointment day: eat first, bring reference material, and leave room for setup and aftercare instructions.",
        ),
        parking=(
            "Use the studio lot instead of resort or mall parking. It is calmer for consults and easier when you are sitting for a longer tattoo session.",
            "If you are coming from the west side after work, allow extra buffer when Strip or arena traffic is active.",
        ),
        why_choose=(
            "Summerlin clients often come for Joshua Cole's realism, black and grey, portraits, sleeves, and cover-up planning.",
            "Teralyn is a good fit for fine line floral work, script, high-detail smaller tattoos, and commissioned custom drawings.",
            "Katelyn Cole handles piercing and ear curation for clients who want placement planned beyond a single impulse piercing.",
        ),
        landmarks=(
            "Summerlin Parkway · Downtown Summerlin · Red Rock area · Charleston corridor · I-215 west beltway",
        ),
        audience_note=(
            "This is a destination-studio page: the point is not that we are closest to Summerlin, but that serious work is worth choosing by the artist and the healed result."
        ),
        drive_time="Cross-valley drive from Summerlin; traffic varies by starting point and event timing",
        related_guides=(
            ("Joshua Cole portfolio", "/artists/joshua-cole/"),
            ("Realism tattoos", "/realism_tattoos_las_vegas_master_authority_guide/"),
            ("Cover-up tattoos", "/cover_up_tattoos_las_vegas_master_authority_guide/"),
            ("Teralyn fine line", "/artists/teralyn/"),
            ("Healed tattoo gallery", "/healed_tattoo_gallery_las_vegas/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_serving_downtown_las_vegas",
        title="Tattoo Shop Serving Downtown Las Vegas",
        intro=(
            "Downtown Las Vegas clients, Arts District visitors, hospitality workers, and hotel guests can reach Work of Art by heading toward the Tropicana corridor. "
            "We are not downtown; we are the studio you choose when the artist fit matters more than staying on Fremont or Main Street."
        ),
        directions=(
            "From the Arts District or Fremont area, expect a drive or rideshare south toward Tropicana rather than a walkable downtown stop.",
            "If you are working a hospitality shift, book enough time for paperwork, placement, stencil changes, and aftercare before your next call time.",
            "For visitors staying downtown, schedule tattoo or piercing work before heavy nightlife plans, not after drinking.",
        ),
        parking=(
            "Downtown parking and valet timing can be unpredictable; the studio lot is simpler once you arrive on Tropicana.",
            "Rideshare is often the easiest choice from Fremont hotels, especially if you are heading back to the Arts District or Fremont Street later.",
        ),
        why_choose=(
            "Downtown visitors may want walk-in energy, but custom tattoos still need the right artist, placement discussion, and sober decision-making.",
            "Joshua Cole is the fit for realism, portraits, sleeves, and cover-ups; Teralyn is the fit for fine line floral work, script, and detailed small tattoos.",
            "Piercing clients can work with Katelyn Cole for anatomy-first placement and follow-up planning.",
        ),
        landmarks=(
            "Arts District · Fremont East · Downtown hotels · Main Street · Fremont Street Experience",
        ),
        audience_note=(
            "Use this page for the broader Downtown market. For landmark-specific tourist planning around Fremont Street, use the Fremont guide."
        ),
        drive_time="Downtown-to-Tropicana trip; allow more time during event and nightlife traffic",
        related_guides=(
            ("Fremont Street guide", "/tattoo_shop_near_fremont_street_las_vegas/"),
            ("Walk-in tattoo guide", "/walk_in_tattoos_las_vegas_authority_guide/"),
            ("How to choose an artist", "/how_to_choose_a_tattoo_artist_master_selection_guide_2/"),
            ("Tattoo healing in Vegas", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_piercing_shop_near_unlv",
        title="Tattoo & Piercing Shop Near UNLV",
        intro=(
            "UNLV, Thomas & Mack, and Maryland Parkway are close to the Tropicana side of Las Vegas, which makes Work of Art a practical studio for students, staff, and campus visitors. "
            "Work of Art is an independent business and is not affiliated with UNLV."
        ),
        directions=(
            "From the UNLV area, head toward Tropicana and use 2375 E. Tropicana Ave, Suite 3 as the destination.",
            "If you are scheduling around class or work, separate quick walk-in ideas from larger custom tattoos that need a consultation.",
            "Thomas & Mack event traffic can change the easy route; check maps before leaving campus.",
        ),
        parking=(
            "Studio parking is simpler than campus or event parking when you are coming for a consult.",
            "Bring valid ID. Do not schedule a tattoo or piercing between classes so tightly that aftercare instructions get rushed.",
        ),
        why_choose=(
            "Small tattoos and script can be great when they are planned carefully; Teralyn handles piercing plus fine line, script, florals, and detailed smaller tattoos.",
            "Bigger work like sleeves, portraits, and cover-ups should start with Joshua Cole so the design fits the body and the long-term plan.",
            "Katelyn Cole and Teralyn offer piercing services for clients who want calm placement discussion and follow-up guidance.",
        ),
        landmarks=(
            "UNLV · Thomas & Mack Center · Maryland Parkway · Tropicana corridor · Paradise area",
        ),
        audience_note=(
            "This page is written for campus-area convenience without pushing students into impulsive spending. Ask questions first; book when the idea and budget make sense."
        ),
        drive_time="Near the UNLV and Tropicana corridor; timing varies with campus and event traffic",
        related_guides=(
            ("Paradise guide", "/tattoo_shop_paradise_nevada/"),
            ("Flash tattoos", "/flash_art_deals_under_100/"),
            ("Teralyn portfolio", "/artists/teralyn/"),
            ("Piercing guide", "/piercing_types_las_vegas_authority_hub/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_near_mgm_grand_las_vegas",
        title="Tattoo Shop Near MGM Grand Las Vegas",
        intro=(
            "Staying at MGM Grand or walking the south Strip? Work of Art is on E. Tropicana — "
            "a practical rideshare east of the resort, not a booth inside a casino mall."
        ),
        directions=(
            "From MGM Grand, use the studio address in maps and route east on Tropicana Ave instead of searching for a generic Strip tattoo pin.",
            "Rideshare drop-off: use the studio address directly; do not use Strip valet addresses.",
            "From Las Vegas Blvd: turn east on Tropicana and keep enough schedule room for resort traffic, stencil changes, and aftercare.",
        ),
        parking=(
            "Use the studio address for arrival instead of a resort garage or valet pin.",
            "If you are coming from a hotel, ask the rideshare driver to take you to the studio address, not to a nearby casino entrance.",
            "Check current traffic before leaving the Strip, especially on fight nights, concert nights, and big convention weeks.",
        ),
        why_choose=(
            "Strip-front shops are built for walk-in volume. We're built for a real consult — reference photos, healed results, and enough time to get the design right before you commit.",
            "Same address for Joshua Cole, Katelyn Cole, and Teralyn — one real studio, not a fake neighborhood branch page.",
            "Check the official hours page before planning around a show; evening traffic near Tropicana can change quickly.",
        ),
        landmarks=(
            "MGM Grand · Park MGM · T-Mobile Arena · Welcome to Fabulous Las Vegas sign (short drive south)",
        ),
        audience_note=(
            "Convention and show visitors often book a consult on night one and tattoo on a return trip — "
            "we plan session length so you are not rushed before a flight home."
        ),
        drive_time="MGM Grand to E. Tropicana studio trip; timing changes with resort and event traffic",
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
            "From Allegiant Stadium, Mandalay Bay, or Luxor, route toward Tropicana and use the studio address directly.",
            "Event nights change traffic quickly. Schedule tattoo or piercing work when you are sober and not racing a kickoff, concert, or flight.",
            "For stadium weekends, compare your hotel, rideshare pickup zone, and post-event plans before assuming the map route will stay easy.",
        ),
        parking=(
            "Avoid treating stadium parking, resort garages, and tattoo appointment arrival as the same plan.",
            "Post-game rideshare pickup works cleanly from Tropicana; share the studio address, not the stadium lot.",
        ),
        why_choose=(
            "Check official hours before planning around kickoff or a concert; event traffic can move slowly around the stadium corridor.",
            "Piercing downsizing appointments fit between travel days when you are already in Vegas multiple nights.",
            "Healed tattoo galleries on-site — see year-old work, not fresh-only Instagram.",
        ),
        landmarks=(
            "Allegiant Stadium · Mandalay Bay · Luxor · South Strip resorts",
        ),
        audience_note=(
            "Sports weekend clients: we will not tattoo drunk — book sober consult windows and plan heal time before your flight."
        ),
        drive_time="Allegiant Stadium corridor to E. Tropicana trip; timing changes sharply on event days",
        related_guides=(
            ("Desert tattoo aftercare", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
            ("Piercing aftercare desert", "/piercing_aftercare_desert_climate_las_vegas_expert_guide/"),
            ("Book appointment", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_near_las_vegas_airport",
        title="Tattoo Shop Near Harry Reid International Airport",
        intro=(
            "Landing at Harry Reid International Airport? Work of Art is a straightforward Tropicana-area studio to plan around arrival, rental car timing, or a return flight — "
            "closer than fighting Strip traffic for a serious consult."
        ),
        directions=(
            "From Harry Reid airport terminals, use the studio address in maps and compare the terminal route with your hotel or rental-car route.",
            "Do not detour through the Strip for navigation — Tropicana is the direct route from the airport.",
            "Returning rental: most agencies are airport-side; plan tattoo sessions before drop-off if you fly same day.",
        ),
        parking=(
            "If you are combining a consult with an airport pickup or drop-off, leave room for terminal delays and aftercare instructions.",
            "Do not book a fresh tattoo or piercing so close to a flight that cleaning, covering, or comfort become rushed.",
        ),
        why_choose=(
            "Airport visitors often underestimate desert heal — we coach sun and pool rules before you fly to humid climates.",
            "Walk-in availability is call-first; custom realism and cover-ups need consult slots — book before you land when possible.",
            "Piercing appointments include placement discussion and aftercare planning — not a rushed stop on the way to baggage claim.",
        ),
        landmarks=(
            "Harry Reid International (LAS) · UNLV campus · Thomas & Mack · Welcome sign",
        ),
        audience_note=(
            "Flying soon after a fresh tattoo or piercing? Ask us about clothing, cleaning access, luggage straps, and dry airplane air before you commit to timing."
        ),
        drive_time="Harry Reid airport-to-Tropicana route; timing varies by terminal, rental-car plans, and traffic",
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
            "rideshare-style trip east, ideal for a daytime consult before an evening performance."
        ),
        directions=(
            "From The Sphere, Venetian, Wynn, or the north Strip, use the studio address in maps and leave room for venue traffic.",
            "North Strip routes change during show entry, show exit, and convention traffic; avoid squeezing tattoo planning into a narrow window.",
            "Use 2375 E. Tropicana Ave, Suite 3 in maps — not a generic 'tattoo near Sphere' pin on the Strip.",
        ),
        parking=(
            "Keep venue parking and appointment arrival separate in your plan.",
            "Evening show plus tattoo planning works best when you check current studio hours and leave a buffer before doors.",
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
        drive_time="Sphere and north Strip to E. Tropicana trip; timing depends on event and resort traffic",
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
            "From Maryland Pkwy, UNLV, or Paradise-area hotels, use 2375 E. Tropicana Ave, Suite 3 as the destination.",
            "Surface streets around UNLV, Thomas & Mack, and Tropicana can change with class, event, and commute traffic.",
            "From Desert Inn Rd corridor: south to Tropicana, east to 2375.",
        ),
        parking=(
            "Use the studio address and look for the Work of Art storefront when you arrive.",
            "Paradise residents can call before coming in with piercing irritation, jewelry-fit, or tattoo-healing questions so the visit is routed correctly.",
        ),
        why_choose=(
            "Three in-studio residents today — Joshua Cole, Katelyn Cole, and Teralyn — not a rotating guest-artist wall.",
            "One studio for tattoos, piercing consults, follow-up questions, and aftercare guidance.",
            "This is the exact city/locality context for the studio address, not a doorway page pretending to be another branch.",
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
            "From Spring Valley, compare Tropicana, Flamingo, Decatur, Jones, and I-215 routes before leaving.",
            "West-valley traffic changes with commute patterns and Strip events, so give yourself space for stencil changes and consultation.",
            "From Rhodes Ranch area: I-215 east to Decatur north, then Tropicana east.",
        ),
        parking=(
            "Plan the drive as part of the appointment, especially for larger work or cover-up consultations.",
            "If you are coming after work, avoid stacking another commitment immediately after the tattoo or piercing appointment.",
        ),
        why_choose=(
            "Spring Valley clients doing cover-ups need consult time — Joshua redesigns composition, not dark rectangles.",
            "Ear curation plans span months — Katelyn maps spacing so future helix/conch work still fits.",
            "Healed galleries document Las Vegas sun and dry-air realities over time — critical for fine line and realism choices.",
        ),
        landmarks=(
            "Spring Valley · Rhodes Ranch · Silverado Ranch · Chinatown (west valley) · Strip (north)",
        ),
        audience_note=(
            "Spring Valley clients are usually choosing artist continuity for multi-session work rather than the closest open chair."
        ),
        drive_time="Spring Valley to E. Tropicana trip; timing varies by west-valley starting point",
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
            "but this page is being consolidated because the current repository does not prove enough Enterprise-specific demand for a separate indexed URL."
        ),
        directions=(
            "From Enterprise or the south valley, compare I-215, I-15, Las Vegas Blvd, and Tropicana before leaving.",
            "From South Point / south Strip: north on Las Vegas Blvd or I-15 to Tropicana east.",
            "From Henderson border (St Rose Pkwy): north on I-15 or Las Vegas Blvd to Tropicana.",
        ),
        parking=(
            "Use the studio address in navigation instead of a resort, mall, or generic tattoo pin.",
            "Enterprise commuters should check the official hours page before planning after-work appointments.",
        ),
        why_choose=(
            "Enterprise and south-valley users are better served by the near-Strip hub until owner/Search Console evidence proves a separate page is useful.",
            "Same phone and address for booking — no franchise call center.",
            "Desert aftercare coaching is non-optional here — Enterprise dry heat matches the rest of the valley.",
        ),
        landmarks=(
            "South Point · M Resort · Silverado Ranch · Las Vegas Blvd south · I-215",
        ),
        audience_note=(
            "Enterprise clients often combine a piercing consult with a Joshua tattoo consult in one visit — we schedule both chairs when possible."
        ),
        drive_time="South-valley to E. Tropicana trip; timing varies with current traffic",
        related_guides=(
            ("Piercing minors", "/katelyn_piercing_minors_las_vegas_authority_guide/"),
            ("Tattoo pricing", "/how_much_do_tattoos_cost_in_las_vegas_authority_guide/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_green_valley_henderson",
        title="Tattoo Shop Serving Green Valley, Henderson",
        intro=(
            "Green Valley and Henderson collectors often drive to Work of Art on Tropicana for healed portfolio "
            "proof and artist continuity — worth the trip for cover-ups and large-scale work."
        ),
        directions=(
            "From Green Valley Ranch, compare I-215, I-515/US-93, Eastern, and surface routes before leaving.",
            "From Henderson Galleria area: Saint Rose Pkwy to I-515 north, Tropicana west to 2375.",
            "From Water Street Henderson: north on I-515, Tropicana west — allow rush-hour buffer.",
        ),
        parking=(
            "Use the studio address in navigation and confirm current arrival details before longer appointments.",
            "Green Valley clients doing repeat sleeve or cover-up sessions should plan travel time around the full appointment window.",
        ),
        why_choose=(
            "Henderson has good shops — clients still choose us for Joshua's black & grey realism and documented heal photos.",
            "Katelyn's piercing work is consultation-led, with placement and follow-up discussed before you commit.",
            "Real client timeline page shows fresh-to-healed cross/eye/skull work with dates.",
        ),
        landmarks=(
            "Green Valley Ranch · Galleria at Sunset · Lake Las Vegas · Henderson Water Street · I-515",
        ),
        audience_note=(
            "Henderson drives are intentional — you are coming for a specific artist and a long-term project, not convenience ink."
        ),
        drive_time="Green Valley or Henderson to E. Tropicana trip; timing varies with current traffic",
        related_guides=(
            ("Broader Henderson guide", "/tattoo_shop_serving_henderson_nevada/"),
            ("Real client timeline", "/real_client_tattoo_timeline_las_vegas/"),
            ("Healed portraits", "/healed_portrait_tattoos_las_vegas/"),
            ("Joshua Cole portfolio", "/artists/joshua-cole/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_serving_henderson_nevada",
        title="Tattoo Shop Serving Henderson, Nevada",
        intro=(
            "Henderson is a larger market than Green Valley alone. This page is for Henderson collectors who are willing to drive to one studio on E. Tropicana for artist continuity, healed results, piercing consults, and larger tattoo planning."
        ),
        directions=(
            "From Henderson, most routes work back toward Tropicana through I-515/US-93, Eastern, Pecos, or other surface streets depending on your neighborhood.",
            "Water Street, Anthem, Inspirada, and Whitney Ranch clients should check traffic before choosing between freeway and surface routes.",
            "For multi-session tattoos, plan the drive as part of the project rhythm: consult, first session, heal, and return for the next phase.",
        ),
        parking=(
            "Use the studio lot for consults and longer appointments. You are not dealing with resort garages or event lots once you arrive.",
            "If you are coming from the southeast valley after work, give yourself enough room for rush-hour traffic and stencil adjustments.",
        ),
        why_choose=(
            "Joshua Cole is the Henderson fit for black and grey realism, portraits, sleeves, cover-ups, and color realistic imagery.",
            "Teralyn handles fine line floral work, script, detailed smaller tattoos, and custom drawings by commission.",
            "Katelyn Cole handles piercing and ear curation for clients who want placement planned around anatomy and long-term styling.",
        ),
        landmarks=(
            "Water Street District · Green Valley · Whitney Ranch · Anthem · Inspirada · Eastern Avenue corridor",
        ),
        audience_note=(
            "Henderson clients usually are not looking for the closest impulse chair; they are choosing the right artist for work they will live with."
        ),
        drive_time="Cross-valley trip from Henderson; timing depends heavily on neighborhood and commute traffic",
        related_guides=(
            ("Near-Strip visitor hub", "/tattoo_shop_near_the_strip_nap_corrected/"),
            ("Large-scale tattoo planning", "/best_tattoo_styles_for_sleeves_large_scale_project_hub/"),
            ("Cover-up tattoos", "/cover_up_tattoos_las_vegas_master_authority_guide/"),
            ("Piercing guide", "/piercing_types_las_vegas_authority_hub/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_serving_north_las_vegas",
        title="Tattoo Shop Serving North Las Vegas",
        intro=(
            "Work of Art is not in North Las Vegas. It is a single studio on E. Tropicana for clients willing to cross the valley for a specific tattoo artist, piercing consult, healed-work proof, and a quieter appointment environment."
        ),
        directions=(
            "From North Las Vegas, routes usually involve I-15, US-95/I-11, or surface streets feeding toward Tropicana.",
            "Do not plan this as a five-minute errand; cross-valley traffic changes with commute hours, construction, and Strip events.",
            "For cover-ups and sleeves, book a consult first so the drive is used for planning, not guesswork.",
        ),
        parking=(
            "The studio lot keeps arrival simple once you get across town.",
            "For long sessions, bring water, eat first, and avoid scheduling another appointment immediately after your tattoo.",
        ),
        why_choose=(
            "North Las Vegas collectors often choose Work of Art for Joshua Cole's realism, portraits, cover-ups, and large compositions.",
            "Teralyn is a fit for fine line, floral work, script, walk-in-sized pieces, and custom drawings by commission.",
            "Piercing clients can book Katelyn Cole for placement planning and follow-up questions instead of choosing by convenience alone.",
        ),
        landmarks=(
            "North Las Vegas · I-15 corridor · US-95/I-11 corridor · Craig Road · Aliante area",
        ),
        audience_note=(
            "This page is about choosing expertise over proximity. If the trip feels too far for an impulse tattoo, start with questions and book when it makes sense."
        ),
        drive_time="Cross-valley trip from North Las Vegas; plan around commute and event traffic",
        related_guides=(
            ("How to choose a tattoo artist", "/how_to_choose_a_tattoo_artist_master_selection_guide_2/"),
            ("Realism tattoos", "/realism_tattoos_las_vegas_master_authority_guide/"),
            ("Healed gallery", "/healed_tattoo_gallery_las_vegas/"),
            ("Piercing guide", "/piercing_types_las_vegas_authority_hub/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_near_las_vegas_convention_center",
        title="Tattoo Shop Near Las Vegas Convention Center",
        intro=(
            "Las Vegas Convention Center visitors have a different tattoo timeline than vacationers: badge hours, booth work, client dinners, flights, and hotel pools all matter. Work of Art is a single E. Tropicana studio for sober, planned tattoo and piercing appointments around that schedule."
        ),
        directions=(
            "From the Las Vegas Convention Center or West Hall area, use rideshare or drive toward Tropicana rather than trying to fit a tattoo into a narrow show-floor break.",
            "Exhibitors should avoid booking large work before setup, teardown, or a flight home.",
            "If you are staying near Resorts World or the north Strip, compare the Convention Center route with the Sphere and Strip guides before booking.",
        ),
        parking=(
            "Convention parking and rideshare zones are built for crowds. The studio lot is simpler once you arrive for the appointment.",
            "Bring your badge schedule and flight timing into the consult conversation so the tattoo plan matches the trip.",
        ),
        why_choose=(
            "Convention-week tattoos work best when the studio helps you think through clothing friction, sleep, alcohol, flights, sun, and pool plans.",
            "Walk-in-sized pieces may fit a Vegas work trip; sleeves, portraits, and cover-ups usually need a planned consult.",
            "Piercing clients should consider headset use, hotel pillows, and travel before choosing ear placement.",
        ),
        landmarks=(
            "Las Vegas Convention Center · West Hall · Paradise Road · Resorts World area · north Strip",
        ),
        audience_note=(
            "Do not book a tattoo so tightly between convention obligations that aftercare, sobriety, or travel timing becomes an afterthought."
        ),
        drive_time="Convention Center to E. Tropicana trip; leave buffer around show opening and closing traffic",
        related_guides=(
            ("Sphere guide", "/tattoo_shop_near_the_sphere_las_vegas/"),
            ("Strip guide", "/tattoo_shop_near_the_strip_nap_corrected/"),
            ("Tattoo flying after session", "/knowledge/tattoo-flying-after-session/"),
            ("Walk-in guide", "/walk_in_tattoos_las_vegas_authority_guide/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_near_mandalay_bay_las_vegas",
        title="Tattoo Shop Near Mandalay Bay Las Vegas",
        intro=(
            "Mandalay Bay, Luxor, Allegiant Stadium, and the south Strip all sit close to the Tropicana corridor. Work of Art is not inside Mandalay Bay or affiliated with MGM Resorts; it is a dedicated tattoo and piercing studio east of the Strip."
        ),
        directions=(
            "From Mandalay Bay or Luxor, rideshare or taxi east along Tropicana is usually more straightforward than moving through casino garages.",
            "Airport and south Strip plans often overlap here, so do not book tattoo work too close to a departing flight.",
            "For stadium weekends, check event traffic before assuming the short map distance will feel short in real life.",
        ),
        parking=(
            "Use the studio lot for your appointment instead of paying or waiting for resort garage access.",
            "If you are returning to a hotel pool, plan healing first. Fresh tattoos and piercings do not belong in pools.",
        ),
        why_choose=(
            "South Strip visitors often want something memorable; we help separate a quick walk-in idea from a custom tattoo that deserves a return trip.",
            "Joshua Cole fits realism, portraits, sleeves, cover-ups, blackwork, and color realistic imagery.",
            "Teralyn fits fine line floral work, script, small detailed tattoos, flash, and custom drawings by commission.",
        ),
        landmarks=(
            "Mandalay Bay · Luxor · Allegiant Stadium · Welcome to Fabulous Las Vegas sign · Harry Reid Airport",
        ),
        audience_note=(
            "This page is for south Strip planning. Use the Allegiant guide when your timing is built around a game, concert, or stadium event."
        ),
        drive_time="South Strip to Tropicana studio trip; traffic changes around stadium and resort events",
        related_guides=(
            ("Allegiant Stadium guide", "/tattoo_shop_near_allegiant_stadium_las_vegas/"),
            ("Airport guide", "/tattoo_shop_near_las_vegas_airport/"),
            ("Strip guide", "/tattoo_shop_near_the_strip_nap_corrected/"),
            ("Tattoo aftercare in Vegas", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_near_t_mobile_arena_las_vegas",
        title="Tattoo Shop Near T-Mobile Arena Las Vegas",
        intro=(
            "T-Mobile Arena visitors are usually planning around concerts, Golden Knights games, UFC weekends, or events near Park MGM and New York-New York. Work of Art is not affiliated with the arena, teams, promoters, or MGM Resorts; we are a separate studio on E. Tropicana."
        ),
        directions=(
            "From the Park MGM/New York-New York area, head toward Tropicana and use the studio address directly in maps.",
            "On event days, plan tattoo consultations before alcohol and before arena congestion peaks.",
            "Post-event appointments only make sense if the studio is open, you are sober, and you have enough time for aftercare instructions.",
        ),
        parking=(
            "Arena parking and rideshare zones are event-focused; the studio lot is easier for appointment arrivals.",
            "If you are dressed for an event, consider clothing friction on the tattoo or piercing placement before committing.",
        ),
        why_choose=(
            "A concert or fight weekend can inspire a tattoo, but the design still needs the right artist and a clean schedule.",
            "Small fine line or script ideas may fit Teralyn; realism, portraits, cover-ups, and larger work belong in a consult with Joshua Cole.",
            "Piercing clients should think about headphones, helmets, hats, and sleeping position after the event.",
        ),
        landmarks=(
            "T-Mobile Arena · Park MGM · New York-New York · Toshiba Plaza · south/central Strip",
        ),
        audience_note=(
            "Event-night planning is about timing, sobriety, and comfort. The best appointment is the one you can actually heal correctly."
        ),
        drive_time="T-Mobile Arena area to Tropicana studio trip; event traffic can add meaningful delay",
        related_guides=(
            ("MGM Grand guide", "/tattoo_shop_near_mgm_grand_las_vegas/"),
            ("Strip guide", "/tattoo_shop_near_the_strip_nap_corrected/"),
            ("Allegiant Stadium guide", "/tattoo_shop_near_allegiant_stadium_las_vegas/"),
            ("Walk-in tattoo guide", "/walk_in_tattoos_las_vegas_authority_guide/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_near_fashion_show_las_vegas",
        title="Tattoo Shop Near Fashion Show Las Vegas",
        intro=(
            "Fashion Show Las Vegas is a north Strip shopping, dining, and resort-area landmark. Work of Art is not inside the mall; it is a dedicated tattoo and piercing studio on E. Tropicana for clients who want privacy, consultation, artist selection, and healed-work proof."
        ),
        directions=(
            "From Fashion Show Las Vegas, rideshare is usually easier than moving between Strip garages before an appointment.",
            "If you are shopping before a piercing or tattoo, avoid tight clothing, heavy bags, or plans that will rub the fresh area afterward.",
            "Use the studio address in maps and leave extra time when north Strip traffic is heavy.",
        ),
        parking=(
            "The studio lot keeps the appointment separate from mall or resort parking decisions.",
            "For jewelry questions or ear curation, bring photos of current piercings and note any irritation before you arrive.",
        ),
        why_choose=(
            "Mall-adjacent searches often come from convenience. Work of Art is better framed as a dedicated studio with artist portfolios and aftercare support.",
            "Teralyn is a strong fit for fine line floral tattoos, script, and detailed small pieces after a shopping day.",
            "Katelyn Cole handles piercing and ear curation when jewelry fit and anatomy matter more than impulse timing.",
        ),
        landmarks=(
            "Fashion Show Las Vegas · Wynn · Encore · The Venetian · north Strip resorts",
        ),
        audience_note=(
            "Choose the studio because the work and follow-up fit you, not because it is the nearest storefront while you are shopping."
        ),
        drive_time="North Strip to Tropicana studio trip; plan around resort and shopping traffic",
        related_guides=(
            ("Sphere guide", "/tattoo_shop_near_the_sphere_las_vegas/"),
            ("Fine line tattoo guide", "/fine_line_tattoos_las_vegas_master_authority_guide/"),
            ("Piercing jewelry guide", "/piercing_jewelry_guide_las_vegas/"),
            ("Teralyn portfolio", "/artists/teralyn/"),
            ("Appointments", "/appointments/"),
        ),
    ),
    GeoPage(
        slug="tattoo_shop_near_fremont_street_las_vegas",
        title="Tattoo Shop Near Fremont Street Las Vegas",
        intro=(
            "Fremont Street searches are usually tourist searches: downtown hotels, live entertainment, bar-hopping, and a limited Vegas timeline. Work of Art is not on Fremont Street and is not affiliated with Fremont Street Experience; it is a dedicated studio on E. Tropicana."
        ),
        directions=(
            "From Fremont Street or downtown hotels, plan a rideshare or drive toward Tropicana instead of trying to squeeze a tattoo between drinks.",
            "Book before nightlife, not after it. We will not tattoo or pierce someone who is intoxicated.",
            "If you are flying home the next morning, ask about placement, clothing friction, and aftercare before committing.",
        ),
        parking=(
            "Downtown parking can be crowded or event-dependent; use the studio lot once you arrive.",
            "If your group is splitting up, share the exact studio address so nobody follows a generic downtown tattoo pin.",
        ),
        why_choose=(
            "A Fremont trip can make people want the nearest chair. A better tattoo starts with artist fit, sober timing, and healed-work examples.",
            "Teralyn can help with fine line, script, flash, and smaller detailed ideas when the scope is realistic.",
            "Joshua Cole is the better path for realism, portraits, sleeves, cover-ups, and anything that needs deeper planning.",
        ),
        landmarks=(
            "Fremont Street Experience · Downtown hotels · Fremont East · Arts District · Main Street",
        ),
        audience_note=(
            "Use this page for the landmark/tourist intent. Use the Downtown guide for broader downtown residents, workers, and Arts District planning."
        ),
        drive_time="Downtown/Fremont to Tropicana studio trip; nightlife and event traffic can change timing",
        related_guides=(
            ("Downtown Las Vegas guide", "/tattoo_shop_serving_downtown_las_vegas/"),
            ("Walk-in tattoo guide", "/walk_in_tattoos_las_vegas_authority_guide/"),
            ("Tattoo aftercare in Vegas", "/tattoo_healing_in_desert_climate_expert_aftercare_guide/"),
            ("Teralyn portfolio", "/artists/teralyn/"),
            ("Appointments", "/appointments/"),
        ),
    ),
)


GEO_PAGE_ACTIONS: dict[str, str] = {
    "tattoo_shop_serving_summerlin_las_vegas": "MERGE_301",
    "tattoo_shop_serving_downtown_las_vegas": "MERGE_301",
    "tattoo_piercing_shop_near_unlv": "MERGE_301",
    "tattoo_shop_near_mgm_grand_las_vegas": "KEEP_IMPROVE",
    "tattoo_shop_near_allegiant_stadium_las_vegas": "KEEP_IMPROVE",
    "tattoo_shop_near_las_vegas_airport": "KEEP_IMPROVE",
    "tattoo_shop_near_the_sphere_las_vegas": "KEEP_IMPROVE",
    "tattoo_shop_paradise_nevada": "KEEP",
    "tattoo_shop_spring_valley_las_vegas": "KEEP_IMPROVE",
    "tattoo_shop_enterprise_las_vegas": "MERGE_301",
    "tattoo_shop_green_valley_henderson": "MERGE_301",
    "tattoo_shop_serving_henderson_nevada": "KEEP_IMPROVE",
    "tattoo_shop_serving_north_las_vegas": "MERGE_301",
    "tattoo_shop_near_las_vegas_convention_center": "MERGE_301",
    "tattoo_shop_near_mandalay_bay_las_vegas": "MERGE_301",
    "tattoo_shop_near_t_mobile_arena_las_vegas": "MERGE_301",
    "tattoo_shop_near_fashion_show_las_vegas": "MERGE_301",
    "tattoo_shop_near_fremont_street_las_vegas": "MERGE_301",
}

GEO_PAGE_REDIRECTS: dict[str, str] = {
    "tattoo_shop_serving_summerlin_las_vegas": "/tattoo_shop_spring_valley_las_vegas/",
    "tattoo_shop_serving_downtown_las_vegas": "/tattoo_shop_near_the_strip_nap_corrected/",
    "tattoo_piercing_shop_near_unlv": "/tattoo_shop_paradise_nevada/",
    "tattoo_shop_enterprise_las_vegas": "/tattoo_shop_near_the_strip_nap_corrected/",
    "tattoo_shop_green_valley_henderson": "/tattoo_shop_serving_henderson_nevada/",
    "tattoo_shop_serving_north_las_vegas": "/tattoo_shop_near_the_strip_nap_corrected/",
    "tattoo_shop_near_las_vegas_convention_center": "/tattoo_shop_near_the_sphere_las_vegas/",
    "tattoo_shop_near_mandalay_bay_las_vegas": "/tattoo_shop_near_allegiant_stadium_las_vegas/",
    "tattoo_shop_near_t_mobile_arena_las_vegas": "/tattoo_shop_near_mgm_grand_las_vegas/",
    "tattoo_shop_near_fashion_show_las_vegas": "/tattoo_shop_near_the_sphere_las_vegas/",
    "tattoo_shop_near_fremont_street_las_vegas": "/tattoo_shop_near_the_strip_nap_corrected/",
}

INDEXABLE_GEO_ACTIONS = frozenset({"KEEP", "KEEP_IMPROVE"})


def indexable_geo_pages() -> tuple[GeoPage, ...]:
    return tuple(
        page
        for page in GEO_PAGES
        if GEO_PAGE_ACTIONS.get(page.slug, "KEEP_IMPROVE") in INDEXABLE_GEO_ACTIONS
    )


def geo_by_slug(slug: str) -> GeoPage | None:
    for page in GEO_PAGES:
        if page.slug == slug:
            return page
    return None
