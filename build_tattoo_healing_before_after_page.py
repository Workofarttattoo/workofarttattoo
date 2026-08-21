#!/usr/bin/env python3
"""Build tattoo_healing_before_after_real_results/code.html — fresh vs healed studio proof."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLUG = "tattoo_healing_before_after_real_results"
OUT_DIR = ROOT / SLUG
OUT = OUT_DIR / "code.html"
CANON = f"https://workofarttattoo.com/{SLUG}/"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"
DESERT_GUIDE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"

COMPARISON = f"/{SLUG}/eagle-memorial-calf-fresh-vs-healed-comparison-las-vegas"
FRESH = f"/{SLUG}/eagle-memorial-calf-fresh-tattoo-las-vegas"
OG_IMG = f"{CANON}eagle-memorial-calf-fresh-vs-healed-comparison-las-vegas.webp"

TITLE = "Tattoo Healing: Fresh vs Healed | Real Studio Results | Work of Art"
DESCRIPTION = (
    "See the same color memorial tattoos fresh and healed months later — why ink lightens, "
    "what is normal, and how aftercare affects long-term vibrance. Work of Art Las Vegas."
)

MAIN = f"""
<main class="relative pt-20">
<section class="relative min-h-[70vh] flex items-end px-6 md:px-margin-desktop pb-16 overflow-hidden">
<div class="absolute inset-0 z-0">
<picture>
<source srcset="{COMPARISON}.webp" type="image/webp"/>
<img alt="Eagle memorial calf tattoos — fresh vs healed comparison, Work of Art Las Vegas" class="w-full h-full object-cover opacity-50" decoding="async" height="1024" loading="eager" src="{COMPARISON}.png"/>
</picture>
<div class="absolute inset-0 bg-gradient-to-t from-background via-background/60 to-transparent"></div>
</div>
<div class="relative z-10 max-w-4xl">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em] mb-4 block">Healing education · real studio photos</span>
<h1 class="font-headline-xl text-[40px] md:text-headline-xl text-on-surface mb-6 leading-tight">Fresh vs healed: what your tattoo will look like over time</h1>
<p class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">These are the same two clients — photographed right after their sessions, then again a few months later once healing finished. Color always settles. That is normal, not a mistake.</p>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" id="comparison">
<div class="max-w-5xl mx-auto space-y-8">
<h2 class="font-headline-lg text-on-surface">Same design, two healing stages</h2>
<p class="font-body-md text-on-surface-variant max-w-3xl">Both calves carry the same memorial eagle piece — flames, banner lettering, and dates. The photo on the <strong>left</strong> was taken right after the session; the <strong>right</strong> was taken several months later after full healing.</p>
<figure class="border border-outline-variant bg-surface overflow-hidden">
<picture>
<source srcset="{COMPARISON}.webp" type="image/webp"/>
<img alt="Side by side — fresh tattoo on left calf, healed tattoo on right calf, eagle memorial color work by Joshua Cole" class="w-full h-auto" decoding="async" height="1024" loading="lazy" src="{COMPARISON}.png" width="1011"/>
</picture>
<figcaption class="p-6 md:p-8 font-body-md text-on-surface-variant border-t border-outline-variant/30">
<span class="font-label-caps text-secondary text-[10px] uppercase tracking-widest block mb-2">Left · fresh</span>
Redness, swelling, and a glossy “just finished” look — colors read at peak saturation.
<span class="font-label-caps text-secondary text-[10px] uppercase tracking-widest block mt-4 mb-2">Right · healed (months later)</span>
Skin tone normal; yellows and oranges softened into a stable, matte finish. Detail is still clear — the ink lives <em>in</em> the skin instead of sitting on top of it.
</figcaption>
</figure>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
<div>
<h2 class="font-headline-lg text-on-surface mb-6">Why fresh tattoos look brighter</h2>
<ul class="font-body-md text-on-surface-variant space-y-4 list-disc pl-5">
<li><strong>Plasma and lymph</strong> sit on the surface right after tattooing, adding shine and contrast.</li>
<li><strong>Inflammation</strong> brings blood flow to the area — reds and oranges appear more intense.</li>
<li><strong>Ink is concentrated</strong> in the upper dermis before your body encases pigment in healed tissue.</li>
<li><strong>No dead skin layer yet</strong> — once the epidermis renews, a thin matte veil sits over the color.</li>
</ul>
</div>
<figure class="border border-outline-variant bg-surface overflow-hidden">
<picture>
<source srcset="{FRESH}.webp" type="image/webp"/>
<img alt="Fresh color eagle memorial tattoo on calf immediately after session — Work of Art Las Vegas" class="w-full h-auto" decoding="async" height="1024" loading="lazy" src="{FRESH}.png" width="735"/>
</picture>
<figcaption class="p-5 font-body-md text-on-surface-variant border-t border-outline-variant/30">Close-up fresh work — note redness around the piece and the wet sheen. This is expected on day zero.</figcaption>
</figure>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low">
<div class="max-w-3xl mx-auto space-y-8">
<h2 class="font-headline-lg text-on-surface">Why tattoos lighten while healing</h2>
<p class="font-body-lg text-on-surface-variant">Lightening does not mean the artist “lost” color. Healing is your skin rebuilding over intentional punctures. Several things happen at once:</p>
<div class="space-y-6 font-body-md text-on-surface-variant">
<p><strong>1. The epidermis replaces itself.</strong> The top layer you see on day one sheds during peeling (usually days 5–14). When new skin forms, pigment reads slightly softer.</p>
<p><strong>2. Excess ink clears.</strong> Some pigment sits too shallow and washes out with plasma — that is why we wipe and refine during the session. What remains is the stable layer in the dermis.</p>
<p><strong>3. White highlights are skin, not ink.</strong> Bright spots in fresh color work often come from leaving skin open. After healing, those areas look naturally lighter — by design.</p>
<p><strong>4. Scar tissue maturation.</strong> The dermis contracts and settles over 6–12 weeks. Contrast evens out; harsh edges soften into a readable long-term image.</p>
<p><strong>5. Sun, dryness, and aftercare.</strong> In Las Vegas, UV and low humidity can fade color faster if you skip SPF or let the tattoo dry out. Follow our <a class="text-secondary underline" href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/">desert climate aftercare guide</a>.</p>
</div>
<div class="bg-surface border-l-4 border-secondary p-8 mt-8">
<h3 class="font-label-caps text-label-caps text-secondary mb-2">What “normal” looks like</h3>
<p class="font-body-md text-on-surface italic">A healed tattoo should still read clearly at arm’s length. Colors mellow — they should not turn muddy grey or patchy. If something looks uneven after month three, book a healed check-in.</p>
</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto">
<h2 class="font-headline-lg text-on-surface mb-8">Healing timeline (color work)</h2>
<ol class="space-y-8 font-body-md text-on-surface-variant">
<li class="flex gap-4"><span class="font-headline-md text-secondary shrink-0">01</span><div><strong class="text-on-surface">Days 0–3</strong> — Wrap or second skin per artist instructions. Wash gently 2–3× daily; pat dry. Redness and warmth are normal.</div></li>
<li class="flex gap-4"><span class="font-headline-md text-secondary shrink-0">02</span><div><strong class="text-on-surface">Days 4–14</strong> — Light peeling and itch. Do not pick. Thin lotion if skin feels tight — especially in desert air.</div></li>
<li class="flex gap-4"><span class="font-headline-md text-secondary shrink-0">03</span><div><strong class="text-on-surface">Weeks 3–6</strong> — Surface looks healed but deeper layers still settle. Colors appear slightly dull — this is the stage clients worry about most.</div></li>
<li class="flex gap-4"><span class="font-headline-md text-secondary shrink-0">04</span><div><strong class="text-on-surface">Months 2–4+</strong> — Final vibrance. Compare to fresh photos like the ones on this page. Touch-ups are optional if saturation needs a boost.</div></li>
</ol>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" id="faq">
<div class="max-w-3xl mx-auto space-y-6">
<h2 class="font-headline-lg text-on-surface mb-4">Common questions</h2>
<details class="group bg-surface border border-outline-variant/30 p-6 cursor-pointer hover:border-secondary transition-all"><summary class="flex justify-between items-center font-headline-md list-none">Is it normal for my tattoo to look faded after peeling?<span class="material-symbols-outlined group-open:rotate-180 transition-transform">expand_more</span></summary><p class="mt-4 font-body-md text-on-surface-variant">Yes. Peeling removes the most saturated surface layer. Color returns as the epidermis fully regenerates — usually over several weeks. If it still looks washed out after 8–12 weeks, ask about a touch-up.</p></details>
<details class="group bg-surface border border-outline-variant/30 p-6 cursor-pointer hover:border-secondary transition-all"><summary class="flex justify-between items-center font-headline-md list-none">Will color tattoos lighten more than black and grey?<span class="material-symbols-outlined group-open:rotate-180 transition-transform">expand_more</span></summary><p class="mt-4 font-body-md text-on-surface-variant">Color often shows more visible change from fresh to healed because bright pigments start at higher saturation. Black and grey also settles — contrast softens slightly while blacks stay anchored in the dermis.</p></details>
<details class="group bg-surface border border-outline-variant/30 p-6 cursor-pointer hover:border-secondary transition-all"><summary class="flex justify-between items-center font-headline-md list-none">When should I worry something went wrong?<span class="material-symbols-outlined group-open:rotate-180 transition-transform">expand_more</span></summary><p class="mt-4 font-body-md text-on-surface-variant">Spreading redness, heat, pus, red streaks, or pain that worsens after day three are infection signs — see a doctor. Patchy ink loss from picking scabs is different; prevention is easier than repair.</p></details>
<details class="group bg-surface border border-outline-variant/30 p-6 cursor-pointer hover:border-secondary transition-all"><summary class="flex justify-between items-center font-headline-md list-none">Can I prevent lightening in Las Vegas sun?<span class="material-symbols-outlined group-open:rotate-180 transition-transform">expand_more</span></summary><p class="mt-4 font-body-md text-on-surface-variant">Keep fresh work out of direct sun until fully closed. After healing, daily SPF on exposed tattoos slows UV breakdown of pigment. Hydration and fragrance-free aftercare help in dry desert air.</p></details>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background text-center">
<div class="max-w-2xl mx-auto space-y-6">
<h2 class="font-headline-lg text-on-surface">Planning color work?</h2>
<p class="font-body-md text-on-surface-variant">Joshua Cole documents fresh and healed photos in-studio so you know what to expect. Start with a consult — we walk through design, session length, and aftercare before you commit.</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest hover:glow-sm transition-all" href="/appointments/">Book consult</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all" href="/artists/joshua-cole/">Joshua's portfolio</a>
</div>
<p class="font-body-md text-on-surface-variant pt-4">More reading: <a class="text-secondary underline" href="/healed_tattoo_gallery_las_vegas/">healed tattoo gallery by style</a> · <a class="text-secondary underline" href="/knowledge/tattoo-aging-and-fading-over-time/">how tattoos age over time</a> · <a class="text-secondary underline" href="/reviews_vault_100_verified_masterpieces/">healed client stories</a></p>
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
        r'<link href="https://workofarttattoo.com/[^"]*" rel="canonical"/>',
        f'<link href="{CANON}" rel="canonical"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta content="https://workofarttattoo.com/tattoo_healing_in_desert_climate[^"]*" property="og:url"/>',
        f'<meta content="{CANON}" property="og:url"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta content="Tattoo &amp; Piercing Aftercare in Desert Climate \| Work of Art" property="og:title"/>',
        f'<meta content="{TITLE}" property="og:title"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta content="Vegas-specific healing:[^"]*" property="og:description"/>',
        f'<meta content="{DESCRIPTION}" property="og:description"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta content="https://workofarttattoo.com/how_much[^"]*" property="og:image"/>',
        f'<meta content="{OG_IMG}" property="og:image"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta content="Tattoo &amp; Piercing Aftercare in Desert Climate \| Work of Art" name="twitter:title"/>',
        f'<meta content="{TITLE}" name="twitter:title"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta content="Vegas-specific healing:[^"]*" name="twitter:description"/>',
        f'<meta content="{DESCRIPTION}" name="twitter:description"/>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta content="https://workofarttattoo.com/how_much[^"]*" name="twitter:image"/>',
        f'<meta content="{OG_IMG}" name="twitter:image"/>',
        html,
        count=1,
    )
    return html


