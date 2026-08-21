#!/usr/bin/env python3
"""Build Joshua Cole oil-painting → black & grey tattoo longevity page."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_entity_schema import guide_article_graph, schema_script

ROOT = Path(__file__).resolve().parent
SLUG = "joshua_oil_painting_black_grey_tattoo_aging_las_vegas"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"
SITE = "https://workofarttattoo.com"
OG = "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-statue-bust-cloth-drape-las-vegas"

TITLE = "Why Oil Painting Training Shapes How My Black & Grey Tattoos Age"
DESCRIPTION = (
    "Joshua Cole on values, contrast, composition, and edge control — how classical painting "
    "principles influence black and grey tattoo design for long-term healing in Las Vegas."
)

MAIN = f"""
<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl space-y-6">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Joshua Cole · artist essay</span>
<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">{html.escape(TITLE)}</h1>
<p class="font-body-lg text-on-surface-variant">Before I was a tattoo artist, I spent years studying oil painting — values, composition, and how light behaves on form. That training did not magically guarantee every tattoo ages perfectly. What it did give me is a way to <em>plan</em> for healing: where to leave skin open, where to anchor black, and how a piece should read six months later — not just under studio lights on day one.</p>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-3xl mx-auto space-y-10 font-body-lg text-on-surface-variant">
<h2 class="font-headline-lg text-on-surface">Values first — not maximum black</h2>
<p>In painting, you establish a value range before you chase detail. In black and grey tattooing, the same idea keeps work readable after healing. If every shadow is packed to the same depth, the piece closes up and turns flat once the skin settles. I map a deliberate range: deepest blacks for anchors, mid greys for form, and skin left open for highlights that still read after peeling.</p>
<p>That is why our <a class="text-secondary underline" href="/healed_black_grey_tattoos_las_vegas/">healed black and grey gallery</a> matters — you can see whether contrast survived, not just how dramatic the fresh photo looked.</p>

<h2 class="font-headline-lg text-on-surface pt-4">Contrast that survives distance — and time</h2>
<p>A portrait or wildlife piece has to work at arm's length, not only in a cropped Instagram square. Painting taught me to step back from the canvas constantly. I do the same with tattoos: if the silhouette and major value shapes do not hold from across the room, no amount of micro-detail will save it once healed.</p>
<p>Desert sun adds another variable. Las Vegas UV is relentless on exposed ink. Contrast planned with long-term readability in mind — not day-one shock — tends to hold up better for collectors who live here or visit often.</p>

<h2 class="font-headline-lg text-on-surface pt-4">Composition for a living body</h2>
<p>Canvas does not bend, swell, or sit in a car seat. A sleeve has to flow through the elbow; a thigh piece has to survive jeans and sun. Composition in painting is about directing the eye; on skin it is also about <em>where the body moves</em>. I plan major masses around joints and high-friction zones so detail does not land where it will blur fastest.</p>
<p>When clients ask about future work — connecting a half sleeve to a chest piece, for example — I am thinking in compositions, not isolated flash. That long-term view shows up in healed photos across multi-session projects.</p>

<h2 class="font-headline-lg text-on-surface pt-4">Edge control: hard, soft, and lost edges</h2>
<p>Classical training emphasizes when to sharpen an edge and when to let it dissolve. Tattooing rewards the same discipline. Hair, smoke, fabric folds, and skin texture all need different edge treatments. Over-hard outlines everywhere make realism look like a sticker; over-soft everything turns to mush at six months.</p>
<p>Edge decisions are also where cover-up work lives or dies. A redesign has to respect what is already in the skin while rebuilding value structure — the same problem as painting over an old canvas, with less room for error.</p>

<h2 class="font-headline-lg text-on-surface pt-4">What I cannot promise — and what I document instead</h2>
<p>No ethical artist guarantees a tattoo will age "better" than someone else's in every case. Skin type, lifestyle, sun exposure, and aftercare all matter. What I can show you is <strong>healed documentation</strong>: fresh photos, follow-ups, and honest notes about touch-ups when they happen.</p>
<p>Browse our <a class="text-secondary underline" href="/healed_tattoo_gallery_las_vegas/">healed tattoo gallery</a>, <a class="text-secondary underline" href="/tattoo_healing_before_after_real_results/">fresh vs healed color comparison</a>, and <a class="text-secondary underline" href="/realism_tattoos_las_vegas_master_authority_guide/">realism portfolio</a> — then book a consult if the approach matches what you want on your skin for years, not just for vacation photos.</p>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background text-center">
<div class="max-w-xl mx-auto space-y-6">
<h2 class="font-headline-md text-on-surface">See the approach on healed skin</h2>
<div class="flex flex-col sm:flex-row gap-4 justify-center">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest" href="/healed_black_grey_tattoos_las_vegas/">Healed black &amp; grey</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:border-secondary transition-colors" href="/appointments/">Book with Joshua</a>
</div>
</div>
</section>
</main>
"""


def patch_meta(page: str) -> str:
    canon = f"{SITE}/{SLUG}/"
    page = re.sub(r"<title>.*?</title>", f"<title>{html.escape(TITLE)} | Work of Art</title>", page, count=1)
    page = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{html.escape(DESCRIPTION)}" name="description"/>',
        page,
        count=1,
    )
    page = re.sub(
        r'<link href="https://workofarttattoo.com/[^"]*" rel="canonical"/>',
        f'<link href="{canon}" rel="canonical"/>',
        page,
        count=1,
    )
    og = f"{SITE}{OG}.webp"
    page = re.sub(
        r'<meta content="https://workofarttattoo.com/how_much[^"]*" property="og:image"/>',
        f'<meta content="{og}" property="og:image"/>',
        page,
        count=1,
    )
    return page


def main() -> int:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    out = ROOT / SLUG
    out.mkdir(parents=True, exist_ok=True)
    page = TEMPLATE.read_text(encoding="utf-8")
    page = re.sub(
        r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*',
        "",
        page,
        flags=re.DOTALL,
    )
    page = patch_meta(page)
    page = re.sub(
        r'<main class="relative pt-20">.*?</main>',
        MAIN.strip(),
        page,
        count=1,
        flags=re.DOTALL,
    )
    graph = guide_article_graph(slug=SLUG, title=TITLE, description=DESCRIPTION)
    page = page.replace("</head>", schema_script(graph) + "\n</head>", 1)
    (out / "code.html").write_text(page, encoding="utf-8")
    print(f"[ok] {SLUG}/code.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
