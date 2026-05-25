#!/usr/bin/env python3
"""
Deploy Stitch exports at the site document root (no /stitch-pages/ prefix).

- Each folder with code.html → /<slug>/index.html (+ image assets)
- Home export also written to /index.html
- `appointments/` is a static landing so /appointments/index.html wins over WordPress
  (otherwise the theme header appears on that URL).
- Prepends DirectoryIndex so index.html wins over index.php on /
- Removes remote stitch-pages/ tree if present
"""

from __future__ import annotations

import os
import sys
from ftplib import FTP, error_perm
from io import BytesIO
from pathlib import Path

# Base export folder + any "stitch_work_of_art_digital_overhaul N" siblings under Downloads.
# Merge order: base first, then numbered folders sorted numerically (6 wins over 2 on same slug).
_DOWNLOADS = Path("/Users/noone/Downloads")
_SOURCE_PREFIX = "stitch_work_of_art_digital_overhaul"


def _discover_source_roots() -> list[Path]:
    roots: list[Path] = []
    base = _DOWNLOADS / _SOURCE_PREFIX
    if base.is_dir():
        roots.append(base)
    numbered: list[tuple[int, Path]] = []
    for p in _DOWNLOADS.iterdir():
        if not p.is_dir():
            continue
        name = p.name
        if not name.startswith(_SOURCE_PREFIX + " "):
            continue
        suffix = name[len(_SOURCE_PREFIX) :].strip()
        try:
            n = int(suffix)
        except ValueError:
            continue
        numbered.append((n, p))
    for _, p in sorted(numbered, key=lambda t: t[0]):
        roots.append(p)
    return roots


SOURCES = _discover_source_roots()
HOST = "ftp.workofarttattoo.com"
HOME_SLUG = "home_work_of_art_tattoo_piercing"
LEGACY_PREFIX = "stitch-pages"

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ico"}

HTACCESS_MARKER = "# Stitch: prefer static index.html before WordPress\n"
HTACCESS_SNIPPET = HTACCESS_MARKER + """<IfModule mod_dir.c>
DirectoryIndex index.html index.php
</IfModule>

"""


def ftp_mkdir_p(ftp: FTP, remote_path: str) -> None:
    parts = [p for p in remote_path.strip("/").split("/") if p]
    ftp.cwd("/")
    for part in parts:
        try:
            ftp.mkd(part)
        except error_perm:
            pass
        ftp.cwd(part)


def gather_folders() -> dict[str, Path]:
    merged: dict[str, Path] = {}
    for root in SOURCES:
        if not root.is_dir():
            continue
        for d in sorted(root.iterdir()):
            if not d.is_dir() or d.name.startswith("."):
                continue
            merged[d.name] = d
    return merged


def ftp_rmtree(ftp: FTP, path: str) -> None:
    """Remove path (under FTP home) recursively."""
    ftp.cwd("/")
    try:
        ftp.cwd(path)
    except error_perm:
        return

    for name, meta in ftp.mlsd():
        if name in (".", ".."):
            continue
        if meta.get("type") == "dir":
            ftp_rmtree(ftp, f"{path}/{name}")
            ftp.cwd("/")
            ftp.cwd(path)
        else:
            try:
                ftp.delete(name)
            except error_perm as e:
                print(f"[warn] delete {path}/{name}: {e}")

    ftp.cwd("/")
    try:
        ftp.rmd(path)
    except error_perm as e:
        print(f"[warn] rmd {path}: {e}")


def patch_htaccess(raw: bytes) -> bytes:
    text = raw.decode("utf-8", errors="replace")
    if HTACCESS_MARKER in text:
        return raw
    return (HTACCESS_SNIPPET + text).encode("utf-8")


def main() -> int:
    user = os.environ.get("FTP_USER", "").strip()
    pw = os.environ.get("FTP_PASS", "").strip()
    if not user or not pw:
        print("Set FTP_USER and FTP_PASS.", file=sys.stderr)
        return 1

    merged = gather_folders()
    if HOME_SLUG not in merged:
        print(f"Missing home folder {HOME_SLUG!r}; cannot write /index.html.", file=sys.stderr)
        return 1

    print(f"SOURCES: {[str(s) for s in SOURCES]}")
    print(f"Unique folders: {len(merged)} (home slug: {HOME_SLUG})")

    ftp = FTP(HOST, timeout=120)
    ftp.login(user, pw)
    ftp.set_pasv(True)

    buf = BytesIO()
    ftp.retrbinary("RETR .htaccess", buf.write)
    old_ht = buf.getvalue()
    new_ht = patch_htaccess(old_ht)
    if new_ht != old_ht:
        print("[up] /.htaccess (prepend DirectoryIndex for index.html)")
        ftp.cwd("/")
        ftp.storbinary("STOR .htaccess", BytesIO(new_ht))

    uploaded = 0
    skipped = 0

    for slug in sorted(merged.keys()):
        local_dir = merged[slug]
        code = local_dir / "code.html"
        if not code.is_file():
            print(f"[skip] {slug} — no code.html")
            skipped += 1
            continue

        ftp_mkdir_p(ftp, slug)
        print(f"[up] /{slug}/index.html")
        with open(code, "rb") as fh:
            ftp.storbinary("STOR index.html", fh)

        for fpath in sorted(local_dir.iterdir()):
            if not fpath.is_file() or fpath.name == "code.html":
                continue
            if fpath.suffix.lower() not in IMAGE_EXT:
                continue
            print(f"[up]   asset /{slug}/{fpath.name}")
            with open(fpath, "rb") as bf:
                ftp.storbinary(f"STOR {fpath.name}", bf)

        uploaded += 1

    home_code = merged[HOME_SLUG] / "code.html"
    ftp.cwd("/")
    print("[up] /index.html (from home export)")
    with open(home_code, "rb") as fh:
        ftp.storbinary("STOR index.html", fh)

    print(f"[rm] removing legacy /{LEGACY_PREFIX}/ …")
    ftp_rmtree(ftp, LEGACY_PREFIX)

    ftp.quit()
    print(
        f"Done. Uploaded {uploaded} section roots + homepage, skipped {skipped} folders without code.html."
    )
    print(f"Try: https://workofarttattoo.com/")
    print("Example slug: https://workofarttattoo.com/walk_in_tattoos_las_vegas_authority_guide/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
