#!/usr/bin/env python3
"""Build offsite_bookings/code.html — private event & VIP house-call portfolio."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from woa_offsite_media_manifest import OFFSITE_EVENTS, OffsiteMediaItem, offsite_manifest_items

ROOT = Path(__file__).resolve().parent
ASSETS = Path("/Users/noone/.cursor/projects/Users-noone-Downloads-GitHub-workofarttattoo/assets")
SLUG = "offsite_bookings"
OUT_DIR = ROOT / SLUG
OUT = OUT_DIR / "code.html"
CANON = f"https://www.workofarttattoo.com/{SLUG}/"
TEMPLATE = ROOT / "tattoo_healing_before_after_real_results" / "code.html"
HERO_PREFIX = "CE767869"

TITLE = "Offsite Tattoo Bookings | Private Events | Work of Art Las Vegas"
DESCRIPTION = (
    "Joshua Cole mobile tattoo studio for VIP private events and house calls in Las Vegas — "
    "documented offsite bookings including Party at Mike Tyson's House."
)


def find_asset(uuid_prefix: str) -> Path | None:
    if not ASSETS.is_dir():
        return None
    matches = sorted(ASSETS.glob(f"{uuid_prefix}*.png"))
    return matches[0] if matches else None


def copy_assets(items: list[OffsiteMediaItem]) -> list[OffsiteMediaItem]:
    copied: list[OffsiteMediaItem] = []
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


def gallery_cell(item: OffsiteMediaItem) -> str:
    return f"""<figure class="overflow-hidden border border-outline-variant/30 hover:border-secondary/50 transition-colors bg-surface">
{picture(item.stem, item.alt)}
<figcaption class="p-3 font-body-md text-on-surface-variant text-sm">{item.title}</figcaption>
</figure>"""


def event_section(event_slug: str, heading: str, blurb: str, items: list[OffsiteMediaItem]) -> str:
    if not items:
        return ""
    cells = "".join(gallery_cell(i) for i in items)
    return f"""
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background scroll-mt-24" id="{event_slug}">
<div class="max-w-6xl mx-auto space-y-8">
<div class="max-w-3xl space-y-3">
<h2 class="font-headline-lg text-on-surface">{heading}</h2>
<p class="font-body-md text-on-surface-variant">{blurb}</p>
</div>
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">{cells}</div>
</div>
</section>"""


def build_main(items: list[OffsiteMediaItem], hero: OffsiteMediaItem | None) -> str:
    hero_stem = hero.stem if hero else ""
    hero_alt = hero.alt if hero else "Offsite tattoo booking Work of Art Las Vegas"
    by_event: dict[str, list[OffsiteMediaItem]] = {}
    for item in items:
        by_event.setdefault(item.event_slug, []).append(item)
    sections = "".join(
        event_section(ev.slug, ev.heading, ev.blurb, by_event.get(ev.slug, []))
        for ev in OFFSITE_EVENTS
    )
    event_nav = "".join(
        f'<a class="border border-outline-variant/40 px-4 py-2 font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary hover:text-secondary transition-colors" href="#{ev.slug}">{ev.heading}</a>'
        for ev in OFFSITE_EVENTS
        if by_event.get(ev.slug)
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
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em] mb-4 block">VIP · private events · house calls</span>
<h1 class="font-headline-xl text-[40px] md:text-headline-xl text-on-surface mb-6 leading-tight">Offsite bookings</h1>
<p class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">Joshua Cole travels with a full mobile studio — sterile setup, professional lighting, flash sheets, and custom work for private parties, celebrity residences, and corporate events across Las Vegas.</p>
<div class="flex flex-wrap gap-3 mt-8">{event_nav}</div>
</div>
</section>

<section class="py-10 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-5xl mx-auto space-y-4 text-center">
<p class="font-body-md text-on-surface-variant">Same artist quality as our Tropicana studio — brought to your venue. Minimum booking requirements apply for travel and setup.</p>
<p class="font-body-md text-on-surface-variant text-sm"><a class="text-secondary underline" href="/artists/joshua-cole/">Joshua Cole</a> · <a class="text-secondary underline" href="/studio_gallery/">Studio gallery</a> · <a class="text-secondary underline" href="/appointments/">Book a consult</a></p>
</div>
</section>
{sections}
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low text-center">
<div class="max-w-2xl mx-auto space-y-6">
<h2 class="font-headline-lg text-on-surface">Book an offsite event</h2>
<p class="font-body-md text-on-surface-variant">Private parties, brand activations, and VIP house calls — tell us your date, guest count, and whether you need flash-only or custom work.</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest hover:glow-sm transition-all" href="/appointments/">Request offsite quote</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all" href="/studio_gallery/">Studio portfolio</a>
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
        r'<link href="https://www.workofarttattoo.com/[^"]*" rel="canonical"/>',
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
    pill = f'<a class="woa-guide-pill" href="/{SLUG}/">Offsite Bookings</a>'
    anchor = 'href="/studio_gallery/">Studio Gallery</a>'
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
    items = offsite_manifest_items()
    copied = copy_assets(items)
    if not copied:
        raise SystemExit("No offsite booking assets copied")
    hero = next((i for i in copied if i.uuid_prefix == HERO_PREFIX), copied[0])
    html = TEMPLATE.read_text(encoding="utf-8")
    html = patch_meta(html, hero.stem)
    html = patch_guide_hub(html)
    html = patch_main(html, build_main(copied, hero))
    OUT.write_text(html, encoding="utf-8")
    print(f"[ok] {OUT.relative_to(ROOT)} — {len(copied)} images")
    for ev in OFFSITE_EVENTS:
        count = sum(1 for i in copied if i.event_slug == ev.slug)
        print(f"  {ev.slug}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
