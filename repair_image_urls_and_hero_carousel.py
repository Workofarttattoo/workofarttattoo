#!/usr/bin/env python3
"""
Fix common Stitch static-site image failures:

1) Hero carousel: `#hero-carousel` sometimes has inline `transform: translateX(-100%)`
   with no carousel JS → slides sit off-screen. Reset to `translateX(0)`.

2) Blocked Google URLs: `https://lh3.googleusercontent.com/aida/...` (private AIDA
   bucket) often 403 in normal browsers. Each file's own `.../aida-public/...` URLs are
   preferred; if a file has blocked links but no public ones, replacements use a
   project-wide pool gathered from all other HTML (so raw exports still get working
   CDN URLs).

3) Visibility / lazy-load: carousel background wrappers using `z-[-1]` can paint behind
   the page in Safari; bumped to `z-0` with `isolate` on the hero `<section>`.

4) Hero carousel images: swap `loading="lazy"` → `loading="eager"`, first slide
   gets `fetchpriority="high"` (LCP / “images not appearing” fixes).

5) Global: one-shot retry on failed Google CDN `<img>` loads (capture-phase error listener).
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from pathlib import Path

from bs4 import BeautifulSoup

_ROOT_A = Path(__file__).resolve().parent
_ROOT_B = Path("/Users/noone/Downloads/stitch_work_of_art_digital_overhaul 2")

BLOCKED_PATTERN = re.compile(
    r"https://lh3\.googleusercontent\.com/aida/[^\"')\s<>]+"
)
PUBLIC_PATTERN = re.compile(
    r"https://lh3\.googleusercontent\.com/aida-public/[^\"')\s<>]+"
)

CAROUSEL_BAD = (
    'style="transform: translateX(-100%);"',
)
CAROUSEL_FIX = 'style="transform: translateX(0);"'

_IMG_RETRY_MARKER = 'data-woa-img-load-repair="1"'
_IMG_RETRY_SCRIPT = """<script data-woa-img-load-repair="1" type="text/javascript">(function(){
window.addEventListener("error",function(e){
var t=e.target;
if(!t||t.tagName!=="IMG"||!t.getAttribute||t.getAttribute("data-woa-retry-done"))return;
var s=t.src||"";
if(s.indexOf("googleusercontent")<0&&s.indexOf("googleapis.com")<0)return;
if(s.indexOf("woa-retry=")>=0)return;
t.setAttribute("data-woa-retry-done","1");
var i=s.indexOf("?");
var base=i<0?s:s.slice(0,i);
t.src=base+"?woa-retry="+Date.now();
},true);
})();</script>"""


def _inject_img_retry(html: str) -> tuple[str, list[str]]:
    msgs: list[str] = []
    if _IMG_RETRY_MARKER in html:
        return html, msgs
    if "googleusercontent" not in html and "googleapis.com" not in html:
        return html, msgs
    li = html.lower().rfind("</body>")
    if li < 0:
        return html, msgs
    out = html[:li] + "\n" + _IMG_RETRY_SCRIPT + "\n" + html[li:]
    msgs.append("inject one-shot google CDN img retry (before </body>)")
    return out, msgs


def _beautiful_repairs(html: str) -> tuple[str, list[str]]:
    """
    Parser-based fixes for `#hero-carousel` pages (mostly the home hero).
    """
    msgs: list[str] = []
    if 'id="hero-carousel"' not in html and "id='hero-carousel'" not in html:
        return html, msgs

    soup = BeautifulSoup(html, "html.parser")
    carousel = soup.find(id="hero-carousel")
    if not carousel:
        return html, msgs

    parent = carousel.parent
    if parent is not None and getattr(parent, "name", "") == "div":
        pcs = parent.get("class")
        if isinstance(pcs, list):
            patched = []
            for c in pcs:
                cs = str(c)
                patched.append(cs.replace("z-[-1]", "z-0") if cs else cs)
            if patched != pcs:
                parent["class"] = patched
                msgs.append("hero backdrop: Tailwind z-[-1] → z-0")

    section = carousel.find_parent("section")
    if section is not None:
        scl = section.get("class")
        if isinstance(scl, list) and all(str(c).strip() != "isolate" for c in scl):
            scl.append("isolate")
            msgs.append("hero section: isolate (stable stacking context)")

    imgs = carousel.find_all("img", recursive=True)
    img_changed = False
    for idx, img in enumerate(imgs):
        if img.get("loading") == "lazy":
            img["loading"] = "eager"
            img_changed = True
        if idx == 0 and not img.get("fetchpriority"):
            img["fetchpriority"] = "high"
            img_changed = True
        if not img.get("decoding"):
            img["decoding"] = "async"
            img_changed = True
    if img_changed:
        msgs.append("hero-carousel <img>: eager + fetchpriority/decoding")

    return str(soup), msgs


def collect_html_files(include_root_b: bool, skip_artists_raw: bool = False) -> list[Path]:
    out: list[Path] = []
    seen: set[str] = set()
    roots = [_ROOT_A]
    if include_root_b and _ROOT_B.is_dir():
        roots.append(_ROOT_B)
    for root in roots:
        if not root.is_dir():
            continue
        for p in root.rglob("*.html"):
            if skip_artists_raw and "artists_raw" in str(p.resolve()):
                continue
            if "__pycache__" in p.parts:
                continue
            rp = str(p.resolve())
            if rp in seen:
                continue
            seen.add(rp)
            out.append(p)
    return sorted(out)


def unique_ordered(matches: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out


def build_global_public_pool(files: list[Path]) -> list[str]:
    """Stable-ordered unique list of embeddable aida-public URLs across the repo."""
    out: list[str] = []
    seen: set[str] = set()
    for path in files:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for u in PUBLIC_PATTERN.findall(raw):
            if u not in seen:
                seen.add(u)
                out.append(u)
    return out


def _apply_repairs(raw: str, global_public: Sequence[str]) -> tuple[str, list[str]]:
    msgs: list[str] = []
    text = raw
    for bad in CAROUSEL_BAD:
        if bad in text:
            n = text.count(bad)
            msgs.append(f"carousel transform reset ({n} occurrence(s))")
            text = text.replace(bad, CAROUSEL_FIX)

    public_local = unique_ordered(PUBLIC_PATTERN.findall(text))
    pool: list[str] = public_local if public_local else list(global_public)
    blocked_ordered = unique_ordered(BLOCKED_PATTERN.findall(text))

    if blocked_ordered and pool:
        mapping = {b: pool[i % len(pool)] for i, b in enumerate(blocked_ordered)}
        swaps = 0
        for bad_u, neu in mapping.items():
            swaps += text.count(bad_u)
            text = text.replace(bad_u, neu)
        if swaps:
            src = (
                "using each file's own public URLs first"
                if public_local
                else "repo-wide /aida-public/ pool fallback"
            )
            msgs.append(f"/aida/ → /aida-public/ round-robin ({swaps} replacement(s); {src})")
    elif blocked_ordered and not pool:
        msgs.append(
            f"[warn] {len(blocked_ordered)} blocked /aida/ URL(s), "
            "no /aida-public/ anywhere in project — left unchanged"
        )

    text2, m2 = _beautiful_repairs(text)
    msgs.extend(m2)
    text3, m3 = _inject_img_retry(text2)
    msgs.extend(m3)

    return text3, msgs


def process_one(path: Path, dry_run: bool, global_public: Sequence[str]) -> list[str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    new_raw, msgs = _apply_repairs(raw, global_public)
    if new_raw != raw and not dry_run:
        path.write_text(new_raw, encoding="utf-8")
    return msgs


def rel_display(p: Path) -> str:
    try:
        return str(p.relative_to(_ROOT_A))
    except ValueError:
        try:
            return str(p.relative_to(_ROOT_B))
        except ValueError:
            return str(p)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--no-root-b",
        action="store_true",
        help=f"Skip second root ({_ROOT_B.name})",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing files",
    )
    ap.add_argument(
        "--skip-artists-raw",
        action="store_true",
        help='Do not process artists_raw/*.html (default: raw files ARE repaired)',
    )
    args = ap.parse_args()

    files = collect_html_files(
        include_root_b=not args.no_root_b,
        skip_artists_raw=args.skip_artists_raw,
    )

    global_public = build_global_public_pool(files)

    touched = 0
    for path in files:
        msgs = process_one(path, dry_run=args.dry_run, global_public=global_public)

        if msgs:
            print(f"[{rel_display(path)}]")
            for m in msgs:
                print(f"  {m}")
            touched += 1
    print(f"\nScanned {len(files)} HTML file(s); {touched} reported changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
