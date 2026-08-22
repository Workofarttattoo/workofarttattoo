#!/usr/bin/env python3
"""Curate homepage portfolio, artist portraits, showcase grid, and optional banner hero."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
CODE = HOME / "code.html"
ROOT_CODE = ROOT / "code.html"
CLIENT = HOME / "client-portfolio"
HERO_PREMIUM = HOME / "hero-premium"
COVER = ROOT / "cover_up_tattoos_las_vegas_master_authority_guide"

_ASSETS_DIRS = (
    ROOT / "assets",
    Path("/Users/noone/.cursor/projects/Users-noone-Downloads-GitHub-workofarttattoo/assets"),
)


def _find_asset(name_fragment: str) -> Path | None:
    for d in _ASSETS_DIRS:
        if not d.is_dir():
            continue
        for p in sorted(d.glob(f"*{name_fragment}*")):
            if p.suffix.lower() in {".png", ".jpg", ".webp"}:
                return p
    return None

CARD_W, CARD_H = 800, 1067
BANNER_STEM = "work-of-art-studio-banner-las-vegas"
STATUE_BUST_STEM = "black-grey-statue-bust-cloth-drape-las-vegas"
STATUE_BUST_SOURCE = ROOT / "img_2291.jpeg" / "tattoo-portfolio-las-vegas-2291.png"
STATUE_BUST_CROP = (600, 700, 1000, 1200)

from import_landing_portfolio_images import (  # noqa: E402
    CURATED_STEMS,
    SHOWCASE_STEMS,
    import_all as import_landing_images,
    landing_items,
)

PORTFOLIO_EXCLUDE_STEMS = frozenset(
    {
        "woman-skull-skeletal-hand-forearm-realism-las-vegas",
        "hero-woman-skull-skeletal-hand-forearm-realism",
        "cover-up-tattoo-sunflower-over-black-ink-las-vegas",
        "healed-color-sunflower-cover-up-leg-las-vegas",
        "black-grey-sunflower-neck-shoulder-tattoo-las-vegas",
        "color-parrot-cover-up-forearm-las-vegas",
        "color-character-cover-up-over-geometric-las-vegas",
        "color-panther-snake-flames-upper-arm-las-vegas",
        "black-grey-realism-snake-sleeve-tattoo",
        "black-grey-realism-snake-sleeve-tattoo",
        "healed-black-grey-chain-heart-tattoo",
        "cover-up-tattoo-phoenix-hand-las-vegas-after",
        "money-rose-black-grey-realism-upper-arm-las-vegas",
        "las-vegas-tattoo-artist-working-closeup",
    }
)

# Only allow the first curated stem per family (extra safety if list is edited).
_PORTFOLIO_ONCE_FAMILIES: tuple[tuple[str, str], ...] = (
    ("phoenix", "phoenix"),
    ("chain-heart", "chain"),
    ("sunflower", "sunflower"),
)


def _portfolio_family(stem: str) -> str | None:
    low = stem.lower()
    for needle, family in _PORTFOLIO_ONCE_FAMILIES:
        if needle in low:
            return family
    return None



def save_portrait(src: Path, dest_png: Path) -> None:
    dest_png.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as raw:
        im = ImageOps.exif_transpose(raw).convert("RGB")
        w, h = im.size
        target = CARD_W / CARD_H
        cur = w / h
        if cur > target:
            new_w = int(h * target)
            x0 = (w - new_w) // 2
            im = im.crop((x0, 0, x0 + new_w, h))
        else:
            new_h = int(w / target)
            y0 = max(0, (h - new_h) // 3)
            im = im.crop((0, y0, w, min(h, y0 + new_h)))
        im = im.resize((CARD_W, CARD_H), Image.Resampling.LANCZOS)
        im.save(dest_png, "PNG", optimize=True)
        im.save(dest_png.with_suffix(".webp"), "WEBP", quality=84, method=6)
    jpg = dest_png.with_suffix(".jpg")
    if jpg != dest_png:
        with Image.open(dest_png) as im:
            im.save(jpg, "JPEG", quality=88, optimize=True)


def resolve_asset(stem: str) -> tuple[str, str] | None:
    """Return (webp_url, png_url) for a stem searched in known tattoo folders."""
    dirs = (
        CLIENT,
        HERO_PREMIUM,
        HOME,
        COVER,
        ROOT / "reviews_vault_100_verified_masterpieces",
        ROOT / "artists" / "joshua-cole",
        ROOT / "artists" / "katelyn-cole",
        ROOT / "artists" / "teralyn",
    )
    for d in dirs:
        webp = d / f"{stem}.webp"
        png = d / f"{stem}.png"
        jpg = d / f"{stem}.jpg"
        if webp.is_file() and png.is_file():
            rel = d.relative_to(ROOT).as_posix()
            return f"/{rel}/{webp.name}", f"/{rel}/{png.name}"
        if webp.is_file() and jpg.is_file():
            rel = d.relative_to(ROOT).as_posix()
            return f"/{rel}/{webp.name}", f"/{rel}/{jpg.name}"
        if png.is_file():
            rel = d.relative_to(ROOT).as_posix()
            return (f"/{rel}/{webp.name}" if webp.is_file() else "", f"/{rel}/{png.name}")
    return None


def picture_tag(
    webp: str,
    png: str,
    alt: str,
    *,
    lazy: bool = True,
    eager: bool = False,
    img_class: str = "w-full h-full object-cover object-center",
    object_pos: str = "",
) -> str:
    loading = "eager" if eager else "lazy"
    pos = f" object-[{object_pos}]" if object_pos else ""
    cls = f"{img_class}{pos}"
    if webp:
        return (
            f'<picture><source srcset="{webp}" type="image/webp"/>'
            f'<img alt="{alt}" class="{cls}" decoding="async" loading="{loading}" '
            f'src="{png}" width="800" height="800"/></picture>'
        )
    return (
        f'<img alt="{alt}" class="{cls}" decoding="async" loading="{loading}" '
        f'src="{png}" width="800" height="800"/>'
    )


def sync_katelyn_from_user() -> None:
    src = _find_asset("image-709287ce") or _find_asset("katelyn")
    if not src or not src.is_file():
        print("[skip] Katelyn user portrait asset not found")
        return
    dest = (
        ROOT
        / "artists"
        / "katelyn-cole"
        / "katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas.png"
    )
    save_portrait(src, dest)
    print(f"[ok] Katelyn portrait ← {src.name}")


def sync_statue_bust_asset() -> None:
    """Crop veiled statue bust from studio portfolio photo (forearm, img_2291)."""
    if not STATUE_BUST_SOURCE.is_file():
        print("[skip] statue bust source missing")
        return
    dest = CLIENT / f"{STATUE_BUST_STEM}.png"
    with Image.open(STATUE_BUST_SOURCE) as raw:
        im = ImageOps.exif_transpose(raw).convert("RGB")
        crop = im.crop(STATUE_BUST_CROP)
    CARD_W, CARD_H = 800, 1067
    target = CARD_W / CARD_H
    cw, ch = crop.size
    cur = cw / ch
    if cur > target:
        new_w = int(ch * target)
        x0 = cw - new_w
        out = crop.crop((x0, 0, x0 + new_w, ch))
    else:
        new_h = int(cw / target)
        y0 = max(0, (ch - new_h) // 8)
        out = crop.crop((0, y0, cw, min(ch, y0 + new_h)))
    out = out.resize((CARD_W, CARD_H), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, "PNG", optimize=True)
    out.save(dest.with_suffix(".webp"), "WEBP", quality=84, method=6)
    print(f"[ok] statue bust → {dest.relative_to(ROOT)}")


def sync_banner() -> None:
    src = _find_asset("work_of_art_banner") or _find_asset("banner_1600")
    if not src or not src.is_file():
        print("[skip] studio banner asset not found")
        return
    dest = HOME / f"{BANNER_STEM}.png"
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.save(dest, "PNG", optimize=True)
        im.save(dest.with_suffix(".webp"), "WEBP", quality=86, method=6)
    print(f"[ok] banner → {dest.relative_to(ROOT)}")


_SHOWCASE_LABELS = {
    "norse-odin-viking-ship-sleeve-realism-las-vegas": (
        "Norse Odin Sleeve",
        "Black and grey Norse Odin and Viking ship sleeve — Work of Art Tattoo Las Vegas",
    ),
    "black-grey-warrior-profile-shoulder-realism-las-vegas": (
        "Warrior Profile Realism",
        "Black and grey warrior profile shoulder realism — Work of Art Tattoo Las Vegas",
    ),
    "veiled-woman-statue-black-grey-realism-las-vegas": (
        "Veiled Statue Realism",
        "Veiled woman statue black and grey realism — Work of Art Tattoo Las Vegas",
    ),
    "all-seeing-eye-triangle-forearm-realism-las-vegas": (
        "All-Seeing Eye Realism",
        "All-seeing eye triangle forearm realism — Work of Art Tattoo Las Vegas",
    ),
}


def showcase_grid_html() -> str:
    pairs: list[tuple[str, str, str, str]] = []
    for stem in SHOWCASE_STEMS:
        resolved = resolve_asset(stem)
        if not resolved:
            raise SystemExit(f"Missing showcase asset: {stem}")
        title, alt = _SHOWCASE_LABELS.get(stem, (stem, stem))
        pairs.append((resolved[0], resolved[1], title, alt))
    if len(pairs) < 4:
        raise SystemExit("Need 4 showcase tattoo assets")

    hero_w, hero_p, hero_title, hero_alt = pairs[0]
    tiles = pairs[1:]

    side_cells = ""
    for webp, png, title, alt in tiles:
        side_cells += f"""<div class="group relative aspect-square bg-surface-container overflow-hidden" data-category="all black-grey">
{picture_tag(webp, png, alt)}
<div class="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-6">
<span class="font-label-caps text-label-caps text-on-surface uppercase tracking-widest">{title}</span>
</div>
</div>
"""

    return f"""<div class="grid grid-cols-1 md:grid-cols-12 gap-gutter" id="showcase-grid">
