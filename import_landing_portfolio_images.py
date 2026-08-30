#!/usr/bin/env python3
"""Import user-provided portfolio photos into client-portfolio for the landing page."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
CLIENT = ROOT / "home_work_of_art_tattoo_piercing" / "client-portfolio"
ASSETS_DIRS = (
    ROOT / "assets",
    Path("/Users/noone/.cursor/projects/Users-noone-Downloads-GitHub-workofarttattoo/assets"),
)

# (asset uuid fragment, output stem, alt text, category tags for filters)
LANDING_IMAGES: tuple[tuple[str, str, str, str], ...] = (
    (
        "F4DDBBB2",
        "black-grey-warrior-profile-shoulder-realism-las-vegas",
        "Black and grey warrior profile shoulder realism tattoo — Joshua Cole, Work of Art Las Vegas",
        "all black-grey realism client",
    ),
    (
        "29096302",
        "norse-odin-viking-ship-sleeve-realism-las-vegas",
        "Norse Odin and Viking ship black and grey sleeve — Joshua Cole, Work of Art Las Vegas",
        "all black-grey realism sleeves client",
    ),
    (
        "FE20F013",
        "portrait-legs-black-grey-realism-las-vegas",
        "Black and grey portrait leg tattoos — Joshua Cole, Work of Art Las Vegas",
        "all black-grey realism client",
    ),
    (
        "7168E5BE",
        "eagle-memorial-color-leg-tattoo-las-vegas",
        "Color eagle memorial leg tattoo — Joshua Cole, Work of Art Las Vegas",
        "all color-realism client",
    ),
    (
        "EF852DBB",
        "falling-angel-black-grey-realism-las-vegas",
        "Falling angel black and grey realism tattoo — Joshua Cole, Work of Art Las Vegas",
        "all black-grey realism client",
    ),
    (
        "609EC82D",
        "original-portrait-drawing-graphite-las-vegas",
        "Original graphite portrait drawing by Joshua Cole — Work of Art Las Vegas",
        "all client",
    ),
    (
        "3D49B9F9",
        "egyptian-face-neck-realism-tattoo-las-vegas",
        "Egyptian face neck black and grey realism tattoo — Joshua Cole, Work of Art Las Vegas",
        "all black-grey realism client",
    ),
    (
        "20D31CAD",
        "veiled-woman-statue-black-grey-realism-las-vegas",
        "Veiled woman statue black and grey realism tattoo — Joshua Cole, Work of Art Las Vegas",
        "all black-grey realism client",
    ),
    (
        "187BEB35",
        "fly-high-eagle-memorial-color-las-vegas",
        "Fly High With The Eagles memorial color leg tattoo — Joshua Cole, Work of Art Las Vegas",
        "all color-realism client",
    ),
    (
        "E010665E",
        "all-seeing-eye-triangle-forearm-realism-las-vegas",
        "All-seeing eye triangle forearm black and grey realism — Joshua Cole, Work of Art Las Vegas",
        "all black-grey realism client",
    ),
    (
        "3D695F6F",
        "original-singer-portrait-drawing-las-vegas",
        "Original singer portrait drawing by Joshua Cole — Work of Art Las Vegas",
        "all client",
    ),
    (
        "2EA11860",
        "original-pennywise-drawing-las-vegas",
        "Original Pennywise portrait drawing by Joshua Cole — Work of Art Las Vegas",
        "all client",
    ),
    (
        "8EE69C62",
        "red-rose-memorial-name-tattoo-las-vegas",
        "Red rose memorial name tattoo — Joshua Cole, Work of Art Las Vegas",
        "all color-realism client",
    ),
)

SHOWCASE_STEMS: tuple[str, ...] = (
    "norse-odin-viking-ship-sleeve-realism-las-vegas",
    "black-grey-warrior-profile-shoulder-realism-las-vegas",
    "veiled-woman-statue-black-grey-realism-las-vegas",
    "all-seeing-eye-triangle-forearm-realism-las-vegas",
)

CURATED_STEMS: tuple[str, ...] = tuple(stem for _, stem, _, _ in LANDING_IMAGES)


def find_asset(fragment: str) -> Path | None:
    for assets_dir in ASSETS_DIRS:
        if not assets_dir.is_dir():
            continue
        matches = sorted(assets_dir.glob(f"*{fragment}*"))
        for path in matches:
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                return path
    return None


def save_portfolio_image(src: Path, stem: str) -> None:
    CLIENT.mkdir(parents=True, exist_ok=True)
    dest_png = CLIENT / f"{stem}.png"
    with Image.open(src) as raw:
        im = ImageOps.exif_transpose(raw).convert("RGB")
        w, h = im.size
        max_edge = 1200
        if max(w, h) > max_edge:
            scale = max_edge / max(w, h)
            im = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        im.save(dest_png, "PNG", optimize=True)
        im.save(dest_png.with_suffix(".webp"), "WEBP", quality=84, method=6)


def import_all() -> list[str]:
    imported: list[str] = []
    for fragment, stem, _alt, _cats in LANDING_IMAGES:
        src = find_asset(fragment)
        if not src:
            print(f"[warn] missing asset for {stem} ({fragment})")
            continue
        save_portfolio_image(src, stem)
        imported.append(stem)
        print(f"[ok] {stem} ← {src.name}")
    return imported


def landing_items() -> list[dict]:
    """Items dicts for expand_homepage_conversion masonry helpers."""
    items: list[dict] = []
    base = f"/home_work_of_art_tattoo_piercing/client-portfolio"
    for _frag, stem, alt, cats in LANDING_IMAGES:
        png = CLIENT / f"{stem}.png"
        webp = CLIENT / f"{stem}.webp"
        if not png.is_file():
            continue
        items.append(
            {
                "stem": stem,
                "webp": f"{base}/{webp.name}" if webp.is_file() else "",
                "png": f"{base}/{png.name}",
                "cats": cats,
                "alt": alt,
            }
        )
    return items


def main() -> int:
    stems = import_all()
    if len(stems) < 4:
        raise SystemExit("Need at least 4 landing portfolio images imported")
    print(f"Imported {len(stems)} landing portfolio image(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
