#!/usr/bin/env python3
"""Inject gold cursor + sparkle trail into static HTML pages."""

from __future__ import annotations

from pathlib import Path

from woa_sparkle_cursor import inject_sparkle_into_html

ROOT = Path(__file__).resolve().parent

TARGETS = [
    ROOT / "home_work_of_art_tattoo_piercing" / "code.html",
    ROOT / "code.html",
    ROOT / "appointments" / "code.html",
    ROOT / "studio_videos" / "code.html",
    *sorted((ROOT / "artists_build").glob("*.html")),
]


def main() -> int:
    changed = 0
    for path in TARGETS:
        if not path.is_file():
            print(f"skip missing {path}")
            continue
        raw = path.read_text(encoding="utf-8")
        new_html, ok = inject_sparkle_into_html(raw)
        if ok:
            path.write_text(new_html, encoding="utf-8")
            print(f"sparkle {path}")
            changed += 1
        else:
            print(f"unchanged {path}")
    print(f"done — updated {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
