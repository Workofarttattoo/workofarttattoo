#!/usr/bin/env python3
"""Build desert-climate piercing aftercare authority guide (Katelyn Cole voice)."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_content_standards import reviewed_by_block
from woa_entity_schema import ID_KATELYN, guide_article_graph, schema_script

ROOT = Path(__file__).resolve().parent
SLUG = "piercing_aftercare_desert_climate_las_vegas_expert_guide"
CANON = f"https://workofarttattoo.com/{SLUG}/"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"
TITLE = "Piercing Aftercare Las Vegas | Desert Climate Guide — Book Online"
DESCRIPTION = (
    "Las Vegas piercing aftercare — swimming, hot tubs, dust, gym sweat, and saline routines "
    "for dry desert heat. Master piercer Katelyn Cole at Work of Art. Book piercing online."
)
OG = "/studio_gallery/ear-lobe-piercing-session-da19eec5"

MAIN = """
<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-4xl space-y-6">
<span class="font-label-caps text-secondary uppercase tracking-[0.2em]">Desert piercing aftercare · Katelyn Cole</span>
<h1 class="font-headline-xl text-on-surface leading-tight">Piercing aftercare in the Las Vegas desert</h1>
{REVIEWED_BY}
<p class="font-body-lg text-on-surface-variant">Humidity below 10% is normal here. Your crusties tighten faster, pools are everywhere, and dust storms show up without warning. This guide is what I tell every client before they leave my chair.</p>
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline" href="/piercing_types_las_vegas_authority_hub/">Piercing encyclopedia</a> · <a class="text-secondary underline" href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/">Tattoo desert aftercare</a> · <a class="text-secondary underline" href="/studio_videos/#katelyn-piercing">Piercing videos</a></p>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-3xl mx-auto space-y-12 font-body-md text-on-surface-variant">
<section class="space-y-4"><h2 class="font-headline-md text-on-surface text-2xl">Why Vegas dries out new piercings</h2>
<p>Low humidity pulls moisture from healing skin. Crusties form a hard shell faster than at the coast — that is normal, not a crisis. Picking them micro-tears the fistula. Sterile saline mist softens crust; your fingers do not belong on the jewelry.</p></section>
<section class="space-y-4"><h2 class="font-headline-md text-on-surface text-2xl">Swimming in Las Vegas</h2>
<p>Hotel pools, day clubs, and vacation dips are tempting — wait until your piercer clears you. Bacteria in standing water is the leading cause of irritation bumps I see on tourists. Ear and navel piercings: minimum 4–6 weeks before submerging; cartilage often longer.</p></section>
<section class="space-y-4"><h2 class="font-headline-md text-on-surface text-2xl">Hot tubs &amp; saunas</h2>
<p>Hot water softens healing tissue and introduces bacteria. No hot tubs, steam rooms, or long baths until fully healed. A quick shower is fine — keep saline after if shampoo runs over the piercing.</p></section>
<section class="space-y-4"><h2 class="font-headline-md text-on-surface text-2xl">Dust storms &amp; outdoor events</h2>
<p>Spring wind in the valley kicks up fine dust that irritates fresh nostril and conch work. Rinse with saline after outdoor festivals; change pillowcases if you come home dusty.</p></section>
<section class="space-y-4"><h2 class="font-headline-md text-on-surface text-2xl">Sunscreen &amp; sun</h2>
<p>Never SPF on a fresh piercing — chemicals burn open tissue. Healed piercings still need protection; titanium jewelry can heat in direct sun. Hats and shade beat re-traumatizing a healing helix.</p></section>
<section class="space-y-4"><h2 class="font-headline-md text-on-surface text-2xl">Gym sweat</h2>
<p>Sweat is salty — it dries into crust on cartilage posts. Rinse with saline after workouts; do not wipe with a gym towel on fresh work. Headbands and over-ear headphones add pressure — plan around them.</p></section>
<section class="space-y-4"><h2 class="font-headline-md text-on-surface text-2xl">Daily cleaning routine</h2>
<ul class="list-disc pl-5 space-y-2"><li>Wash hands before touching anywhere near the piercing.</li><li>Sterile saline mist 1–2× daily — spray, wait, pat dry with paper towel.</li><li>No alcohol, peroxide, or tea tree unless I specifically adjust your plan.</li><li>No twisting the jewelry — ever.</li></ul></section>
<section class="space-y-4"><h2 class="font-headline-md text-on-surface text-2xl">When to call your piercer</h2>
<ul class="list-disc pl-5 space-y-2"><li>Jewelry embedding into swollen skin.</li><li>Bump growing for two weeks straight after fixing sleep and pressure.</li><li>Spreading redness, pus, fever, or red streaks — see a clinician too.</li></ul></section>
<div class="flex flex-wrap gap-4 pt-4">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps tracking-widest" href="/appointments/">Book piercing</a>
<a class="border border-outline px-10 py-4 font-label-caps tracking-widest hover:border-secondary" href="/katelyn_cole_piercing_authority_hub_las_vegas/">Katelyn's authority topics</a>
</div>
</div>
</section>
</main>
"""


def main() -> int:
    main_html = MAIN.replace("{REVIEWED_BY}", reviewed_by_block(expert="katelyn"))
    page = TEMPLATE.read_text(encoding="utf-8")
    page = re.sub(r"<title>.*?</title>", f"<title>{html.escape(TITLE)} | Work of Art</title>", page, count=1)
    page = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{html.escape(DESCRIPTION)}" name="description"/>', page, count=1)
    page = re.sub(r'<link href="https://workofarttattoo.com/[^"]*" rel="canonical"/>', f'<link href="{CANON}" rel="canonical"/>', page, count=1)
    page = re.sub(r'<main class="relative pt-20">.*?</main>', main_html.strip(), page, count=1, flags=re.DOTALL)
    page = re.sub(r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*', "", page, flags=re.DOTALL)
    graph = guide_article_graph(slug=SLUG, title=TITLE, description=DESCRIPTION, author_id=ID_KATELYN)
    page = page.replace("</head>", schema_script(graph) + "\n</head>", 1)
    out = ROOT / SLUG
    out.mkdir(parents=True, exist_ok=True)
    (out / "code.html").write_text(page, encoding="utf-8")
    print(f"[ok] {SLUG}/code.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
