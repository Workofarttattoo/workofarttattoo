#!/usr/bin/env python3
"""Inject WOA client video (Instagram) section into homepage and portfolio pages."""

from __future__ import annotations

import re
from pathlib import Path

from client_videos import (
    FEATURED_MARKER_END,
    FEATURED_MARKER_START,
    HERO_LEAD_MARKER_END,
    HERO_LEAD_MARKER_START,
    HOME_VIDEO_GRID_MARKER_END,
    HOME_VIDEO_GRID_MARKER_START,
    KATELYN_MARKER_END,
    KATELYN_MARKER_START,
    KATELYN_MINORS_MARKER_END,
    KATELYN_MINORS_MARKER_START,
    MARKER_END,
    MARKER_START,
    PIERCING_VIDEO_MARKER_END,
    PIERCING_VIDEO_MARKER_START,
    VIDEO_REPO_MARKER_END,
    VIDEO_REPO_MARKER_START,
    export_videos_catalog,
    render_featured_section,
    JOSHUA_EDUCATION_MARKER_END,
    JOSHUA_EDUCATION_MARKER_START,
    render_hero_lead_embed,
    render_home_video_grid,
    render_joshua_education_section,
    render_katelyn_minors_section,
    render_katelyn_section,
    render_piercing_section_video,
    render_section,
    render_video_repo_page,
)

ROOT = Path(__file__).resolve().parent
GITHUB = Path("/Users/noone/Downloads/GitHub/workofarttattoo")

HOME = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"

TARGETS: list[tuple[Path, str, bool]] = [
    (HOME, "after_masonry", False),
    (ROOT / "artists" / "code.html", "before_curated", True),
]

KATELYN_PAGE = ROOT / "artists_build" / "katelyn-cole.html"
KATELYN_ANCHOR = "<!-- Specialties Section -->"
KATELYN_MINORS_ANCHOR = "<!-- FAQ Section -->"

JOSHUA_PAGE = ROOT / "artists_build" / "joshua-cole.html"
JOSHUA_EDUCATION_ANCHOR = "<!-- SEO-Rich Comprehensive Biography -->"

MARKER_RE = re.compile(
    rf"{re.escape(MARKER_START)}[\s\S]*?{re.escape(MARKER_END)}",
    re.MULTILINE,
)
FEATURED_RE = re.compile(
    rf"{re.escape(FEATURED_MARKER_START)}[\s\S]*?{re.escape(FEATURED_MARKER_END)}",
    re.MULTILINE,
)
HERO_LEAD_RE = re.compile(
    rf"{re.escape(HERO_LEAD_MARKER_START)}[\s\S]*?{re.escape(HERO_LEAD_MARKER_END)}",
    re.MULTILINE,
)
KATELYN_RE = re.compile(
    rf"{re.escape(KATELYN_MARKER_START)}[\s\S]*?{re.escape(KATELYN_MARKER_END)}",
    re.MULTILINE,
)
KATELYN_MINORS_RE = re.compile(
    rf"{re.escape(KATELYN_MINORS_MARKER_START)}[\s\S]*?{re.escape(KATELYN_MINORS_MARKER_END)}",
    re.MULTILINE,
)
JOSHUA_EDUCATION_RE = re.compile(
    rf"{re.escape(JOSHUA_EDUCATION_MARKER_START)}[\s\S]*?{re.escape(JOSHUA_EDUCATION_MARKER_END)}",
    re.MULTILINE,
)
HOME_VIDEO_GRID_RE = re.compile(
    rf"{re.escape(HOME_VIDEO_GRID_MARKER_START)}[\s\S]*?{re.escape(HOME_VIDEO_GRID_MARKER_END)}",
    re.MULTILINE,
)
PIERCING_VIDEO_RE = re.compile(
    rf"{re.escape(PIERCING_VIDEO_MARKER_START)}[\s\S]*?{re.escape(PIERCING_VIDEO_MARKER_END)}",
    re.MULTILINE,
)
VIDEO_REPO_RE = re.compile(
    rf"{re.escape(VIDEO_REPO_MARKER_START)}[\s\S]*?{re.escape(VIDEO_REPO_MARKER_END)}",
    re.MULTILINE,
)

