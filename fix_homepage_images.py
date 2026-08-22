#!/usr/bin/env python3
"""Replace sideways / missing homepage images with vertical portrait assets."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
HOME_HTML = HOME / "code.html"
ROOT_HTML = ROOT / "code.html"
PORTFOLIO = HOME / "client-portfolio"
HERO_DIR = HOME / "hero-premium"
SITE = "https://www.workofarttattoo.com"

CARD_W = 1200
CARD_H = 1600
ARTIST_W = 800
ARTIST_H = 1067

KATELYN_PORTRAIT_URL = (
    "https://lh3.googleusercontent.com/aida-public/AB6AXuCpVfsrMxJ1TWFUawXyhLtweBHXX3mhmXiFPwxsM8bzwk-8ZIoREIuqUdMp-H_E18mXBuVwTkcUFgz7cHDdioWMBwQY5ZwpRoyhqMHu2gbUtK4jUmUO-qFqtCxylY-MqKHWa4Z_3hH_qzzIAz5ZDYNqqY5mZ8HeFMeYyslycUgdoxofrPBPbpPMIKiXU3AMryCruXwB17mjGRnNU7VRVnAPOttEqBWlTQSTe28PbC7u8vZ0RySTUEr4gTV0V_cTkAuFOvihP6p8BqY9"
)
JOSHUA_PORTRAIT_URL = (
    "https://lh3.googleusercontent.com/aida-public/AB6AXuBfGjuOBG0vVOPkw6TmhOZSHl07XFtjuEk5Xt7w6b4U4n2VkifK7lsH6e54zRSkQgj-BgZwBYGOkYhs43EHjcBswi-k2WZ1jwW_ASvw6QzVXjDIbbRorXfQ_MgjOOmXq-RWpJ530DfbAN3xVqnGmCY6AlEaPXb-1XGN1XUO0MBRHBiPqQXyhf7t0NR6KAVaSFY3vVCm46rZkH-7Uts1rq9mvJpDYlAu78uH1tXA0hmKwoDgoMC0ZTXM415HuVjJVIBtOOos1KfoL1Ge"
)

HERO_FILES = [
    "hero-woman-skull-skeletal-hand-forearm-realism",
    "hero-roaring-lion-tiger-forearm-realism",
    "hero-realistic-eye-triangle-square-las-vegas",
    "hero-archangel-michael-demon-upper-arm-realism",
    "hero-lion-clock-realism-shoulder-tattoo",
    "hero-lion-thigh-realism-las-vegas",
    "hero-medusa-snake-hair-forearm-realism",
]


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


def is_bad_asset(path: Path) -> bool:
    if not path.is_file():
        return True
    try:
        im = ImageOps.exif_transpose(Image.open(path))
    except OSError:
        return True
    w, h = im.size
    if w < 600 and h / max(w, 1) >= 3:
        return True
    if h / max(w, 1) >= 4 and h >= 3000:
        return True
    if w > h * 1.1:
        return True
    return False


def portrait_pool() -> list[Path]:
    pool: list[Path] = []
    patterns = [
        "cover_up_tattoos_las_vegas_master_authority_guide/*.png",
        "img_*.jpeg/*.png",
        "how_much_do_tattoos_cost_in_las_vegas_authority_guide/*.png",
        "fine_line_tattoos_las_vegas_master_authority_guide/*.png",
        "realism_tattoos_las_vegas_master_authority_guide/*.png",
        "reviews_vault_100_verified_masterpieces/*.png",
    ]
    seen: set[str] = set()
    for pat in patterns:
        for p in sorted(ROOT.glob(pat)):
            if "texture" in p.name.lower() or p.name.startswith("."):
                continue
            key = str(p.resolve())
            if key in seen:
                continue
            try:
                im = ImageOps.exif_transpose(Image.open(p))
            except OSError:
                continue
            w, h = im.size
            if h < w * 1.05:
                continue
            if w < 500:
                continue
            seen.add(key)
            pool.append(p)
    return pool


def save_portrait(src: Path, dest: Path, *, out_w: int = CARD_W, out_h: int = CARD_H) -> tuple[int, int]:
    im = ImageOps.exif_transpose(Image.open(src))
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    im = ImageOps.fit(im, (out_w, out_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "PNG", optimize=True)
    webp = dest.with_suffix(".webp")
    im.save(webp, "WEBP", quality=82, method=6)
    return im.size


def save_artist_portrait(src: Path, dest: Path) -> tuple[int, int]:
    return save_portrait(src, dest, out_w=ARTIST_W, out_h=ARTIST_H)


def portfolio_refs(html: str) -> list[str]:
    stems: list[str] = []
    for m in re.finditer(r"/home_work_of_art_tattoo_piercing/client-portfolio/([a-z0-9-]+)\.(?:png|webp)", html):
        if m.group(1) not in stems:
            stems.append(m.group(1))
    return stems


def patch_img_dims(html: str, rel_path: str, w: int, h: int) -> str:
    esc = re.escape(rel_path)

    def repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        tag = re.sub(r'\s*width="[^"]*"', "", tag)
        tag = re.sub(r'\s*height="[^"]*"', "", tag)
        return tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)

    return re.sub(
        rf'<img\s[^>]*\ssrc="/{esc}"[^>]*>',
        repl,
        html,
        flags=re.I,
    )


def fix_client_portfolio(html: str) -> str:
    PORTFOLIO.mkdir(parents=True, exist_ok=True)
    pool = portrait_pool()
    if not pool:
        raise SystemExit("No vertical portrait pool images found in repo.")
    pi = 0
    for stem in portfolio_refs(html):
        dest = PORTFOLIO / f"{stem}.png"
        if not is_bad_asset(dest):
            with Image.open(dest) as im:
                w, h = im.size
            html = patch_img_dims(html, f"home_work_of_art_tattoo_piercing/client-portfolio/{stem}.png", w, h)
            continue
        src = pool[pi % len(pool)]
        pi += 1
        w, h = save_portrait(src, dest)
        print(f"[portfolio] {stem}.png ← {src.relative_to(ROOT)} ({w}x{h})")
        html = patch_img_dims(html, f"home_work_of_art_tattoo_piercing/client-portfolio/{stem}.png", w, h)
    return html


def fix_hero_premium() -> int:
    HERO_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for stem in HERO_FILES:
        dest = HERO_DIR / f"{stem}.png"
        if dest.is_file() and not is_bad_asset(dest):
            continue
        url = f"{SITE}/home_work_of_art_tattoo_piercing/hero-premium/{stem}.png"
        tmp = HERO_DIR / f".{stem}.download.png"
        if curl_download(url, tmp):
            shutil.move(tmp, dest)
            with Image.open(dest) as im:
                w, h = im.size
            webp = dest.with_suffix(".webp")
            ImageOps.exif_transpose(Image.open(dest)).save(webp, "WEBP", quality=82, method=6)
            print(f"[hero] {stem}.png ({w}x{h}) from live")
            n += 1
        elif stem == "hero-woman-skull-skeletal-hand-forearm-realism":
            src = ROOT / "cover_up_tattoos_las_vegas_master_authority_guide" / "healed-realism-seraphim-eye-wings-tattoo.png"
            if src.is_file():
                im = ImageOps.exif_transpose(Image.open(src))
                im = im.resize((2400, 1800), Image.Resampling.LANCZOS)
                im.save(dest, "PNG", optimize=True)
                im.save(dest.with_suffix(".webp"), "WEBP", quality=82, method=6)
                print(f"[hero] {stem}.png from cover_up fallback")
                n += 1
    return n


def fix_artist_roster() -> None:
    joshua_dir = ROOT / "artists" / "joshua-cole"
    katelyn_dir = ROOT / "artists" / "katelyn-cole"
    joshua_dir.mkdir(parents=True, exist_ok=True)
    katelyn_dir.mkdir(parents=True, exist_ok=True)

    joshua_dest = joshua_dir / "joshua-cole-portrait-las-vegas.png"
    if is_bad_asset(joshua_dest):
        tmp = joshua_dir / ".joshua-dl.png"
        if curl_download(JOSHUA_PORTRAIT_URL, tmp):
            save_artist_portrait(tmp, joshua_dest)
            tmp.unlink(missing_ok=True)
            print("[artist] joshua-cole-portrait from Google")
        else:
            closeup = HOME / "las-vegas-tattoo-artist-working-closeup.png"
            if closeup.is_file():
                save_artist_portrait(closeup, joshua_dest)
                print("[artist] joshua-cole-portrait from studio closeup")

    katelyn_dest = katelyn_dir / "katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas.png"
    if is_bad_asset(katelyn_dest):
        tmp = katelyn_dir / ".katelyn-dl.png"
        if curl_download(KATELYN_PORTRAIT_URL, tmp):
            save_artist_portrait(tmp, katelyn_dest)
            tmp.unlink(missing_ok=True)
            print("[artist] katelyn portrait from Google")


def fix_featured_snake() -> None:
    dest = HOME / "custom-tattoos-las-vegas-epic-snake-black-and-grey-realism.png"
    if is_bad_asset(dest):
        src = ROOT / "cover_up_tattoos_las_vegas_master_authority_guide" / "black-grey-realism-snake-sleeve-tattoo.png"
        save_portrait(src, dest)


def main() -> int:
    fix_hero_premium()
    fix_featured_snake()
    fix_artist_roster()

    for path in (HOME_HTML, ROOT_HTML):
        if not path.is_file():
            continue
        html = path.read_text(encoding="utf-8")
        html = fix_client_portfolio(html)
        w, h = Image.open(HOME / "custom-tattoos-las-vegas-epic-snake-black-and-grey-realism.png").size
        html = patch_img_dims(
            html,
            "home_work_of_art_tattoo_piercing/custom-tattoos-las-vegas-epic-snake-black-and-grey-realism.png",
            w,
            h,
        )
        path.write_text(html, encoding="utf-8")
        print(f"[html] {path.relative_to(ROOT)}")

    print("Done. Run: python3 inject_client_videos.py  &&  deploy_stitch_site_root.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
