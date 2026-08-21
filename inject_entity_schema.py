#!/usr/bin/env python3
"""Inject unified entity @graph JSON-LD across static HTML exports."""

from __future__ import annotations

import re
from pathlib import Path

from woa_entity_schema import (
    artist_profile_graph,
    artists_index_graph,
    extract_faqs_from_html,
    guide_article_graph,
    schema_script,
    sitewide_graph,
)
from woa_nav_config import GUIDE_META, HOME_SLUG

ROOT = Path(__file__).resolve().parent
MARKER = 'data-woa-entity-schema="1"'
SKIP_PARTS = frozenset({"skipped_upload_build", ".git", "__pycache__"})
LD_JSON_RE = re.compile(
    r'<script(?:\s[^>]*?)?(?:\sdata-woa-entity-schema="1")?(?:\s[^>]*?)?type="application/ld\+json"[^>]*>.*?</script>\s*',
    re.DOTALL | re.IGNORECASE,
)


def iter_targets() -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(p in SKIP_PARTS for p in path.parts):
            continue
        if path.name not in {"code.html"} and path.parent.name != "artists_build":
            continue
        out.append(path)
    if (ROOT / "artists" / "code.html").is_file():
        out.append(ROOT / "artists" / "code.html")
    return sorted(set(out))


def pick_graph(path: Path, html: str) -> dict:
    rel = path.relative_to(ROOT)
    if rel == Path("artists/code.html"):
        return artists_index_graph()
    if rel.parts[0] == "artists_build":
        slug = path.stem
        if slug == "joshua-cole":
            return artist_profile_graph("joshua", root=ROOT)
        if slug == "katelyn-cole":
            return artist_profile_graph("katelyn", root=ROOT)
    slug = rel.parts[0] if len(rel.parts) > 1 else ""
    if rel.parts[0] == "knowledge" and len(rel.parts) >= 3:
        slug = rel.parts[1]
    if slug in GUIDE_META:
        title, desc = GUIDE_META[slug]
        author = None
        if "piercing" in slug or "katelyn" in slug.lower():
            from woa_entity_schema import ID_KATELYN

            author = ID_KATELYN
        faqs = extract_faqs_from_html(html)
        return guide_article_graph(
            slug=slug,
            title=title,
            description=desc,
            author_id=author,
            faqs=faqs or None,
            root=ROOT,
        )
    return sitewide_graph()


SKIP_SCHEMA_REPLACE = frozenset(
    {
        "cover_up_tattoos_las_vegas_master_authority_guide",
        "geo_hub_ai_source_of_truth_work_of_art",
    }
)


def inject_schema(html: str, graph: dict, *, replace_all: bool = True) -> str:
    block = schema_script(graph).replace(
        "<script",
        f'<script {MARKER}',
        1,
    )
    if replace_all:
        cleaned = LD_JSON_RE.sub("", html)
    else:
        cleaned = html
    if "</head>" in cleaned:
        return cleaned.replace("</head>", block + "\n</head>", 1)
    return cleaned.replace("</body>", block + "\n</body>", 1)


def patch_geo_hub_employee_count(html: str) -> str:
    return html.replace('"numberOfEmployees": 3,', '"numberOfEmployees": 2,')


def main() -> int:
    changed = 0
    for path in iter_targets():
        raw = path.read_text(encoding="utf-8")
        slug = path.parent.name if path.name == "code.html" else path.stem
        if path.relative_to(ROOT).parts[0] == "artists_build":
            slug = path.stem
        if slug in SKIP_SCHEMA_REPLACE:
            updated = patch_geo_hub_employee_count(raw) if "geo_hub" in slug else raw
            if updated != raw:
                path.write_text(updated, encoding="utf-8")
                changed += 1
                print(f"[patch] {path.relative_to(ROOT)}")
            continue
        graph = pick_graph(path, raw)
        updated = inject_schema(raw, graph, replace_all=True)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ok] {path.relative_to(ROOT)}")
    print(f"Done: {changed} file(s) with entity schema")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
