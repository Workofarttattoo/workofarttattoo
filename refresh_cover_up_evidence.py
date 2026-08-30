#!/usr/bin/env python3
"""Refresh cover-up pages with Joshua-supplied cover-up/rework evidence."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGE_SLUGS = ("cover-up-tattoos-las-vegas",)
CANONICAL_SLUG = "cover-up-tattoos-las-vegas"
CANON = f"https://www.workofarttattoo.com/{CANONICAL_SLUG}/"
MARKER = 'data-woa-coverup-evidence="2026-08"'

IMAGES = {
    "hero": {
        "slug": "large-scale-arm-rework-praying-hands-rose-las-vegas",
        "width": 1200,
        "height": 1600,
        "alt": "Large-scale arm rework by Joshua Cole at Work of Art Tattoo in Las Vegas",
    },
    "floral": {
        "slug": "floral-tattoo-cover-up-before-after-las-vegas",
        "width": 474,
        "height": 421,
        "alt": "Before and after floral tattoo cover-up by Joshua Cole in Las Vegas",
    },
    "arm_alt": {
        "slug": "large-scale-arm-rework-viking-portrait-alt-view-las-vegas",
        "width": 682,
        "height": 1862,
        "alt": "Alternate view of large-scale arm rework by Joshua Cole",
    },
    "wing": {
        "slug": "dark-pigment-black-grey-wing-eye-rework-las-vegas",
        "width": 1200,
        "height": 1600,
        "alt": "Dark pigment black and grey tattoo rework by Joshua Cole",
    },
    "skull": {
        "slug": "black-grey-skull-crown-rose-rework-las-vegas",
        "width": 1200,
        "height": 1600,
        "alt": "Black and grey skull and rose corrective tattoo work by Joshua Cole",
    },
    "dragon": {
        "slug": "color-dragon-tattoo-redesign-las-vegas",
        "width": 1200,
        "height": 1600,
        "alt": "Color dragon tattoo redesign work by Joshua Cole",
    },
    "neck": {
        "slug": "neck-butterfly-corrective-tattoo-work-las-vegas",
        "width": 1200,
        "height": 1600,
        "alt": "Neck butterfly corrective tattoo work by Joshua Cole",
    },
    "angel": {
        "slug": "angel-money-black-grey-tattoo-redesign-las-vegas",
        "width": 1200,
        "height": 1600,
        "alt": "Black and grey angel and money tattoo redesign by Joshua Cole",
    },
    "butterfly": {
        "slug": "blue-butterfly-color-tattoo-rework-las-vegas",
        "width": 1200,
        "height": 1600,
        "alt": "Blue butterfly color tattoo rework by Joshua Cole",
    },
}

OLD_COVERUP_IMAGE_RE = re.compile(
    r"cover-up-tattoo-phoenix-hand-las-vegas-after|"
    r"cover-up-tattoo-sunflower-over-black-ink-las-vegas|"
    r"cover-up-tattoo-faded-butterflies-hand-before|"
    r"cover-up-tattoo-faded-floral-leg-before|"
    r"healed-realism-seraphim-eye-wings-tattoo|"
    r"healed-black-grey-chain-heart-tattoo|"
    r"black-grey-collarbone-thorns-wreath-tattoo|"
    r"black-grey-realism-snake-sleeve-tattoo",
    re.I,
)


def picture(key: str, cls: str, loading: str = "lazy", sizes: str = "(min-width: 768px) 50vw, 100vw") -> str:
    info = IMAGES[key]
    slug = info["slug"]
    return (
        f'<picture>'
        f'<source srcset="/{CANONICAL_SLUG}/{slug}-800.webp 800w, /{CANONICAL_SLUG}/{slug}.webp {info["width"]}w" '
        f'sizes="{sizes}" type="image/webp"/>'
        f'<source srcset="/{CANONICAL_SLUG}/{slug}-800.jpg 800w, /{CANONICAL_SLUG}/{slug}.jpg {info["width"]}w" '
        f'sizes="{sizes}" type="image/jpeg"/>'
        f'<img alt="{info["alt"]}" class="{cls}" height="{info["height"]}" loading="{loading}" '
        f'src="/{CANONICAL_SLUG}/{slug}.jpg" width="{info["width"]}"/>'
        f'</picture>'
    )


def ensure_assets() -> None:
    missing: list[str] = []
    for folder_slug in PAGE_SLUGS:
        folder = ROOT / folder_slug
        for info in IMAGES.values():
            for ext in ("jpg", "webp"):
                path = folder / f"{info['slug']}.{ext}"
                if not path.is_file():
                    missing.append(str(path.relative_to(ROOT)))
    if missing:
        raise SystemExit("Missing cover-up evidence assets:\n- " + "\n- ".join(missing))


def evidence_sections() -> str:
    gallery = [
        ("wing", "Dark Pigment / Black-and-Grey Rework", "Heavy value areas need a design that controls contrast, not a promise that every old mark can vanish."),
        ("skull", "Black-and-Grey Corrective Work", "Skulls, roses, crowns, and textured shadows can redirect the eye when the old shape is awkward."),
        ("dragon", "Color Redesign", "Color can help when the new design has enough room, edge control, and value separation."),
        ("neck", "Corrective Neck Work", "Visible placements need extra care because line weight, symmetry, and skin movement are unforgiving."),
        ("angel", "Black-and-Grey Tattoo Redesign", "Large compositions work when the new image gives the eye a clear subject and supporting detail."),
        ("butterfly", "Blue Butterfly Rework", "Organic shapes can soften older pigment when the surrounding skin gives the artist room to move."),
    ]
    cards = "\n".join(
        f"""<article class="border border-outline-variant bg-surface overflow-hidden">
