#!/usr/bin/env python3
"""Build studio_gallery/code.html — Joshua tattoos & art, Katelyn piercing, studio life."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from woa_studio_media_manifest import (
    MediaCategory,
    MediaItem,
    manifest_items,
)

ROOT = Path(__file__).resolve().parent
ASSETS = Path("/Users/noone/.cursor/projects/Users-noone-Downloads-GitHub-workofarttattoo/assets")
SLUG = "studio_gallery"
OUT_DIR = ROOT / SLUG
OUT = OUT_DIR / "code.html"
CANON = f"https://workofarttattoo.com/{SLUG}/"
TEMPLATE = ROOT / "tattoo_healing_before_after_real_results" / "code.html"

TITLE = "Studio Gallery | Tattoos, Original Art & Piercing | Work of Art Las Vegas"
DESCRIPTION = (
    "Real tattoo portfolio, original fine art, and piercing work from Work of Art Las Vegas — "
    "Joshua Cole tattoos & paintings, Katelyn Cole ear curation and body piercing."
)

SECTIONS: list[tuple[MediaCategory, str, str, str]] = [
    (
        MediaCategory.JOSHUA_TATTOO,
        "Joshua Cole · Tattoos",
        "Black & grey realism, portraits, and custom illustrative work from the studio lead.",
        "joshua-tattoos",
    ),
    (
        MediaCategory.JOSHUA_TATTOOING,
        "Joshua Cole · Tattooing",
        "Joshua at the machine — real in-studio sessions only, not stock or portrait shots.",
        "joshua-tattooing",
    ),
    (
        MediaCategory.JOSHUA_ART,
        "Joshua Cole · Original art",
        "Paintings and illustrations behind the tattoo designs — fine art before the needle.",
        "joshua-art",
    ),
    (
        MediaCategory.JOSHUA_DESIGNS,
        "Joshua Cole · Designs to book",
        "Original concepts and inspired pieces Joshua wants to tattoo — screenshot the one you want and book a custom session.",
        "joshua-designs",
    ),
    (
        MediaCategory.KATELYN_PIERCING,
        "Katelyn Cole · Piercing",
        "Ear curation, facial piercing, and implant-grade jewelry — documented in studio.",
        "katelyn-piercing",
    ),
    (
        MediaCategory.STUDIO_LIFE,
        "In the studio",
        "Our workspace, storefront, and studio life — no artist portraits mixed in here.",
        "studio-life",
    ),
]


def find_asset(uuid_prefix: str) -> Path | None:
    if not ASSETS.is_dir():
        return None
    matches = sorted(ASSETS.glob(f"{uuid_prefix}*.png"))
    return matches[0] if matches else None


def copy_assets(items: list[MediaItem]) -> list[MediaItem]:
    copied: list[MediaItem] = []
    for item in items:
        src = find_asset(item.uuid_prefix)
        if not src:
            print(f"[warn] missing {item.uuid_prefix} ({item.title})")
            continue
        dst = OUT_DIR / f"{item.stem}.png"
        shutil.copy2(src, dst)
        webp = OUT_DIR / f"{item.stem}.webp"
        if shutil.which("cwebp"):
            subprocess.run(
                ["cwebp", "-q", "85", str(dst), "-o", str(webp)],
                check=False,
                capture_output=True,
            )
        copied.append(item)
    return copied


def picture(stem: str, alt: str, eager: bool = False) -> str:
    loading = "eager" if eager else "lazy"
    return f"""<picture>
<source srcset="/{SLUG}/{stem}.webp" type="image/webp"/>
<img alt="{alt}" class="w-full h-full object-cover object-center aspect-[3/4] bg-surface-container-low" decoding="async" loading="{loading}" src="/{SLUG}/{stem}.png"/>
</picture>"""


def gallery_cell(item: MediaItem) -> str:
    return f"""<figure class="overflow-hidden border border-outline-variant/30 hover:border-secondary/50 transition-colors bg-surface">
{picture(item.stem, item.alt)}
<figcaption class="p-3 font-body-md text-on-surface-variant text-sm">{item.title}</figcaption>
</figure>"""


def section_block(cat: MediaCategory, heading: str, blurb: str, anchor: str, items: list[MediaItem]) -> str:
    if not items:
        return ""
    cells = "".join(gallery_cell(i) for i in items)
    return f"""
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background scroll-mt-24" id="{anchor}">
<div class="max-w-6xl mx-auto space-y-8">
<div class="max-w-3xl space-y-3">
<h2 class="font-headline-lg text-on-surface">{heading}</h2>
<p class="font-body-md text-on-surface-variant">{blurb}</p>
</div>
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">{cells}</div>
</div>
</section>"""


def build_main(buckets: dict[MediaCategory, list[MediaItem]], hero: MediaItem | None) -> str:
    hero_stem = hero.stem if hero else ""
    hero_alt = hero.alt if hero else "Work of Art Tattoo studio gallery Las Vegas"
    sections = "".join(
        section_block(cat, heading, blurb, anchor, buckets.get(cat, []))
        for cat, heading, blurb, anchor in SECTIONS
    )
    nav_pills = "".join(
        f'<a class="border border-outline-variant/40 px-4 py-2 font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary hover:text-secondary transition-colors" href="#{anchor}">{heading}</a>'
        for cat, heading, _blurb, anchor in SECTIONS
        if buckets.get(cat)
    )
    return f"""
