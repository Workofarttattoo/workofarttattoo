#!/usr/bin/env python3
"""Hero rating bar (Google stars) + interview card layout tweaks."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODE = ROOT / "home_work_of_art_tattoo_piercing/code.html"
ROOT_CODE = ROOT / "code.html"

GOOGLE_REVIEW_URL = "/reviews_vault_100_verified_masterpieces/"

RATING_INNER = f"""<div class="flex flex-col sm:flex-row sm:flex-wrap sm:items-center gap-4 sm:gap-8">
<div class="woa-google-rating flex items-center gap-3">
<span aria-hidden="true" class="woa-google-stars">★★★★★</span>
<span class="font-body-md text-on-surface leading-tight"><strong class="text-secondary font-semibold">5.0</strong> stars on <a class="text-secondary hover:underline font-semibold" href="{GOOGLE_REVIEW_URL}">Google</a></span>
</div>
<div class="h-8 w-px bg-outline-variant/30 hidden sm:block"></div>
<div class="text-on-surface-variant font-body-md text-body-md leading-snug">
<span class="text-on-surface font-bold">Hundreds of</span> positive Google reviews from our clients
</div>
</div>"""


def patch_rating_bar(html: str) -> str:
    return re.sub(
        r'<div class="woa-hero-rating-bar[^>]*>[\s\S]*?</div>\s*</section>',
        f'<div class="woa-hero-rating-bar absolute bottom-12 left-margin-mobile right-margin-mobile md:left-margin-desktop md:right-margin-desktop flex flex-wrap gap-6 md:gap-12 items-center py-8 border-t border-outline-variant/20">\n{RATING_INNER}\n</div>\n</section>',
        html,
        count=1,
    )


EXPERIENCE_OLD = (
    '<picture><source srcset="/home_work_of_art_tattoo_piercing/las-vegas-tattoo-artist-working-closeup.webp" '
    'type="image/webp"/><img alt="Tattoo artist at work inside Work of Art Tattoo Las Vegas studio" '
    'class="w-full h-full object-cover" height="1200" loading="lazy" '
    'src="/home_work_of_art_tattoo_piercing/las-vegas-tattoo-artist-working-closeup.png" width="1163"/></picture>'
)
EXPERIENCE_NEW = (
    '<picture><source srcset="/cover_up_tattoos_las_vegas_master_authority_guide/healed-realism-seraphim-eye-wings-tattoo.webp" '
    'type="image/webp"/><img alt="Healed black and grey seraphim eye and wings tattoo by Work of Art — Las Vegas" '
    'class="w-full h-full object-cover object-[center_35%]" height="800" loading="lazy" '
    'src="/cover_up_tattoos_las_vegas_master_authority_guide/healed-realism-seraphim-eye-wings-tattoo.png" width="800"/></picture>'
)
SUNFLOWER_EXPERIENCE = (
    '<picture><source srcset="/home_work_of_art_tattoo_piercing/client-portfolio/healed-color-sunflower-cover-up-leg-las-vegas.webp" '
    'type="image/webp"/><img alt="Healed color sunflower cover-up tattoo by Work of Art — Las Vegas" '
    'class="w-full h-full object-cover object-center" height="800" loading="lazy" '
    'src="/home_work_of_art_tattoo_piercing/client-portfolio/healed-color-sunflower-cover-up-leg-las-vegas.png" width="800"/></picture>'
)


def patch_experience_image(html: str) -> str:
    html = html.replace(EXPERIENCE_OLD, EXPERIENCE_NEW)
    html = html.replace(SUNFLOWER_EXPERIENCE, EXPERIENCE_NEW)
    return html


def patch_hero_interview_img(html: str) -> str:
    return html.replace(
        'class="w-full h-full object-cover object-center" decoding="async" fetchpriority="high" loading="eager" src="/home_work_of_art_tattoo_piercing/joshua-cole-studio-interview-las-vegas.png"',
        'class="w-full h-full object-cover object-[center_18%]" decoding="async" fetchpriority="high" loading="eager" src="/home_work_of_art_tattoo_piercing/joshua-cole-studio-interview-las-vegas.png"',
        1,
    )


def main() -> int:
    for path in (CODE, ROOT_CODE):
        if not path.is_file():
            continue
        html = path.read_text(encoding="utf-8")
        html = patch_rating_bar(html)
        html = patch_experience_image(html)
        html = patch_hero_interview_img(html)
        path.write_text(html, encoding="utf-8")
        print(f"[hero-ui] {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
