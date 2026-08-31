#!/usr/bin/env python3
"""
Rename every export folder's screen.png to an SEO-friendly filename derived from
image alt text (when referenced in HTML) or the folder slug.

Updates all HTML under the repo: /{folder}/screen.png → /{folder}/{seo-name}.png

  python3 rename_screen_png_seo.py
  python3 rename_screen_png_seo.py --dry-run
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
OLD_NAME = "screen.png"
MAX_STEM = 72

STRIP_ALT_SUFFIX = re.compile(
    r",?\s*Work of Art Tattoo\s*&?\s*Piercing,?\s*Las Vegas\s*$",
    re.I,
)


def seo_stem_from_alt(alt: str) -> str:
    text = STRIP_ALT_SUFFIX.sub("", alt).strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text).strip("-").lower()
    return text[:MAX_STEM] or "work-of-art-tattoo-las-vegas"


def seo_stem_from_folder(slug: str) -> str:
    s = slug.lower()
    if s.startswith("img_") and (s.endswith(".jpeg") or s.endswith(".jpg") or s.endswith(".png")):
        num = re.sub(r"\D", "", s) or "portfolio"
        return f"tattoo-portfolio-las-vegas-{num}"[:MAX_STEM]
    if s.startswith("image_"):
        return re.sub(r"[-_]+", "-", s).strip("-")[:MAX_STEM]
    stem = slug.replace("_", "-").lower()
    stem = re.sub(r"-+", "-", stem).strip("-")
    if not stem.endswith(("las-vegas", "vegas", "guide", "hub")):
        stem = f"{stem}-las-vegas"[:MAX_STEM]
    return stem[:MAX_STEM]


def collect_html_files() -> list[Path]:
    out: list[Path] = []
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts or "__pycache__" in p.parts:
            continue
        out.append(p)
    return out


def alts_by_folder(html_files: list[Path]) -> dict[str, list[str]]:
    """folder_slug -> list of alt strings from <img src="/{slug}/screen.png">."""
    by_folder: dict[str, list[str]] = {}
    for path in html_files:
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        for img in soup.find_all("img"):
            src = (img.get("src") or "").strip()
            m = re.match(rf"^/([^/]+)/{re.escape(OLD_NAME)}$", src)
            if not m:
                continue
            folder = m.group(1)
            alt = (img.get("alt") or "").strip()
            if alt:
                by_folder.setdefault(folder, []).append(alt)
    return by_folder


def pick_alt(alts: list[str]) -> str | None:
    if not alts:
        return None
    # Prefer longest descriptive alt (usually most specific).
    return max(alts, key=len)


def unique_filename(stem: str, used: set[str], folder_slug: str) -> str:
    base = stem
    candidate = f"{base}.png"
    if candidate not in used:
        used.add(candidate)
        return candidate
    suffix = re.sub(r"[^a-z0-9]+", "-", folder_slug.lower()).strip("-")[:24]
    candidate = f"{base}-{suffix}.png"
    n = 2
    while candidate in used:
        candidate = f"{base}-{suffix}-{n}.png"
        n += 1
    used.add(candidate)
    return candidate


def build_rename_plan(html_files: list[Path]) -> dict[str, str]:
    """folder_slug -> new filename (e.g. custom-sleeve-tattoo-las-vegas.png)."""
    alts = alts_by_folder(html_files)
    used_names: set[str] = set()
    plan: dict[str, str] = {}

    folders = sorted(
        d.name
        for d in ROOT.iterdir()
        if d.is_dir() and (d / OLD_NAME).is_file()
    )

    for slug in folders:
        alt = pick_alt(alts.get(slug, []))
        stem = seo_stem_from_alt(alt) if alt else seo_stem_from_folder(slug)
        plan[slug] = unique_filename(stem, used_names, slug)
    return plan


def apply_html_updates(html_files: list[Path], plan: dict[str, str], dry_run: bool) -> int:
    changed_files = 0
    for path in html_files:
        raw = path.read_text(encoding="utf-8", errors="replace")
        new = raw
        for slug, fname in plan.items():
            new = new.replace(f"/{slug}/{OLD_NAME}", f"/{slug}/{fname}")
        if new != raw:
            if not dry_run:
                path.write_text(new, encoding="utf-8")
            changed_files += 1
    return changed_files


def apply_renames(plan: dict[str, str], dry_run: bool) -> int:
    n = 0
    for slug, fname in sorted(plan.items()):
        src = ROOT / slug / OLD_NAME
        dst = ROOT / slug / fname
        if not src.is_file():
            continue
        if dst.exists() and dst != src:
            print(f"[warn] skip {slug}: target exists {fname}")
            continue
        print(f"  /{slug}/{OLD_NAME} → /{slug}/{fname}")
        if not dry_run:
            src.rename(dst)
        n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    html_files = collect_html_files()
    plan = build_rename_plan(html_files)

    print(f"Folders with {OLD_NAME}: {len(plan)}")
    for slug, fname in sorted(plan.items())[:8]:
        print(f"  {slug} → {fname}")
    if len(plan) > 8:
        print(f"  … and {len(plan) - 8} more")

    n_disk = apply_renames(plan, dry_run=args.dry_run)
    n_html = apply_html_updates(html_files, plan, dry_run=args.dry_run)

    mode = "would rename" if args.dry_run else "renamed"
    print(f"\n{mode} {n_disk} file(s); updated {n_html} HTML file(s).")
    if not args.dry_run:
        print("Next: python3 deploy_stitch_site_root.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
