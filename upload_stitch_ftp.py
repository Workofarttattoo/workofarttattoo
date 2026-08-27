#!/usr/bin/env python3
"""Upload Stitch export folders (code.html → index.html) to Bluehost FTP."""

import os
import sys
from ftplib import FTP, error_perm
from pathlib import Path

SOURCES = [
    Path("/Users/noone/Downloads/stitch_work_of_art_digital_overhaul"),
    Path("/Users/noone/Downloads/stitch_work_of_art_digital_overhaul 2"),
]
REMOTE_BASE = "stitch-pages"
HOST = "ftp.workofarttattoo.com"

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ico"}


def ftp_mkdir_p(ftp: FTP, remote_path: str) -> None:
    """Cd to / then create nested dirs and leave cwd inside the deepest path."""
    parts = [p for p in remote_path.strip("/").split("/") if p]
    ftp.cwd("/")
    for part in parts:
        try:
            ftp.mkd(part)
        except error_perm:
            pass  # Already exists or parent missing edge cases resolved by traversal
        ftp.cwd(part)


def gather_folders():
    merged = {}
    for root in SOURCES:
        if not root.is_dir():
            continue
        for d in sorted(root.iterdir()):
            if not d.is_dir() or d.name.startswith("."):
                continue
            merged[d.name] = d
    return merged


def main() -> int:
    user = os.environ.get("FTP_USER", "").strip()
    pw = os.environ.get("FTP_PASS", "").strip()
    if not user or not pw:
        print("Set FTP_USER and FTP_PASS.", file=sys.stderr)
        return 1

    merged = gather_folders()
    print(f"SOURCES: {[str(s) for s in SOURCES]}")
    print(f"Unique slug folders: {len(merged)}")

    ftp = FTP(HOST, timeout=60)
    ftp.login(user, pw)
    ftp.set_pasv(True)

    uploaded = 0
    skipped = 0

    for slug in sorted(merged.keys()):
        local_dir = merged[slug]
        code = local_dir / "code.html"
        if not code.is_file():
            print(f"[skip] {slug} — no code.html")
            skipped += 1
            continue

        ftp_mkdir_p(ftp, f"{REMOTE_BASE}/{slug}")
        remote_index = f"/{REMOTE_BASE}/{slug}/index.html"
        print(f"[up] {local_dir.name} → {remote_index}")
        with open(code, "rb") as fh:
            ftp.storbinary("STOR index.html", fh)

        for fpath in sorted(local_dir.iterdir()):
            if not fpath.is_file() or fpath.name == "code.html":
                continue
            if fpath.suffix.lower() not in IMAGE_EXT:
                continue
            print(f"[up]   asset {fpath.name}")
            with open(fpath, "rb") as bf:
                ftp.storbinary(f"STOR {fpath.name}", bf)

        uploaded += 1

    ftp.quit()
    print(f"Done. Uploaded {uploaded} HTML pages, skipped {skipped} folders without code.html.")
    print(f"Base URL prefix: https://workofarttattoo.com/{REMOTE_BASE}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
