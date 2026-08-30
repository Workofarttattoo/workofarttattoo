#!/usr/bin/env python3
"""Three-way reconciliation: main vs gh-pages vs live site."""

from __future__ import annotations

import hashlib
import re
import ssl
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from html import unescape
from pathlib import Path

SITE = "https://www.workofarttattoo.com"
ROOT = Path(__file__).resolve().parent

ROUTES: tuple[str, ...] = (
    "/",
    "/artists/",
    "/artists/joshua-cole/",
    "/artists/katelyn-cole/",
    "/artists/teralyn/",
    "/appointments/",
    "/merchandise/",
    "/cover-up-tattoos-las-vegas/",
    "/best_piercing_shop_las_vegas_updated_jewelry_standards/",
    "/fine_line_tattoos_las_vegas_master_authority_guide/",
    "/best_tattoo_styles_for_sleeves_large_scale_project_hub/",
    "/walk_in_tattoos_las_vegas_authority_guide/",
    "/tattoo_shop_near_the_strip_geo_seo_optimized/",
    "/dermis_skin_science_las_vegas_authority_guide/",
)

ROSTER_NEEDLE = (
    "Joshua Cole (tattoo and piercing, studio lead), "
    "Katelyn Cole (professional piercer), and Teralyn"
)
PHONE_PATTERNS = ("(725) 224-1240", "725-224-1240", "7252241240", "tel:+17252241240")
EMAIL_PATTERNS = ("thewhiteknight702@gmail.com", "mailto:thewhiteknight702@gmail.com")
HOURS_PATTERNS = (
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
    "Monday",
    "Closed",
    "11:00",
    "7:00",
)

MODULE_MARKERS: dict[str, tuple[str, ...]] = {
    "/": (
        'class="woa-kb-group"',
        "STUDIO_ROSTER",
        "Book Appointment",
        "las-vegas-tattoo-hero-background",
    ),
    "/artists/": ("Joshua Cole", "Katelyn Cole", "Teralyn"),
    "/appointments/": ("Fresha", "Book", "appointment"),
    "/merchandise/": ("merch", "Add to cart", "Shop"),
    "/cover-up-tattoos-las-vegas/": ("cover-up", "Cover Up", "consultation"),
    "/dermis_skin_science_las_vegas_authority_guide/": ("dermis", "skin science", "authority"),
}


@dataclass
class PageSignals:
    source: str
    route: str
    exists: bool = False
    http_status: int | None = None
    file_path: str = ""
    title: str = ""
    canonical: str = ""
    h1: str = ""
    roster_present: bool = False
    phone_present: bool = False
    email_present: bool = False
    hours_present: bool = False
    key_images: list[str] = field(default_factory=list)
    cta_hrefs: list[str] = field(default_factory=list)
    modules: dict[str, bool] = field(default_factory=dict)
    content_hash: str = ""
    error: str = ""

    def summary(self) -> str:
        if not self.exists:
            return self.error or "MISSING"
        parts = [
            f"title={self.title[:60]}..." if len(self.title) > 60 else f"title={self.title or '∅'}",
            f"canon={self.canonical or '∅'}",
            f"h1={self.h1[:40]}..." if len(self.h1) > 40 else f"h1={self.h1 or '∅'}",
        ]
        nap = []
        if self.roster_present:
            nap.append("roster✓")
        if self.phone_present:
            nap.append("phone✓")
        if self.email_present:
            nap.append("email✓")
        if self.hours_present:
            nap.append("hours✓")
        if nap:
            parts.append(",".join(nap))
        if self.key_images:
            parts.append(f"imgs={len(self.key_images)}")
        if self.cta_hrefs:
            parts.append(f"ctas={len(self.cta_hrefs)}")
        return " | ".join(parts)


def route_candidates(route: str) -> list[str]:
    if route == "/":
        return [
            "index.html",
            "home_work_of_art_tattoo_piercing/index.html",
            "code.html",
            "home_work_of_art_tattoo_piercing/code.html",
        ]
    slug = route.strip("/")
    return [f"{slug}/index.html", f"{slug}/code.html"]


def git_show(ref: str, path: str) -> str | None:
    out = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True,
        cwd=ROOT,
    )
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8", errors="replace")


def local_read(route: str) -> tuple[str | None, str]:
    for p in route_candidates(route):
        fp = ROOT / p
        if fp.is_file():
            return fp.read_text(encoding="utf-8", errors="replace"), p
    return None, ""


def fetch_live(route: str) -> tuple[str | None, int | None, str]:
    url = SITE + route
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "WOA-ThreeWay-Reconcile/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="replace"), resp.status, url
    except urllib.error.HTTPError as exc:
        return None, exc.code, url
    except OSError as exc:
        return None, None, str(exc)


