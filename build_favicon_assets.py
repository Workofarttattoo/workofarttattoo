#!/usr/bin/env python3
"""Build root favicon.ico and logo.png from the studio logo asset."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "home_work_of_art_tattoo_piercing" / "work-of-art-logo.png"
FAVICON = ROOT / "favicon.ico"
LOGO = ROOT / "logo.png"


def main() -> int:
    if not SOURCE.is_file():
        print(f"[error] missing logo source: {SOURCE}", flush=True)
        return 1

    try:
        from PIL import Image
    except ImportError as exc:
        print(f"[error] Pillow required: {exc}", flush=True)
        return 1

    img = Image.open(SOURCE).convert("RGBA")
    img.save(LOGO, format="PNG", optimize=True)

    sizes = [(16, 16), (32, 32), (48, 48)]
    icons = [img.resize(size, Image.Resampling.LANCZOS) for size in sizes]
    icons[0].save(
        FAVICON,
        format="ICO",
        sizes=[(icon.width, icon.height) for icon in icons],
        append_images=icons[1:],
    )
    print(f"[ok] wrote {FAVICON.name} and {LOGO.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