<div class="md:col-span-8 group relative aspect-[3/4] md:aspect-[4/5] min-h-[320px] bg-surface-container overflow-hidden" data-category="black-grey">
{picture_tag(hero_w, hero_p, hero_alt, eager=True, img_class="w-full h-full object-cover", object_pos="center_35%")}
<div class="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent opacity-80"></div>
<div class="absolute bottom-0 left-0 p-8 w-full">
<p class="font-label-caps text-label-caps text-secondary uppercase tracking-widest mb-2">Masterpiece</p>
<h3 class="font-headline-md text-headline-md text-on-surface">{hero_title}</h3>
</div>
</div>
<div class="md:col-span-4 space-y-gutter">
{side_cells}
</div>
</div>"""


def artist_cards_html() -> str:
    josh = resolve_asset("joshua-cole-tattooing-portrait-las-vegas")
    kat = resolve_asset("katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas")
    ter = resolve_asset("teralyn-fine-line-tattoo-artist-las-vegas")
    if not (josh and kat and ter):
        raise SystemExit("Missing artist portrait assets")

    jw, jp = josh
    kw, kp = kat
    tw, tp = ter
    kat_src = kp.replace(".png", ".jpg") if "katelyn-cole" in kp else kp

    return f"""<div class="grid grid-cols-1 sm:grid-cols-3 gap-gutter max-w-5xl mx-auto">
