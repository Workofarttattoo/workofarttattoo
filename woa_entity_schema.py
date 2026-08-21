#!/usr/bin/env python3
"""Sitewide entity graph (WebSite, LocalBusiness, Person, Service, FAQ, Video, Image) for JSON-LD."""

from __future__ import annotations

import json
import re
from pathlib import Path

from woa_nav_config import (
    HREF_FACEBOOK_STUDIO,
    HREF_INSTAGRAM_JOSHUA,
    HREF_INSTAGRAM_STUDIO,
    HREF_INSTAGRAM_TERALYN,
    RESIDENT_ARTIST_COUNT,
    STUDIO_ADDRESS_LOCALITY,
    STUDIO_ADDRESS_REGION,
    STUDIO_BOOKING_EMAIL,
    STUDIO_LEGAL_NAME,
    STUDIO_PHONE_SCHEMA,
    STUDIO_POSTAL_CODE,
    STUDIO_STREET_ADDRESS,
)

SITE = "https://workofarttattoo.com"
ID_WEBSITE = f"{SITE}/#website"
ID_BUSINESS = f"{SITE}/#localbusiness"
ID_JOSHUA = f"{SITE}/#person-joshua-cole"
ID_KATELYN = f"{SITE}/#person-katelyn-cole"
ID_TERALYN = f"{SITE}/#person-teralyn"
IMAGE_LICENSE_URL = f"{SITE}/image-license/"
IMAGE_CREDIT_TEXT = "Work of Art Tattoo & Piercing"
IMAGE_COPYRIGHT_NOTICE = "Copyright Work of Art Tattoo & Piercing. All rights reserved."

FAQ_DETAILS_RE = re.compile(
    r"<details[^>]*>.*?<summary[^>]*>(?P<q>.*?)</summary>.*?<p[^>]*>(?P<a>.*?)</p>.*?</details>",
    re.DOTALL | re.IGNORECASE,
)
STRIP_TAGS_RE = re.compile(r"<[^>]+>")

