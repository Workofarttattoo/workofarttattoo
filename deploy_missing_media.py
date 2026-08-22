#!/usr/bin/env python3
"""Upload portrait + interview assets that often 404 after a partial deploy."""

from __future__ import annotations

import os
import sys
from ftplib import FTP, error_perm
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOST = "ftp.workofarttattoo.com"

# (local_path_relative_to_root, remote_dir_under_public_html)
UPLOADS: list[tuple[str, str]] = [
    (
        "artists/katelyn-cole/katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas.webp",
        "artists/katelyn-cole",
    ),
    (
        "artists/katelyn-cole/katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas.jpg",
        "artists/katelyn-cole",
    ),
    (
        "home_work_of_art_tattoo_piercing/joshua-cole-studio-interview-las-vegas.png",
        "home_work_of_art_tattoo_piercing",
    ),
    (
        "home_work_of_art_tattoo_piercing/joshua-cole-studio-interview-las-vegas.webp",
        "home_work_of_art_tattoo_piercing",
    ),
    (
        f"home_work_of_art_tattoo_piercing/work-of-art-studio-banner-las-vegas.png",
        "home_work_of_art_tattoo_piercing",
    ),
    (
        f"home_work_of_art_tattoo_piercing/work-of-art-studio-banner-las-vegas.webp",
        "home_work_of_art_tattoo_piercing",
    ),
]

DELETE_ON_KATELYN = (
    "katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas.png"
)


def ftp_mkdir_p(ftp: FTP, remote_path: str) -> None:
    ftp.cwd("/")
    for part in remote_path.strip("/").split("/"):
        try:
            ftp.mkd(part)
        except error_perm:
            pass
        ftp.cwd(part)


def upload_one(ftp: FTP, local: Path, remote_dir: str) -> None:
    expected = local.stat().st_size
    ftp.cwd("/")
    ftp_mkdir_p(ftp, remote_dir)
    print(f"[up] /{remote_dir}/{local.name} ({expected:,} bytes)")
    with open(local, "rb") as fh:
        ftp.storbinary(f"STOR {local.name}", fh)
    actual = ftp.size(local.name)
    ftp.cwd("/")
    if actual != expected:
        raise RuntimeError(f"Size mismatch {local.name}: local={expected} remote={actual}")


def main() -> int:
    user = os.environ.get("FTP_USER", "").strip()
    pw = os.environ.get("FTP_PASS", "").strip()
    if not user or not pw:
        print("Set FTP_USER and FTP_PASS.", file=sys.stderr)
        return 1

    missing: list[Path] = []
    for rel, _ in UPLOADS:
        p = ROOT / rel
        if not p.is_file():
            missing.append(p)
    if missing:
        print("Missing local files:", file=sys.stderr)
        for p in missing:
            print(f"  {p}", file=sys.stderr)
        print("Run: python3 prepare_site_deploy.py", file=sys.stderr)
        return 1

    ftp = FTP(HOST, timeout=120)
    try:
        ftp.login(user, pw)
        ftp.set_pasv(True)
        ftp.cwd("/")
        ftp_mkdir_p(ftp, "artists/katelyn-cole")
        try:
            ftp.delete(DELETE_ON_KATELYN)
            print(f"[rm] artists/katelyn-cole/{DELETE_ON_KATELYN}")
        except error_perm:
            pass
        ftp.cwd("/")
        for rel, remote_dir in UPLOADS:
            upload_one(ftp, ROOT / rel, remote_dir)
        ftp.quit()
    except (error_perm, OSError, RuntimeError) as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1

    print("Done. Run: python3 verify_live_deploy.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