<div class="text-center">
<a class="group block" href="/artists/joshua-cole/">
<div class="aspect-[3/4] bg-surface-container mb-4 overflow-hidden relative border border-outline-variant/30">
<picture><source srcset="{jw}" type="image/webp"/><img width="800" height="1067" alt="Joshua Cole — black and grey realism tattoo artist, Work of Art Tattoo Las Vegas" class="w-full h-full object-cover object-top transition-transform duration-500 group-hover:scale-105" decoding="async" loading="lazy" src="{jp}"/></picture>
<div class="absolute inset-0 bg-secondary/20 opacity-0 group-hover:opacity-100 transition-opacity"></div>
</div>
<span class="font-label-caps text-label-caps text-on-surface group-hover:text-secondary transition-colors block">Joshua Cole</span>
<span class="font-body-md text-[13px] text-on-surface-variant block mt-1">Black &amp; Grey Realism</span>
</a>
<a class="font-body-md text-[12px] text-secondary hover:underline block mt-2" href="https://www.instagram.com/workofarttattoo/" rel="noopener noreferrer" target="_blank">@workofarttattoo</a>
</div>
<div class="text-center">
<a class="group block" href="/artists/katelyn-cole/">
<div class="aspect-[3/4] bg-surface-container mb-4 overflow-hidden relative border border-outline-variant/30">
<picture><source srcset="{kw}" type="image/webp"/><img width="800" height="1067" alt="Katelyn Cole — master body piercer, Work of Art Tattoo Las Vegas" class="w-full h-full object-cover object-top transition-transform duration-500 group-hover:scale-105" decoding="async" loading="lazy" src="{kat_src}"/></picture>
<div class="absolute inset-0 bg-secondary/20 opacity-0 group-hover:opacity-100 transition-opacity"></div>
</div>
<span class="font-label-caps text-label-caps text-on-surface group-hover:text-secondary transition-colors block">Katelyn Cole</span>
<span class="font-body-md text-[13px] text-on-surface-variant block mt-1">Master Piercer</span>
</a>
<a class="font-body-md text-[12px] text-secondary hover:underline block mt-2" href="https://www.instagram.com/stabislifee/" rel="noopener noreferrer" target="_blank">@stabislifee</a>
</div>
<div class="text-center">
<a class="group block" href="/artists/teralyn/">
<div class="aspect-[3/4] bg-surface-container mb-4 overflow-hidden relative border border-outline-variant/30">
<picture><source srcset="{tw}" type="image/webp"/><img width="800" height="1067" alt="Teralyn — fine line tattoo artist, Work of Art Tattoo Las Vegas" class="w-full h-full object-cover object-top transition-transform duration-500 group-hover:scale-105" decoding="async" loading="lazy" src="{tp}"/></picture>
<div class="absolute inset-0 bg-secondary/20 opacity-0 group-hover:opacity-100 transition-opacity"></div>
</div>
<span class="font-label-caps text-label-caps text-on-surface group-hover:text-secondary transition-colors block">Teralyn</span>
<span class="font-body-md text-[13px] text-on-surface-variant block mt-1">Fineline Floral · Script · Custom</span>
</a>
<a class="font-body-md text-[12px] text-secondary hover:underline block mt-2" href="https://www.instagram.com/mischiefmodifies/" rel="noopener noreferrer" target="_blank">@mischiefmodifies</a>
</div>
</div>"""


def banner_hero_html() -> str:
    webp = f"/{HOME.name}/{BANNER_STEM}.webp"
    png = f"/{HOME.name}/{BANNER_STEM}.png"
    if not (HOME / f"{BANNER_STEM}.png").is_file():
        return ""
    links = (
        ("Book", "/appointments/"),
        ("Artists", "#gallery"),
        ("Portfolio", "#portfolio"),
        ("Piercing", "#piercing"),
        ("Interview", "#studio-interview"),
        ("Appointments", "/appointments/"),
    )
    nav_links = "\n".join(
        f'<a class="woa-banner-nav-link" href="{href}">{label}</a>' for label, href in links
    )
    return f"""<!-- WOA_HERO_BANNER_START -->