SERVICE_BY_SLUG: dict[str, tuple[str, str]] = {
    "realism_tattoos_las_vegas_master_authority_guide": (
        "Black and Grey Realism Tattoo",
        "Custom black-and-grey realism tattoos — portraits, wildlife, and sleeves at Work of Art Las Vegas.",
    ),
    "cover_up_tattoos_las_vegas_master_authority_guide": (
        "Tattoo Cover-Up",
        "Cover-up consults and multi-session redesigns for old or faded tattoos in Las Vegas.",
    ),
    "fine_line_tattoos_las_vegas_master_authority_guide": (
        "Fine Line Tattoo",
        "Fine line and micro-detail tattoo work with longevity-focused planning.",
    ),
    "best_fine_line_tattoos_in_vegas_ultimate_authority_guide": (
        "Fine Line Tattoo",
        "Fine line tattoo selection and healed clarity guidance in Las Vegas.",
    ),
    "best_piercing_shop_las_vegas_updated_jewelry_standards": (
        "Body Piercing",
        "Medical-grade body piercing and ear curation with implant-grade jewelry.",
    ),
    "piercing_types_las_vegas_authority_hub": (
        "Complete Piercing Guide",
        "Placement-by-placement piercing guides with pain, healing, jewelry, and desert aftercare.",
    ),
    "ear_piercing_guide_las_vegas": (
        "Ear Piercing Guide",
        "Helix, conch, tragus, daith, industrial, and curated ear placement guides.",
    ),
    "facial_piercing_guide_las_vegas": (
        "Facial Piercing Guide",
        "Nostril, septum, bridge, and eyebrow piercing placement guides.",
    ),
    "oral_piercing_guide_las_vegas": (
        "Oral Piercing Guide",
        "Tongue, labret, philtrum, and lip piercing guides with downsizing timelines.",
    ),
    "body_piercing_guide_las_vegas": (
        "Body Piercing Guide",
        "Navel and nipple piercing guides with anatomy-first consults.",
    ),
    "piercing_aftercare_guide_las_vegas": (
        "Piercing Aftercare Guide",
        "Cleaning, sleeping, swimming, and gym with a fresh piercing in Las Vegas.",
    ),
    "piercing_jewelry_guide_las_vegas": (
        "Piercing Jewelry Guide",
        "Implant-grade titanium, threadless jewelry, and downsizing standards.",
    ),
    "piercing_healing_guide_las_vegas": (
        "Piercing Healing Guide",
        "Healing times by placement — honest timelines from master piercer Katelyn Cole.",
    ),
    "katelyn_cole_piercing_authority_hub_las_vegas": (
        "Katelyn Cole Piercing Authority",
        "Expert topics on titanium, ear curation, anatomy, downsizing, and piercing safety.",
    ),
    "piercing_aftercare_desert_climate_las_vegas_expert_guide": (
        "Desert Piercing Aftercare",
        "Vegas-specific piercing healing — pools, heat, dust, and saline routines.",
    ),
    "real_client_tattoo_timeline_las_vegas": (
        "Real Client Tattoo Timeline",
        "One documented tattoo from fresh to one year — Joshua Cole black & grey realism in Las Vegas.",
    ),
    "walk_in_tattoos_las_vegas_authority_guide": (
        "Walk-In Tattoo",
        "Same-day tattoo and piercing availability when the schedule allows.",
    ),
    "flash_art_deals_under_100": (
        "Flash Tattoo",
        "Palm-size flash art from studio sheets — under $100 and under one hour.",
    ),
    "studio_gallery": (
        "Studio Portfolio",
        "Documented tattoos, original art, and piercing work from Work of Art Las Vegas artists.",
    ),
    "offsite_bookings": (
        "Offsite Tattoo Booking",
        "Mobile tattoo studio for private VIP events and house calls in Las Vegas.",
    ),
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": (
        "Tattoo Aftercare Consultation",
        "Desert-climate aftercare education for Las Vegas collectors.",
    ),
    "skin_science_tattoo_dermatology_authority_guide": (
        "Skin Science for Tattoo Collectors",
        "How skin layers, immune cells, and collagen hold ink — plus conditions that change tattoo planning.",
    ),
    "epidermis_skin_science_las_vegas_authority_guide": (
        "Epidermis & Tattoo Healing",
        "Outer skin layer turnover, peeling, and why surface ink does not stay.",
    ),
    "dermis_skin_science_las_vegas_authority_guide": (
        "Dermis — Where Ink Lives",
        "Needle depth, collagen matrix, and why the dermis holds pigment for life.",
    ),
    "hypodermis_skin_science_las_vegas_authority_guide": (
        "Hypodermis & Blowouts",
        "Fat layer anatomy and why ink in subcutaneous tissue blurs.",
    ),
    "why_tattoos_stay_forever_skin_science_las_vegas_authority_guide": (
        "Why Tattoos Stay Forever",
        "Particle size, dermal trapping, and what still fades over decades.",
    ),
    "macrophages_skin_science_las_vegas_authority_guide": (
        "Macrophages & Tattoo Ink",
        "Immune cells that engulf pigment and lock color in the dermis.",
    ),
    "collagen_skin_science_las_vegas_authority_guide": (
        "Collagen & Tattoos",
        "Dermal scaffold, healing, and how structure affects line clarity.",
    ),
    "scar_tissue_tattoo_skin_science_las_vegas_authority_guide": (
        "Scar Tissue & Tattoos",
        "Why scars tattoo differently — timing, technique, and cover-ups.",
    ),
    "stretch_marks_skin_science_las_vegas_authority_guide": (
        "Stretch Marks & Tattoos",
        "Striae anatomy, pregnancy timing, and design strategies.",
    ),
    "eczema_skin_science_las_vegas_authority_guide": (
        "Eczema & Tattoos",
        "Barrier flares, Koebner risk, and when to wait — consult your dermatologist.",
    ),
    "psoriasis_skin_science_las_vegas_authority_guide": (
        "Psoriasis & Tattoos",
        "Koebner phenomenon, biologics, and dermatologist clearance.",
    ),
    "diabetes_skin_science_las_vegas_authority_guide": (
        "Diabetes & Tattoo Healing",
        "Blood sugar, neuropathy, and studio requirements for safe healing.",
    ),
    "aging_skin_skin_science_las_vegas_authority_guide": (
        "Aging Skin & Tattoos",
        "Collagen loss, sun damage, and design choices that age well.",
    ),
    "tattoo_healing_before_after_real_results": (
        "Tattoo Healing Education",
        "Fresh vs healed tattoo documentation — what lightening means and normal healing timelines.",
    ),
    "healed_tattoo_gallery_las_vegas": (
        "Healed Tattoo Portfolio",
        "Documented fresh and healed work by style — proof of long-term craftsmanship.",
    ),
    "healing_database_tattoo_timeline_encyclopedia_las_vegas": (
        "Tattoo Healing Education",
        "Stage-by-stage healing encyclopedia — day 1 through year 1 by tattoo style with Las Vegas desert notes.",
    ),
    "joshua_oil_painting_black_grey_tattoo_aging_las_vegas": (
        "Artist Education",
        "How classical oil painting training informs black and grey tattoo design for aging.",
    ),
}

