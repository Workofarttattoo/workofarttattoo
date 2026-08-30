#!/usr/bin/env python3
"""Import best fresh/healed tattoo photos from the user asset batch."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
GALLERY = ROOT / "healed_tattoo_gallery_las_vegas"
HEALING = ROOT / "tattoo_healing_before_after_real_results"
ASSETS_DIRS = (
    ROOT / "assets",
    Path("/Users/noone/.cursor/projects/Users-noone-Downloads-GitHub-workofarttattoo/assets"),
)

# (uuid fragment, output stem under healed_tattoo_gallery_las_vegas/)
FRESH_IMPORTS: tuple[tuple[str, str], ...] = (
    # Best front-facing lion on black — replaces older fresh thigh photo
    ("D3613630", "fresh-roaring-lion-thigh-black-grey-joshua-cole-las-vegas"),
    # Straight-on elbow all-seeing eye — best angle in the batch
    ("6382CC1E", "fresh-all-seeing-eye-skull-elbow-joshua-cole-las-vegas"),
    # Dog portrait chest — fresh session
    ("4E0E77F8", "fresh-dog-portrait-chest-realism-joshua-cole-las-vegas"),
    # Bear roar outer forearm — highest resolution fresh bear angle
    ("85BE9FC5", "fresh-bear-roar-forearm-realism-joshua-cole-las-vegas"),
    # Eagle memorial forearm — fresh black & grey
    ("6B7C189C", "fresh-eagle-memorial-forearm-black-grey-joshua-cole-las-vegas"),
)

HEALED_STEM = "eagle-memorial-calf-healed-tattoo-las-vegas"
FRESH_EAGLE_STEM = "fresh-eagle-memorial-calf-tattoo-las-vegas"
COMPARISON_STEM = "eagle-memorial-calf-fresh-vs-healed-comparison-las-vegas"
FRESH_EAGLE_SRC = HEALING / "eagle-memorial-calf-fresh-tattoo-las-vegas.png"


def find_asset(fragment: str) -> Path | None:
    for assets_dir in ASSETS_DIRS:
        if not assets_dir.is_dir():
            continue
        matches = sorted(assets_dir.glob(f"*{fragment}*"))
        for path in matches:
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                return path
    return None


def save_gallery_image(src: Path, stem: str) -> None:
    GALLERY.mkdir(parents=True, exist_ok=True)
    dest_png = GALLERY / f"{stem}.png"
    with Image.open(src) as raw:
        im = ImageOps.exif_transpose(raw).convert("RGB")
        w, h = im.size
        max_edge = 1400
        if max(w, h) > max_edge:
            scale = max_edge / max(w, h)
            im = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        im.save(dest_png, "PNG", optimize=True)
        im.save(dest_png.with_suffix(".webp"), "WEBP", quality=84, method=6)
        thumb = im.copy()
        tw, th = thumb.size
        if max(tw, th) > 400:
            scale = 400 / max(tw, th)
            thumb = thumb.resize((int(tw * scale), int(th * scale)), Image.Resampling.LANCZOS)
        thumb.save(GALLERY / f"{stem}-400.webp", "WEBP", quality=80, method=6)


def split_eagle_healed_half() -> None:
    for base in (HEALING, ROOT / "las-vegas-tattoo-healing-guide"):
        src = base / f"{COMPARISON_STEM}.png"
        if not src.is_file():
            continue
        with Image.open(src) as im:
            w, h = im.size
            healed = im.crop((w // 2, 0, w, h))
        save_gallery_image_from_image(healed, HEALED_STEM)
        print(f"[ok] {HEALED_STEM} ← right half of {src.name}")
        return
    print("[warn] eagle comparison PNG not found — skipped healed calf crop")


def sync_eagle_fresh_to_gallery() -> None:
    """Homepage serves gallery folder media; healing-page folder is not on FTP."""
    if not FRESH_EAGLE_SRC.is_file():
        print(f"[warn] missing {FRESH_EAGLE_SRC.name} — skipped fresh eagle sync")
        return
    save_gallery_image(FRESH_EAGLE_SRC, FRESH_EAGLE_STEM)
    print(f"[ok] {FRESH_EAGLE_STEM} ← {FRESH_EAGLE_SRC.name}")


def save_gallery_image_from_image(im: Image.Image, stem: str) -> None:
    GALLERY.mkdir(parents=True, exist_ok=True)
    dest_png = GALLERY / f"{stem}.png"
    im.save(dest_png, "PNG", optimize=True)
    im.save(dest_png.with_suffix(".webp"), "WEBP", quality=84, method=6)


def import_all() -> list[str]:
    imported: list[str] = []
    for fragment, stem in FRESH_IMPORTS:
        src = find_asset(fragment)
        if not src:
            print(f"[warn] missing asset for {stem} ({fragment})")
            continue
        save_gallery_image(src, stem)
        imported.append(stem)
        print(f"[ok] {stem} ← {src.name}")
    split_eagle_healed_half()
    sync_eagle_fresh_to_gallery()
    return imported


def main() -> int:
    stems = import_all()
    if len(stems) < 3:
        print(
            f"[warn] Only imported {len(stems)} fresh gallery image(s); "
            "local asset batch unavailable — continuing build with existing gallery media."
        )
        return 0
    print(f"Imported {len(stems)} fresh gallery image(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