<div class="woa-hero-banner relative w-full overflow-hidden border-b border-outline-variant/20" aria-hidden="false">
<picture>
<source srcset="{webp}" type="image/webp"/>
<img alt="Work of Art Tattoo &amp; Piercing — Las Vegas studio banner" class="woa-hero-banner-img w-full block object-cover object-[center_20%]" decoding="async" fetchpriority="high" loading="eager" src="{png}" width="1600" height="1040"/>
</picture>
<div aria-hidden="true" class="woa-hero-banner-shade"></div>
<nav class="woa-hero-banner-nav" aria-label="Quick links">
{nav_links}
</nav>
</div>
<!-- WOA_HERO_BANNER_END -->"""


def curated_masonry_items() -> list[dict]:
    items = landing_items()
    if items:
        return items

    from expand_homepage_conversion import alt_from_stem, categorize  # noqa: PLC0415

    fallback: list[dict] = []
    seen: set[str] = set()
    families_seen: set[str] = set()
    for stem in CURATED_STEMS:
        if stem in seen or stem in PORTFOLIO_EXCLUDE_STEMS:
            continue
        family = _portfolio_family(stem)
        if family and family in families_seen:
            continue
        pair = resolve_asset(stem)
        if not pair:
            continue
        webp, png = pair
        rel = png.lstrip("/").rsplit("/", 1)[0]
        fallback.append(
            {
                "stem": stem,
                "webp": webp,
                "png": png,
                "cats": categorize(rel, stem),
                "alt": alt_from_stem(stem),
            }
        )
        seen.add(stem)
        if family:
            families_seen.add(family)
    return fallback


def patch_homepage() -> None:
    from expand_homepage_conversion import masonry_section_html  # noqa: PLC0415

    items = curated_masonry_items()
    showcase = showcase_grid_html()
    artists_block = artist_cards_html()
    banner = banner_hero_html()
    masonry = masonry_section_html(items)

    for out_path in (CODE, ROOT_CODE):
        if not out_path.is_file():
            continue
        text = out_path.read_text(encoding="utf-8")

        text = re.sub(
            r'<div class="grid grid-cols-1 md:grid-cols-12 gap-gutter" id="showcase-grid">[\s\S]*?'
            r'</div>\s*(?=<!-- WOA_HOME_MASONRY_START -->)',
            showcase + "\n",
            text,
            count=1,
        )
        text = re.sub(
            r'<div class="grid grid-cols-1 md:grid-cols-12 gap-gutter" id="showcase-grid">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>',
            showcase + "\n</div>\n</div>\n</div>\n</div>",
            text,
            count=1,
            flags=re.DOTALL,
        )

        text = re.sub(
            r'<div class="grid grid-cols-1 sm:grid-cols-[23] gap-gutter max-w-3xl mx-auto">[\s\S]*?'
            r'</div>\s*(?=<div aria-label="Gallery category filter")',
            artists_block + "\n",
            text,
            count=1,
        )

        if banner and "WOA_HERO_BANNER_START" in text:
            if "WOA_HERO_BANNER_END" in text:
                text = re.sub(
                    r"<!-- WOA_HERO_BANNER_START -->.*?<!-- WOA_HERO_BANNER_END -->",
                    banner.strip(),
                    text,
                    count=1,
                    flags=re.DOTALL,
                )
            elif "WOA_HOME_MASONRY_END" in text:
                # Banner marker leaked into masonry — replace merged block.
                text = re.sub(
                    r"<!-- WOA_HERO_BANNER_START -->[\s\S]*?<!-- WOA_HOME_MASONRY_END -->",
                    banner.strip() + "\n" + masonry.strip(),
                    text,
                    count=1,
                )
            else:
                text = re.sub(
                    r"<!-- WOA_HERO_BANNER_START -->[\s\S]*?(?=<!-- Piercing Section -->|<div class=\"flex justify-center pt-8\">)",
                    banner.strip() + "\n",
                    text,
                    count=1,
                )
        elif banner and 'id="hero"' in text:
            text = text.replace(
                '<section class="relative min-h-screen flex flex-col justify-center',
                banner + '\n<section class="relative min-h-screen flex flex-col justify-center',
                1,
            )
        elif banner and "<!-- Hero Section -->" in text:
            text = text.replace("<!-- Hero Section -->", banner + "\n<!-- Hero Section -->", 1)

        if "WOA_HOME_MASONRY_START" in text:
            text = re.sub(
                r"<!-- WOA_HOME_MASONRY_START -->.*?<!-- WOA_HOME_MASONRY_END -->",
                masonry,
                text,
                count=1,
                flags=re.DOTALL,
            )

        # Remove mislabeled snake from featured slot if still present
        text = text.replace(
            'custom-tattoos-las-vegas-epic-snake-black-and-grey-realism',
            'black-grey-lion-realism-thigh-client-photo-las-vegas',
            1,
        )

        out_path.write_text(text, encoding="utf-8")

    print(f"[ok] homepage portfolio: {len(items)} curated masonry tiles")


def main() -> int:
    import_landing_images()
    sync_statue_bust_asset()
    sync_katelyn_from_user()
    sync_banner()
    patch_homepage()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