VIDEO_REPO_PAGE = ROOT / "studio_videos" / "code.html"


def inject_grid(html: str, mode: str, compact: bool) -> tuple[str, bool]:
    exclude_featured = mode == "after_masonry"
    block = render_section(compact=compact, exclude_featured=exclude_featured)
    if not block.strip():
        return html, False

    if MARKER_START in html:
        new_html, n = MARKER_RE.subn(block, html, count=1)
        return new_html, n > 0

    if mode == "after_masonry":
        anchor = "<!-- WOA_HOME_MASONRY_END -->"
        if anchor not in html:
            return html, False
        return html.replace(anchor, anchor + "\n" + block, 1), True

    if mode == "before_portfolio":
        anchor = '<section class="py-section-gap" id="portfolio">'
        if anchor not in html:
            return html, False
        return html.replace(anchor, block + "\n" + anchor, 1), True

    if mode == "before_curated":
        anchor = "<!-- WOA_CURATED_PORTFOLIO_START -->"
        if anchor not in html:
            return html, False
        return html.replace(anchor, block + "\n" + anchor, 1), True

    return html, False


def inject_hero_lead(html: str) -> tuple[str, bool]:
    block = render_hero_lead_embed()
    if not block.strip():
        return html, False

    if HERO_LEAD_MARKER_START in html:
        new_html, n = HERO_LEAD_RE.subn(block, html, count=1)
        return new_html, n > 0

    anchor = '<div class="woa-hero-media-grid absolute inset-0 z-0">'
    if anchor not in html:
        return html, False
    return html.replace(
        anchor,
        anchor + '\n<div class="woa-hero-video-panel order-1 lg:order-2 relative z-[1]">'
        + block
        + "</div>",
        1,
    ), True


def inject_featured_home(html: str) -> tuple[str, bool]:
    block = render_featured_section()
    if FEATURED_MARKER_START in html:
        if not block.strip():
            new_html, n = FEATURED_RE.subn("", html, count=1)
            return new_html, n > 0
        new_html, n = FEATURED_RE.subn(block, html, count=1)
        return new_html, n > 0
    if not block.strip():
        return html, False

    anchor = "<!-- WOA_HOME_REVIEWS_START -->"
    if anchor not in html:
        return html, False
    return html.replace(anchor, block + "\n" + anchor, 1), True


def strip_homepage_video_blocks(html: str) -> tuple[str, bool]:
    """Remove extra video bands from the landing page; keep hero preview + #studio-interview."""
    changed = False
    for pattern in (HOME_VIDEO_GRID_RE, MARKER_RE, PIERCING_VIDEO_RE):
        html, n = pattern.subn("", html, count=1)
        if n:
            changed = True
    return html, changed


def inject_home_video_grid(html: str) -> tuple[str, bool]:
    block = render_home_video_grid()
    if HOME_VIDEO_GRID_MARKER_START in html:
        if not block.strip():
            new_html, n = HOME_VIDEO_GRID_RE.subn("", html, count=1)
            return new_html, n > 0
        new_html, n = HOME_VIDEO_GRID_RE.subn(block, html, count=1)
        return new_html, n > 0
    if not block.strip():
        return html, False

    anchor = "<!-- Featured Work Portfolio Carousel -->"
    if anchor not in html:
        return html, False
    return html.replace(anchor, anchor + "\n" + block, 1), True


def inject_piercing_video(html: str) -> tuple[str, bool]:
    from client_videos import PIERCING_SECTION_STATIC_IMAGE

    block = render_piercing_section_video()
    if PIERCING_VIDEO_MARKER_START in html:
        if not block.strip():
            new_html, n = PIERCING_VIDEO_RE.subn(PIERCING_SECTION_STATIC_IMAGE, html, count=1)
            return new_html, n > 0
        new_html, n = PIERCING_VIDEO_RE.subn(block, html, count=1)
        return new_html, n > 0
    if not block.strip():
        return html, False

    old = """<div class="relative group">
<picture><source srcset="/artists/katelyn-cole/katelyn-cole-professional-piercer-ear-curation-no-duplicates-las-vegas.webp" type="image/webp"/><img alt="Katelyn Cole professional piercer — curated ear piercing at Work of Art Tattoo Las Vegas" class="w-full aspect-[4/5] object-cover grayscale hover:grayscale-0 transition-all duration-1000" height="1600" loading="lazy" src="/artists/katelyn-cole/katelyn-cole-professional-piercer-ear-curation-no-duplicates-las-vegas.jpg" width="800"/></picture>
<div class="absolute -bottom-8 -right-8 w-48 h-48 bg-secondary flex items-center justify-center p-8 hidden md:flex">
<span class="font-headline-md text-headline-md text-on-secondary text-center leading-tight">Professional Piercing</span>
</div>
</div>"""
    if old in html:
        return html.replace(old, block, 1), True
    return html, False


