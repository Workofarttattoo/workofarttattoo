#!/usr/bin/env python3
"""Build flash_art_deals_under_100/code.html — palm-size flash under $100."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from woa_nav_config import STUDIO_ADDRESS_SINGLE_LINE

ROOT = Path(__file__).resolve().parent
ASSETS = Path("/Users/noone/.cursor/projects/Users-noone-Downloads-GitHub-workofarttattoo/assets")
SLUG = "flash_art_deals_under_100"
OUT_DIR = ROOT / SLUG
OUT = OUT_DIR / "code.html"
CANON = f"https://www.workofarttattoo.com/{SLUG}/"
TEMPLATE = ROOT / "tattoo_healing_before_after_real_results" / "code.html"
WALK_IN = ROOT / "walk_in_tattoos_las_vegas_authority_guide" / "code.html"

TITLE = "Flash Tattoo Deals Under $100 | Palm-Size | Work of Art Las Vegas"
DESCRIPTION = (
    "Palm-size flash tattoos under $100 at Work of Art Las Vegas — pick a design, "
    "under one hour, walk-in friendly when slots are open. Fine line, floral, and blackwork flash sheets."
)
OG_STEM = "flash-fine-line-symbolic-sheet"
OG_IMG = f"{CANON}{OG_STEM}.webp"

# (asset filename suffix fragment, output stem, title, description)
FLASH_SHEETS: list[tuple[str, str, str, str]] = [
    (
        "659AB1DF-E1EE-44BA-9329-50BFA43C64B6",
        "flash-fine-line-symbolic-sheet",
        "Fine line · symbolic",
        "Rose, moon, hands, candle, and geometric mini flash — clean linework for first tattoos and small placements.",
    ),
    (
        "E67DDAA9-D646-41F6-B0FC-7F7BC1B3AE28",
        "flash-traditional-blackwork-sheet",
        "Traditional blackwork mini flash",
        "Skull, lion, compass, dagger & rose, wolf, bear, and ace of spades — bold silhouettes sized for palm placements.",
    ),
    (
        "2081DC55-F354-4178-A537-3CBB668B25EE",
        "flash-mystical-nature-4-sheet",
        "Mystical nature · 4 designs",
        "Moon & roses, wolf portrait, crystal cluster, and potion bottle — illustrative black and grey flash.",
    ),
    (
        "6857A6B0-1226-4F41-81C6-F44E0E58810B",
        "flash-dagger-skull-rose-sheet",
        "Dagger · skull · rose set",
        "Nine classic dagger-and-skull compositions with roses — pick one motif for a quick session.",
    ),
    (
        "7945073D-68D2-4C04-A4D1-E9B73296B8C4",
        "flash-gothic-nature-sheet",
        "Gothic nature flash",
        "Ladybug, spider web, spectacles, skull & roses, magnifying glass — detailed but palm-scale.",
    ),
    (
        "95AEFAA3-4877-4818-A46B-0FBA11FFC40F",
        "flash-floral-classic-4-sheet",
        "Classic floral · 4 designs",
        "Lilies, skull & roses, crescent moon floral, and wildflower vase — feminine fine-line options.",
    ),
    (
        "350E170E-FE3C-4F85-B11C-D779FBF94452",
        "flash-floral-duo-sheet",
        "Floral duo",
        "Peony cluster and classic rose — two standalone palm pieces on one sheet.",
    ),
    (
        "61D5E754-BC70-40EF-AAEF-5A0F14F3C4A5",
        "flash-insect-crystal-sheet",
        "Insects & crystals",
        "Beetles, praying mantis, crescent moon, and quartz — mystical nature flash.",
    ),
    (
        "927E2780-1519-4D7B-81EF-7C3573D16C1D",
        "flash-animal-geometric-sheet",
        "Animals & geometry",
        "Skull & feather, framed lion, owl on moon, celestial triangles, howling wolf, double feathers.",
    ),
    (
        "17BEF5D1-83C5-428B-9990-66CD132F614D",
        "flash-botanical-celestial-sheet",
        "Botanical & celestial",
        "Rose, peony, daisy, moon & roses, lily, sunflower, and vase bouquet — floral flash row.",
    ),
    (
        "34626C14-3AC9-43A6-8352-49AE1C728FCA",
        "flash-potion-bottles-sheet",
        "Potion bottles · witchy",
        "Four potion flask designs with candles, crystals, and spellbook accents.",
    ),
    (
        "AF683B2E-C4EF-4B58-83CF-1D693AD797A4",
        "flash-wine-lovers-sheet",
        "Wine lovers flash",
        "Bottle, glass, grapes, cheese, and basket still-life mini designs.",
    ),
    (
        "87FA191F-A018-45D6-A8C7-6A752C8E1CA9",
        "flash-skull-insect-sheet",
        "Skull & insect grid",
        "Nine skull designs with beetles, bees, moths, roses, and daggers.",
    ),
    (
        "C759FE19-921D-4D49-BCAA-2AF63ECE2524",
        "flash-feather-charms-sheet",
        "Feather & charm flash",
        "Four feather designs with moon, star, and bead dangle details.",
    ),
    (
        "5E180922-873A-4D26-9FBF-7D925B67DB7C",
        "flash-mantis-mystical-sheet",
        "Mystical mantis set",
        "Four praying mantis scenes — crystal ball, wizard hat, tarot, and potion bottle.",
    ),
    (
        "CC347721-2986-4758-AFE5-0423995BE6FB",
        "flash-color-potion-sheet",
        "Color potion flash",
        "Four small color potion bottles — pink, gold, blue, and purple with floral accents.",
    ),
]


def find_asset(fragment: str) -> Path | None:
    if not ASSETS.is_dir():
        return None
    for path in ASSETS.glob(f"*{fragment}*.png"):
        return path
    return None


def copy_assets() -> list[tuple[str, str, str, str]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    copied: list[tuple[str, str, str, str]] = []
    for fragment, stem, title, blurb in FLASH_SHEETS:
        src = find_asset(fragment)
        if not src:
            print(f"[warn] missing asset {fragment}")
            continue
        dst = OUT_DIR / f"{stem}.png"
        shutil.copy2(src, dst)
        webp = OUT_DIR / f"{stem}.webp"
        if shutil.which("cwebp"):
            subprocess.run(
                ["cwebp", "-q", "85", str(dst), "-o", str(webp)],
                check=False,
                capture_output=True,
            )
        copied.append((stem, title, blurb, fragment))
        print(f"[asset] {stem}")
    return copied


def gallery_card(stem: str, title: str, blurb: str) -> str:
    webp = f"/{SLUG}/{stem}.webp"
    png = f"/{SLUG}/{stem}.png"
    return f"""
