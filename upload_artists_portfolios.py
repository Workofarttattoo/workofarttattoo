#!/usr/bin/env python3
"""
Fix Stitch-export HTML artifacts (empty <head>, ```html fences) and upload artist pages.

Deploys:
  artists/katelyn-cole/index.html
  artists/joshua-cole/index.html

Requires: FTP_USER, FTP_PASS
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from ftplib import FTP, error_perm
from io import BytesIO
from pathlib import Path

HOST = "ftp.workofarttattoo.com"


def ftp_mkdir_p(ftp: FTP, remote_path: str) -> None:
    parts = [p for p in remote_path.strip("/").split("/") if p]
    ftp.cwd("/")
    for part in parts:
        try:
            ftp.mkd(part)
        except error_perm:
            pass
        ftp.cwd(part)


def strip_leading_section_comment(s: str) -> str:
    return re.sub(r"^<!--[^>]*?-->\s*", "", s.strip(), count=1, flags=re.DOTALL)


def strip_markdown_fences(s: str) -> str:
    s = re.sub(r"```html\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"```\s*", "", s)
    return s


def fix_html(doc: str, body_start_anchor: str) -> str:
    """Move orphan head-ish tags from after <body open> until anchor into real <head>."""
    doc = strip_leading_section_comment(doc)
    doc = strip_markdown_fences(doc)

    m = re.search(
        r"(<!DOCTYPE\s+[^>]+>)?\s*<html([^>]*)>\s*<head></head>\s*<body([^>]*)>\s*",
        doc,
        re.IGNORECASE | re.DOTALL,
    )
    if not m:
        raise ValueError("Expected Stitch pattern: <!DOCTYPE>? <html ...><head></head><body ...>.")

    doctype_line = "<!DOCTYPE html>"
    if m.group(1):
        doctype_line = m.group(1).strip()

    html_attrs = (m.group(2) or "").strip()
    body_attrs = (m.group(3) or "").strip()
    suffix = doc[m.end() :]

    idx = suffix.find(body_start_anchor)
    if idx == -1:
        raise ValueError(f"Anchor not found for body split: {body_start_anchor[:60]!r}")

    orphaned_head_bits = suffix[:idx].strip()
    body_markup = suffix[idx:]

    html_attr_str = f" {html_attrs}" if html_attrs else ""
    body_attr_str = f" {body_attrs}" if body_attrs else ""

    return (
        f"{doctype_line}\n"
        f"<html{html_attr_str}>\n"
        f"<head>\n{orphaned_head_bits}\n</head>\n"
        f"<body{body_attr_str}>\n{body_markup}\n</body>\n"
        "</html>\n"
    )


def extract_first_document_blob(block: str) -> str:
    """If two HTML docs pasted back-to-back, keep the first ending at first </html>."""
    low = block.lower()
    idx = low.find("</html>")
    if idx == -1:
        return block
    return block[: idx + len("</html>")]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("katelyn_file", type=Path, help="Raw Katelyn HTML file from Stitch")
    ap.add_argument("joshua_file", type=Path, help="Raw Joshua HTML file from Stitch")
    args = ap.parse_args()

    user = os.environ.get("FTP_USER", "").strip()
    pw = os.environ.get("FTP_PASS", "").strip()
    if not user or not pw:
        print("Set FTP_USER and FTP_PASS (e.g. tattoojosh@workofarttattoo.com).", file=sys.stderr)
        return 1

    kt_raw = args.katelyn_file.read_text(encoding="utf-8", errors="strict")
    jc_raw = args.joshua_file.read_text(encoding="utf-8", errors="strict")

    kt_html = fix_html(
        extract_first_document_blob(kt_raw),
        '<header class="fixed top-0 left-0 w-full z-50 flex justify-between',
    )
    jc_html = fix_html(
        extract_first_document_blob(jc_raw),
        "<!-- Sparkle Cursor Implementation -->",
    )

    ftp = FTP(HOST, timeout=120)
    ftp.login(user, pw)
    ftp.set_pasv(True)

    for rel, data in (
        ("artists/katelyn-cole/index.html", kt_html.encode("utf-8")),
        ("artists/joshua-cole/index.html", jc_html.encode("utf-8")),
    ):
        ftp_mkdir_p(ftp, str(Path(rel).parent))
        print(f"[up] /{rel} ({len(data)} bytes)")
        bio = BytesIO(data)
        ftp.storbinary(f"STOR {Path(rel).name}", bio)

    ftp.quit()
    print("Done.")
    print("https://workofarttattoo.com/artists/katelyn-cole/")
    print("https://workofarttattoo.com/artists/joshua-cole/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
