#!/usr/bin/env python3
"""Set keyword-rich img alt text from filenames and page context across static HTML."""

from __future__ import annotations

import re
from html import escape
from pathlib import Path
from urllib.parse import urlparse

from woa_nav_config import GUIDE_META, HOME_SLUG, merged_export_roots

ROOT = Path(__file__).resolve().parent
STUDIO = "Work of Art Tattoo & Piercing, Las Vegas"
MAX_ALT = 140

# Page-level keyword phrases for alt suffixes
PAGE_KEYWORDS: dict[str, str] = {
    HOME_SLUG: "Las Vegas tattoo shop and piercing studio",
    "artists": "Las Vegas tattoo artists directory",
    "appointments": "book tattoo and piercing appointments Las Vegas",
}
for slug, (title, _blurb) in GUIDE_META.items():
    PAGE_KEYWORDS[slug] = title

PAGE_KEYWORDS["artists/joshua-cole"] = "Joshua Cole tattoo artist Las Vegas"
PAGE_KEYWORDS["artists/katelyn-cole"] = "Katelyn Cole piercer Las Vegas"

# Filename stem overrides (normalized stem — see normalize_stem)
STEM_OVERRIDES: dict[str, str] = {
    "best-tattoo-las-vegas-custom-sleeve-by-master-artist": (
        "Best custom tattoo sleeve Las Vegas by master artist"
    ),
    "professional-tattoo-artist-work-of-art-las-vegas-studio": (
        "Professional tattoo artist at Work of Art Las Vegas studio"
    ),
    "joshua-cole-masterpiece-wall-consistently-unique": (
        "Joshua Cole tattoo artist — black and grey realism portfolio wall"
    ),
    "joshua-cole-portrait-las-vegas": (
        "Joshua Cole tattoo artist working in the Work of Art Las Vegas studio"
    ),
    "katelyn-cole-master-body-piercer-ear-curation-no-duplicates": (
        "Katelyn Cole professional piercer — curated ear and body piercing Las Vegas"
    ),
    "jay-jay-artist-portfolio-authentic-masterpieces": (
        "Jay Jay tattoo artist — realism portfolio Las Vegas"
    ),
    "expert-body-piercing-services-las-vegas-luxury-jewelry": (
        "Body piercing Las Vegas with luxury implant-grade jewelry"
    ),
    "custom-tattoos-las-vegas-epic-snake-black-and-grey-realism": (
        "Black and grey lion thigh tattoo Las Vegas — realism portfolio"
    ),
    "black-and-grey-artistry-dynamic-snake-masterpiece": (
        "Black and grey snake tattoo sleeve masterpiece Las Vegas"
    ),
    "realism-tattoos-color-butterfly-and-floral-coverup": (
        "Color realism butterfly and floral cover-up tattoo Las Vegas"
    ),
    "realism-tattoos-floral-and-roman-numeral-sleeve": (
        "Fine line floral and roman numeral sleeve tattoo Las Vegas"
    ),
    "realism-tattoos-grim-reaper-dark-art": (
        "Black and grey grim reaper realism tattoo Las Vegas"
    ),
    "custom-tattoos-las-vegas-vibrant-color-sunflower-design": (
        "Vibrant color sunflower custom tattoo Las Vegas"
    ),
    "custom-tattoos-las-vegas-flying-dove-realism": (
        "Flying dove black and grey realism tattoo Las Vegas"
    ),
    "custom-tattoos-las-vegas-matching-nightmare-before-christmas-tattoos": (
        "Matching Nightmare Before Christmas custom tattoos Las Vegas"
    ),
    "cover-up-tattoo-phoenix-hand": (
        "Color phoenix hand cover-up tattoo Las Vegas — finished work"
    ),
    "cover-up-tattoo-faded-butterflies-hand": (
        "Consult photo — faded hand tattoos for cover-up planning Las Vegas"
    ),
    "cover-up-tattoo-faded-floral-leg": (
        "Consult photo — aged floral leg tattoo for cover-up consult Las Vegas"
    ),
    "cover-up-tattoo-sunflower-over-black-ink": (
        "Cover-up tattoo Las Vegas — sunflower over solid black ink"
    ),
    "healed-realism-seraphim-eye-wings-tattoo": (
        "Healed black and grey seraphim eye and wings realism tattoo"
    ),
    "healed-black-grey-chain-heart-tattoo": (
        "Healed cover-up tattoo — black and grey chain and heart detail"
    ),
    "black-grey-collarbone-thorns-wreath-tattoo": (
        "Black and grey collarbone thorns and wreath tattoo Las Vegas"
    ),
    "black-grey-realism-snake-sleeve-tattoo": (
        "Black and grey realism snake sleeve tattoo Las Vegas"
    ),
}

WORD_FIXES = (
    ("b g", "black and grey"),
    ("bg ", "black and grey "),
    ("cover up", "cover-up"),
    ("walk in", "walk-in"),
    ("fine line", "fine line"),
    ("neo traditional", "neo-traditional"),
    ("t shirt", "t-shirt"),
)


