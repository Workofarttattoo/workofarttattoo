#!/usr/bin/env python3
"""
Refinement pass — no new pages.

- Consolidate overlapping URLs to canonical paths
- Trim topic-cluster / internal-link bloat on guide pages
- Enforce NAP / citation cleanup (5025, old phones)
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from woa_page_consolidation import HREF_REPLACEMENTS

ROOT = Path(__file__).resolve().parent

TOPIC_CLUSTER_RE = re.compile(
    r'<nav[^>]*data-woa-topic-cluster="1"[^>]*>.*?</nav>\s*',
    re.DOTALL,
)
INTERNAL_LINKS_RE = re.compile(
    r'<nav[^>]*data-woa-internal-links="1"[^>]*>.*?</nav>\s*',
    re.DOTALL,
)

# Old directory / listing phone numbers — never publish on-site
CITATION_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("(725) 224-1240", "(725) 224-1240"),
    ("725-224-1240", "725-224-1240"),
    ("725-224-1240", "725-224-1240"),
    ("702.960.9607", "725-224-1240"),
    ("2375 E. Tropicana Suite 3", "2375 E. Tropicana Suite 3"),
    ("2375 E. Tropicana Suite 3", "2375 E. Tropicana Suite 3"),
    ("2375 E. Tropicana Suite 3", "2375 E. Tropicana Suite 3"),
    ("/tattoo_shop_near_the_strip_geo_seo_optimized/", "/tattoo_shop_near_the_strip_nap_corrected/"),
)


def iter_html() -> list[Path]:
    paths: list[Path] = []
    for path in sorted(ROOT.rglob("code.html")):
        if "skipped" in path.parts:
            continue
        paths.append(path)
    paths.extend(sorted((ROOT / "artists_build").glob("*.html")))
    root_home = ROOT / "code.html"
    if root_home.is_file():
        paths.append(root_home)
    return paths


def consolidate_hrefs(html: str) -> str:
    for old, new in HREF_REPLACEMENTS:
        html = html.replace(old, new)
    return html


def clean_citations(html: str) -> str:
    for old, new in CITATION_REPLACEMENTS:
        html = html.replace(old, new)
    return html


def trim_link_bloat(html: str) -> tuple[str, bool]:
    """Drop redundant footer-style link blocks; keep compact hub bar."""
    changed = False
    if 'data-woa-guide-hub-bar="1"' in html and TOPIC_CLUSTER_RE.search(html):
        html = TOPIC_CLUSTER_RE.sub("", html)
        changed = True
    if INTERNAL_LINKS_RE.search(html):
        html = INTERNAL_LINKS_RE.sub("", html)
        changed = True
    return html, changed


def slim_remaining_clusters(html: str) -> tuple[str, bool]:
    """Cap topic clusters at three links where they remain."""

    def repl(m: re.Match[str]) -> str:
        block = m.group(0)
        items = re.findall(
            r'<li><a class="text-secondary underline hover:no-underline" href="([^"]+)">([^<]+)</a></li>',
            block,
        )
        if len(items) <= 3:
            return block
        keep = items[:3]
        lis = "\n".join(
            f'<li><a class="text-secondary underline hover:no-underline" href="{h}">{lbl}</a></li>'
            for h, lbl in keep
        )
        return re.sub(
            r"<ul class=\"font-body-md[^\"]*\"[^>]*>.*?</ul>",
            f'<ul class="font-body-md text-on-surface-variant space-y-2">{lis}</ul>',
            block,
            count=1,
            flags=re.DOTALL,
        )

    new_html, n = TOPIC_CLUSTER_RE.subn(repl, html)
    return new_html, n > 0 and new_html != html


def patch_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    html = consolidate_hrefs(raw)
    html = clean_citations(html)
    html, c1 = trim_link_bloat(html)
    html, c2 = slim_remaining_clusters(html)
    if html != raw:
        path.write_text(html, encoding="utf-8")
        return True
    return c1 or c2


def run_fix_studio_nap() -> None:
    script = ROOT / "fix_studio_nap.py"
    if script.is_file():
        subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)


def main() -> int:
    n = 0
    for path in iter_html():
        if patch_file(path):
            print(f"[ok] {path.relative_to(ROOT)}")
            n += 1
    run_fix_studio_nap()
    print(f"\nRefinement complete — updated {n} file(s).")
    print("Deploy to apply 301 rules for retired overlap pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
