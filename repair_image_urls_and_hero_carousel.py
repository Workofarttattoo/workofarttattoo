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

6) Dead `aida-public` placeholders (HTTP 400): swap to self-hosted `/…/{seo-image}.png` assets
   already in the repo (Stitch export folders + img_* batches).
"""

from __future__ import annotations

import argparse
import re
import subprocess
from collections.abc import Sequence
from pathlib import Path

from bs4 import BeautifulSoup

_ROOT_A = Path(__file__).resolve().parent
_ROOT_B = Path("/Users/noone/Downloads/stitch_work_of_art_digital_overhaul 2")

GOOGLE_IMG_PATTERN = re.compile(
    r"https://lh3\.googleusercontent\.com/(?:aida-public|aida)/[^\"')\s<>]+"
)

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


def curl_ok(url: str) -> bool:
    try:
        proc = subprocess.run(
            ["curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}", url],
            capture_output=True,
            text=True,
            timeout=20,
        )
        return proc.stdout.strip() == "200"
    except (OSError, subprocess.TimeoutExpired):
        return False


def build_google_health_map(files: list[Path]) -> dict[str, bool]:
    """HEAD-check every unique Google CDN URL used in the project (once)."""
    urls: set[str] = set()
    for path in files:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        urls.update(GOOGLE_IMG_PATTERN.findall(raw))
    return {u: curl_ok(u) for u in sorted(urls)}


def folder_hosted_image_path(folder: Path) -> str | None:
    """First image asset in an export folder (SEO-renamed png preferred)."""
    if not folder.is_dir():
        return None
    images = [
        p
        for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ]
    if not images:
        return None
    images.sort(key=lambda p: (p.name == "screen.png", p.name))
    return f"/{folder.name}/{images[0].name}"


def build_local_hosted_pool(root: Path) -> list[str]:
    """`/folder/{image}.png` for every export dir with a hosted image."""
    out: list[str] = []
    if not root.is_dir():
        return out
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        url = folder_hosted_image_path(d)
        if url:
            out.append(url)
    return out


def file_local_pool(path: Path) -> list[str]:
    """Prefer this page's own folder image asset."""
    pools: list[str] = []
    url = folder_hosted_image_path(path.parent)
    if url:
        pools.append(url)
    return pools


def replace_dead_google_images(
    text: str,
    health: dict[str, bool],
    hosted_pool: Sequence[str],
    file_pool: Sequence[str],
    *,
    replace_all_google: bool = False,
) -> tuple[str, list[str]]:
    msgs: list[str] = []
    if not hosted_pool and not file_pool:
        return text, msgs

    all_google = unique_ordered(GOOGLE_IMG_PATTERN.findall(text))
    dead = [u for u in all_google if not health.get(u, False)]
    if replace_all_google and all_google:
        targets = all_google
    else:
        targets = dead
    if not targets:
        return text, msgs

    cycle: list[str] = list(file_pool)
    for u in hosted_pool:
        if u not in cycle:
            cycle.append(u)
    if not cycle:
        return text, msgs

    swaps = 0
    for i, bad_u in enumerate(targets):
        neu = cycle[i % len(cycle)]
        n = text.count(bad_u)
        if n:
            text = text.replace(bad_u, neu)
            swaps += n
    if swaps:
        label = "all Google CDN" if replace_all_google else "dead Google CDN"
        msgs.append(
            f"{label} → self-hosted images ({swaps} img src; "
            f"{len(targets)} unique URL(s))"
        )
    return text, msgs


def _apply_repairs(
    raw: str,
    global_public: Sequence[str],
    *,
    health: dict[str, bool] | None = None,
    hosted_pool: Sequence[str] | None = None,
    file_pool: Sequence[str] | None = None,
    replace_all_google: bool = False,
) -> tuple[str, list[str]]:
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

    if health is not None and hosted_pool is not None:
        text, m_dead = replace_dead_google_images(
            text,
            health,
            hosted_pool,
            file_pool or (),
            replace_all_google=replace_all_google,
        )
        msgs.extend(m_dead)

    text2, m2 = _beautiful_repairs(text)
    msgs.extend(m2)
    text3, m3 = _inject_img_retry(text2)
    msgs.extend(m3)

    return text3, msgs


def process_one(
    path: Path,
    dry_run: bool,
    global_public: Sequence[str],
    *,
    health: dict[str, bool] | None = None,
    hosted_pool: Sequence[str] | None = None,
) -> list[str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    use_all_local = path.parent.name.startswith("home_work_of_art")
    new_raw, msgs = _apply_repairs(
        raw,
        global_public,
        health=health,
        hosted_pool=hosted_pool,
        file_pool=file_local_pool(path),
        replace_all_google=use_all_local,
    )
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
    ap.add_argument(
        "--skip-hosted-swap",
        action="store_true",
        help="Do not replace dead Google CDN URLs with self-hosted /folder/*.png paths",
    )
    args = ap.parse_args()

    files = collect_html_files(
        include_root_b=not args.no_root_b,
        skip_artists_raw=args.skip_artists_raw,
    )

    global_public = build_global_public_pool(files)
    health: dict[str, bool] | None = None
    hosted_pool: list[str] | None = None
    if not args.skip_hosted_swap:
        print("Checking Google CDN image URLs (HEAD)…")
        health = build_google_health_map(files)
        dead_n = sum(1 for ok in health.values() if not ok)
        live_n = len(health) - dead_n
        print(f"  {live_n} OK, {dead_n} dead (of {len(health)} unique URLs)")
        hosted_pool = build_local_hosted_pool(_ROOT_A)
        if not args.no_root_b and _ROOT_B.is_dir():
            for u in build_local_hosted_pool(_ROOT_B):
                if u not in hosted_pool:
                    hosted_pool.append(u)
        print(f"  {len(hosted_pool)} self-hosted image path(s) for fallback")

    touched = 0
    for path in files:
        msgs = process_one(
            path,
            dry_run=args.dry_run,
            global_public=global_public,
            health=health,
            hosted_pool=hosted_pool,
        )

        if msgs:
            print(f"[{rel_display(path)}]")
            for m in msgs:
                print(f"  {m}")
            touched += 1
    print(f"\nScanned {len(files)} HTML file(s); {touched} reported changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