<main class="relative pt-20">
<section class="relative min-h-[55vh] flex items-end px-6 md:px-margin-desktop pb-16 overflow-hidden">
<div class="absolute inset-0 z-0">
<picture>
<source srcset="/{SLUG}/{hero_stem}.webp" type="image/webp"/>
<img alt="{hero_alt}" class="w-full h-full object-cover opacity-35" decoding="async" loading="eager" src="/{SLUG}/{hero_stem}.png"/>
</picture>
<div class="absolute inset-0 bg-gradient-to-t from-background via-background/75 to-transparent"></div>
</div>
<div class="relative z-10 max-w-4xl">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em] mb-4 block">Original work · real clients</span>
<h1 class="font-headline-xl text-[40px] md:text-headline-xl text-on-surface mb-6 leading-tight">Studio gallery</h1>
<p class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">Completed tattoos, original paintings, designs waiting for the right client, and piercing work shot in our Las Vegas studio — not stock photos. Joshua Cole on custom ink and fine art; Katelyn Cole on ear curation and body piercing.</p>
<div class="flex flex-wrap gap-3 mt-8">{nav_pills}</div>
</div>
</section>

<section class="py-10 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-2 gap-6 text-center">
<div class="space-y-2"><a class="text-secondary underline font-headline-md" href="/artists/joshua-cole/">Joshua Cole</a><p class="font-body-md text-on-surface-variant text-sm">Tattoos &amp; original art · <a class="text-secondary underline" href="/realism_tattoos_las_vegas_master_authority_guide/">realism guide</a></p></div>
<div class="space-y-2"><a class="text-secondary underline font-headline-md" href="/artists/katelyn-cole/">Katelyn Cole</a><p class="font-body-md text-on-surface-variant text-sm">Piercing &amp; ear curation · <a class="text-secondary underline" href="/best_piercing_shop_las_vegas_updated_jewelry_standards/">piercing standards</a></p></div>
</div>
</section>
{sections}
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low text-center">
<div class="max-w-2xl mx-auto space-y-6">
<h2 class="font-headline-lg text-on-surface">Book with the artist you saw</h2>
<p class="font-body-md text-on-surface-variant">Custom tattoos start with a consult. Piercing appointments include placement planning and aftercare for desert heat.</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest hover:glow-sm transition-all" href="/appointments/">Book appointment</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all" href="/flash_art_deals_under_100/">Flash under $100</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all" href="#joshua-designs">Designs to book</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all" href="/offsite_bookings/">Offsite bookings</a>
</div>
</div>
</section>
</main>
"""


def patch_meta(html: str, hero_stem: str) -> str:
    og_img = f"{CANON}{hero_stem}.webp"
    html = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", html, count=1)
    html = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{DESCRIPTION}" name="description"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<link href="https://workofarttattoo.com/[^"]*" rel="canonical"/>',
        f'<link href="{CANON}" rel="canonical"/>',
        html,
        count=1,
    )
    for prop, val in (
        ("og:url", CANON),
        ("og:title", TITLE),
        ("og:description", DESCRIPTION),
        ("og:image", og_img),
    ):
        html = re.sub(
            rf'<meta content="[^"]*" property="{prop}"/>',
            f'<meta content="{val}" property="{prop}"/>',
            html,
            count=1,
        )
    for name, val in (
        ("twitter:title", TITLE),
        ("twitter:description", DESCRIPTION),
        ("twitter:image", og_img),
    ):
        html = re.sub(
            rf'<meta content="[^"]*" name="{name}"/>',
            f'<meta content="{val}" name="{name}"/>',
            html,
            count=1,
        )
    return html


def patch_guide_hub(html: str) -> str:
    pill = f'<a class="woa-guide-pill" href="/{SLUG}/">Studio Gallery</a>'
    anchor = 'href="/realism_tattoos_las_vegas_master_authority_guide/">Realism Tattoos in Las Vegas</a>'
    if f'href="/{SLUG}/"' in html:
        return html
    return html.replace(anchor, anchor + pill, 1)


def patch_main(html: str, main: str) -> str:
    html = re.sub(
        r'<script data-woa-entity-schema="1" type="application/ld\\+json">.*?</script>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<main class="relative pt-20">.*?</main>',
        main.strip(),
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<nav[^>]*data-woa-topic-cluster="1"[^>]*>.*?</nav>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    return html


def main() -> int:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    items = manifest_items()
    copied = copy_assets(items)
    if not copied:
        raise SystemExit("No studio gallery assets copied")
    buckets: dict[MediaCategory, list[MediaItem]] = {c: [] for c in MediaCategory if c.value != "skip"}
    for item in copied:
        buckets[item.category].append(item)
    hero = next((i for i in copied if i.uuid_prefix == "B9702CF5"), copied[0])
    html = TEMPLATE.read_text(encoding="utf-8")
    html = patch_meta(html, hero.stem)
    html = patch_guide_hub(html)
    html = patch_main(html, build_main(buckets, hero))
    OUT.write_text(html, encoding="utf-8")
    print(f"[ok] {OUT.relative_to(ROOT)} — {len(copied)} images")
    for cat, _h, _b, _a in SECTIONS:
        print(f"  {cat.value}: {len(buckets.get(cat, []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
