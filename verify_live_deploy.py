#!/usr/bin/env python3
"""Check whether production matches the prepared static export."""

from __future__ import annotations

import io
import sys
import urllib.error
import urllib.request

from PIL import Image

SITE = "https://www.workofarttattoo.com"
HOME_LOCAL = "home_work_of_art_tattoo_piercing/code.html"
KATELYN_BASE = (
    "katelyn-cole-professional-piercer-ear-curation-no-duplicates-las-vegas"
)
KATELYN_WEBP = f"/artists/katelyn-cole/{KATELYN_BASE}.webp"
KATELYN_JPG = f"/artists/katelyn-cole/{KATELYN_BASE}.jpg"
PORTRAIT_WEBP_SIZE = (640, 853)
PORTRAIT_JPG_SIZE = (800, 1067)
INTERVIEW_STILL = (
    "/home_work_of_art_tattoo_piercing/joshua-cole-studio-interview-las-vegas.png"
)


def fetch(url: str) -> tuple[bytes | None, dict[str, str], int | None]:
    """Return (body, headers, http_status). body is None on hard failures."""
    req = urllib.request.Request(url, headers={"User-Agent": "WOA-Deploy-Verify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return body, headers, resp.status
    except urllib.error.HTTPError as e:
        headers = {k.lower(): v for k, v in e.headers.items()} if e.headers else {}
        return None, headers, e.code


def image_size(body: bytes) -> tuple[int, int]:
    with Image.open(io.BytesIO(body)) as im:
        return im.size


def main() -> int:
    from pathlib import Path

    root = Path(__file__).resolve().parent
    local_path = root / HOME_LOCAL
    if not local_path.is_file():
        print(f"Missing {local_path}", file=sys.stderr)
        return 1

    local_html = local_path.read_text(encoding="utf-8", errors="replace")
    local_size = local_path.stat().st_size

    live_body, headers, _ = fetch(f"{SITE}/index.html")
    if live_body is None:
        print("Could not fetch live homepage.", file=sys.stderr)
        return 1
    live_html = live_body.decode("utf-8", errors="replace")
    live_size = len(live_body)

    print(f"Local homepage:  {local_size:,} bytes")
    print(f"Live index.html: {live_size:,} bytes (Last-Modified: {headers.get('last-modified', '?')})")

    errors: list[str] = []
    warnings: list[str] = []

    if abs(live_size - local_size) > 500:
        errors.append("homepage byte size differs — deploy did not upload the prepared export")

    for needle in ('WOA_BUILD_STAMP:', 'id="studio-interview"', "instagram.com/reel/DDiX988y0tR"):
        if needle in local_html and needle not in live_html:
            errors.append(f"live homepage missing {needle}")

    for banned in ("DXSZTKZyt2l", 'href="#hero-interview"', "woa-ig-preview"):
        if banned in live_html:
            errors.append(f"live homepage still has banned content: {banned}")

    if INTERVIEW_STILL.lstrip("/") in local_html:
        interview_body, interview_headers, interview_status = fetch(f"{SITE}{INTERVIEW_STILL}")
        if interview_status != 200 or interview_body is None:
            errors.append(
                f"interview hero still missing on server ({INTERVIEW_STILL}) — redeploy home assets"
            )
        else:
            print(
                f"Interview still: live {len(interview_body):,} bytes "
                f"({interview_headers.get('last-modified', '?')})"
            )

    local_webp = root / KATELYN_WEBP.lstrip("/")
    local_jpg = root / KATELYN_JPG.lstrip("/")
    local_webp_len = local_webp.stat().st_size if local_webp.is_file() else 0
    local_jpg_len = local_jpg.stat().st_size if local_jpg.is_file() else 0

    live_webp_body, live_webp_headers, webp_status = fetch(f"{SITE}{KATELYN_WEBP}")
    live_jpg_body, live_jpg_headers, jpg_status = fetch(f"{SITE}{KATELYN_JPG}")

    live_webp_len = (
        int(live_webp_headers.get("content-length", "0") or 0)
        if live_webp_body
        else 0
    )
    live_jpg_len = (
        int(live_jpg_headers.get("content-length", "0") or 0) if live_jpg_body else 0
    )

    print(f"Katelyn webp: local {local_webp_len:,} vs live {live_webp_len:,} (HTTP {webp_status})")
    print(f"Katelyn jpg:  local {local_jpg_len:,} vs live {live_jpg_len:,} (HTTP {jpg_status})")

    if webp_status != 200 or live_webp_body is None:
        errors.append("Katelyn .webp missing on server")
    elif local_webp_len and abs(live_webp_len - local_webp_len) > 5000:
        errors.append("Katelyn .webp on server is stale (wrong file size)")
    else:
        try:
            if image_size(live_webp_body) != PORTRAIT_WEBP_SIZE:
                errors.append(
                    f"Katelyn .webp wrong dimensions on live: {image_size(live_webp_body)}"
                )
        except OSError as e:
            errors.append(f"Katelyn .webp not a valid image on live: {e}")

    if local_jpg_len:
        if jpg_status == 404 or live_jpg_body is None:
            errors.append(
                "Katelyn .jpg not on server (404) — run: python3 deploy_missing_media.py"
            )
        elif live_jpg_len < 50_000:
            errors.append(
                "Katelyn .jpg fallback too small on server — run: python3 deploy_missing_media.py"
            )
        elif abs(live_jpg_len - local_jpg_len) > 8000:
            errors.append("Katelyn .jpg on server is stale (wrong file size)")
        else:
            try:
                if image_size(live_jpg_body) != PORTRAIT_JPG_SIZE:
                    errors.append(
                        f"Katelyn .jpg wrong dimensions on live: {image_size(live_jpg_body)}"
                    )
            except OSError as e:
                errors.append(f"Katelyn .jpg not a valid image on live: {e}")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print("\nFAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print("\nFull site: python3 prepare_site_deploy.py", file=sys.stderr)
        print("         Merge/push to main so Deploy Work of Art Production publishes gh-pages.", file=sys.stderr)
        print("Do not use Bluehost FTP scripts for production.", file=sys.stderr)
        return 1

    print("\nOK — live homepage and Katelyn portrait match prepared export.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