def strip_tags(text: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return unescape(re.sub(r"\s+", " ", text)).strip()


def extract_signals(html: str, source: str, route: str, file_path: str = "", http_status: int | None = None) -> PageSignals:
    sig = PageSignals(source=source, route=route, exists=True, http_status=http_status, file_path=file_path)

    m = re.search(r"<title>([^<]*)</title>", html, re.I)
    sig.title = unescape(m.group(1).strip()) if m else ""

    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html, re.I)
    if not m:
        m = re.search(r'href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', html, re.I)
    sig.canonical = unescape(m.group(1).strip()) if m else ""

    h1s = re.findall(r"<h1[^>]*>([\s\S]*?)</h1>", html, re.I)
    sig.h1 = strip_tags(h1s[0]) if h1s else ""

    lower = html.lower()
    sig.roster_present = ROSTER_NEEDLE.lower() in lower or (
        "joshua cole" in lower and "katelyn cole" in lower and "teralyn" in lower
    )
    sig.phone_present = any(p.lower() in lower for p in PHONE_PATTERNS)
    sig.email_present = any(p.lower() in lower for p in EMAIL_PATTERNS)
    sig.hours_present = sum(1 for p in HOURS_PATTERNS if p.lower() in lower) >= 3

    imgs = re.findall(r'(?:src|href)=["\']([^"\']+\.(?:webp|png|jpe?g|gif|svg))["\']', html, re.I)
    seen: set[str] = set()
    for img in imgs:
        name = img.split("/")[-1].split("?")[0]
        if name and name not in seen and not name.startswith("data:"):
            seen.add(name)
            sig.key_images.append(name)
    sig.key_images = sig.key_images[:8]

    cta_patterns = (
        r'href=["\']([^"\']*(?:fresha|appointments|book|consult|merchandise|cover-up|artists)[^"\']*)["\']',
    )
    cta_seen: set[str] = set()
    for pat in cta_patterns:
        for href in re.findall(pat, html, re.I):
            if href.startswith("#") or href.startswith("javascript:"):
                continue
            if href not in cta_seen:
                cta_seen.add(href)
                sig.cta_hrefs.append(href)
    sig.cta_hrefs = sig.cta_hrefs[:6]

    markers = MODULE_MARKERS.get(route, ())
    for marker in markers:
        sig.modules[marker] = marker.lower() in lower or marker in html

    normalized = re.sub(r"\s+", " ", html)
    sig.content_hash = hashlib.sha256(normalized.encode()).hexdigest()[:12]
    return sig


def load_main(route: str) -> PageSignals:
    html, path = local_read(route)
    if html is None:
        for p in route_candidates(route):
            html = git_show("main", p)
            if html:
                path = p
                break
    if html is None:
        return PageSignals(source="MAIN", route=route, exists=False, error="no index.html or code.html")
    return extract_signals(html, "MAIN", route, path)


def load_ghpages(route: str) -> PageSignals:
    for p in route_candidates(route):
        html = git_show("origin/gh-pages", p)
        if html:
            return extract_signals(html, "GH-PAGES", route, p)
    return PageSignals(source="GH-PAGES", route=route, exists=False, error="not on gh-pages")


def load_live(route: str) -> PageSignals:
    html, status, meta = fetch_live(route)
    if html is None:
        return PageSignals(
            source="LIVE",
            route=route,
            exists=False,
            http_status=status,
            error=f"HTTP {status}" if status else meta,
        )
    return extract_signals(html, "LIVE", route, meta, status)


def normalize_title(t: str) -> str:
    return re.sub(r"\s+", " ", t.replace("&amp;", "&")).strip().lower()


def normalize_canonical(c: str, route: str) -> str:
    if not c:
        return ""
    c = c.rstrip("/") + "/"
    expected = (SITE + route).rstrip("/") + "/"
    if c == expected:
        return "OK"
    return c


