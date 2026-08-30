#!/usr/bin/env python3
"""Full customer-facing site QA — machine-readable report by severity."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from woa_geo_pages import GEO_PAGE_ACTIONS, GEO_PAGE_REDIRECTS
from woa_nav_config import STUDIO_STREET_ADDRESS
from woa_page_consolidation import RETIRE_OVERLAP_SLUGS
from tools.seo_qa import (
    ARTIST_NAMES,
    ARTIST_COUNT,
    CANONICAL_HOST,
    CANONICAL_NETLOC,
    FORBIDDEN,
    GEO_STALE_RE,
    INTERNAL_HOSTS,
    MERGED_GEO_SLUGS,
    OLD_COVERUP_IMAGE_RE,
    PIERCING_ASSET_RE,
    PIERCING_ROUTE_RE,
    REVIEW_COUNT,
    SKIN_SCIENCE_ROUTE_RE,
    TATTOO_PROOF_IMAGE_RE,
    VISIBLE_ONLY_FORBIDDEN,
    load_retired_slugs,
    published_routes,
    route_for,
    slug_for_path,
    visible_text,
)

AUDITS = ROOT / "audits"
REPORT_PATH = AUDITS / "customer-site-qa-report.json"

IMAGE_EXT_RE = re.compile(r"\.(?:png|jpe?g|webp|gif|avif)(?:\s|$|\?)", re.I)
DEPRECATED_PHONE_RE = re.compile(
    r"725[-\s.]224[-\s.]2617|725[-\s.]224[-\s.]2931|725[-\s.]260[-\s.]6376|702[-\s.]960[-\s.]9607",
    re.I,
)
JAY_JAY_RE = re.compile(r"Jay\s*Jay|jay_jay_artist_portfolio", re.I)
COVER_UNDERSCORE_BODY_RE = re.compile(r"/cover_up_tattoos_las_vegas_master_authority_guide/", re.I)
PIERCING_TATTOO_FOOTER_RE = re.compile(
    r"Photos from Work of Art tattoo clients[\s\S]{0,120}healed_tattoo_gallery_las_vegas",
    re.I,
)
STALE_BUTTERFLY_COVER_RE = re.compile(
    r"cover-up-tattoo-faded-butterflies-hand-before|cover-up-tattoo-faded-floral-leg-before|"
    r"blue-butterfly-color-tattoo-rework-las-vegas|color-butterfly-back-tattoo-las-vegas|"
    r"realism-tattoos-color-butterfly-and-floral-coverup|"
    r"cover-up-tattoo-sunflower-over-black-ink-las-vegas",
    re.I,
)
MALFORMED_COPY_RE = re.compile(
    r"Too deep:\s*pigment can spread[^.<]{0,200}trauma\.el\s|"
    r"Can you tattoo Too deep:|"
    r"&lt;&gt;|&lt; &gt;",
    re.I,
)


@dataclass
class Finding:
    severity: str
    category: str
    route: str
    file: str
    message: str
    evidence: str = ""

    def as_dict(self) -> dict:
        return {
            "severity": self.severity,
            "category": self.category,
            "route": self.route,
            "file": self.file,
            "message": self.message,
            "evidence": self.evidence,
        }


@dataclass
class Report:
    generated_at: str
    pages_scanned: int
    routes_in_sitemap: int
    findings: list[Finding] = field(default_factory=list)

    def add(self, severity: str, category: str, route: str, file: str, message: str, evidence: str = "") -> None:
        self.findings.append(Finding(severity, category, route, file, message, evidence))

    def grouped(self) -> dict[str, list[dict]]:
        out: dict[str, list[dict]] = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": []}
        for f in self.findings:
            out.setdefault(f.severity, []).append(f.as_dict())
        return out

    def summary(self) -> dict:
        grouped = self.grouped()
        return {k: len(grouped.get(k, [])) for k in ("CRITICAL", "HIGH", "MEDIUM", "LOW")}


def html_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("code.html") if ".git" not in p.parts)


def route_exists(route: str, published: set[str]) -> bool:
    if route.startswith("#") or route.startswith("mailto:") or route.startswith("tel:"):
        return True
    if not route.startswith("/"):
        return True
    path = route.split("#")[0].split("?")[0]
    if not path.endswith("/"):
        path += "/"
    if path in published:
        return True
    slug = path.strip("/")
    if slug in load_retired_slugs() or slug in MERGED_GEO_SLUGS or slug in RETIRE_OVERLAP_SLUGS:
        return True
    candidate = ROOT / slug / "code.html"
    if slug == "":
        candidate = ROOT / "code.html"
    return candidate.is_file()


def resolve_asset(href: str) -> Path | None:
    if not href or href.startswith(("http://", "https://", "data:", "//")):
        return None
    clean = href.split("?")[0].split("#")[0]
    if not clean.startswith("/"):
        return None
    return ROOT / clean.lstrip("/")


def collect_image_refs(soup: BeautifulSoup, raw: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    for tag in soup.find_all(["img", "source"]):
        for attr in ("src", "srcset"):
            val = tag.get(attr)
            if val:
                refs.append((str(val), tag.get("alt", "") or ""))
    for tag in soup.find_all(style=True):
        style = str(tag.get("style") or "")
        if "url(" in style:
            refs.append((style, ""))
    return refs


def audit_page(path: Path, report: Report, published: set[str], contact: dict, business: dict) -> None:
    slug = slug_for_path(path)
    route = route_for(path)
    rel = str(path.relative_to(ROOT))
    if slug in MERGED_GEO_SLUGS:
        return
    if slug in load_retired_slugs():
        return
    if published and route not in published:
        return

    raw = path.read_text(encoding="utf-8", errors="ignore")
    if "<<<<<<< HEAD" in raw:
        report.add("CRITICAL", "malformed_copy", route, rel, "Unresolved git merge conflict markers in HTML")

    if path == ROOT / "code.html" and (ROOT / "home_work_of_art_tattoo_piercing" / "code.html").is_file():
        return

    soup = BeautifulSoup(raw, "html.parser")
    body_text = visible_text(BeautifulSoup(raw, "html.parser"))

    # Stale deploy artifact: index.html out of sync with source page
    source = path
    if route == "/" and path == ROOT / "code.html":
        source = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
    idx = path.parent / "index.html"
    if route == "/":
        idx = ROOT / "index.html"
    if idx.is_file() and source.is_file():
        idx_raw = idx.read_text(encoding="utf-8", errors="ignore")
        src_raw = source.read_text(encoding="utf-8", errors="ignore")
        if idx_raw != src_raw:
            report.add(
                "HIGH",
                "stale_deploy_artifact",
                route,
                str(idx.relative_to(ROOT)),
                "index.html does not match code.html (customers may see outdated content)",
            )

    for label, pattern in FORBIDDEN.items():
        haystack = body_text if label in VISIBLE_ONLY_FORBIDDEN else raw
        if re.search(pattern, haystack, re.I):
            report.add("HIGH", "forbidden_content", route, rel, f"Forbidden pattern: {label}")

    if JAY_JAY_RE.search(body_text) or JAY_JAY_RE.search(raw):
        report.add("CRITICAL", "stale_roster", route, rel, "Jay Jay reference on current roster or retired artist page")

    if MALFORMED_COPY_RE.search(raw):
        report.add("HIGH", "malformed_copy", route, rel, "Malformed or corrupted copy detected")

    if PIERCING_ROUTE_RE.search(route) and PIERCING_TATTOO_FOOTER_RE.search(raw):
        report.add(
            "HIGH",
            "visual_intent",
            route,
            rel,
            "Piercing placement guide links to healed tattoo gallery in proof-strip footer",
        )

    if PIERCING_ROUTE_RE.search(route):
        refs = collect_image_refs(soup, raw)
        joined = "\n".join(f"{r} {a}" for r, a in refs)
        if any(TATTOO_PROOF_IMAGE_RE.search(r) for r, _ in refs):
            report.add("HIGH", "visual_intent", route, rel, "Piercing page contains tattoo proof imagery")
        if SKIN_SCIENCE_ROUTE_RE.search(route) and PIERCING_ASSET_RE.search(joined):
            report.add("MEDIUM", "visual_intent", route, rel, "Skin-science page contains piercing imagery")

    if OLD_COVERUP_IMAGE_RE.search(raw):
        report.add("MEDIUM", "stale_media", route, rel, "Stale generic cover-up image reference")

    if STALE_BUTTERFLY_COVER_RE.search(raw):
        report.add("MEDIUM", "stale_media", route, rel, "Stale butterfly/flower cover-up before image reference")

    # Canonical / head
    canonical = soup.find("link", rel="canonical")
    if not canonical:
        report.add("HIGH", "bad_canonical", route, rel, "Missing canonical link")
    else:
        href = canonical.get("href", "")
        if href and urlparse(href).netloc and urlparse(href).netloc != CANONICAL_NETLOC:
            report.add("HIGH", "bad_canonical", route, rel, f"Canonical host mismatch: {href}")
        if slug and f"/{slug}/" not in href and route != "/":
            if not any(x in href for x in ("/walk-in-tattoos-las-vegas/", "/cover-up-tattoos-las-vegas/")):
                report.add("MEDIUM", "bad_canonical", route, rel, f"Canonical may not match route: {href}")

    h1s = soup.find_all("h1")
    if len(h1s) != 1:
        report.add("MEDIUM", "duplicate_headings", route, rel, f"Expected 1 h1, found {len(h1s)}")

    h2_texts = [visible_text(BeautifulSoup(str(h), "html.parser")) for h in soup.find_all("h2")]
    dup_h2 = sorted({t for t in h2_texts if t and h2_texts.count(t) > 1})
    if dup_h2:
        report.add("LOW", "duplicate_headings", route, rel, f"Duplicate h2: {dup_h2[0][:80]}")

    # NAP
    phone_canon = contact.get("phoneDisplay", "")
    email_canon = contact.get("bookingEmail", "")
    if phone_canon and phone_canon not in raw and route in {
        "/official_location_hours_contact/",
        "/appointments/",
        "/",
    }:
        report.add("MEDIUM", "contact_info", route, rel, "Canonical phone not found on key NAP page")
    if DEPRECATED_PHONE_RE.search(raw):
        report.add("CRITICAL", "contact_info", route, rel, "Deprecated phone number present")

    if email_canon and "booking@workofarttattoo.com" in raw:
        report.add("HIGH", "contact_info", route, rel, "Disconnected booking@workofarttattoo.com email")

    # Internal links
    for a in soup.find_all("a", href=True):
        href = a.get("href", "").strip()
        if not href or href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
            if href.startswith("http"):
                netloc = urlparse(href).netloc
                if netloc in INTERNAL_HOSTS and netloc != CANONICAL_NETLOC:
                    report.add("MEDIUM", "broken_internal_links", route, rel, f"Internal link wrong host: {href}")
            continue
        if href.startswith("/") and not route_exists(href, published):
            report.add("HIGH", "broken_internal_links", route, rel, f"Broken internal link: {href}", href)

    if COVER_UNDERSCORE_BODY_RE.search(raw) and "piercing" in route.lower():
        report.add("LOW", "obsolete_urls", route, rel, "Underscore cover-up authority URL in piercing page body")

    # Images
    for ref, alt in collect_image_refs(soup, raw):
        for part in re.split(r"[\s,]+", ref):
            if not IMAGE_EXT_RE.search(part):
                if "url(" in part:
                    m = re.search(r"url\(['\"]?([^)'\"]+)", part)
                    if m:
                        part = m.group(1)
                else:
                    continue
            asset = resolve_asset(part)
            if asset and not asset.is_file():
                report.add("HIGH", "missing_images", route, rel, f"Missing image asset: {part}", part)

    # JSON-LD
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        block = (script.string or script.get_text() or "").strip()
        if not block:
            continue
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            report.add("HIGH", "malformed_copy", route, rel, f"Malformed JSON-LD: {exc}")

    if GEO_STALE_RE.search(body_text):
        report.add("MEDIUM", "obsolete_urls", route, rel, "Harry Reid International Airport naming (policy: use LAS/Las Vegas Airport)")

    if "Google" in body_text and "review" in body_text.lower():
        visible_counts = {
            int(m.group(1).replace(",", ""))
            for m in re.finditer(
                r"\b(\d{2,4}(?:,\d{3})?)\s+(?:verified\s+)?(?:five-star\s+)?(?:Google\s+)?reviews?\b",
                body_text,
                re.I,
            )
        }
        for count in visible_counts:
            if count != REVIEW_COUNT:
                report.add(
                    "MEDIUM",
                    "unsupported_claims",
                    route,
                    rel,
                    f"Rendered review count {count} contradicts siteData {REVIEW_COUNT}",
                )

    if re.search(r"\b(?:resident\s+artists|artists\s+in-studio)\b", body_text, re.I):
        if str(ARTIST_COUNT) not in body_text and "three" not in body_text.lower():
            report.add("MEDIUM", "stale_roster", route, rel, f"Artist count may contradict siteData ({ARTIST_COUNT})")
        missing = [name for name in ARTIST_NAMES if name.split()[0] not in body_text]
        if missing and "resident" in body_text.lower():
            report.add("MEDIUM", "stale_roster", route, rel, f"Incomplete roster near roster copy: {', '.join(missing)}")


def audit_sitewide(report: Report, published: set[str]) -> None:
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.is_file():
        report.add("CRITICAL", "broken_internal_links", "/", "sitemap.xml", "Missing sitemap.xml")
        return

    for slug in MERGED_GEO_SLUGS | RETIRE_OVERLAP_SLUGS:
        if f"/{slug}/" in sitemap.read_text(encoding="utf-8", errors="ignore"):
            report.add("HIGH", "obsolete_urls", f"/{slug}/", "sitemap.xml", "Retired URL still in sitemap")

    jay_page = ROOT / "jay_jay_artist_portfolio_authentic_masterpieces" / "code.html"
    if jay_page.is_file() and "/jay_jay_artist_portfolio_authentic_masterpieces/" in published:
        report.add("CRITICAL", "stale_roster", "/jay_jay_artist_portfolio_authentic_masterpieces/", str(jay_page), "Jay Jay portfolio still indexable in sitemap")


def main() -> int:
    contact = json.loads((ROOT / "siteData" / "contact.json").read_text(encoding="utf-8"))
    business = json.loads((ROOT / "siteData" / "business.json").read_text(encoding="utf-8"))
    published = published_routes()

    report = Report(
        generated_at=datetime.now(timezone.utc).isoformat(),
        pages_scanned=0,
        routes_in_sitemap=len(published),
    )

    for path in html_files():
        slug = slug_for_path(path)
        route = route_for(path)
        if slug in MERGED_GEO_SLUGS:
            continue
        if slug in load_retired_slugs():
            continue
        if published and route not in published:
            continue
        report.pages_scanned += 1
        audit_page(path, report, published, contact, business)

    audit_sitewide(report, published)

    AUDITS.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": report.generated_at,
        "pages_scanned": report.pages_scanned,
        "routes_in_sitemap": report.routes_in_sitemap,
        "summary": report.summary(),
        "findings": report.grouped(),
        "canonical_contact": contact,
    }
    REPORT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({"summary": report.summary(), "report": str(REPORT_PATH.relative_to(ROOT))}, indent=2))
    return 1 if report.summary().get("CRITICAL", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
