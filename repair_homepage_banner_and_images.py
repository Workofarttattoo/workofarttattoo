#!/usr/bin/env python3
"""Restore homepage studio banner and repair readability-broken <img> tags."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
CODE = HOME / "code.html"
ROOT_CODE = ROOT / "code.html"

WOA_HOME_CSS = '<link href="/home_work_of_art_tattoo_piercing/woa-home.css" rel="stylesheet"/>'

# Self-hosted fallbacks for homepage grids (dead Google AIDA bucket URLs).
HOSTED_POOL: list[str] = [
    "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-medusa-snakehair-realism-las-vegas.png",
    "/home_work_of_art_tattoo_piercing/client-portfolio/roaring-lion-tiger-forearm-realism-las-vegas.png",
    "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-skeleton-reaper-hand-realism-las-vegas.png",
    "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-thigh-realism-las-vegas.png",
    "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-statue-bust-cloth-drape-las-vegas.png",
    "/home_work_of_art_tattoo_piercing/client-portfolio/geometric-portrait-realism-sleeve-client-las-vegas.png",
    "/home_work_of_art_tattoo_piercing/client-portfolio/steampunk-clock-gears-rose-forearm-healed-las-vegas.png",
    "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-wings-script-angel-forearm-las-vegas.png",
    "/home_work_of_art_tattoo_piercing/client-portfolio/las-vegas-tattoo-artist-working-closeup.png",
    "/home_work_of_art_tattoo_piercing/joshua-cole-studio-interview-las-vegas.png",
]

GOOGLE_AIDA = re.compile(
    r"https://lh3\.googleusercontent\.com/aida/[^\"')\s<>]+"
)

# Readability pass broke alt/class when trimming ", Work of Art Tattoo & Piercing, Las Vegas".
BROKEN_GRID_IMG = re.compile(
    r'<img alt="([^"]*?), Work of Art class=" duration-500"="" grayscale="" '
    r'group-hover:grayscale-0="" h-full="" loading="lazy" object-cover="" '
    r'src="([^"]+)" transition-all="" w-full=""/>'
)

BROKEN_DISCOUNT_IMG = re.compile(
    r'<img 20="" alt="([^"]*?), Work of Art class=" border="" border-outline-variant="" '
    r'duration-500="" group-hover:scale-\[1\.02\]"="" loading="lazy" shadow-2xl="" '
    r'src="([^"]+)" transition-transform="" w-full=""/>'
)

BROKEN_PIERCING_IMG = re.compile(
    r'<img 5\]="" alt="([^"]*?), Work of Art class=" aspect-\[4="" duration-1000"="" '
    r'grayscale="" hover:grayscale-0="" loading="lazy" object-cover="" '
    r'src="([^"]+)" transition-all="" w-full=""/>'
)

BROKEN_EXPERIENCE_IMG = re.compile(
    r'<img alt="([^"]*?), Work of Art class=" h-full="" loading="lazy" object-cover"="" '
    r'src="([^"]+)" w-full=""/>'
)


def _load_banner_html() -> str:
    spec = importlib.util.spec_from_file_location(
        "fix_homepage_portfolio",
        ROOT / "fix_homepage_portfolio.py",
    )
    if spec is None or spec.loader is None:
        raise SystemExit("fix_homepage_portfolio.py not found")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.sync_banner()
    banner = mod.banner_hero_html()
    if not banner:
        raise SystemExit("Studio banner asset missing — add work_of_art_banner to assets/")
    return banner.strip()


def ensure_home_css(html: str) -> str:
    if "woa-home.css" in html:
        return html
    if WOA_HOME_CSS in html:
        return html
    marker = '<link href="/home_work_of_art_tattoo_piercing/woa-typography.css" rel="stylesheet"/>'
    if marker in html:
        return html.replace(marker, marker + "\n" + WOA_HOME_CSS, 1)
    return html.replace("</head>", f"{WOA_HOME_CSS}\n</head>", 1)


def ensure_banner(html: str, banner: str) -> str:
    if "WOA_HERO_BANNER_START" in html and "WOA_HERO_BANNER_END" in html:
        return re.sub(
            r"<!-- WOA_HERO_BANNER_START -->.*?<!-- WOA_HERO_BANNER_END -->",
            banner,
            html,
            count=1,
            flags=re.DOTALL,
        )
    if "WOA_HERO_BANNER_START" in html and "WOA_HOME_MASONRY_END" in html:
        return re.sub(
            r"<!-- WOA_HERO_BANNER_START -->[\s\S]*?<!-- WOA_HOME_MASONRY_END -->",
            banner,
            html,
            count=1,
        )
    anchor = "<!-- Hero Section -->"
    if anchor in html:
        return html.replace(anchor, banner + "\n" + anchor, 1)
    anchor = '<main class="relative z-10 woa-home-main">'
    if anchor in html:
        return html.replace(anchor, anchor + "\n" + banner, 1)
    return html


def fix_broken_img_tags(html: str) -> tuple[str, int]:
    fixes = 0

    def grid_repl(m: re.Match[str]) -> str:
        nonlocal fixes
        fixes += 1
        alt, src = m.group(1), m.group(2)
        return (
            f'<img alt="{alt}, Work of Art Tattoo &amp; Piercing" '
            f'class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500" '
            f'loading="lazy" src="{src}"/>'
        )

    def discount_repl(m: re.Match[str]) -> str:
        nonlocal fixes
        fixes += 1
        alt, src = m.group(1), m.group(2)
        return (
            f'<img alt="{alt}, Work of Art Tattoo &amp; Piercing" '
            f'class="w-full shadow-2xl border border-outline-variant/20 transition-transform duration-500 group-hover:scale-[1.02]" '
            f'loading="lazy" src="{src}"/>'
        )

    def piercing_repl(m: re.Match[str]) -> str:
        nonlocal fixes
        fixes += 1
        alt, src = m.group(1), m.group(2)
        return (
            f'<img alt="{alt}, Work of Art Tattoo &amp; Piercing" '
            f'class="w-full aspect-[4/5] object-cover grayscale hover:grayscale-0 transition-all duration-1000" '
            f'loading="lazy" src="{src}"/>'
        )

    def experience_repl(m: re.Match[str]) -> str:
        nonlocal fixes
        fixes += 1
        alt, src = m.group(1), m.group(2)
        return (
            f'<img alt="{alt}, Work of Art Tattoo &amp; Piercing" '
            f'class="w-full h-full object-cover" loading="lazy" src="{src}"/>'
        )

    html = BROKEN_GRID_IMG.sub(grid_repl, html)
    html = BROKEN_DISCOUNT_IMG.sub(discount_repl, html)
    html = BROKEN_PIERCING_IMG.sub(piercing_repl, html)
    html = BROKEN_EXPERIENCE_IMG.sub(experience_repl, html)
    return html, fixes


def swap_dead_google_urls(html: str) -> tuple[str, int]:
    urls = GOOGLE_AIDA.findall(html)
    if not urls:
        return html, 0
    seen: set[str] = set()
    swaps = 0
    pool_i = 0
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        replacement = HOSTED_POOL[pool_i % len(HOSTED_POOL)]
        pool_i += 1
        while not (ROOT / replacement.lstrip("/")).is_file() and pool_i < len(HOSTED_POOL) * 2:
            pool_i += 1
            replacement = HOSTED_POOL[pool_i % len(HOSTED_POOL)]
        if not (ROOT / replacement.lstrip("/")).is_file():
            continue
        count = html.count(url)
        if count:
            html = html.replace(url, replacement)
            swaps += count
    return html, swaps


def repair_html(html: str, banner: str) -> tuple[str, dict[str, int]]:
    stats = {"img_tag_fixes": 0, "google_swaps": 0, "banner": 0, "css": 0}
    before_css = html
    html = ensure_home_css(html)
    if html != before_css:
        stats["css"] = 1

    before_banner = html
    html = ensure_banner(html, banner)
    if html != before_banner:
        stats["banner"] = 1

    html, img_fixes = fix_broken_img_tags(html)
    stats["img_tag_fixes"] = img_fixes

    html, google_swaps = swap_dead_google_urls(html)
    stats["google_swaps"] = google_swaps

    return html, stats


def main() -> int:
    banner = _load_banner_html()
    for path in (CODE, ROOT_CODE):
        if not path.is_file():
            continue
        html = path.read_text(encoding="utf-8")
        repaired, stats = repair_html(html, banner)
        path.write_text(repaired, encoding="utf-8")
        print(f"[repair] {path.relative_to(ROOT)}")
        for key, val in stats.items():
            if val:
                print(f"  {key}: {val}")

    if 'Work of Art class="' in CODE.read_text(encoding="utf-8"):
        print("[warn] Some corrupted <img> tags remain — inspect homepage manually.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
