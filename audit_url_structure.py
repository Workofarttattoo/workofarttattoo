#!/usr/bin/env python3
"""Audit deploy URL slugs — underscores, length, canonical, recommended aliases."""

from __future__ import annotations

import csv
import re
from pathlib import Path

from woa_sitemap import discover_deploy_urls
from woa_url_aliases import ALIASES_BY_SOURCE

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "audit_url_structure.csv"


def slug_issues(slug: str) -> list[str]:
    issues: list[str] = []
    if "_" in slug:
        issues.append("underscores")
    if len(slug) > 45:
        issues.append("long_slug")
    if slug.count("_") >= 4:
        issues.append("keyword_stuffed")
    if "authority_guide" in slug or "expert_guide" in slug:
        issues.append("boilerplate_suffix")
    return issues


def recommend_short(slug: str) -> str:
    if slug in ALIASES_BY_SOURCE:
        return ALIASES_BY_SOURCE[slug].short_slug
    parts = slug.replace("_las_vegas_authority_guide", "")
    parts = parts.replace("_master_authority_guide", "")
    parts = parts.replace("_ultimate_authority_guide", "")
    parts = parts.replace("_expert_aftercare_guide", "")
    parts = parts.replace("_expert_guide", "")
    parts = parts.replace("_authority_guide", "")
    parts = parts.replace("_las_vegas", "")
    parts = parts.replace("_", "-")
    while "--" in parts:
        parts = parts.replace("--", "-")
    return parts.strip("-")[:50]


def has_canonical(code: Path) -> bool:
    if not code.is_file():
        return False
    head = code.read_text(encoding="utf-8", errors="replace")[:8000]
    return 'rel="canonical"' in head


def main() -> int:
    rows: list[dict[str, str]] = []
    for path, _pri, _freq in discover_deploy_urls(ROOT):
        slug = path.strip("/")
        if not slug:
            slug = "(homepage)"
            folder = ROOT / "home_work_of_art_tattoo_piercing"
        elif slug.startswith("knowledge/"):
            folder = ROOT / slug.split("/", 1)[0] / slug.split("/", 1)[1]
            slug = slug  # noqa: PLW0127
        else:
            folder = ROOT / slug
        code = folder / "code.html"
        issues = slug_issues(slug) if slug != "(homepage)" else []
        alias = ALIASES_BY_SOURCE.get(slug)
        rows.append(
            {
                "url_path": path,
                "slug_length": str(len(slug)) if slug != "(homepage)" else "0",
                "issues": ";".join(issues) if issues else "ok",
                "has_canonical": "yes" if has_canonical(code) else "no",
                "recommended_short_slug": alias.short_slug if alias else recommend_short(slug),
                "alias_live": "yes" if alias else "planned",
                "priority": "P0" if "tattoo_healing_in_desert" in slug else ("P1" if issues else "P2"),
            }
        )

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    bad = sum(1 for r in rows if r["issues"] != "ok")
    print(f"Wrote {OUT} ({len(rows)} URLs, {bad} with slug issues)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