JOSHUA_PAGE = f"{SITE}/artists/joshua-cole/"
KATELYN_PAGE = f"{SITE}/artists/katelyn-cole/"
TERALYN_PAGE = f"{SITE}/artists/teralyn/"
JOSHUA_IMAGE = f"{SITE}/artists/joshua-cole/joshua-cole-tattooing-portrait-las-vegas.webp"
KATELYN_IMAGE = (
    f"{SITE}/artists/katelyn-cole/"
    "katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas.webp"
)
TERALYN_IMAGE = f"{SITE}/artists/teralyn/teralyn-fine-line-tattoo-artist-las-vegas.webp"

JOSHUA_KNOWS_ABOUT = (
    "Black and grey realism tattoo",
    "Portrait tattoo",
    "Hyperrealism",
    "Color realism tattoo",
    "Color realistic imagery",
    "Blackwork tattoo",
    "Sleeve tattoo",
    "Cover-up tattoo",
    "Las Vegas tattoo artist",
    "Custom tattoo design",
)

KATELYN_KNOWS_ABOUT = (
    "Body piercing",
    "Ear curation",
    "Implant-grade titanium jewelry",
    "316L surgical steel jewelry",
    "APP piercing standards",
    "Las Vegas piercing",
)

TERALYN_KNOWS_ABOUT = (
    "Fine line tattoo",
    "Award-winning fine line floral tattoo",
    "Floral fine line tattoo",
    "Small script tattoo",
    "Fine line script tattoo",
    "High-detail small tattoo",
    "Custom tattoo drawings by commission",
    "Commissioned custom tattoo drawings",
    "Walk-in tattoo",
    "Flash tattoo",
    "Las Vegas tattoo artist",
    "Female piercing team",
)


def _opening_hours() -> list[dict]:
    return [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"],
            "opens": "12:00",
            "closes": "00:00",
        },
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Friday", "Saturday", "Sunday"],
            "opens": "12:00",
            "closes": "00:00",
        },
    ]


def _postal_address() -> dict:
    return {
        "@type": "PostalAddress",
        "streetAddress": STUDIO_STREET_ADDRESS,
        "addressLocality": STUDIO_ADDRESS_LOCALITY,
        "addressRegion": STUDIO_ADDRESS_REGION,
        "postalCode": STUDIO_POSTAL_CODE,
        "addressCountry": "US",
    }


def _strip_html(text: str) -> str:
    return re.sub(r"\s+", " ", STRIP_TAGS_RE.sub("", text)).strip()


def extract_faqs_from_html(html: str, *, limit: int = 8) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []
    for match in FAQ_DETAILS_RE.finditer(html):
        q = _strip_html(match.group("q"))
        a = _strip_html(match.group("a"))
        if len(q) < 8 or len(a) < 20:
            continue
        faqs.append((q, a))
        if len(faqs) >= limit:
            break
    return faqs


def service_node(*, slug: str, name: str, description: str) -> dict:
    page_url = f"{SITE}/{slug}/"
    return {
        "@type": "Service",
        "@id": f"{page_url}#service",
        "name": name,
        "description": description,
        "url": page_url,
        "provider": {"@id": ID_BUSINESS},
        "areaServed": {"@type": "City", "name": "Las Vegas"},
    }


def image_object(*, url: str, caption: str, creator_id: str | None = None) -> dict:
    node: dict = {
        "@type": "ImageObject",
        "contentUrl": url,
        "description": caption,
        "license": IMAGE_LICENSE_URL,
        "acquireLicensePage": IMAGE_LICENSE_URL,
        "creditText": IMAGE_CREDIT_TEXT,
        "copyrightNotice": IMAGE_COPYRIGHT_NOTICE,
    }
    if creator_id:
        node["creator"] = {"@id": creator_id}
    return node