<article class="border border-outline-variant/40 bg-surface overflow-hidden hover:border-secondary/60 transition-colors">
<picture>
<source srcset="{webp}" type="image/webp"/>
<img alt="{title} — palm-size flash tattoo under $100, Work of Art Las Vegas" class="w-full h-auto bg-surface-container-low" decoding="async" loading="lazy" src="{png}"/>
</picture>
<div class="p-5 space-y-2">
<h3 class="font-headline-md text-[18px] text-on-surface">{title}</h3>
<p class="font-body-md text-on-surface-variant text-sm">{blurb}</p>
<p class="font-label-caps text-[10px] text-secondary uppercase tracking-widest">Palm size · under 1 hr · from $100</p>
</div>
</article>"""


def build_main(sheets: list[tuple[str, str, str, str]]) -> str:
    cards = "".join(gallery_card(stem, title, blurb) for stem, title, blurb, _ in sheets)
    hero_img = f"/{SLUG}/{sheets[0][0]}.webp" if sheets else ""
    hero_png = f"/{SLUG}/{sheets[0][0]}.png" if sheets else ""
    return f"""
<main class="relative pt-20">
<section class="relative min-h-[60vh] flex items-end px-6 md:px-margin-desktop pb-16 overflow-hidden">
<div class="absolute inset-0 z-0">
<picture>
<source srcset="{hero_img}" type="image/webp"/>
<img alt="Flash tattoo designs under $100 — Work of Art Las Vegas" class="w-full h-full object-cover opacity-40" decoding="async" loading="eager" src="{hero_png}"/>
</picture>
<div class="absolute inset-0 bg-gradient-to-t from-background via-background/70 to-transparent"></div>
</div>
<div class="relative z-10 max-w-4xl">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em] mb-4 block">Walk-in friendly · quick sessions</span>
<h1 class="font-headline-xl text-[40px] md:text-headline-xl text-on-surface mb-6 leading-tight">Flash art deals under $100</h1>
<p class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">Pick a design from our current flash sheets — palm-size only, finished in under an hour. Perfect for first tattoos, gap fillers, and vacation ink without Strip-booth regret.</p>
<div class="flex flex-col sm:flex-row gap-4 mt-8">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest hover:glow-sm transition-all text-center" href="/appointments/">Book flash slot</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all text-center" href="/walk_in_tattoos_las_vegas_authority_guide/">Walk-in info</a>
</div>
</div>
</section>