def compare_route(main: PageSignals, pages: PageSignals, live: PageSignals) -> tuple[str, str]:
    if not live.exists:
        if main.exists and not pages.exists:
            return "BROKEN", "Build/deploy route; gh-pages missing, live 404"
        if main.exists and pages.exists:
            return "BROKEN", "Route on gh-pages but live 404 — DNS/cache or deploy marker issue"
        if not main.exists:
            return "BROKEN", "Route missing from main and live"
        return "BROKEN", "Live unavailable"

    if live.content_hash == pages.content_hash if pages.exists else False:
        live_pages_match = True
    elif pages.exists and main.exists:
        live_pages_match = live.content_hash == pages.content_hash
    else:
        live_pages_match = False

    live_main_match = live.exists and main.exists and live.content_hash == main.content_hash

    title_live_main = normalize_title(live.title) == normalize_title(main.title) if main.exists else False
    title_live_pages = normalize_title(live.title) == normalize_title(pages.title) if pages.exists else False
    canon_live = normalize_canonical(live.canonical, live.route)
    canon_main = normalize_canonical(main.canonical, main.route) if main.exists else ""
    canon_pages = normalize_canonical(pages.canonical, pages.route) if pages.exists else ""

    h1_live_main = live.h1.lower().strip() == main.h1.lower().strip() if main.exists and live.h1 and main.h1 else False

    if live_pages_match and (not main.exists or live_main_match):
        return "MATCH", "Live matches gh-pages; main aligned"

    if live_pages_match and main.exists and not live_main_match:
        if main.file_path.endswith("code.html") and not (ROOT / main.route.strip("/") / "index.html").exists():
            return "MAIN AHEAD", "Live=gh-pages; main has newer code.html source not yet deployed"
        return "MAIN AHEAD", "Live=gh-pages; main source differs — review before deploy"

    if live_main_match and pages.exists and live.content_hash != pages.content_hash:
        return "GH-PAGES STALE", "Live matches main but gh-pages branch out of date"

    if not pages.exists and main.exists and live.exists:
        if live.content_hash == main.content_hash:
            return "LIVE AHEAD", "Live serves content not on current gh-pages (manual/prior deploy)"
        return "MAIN AHEAD", "Main has source; gh-pages missing — deploy needed"

    if live.exists and pages.exists and live.content_hash != pages.content_hash:
        if abs(len(live.title) - len(pages.title)) > 0 or live.canonical != pages.canonical:
            return "NEEDS HUMAN REVIEW", "Live diverges from gh-pages — possible CDN partial deploy"
        return "NEEDS HUMAN REVIEW", "Live ≠ gh-pages byte/content hash"

    if not main.exists and live.exists:
        return "LIVE AHEAD", "Production-only route not in main source"

    if main.exists and not pages.exists and live.exists:
        return "MAIN AHEAD", "Deploy main source to gh-pages"

    if main.file_path.endswith("code.html") and pages.file_path.endswith("index.html"):
        if live.content_hash == pages.content_hash:
            return "MATCH", "Main=code.html source; gh-pages/live=deployed index.html"

    return "NEEDS HUMAN REVIEW", "Manual triage required"


def detail_notes(main: PageSignals, pages: PageSignals, live: PageSignals) -> list[str]:
    notes: list[str] = []
    if main.exists and main.file_path.endswith("code.html"):
        idx = ROOT / main.route.strip("/") / "index.html"
        if not idx.is_file():
            notes.append(f"main source={main.file_path} (no index.html)")
    if live.exists and pages.exists and live.content_hash != pages.content_hash:
        notes.append(f"hash live={live.content_hash} gh-pages={pages.content_hash}")
    if main.exists and live.exists and main.content_hash != live.content_hash:
        notes.append(f"hash main={main.content_hash} live={live.content_hash}")
    if live.exists and normalize_canonical(live.canonical, live.route) != "OK":
        notes.append(f"live canonical={live.canonical}")
    if main.exists and pages.exists:
        if main.title and pages.title and normalize_title(main.title) != normalize_title(pages.title):
            notes.append(f"title drift main≠gh-pages")
        if set(main.key_images[:5]) != set(pages.key_images[:5]):
            notes.append(f"image set differs")
    for src, sig in (("live", live), ("main", main), ("gh-pages", pages)):
        if sig.exists and not sig.phone_present:
            notes.append(f"{src} missing phone")
        if sig.exists and not sig.email_present:
            notes.append(f"{src} missing email")
    return notes


def main_cli() -> int:
    rows: list[dict[str, str]] = []
    print("| ROUTE | MAIN | GH-PAGES | LIVE | STATUS | ACTION |")
    print("|-------|------|----------|------|--------|--------|")

    for route in ROUTES:
        m = load_main(route)
        g = load_ghpages(route)
        l = load_live(route)
        status, action = compare_route(m, g, l)
        notes = detail_notes(m, g, l)
        if notes:
            action = action + "; " + "; ".join(notes[:3])

        main_col = m.summary() if m.exists else (m.error or "MISSING")
        g_col = g.summary() if g.exists else (g.error or "MISSING")
        l_col = l.summary() if l.exists else (l.error or "MISSING")

        print(f"| `{route}` | {main_col} | {g_col} | {l_col} | **{status}** | {action} |")

        rows.append(
            {
                "route": route,
                "main_exists": str(m.exists),
                "main_path": m.file_path,
                "main_title": m.title,
                "main_canonical": m.canonical,
                "main_h1": m.h1,
                "main_hash": m.content_hash,
                "ghpages_exists": str(g.exists),
                "ghpages_path": g.file_path,
                "ghpages_title": g.title,
                "ghpages_hash": g.content_hash,
                "live_status": str(l.http_status or ""),
                "live_title": l.title,
                "live_canonical": l.canonical,
                "live_h1": l.h1,
                "live_hash": l.content_hash,
                "status": status,
                "action": action,
            }
        )

    out = ROOT / "audits" / "three-way-reconciliation-2026-08-30.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    import csv

    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_cli())