def load_studio_videos(root: Path) -> list[dict]:
    # Instagram links are kept visible, but they are not first-party playable
    # video files. Do not emit VideoObject unless a crawlable video host/source is added.
    return []


def person_joshua() -> dict:
    return {
        "@type": "Person",
        "@id": ID_JOSHUA,
        "name": "Joshua Cole",
        "url": JOSHUA_PAGE,
        "image": JOSHUA_IMAGE,
        "jobTitle": "Studio Lead — Tattoo & Piercing Artist",
        "description": (
            "Joshua Cole leads Work of Art Tattoo & Piercing in Las Vegas with black & grey "
            "realism, portrait work, sleeves, and cover-ups. He trains resident artists and "
            "offers piercing consults in-studio."
        ),
        "knowsAbout": list(JOSHUA_KNOWS_ABOUT),
        "sameAs": [HREF_INSTAGRAM_JOSHUA, HREF_FACEBOOK_STUDIO],
        "worksFor": {"@id": ID_BUSINESS},
    }


def person_katelyn() -> dict:
    return {
        "@type": "Person",
        "@id": ID_KATELYN,
        "name": "Katelyn Cole",
        "url": KATELYN_PAGE,
        "image": KATELYN_IMAGE,
        "jobTitle": "Master Body Piercer",
        "description": (
            "Katelyn Cole is Work of Art's master piercer in Las Vegas — ear curation, "
            "implant-grade titanium and surgical steel jewelry, and APP-aligned sterile technique."
        ),
        "knowsAbout": list(KATELYN_KNOWS_ABOUT),
        "sameAs": [HREF_INSTAGRAM_STUDIO, HREF_FACEBOOK_STUDIO],
        "worksFor": {"@id": ID_BUSINESS},
    }


def person_teralyn() -> dict:
    return {
        "@type": "Person",
        "@id": ID_TERALYN,
        "name": "Teralyn",
        "url": TERALYN_PAGE,
        "image": TERALYN_IMAGE,
        "jobTitle": "Fine Line Tattoo Artist",
        "description": (
            "Teralyn graduated from Work of Art's piercing apprenticeship and grew into a "
            "tattoo artist focused on award-winning fine line floral work, fine line, "
            "small script, commissioned custom drawings, high-detail smaller tattoos, "
            "walk-in requests, and flash designs. "
            "She is also part of the female piercing team with Katelyn Cole."
        ),
        "knowsAbout": list(TERALYN_KNOWS_ABOUT),
        "sameAs": [HREF_INSTAGRAM_TERALYN],
        "worksFor": {"@id": ID_BUSINESS},
    }


def local_business_node() -> dict:
    return {
        "@type": ["LocalBusiness", "TattooParlor"],
        "@id": ID_BUSINESS,
        "name": STUDIO_LEGAL_NAME,
        "alternateName": "Work of Art",
        "url": f"{SITE}/",
        "telephone": STUDIO_PHONE_SCHEMA,
        "email": STUDIO_BOOKING_EMAIL,
        "image": f"{SITE}/home_work_of_art_tattoo_piercing/work-of-art-studio-banner-las-vegas.webp",
        "logo": f"{SITE}/logo.png",
        "priceRange": "$$",
        "address": _postal_address(),
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 36.1008,
            "longitude": -115.1189,
        },
        "openingHoursSpecification": _opening_hours(),
        "sameAs": [
            HREF_INSTAGRAM_STUDIO,
            HREF_FACEBOOK_STUDIO,
            HREF_INSTAGRAM_JOSHUA,
            HREF_INSTAGRAM_TERALYN,
        ],
        "numberOfEmployees": RESIDENT_ARTIST_COUNT,
        "employee": [{"@id": ID_JOSHUA}, {"@id": ID_KATELYN}, {"@id": ID_TERALYN}],
        "areaServed": [
            {"@type": "City", "name": "Las Vegas"},
            {"@type": "Place", "name": "Paradise, Nevada"},
            {"@type": "Place", "name": "Clark County, Nevada"},
        ],
    }


def website_node() -> dict:
    return {
        "@type": "WebSite",
        "@id": ID_WEBSITE,
        "url": f"{SITE}/",
        "name": STUDIO_LEGAL_NAME,
        "publisher": {"@id": ID_BUSINESS},
        "inLanguage": "en-US",
    }


def sitewide_graph() -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            website_node(),
            local_business_node(),
            person_joshua(),
            person_katelyn(),
            person_teralyn(),
        ],
    }


