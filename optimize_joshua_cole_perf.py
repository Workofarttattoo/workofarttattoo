#!/usr/bin/env python3
"""Download Joshua Cole page images, emit WebP, patch artists_build/joshua-cole.html."""

from __future__ import annotations

import hashlib
import re
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "artists_build" / "joshua-cole.html"
ASSETS = ROOT / "artists_joshua_cole_assets"
HERO_WEBP = (
    "/joshua_cole_masterpiece_wall_consistently_unique/"
    "joshua-cole-tattooing-portrait-las-vegas.webp"
)
MAX_GALLERY_W = 700
QUALITY = 82


def slug_from_url(url: str) -> str:
    h = hashlib.sha256(url.encode()).hexdigest()[:10]
    return f"joshua-gallery-{h}"


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def to_webp(src: Path, dest: Path, max_w: int) -> tuple[int, int]:
    with Image.open(src) as im:
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        w, h = im.size
        if w > max_w:
            nh = max(1, int(h * max_w / w))
            im = im.resize((max_w, nh), Image.Resampling.LANCZOS)
            w, h = im.size
        im.save(dest, "WEBP", quality=QUALITY, method=6)
    return w, h


def picture_tag(webp_path: str, alt: str, w: int, h: int, *, lazy: bool, high: bool) -> str:
    attrs = [
        f'width="{w}"',
        f'height="{h}"',
        f'alt="{alt}"',
        'class="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-500"',
        'decoding="async"',
    ]
    if lazy:
        attrs.append('loading="lazy"')
    if high:
        attrs.append('fetchpriority="high"')
    img = f'<img {" ".join(attrs)} src="{webp_path}"/>'
    return f'<picture><source srcset="{webp_path}" type="image/webp"/>{img}</picture>'


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    urls = sorted(set(re.findall(r"https://lh3\.googleusercontent\.com/[^\"')\s]+", html)))
    mapping: dict[str, str] = {}
    dims: dict[str, tuple[int, int]] = {}

    for url in urls:
        if "AB6AXuBAeI1Ddzsi6g7RlVQzroDGqUo04" in url:
            continue
        slug = slug_from_url(url)
        raw = ASSETS / f"{slug}.jpg"
        webp = ASSETS / f"{slug}.webp"
        if not webp.is_file():
            print(f"download {slug}…")
            download(url, raw)
            dims[url] = to_webp(raw, webp, MAX_GALLERY_W)
            raw.unlink(missing_ok=True)
        else:
            with Image.open(webp) as im:
                dims[url] = im.size
        mapping[url] = f"/artists_joshua_cole_assets/{slug}.webp"

    for url, path in mapping.items():
        html = html.replace(url, path)

    hero_dims = (496, 512)
    hero_alt = (
        "Joshua Cole Master Tattoo Artist Las Vegas, Work of Art Tattoo &amp; Piercing, Las Vegas"
    )
    hero_old = re.search(
        r'<img alt="Joshua Cole Master Tattoo Artist[^"]*"[^>]*src="[^"]+"[^>]*/>',
        html,
    )
    if hero_old:
        hero_new = picture_tag(
            HERO_WEBP,
            hero_alt,
            hero_dims[0],
            hero_dims[1],
            lazy=False,
            high=True,
        ).replace(
            "duration-500",
            "duration-1000 ease-in-out transform hover:scale-110",
        )
        html = html.replace(hero_old.group(0), hero_new)

    for url, path in mapping.items():
        w, h = dims[url]
        pattern = rf'<img([^>]*src="{re.escape(path)}"[^>]*)/>'
        def repl(m: re.Match[str]) -> str:
            tag = m.group(1)
            if "width=" not in tag:
                tag += f' width="{w}" height="{h}"'
            if 'loading="lazy"' not in tag:
                tag += ' loading="lazy" decoding="async"'
            return f"<picture><source srcset=\"{path}\" type=\"image/webp\"/><img{tag}/></picture>"
        html = re.sub(pattern, repl, html)

    HTML.write_text(html, encoding="utf-8")
    print(f"Patched {HTML.name}; assets in {ASSETS.name}/ ({len(mapping)} gallery images)")


if __name__ == "__main__":
    main()