def page_slug_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) >= 2 and parts[0] == "artists_build":
        name = parts[1].replace(".html", "")
        return f"artists/{name}"
    if len(parts) >= 1 and parts[0] != "code.html":
        return parts[0]
    return HOME_SLUG


def stem_from_src(src: str) -> str | None:
    if not src or src.startswith("data:"):
        return None
    if "googleusercontent" in src or "googleapis.com" in src:
        return None
    path = urlparse(src).path if "://" in src else src
    name = Path(path).name
    for ext in (".webp", ".png", ".jpg", ".jpeg", ".gif"):
        if name.lower().endswith(ext):
            return name[: -len(ext)]
    return None


def normalize_stem(stem: str) -> tuple[str, str]:
    """Return (normalized_key, prefix like Before/After/Healed)."""
    s = stem.lower()
    prefix = ""
    for suffix, label in (
        ("-las-vegas-before", "Before "),
        ("-las-vegas-after", "After "),
        ("-before", "Before "),
        ("-after", "After "),
    ):
        if s.endswith(suffix):
            s = s[: -len(suffix)]
            prefix = label
            break
    if s.startswith("healed-"):
        prefix = "Healed "
        s = s[7:]
    if s.endswith("-las-vegas"):
        s = s[: -len("-las-vegas")]
    s = s.strip("-")
    return s, prefix


def humanize_stem(stem: str) -> str:
    key, prefix = normalize_stem(stem)
    if key in STEM_OVERRIDES:
        return STEM_OVERRIDES[key]

    phrase = key.replace("-", " ")
    for old, new in WORD_FIXES:
        phrase = phrase.replace(old, new)
    phrase = phrase.replace("grey", "and grey").replace("black and and grey", "black and grey")

    drop = {"las", "vegas", "work", "of", "art", "master", "guide", "authentic", "variant"}
    words = [w for w in phrase.split() if w not in drop or len(phrase.split()) <= 5]
    desc = " ".join(words) if words else phrase
    desc = desc[0].upper() + desc[1:] if desc else desc
    return prefix + desc


def generic_alt_for_external(page_kw: str, index: int) -> str:
    templates = [
        f"Custom tattoo work — {page_kw} at {STUDIO}",
        f"Tattoo portfolio photo — {page_kw} at {STUDIO}",
        f"Las Vegas tattoo studio portfolio — {page_kw}",
        f"Professional tattoo session — {page_kw} at {STUDIO}",
        f"Healed tattoo detail — {page_kw} at {STUDIO}",
        f"Body piercing and tattoo artistry — {page_kw} at {STUDIO}",
    ]
    return templates[index % len(templates)]


def build_alt(src: str, page_slug: str, img_index: int) -> str:
    page_kw = PAGE_KEYWORDS.get(page_slug, "Las Vegas tattoo and piercing")
    stem = stem_from_src(src)

    if stem is None:
        alt = generic_alt_for_external(page_kw, img_index)
    else:
        subject = humanize_stem(stem)
        low = subject.lower()
        if "las vegas" in low:
            alt = f"{subject} — {page_kw} at {STUDIO}"
        else:
            alt = f"{subject} — {page_kw}, {STUDIO}"

    if len(alt) > MAX_ALT:
        alt = alt[: MAX_ALT - 1].rstrip(" ,—") + "…"
    return alt


IMG_TAG_RE = re.compile(r"<img\s+([^>]+?)/?\s*>", re.IGNORECASE)
SRC_RE = re.compile(r"""src=(['"])([^'"]+)\1""", re.IGNORECASE)
ALT_RE = re.compile(r"""alt=(['"])([^'"]*)\1""", re.IGNORECASE)


def replace_img_alts(html: str, page_slug: str) -> tuple[str, int]:
    count = 0
    img_index = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count, img_index
        attrs = match.group(1)
        src_m = SRC_RE.search(attrs)
        if not src_m:
            return match.group(0)
        src = src_m.group(2)
        new_alt = escape(build_alt(src, page_slug, img_index), quote=True)
        img_index += 1
        if ALT_RE.search(attrs):
            attrs = ALT_RE.sub(f'alt="{new_alt}"', attrs, count=1)
        else:
            attrs = f'alt="{new_alt}" {attrs}'
        count += 1
        return f"<img {attrs}>"

    return IMG_TAG_RE.sub(repl, html), count


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for slug, folder in merged_export_roots().items():
        code = folder / "code.html"
        if code.is_file():
            files.append(code)
    for extra in (
        ROOT / "artists_build" / "joshua-cole.html",
        ROOT / "artists_build" / "katelyn-cole.html",
    ):
        if extra.is_file():
            files.append(extra)
    return sorted(set(files))


def main() -> int:
    total_files = 0
    total_imgs = 0
    for path in iter_html_files():
        slug = page_slug_for(path)
        html = path.read_text(encoding="utf-8", errors="replace")
        new_html, n = replace_img_alts(html, slug)
        if n:
            path.write_text(new_html, encoding="utf-8")
            total_files += 1
            total_imgs += n
            print(f"{path.relative_to(ROOT)}: {n} images")
    print(f"Updated {total_imgs} alt texts across {total_files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