<div class="aspect-[4/5] bg-surface-container">{picture(key, "w-full h-full object-cover")}</div>
<div class="p-5 space-y-2">
<h3 class="font-headline-md text-on-surface text-xl">{title}</h3>
<p class="font-body-md text-on-surface-variant text-sm leading-relaxed">{copy}</p>
</div>
</article>"""
        for key, title, copy in gallery
    )

    return f"""
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low" id="studio-portfolio" {MARKER}>
<div class="max-w-5xl mx-auto space-y-12">
<div class="max-w-3xl space-y-4">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">REAL STUDIO PHOTOS</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Real Cover-Ups &amp; Tattoo Reworks by Joshua Cole</h2>
<p class="font-body-lg text-on-surface-variant leading-relaxed">Cover-ups are not about putting something darker on top of an old tattoo. The new design has to use shape, value, movement, texture, and placement to control what the eye sees.</p>
</div>

<article class="grid grid-cols-1 lg:grid-cols-[1.05fr_0.95fr] gap-8 items-center border border-outline-variant bg-surface p-5 md:p-8">
<div class="bg-surface-container">{picture("floral", "w-full h-auto object-contain", sizes="(min-width: 1024px) 45vw, 100vw")}</div>
<div class="space-y-5">
<p class="font-label-caps text-[10px] uppercase tracking-[0.22em] text-secondary">Before / After</p>
<h3 class="font-headline-md text-on-surface text-3xl">Floral Transformation</h3>
<p class="font-body-md text-on-surface-variant leading-relaxed">This is the strongest true before-and-after evidence in the supplied set. The old tattoo is visibly present in the top frame, and the floral design in the lower frame shows how color, leaf shapes, and movement can pull attention away from the original mark.</p>
<p class="font-body-md text-on-surface-variant leading-relaxed">Not every tattoo can use this exact approach. A useful consult photo needs the existing tattoo, surrounding skin, clear lighting, straight-on angle, and rough size.</p>
<div class="flex flex-col sm:flex-row gap-3">
<a class="inline-flex justify-center bg-secondary text-on-secondary px-6 py-3 font-label-caps text-[11px] uppercase tracking-widest" href="/appointments/">Send Joshua a Photo</a>
<a class="inline-flex justify-center border border-outline px-6 py-3 font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary" href="/artists/joshua-cole/">Joshua's portfolio</a>
</div>
</div>
</article>

