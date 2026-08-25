#!/usr/bin/env python3
"""Run enterprise SEO pipeline before deploy (safe — does not run prepare_site_deploy.py)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PIPELINE: list[str] = [
    "fix_studio_nap.py",
    "fix_studio_booking_email.py",
    "build_official_nap_page.py",
    "build_knowledge_hub.py",
    "build_start_here_hub.py",
    "build_geo_landing_pages.py",
    "build_piercing_authority_pages.py",
    "build_piercing_pillar_pages.py",
    "build_katelyn_piercing_authority_pages.py",
    "build_piercing_desert_aftercare_guide.py",
    "build_skin_science_pages.py",
    "inject_tattoo_seo_conversion.py",
    "build_artists_index_page.py",
    "enhance_artist_entity_pages.py",
    "fix_social_links.py",
    "inject_entity_schema.py",
    "fix_yoast_seo_meta.py",
    "inject_internal_links.py",
    "inject_contextual_links.py",
    "inject_sticky_book_cta.py",
    "update_image_alt_text.py",
    "fix_artist_roster_copy.py",
    ("inject_guides_hub.py", ("--refresh",)),
    "inject_guide_videos.py",
    "inject_guide_proof_strips.py",
    "tools/piercing_seo_inventory.py",
    "build_url_aliases.py",
    "build_studio_gallery_page.py",
    "inject_studio_portfolio.py",
    "fix_homepage_portfolio.py",
    "inject_homepage_welcome.py",
    "inject_homepage_healed_proof.py",
    "inject_sitewide_conversion.py",
    "inject_official_nap_links.py",
    "humanize_site_copy.py",
    "inject_google_tag_manager.py",
    "inject_mixpanel.py",
    "inject_ga4_conversions.py",
    "inject_robots_and_llms_discovery.py",
    "fix_homepage_seo.py",
    "fix_marketing_superlatives.py",
    "fix_social_links.py",
    "fix_studio_nap.py",
    "fix_yoast_seo_meta.py",
    "inject_entity_schema.py",
    "normalize_head_metadata.py",
    "fix_piercing_content_integrity.py",
]


def run(script: str, *extra_args: str) -> None:
    path = ROOT / script
    if not path.is_file():
        print(f"[skip] missing {script}")
        return
    cmd = [sys.executable, str(path), *extra_args]
    print(f"\n>>> {' '.join(cmd)}")
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    for entry in PIPELINE:
        if isinstance(entry, tuple):
            run(entry[0], *entry[1])
        else:
            run(entry)
    from woa_ai_crawl import write_ai_crawl_assets

    written = write_ai_crawl_assets(ROOT)
    print(f"\n[gen] crawl assets: {', '.join(p.name for p in written)}")
    print("\nSEO pipeline complete. Deploy with:")
    print("  FTP_USER='...' FTP_PASS='...' python3 deploy_stitch_site_root.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
