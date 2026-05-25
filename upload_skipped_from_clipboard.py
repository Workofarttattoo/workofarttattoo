#!/usr/bin/env python3
"""
Split skipped_pages_clipboard.html (paste from clipboard saved to disk),
apply HTML fixes, and FTP-upload to slug folders matching prior deploy conventions.

FTP_USER / FTP_PASS required (tattoojosh@workofarttattoo.com).
"""

from __future__ import annotations

import os
import re
import sys
from ftplib import FTP, error_perm
from io import BytesIO
from pathlib import Path

HOST = "ftp.workofarttattoo.com"
CLIPBOARD_HTML = Path(__file__).resolve().parent / "skipped_pages_clipboard.html"
BUILD_DIR = Path(__file__).resolve().parent / "skipped_upload_build"


def ftp_mkdir_p(ftp: FTP, remote_path: str) -> None:
    parts = [p for p in remote_path.strip("/").split("/") if p]
    ftp.cwd("/")
    for part in parts:
        try:
            ftp.mkd(part)
        except error_perm:
            pass
        ftp.cwd(part)


def split_documents(raw: str) -> list[str]:
    idx = raw.find("<!DOCTYPE")
    if idx == -1:
        raise ValueError("No <!DOCTYPE in clipboard export.")
    body = raw[idx:]
    parts = [
        x.strip()
        for x in re.split(r"(?=<!DOCTYPE\s+html\b)", body, flags=re.IGNORECASE)
        if x.strip()
    ]
    return parts


def fix_stitch_placeholders(html: str) -> str:
    return re.sub(r"\{\{DATA:SCREEN:[^}]+\}\}", "/", html)


def strip_article_p_apply(html: str) -> str:
    html = html.replace(
        'class="article-p"',
        'class="font-body-lg text-body-lg leading-[1.8] text-on-surface-variant mb-8"',
    )
    return re.sub(
        r"\.article-p\s*\{[^}]*@apply[^}]*\}",
        "",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )


def classify(chunk: str) -> str | None:
    tm = re.search(r"<title[^>]*>([^<]*)</title>", chunk, flags=re.I | re.DOTALL)
    title = tm.group(1).strip().lower() if tm else ""

    if "best tattoo styles for sleeves" in title:
        return "large_scale_masterpieces_sleeves_back_pieces_hub"
    if "walk-in tattoos las vegas" in title:
        return "walk_in_tattoos_las_vegas_nap_corrected"
    if "how to choose a tattoo artist" in title:
        # Two variants share the title; pick the long-form fine-art guide.
        if "01. The Anatomy of Mastery" in chunk or 'id="anatomy"' in chunk:
            return "how_to_choose_a_tattoo_artist_master_selection_guide_1"
        if "01. Portfolio Techniques" in chunk:
            return None  # shorter duplicate; skip in favor of long guide
        return "how_to_choose_a_tattoo_artist_master_selection_guide_1"
    return None


def prepare_html(slug: str, html: str) -> bytes:
    if slug == "how_to_choose_a_tattoo_artist_master_selection_guide_1":
        html = fix_stitch_placeholders(html)
        html = strip_article_p_apply(html)
    return html.encode("utf-8")


def main() -> int:
    user = os.environ.get("FTP_USER", "").strip()
    pw = os.environ.get("FTP_PASS", "").strip()
    if not user or not pw:
        print("Set FTP_USER and FTP_PASS.", file=sys.stderr)
        return 1
    if not CLIPBOARD_HTML.is_file():
        print(f"Missing {CLIPBOARD_HTML}", file=sys.stderr)
        return 1

    raw = CLIPBOARD_HTML.read_text(encoding="utf-8", errors="strict")
    chunks = split_documents(raw)
    chosen: dict[str, str] = {}
    for ch in chunks:
        slug = classify(ch)
        if slug is None:
            tm = re.search(r"<title[^>]*>([^<]*)</title>", ch, flags=re.I | re.DOTALL)
            title_hint = tm.group(1).strip()[:60] + "…" if tm else "(no title)"
            print(f"[skip] {title_hint} — not deployed (duplicate or unrecognized layout)")
            continue
        if slug in chosen:
            print(f"[warn] duplicate slug {slug}; keeping first blob only")
            continue
        chosen[slug] = ch

    if not chosen:
        print("No classifiable documents found.", file=sys.stderr)
        return 1

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    ftp = FTP(HOST, timeout=120)
    ftp.login(user, pw)
    ftp.set_pasv(True)

    for slug in sorted(chosen.keys()):
        html = chosen[slug]
        data = prepare_html(slug, html)
        out = BUILD_DIR / f"{slug}.html"
        out.write_bytes(data)
        ftp_mkdir_p(ftp, slug)
        print(f"[up] /{slug}/index.html ({len(data)} bytes)")
        bio = BytesIO(data)
        ftp.storbinary("STOR index.html", bio)

    ftp.quit()
    print("Done.")
    for slug in sorted(chosen.keys()):
        print(f"https://workofarttattoo.com/{slug}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
