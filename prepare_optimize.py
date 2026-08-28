#!/usr/bin/env python3
"""Optimize existing content (no new articles) — humanize copy, EEAT, schema, links."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PIPELINE: list[str] = [
    "build_tattoo_healing_before_after_page.py",
    "build_healed_gallery_pages.py",
    "build_real_client_timeline_page.py",
    "build_healing_database_pages.py",
    "build_joshua_oil_painting_tattoo_aging_page.py",
    "build_flash_art_deals_page.py",
    "build_studio_gallery_page.py",
    "build_offsite_bookings_page.py",
    "audit_gallery_image_alts.py",
    "inject_studio_portfolio.py",
    "humanize_site_copy.py",
    "inject_contextual_portfolio.py",
    "inject_service_proof_blocks.py",
    "inject_guide_proof_strips.py",
    "optimize_reviews_vault.py",
    "enhance_artist_entity_pages.py",
    "inject_entity_schema.py",
    "inject_contextual_links.py",
    "inject_internal_links.py",
    "fix_studio_nap.py",
    "fix_studio_booking_email.py",
    "update_image_alt_text.py",
]


def run(script: str) -> None:
    path = ROOT / script
    if not path.is_file():
        print(f"[skip] missing {script}")
        return
    print(f"\n>>> python3 {script}")
    subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)


def main() -> int:
    for script in PIPELINE:
        run(script)
    print("\nOptimize pipeline complete. Deploy with:")
    print("  FTP_HOST=workofarttattoo.com FTP_USER='...' FTP_PASS='...' python3 deploy_stitch_site_root.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
