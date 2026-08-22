#!/usr/bin/env python3
"""Swap repeated lion tiles for topic-matched portfolio images; repair broken curated HTML."""

from __future__ import annotations

import re
from pathlib import Path

from woa_nav_config import GUIDE_META
from woa_page_portfolio import curated_tile, pick_images, seo_alt, topic_for_slug

ROOT = Path(__file__).resolve().parent
LION = "black-grey-lion-thigh-realism-las-vegas"

BROKEN_NESTED_RE = re.compile(r"</picture>\s*<a class=\"woa-curated-tile group\"")
FULL_SECTION_RE = re.compile(
    r"<!-- WOA_CURATED_PORTFOLIO_START -->[\s\S]*?<!-- WOA_CURATED_PORTFOLIO_END -->"
)
BROKEN_TAIL_RE = re.compile(
    r"(?:<!-- Artist Spotlight -->\s*"
    r"<section[^>]*>\s*<div class=\"relative group\">[\s\S]*?)?"
    r"<a class=\"woa-curated-tile group\"[\s\S]*?<!-- WOA_CURATED_PORTFOLIO_END -->"
)
ORPHAN_SPOTLIGHT_RE = re.compile(
    r"<!-- Artist Spotlight -->\s*"
    r"<section class=\"py-section-gap px-margin-mobile md:px-margin-desktop grid grid-cols-1 md:grid-cols-2 items-center gap-20\">\s*"
    r"<div class=\"relative group\">\s*"
    r"<div class=\"absolute -top-4 -left-4 w-full h-full border border-secondary transition-transform group-hover:translate-x-2 group-hover:translate-y-2\"></div>\s*"
    r"<span>[^<]*</span>"
)
PICTURE_LION_RE = re.compile(
    rf"<picture>[\s\S]*?{re.escape(LION)}[\s\S]*?</picture>",
    re.IGNORECASE,
)
CURATED_GRID_RE = re.compile(
    r'(<div class="woa-curated-grid">)(.*?)(</div>)',
    re.DOTALL,
)


def page_label(slug: str) -> str:
    if slug in GUIDE_META:
        return GUIDE_META[slug][0]
    return slug.replace("_", " ").title()


def section_heading(topic: str) -> str:
    return {
        "piercing": "Piercing & jewelry from our chair",
        "healing": "Fresh & healed studio work",
        "cover_up": "Cover-up transformations",
        "realism": "Black & grey realism portfolio",
        "fine_line": "Fine-line tattoo work",
    }.get(topic, "Verified studio work")


def section_blurb(topic: str) -> str:
    return {
        "piercing": "Ear curation, facial piercing, and implant-grade jewelry — documented by Katelyn Cole in our Las Vegas studio.",
        "healing": "Fresh and healed photos from the same clients — what desert-climate aftercare looks like when it is done right.",
        "cover_up": "Redesigns and camouflage work from consult through healed photos.",
        "realism": "Portraits, wildlife, and large-scale black and grey pieces by Joshua Cole.",
        "fine_line": "Delicate linework and small custom pieces from our Las Vegas portfolio.",
    }.get(topic, "Real client work from the studio, photographed so you can see the style before you book.")


def gallery_href(topic: str) -> str:
    if topic == "piercing":
        return "/studio_gallery/#katelyn-piercing"
    return "/studio_gallery/"


def build_tiles(slug: str, count: int = 4) -> str:
    topic = topic_for_slug(slug)
    images = pick_images(slug, count)
    label = page_label(slug)
    href = gallery_href(topic)
    return "".join(curated_tile(img, label, href) for img in images)


def curated_section_html(slug: str, *, include_markers: bool = True) -> str:
    topic = topic_for_slug(slug)
    tiles = build_tiles(slug, 4)
    href = gallery_href(topic)
    body = f"""<section class="woa-curated-portfolio py-12 md:py-16 px-6 md:px-12 bg-surface-container-low" data-woa-curated="1">
<div class="max-w-6xl mx-auto space-y-6">
<div class="text-center space-y-2 max-w-2xl mx-auto">
<p class="text-secondary text-xs uppercase tracking-[0.2em]">Verified studio work</p>
<h2 class="font-headline-md text-2xl md:text-3xl text-on-surface">{section_heading(topic)}</h2>
<p class="text-on-surface-variant text-sm">{section_blurb(topic)}</p>
</div>
<div class="woa-curated-grid">{tiles}</div>
<p class="text-center pt-4"><a class="text-secondary text-xs uppercase tracking-widest hover:underline" href="{href}">View full studio gallery</a></p>
</div>
</section>"""
    if include_markers:
        return f"<!-- WOA_CURATED_PORTFOLIO_START -->\n{body}\n<!-- WOA_CURATED_PORTFOLIO_END -->"
    return body


def has_broken_tiles(html: str) -> bool:
    return bool(BROKEN_NESTED_RE.search(html))


def replace_curated_grid(html: str, slug: str) -> tuple[str, bool]:
    topic = topic_for_slug(slug)
    if topic == "general" and LION not in html and not has_broken_tiles(html):
        return html, False
    tiles = build_tiles(slug, 4)
    new_grid = f'<div class="woa-curated-grid">{tiles}</div>'
    if 'class="woa-curated-grid"' not in html:
        return html, False
    html2, n = CURATED_GRID_RE.subn(new_grid, html, count=1)
    return html2, n > 0