<article class="border border-outline-variant bg-background p-5 md:p-8">
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
<div class="space-y-4">
<p class="font-label-caps text-[10px] uppercase tracking-[0.22em] text-secondary">Large-scale arm rework</p>
<h3 class="font-headline-md text-on-surface text-3xl">When Going Bigger Makes the Work Cleaner</h3>
<p class="font-body-md text-on-surface-variant leading-relaxed">Large reworks often work better when the artist treats the entire area as one composition instead of trying to hide individual marks one at a time. These two photos are grouped as one arm project so the page does not overstate the number of finished projects.</p>
<p class="font-body-md text-on-surface-variant leading-relaxed">The useful lesson for clients: sometimes a stronger tattoo means expanding the design boundaries, not chasing a tiny patch.</p>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
<figure class="space-y-3">{picture("hero", "w-full h-auto object-cover", sizes="(min-width: 1024px) 24vw, 100vw")}<figcaption class="font-body-md text-on-surface-variant text-sm">Primary view of large arm rework.</figcaption></figure>
<figure class="space-y-3">{picture("arm_alt", "w-full h-auto object-cover", sizes="(min-width: 1024px) 24vw, 100vw")}<figcaption class="font-body-md text-on-surface-variant text-sm">Alternate angle from the same large-scale arm project.</figcaption></figure>
</div>
</div>
</article>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background" id="coverable">
<div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-[0.8fr_1.2fr] gap-10 items-start">
<div class="space-y-4">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">ASSESSMENT</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">What Makes a Tattoo Coverable?</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">A cover-up depends on what is already in the skin and how much room the new design has to work. Photos help, but an in-person consult is still the most accurate way to judge what is realistic.</p>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
<div class="border border-outline-variant bg-surface p-5"><h3 class="font-headline-md text-on-surface text-lg mb-2">Pigment Density</h3><p class="font-body-md text-on-surface-variant text-sm">Packed black and saturated color need stronger planning than faded gray work.</p></div>
<div class="border border-outline-variant bg-surface p-5"><h3 class="font-headline-md text-on-surface text-lg mb-2">Line Weight</h3><p class="font-body-md text-on-surface-variant text-sm">Heavy outlines can limit delicate options, especially script and fine-line designs.</p></div>
<div class="border border-outline-variant bg-surface p-5"><h3 class="font-headline-md text-on-surface text-lg mb-2">Age and Fading</h3><p class="font-body-md text-on-surface-variant text-sm">Older tattoos often give the artist more flexibility than fresh dark work.</p></div>
<div class="border border-outline-variant bg-surface p-5"><h3 class="font-headline-md text-on-surface text-lg mb-2">Surrounding Skin</h3><p class="font-body-md text-on-surface-variant text-sm">Extra room lets the new design move past the old tattoo's boundaries.</p></div>
<div class="border border-outline-variant bg-surface p-5"><h3 class="font-headline-md text-on-surface text-lg mb-2">Subject Matter</h3><p class="font-body-md text-on-surface-variant text-sm">Florals, realism, ornamental shapes, texture, and black-and-grey can work, but not for every old tattoo.</p></div>
<div class="border border-outline-variant bg-surface p-5"><h3 class="font-headline-md text-on-surface text-lg mb-2">Size of New Design</h3><p class="font-body-md text-on-surface-variant text-sm">Going larger can create cleaner flow and better long-term readability.</p></div>
</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-lowest" id="more-rework">
<div class="max-w-5xl mx-auto space-y-10">
<div class="max-w-3xl space-y-4">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">MORE REAL WORK</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">More Cover-Up and Rework Portfolio Examples</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">These are supplied studio examples for the cover-up and rework page. Where the original tattoo is not visible, captions describe the visible strategy without calling it a confirmed cover-up.</p>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
{cards}
</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface" id="coverup-ideas">
<div class="max-w-4xl mx-auto space-y-8">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">DESIGN STRATEGY</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Cover-Up Ideas: What Usually Works?</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">Good cover-up ideas usually create motion and contrast. Florals, organic shapes, black-and-grey realism, ornamental elements, texture, and larger compositions can work because they give the artist ways to hide or redirect older lines. The right answer depends on the existing tattoo.</p>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
<div class="border border-outline-variant bg-background p-5"><h3 class="font-headline-md text-on-surface text-lg">Cover-Up</h3><p class="font-body-md text-on-surface-variant text-sm">A new tattoo is designed to visually control or hide an existing tattoo.</p></div>
<div class="border border-outline-variant bg-background p-5"><h3 class="font-headline-md text-on-surface text-lg">Rework</h3><p class="font-body-md text-on-surface-variant text-sm">The old tattoo remains part of the new design, but structure, contrast, or detail is rebuilt.</p></div>
<div class="border border-outline-variant bg-background p-5"><h3 class="font-headline-md text-on-surface text-lg">Laser Lightening</h3><p class="font-body-md text-on-surface-variant text-sm">Lightening may create more options for dense black ink; ask during consult before assuming it is required.</p></div>
</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background" id="artists">
<div class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-[0.9fr_1.1fr] gap-10 items-center">
<div class="aspect-[4/5] bg-surface-container border border-outline-variant overflow-hidden">{picture("skull", "w-full h-full object-cover", sizes="(min-width: 768px) 40vw, 100vw")}</div>
<div class="space-y-5">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">ARTIST AUTHORITY</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Meet Joshua Cole</h2>
<p class="font-label-caps text-label-caps text-secondary">Cover-Up / Rework / Realism Tattoo Artist</p>
<p class="font-body-md text-on-surface-variant leading-relaxed">Joshua Cole leads cover-up, rework, black-and-grey realism, color realistic imagery, blackwork, and large-scale redesign consults at Work of Art Tattoo &amp; Piercing in Las Vegas.</p>
<div class="flex flex-wrap gap-3">
<a class="inline-flex justify-center bg-secondary text-on-secondary px-6 py-3 font-label-caps text-[11px] uppercase tracking-widest" href="/artists/joshua-cole/">Joshua artist page</a>
<a class="inline-flex justify-center border border-outline px-6 py-3 font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary" href="/realism-tattoos-las-vegas/">Realism portfolio</a>
<a class="inline-flex justify-center border border-outline px-6 py-3 font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary" href="/healed_tattoo_gallery_las_vegas/">Healed work</a>
</div>
</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low" id="consult-photos">
<div class="max-w-4xl mx-auto border border-outline-variant bg-surface p-8 md:p-12 space-y-6">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">NEXT STEP</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Have a Tattoo You Want Covered or Reworked?</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">Send a clear photo before you book so Joshua can see the whole problem, not just the part you dislike.</p>
<ul class="grid grid-cols-1 sm:grid-cols-2 gap-3 font-body-md text-on-surface-variant">
<li>Entire existing tattoo</li>
<li>Surrounding skin</li>
<li>Clear lighting</li>
<li>Straight-on view</li>
<li>Approximate size</li>
<li>Placement on the body</li>
</ul>
<div class="flex flex-col sm:flex-row gap-3">
<a class="inline-flex justify-center bg-secondary text-on-secondary px-8 py-4 font-label-caps text-[11px] uppercase tracking-widest" href="/appointments/">Send Joshua a Photo</a>
<a class="inline-flex justify-center border border-outline px-8 py-4 font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary" href="#consult">Book a Cover-Up Consultation</a>
</div>
</div>
</section>
"""


def patch_page(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    text = raw
    text = re.sub(
        r'https://www\.workofarttattoo\.com/(?:cover-up-tattoos-las-vegas|cover_up_tattoos_las_vegas_master_authority_guide)/cover-up-tattoo-phoenix-hand-las-vegas-after\.webp',
        f"https://www.workofarttattoo.com/{CANONICAL_SLUG}/{IMAGES['hero']['slug']}.webp",
        text,
    )
    text = re.sub(
        r'<meta property="og:image:width" content="\d+"/>',
        '<meta property="og:image:width" content="1200"/>',
        text,
        count=1,
    )
    text = re.sub(
        r'<meta property="og:image:height" content="\d+"/>',
        '<meta property="og:image:height" content="1600"/>',
        text,
        count=1,
    )
    text = re.sub(
        r'<picture><source srcset="/cover-up-tattoos-las-vegas/cover-up-tattoo-phoenix-hand-las-vegas-after\.webp" type="image/webp"/><img[^>]*?></picture>',
        picture("hero", "w-full h-full object-cover opacity-55", "eager", "100vw"),
        text,
        count=1,
    )
    text = re.sub(
        r'<section[^>]*id="studio-portfolio"[\s\S]*?(?=<section[^>]*id="(?:scar-cover|coverable|pricing)")',
        evidence_sections(),
        text,
        count=1,
    )
    text = re.sub(
        r'\n<section[^>]*data-woa-proof-block="1"[\s\S]*?</section>\s*',
        "\n",
        text,
    )
    text = re.sub(
        r'<a class="px-10 py-5 border border-outline text-on-surface font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all text-center" href="#studio-portfolio">VIEW STUDIO WORK</a>',
        '<a class="px-10 py-5 border border-outline text-on-surface font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all text-center" href="#studio-portfolio">VIEW REAL WORK</a>',
        text,
    )
    if OLD_COVERUP_IMAGE_RE.search(text):
        raise SystemExit(f"{path.relative_to(ROOT)} still references old cover-up imagery")
    if MARKER not in text:
        raise SystemExit(f"{path.relative_to(ROOT)} missing cover-up evidence marker")
    if text != raw:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    ensure_assets()
    changed = 0
    for slug in PAGE_SLUGS:
        path = ROOT / slug / "code.html"
        if path.is_file() and patch_page(path):
            changed += 1
            print(f"[cover-up evidence] {path.relative_to(ROOT)}")
    print(f"Done: refreshed {changed} cover-up page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