def patch_guide_hub(html: str) -> str:
    current = 'aria-current="page" class="woa-guide-pill is-current" href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/"'
    if current in html:
        html = html.replace(
            current,
            'class="woa-guide-pill" href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/"',
            1,
        )
    pill = (
        f'<a aria-current="page" class="woa-guide-pill is-current" href="/{SLUG}/">'
        "Fresh vs Healed Healing</a>"
    )
    anchor = 'href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/">Desert Climate Aftercare</a>'
    return html.replace(anchor, anchor + pill, 1)


def patch_main(html: str) -> str:
    html = re.sub(
        r'<main class="relative pt-20">.*?</main>',
        MAIN.strip(),
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def link_from_desert_guide() -> None:
    if not DESERT_GUIDE.is_file():
        return
    raw = DESERT_GUIDE.read_text(encoding="utf-8")
    link = 'href="/tattoo_healing_before_after_real_results/"'
    if link in raw:
        return
    needle = '<p class="font-body-lg text-body-lg text-on-surface-variant mb-12 leading-relaxed">\n                        Healing a tattoo in a desert climate'
    insert = (
        '<p class="font-body-lg text-body-lg text-on-surface-variant mb-6 leading-relaxed">\n'
        "                        Wondering how much a tattoo lightens after healing? See our "
        f'<a class="text-secondary underline" href="/{SLUG}/">fresh vs healed studio photos</a> '
        "— same clients, months apart.\n"
        "                    </p>\n"
    )
    if needle not in raw:
        return
    updated = raw.replace(needle, insert + needle, 1)
    DESERT_GUIDE.write_text(updated, encoding="utf-8")
    print(f"[ok] linked from {DESERT_GUIDE.relative_to(ROOT)}")


def main() -> int:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = TEMPLATE.read_text(encoding="utf-8")
    html = re.sub(
        r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    html = patch_meta(html)
    html = patch_guide_hub(html)
    html = patch_main(html)
    OUT.write_text(html, encoding="utf-8")
    print(f"[ok] {OUT.relative_to(ROOT)}")
    link_from_desert_guide()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