def inject_video_repo_page(html: str) -> tuple[str, bool]:
    block = render_video_repo_page()
    if not block.strip():
        return html, False

    if VIDEO_REPO_MARKER_START in html:
        new_html, n = VIDEO_REPO_RE.subn(block, html, count=1)
        return new_html, n > 0

    anchor = '<main class="pt-20">'
    if anchor not in html:
        return html, False
    return html.replace(anchor, anchor + "\n" + block, 1), True


def mirror_path(rel: Path) -> Path | None:
    if not GITHUB.is_dir():
        return None
    candidate = GITHUB / rel
    return candidate if candidate.is_file() else None


def fix_studio_interview_anchor(html: str) -> tuple[str, bool]:
    """Point legacy #hero-interview jumps at the full interview section."""
    if "#hero-interview" not in html:
        return html, False
    return html.replace("#hero-interview", "#studio-interview"), True


def process_file(path: Path, mode: str, compact: bool) -> None:
    if not path.is_file():
        print(f"skip missing {path}")
        return

    html = path.read_text(encoding="utf-8")
    changed = False

    if path == HOME:
        html, ok = inject_hero_lead(html)
        if ok:
            changed = True
            print(f"hero-lead {path}")
        html, ok = strip_homepage_video_blocks(html)
        if ok:
            changed = True
            print(f"strip-home-videos {path}")
        html, ok = inject_featured_home(html)
        if ok:
            changed = True
            print(f"featured {path}")
        html, ok = inject_home_video_grid(html)
        if ok:
            changed = True
            print(f"home-video-grid {path}")
        html, ok = inject_piercing_video(html)
        if ok:
            changed = True
            print(f"piercing-video {path}")
        html, ok = fix_studio_interview_anchor(html)
        if ok:
            changed = True
            print(f"interview-anchor {path}")
    else:
        html, ok = inject_grid(html, mode, compact)
        if ok:
            changed = True
            print(f"grid {path}")

    if changed:
        path.write_text(html, encoding="utf-8")
    else:
        print(f"unchanged {path}")

    rel = path.relative_to(ROOT)
    mirror = mirror_path(rel)
    if mirror and mirror != path:
        m_html = mirror.read_text(encoding="utf-8")
        m_changed = False
        if path == HOME:
            m_html, ok = inject_hero_lead(m_html)
            if ok:
                m_changed = True
            m_html, ok = strip_homepage_video_blocks(m_html)
            if ok:
                m_changed = True
            m_html, ok = inject_featured_home(m_html)
            if ok:
                m_changed = True
            m_html, ok = inject_home_video_grid(m_html)
            if ok:
                m_changed = True
            m_html, ok = inject_piercing_video(m_html)
            if ok:
                m_changed = True
            m_html, ok = fix_studio_interview_anchor(m_html)
            if ok:
                m_changed = True
        else:
            m_html, ok = inject_grid(m_html, mode, compact)
            if ok:
                m_changed = True
        if m_changed:
            mirror.write_text(m_html, encoding="utf-8")
            print(f"mirror {mirror}")


def inject_katelyn_page(html: str) -> tuple[str, bool]:
    block = render_katelyn_section()
    if not block.strip():
        return html, False

    if KATELYN_MARKER_START in html:
        new_html, n = KATELYN_RE.subn(block, html, count=1)
        return new_html, n > 0

    if KATELYN_ANCHOR not in html:
        return html, False
    return html.replace(KATELYN_ANCHOR, block + "\n" + KATELYN_ANCHOR, 1), True


