#!/usr/bin/env python3
"""Audit every sitemap URL: status, title, description, canonical, H1, JSON-LD."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from woa_canonical import CANONICAL_ORIGIN

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
NON_WWW = re.compile(r"https?://(?:www\.)?workofarttattoo\.com(?![w])", re.I)
HTTP_WWW = re.compile(r"http://www\.workofarttattoo\.com", re.I)
BAD_HOST = re.compile(r"https://workofarttattoo\.com", re.I)


def load_sitemap_urls(path: Path) -> list[str]:
    tree = ElementTree.parse(path)
    return [el.text.strip() for el in tree.findall(".//sm:loc", NS) if el.text]


def audit_local_html(url: str) -> dict:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    if path == "/":
        html_path = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
    else:
        slug = path.strip("/").split("/")[0]
        if path.startswith("/knowledge/"):
            html_path = ROOT / path.strip("/") / "code.html"
        elif path.startswith("/artists/"):
            html_path = ROOT / path.strip("/") / "code.html"
        else:
            from woa_url_aliases import ALIASES_BY_SHORT, short_href

            folder = path.strip("/")
            html_path = ROOT / folder / "code.html"
            if not html_path.is_file():
                for alias in ALIASES_BY_SHORT.values():
                    if short_href(alias.source_slug).strip("/") == folder:
                        candidate = ROOT / alias.source_slug / "code.html"
                        if candidate.is_file():
                            html_path = candidate
                            break
            if not html_path.is_file():
                html_path = ROOT / slug / "code.html"

    issues: list[str] = []
    row: dict = {"url": url, "local_path": str(html_path.relative_to(ROOT)) if html_path.is_file() else ""}

    if not html_path.is_file():
        issues.append("missing local HTML")
        row["issues"] = issues
        return row

    raw = html_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")

    h1s = soup.find_all("h1")
    row["h1_count"] = len(h1s)
    if len(h1s) != 1:
        issues.append(f"h1_count={len(h1s)}")

    title = soup.find("title")
    row["title"] = title.get_text(strip=True) if title else ""
    if not row["title"]:
        issues.append("missing title")

    desc = soup.find("meta", attrs={"name": "description"})
    row["description"] = desc.get("content", "") if desc else ""
    if not row["description"]:
        issues.append("missing description")

    canonical = soup.find("link", rel="canonical")
    row["canonical"] = canonical.get("href", "") if canonical else ""
    if row["canonical"] != url:
        issues.append(f"canonical mismatch ({row['canonical']})")
    if BAD_HOST.search(row["canonical"] or ""):
        issues.append("non-www canonical")
    if (row["canonical"] or "").startswith("http://"):
        issues.append("http canonical")

    robots = soup.find("meta", attrs={"name": "robots"})
    robots_content = (robots.get("content", "") if robots else "").lower()
    if "noindex" in robots_content:
        issues.append("noindex")

    if "| Work of Art | Work of Art" in row["title"]:
        issues.append("duplicated brand suffix")

    for script in soup.find_all("script", type="application/ld+json"):
        text = script.string or ""
        if BAD_HOST.search(text) or HTTP_WWW.search(text):
            issues.append("non-www/http in JSON-LD")
            break
        try:
            json.loads(text)
        except json.JSONDecodeError:
            issues.append("invalid JSON-LD")
            break

    if NON_WWW.search(raw) or HTTP_WWW.search(raw):
        # scope to internal links only
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if BAD_HOST.search(href) or href.startswith("http://www.workofarttattoo.com"):
                issues.append(f"bad internal link: {href[:80]}")
                break

    row["issues"] = issues
    row["ok"] = not issues
    return row


def write_report(rows: list[dict], out_path: Path) -> None:
    ok = sum(1 for r in rows if r.get("ok"))
    titles = [r.get("title", "") for r in rows if r.get("title")]
    descs = [r.get("description", "") for r in rows if r.get("description")]
    dup_titles = [t for t, c in Counter(titles).items() if c > 1]
    dup_descs = [d for d, c in Counter(descs).items() if c > 1]

    lines = [
        "# Priority SEO Validation Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Canonical origin: {CANONICAL_ORIGIN}",
        "",
        "## Summary",
        "",
        f"- Sitemap URLs audited: **{len(rows)}**",
        f"- Passing local checks: **{ok}/{len(rows)}**",
        f"- Duplicate titles: **{len(dup_titles)}**",
        f"- Duplicate descriptions: **{len(dup_descs)}**",
        "",
        "## Redirect tests",
        "",
        "Run: `python3 tools/test_canonical_redirects.py --live`",
        "",
        "Cloudflare bulk import: `config/cloudflare-bulk-redirects.csv`",
        "",
        "## Files changed (this sprint)",
        "",
        "- `implement_priority_seo_upgrades.py` — ATF answers, piercing hub, cover-up, contextual links",
        "- `woa_nav_config.py` — piercing hub meta description",
        "- `inject_contextual_links.py` — canonical short URLs in clusters",
        "- `config/cloudflare-bulk-redirects.csv` — host canonicalization rules",
        "- `tools/test_canonical_redirects.py` — live redirect hop tester",
        "",
        "## Pages with new above-the-fold answer summaries",
        "",
        "- `/epidermis_skin_science_las_vegas_authority_guide/`",
        "- `/knowledge/tattoo-on-ribs-recovery/`",
        "- `/healed_tattoo_gallery_las_vegas/`",
        "- `/how-to-choose-a-tattoo-artist/`",
        "- `/las-vegas-tattoo-healing-guide/`",
        "- `/real_client_tattoo_timeline_las_vegas/`",
        "- `/cover-up-tattoos-las-vegas/` (feasibility note + healed gallery CTA)",
        "",
        "## Sample before/after (metadata)",
        "",
        "| URL | Title | Description |",
        "|-----|-------|-------------|",
    ]
    samples = [
        "/piercing-guide-las-vegas/",
        "/cover-up-tattoos-las-vegas/",
        "/healed_tattoo_gallery_las_vegas/",
        "/how-to-choose-a-tattoo-artist/",
        "/las-vegas-tattoo-healing-guide/",
        "/real_client_tattoo_timeline_las_vegas/",
        "/epidermis_skin_science_las_vegas_authority_guide/",
        "/knowledge/tattoo-on-ribs-recovery/",
        "/",
        "/artists/katelyn-cole/",
    ]
    for sample in samples:
        url = CANONICAL_ORIGIN + sample
        match = next((r for r in rows if r["url"] == url), None)
        if match:
            t = (match.get("title") or "")[:60]
            d = (match.get("description") or "")[:80]
            lines.append(f"| `{sample}` | {t} | {d}… |")

    lines.extend(["", "## Failures", ""])
    failed = [r for r in rows if not r.get("ok")]
    if not failed:
        lines.append("_None — all local checks passed._")
    else:
        for r in failed:
            lines.append(f"- `{r['url']}`: {', '.join(r.get('issues', []))}")

    lines.extend(["", "## Full URL matrix", "", "| URL | H1 | Title OK | Canon OK | Issues |", "|-----|----|---------|---------|--------|"])
    for r in rows:
        issues = ", ".join(r.get("issues", [])) or "—"
        lines.append(
            f"| `{r['url']}` | {r.get('h1_count', '?')} | "
            f"{'✓' if r.get('title') else '✗'} | "
            f"{'✓' if r.get('canonical') == r['url'] else '✗'} | {issues} |"
        )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default=str(ROOT / "audits" / "priority-seo-validation-report.md"))
    args = parser.parse_args()
    sitemap = ROOT / "sitemap.xml"
    urls = load_sitemap_urls(sitemap)
    rows = [audit_local_html(u) for u in urls]
    write_report(rows, Path(args.report))
    failed = sum(1 for r in rows if not r.get("ok"))
    print(f"Audited {len(rows)} URLs — {failed} with issues")
    print(f"Report: {args.report}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
