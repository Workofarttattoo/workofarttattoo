#!/usr/bin/env python3
"""Remove non-studio butterfly assets site-wide; use black & grey lion thigh instead."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_PARTS = frozenset({".git", "__pycache__", "node_modules", "skipped_upload_build"})

LION_STEM = "black-grey-lion-thigh-realism-las-vegas"
LION_PNG = f"/home_work_of_art_tattoo_piercing/client-portfolio/{LION_STEM}.png"
LION_WEBP = f"/home_work_of_art_tattoo_piercing/client-portfolio/{LION_STEM}.webp"
LION_OG = f"https://www.workofarttattoo.com{LION_WEBP}"

BUTTERFLY_ASSET_GLOBS = (
    "**/color-butterfly-back-tattoo-las-vegas.*",
    "**/realism-tattoos-color-butterfly-and-floral-coverup.*",
)

BUTTERFLY_PATTERNS: tuple[tuple[str, str], ...] = (
    ("color-butterfly-back-tattoo-las-vegas", LION_STEM),
    ("realism-tattoos-color-butterfly-and-floral-coverup", LION_STEM),
    (
        "img_0279.jpeg/realism-tattoos-color-butterfly-and-floral-coverup",
        f"home_work_of_art_tattoo_piercing/client-portfolio/{LION_STEM}",
    ),
    (f"{LION_STEM}.webp.png", f"{LION_STEM}.png"),
)

TEXT_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    (
        "Realisms - Color Butterfly and Floral Coverup, Work of Art Tattoo &amp; Piercing",
        "Black and grey skeleton reaper hand realism — Work of Art Tattoo Las Vegas",
    ),
    (
        "Cover up tattoo Las Vegas — floral butterfly cover-up transformation, Work of Art Tattoo &amp; Piercing",
        "Cover up tattoo Las Vegas — black and grey lion thigh realism, Work of Art Tattoo",
    ),
    (
        "Healed cover up tattoo Las Vegas — color butterfly floral",
        "Healed cover up tattoo Las Vegas — black and grey lion thigh realism",
    ),
    ("Color realism butterfly and floral cover-up tattoo Las Vegas", LION_STEM.replace("-", " ").title()),
    ("butterfly-and-floral-cover", LION_STEM),
    ("Color Butterfly and Floral Coverup", "Black and grey skeleton reaper hand realism"),
    ("floral butterfly cover-up", "black and grey lion thigh realism cover-up"),
    ("color butterfly floral", "black and grey lion thigh realism"),
)

LION_THIGH_TILE = (
    '<a class="woa-curated-tile group" href="/#portfolio">'
    f'<picture><source srcset="{LION_WEBP}" type="image/webp"/>'
    f'<img alt="Black and grey lion thigh realism tattoo — Work of Art Tattoo Las Vegas" '
    f'class="w-full h-full object-cover object-center" decoding="async" height="800" loading="lazy" '
    f'src="{LION_PNG}" width="800"/></picture>'
    "<span>Lion Thigh Realism (Client)</span></a>"
)

EMPTY_LION_TILE = (
    '<a class="woa-curated-tile group" href="/#portfolio">'
    "<span>Lion Thigh Realism (Client)</span></a>"
)

BUTTERFLY_ALT = re.compile(r'alt="[^"]*\bbutterfly\b[^"]*"', re.I)


def swap_butterfly_paths(text: str) -> tuple[str, int]:
    n = 0
    for old, new in BUTTERFLY_PATTERNS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            n += count
    return text, n


def scrub_butterfly_alt(text: str) -> tuple[str, int]:
    """Replace any remaining alt text that still mentions butterfly."""
    fixes = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal fixes
        fixes += 1
        if "cover" in match.group(0).lower():
            return (
                'alt="Cover up tattoo Las Vegas — black and grey lion thigh realism, '
                'Work of Art Tattoo &amp; Piercing"'
            )
        return (
            'alt="Black and grey lion thigh realism tattoo — Work of Art Tattoo Las Vegas"'
        )

    text = BUTTERFLY_ALT.sub(repl, text)
    for old, new in TEXT_REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            fixes += count
    return text, fixes


def fix_curated_first_tile(text: str) -> tuple[str, int]:
    fixes = 0
    if EMPTY_LION_TILE in text:
        count = text.count(EMPTY_LION_TILE)
        text = text.replace(EMPTY_LION_TILE, LION_THIGH_TILE)
        fixes += count

    broken_lead = re.compile(
        r'<span>Lion Thigh Realism \(Client\)</span>\s*(?:</a>\s*)?'
        r'(?=<a class="woa-curated-tile group")'
    )
    text, n = broken_lead.subn(LION_THIGH_TILE, text)
    fixes += n

    if '<div class="my-12">' in text and "woa-curated-tile group" in text:
        text, n = re.subn(
            r'(<div class="my-12">)\s*(<a class="woa-curated-tile group")',
            r'\1\n<div class="woa-curated-grid">\n\2',
            text,
            count=1,
        )
        if n:
            fixes += n
            text = re.sub(
                r'(<span>Money Rose Realism</span></a>)(</div>\s*<p class="text-center pt-4">)',
                r"\1</div>\2",
                text,
                count=1,
            )

    return text, fixes


def patch_file(path: Path) -> dict[str, int]:
    raw = path.read_text(encoding="utf-8")
    text, path_swaps = swap_butterfly_paths(raw)
    text, alt_fixes = scrub_butterfly_alt(text)
    text, tile_fixes = fix_curated_first_tile(text)
    if text != raw:
        path.write_text(text, encoding="utf-8")
    return {"path_swaps": path_swaps, "alt_fixes": alt_fixes, "tile_fixes": tile_fixes}


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        out.append(path)
    return out


def patch_python_defaults() -> None:
    for rel in (
        "fix_yoast_seo_meta.py",
        "build_cover_up_authority_page.py",
        "repair_homepage_banner_and_images.py",
        "update_image_alt_text.py",
        "expand_homepage_conversion.py",
    ):
        path = ROOT / rel
        if not path.is_file():
            continue
        t = path.read_text(encoding="utf-8")
        for old, new in BUTTERFLY_PATTERNS:
            t = t.replace(old, new)
        for old, new in TEXT_REPLACEMENTS:
            t = t.replace(old, new)
        t = t.replace(
            'COVER_IMG = "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-thigh-realism-las-vegas.webp"',
            'COVER_STEM = "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-thigh-realism-las-vegas"\n'
            'COVER_IMG = COVER_STEM',
        )
        t = t.replace('src="{COVER_IMG}.png"', 'src="{COVER_STEM}.png"')
        path.write_text(t, encoding="utf-8")
        print(f"[py] {rel}")


def delete_butterfly_assets() -> int:
    removed = 0
    for pattern in BUTTERFLY_ASSET_GLOBS:
        for path in ROOT.glob(pattern):
            if not path.is_file():
                continue
            path.unlink()
            removed += 1
            print(f"[del] {path.relative_to(ROOT)}")
    return removed


def main() -> int:
    stats = {"files": 0, "path_swaps": 0, "alt_fixes": 0, "tile_fixes": 0}
    for path in iter_html_files():
        s = patch_file(path)
        if s["path_swaps"] or s["alt_fixes"] or s["tile_fixes"]:
            stats["files"] += 1
            stats["path_swaps"] += s["path_swaps"]
            stats["alt_fixes"] += s["alt_fixes"]
            stats["tile_fixes"] += s["tile_fixes"]
            print(
                f"[ok] {path.relative_to(ROOT)} "
                f"swaps={s['path_swaps']} alt={s['alt_fixes']} tiles={s['tile_fixes']}"
            )

    patch_python_defaults()
    deleted = delete_butterfly_assets()
    print(
        f"\nDone: {stats['files']} HTML file(s), "
        f"{stats['path_swaps']} path swap(s), {stats['alt_fixes']} alt fix(es), "
        f"{stats['tile_fixes']} tile fix(es), {deleted} asset(s) deleted."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
