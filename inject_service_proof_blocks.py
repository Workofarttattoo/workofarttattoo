#!/usr/bin/env python3
"""Inject compact proof blocks on service guide pages."""

from __future__ import annotations

import re
from pathlib import Path

from woa_healed_timelines import JOSHUA_CASE_STUDIES, KATELYN_CASE_STUDIES, CaseStudy
from woa_nav_config import HOME_SLUG

ROOT = Path(__file__).resolve().parent
MARKER = 'data-woa-proof-block="1"'

SERVICE_STUDIES: dict[str, CaseStudy] = {
    "realism_tattoos_las_vegas_master_authority_guide": JOSHUA_CASE_STUDIES[0],
    "cover_up_tattoos_las_vegas_master_authority_guide": JOSHUA_CASE_STUDIES[2],
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": JOSHUA_CASE_STUDIES[1],
    "tattoo_healing_before_after_real_results": JOSHUA_CASE_STUDIES[0],
    "best_piercing_shop_las_vegas_updated_jewelry_standards": KATELYN_CASE_STUDIES[0],
    "fine_line_tattoos_las_vegas_master_authority_guide": JOSHUA_CASE_STUDIES[1],
    "walk_in_tattoos_las_vegas_authority_guide": JOSHUA_CASE_STUDIES[0],
}

PIERCING_PROOF_SKIP = frozenset(
    {
        HOME_SLUG,
        "studio_gallery",
        "artists",
        "appointments",
        "studio_videos",
        "reviews_vault_100_verified_masterpieces",
        "flash_art_deals_under_100",
        "healed_tattoo_gallery_las_vegas",
        "offsite_bookings",
    }
)


def is_piercing_study(study: CaseStudy) -> bool:
    if study.artist == "Katelyn Cole":
        return True
    blob = f"{study.title} {study.placement}".lower()
    return "piercing" in blob or "ear curation" in blob


def is_piercing_slug(slug: str) -> bool:
    if slug in PIERCING_PROOF_SKIP:
        return False
    if slug.startswith("tattoo_") or slug.endswith("_tattoo_guide"):
        return False
    return slug.startswith("katelyn_") or "piercing" in slug


def study_for_slug(slug: str) -> CaseStudy | None:
    if slug in SERVICE_STUDIES:
        return SERVICE_STUDIES[slug]
    if is_piercing_slug(slug):
        return KATELYN_CASE_STUDIES[0]
    return None


def proof_block(study: CaseStudy) -> str:
    healed = study.stages[-1].note if study.stages else "Documented in studio."
    aftercare = (
        "Written piercing aftercare for Vegas heat; downsizing consult at 6 weeks when appropriate."
        if is_piercing_study(study)
        else "Desert-climate aftercare handout included — see our healing guide for saline and sun rules."
    )
    img = ""
    if study.image_stem:
        webp = f"/{study.image_dir}/{study.image_stem}.webp"
        png = f"/{study.image_dir}/{study.image_stem}.png"
        if study.image_dir.startswith("cover"):
            png = webp
        img = f"""
<div class="md:col-span-5">
<picture><source srcset="{webp}" type="image/webp"/>
<img alt="{study.title} — {study.artist}, Work of Art Las Vegas" class="w-full h-auto object-cover border border-outline-variant/30" loading="lazy" src="{png}"/>
</picture>
</div>"""
    return f"""
<section class="py-12 px-margin-mobile md:px-margin-desktop bg-surface-container border-y border-outline-variant/20" {MARKER}>
<div class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
{img}
<div class="{'md:col-span-7' if img else 'md:col-span-12'} space-y-6">
<h2 class="font-headline-md text-on-surface">Real work from this studio</h2>
<dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-4 font-body-md text-on-surface-variant">
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[11px] mb-1">Real client piece</dt><dd class="text-on-surface">{study.title}</dd></div>
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[11px] mb-1">Artist</dt><dd class="text-on-surface">{study.artist}</dd></div>
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[11px] mb-1">Time</dt><dd>{study.sessions}</dd></div>
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[11px] mb-1">Placement</dt><dd>{study.placement}</dd></div>
<div class="sm:col-span-2"><dt class="font-label-caps text-secondary uppercase tracking-widest text-[11px] mb-1">Healed result</dt><dd>{healed}</dd></div>
<div class="sm:col-span-2"><dt class="font-label-caps text-secondary uppercase tracking-widest text-[11px] mb-1">Aftercare note</dt><dd>{aftercare}</dd></div>
</dl>
<p class="font-body-md text-on-surface-variant">{study.summary}</p>
</div>
</div>
</section>
"""


PROOF_RE = re.compile(
    rf'<section[^>]*{re.escape(MARKER)}[\s\S]*?</section>',
    re.MULTILINE,
)


def inject(path: Path, slug: str) -> bool:
    study = study_for_slug(slug)
    if not study:
        return False
    raw = path.read_text(encoding="utf-8")
    block = proof_block(study)
    if MARKER in raw:
        new_html = PROOF_RE.sub(block, raw, count=1)
    elif "<footer" in raw:
        new_html = raw.replace("<footer", block + "\n<footer", 1)
    elif "</main>" in raw:
        new_html = raw.replace("</main>", block + "\n</main>", 1)
    else:
        return False
    if new_html != raw:
        path.write_text(new_html, encoding="utf-8")
        return True
    return False


def iter_target_slugs() -> list[str]:
    slugs: set[str] = set(SERVICE_STUDIES)
    for path in ROOT.glob("*/code.html"):
        slug = path.parent.name
        if study_for_slug(slug):
            slugs.add(slug)
    return sorted(slugs)


def main() -> int:
    n = 0
    for slug in iter_target_slugs():
        path = ROOT / slug / "code.html"
        if path.is_file() and inject(path, slug):
            print(f"[ok] {slug}")
            n += 1
    print(f"Done: {n} proof block(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