def artist_profile_graph(artist: str, *, root: Path | None = None) -> dict:
    if artist == "joshua":
        person = person_joshua()
        page_url = JOSHUA_PAGE
        page_name = "Joshua Cole — Realism Tattoo Artist Las Vegas"
    elif artist == "katelyn":
        person = person_katelyn()
        page_url = KATELYN_PAGE
        page_name = "Katelyn Cole — Master Piercer Las Vegas"
    else:
        person = person_teralyn()
        page_url = TERALYN_PAGE
        page_name = "Teralyn — Fine Line Tattoo Artist Las Vegas"
    graph: list[dict] = [
        website_node(),
        local_business_node(),
        person,
        {
            "@type": "ProfilePage",
            "@id": f"{page_url}#webpage",
            "url": page_url,
            "name": page_name,
            "mainEntity": {"@id": person["@id"]},
            "isPartOf": {"@id": ID_WEBSITE},
            "about": {"@id": person["@id"]},
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{page_url}#breadcrumb",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": f"{SITE}/",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Artists",
                    "item": f"{SITE}/artists/",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": person["name"],
                    "item": page_url,
                },
            ],
        },
    ]
    if artist == "joshua":
        graph.append(
            image_object(
                url=f"{SITE}/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-thigh-realism-las-vegas.webp",
                caption="Joshua Cole — black and grey lion thigh realism portfolio",
                creator_id=ID_JOSHUA,
            )
        )
        graph.append(
            service_node(
                slug="realism_tattoos_las_vegas_master_authority_guide",
                name="Black and Grey Realism Tattoo",
                description="Custom realism tattoos by Joshua Cole at Work of Art Las Vegas.",
            )
        )
    elif artist == "katelyn":
        graph.append(
            service_node(
                slug="best_piercing_shop_las_vegas_updated_jewelry_standards",
                name="Body Piercing",
                description="Ear curation and medical-grade piercing by Katelyn Cole.",
            )
        )
    else:
        graph.append(
            service_node(
                slug="best_fine_line_tattoos_in_vegas_ultimate_authority_guide",
                name="Fine Line Tattoo",
                description="Fine line, floral fine line, small script, commissioned custom drawings, walk-in, and flash tattoos by Teralyn.",
            )
        )
    if root:
        graph.extend(load_studio_videos(root)[:2])
    return {
        "@context": "https://schema.org",
        "@graph": graph,
    }


def artists_index_graph() -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            website_node(),
            local_business_node(),
            person_joshua(),
            person_katelyn(),
            person_teralyn(),
            {
                "@type": "CollectionPage",
                "@id": f"{SITE}/artists/#webpage",
                "url": f"{SITE}/artists/",
                "name": "Artists at Work of Art Tattoo Las Vegas",
                "isPartOf": {"@id": ID_WEBSITE},
                "about": {"@id": ID_BUSINESS},
                "mainEntity": {
                    "@type": "ItemList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "item": {"@id": ID_JOSHUA},
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "item": {"@id": ID_KATELYN},
                        },
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "item": {"@id": ID_TERALYN},
                        },
                    ],
                },
            },
        ],
    }