def inject_katelyn_minors(html: str) -> tuple[str, bool]:
    block = render_katelyn_minors_section()
    if not block.strip():
        return html, False

    if KATELYN_MINORS_MARKER_START in html:
        new_html, n = KATELYN_MINORS_RE.subn(block, html, count=1)
        return new_html, n > 0

    if KATELYN_MINORS_ANCHOR not in html:
        return html, False
    return html.replace(KATELYN_MINORS_ANCHOR, block + "\n" + KATELYN_MINORS_ANCHOR, 1), True


def _apply_katelyn(html: str) -> tuple[str, bool]:
    changed = False
    html, ok = inject_katelyn_page(html)
    if ok:
        changed = True
    html, ok = inject_katelyn_minors(html)
    if ok:
        changed = True
    return html, changed


def process_katelyn() -> None:
    if not KATELYN_PAGE.is_file():
        print(f"skip missing {KATELYN_PAGE}")
        return
    html = KATELYN_PAGE.read_text(encoding="utf-8")
    new_html, ok = _apply_katelyn(html)
    if ok:
        KATELYN_PAGE.write_text(new_html, encoding="utf-8")
        print(f"katelyn {KATELYN_PAGE}")
    else:
        print(f"unchanged {KATELYN_PAGE}")

    mirror = GITHUB / "artists_build" / "katelyn-cole.html"
    if GITHUB.is_dir() and mirror.is_file():
        m_html = mirror.read_text(encoding="utf-8")
        m_new, m_ok = _apply_katelyn(m_html)
        if m_ok:
            mirror.write_text(m_new, encoding="utf-8")
            print(f"mirror {mirror}")


def inject_joshua_education(html: str) -> tuple[str, bool]:
    block = render_joshua_education_section()
    if not block.strip():
        return html, False

    if JOSHUA_EDUCATION_MARKER_START in html:
        new_html, n = JOSHUA_EDUCATION_RE.subn(block, html, count=1)
        return new_html, n > 0

    if JOSHUA_EDUCATION_ANCHOR not in html:
        return html, False
    return html.replace(JOSHUA_EDUCATION_ANCHOR, block + "\n" + JOSHUA_EDUCATION_ANCHOR, 1), True


def process_joshua() -> None:
    if not JOSHUA_PAGE.is_file():
        print(f"skip missing {JOSHUA_PAGE}")
        return
    html = JOSHUA_PAGE.read_text(encoding="utf-8")
    new_html, ok = inject_joshua_education(html)
    if ok:
        JOSHUA_PAGE.write_text(new_html, encoding="utf-8")
        print(f"joshua {JOSHUA_PAGE}")
    else:
        print(f"unchanged {JOSHUA_PAGE}")

    mirror = GITHUB / "artists_build" / "joshua-cole.html"
    if GITHUB.is_dir() and mirror.is_file():
        m_html = mirror.read_text(encoding="utf-8")
        m_new, m_ok = inject_joshua_education(m_html)
        if m_ok:
            mirror.write_text(m_new, encoding="utf-8")
            print(f"mirror {mirror}")


def process_video_repo() -> None:
    if not VIDEO_REPO_PAGE.is_file():
        print(f"skip missing {VIDEO_REPO_PAGE} — run build_studio_videos_page.py first")
        return
    html = VIDEO_REPO_PAGE.read_text(encoding="utf-8")
    export_videos_catalog(VIDEO_REPO_PAGE.parent / "videos.json")
    new_html, ok = inject_video_repo_page(html)
    if ok:
        VIDEO_REPO_PAGE.write_text(new_html, encoding="utf-8")
        print(f"video-repo {VIDEO_REPO_PAGE}")
    else:
        print(f"unchanged {VIDEO_REPO_PAGE}")

    mirror = GITHUB / "studio_videos" / "code.html"
    if GITHUB.is_dir() and mirror.is_file():
        m_html = mirror.read_text(encoding="utf-8")
        export_videos_catalog(mirror.parent / "videos.json")
        m_new, m_ok = inject_video_repo_page(m_html)
        if m_ok:
            mirror.write_text(m_new, encoding="utf-8")
            print(f"mirror {mirror}")


def main() -> None:
    for path, mode, compact in TARGETS:
        process_file(path, mode, compact)
    process_katelyn()
    process_joshua()
    process_video_repo()


if __name__ == "__main__":
    main()
