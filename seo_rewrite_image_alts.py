#!/usr/bin/env python3
"""
Rewrite <img alt> attributes across Stitch export HTML for SEO.

- Prefer long data-alt text as the primary description (then remove data-alt)
- Expand slug-style alts into readable phrases
- Vary near-duplicate gallery images with light, natural suffixes
- Append a concise Las Vegas / studio phrase when it still fits (~140 chars)
- By default also scans sibling folders `stitch_work_of_art_digital_overhaul 3` … `6`
  (screenshot-only bundles simply yield no HTML; any `code.html` there is included)

Deploy (optional):
  FTP_USER=tattoojosh@workofarttattoo.com FTP_PASS=... \\
    python seo_rewrite_image_alts.py --deploy
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections.abc import Sequence
from collections import defaultdict
from html import unescape
from io import BytesIO
from pathlib import Path
from typing import Callable

from bs4 import BeautifulSoup
from ftplib import FTP, error_perm

_THIS = Path(__file__).resolve().parent
ROOT_A = _THIS
ROOT_B = Path("/Users/noone/Downloads/stitch_work_of_art_digital_overhaul 2")

# Sibling Stitch exports (often screenshots only in 4–6; scanned for any HTML present).
ADJACENT_STITCH_SITE_ROOT_NAMES = (
    "stitch_work_of_art_digital_overhaul 3",
    "stitch_work_of_art_digital_overhaul 4",
    "stitch_work_of_art_digital_overhaul 5",
    "stitch_work_of_art_digital_overhaul 6",
)

BRAND_TAIL = ", Work of Art Tattoo & Piercing, Las Vegas"
BRAND_MARKER = "work of art tattoo & piercing, las vegas"
MAX_ALT = 140

_VARIATIONS = (
    " Close-up composition.",
    " Alternate angle.",
    " Healed-result example.",
    " Full layout on skin.",
    " Detail of shading and contrast.",
)


def discover_adjacent_stitch_roots() -> list[Path]:
    roots: list[Path] = []
    parent = ROOT_A.parent
    for name in ADJACENT_STITCH_SITE_ROOT_NAMES:
        p = parent / name
        if p.is_dir():
            roots.append(p)
    return roots


def collect_html_from_site_tree(
    root: Path,
    take: Callable[[Path], None],
    *,
    include_clipboard: bool = False,
) -> None:
    """code.html nests, artists_build, skipped_upload_build; clipboard only when flagged."""
    if not root.is_dir():
        return
    for p in sorted(root.rglob("code.html")):
        take(p)
    ab = root / "artists_build"
    if ab.is_dir():
        for p in sorted(ab.glob("*.html")):
            take(p)
    ub = root / "skipped_upload_build"
    if ub.is_dir():
        for p in sorted(ub.glob("*.html")):
            take(p)
    if include_clipboard:
        cb = root / "skipped_pages_clipboard.html"
        if cb.is_file():
            take(cb)


def iter_target_files(
    include_clipboard_archive: bool,
    include_adjacent_sites: bool = True,
    extra_roots: Sequence[Path] | None = None,
) -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []

    def take(p: Path) -> None:
        if not p.is_file():
            return
        k = str(p.resolve())
        if k not in seen:
            seen.add(k)
            out.append(p)

    for root in (ROOT_A, ROOT_B):
        if root.is_dir():
            collect_html_from_site_tree(
                root,
                take,
                include_clipboard=include_clipboard_archive
                and root.resolve() == ROOT_A.resolve(),
            )

    if include_adjacent_sites:
        for root in discover_adjacent_stitch_roots():
            collect_html_from_site_tree(root, take, include_clipboard=False)

    if extra_roots:
        for raw in extra_roots:
            root = Path(raw).expanduser().resolve()
            collect_html_from_site_tree(root, take, include_clipboard=False)

    artists_raw_exclude = frozenset(
        {
            (ROOT_A / "artists_raw" / "katelyn.raw.html").resolve(),
            (ROOT_A / "artists_raw" / "joshua.raw.html").resolve(),
        }
    )
    out = [p for p in out if p.resolve() not in artists_raw_exclude]

    return sorted(out, key=lambda p: str(p))


def rel_display_seo(path: Path) -> str:
    rp = path.resolve()
    prefix = ""
    if ROOT_A.is_dir():
        rab = ROOT_A.resolve()
        if rp == rab or rab in rp.parents:
            try:
                return prefix + str(path.relative_to(ROOT_A))
            except ValueError:
                pass

    rb = ROOT_B.resolve()
    if ROOT_B.is_dir() and (rp == rb or rb in rp.parents):
        prefix = "[2] "
        try:
            return prefix + str(path.relative_to(ROOT_B))
        except ValueError:
            pass

    for aj in discover_adjacent_stitch_roots():
        if not aj.is_dir():
            continue
        base = aj.resolve()
        mt = re.search(r"(\d+)\s*$", aj.name.strip())
        label = mt.group(1) if mt else aj.name[-12:].strip()
        if rp == base or base in rp.parents:
            try:
                return f"[export {label}] " + str(path.relative_to(aj))
            except ValueError:
                continue

    return str(path)


def slug_like(s: str) -> bool:
    t = s.strip().lower().replace(" ", "_")
    return bool(re.match(r"^[a-z0-9]+(?:[_-][a-z0-9]+)+$", t))


def kebab_to_readable(s: str) -> str:
    s = unescape(s)
    for ch in ("_", "-"):
        s = s.replace(ch, " ")
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        return ""
    small = {"and", "or", "with", "of", "near", "in", "at", "&", "by", "for"}
    bits = []
    for w in s.split():
        wl = w.lower()
        if "&" in w:
            bits.append(w)
        elif wl in small:
            bits.append(wl)
        elif w.isupper():
            bits.append(w)
        else:
            bits.append(w[0].upper() + w[1:].lower() if len(w) > 1 else w.upper())
    return " ".join(bits)


def compress_ws(s: str) -> str:
    return re.sub(r"\s+", " ", unescape(s)).strip()


def enrich_base(data_alt: str, title: str, cur_alt: str) -> str:
    dac = compress_ws(data_alt) if data_alt else ""
    if len(dac) >= 35:
        return dac.rstrip(".")
    if dac and len(dac) >= 15:
        return dac.rstrip(".")

    t = compress_ws(title) if title else ""
    if len(t) >= 12:
        return (kebab_to_readable(t) if slug_like(t) else t).rstrip(".")

    ca = compress_ws(cur_alt) if cur_alt else ""
    if len(ca) >= 40 and not slug_like(ca):
        return ca.rstrip(".")
    if ca:
        return kebab_to_readable(ca).rstrip(".")

    return "Tattoo and piercing photography at premier Las Vegas studio Work of Art Tattoo & Piercing"


def has_full_brand_phrase(alt: str) -> bool:
    return BRAND_MARKER in alt.lower()


def variation_for_dup(norm_key: str, occ: int) -> str:
    if occ <= 1:
        return ""
    return _VARIATIONS[(occ - 2) % len(_VARIATIONS)]


def shorten(s: str, limit: int) -> str:
    s = s.strip()
    if len(s) <= limit:
        return s
    cut = limit - 1
    trimmed = s[:cut]
    if " " in trimmed:
        trimmed = trimmed[: trimmed.rfind(" ")]
    return trimmed.rstrip(",;— ") + "…"


def process_html(raw: str) -> tuple[str, int]:
    soup = BeautifulSoup(raw, "html.parser")
    counts: dict[str, int] = defaultdict(int)
    changed = 0

    for img in soup.find_all("img"):
        old_alt = compress_ws(img.get("alt") or "")
        dac = img.get("data-alt") or ""
        title = img.get("title") or ""

        base = enrich_base(dac, title, old_alt)
        norm = base[:80].lower()
        counts[norm] += 1
        occ = counts[norm]

        neo = compress_ws(base + variation_for_dup(norm, occ))
        neo = neo.rstrip(".")
        # Remove stutter: "… Las Vegas Work of Art, Work of Art Tattoo & Piercing…"
        neo = re.sub(
            r"\s+work of art(?=\s*,\s*work of art tattoo)",
            "",
            neo,
            flags=re.I,
        ).strip()
        if not has_full_brand_phrase(neo):
            neo = re.sub(r",?\s*work of art\s*$", "", neo, flags=re.I).strip()

        if has_full_brand_phrase(neo):
            neo = shorten(neo, MAX_ALT)
        else:
            room = MAX_ALT - len(BRAND_TAIL)
            body = shorten(neo, max(40, room))
            body = body.rstrip(",;. ")
            neo = body + BRAND_TAIL
            if len(neo) > MAX_ALT:
                neo = shorten(neo, MAX_ALT)

        if img.get("data-alt"):
            del img["data-alt"]

        img["alt"] = neo
        if neo != old_alt and not img.has_attr("loading"):
            img["loading"] = "lazy"

        if neo != old_alt:
            changed += 1

    return str(soup), changed


def process_file(path: Path) -> int:
    raw = path.read_text(encoding="utf-8", errors="replace")
    new, delta = process_html(raw)
    path.write_text(new, encoding="utf-8")
    return delta


def ftp_mkdir_p(ftp: FTP, remote_path: str) -> None:
    parts = [p for p in remote_path.strip("/").split("/") if p]
    ftp.cwd("/")
    for part in parts:
        try:
            ftp.mkd(part)
        except error_perm:
            pass
        ftp.cwd(part)


def ftp_put(ftp: FTP, local: Path, remote_dir: str) -> None:
    data = local.read_bytes()
    ftp_mkdir_p(ftp, remote_dir)
    bio = BytesIO(data)
    ftp.storbinary("STOR index.html", bio)


def deploy_extras(user: str, pw: str) -> None:
    ftp = FTP("ftp.workofarttattoo.com", timeout=120)
    ftp.login(user, pw)
    ftp.set_pasv(True)

    for local, remote in (
        (ROOT_A / "artists_build" / "katelyn-cole.html", "artists/katelyn-cole"),
        (ROOT_A / "artists_build" / "joshua-cole.html", "artists/joshua-cole"),
    ):
        if local.is_file():
            print(f"[ftp] {local.name} → /{remote}/index.html")
            ftp_put(ftp, local, remote)

    bud = ROOT_A / "skipped_upload_build"
    if bud.is_dir():
        for f in sorted(bud.glob("*.html")):
            slug = f.stem
            print(f"[ftp] {f.name} → /{slug}/index.html")
            ftp_put(ftp, f, slug)

    ftp.quit()


def run_deploy_stitch_root() -> int:
    import importlib.util

    spec = importlib.util.spec_from_file_location("dep", _THIS / "deploy_stitch_site_root.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.main()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--include-clipboard-archive",
        action="store_true",
        help="Also rewrite skipped_pages_clipboard.html",
    )
    ap.add_argument(
        "--deploy",
        action="store_true",
        help="Run deploy_stitch_site_root.py then push artists + skipped_upload_build",
    )
    ap.add_argument(
        "--no-adjacent-sites",
        action="store_true",
        help="Skip sibling stitch_work_of_art_digital_overhaul 3–6 (under same parent as ROOT_A)",
    )
    ap.add_argument(
        "--root",
        action="append",
        default=None,
        metavar="DIR",
        help="Extra site root containing code.html nests / artists_build (repeatable)",
    )
    args = ap.parse_args()

    files = iter_target_files(
        include_clipboard_archive=args.include_clipboard_archive,
        include_adjacent_sites=not args.no_adjacent_sites,
        extra_roots=args.root,
    )
    files_with_changes = 0
    total_img_updates = 0
    for f in files:
        n = process_file(f)
        if n:
            files_with_changes += 1
            total_img_updates += n
        print(f"{rel_display_seo(f)}: {n} alt(s) updated")

    print(
        f"\nSummary: {files_with_changes} file(s) had alt changes, ~{total_img_updates} <img> updates."
    )

    if args.deploy:
        user = os.environ.get("FTP_USER", "").strip()
        pw = os.environ.get("FTP_PASS", "").strip()
        if not user or not pw:
            print("FTP_USER / FTP_PASS required for --deploy.", file=sys.stderr)
            return 2
        code = run_deploy_stitch_root()
        if code != 0:
            return code
        deploy_extras(user, pw)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