def guide_article_graph(
    *,
    slug: str,
    title: str,
    description: str,
    author_id: str | None = None,
    faqs: list[tuple[str, str]] | None = None,
    root: Path | None = None,
) -> dict:
    page_url = f"{SITE}/{slug}/"
    article_about: list[dict] = [{"@id": ID_BUSINESS}]
    graph: list[dict] = [
        website_node(),
        local_business_node(),
        person_joshua(),
        person_katelyn(),
    ]
    if slug in SERVICE_BY_SLUG:
        svc_name, svc_desc = SERVICE_BY_SLUG[slug]
        svc = service_node(slug=slug, name=svc_name, description=svc_desc)
        graph.append(svc)
        article_about.append({"@id": svc["@id"]})

    graph.extend(
        [
            {
                "@type": "Article",
                "@id": f"{page_url}#article",
                "headline": title,
                "description": description,
                "url": page_url,
                "mainEntityOfPage": f"{page_url}#webpage",
                "author": {"@id": author_id or ID_JOSHUA},
                "publisher": {"@id": ID_BUSINESS},
                "isPartOf": {"@id": ID_WEBSITE},
                "about": article_about if len(article_about) > 1 else article_about[0],
                "inLanguage": "en-US",
            },
            {
                "@type": "WebPage",
                "@id": f"{page_url}#webpage",
                "url": page_url,
                "name": title,
                "description": description,
                "isPartOf": {"@id": ID_WEBSITE},
                "about": {"@id": ID_BUSINESS},
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{page_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{SITE}/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": title,
                        "item": page_url,
                    },
                ],
            },
        ]
    )

    if slug == "realism_tattoos_las_vegas_master_authority_guide":
        graph.append(
            image_object(
                url=f"{SITE}/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-thigh-realism-las-vegas.webp",
                caption="Black and grey lion thigh realism — Work of Art Las Vegas portfolio",
                creator_id=ID_JOSHUA,
            )
        )

    if slug == "tattoo_healing_before_after_real_results":
        graph.append(
            image_object(
                url=f"{SITE}/tattoo_healing_before_after_real_results/eagle-memorial-calf-fresh-vs-healed-comparison-las-vegas.webp",
                caption="Color memorial eagle tattoos — fresh vs healed comparison, Work of Art Las Vegas",
                creator_id=ID_JOSHUA,
            )
        )

    if slug == "flash_art_deals_under_100":
        graph.append(
            image_object(
                url=f"{SITE}/flash_art_deals_under_100/flash-fine-line-symbolic-sheet.webp",
                caption="Palm-size flash tattoo sheet — deals under $100, Work of Art Las Vegas",
                creator_id=ID_JOSHUA,
            )
        )

    if slug == "studio_gallery":
        graph.append(
            image_object(
                url=f"{SITE}/studio_gallery/fantasy-portrait-with-lightning-b9702cf5.webp",
                caption="Joshua Cole tattoo portfolio — Work of Art Las Vegas studio gallery",
                creator_id=ID_JOSHUA,
            )
        )
        graph.append(
            image_object(
                url=f"{SITE}/studio_gallery/norse-full-sleeve-narrative-1bc3cc09.webp",
                caption="Norse full sleeve tattoo by Joshua Cole — Work of Art Las Vegas",
                creator_id=ID_JOSHUA,
            )
        )
        graph.append(
            image_object(
                url=f"{SITE}/studio_gallery/grim-reaper-with-lantern-07f7a393.webp",
                caption="Custom tattoo design available to book — Joshua Cole, Work of Art Las Vegas",
                creator_id=ID_JOSHUA,
            )
        )
        graph.append(
            image_object(
                url=f"{SITE}/studio_gallery/ear-lobe-piercing-session-da19eec5.webp",
                caption="Katelyn Cole piercing portfolio — Work of Art Las Vegas",
                creator_id=ID_KATELYN,
            )
        )

    if slug == "offsite_bookings":
        graph.append(
            image_object(
                url=f"{SITE}/offsite_bookings/vip-party-overview-ce767869.webp",
                caption="Offsite tattoo booking at private VIP event — Joshua Cole, Work of Art Las Vegas",
                creator_id=ID_JOSHUA,
            )
        )
        graph.append(
            image_object(
                url=f"{SITE}/offsite_bookings/mobile-studio-banner-setup-0d9b5525.webp",
                caption="Mobile tattoo studio setup — Work of Art Las Vegas offsite booking",
                creator_id=ID_JOSHUA,
            )
        )

    if faqs:
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{page_url}#faq",
                "url": page_url,
                "name": title,
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in faqs
                ],
            }
        )

    if root and slug == "studio_videos":
        graph.extend(load_studio_videos(root))

    return {"@context": "https://schema.org", "@graph": graph}


def faq_page_graph(*, slug: str, title: str, faqs: list[tuple[str, str]]) -> dict:
    page_url = f"{SITE}/{slug}/"
    return {
        "@context": "https://schema.org",
        "@graph": [
            website_node(),
            local_business_node(),
            {
                "@type": "FAQPage",
                "@id": f"{page_url}#faq",
                "url": page_url,
                "name": title,
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in faqs
                ],
            },
            {
                "@type": "WebPage",
                "@id": f"{page_url}#webpage",
                "url": page_url,
                "name": title,
                "isPartOf": {"@id": ID_WEBSITE},
            },
        ],
    }


def schema_script(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{payload}\n</script>'


def page_slug_from_path(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root)
    if rel.parts[0] == "artists_build":
        return None
    if rel.name == "code.html":
        if len(rel.parts) == 1:
            return None
        return rel.parts[0]
    return None