<section class="py-12 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-3 gap-8 text-center">
<div class="space-y-2"><span class="material-symbols-outlined text-secondary text-3xl">back_hand</span><p class="font-headline-md text-on-surface">Palm size max</p><p class="font-body-md text-on-surface-variant text-sm">Designs stay roughly palm-sized — no sleeves, no large coverage on this menu.</p></div>
<div class="space-y-2"><span class="material-symbols-outlined text-secondary text-3xl">schedule</span><p class="font-headline-md text-on-surface">Under one hour</p><p class="font-body-md text-on-surface-variant text-sm">Each pick is scoped for a single quick session so you are in and out with quality work.</p></div>
<div class="space-y-2"><span class="material-symbols-outlined text-secondary text-3xl">payments</span><p class="font-headline-md text-on-surface">From $100</p><p class="font-body-md text-on-surface-variant text-sm">Flash pricing starts at $100 before tax/tip. Color or extra detail may adjust slightly at check-in.</p></div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background" id="flash-gallery">
<div class="max-w-6xl mx-auto space-y-10">
<div class="max-w-3xl space-y-4">
<h2 class="font-headline-lg text-on-surface">Current flash sheets</h2>
<p class="font-body-md text-on-surface-variant">Tap a sheet, choose one design, and tell us at booking or walk-in. Teralyn is a strong fit for fineline floral flash, script, detailed small pieces, and custom drawings by commission; artists may simplify fine detail to keep flash palm-sized and under an hour.</p>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">{cards}</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low">
<div class="max-w-3xl mx-auto space-y-8">
<h2 class="font-headline-lg text-on-surface">How flash works here</h2>
<ol class="space-y-6 font-body-md text-on-surface-variant list-decimal pl-5">
<li><strong class="text-on-surface">Pick a design</strong> from the sheets above — screenshot the one you want.</li>
<li><strong class="text-on-surface">Book or walk in</strong> when we have flash slots. <a class="text-secondary underline" href="/walk_in_tattoos_las_vegas_authority_guide/">Walk-in guide</a> · <a class="text-secondary underline" href="/appointments/">Appointments</a></li>
<li><strong class="text-on-surface">Confirm size &amp; placement</strong> with the artist — palm-scale only on this deal menu.</li>
<li><strong class="text-on-surface">Healed aftercare</strong> — follow our <a class="text-secondary underline" href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/">desert climate guide</a> so small work stays crisp.</li>
</ol>
<div class="bg-surface border-l-4 border-secondary p-6">
<p class="font-body-md text-on-surface-variant"><strong class="text-on-surface">Not on this menu:</strong> custom portraits, cover-ups, large color pieces, or anything that needs multiple sessions. Those start with a full consult — see <a class="text-secondary underline" href="/how_much_do_tattoos_cost_in_las_vegas_authority_guide/">pricing guide</a>.</p>
</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background" id="faq">
<div class="max-w-3xl mx-auto space-y-6">
<h2 class="font-headline-lg text-on-surface mb-4">Flash FAQ</h2>
<details class="group bg-surface border border-outline-variant/30 p-6 cursor-pointer hover:border-secondary transition-all"><summary class="flex justify-between items-center font-headline-md list-none">Are flash tattoos really under $100?<span class="material-symbols-outlined group-open:rotate-180 transition-transform">expand_more</span></summary><p class="mt-4 font-body-md text-on-surface-variant">Flash on this page starts at $100 for palm-size designs from these sheets. Tax and tip are separate. If you want a slightly larger placement, the artist will quote before the needle goes in.</p></details>
<details class="group bg-surface border border-outline-variant/30 p-6 cursor-pointer hover:border-secondary transition-all"><summary class="flex justify-between items-center font-headline-md list-none">Can I change the design or add color?<span class="material-symbols-outlined group-open:rotate-180 transition-transform">expand_more</span></summary><p class="mt-4 font-body-md text-on-surface-variant">Minor tweaks are fine if they still fit palm size and one hour. Heavy customization moves you off flash pricing into a custom quote.</p></details>
<details class="group bg-surface border border-outline-variant/30 p-6 cursor-pointer hover:border-secondary transition-all"><summary class="flex justify-between items-center font-headline-md list-none">Do you take walk-ins for flash?<span class="material-symbols-outlined group-open:rotate-180 transition-transform">expand_more</span></summary><p class="mt-4 font-body-md text-on-surface-variant">Yes when flash slots are open — call <a class="text-secondary underline" href="tel:+17252241240">(725) 224-1240</a> or book online to hold a time. Walk-ins are first-come when the schedule allows.</p></details>
<details class="group bg-surface border border-outline-variant/30 p-6 cursor-pointer hover:border-secondary transition-all"><summary class="flex justify-between items-center font-headline-md list-none">Where is the studio?<span class="material-symbols-outlined group-open:rotate-180 transition-transform">expand_more</span></summary><p class="mt-4 font-body-md text-on-surface-variant">Work of Art Tattoo &amp; Piercing — {STUDIO_ADDRESS_SINGLE_LINE}. <a class="text-secondary underline" href="/tattoo-shop-near-las-vegas-strip/">Directions &amp; hours</a></p></details>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low text-center">
<div class="max-w-2xl mx-auto space-y-6">
<h2 class="font-headline-lg text-on-surface">Ready to pick flash?</h2>
<p class="font-body-md text-on-surface-variant">Screenshot your design and book a palm-size slot — in and out in under an hour.</p>
<a class="inline-flex bg-secondary text-on-secondary px-12 py-4 font-label-caps text-label-caps tracking-widest hover:glow-sm transition-all" href="/appointments/">Book flash tattoo</a>
</div>
</section>
</main>
"""


def patch_meta(html: str) -> str:
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
    for prop in ("og:url", "og:title", "og:description", "og:image"):
        if prop == "og:url":
            val = CANON
        elif prop == "og:title":
            val = TITLE
        elif prop == "og:description":
            val = DESCRIPTION
        else:
            val = OG_IMG
        html = re.sub(
            rf'<meta content="[^"]*" property="{prop}"/>',
            f'<meta content="{val}" property="{prop}"/>',
            html,
            count=1,
        )
    for name in ("twitter:title", "twitter:description", "twitter:image"):
        if name == "twitter:title":
            val = TITLE
        elif name == "twitter:description":
            val = DESCRIPTION
        else:
            val = OG_IMG
        html = re.sub(
            rf'<meta content="[^"]*" name="{name}"/>',
            f'<meta content="{val}" name="{name}"/>',
            html,
            count=1,
        )
    return html


def patch_guide_hub(html: str) -> str:
    pill = f'<a aria-current="page" class="woa-guide-pill is-current" href="/{SLUG}/">Flash Under $100</a>'
    anchor = 'href="/walk_in_tattoos_las_vegas_authority_guide/">Walk-In Tattoos in Las Vegas</a>'
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


def link_walk_in_guide() -> None:
    if not WALK_IN.is_file():
        return
    raw = WALK_IN.read_text(encoding="utf-8")
    if f"/{SLUG}/" in raw:
        return
    needle = "Quality work should not always mean a six-month wait."
    if needle not in raw:
        return
    insert = (
        f' Looking for something quick and affordable? See our '
        f'<a class="text-secondary underline" href="/{SLUG}/">flash deals under $100</a> — palm-size, under an hour.'
    )
    WALK_IN.write_text(raw.replace(needle, needle + insert, 1), encoding="utf-8")
    print(f"[ok] linked from {WALK_IN.relative_to(ROOT)}")


def main() -> int:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    sheets = copy_assets()
    if not sheets:
        raise SystemExit("No flash assets copied — check assets folder")
    html = TEMPLATE.read_text(encoding="utf-8")
    html = patch_meta(html)
    html = patch_guide_hub(html)
    html = patch_main(html, build_main(sheets))
    OUT.write_text(html, encoding="utf-8")
    print(f"[ok] {OUT.relative_to(ROOT)} ({len(sheets)} sheets)")
    link_walk_in_guide()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
