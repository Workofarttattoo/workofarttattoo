#!/usr/bin/env python3
"""Phase 9 checks against generated production HTML (not only sources)."""

from __future__ import annotations

import shutil
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".github", "tools", "audits", "skipped_upload_build", "artists_raw"}

BANNED_HOME = [
    "Two resident specialists",
    "2 In-Studio Specialists",
    "Joshua Cole and Joshua Cole",
    "hospital-level",
    "Hospital-grade",
    "museum-level",
    "museum-quality",
    "elite artistry",
    "clinical standards",
    "clinical precision",
    "cleanest environment in Las Vegas",
    "master piercer",
    "medical-grade hygiene",
]
GMAILS = ("thewhiteknight702@gmail.com", "kmorgen14@gmail.com")
REQUIRED = [
    "index.html",
    "merchandise/index.html",
    "artists/teralyn/index.html",
    "cover-up-tattoos-las-vegas/index.html",
]


def generate_index_copies() -> None:
    for code in ROOT.rglob("code.html"):
        if any(part in SKIP or part == "node_modules" for part in code.parts):
            continue
        shutil.copy2(code, code.with_name("index.html"))
    mappings = {
        ROOT / "artists_build/katelyn-cole.html": ROOT / "artists/katelyn-cole/index.html",
        ROOT / "artists_build/joshua-cole.html": ROOT / "artists/joshua-cole/index.html",
        ROOT / "artists_build/teralyn.html": ROOT / "artists/teralyn/index.html",
    }
    for src, dst in mappings.items():
        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    home_src = None
    for candidate in (
        ROOT / "code.html",
        ROOT / "index.html",
        ROOT / "home_work_of_art_tattoo_piercing" / "code.html",
    ):
        if not candidate.is_file():
            continue
        text = candidate.read_text(encoding="utf-8", errors="replace")
        if "woa-hero-banner" in text and "work-of-art-studio-banner-las-vegas" in text:
            home_src = candidate
            break
    if home_src is None:
        raise SystemExit("No homepage source with studio banner found")
    shutil.copy2(home_src, ROOT / "index.html")
    print(f"Homepage source: {home_src.relative_to(ROOT)}")


def main() -> int:
    generate_index_copies()
    errors: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing {rel}")

    home = (ROOT / "index.html").read_text(encoding="utf-8", errors="replace")
    for marker in ("<<<<<<<", "=======", ">>>>>>>"):
        if marker in home:
            errors.append(f"homepage conflict marker {marker}")
    if "Teralyn" not in home:
        errors.append("homepage missing Teralyn")
    if "/artists/teralyn/" not in home:
        errors.append("homepage missing Teralyn nav href")
    if not any(
        s in home
        for s in (
            "3 In-Studio Residents",
            "Three in-studio residents",
            "3 current in-studio residents",
        )
    ):
        errors.append("homepage missing 3-resident wording")
    if "booking@workofarttattoo.com" not in home:
        errors.append("homepage missing booking@")
    for phrase in BANNED_HOME:
        if phrase.lower() in home.lower():
            errors.append(f"homepage banned: {phrase}")

    nap_footer_count = len(
        __import__("re").findall(
            r'<div class="mt-10 pt-8 border-t border-outline-variant/10 max-w-3xl"[^>]*>\s*'
            r'<h5[^>]*>Studio</h5>\s*'
            r'<p class="mt-3 text-on-surface-variant[^"]*"[^>]*>Work of Art Tattoo &amp; Piercing<br/>2375 E\. Tropicana',
            home,
            flags=__import__("re").I,
        )
    )
    if nap_footer_count > 1:
        errors.append(
            f"homepage has {nap_footer_count} duplicate Studio NAP footer blocks; expected 1"
        )

    cover = (ROOT / "cover-up-tattoos-las-vegas" / "index.html")
    legacy = ROOT / "cover_up_tattoos_las_vegas_master_authority_guide" / "index.html"
    if cover.is_file():
        cover_html = cover.read_text(encoding="utf-8", errors="replace")
        if "noindex" in cover_html.lower():
            errors.append("canonical cover-up page is noindex")
        if 'http-equiv="refresh"' in cover_html.lower():
            errors.append("canonical cover-up page has meta refresh")
        if 'rel="canonical"' not in cover_html:
            errors.append("canonical cover-up page missing self-referencing canonical")
    if legacy.is_file():
        legacy_html = legacy.read_text(encoding="utf-8", errors="replace")
        if "noindex" not in legacy_html.lower():
            errors.append("legacy cover-up page missing noindex")
        if 'http-equiv="refresh"' not in legacy_html.lower():
            errors.append("legacy cover-up page missing meta refresh")

    for path in ROOT.rglob("*.html"):
        if any(part in SKIP for part in path.parts):
            continue
        body = path.read_text(encoding="utf-8", errors="replace")
        for gmail in GMAILS:
            if gmail in body:
                errors.append(f"{path.relative_to(ROOT)} has {gmail}")
        if 'href="/cover_up_tattoos_las_vegas_master_authority_guide/"' in body:
            errors.append(f"{path.relative_to(ROOT)} links to legacy cover-up URL")
        if "Southern Nevada Health District body art establishment Health Permit" in body:
            errors.append(f"{path.relative_to(ROOT)} has SNHD permit claim")

    broken = Counter()
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP for part in path.parts):
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        for a in soup.find_all("a", href=True):
            href = (a.get("href") or "").strip()
            if not href.startswith("/") or href.startswith("//"):
                continue
            target = urlsplit(href).path
            if target in ("", "/"):
                continue
            rel = target.lstrip("/")
            if not any((ROOT / c).exists() for c in (rel, f"{rel}/index.html", f"{rel}index.html")):
                broken[target] += 1
    severe = [(u, n) for u, n in broken.items() if n >= 5]
    if severe:
        errors.append(
            "repeated broken internal links: "
            + ", ".join(f"{u} ({n})" for u, n in sorted(severe)[:20])
        )
    print(f"Broken unique internal targets: {len(broken)}")
    for target, count in broken.most_common(15):
        print(f"  {count:4d} {target}")

    if errors:
        print("FAIL")
        for err in errors[:80]:
            print(" -", err)
        if len(errors) > 80:
            print(f" ... +{len(errors) - 80} more")
        return 1
    print("PASS production parity verify")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
