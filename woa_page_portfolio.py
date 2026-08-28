#!/usr/bin/env python3
"""Topic-specific portfolio images and SEO alt text for guide pages."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioImage:
    stem: str
    subject: str
    artist: str = "Joshua Cole"
    folder: str = "home_work_of_art_tattoo_piercing/client-portfolio"


REALISM: tuple[PortfolioImage, ...] = (
    PortfolioImage("black-grey-lion-thigh-realism-las-vegas", "Black and grey lion thigh realism"),
    PortfolioImage("black-grey-medusa-snakehair-realism-las-vegas", "Black and grey Medusa portrait realism"),
    PortfolioImage("black-grey-statue-bust-cloth-drape-las-vegas", "Black and grey statue bust with cloth drape"),
    PortfolioImage("roaring-lion-tiger-forearm-realism-las-vegas", "Roaring lion and tiger forearm realism"),
    PortfolioImage("black-grey-all-seeing-eye-realism-las-vegas", "Black and grey all-seeing eye realism"),
    PortfolioImage("woman-skull-skeletal-hand-forearm-realism-las-vegas", "Woman skull and skeletal hand forearm realism"),
)

PIERCING: tuple[PortfolioImage, ...] = (
    PortfolioImage(
        "triple-flat-conch-lobe-ear-setup-f28e160a",
        "Curated helix, conch, and lobe piercing setup",
        "Katelyn Cole",
        "studio_gallery",
    ),
    PortfolioImage(
        "curated-helix-tragus-lobe-piercings-88475d3e",
        "Helix, tragus, and lobe piercing curation",
        "Katelyn Cole",
        "studio_gallery",
    ),
    PortfolioImage(
        "fresh-upper-cartilage-industrial-bar-2e41fc98",
        "Fresh cartilage industrial bar piercing",
        "Katelyn Cole",
        "studio_gallery",
    ),
    PortfolioImage(
        "septum-piercing-session-in-studio-07aad378",
        "Septum piercing session in studio",
        "Katelyn Cole",
        "studio_gallery",
    ),
    PortfolioImage(
        "curated-facial-piercing-jewelry-display-7d759759",
        "Facial piercing jewelry curation display",
        "Katelyn Cole",
        "studio_gallery",
    ),
    PortfolioImage(
        "nostril-stud-on-smiling-client-dd626b1d",
        "Nostril stud piercing on smiling client",
        "Katelyn Cole",
        "studio_gallery",
    ),
)

HEALING: tuple[PortfolioImage, ...] = (
    PortfolioImage("skull-hourglass-forearm-realism-fresh-las-vegas", "Fresh skull and hourglass forearm realism"),
    PortfolioImage("steampunk-clock-gears-rose-forearm-healed-las-vegas", "Healed steampunk clock and rose forearm"),
    PortfolioImage("black-grey-lion-thigh-realism-las-vegas", "Healed black and grey lion thigh realism"),
    PortfolioImage(
        "cover-up-tattoo-phoenix-hand-las-vegas-after",
        "Healed phoenix hand cover-up tattoo",
        folder="cover_up_tattoos_las_vegas_master_authority_guide",
    ),
)

COVER_UP: tuple[PortfolioImage, ...] = (
    PortfolioImage(
        "cover-up-tattoo-phoenix-hand-las-vegas-after",
        "Healed phoenix hand and forearm cover-up",
        folder="cover_up_tattoos_las_vegas_master_authority_guide",
    ),
    PortfolioImage("color-parrot-cover-up-forearm-las-vegas", "Color parrot cover-up forearm tattoo"),
    PortfolioImage("color-character-cover-up-over-geometric-las-vegas", "Character cover-up over geometric tattoo"),
    PortfolioImage("black-grey-lion-thigh-realism-las-vegas", "Black and grey realism redesign piece"),
)

FINE_LINE: tuple[PortfolioImage, ...] = (
    PortfolioImage(
        "fine-line-howling-werewolf-ankle-7ea2af20",
        "Fine-line howling werewolf ankle tattoo",
        folder="studio_gallery",
    ),
    PortfolioImage(
        "mushroom-ghost-blossom-foot-tattoos-13b96e0d",
        "Fine-line mushroom and ghost foot tattoos",
        folder="studio_gallery",
    ),
    PortfolioImage(
        "beauty-script-roses-inner-forearm-195a396a",
        "Beauty script with roses inner forearm tattoo",
        folder="studio_gallery",
    ),
    PortfolioImage("black-grey-portrait-script-text-lower-arm-las-vegas", "Black and grey portrait with script text"),
)

GENERAL: tuple[PortfolioImage, ...] = REALISM[1:5] + HEALING[:2]


def topic_for_slug(slug: str) -> str:
    s = slug.lower()
    if "piercing" in s or "ear_piercing" in s:
        return "piercing"
    if "healing" in s or "aftercare" in s or "before_after" in s:
        return "healing"
    if "cover_up" in s or "cover-up" in s:
        return "cover_up"
    if "realism" in s:
        return "realism"
    if "fine_line" in s or "fine-line" in s:
        return "fine_line"
    return "general"


def pool_for_topic(topic: str) -> tuple[PortfolioImage, ...]:
    return {
        "piercing": PIERCING,
        "healing": HEALING,
        "cover_up": COVER_UP,
        "realism": REALISM,
        "fine_line": FINE_LINE,
    }.get(topic, GENERAL)


def pick_images(slug: str, count: int = 4) -> list[PortfolioImage]:
    pool = pool_for_topic(topic_for_slug(slug))
    if not pool:
        return []
    start = abs(hash(slug)) % len(pool)
    out: list[PortfolioImage] = []
    for i in range(min(count, len(pool))):
        out.append(pool[(start + i) % len(pool)])
    return out


def seo_alt(img: PortfolioImage, page_label: str = "") -> str:
    base = f"{img.subject} — {img.artist}, Work of Art Las Vegas"
    if page_label and page_label.lower() not in base.lower():
        return f"{img.subject} — {page_label}, {img.artist}, Work of Art Las Vegas"
    return base


def image_paths(img: PortfolioImage) -> tuple[str, str]:
    webp = f"/{img.folder}/{img.stem}.webp"
    png = f"/{img.folder}/{img.stem}.png"
    if img.folder.startswith("cover"):
        png = webp
    return webp, png


def picture_tag(img: PortfolioImage, page_label: str = "", eager: bool = False) -> str:
    webp, png = image_paths(img)
    alt = seo_alt(img, page_label).replace('"', "&quot;")
    loading = "eager" if eager else "lazy"
    return (
        f'<picture><source srcset="{webp}" type="image/webp"/>'
        f'<img alt="{alt}" class="w-full h-full object-cover object-center" decoding="async" '
        f'height="800" loading="{loading}" src="{png}" width="800"/></picture>'
    )


def curated_tile(img: PortfolioImage, page_label: str = "", href: str = "/studio_gallery/") -> str:
    cap = img.subject.split("—")[0].strip()[:48]
    return (
        f'<a class="woa-curated-tile group" href="{href}">'
        f'{picture_tag(img, page_label)}'
        f"<span>{cap}</span></a>"
    )
