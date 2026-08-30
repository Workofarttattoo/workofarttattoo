#!/usr/bin/env python3
"""Regenerate all static HTML/assets before GitHub Pages deploy.

Run this before committing/pushing to main. The GitHub Actions production
workflow regenerates the site again, creates index.html files, and publishes
the result to the gh-pages branch.
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME_HTML = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
ROOT_HTML = ROOT / "code.html"
BUILD_STAMP_RE = re.compile(r"<!-- WOA_BUILD_STAMP: [^>]+ -->\n?")

PIPELINE: list[list[str]] = [
    ["python3", str(ROOT / "restore_katelyn_portrait.py")],
    ["python3", str(ROOT / "import_healed_fresh_batch.py")],
    ["python3", str(ROOT / "fix_homepage_portfolio.py")],
    ["python3", str(ROOT / "inject_homepage_healed_proof.py")],
    ["python3", str(ROOT / "fix_homepage_hero_ui.py")],
    ["python3", str(ROOT / "set_hero_carousel.py")],
    ["python3", str(ROOT / "fix_hero_carousel.py")],
    ["python3", str(ROOT / "inject_client_videos.py")],
    ["python3", str(ROOT / "inject_studio_portfolio.py")],
    ["python3", str(ROOT / "inject_homepage_atmosphere.py")],
    ["python3", str(ROOT / "inject_homepage_welcome.py")],
    # ["python3", str(ROOT / "fix_hero_layout.py")],  # Disabled: breaks new carousel structure
    ["python3", str(ROOT / "inject_site_typography.py")],
    ["python3", str(ROOT / "build_studio_videos_page.py")],
    ["python3", str(ROOT / "build_merchandise_page.py")],
    ["python3", str(ROOT / "build_knowledge_hub.py")],
    ["python3", str(ROOT / "build_piercing_authority_pages.py")],
    ["python3", str(ROOT / "build_piercing_pillar_pages.py")],
    ["python3", str(ROOT / "build_katelyn_piercing_authority_pages.py")],
    ["python3", str(ROOT / "build_piercing_desert_aftercare_guide.py")],
    ["python3", str(ROOT / "build_piercing_specials_page.py")],
    ["python3", str(ROOT / "inject_page_spotlights.py")],
    ["python3", str(ROOT / "inject_sparkle_cursor.py")],
    ["python3", str(ROOT / "inject_ga4_conversions.py")],
    ["python3", str(ROOT / "build_start_here_hub.py")],
    ["python3", str(ROOT / "build_geo_landing_pages.py")],
    ["python3", str(ROOT / "build_retired_geo_redirects.py")],
    ["python3", str(ROOT / "build_near_strip_geo_hub.py")],
    ["python3", str(ROOT / "build_geo_quality_reports.py")],
    ["python3", str(ROOT / "build_url_aliases.py")],
    ["python3", str(ROOT / "upgrade_site_navigation.py")],
    ["python3", str(ROOT / "inject_sticky_book_cta.py")],
    ["python3", str(ROOT / "inject_guides_hub.py"), "--refresh"],
    ["python3", str(ROOT / "inject_availability_urgency.py")],
    ["python3", str(ROOT / "fix_site_footer.py")],
    ["python3", str(ROOT / "optimize_homepage_perf.py")],
    ["python3", str(ROOT / "fix_homepage_pagespeed.py")],
    ["python3", str(ROOT / "refine_site_experience.py")],
    ["python3", str(ROOT / "humanize_site_copy.py")],
    ["python3", str(ROOT / "remove_jay_jay_from_site.py")],
    ["python3", str(ROOT / "bridge_10_copy_gaps.py")],
    ["python3", str(ROOT / "implement_seo_growth_actions.py")],
    ["python3", str(ROOT / "final_copy_polish.py")],
    ["python3", str(ROOT / "fix_social_links.py")],
    ["python3", str(ROOT / "fix_studio_booking_email.py")],
    ["python3", str(ROOT / "inject_piercing_promotions.py")],
    ["python3", str(ROOT / "fix_yoast_seo_meta.py")],
    ["python3", str(ROOT / "inject_entity_schema.py")],
    ["python3", str(ROOT / "refresh_cover_up_evidence.py")],
    ["python3", str(ROOT / "fix_piercing_content_integrity.py")],
    ["python3", str(ROOT / "inject_google_tag_manager.py")],
    ["python3", str(ROOT / "inject_mixpanel.py")],
    # Last: banner markup + woa-home.css + repaired <img> tags (earlier steps may drop the CSS link)
    ["python3", str(ROOT / "repair_homepage_banner_and_images.py")],
    ["python3", str(ROOT / "normalize_head_metadata.py")],
    ["python3", str(ROOT / "inject_piercing_promotions.py")],
    ["python3", str(ROOT / "inject_ga4_conversions.py")],
    ["python3", str(ROOT / "normalize_head_metadata.py")],
    ["python3", str(ROOT / "fix_piercing_content_integrity.py")],
    ["python3", str(ROOT / "repair_visual_intent.py")],
    ["python3", str(ROOT / "remove_elevenlabs_widget.py")],
    ["python3", str(ROOT / "tools/check_merchandise_page.py")],
    ["python3", str(ROOT / "build_retired_cover_up_redirect.py")],
]


def run_step(cmd: list[str]) -> None:
    script = next((Path(part) for part in cmd if part.endswith(".py")), None)
    if script is None or not script.is_file():
        print(f"[skip] missing {script.name if script else 'script'}")
        return
    print(f"\n>>> {' '.join(cmd)}")
    subprocess.run(cmd, cwd=ROOT, check=True)


def stamp_build(html_path: Path) -> None:
    html = html_path.read_text(encoding="utf-8")
    html = BUILD_STAMP_RE.sub("", html)
    stamp = (
        "<!-- WOA_BUILD_STAMP: "
        f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} -->"
    )
    if "<head>" not in html:
        raise SystemExit(f"No <head> in {html_path}")
    html = html.replace("<head>", f"<head>\n{stamp}", 1)
    html_path.write_text(html, encoding="utf-8")


def verify_homepage() -> None:
    if not HOME_HTML.is_file():
        raise SystemExit(f"Missing homepage export: {HOME_HTML}")

    html = HOME_HTML.read_text(encoding="utf-8")
    size = HOME_HTML.stat().st_size
    errors: list[str] = []

    required = [
        ("WOA_HERO_BANNER_START", "studio hero banner block"),
        ("work-of-art-studio-banner-las-vegas", "studio banner image asset ref"),
        ("woa-home.css", "homepage banner/layout stylesheet"),
        ("GTM-TZTQSQBB", "Google Tag Manager container"),
        ("/start_here/", "Start Here hub link"),
        ("WOA_BUILD_STAMP:", "deploy build stamp"),
        ("woa-typography.css", "site typography bundle"),
        ("woa-tailwind.min.css", "compiled Tailwind (no CDN)"),
        ("UnifrakturMaguntia", "gothic drop-cap font"),
    ]
    for needle, label in required:
        if needle not in html:
            errors.append(f"missing {label}")

    banned = [
        ("cdn.tailwindcss.com", "Tailwind CDN (use woa-tailwind.min.css)"),
        ("DXSZTKZyt2l", "weak studio reel"),
        ('href="#hero-interview"', "old hero-interview anchor (without -preview)"),
        ("woa-ig-preview", "legacy Instagram preview cards"),
        ("The interview plays at the top of this page", "stale featured copy"),
        ('blockquote class="instagram-media"', "broken Instagram blockquote embed"),
    ]
    for needle, label in banned:
        if needle in html:
            errors.append(f"still has {label}")

    masonry = re.search(
        r'id="home-gallery-masonry"[\s\S]*?</section>',
        html,
    )
    if masonry:
        block = masonry.group(0)
        for needle, label in (
            ("realism-tattoos-las-vegas-master-authority-guide", "guide screenshot in masonry"),
            ("jay-jay-artist-portfolio-authentic-masterpieces-las-vegas", "Jay page screenshot in masonry"),
        ):
            if needle in block:
                errors.append(f"still has {label}")

    kat_webp = ROOT / "artists" / "katelyn-cole" / (
        "katelyn-cole-professional-piercer-ear-curation-no-duplicates-las-vegas.webp"
    )
    kat_jpg = ROOT / "artists" / "katelyn-cole" / (
        "katelyn-cole-professional-piercer-ear-curation-no-duplicates-las-vegas.jpg"
    )
    if not kat_webp.is_file() or kat_webp.stat().st_size < 50_000:
        errors.append(f"Katelyn portrait webp missing or too small: {kat_webp}")
    if not kat_jpg.is_file() or kat_jpg.stat().st_size < 50_000:
        errors.append(f"Katelyn portrait jpg fallback missing or too small: {kat_jpg}")

    if errors:
        print("\n[verify] FAILED homepage checks:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        raise SystemExit(1)

    print(f"[verify] OK homepage ({size:,} bytes)")


def sync_root_home_copy() -> None:
    """Keep repo-root code.html aligned (some tools open it by mistake)."""
    ROOT_HTML.write_text(HOME_HTML.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"[sync] {ROOT_HTML.name} ← home export")


def main() -> int:
    for cmd in PIPELINE:
        run_step(cmd)

    stamp_build(HOME_HTML)
    sync_root_home_copy()
    run_step(["python3", str(ROOT / "tools" / "production_parity_cleanup.py")])
    sync_root_home_copy()
    verify_homepage()

    print(
        "\nReady for GitHub Pages deploy. Next:\n"
        "  git push origin HEAD:main\n"
        "GitHub Actions will build main, publish gh-pages, and verify WOA_BUILD_STAMP."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
