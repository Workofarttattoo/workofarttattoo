#!/usr/bin/env python3
"""Restore Katelyn Cole's proper standing portfolio portrait site-wide.

Replaces Stitch page-screenshot crops and any sideways/wrong assets with the
canonical titled portrait (Katelyn Cole — Body Piercer) used in the original
artist export.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
KATELYN_PORTRAIT_URL = (
    "https://lh3.googleusercontent.com/aida-public/AB6AXuCpVfsrMxJ1TWFUawXyhLtweBHXX3mhmXiFPwxsM8bzwk-8ZIoREIuqUdMp-H_E18mXBuVwTkcUFgz7cHDdioWMBwQY5ZwpRoyhqMHu2gbUtK4jUmUO-qFqtCxylY-MqKHWa4Z_3hH_qzzIAz5ZDYNqqY5mZ8HeFMeYyslycUgdoxofrPBPbpPMIKiXU3AMryCruXwB17mjGRnNU7VRVnAPOttEqBWlTQSTe28PbC7u8vZ0RySTUEr4gTV0V_cTkAuFOvihP6p8BqY9"
)
FILENAME = "katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas"
# JPEG fallback: Bluehost often rewrites large .png uploads to WebP at the same path.
JPG_NAME = f"{FILENAME}.jpg"
CARD_W = 800
CARD_H = 1067

DEST_DIRS = (
    ROOT / "artists" / "katelyn-cole",
    ROOT / "katelyn_cole_master_body_piercer_ear_curation_no_duplicates",
)

KATELYN_PAGE = ROOT / "artists_build" / "katelyn-cole.html"

KATELYN_HERO_PICTURE = (
    '<picture><source srcset="/artists/katelyn-cole/'
    f'{FILENAME}.webp" type="image/webp"/>'
    '<img alt="Katelyn Cole — master body piercer Las Vegas — Work of Art Tattoo &amp; Piercing" '
    'class="w-full aspect-[3/4] md:aspect-[4/5] object-cover object-top" decoding="async" '
    f'fetchpriority="high" height="{CARD_H}" loading="eager" '
    f'src="/artists/katelyn-cole/{JPG_NAME}" width="{CARD_W}"/></picture>'
)

LION_HERO_RE = re.compile(
    r"<picture><source srcset=\"/home_work_of_art_tattoo_piercing/client-portfolio/"
    r"black-grey-lion-realism-thigh-client-photo-las-vegas\.webp\"[^>]*>.*?"
    r"black-grey-lion-realism-thigh-client-photo-las-vegas\.png\"[^>]*/></picture>",
    re.I | re.S,
)


def curl_download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["curl", "-sfL", url, "-o", str(dest)],
            check=True,
            capture_output=True,
            timeout=120,
        )
        return dest.is_file() and dest.stat().st_size > 500
    except (subprocess.CalledProcessError, OSError):
        return False


def save_portrait(src: Path) -> tuple[int, int]:
    im = ImageOps.exif_transpose(Image.open(src))
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    im = ImageOps.fit(
        im,
        (CARD_W, CARD_H),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.35),
    )
    artists_dir = ROOT / "artists" / "katelyn-cole"
    artists_dir.mkdir(parents=True, exist_ok=True)
    webp = artists_dir / f"{FILENAME}.webp"
    jpg = artists_dir / f"{JPG_NAME}"
    im.save(webp, "WEBP", quality=86, method=6)
    im.save(jpg, "JPEG", quality=88, optimize=True)
    print(f"[portrait] {webp.relative_to(ROOT)} ({CARD_W}x{CARD_H})")
    print(f"[portrait] {jpg.relative_to(ROOT)} ({jpg.stat().st_size:,} bytes)")
    return CARD_W, CARD_H


def fix_katelyn_page_hero() -> bool:
    if not KATELYN_PAGE.is_file():
        print(f"[skip] missing {KATELYN_PAGE}")
        return False
    html = KATELYN_PAGE.read_text(encoding="utf-8")
    changed = False

    new_html, n = LION_HERO_RE.subn(KATELYN_HERO_PICTURE, html, count=1)
    if n:
        html = new_html
        changed = True
        print("[hero] katelyn-cole.html — replaced lion tattoo with Katelyn portrait")

    schema_old = (
        '"image": "url(/home_work_of_art_tattoo_piercing/client-portfolio/'
        'black-grey-lion-realism-thigh-client-photo-las-vegas.webp)",'
    )
    schema_new = f'"image": "https://workofarttattoo.com/artists/katelyn-cole/{FILENAME}.webp",'
    if schema_old in html:
        html = html.replace(schema_old, schema_new)
        changed = True
        print("[schema] katelyn-cole.html — LocalBusiness image")

    if changed:
        KATELYN_PAGE.write_text(html, encoding="utf-8")
    return changed


def patch_img_dims(html: str, rel: str, w: int, h: int) -> str:
    esc = re.escape(rel)

    def repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        tag = re.sub(r'\s*width="[^"]*"', "", tag)
        tag = re.sub(r'\s*height="[^"]*"', "", tag)
        return tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)

    return re.sub(rf'<img\s[^>]*\ssrc="/{esc}"[^>]*>', repl, html, flags=re.I)


def use_jpg_img_fallback(html: str) -> str:
    """Point portrait references at JPEG (host rewrites .png to WebP on the server)."""
    png_src = f"/artists/katelyn-cole/{FILENAME}.png"
    jpg_src = f"/artists/katelyn-cole/{JPG_NAME}"
    if png_src not in html:
        return html
    return html.replace(png_src, jpg_src)


def patch_html_dims() -> int:
    rel = f"artists/katelyn-cole/{JPG_NAME}"
    n = 0
    for path in ROOT.rglob("*.html"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        new_text = use_jpg_img_fallback(text)
        if f"/{rel}" in new_text or f"artists/katelyn-cole/{FILENAME}" in new_text:
            new_text = patch_img_dims(new_text, rel, CARD_W, CARD_H)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            n += 1
            print(f"[jpg-src] {path.relative_to(ROOT)}")
    return n


def main() -> int:
    tmp = ROOT / ".katelyn-portrait-source.png"
    if not curl_download(KATELYN_PORTRAIT_URL, tmp):
        raise SystemExit("Failed to download canonical Katelyn portrait.")
    save_portrait(tmp)
    tmp.unlink(missing_ok=True)
    fix_katelyn_page_hero()
    patch_html_dims()
    print("Done. Re-run: python3 inject_client_videos.py && python3 deploy_stitch_site_root.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
