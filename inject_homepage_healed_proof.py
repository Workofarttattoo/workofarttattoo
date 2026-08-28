#!/usr/bin/env python3
"""Homepage row: fresh→healed side-by-side proof across tattoo categories."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
MARKER = 'data-woa-home-healed-proof="1"'
START = "<!-- WOA_HOME_HEALED_PROOF_START -->"
END = "<!-- WOA_HOME_HEALED_PROOF_END -->"

# label, href, fresh img base, healed img base, caption
COMPARISONS = (
    (
        "Color memorial eagle",
        "/tattoo_healing_before_after_real_results/",
        "/healed_tattoo_gallery_las_vegas/fresh-eagle-memorial-calf-tattoo-las-vegas",
        "/healed_tattoo_gallery_las_vegas/eagle-memorial-calf-healed-tattoo-las-vegas",
        "Same calf piece — day-zero saturation vs. settled color months later.",
        "Fresh color eagle memorial calf tattoo",
        "Healed color eagle memorial calf tattoo",
    ),
    (
        "Lion thigh · black & grey",
        "/healed_black_grey_tattoos_las_vegas/",
        "/healed_tattoo_gallery_las_vegas/fresh-roaring-lion-thigh-black-grey-joshua-cole-las-vegas",
        "/healed_tattoo_gallery_las_vegas/healed-3-month-roaring-lion-thigh-joshua-cole-las-vegas",
        "Roaring lion thigh — fresh redness vs. three-month heal with saturated blacks.",
        "Fresh roaring lion thigh black and grey realism",
        "Healed roaring lion thigh at three months",
    ),
)


def _img_cell(base: str, badge: str, alt: str) -> str:
    return f"""<div class="relative overflow-hidden aspect-[3/4] bg-surface-container">
<picture>
<source srcset="{base}.webp" type="image/webp"/>
<img alt="{alt} — Work of Art Las Vegas" class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-500" decoding="async" height="480" loading="lazy" src="{base}.png" width="360"/>
</picture>
<span class="absolute bottom-0 inset-x-0 bg-background/80 backdrop-blur-sm px-2 py-1.5 font-label-caps text-[9px] uppercase tracking-widest text-secondary text-center">{badge}</span>
</div>"""


def comparison_card(
    label: str,
    href: str,
    fresh_base: str,
    healed_base: str,
    caption: str,
    fresh_alt: str,
    healed_alt: str,
) -> str:
    return f"""<a class="group block border border-outline-variant/30 bg-surface-container overflow-hidden hover:border-secondary/50 transition-colors" href="{href}">
<div class="grid grid-cols-2 gap-px bg-outline-variant/40">
{_img_cell(fresh_base, "Fresh", fresh_alt)}
{_img_cell(healed_base, "Healed", healed_alt)}
</div>
<div class="p-4 space-y-1">
<span class="font-label-caps text-secondary text-[10px] uppercase tracking-widest">{label}</span>
<p class="font-body-md text-on-surface-variant text-sm leading-snug">{caption}</p>
</div>
</a>"""


def block_html() -> str:
    cards = "\n".join(
        comparison_card(label, href, fresh, healed, caption, fresh_alt, healed_alt)
        for label, href, fresh, healed, caption, fresh_alt, healed_alt in COMPARISONS
    )
    return f"""{START}
<section class="py-12 md:py-16 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-b border-outline-variant/20" {MARKER}>
<div class="max-w-6xl mx-auto space-y-8">
<div class="max-w-2xl space-y-3">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Healed proof</span>
<h2 class="font-headline-md text-on-surface text-2xl md:text-3xl">Fresh vs healed — same clients, real timelines</h2>
<p class="font-body-md text-on-surface-variant">We photograph work right after the session and again once it settles. Compare angles side by side before you book.</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 max-w-4xl">
{cards}
</div>
<p class="font-body-md text-on-surface-variant text-sm text-center"><a class="text-secondary underline hover:no-underline" href="/healing_database_tattoo_timeline_encyclopedia_las_vegas/">Healing Database</a> · <a class="text-secondary underline hover:no-underline" href="/healed_tattoo_gallery_las_vegas/">Full healed gallery</a> · <a class="text-secondary underline hover:no-underline" href="/tattoo_healing_before_after_real_results/">Healing before &amp; after guide</a> · <a class="text-secondary underline hover:no-underline" href="/reviews_vault_100_verified_masterpieces/">Client reviews</a></p>
</div>
</section>
{END}
"""


def main() -> int:
    if not HOME.is_file():
        raise SystemExit(f"Missing {HOME}")
    raw = HOME.read_text(encoding="utf-8")
    block = block_html()
    if START in raw:
        updated = re.sub(
            rf"{re.escape(START)}[\s\S]*?{re.escape(END)}",
            block,
            raw,
            count=1,
        )
    else:
        anchor = "<!-- WOA_HOME_WELCOME_END -->"
        if anchor not in raw:
            raise SystemExit("Welcome section marker not found")
        updated = raw.replace(anchor, anchor + "\n" + block, 1)
    if updated != raw:
        HOME.write_text(updated, encoding="utf-8")
        print("[ok] home_work_of_art_tattoo_piercing/code.html")
    else:
        print("[skip] no changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