def is_corrupted_curated(segment: str) -> bool:
    if "Real work from this studio" in segment:
        return True
    tiles = segment.count('<a class="woa-curated-tile group"')
    closes = segment.count("</span></a>")
    if tiles and closes < tiles:
        return True
    if "woa-curated-grid" in segment and "<!-- WOA_CURATED_PORTFOLIO_START -->" in segment:
        start = segment.find("<!-- WOA_CURATED_PORTFOLIO_START -->")
        grid = segment.find('class="woa-curated-grid"', start)
        if grid != -1 and grid < start:
            return True
    return False


def repair_curated_block(html: str, slug: str) -> tuple[str, bool]:
    """Replace broken or stale curated regions with a clean section."""
    if "<!-- WOA_CURATED_PORTFOLIO_START -->" in html:
        block = FULL_SECTION_RE.search(html)
        if not block:
            return html, False
        segment = block.group(0)
        if is_corrupted_curated(segment) or has_broken_tiles(segment) or topic_for_slug(slug) != "realism":
            html2 = FULL_SECTION_RE.sub(curated_section_html(slug), html, count=1)
            return html2, True
        return html, False

    if "<!-- WOA_CURATED_PORTFOLIO_END -->" in html and (
        has_broken_tiles(html) or (topic_for_slug(slug) != "realism" and LION in html)
    ):
        html2, n = BROKEN_TAIL_RE.subn(curated_section_html(slug), html, count=1)
        if n:
            return html2, True

    if has_broken_tiles(html):
        cluster = re.compile(
            r'<a class="woa-curated-tile group"[\s\S]*?(?=<p class="text-center pt-4")'
        )
        tiles = build_tiles(slug, 4)
        html2, n = cluster.subn(f'<div class="woa-curated-grid">{tiles}</div>\n', html, count=1)
        if n:
            return html2, True

    return replace_curated_grid(html, slug)


STYLE_SELECTOR_BROKEN_RE = re.compile(
    r"<!-- Style Selector \(Interactive\) -->[\s\S]*?<!-- WOA_CURATED_PORTFOLIO_END -->"
)
STYLE_SELECTOR_NO_END_RE = re.compile(
    r"<!-- Style Selector \(Interactive\) -->[\s\S]*?(?=<footer)"
)
NESTED_CURATED_WRAPPER_RE = re.compile(
    r'<div class="my-12">\s*<div class="woa-curated-grid"><!-- WOA_CURATED_PORTFOLIO_START -->[\s\S]*?<!-- WOA_CURATED_PORTFOLIO_END -->\s*</div>'
)


def repair_style_selector(html: str, slug: str) -> tuple[str, bool]:
    if "<!-- Style Selector (Interactive) -->" not in html:
        return html, False
    html2, n = STYLE_SELECTOR_BROKEN_RE.subn(curated_section_html(slug), html, count=1)
    if n:
        return html2, True
    html2, n = STYLE_SELECTOR_NO_END_RE.subn(curated_section_html(slug), html, count=1)
    return html2, n > 0


def repair_nested_wrapper(html: str, slug: str) -> tuple[str, bool]:
    html2, n = NESTED_CURATED_WRAPPER_RE.subn(curated_section_html(slug), html, count=1)
    return html2, n > 0


def replace_lion_images(html: str, slug: str) -> tuple[str, bool]:
    """Swap remaining lion <picture> blocks on non-realism pages (never inside proof blocks)."""
    if topic_for_slug(slug) == "realism":
        return html, False
    if LION not in html:
        return html, False

    images = pick_images(slug, 8)
    if not images:
        return html, False

    label = page_label(slug)
    parts = re.split(
        r'(<section[^>]*data-woa-(?:proof-block|healed-stories)="1"[\s\S]*?</section>)',
        html,
    )
    changed = False
    out: list[str] = []
    idx = 0

    def repl_picture(_: re.Match[str]) -> str:
        nonlocal idx
        from woa_page_portfolio import picture_tag

        img = images[idx % len(images)]
        idx += 1
        return picture_tag(img, label)

    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append(part)
            continue
        part2 = PICTURE_LION_RE.sub(repl_picture, part)
        if part2 != part:
            changed = True
        out.append(part2)

    return "".join(out), changed


def strip_orphan_spotlight(html: str) -> tuple[str, bool]:
    html2, n = ORPHAN_SPOTLIGHT_RE.subn("", html)
    return html2, n > 0


def iter_pages() -> list[tuple[Path, str]]:
    out: list[tuple[Path, str]] = []
    for folder in sorted(ROOT.iterdir()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        code = folder / "code.html"
        if code.is_file():
            out.append((code, folder.name))
    return out


def main() -> int:
    changed = 0
    for path, slug in iter_pages():
        raw = path.read_text(encoding="utf-8")
        html = raw
        ok = False
        html, n1 = repair_curated_block(html, slug)
        ok = ok or n1
        html, n1b = repair_style_selector(html, slug)
        ok = ok or n1b
        html, n1c = repair_nested_wrapper(html, slug)
        ok = ok or n1c
        html, n2 = replace_lion_images(html, slug)
        ok = ok or n2
        html, n3 = strip_orphan_spotlight(html)
        ok = ok or n3
        if ok and html != raw:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print(f"[ok] {slug} ({topic_for_slug(slug)})")
    print(f"Done: {changed} page(s) contextual portfolio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
