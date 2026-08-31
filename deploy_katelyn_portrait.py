#!/usr/bin/env python3
"""Upload only Katelyn portrait webp + jpg to /artists/katelyn-cole/ (fast fix for 404 on .jpg)."""

from __future__ import annotations

import os
import sys
from ftplib import FTP, error_perm
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOST = "ftp.workofarttattoo.com"
REMOTE = "artists/katelyn-cole"
STEM = "katelyn-cole-professional-piercer-ear-curation-no-duplicates-las-vegas"
FILES = (f"{STEM}.webp", f"{STEM}.jpg")


def ftp_mkdir_p(ftp: FTP, remote_path: str) -> None:
    ftp.cwd("/")
    for part in remote_path.strip("/").split("/"):
        try:
            ftp.mkd(part)
        except error_perm:
            pass
        ftp.cwd(part)


def upload_one(ftp: FTP, local: Path) -> None:
    expected = local.stat().st_size
    ftp.cwd("/")
    ftp_mkdir_p(ftp, REMOTE)
    print(f"[up] /{REMOTE}/{local.name} ({expected:,} bytes)")
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

    local_dir = ROOT / "artists" / "katelyn-cole"
    missing = [local_dir / name for name in FILES if not (local_dir / name).is_file()]
    if missing:
        print("Missing local files — run: python3 restore_katelyn_portrait.py", file=sys.stderr)
        for p in missing:
            print(f"  {p}", file=sys.stderr)
        return 1

    ftp = FTP(HOST, timeout=120)
    try:
        ftp.login(user, pw)
        ftp.set_pasv(True)
        ftp.cwd("/")
        ftp_mkdir_p(ftp, REMOTE)
        try:
            ftp.delete(f"{STEM}.png")
            print(f"[rm] /{REMOTE}/{STEM}.png (stale host-rewritten copy)")
        except error_perm:
            pass
        ftp.cwd("/")
        for name in FILES:
            upload_one(ftp, local_dir / name)
        ftp.quit()
    except (error_perm, OSError, RuntimeError) as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1

    print("Done. Run: python3 verify_live_deploy.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
