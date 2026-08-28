#!/usr/bin/env python3
"""Upload Katelyn's nested piercing portfolio to the production FTP path.

The general deploy script publishes direct artist media but historically skipped
nested artists/katelyn-cole/piercing-portfolio/*.webp. This closes that gap.
Requires FTP_USER and FTP_PASS.
"""
from __future__ import annotations
import os
from ftplib import FTP, error_perm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / 'artists' / 'katelyn-cole' / 'piercing-portfolio'
REMOTE = 'artists/katelyn-cole/piercing-portfolio'
HOST = 'ftp.workofarttattoo.com'


def mkdir_p(ftp: FTP, path: str) -> None:
    ftp.cwd('/')
    for part in [p for p in path.strip('/').split('/') if p]:
        try:
            ftp.mkd(part)
        except error_perm:
            pass
        ftp.cwd(part)


def main() -> int:
    user = os.environ.get('FTP_USER','').strip()
    pw = os.environ.get('FTP_PASS','').strip()
    if not user or not pw:
        raise SystemExit('FTP_USER and FTP_PASS are required')
    files = sorted(LOCAL.glob('*.webp'))
    if not files:
        raise SystemExit(f'No WebPs found in {LOCAL}')
    ftp = FTP(HOST, timeout=120)
    ftp.login(user, pw)
    ftp.set_pasv(True)
    mkdir_p(ftp, REMOTE)
    for p in files:
        expected = p.stat().st_size
        with p.open('rb') as fh:
            ftp.storbinary(f'STOR {p.name}', fh)
        actual = ftp.size(p.name)
        if actual != expected:
            raise RuntimeError(f'{p.name}: local={expected}, remote={actual}')
        print(f'[up] /{REMOTE}/{p.name} ({expected:,} bytes)')
    ftp.quit()
    print(f'Uploaded and size-verified {len(files)} Katelyn piercing WebPs.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
