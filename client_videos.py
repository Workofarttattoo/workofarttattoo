#!/usr/bin/env python3
"""Client interview / Instagram reel embeds for portfolio and homepage."""

from __future__ import annotations

import json
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Union

REPO_ROOT = Path(__file__).resolve().parent
MERGED_CATALOG_JSON = REPO_ROOT / "videos_catalog_merged.json"

STUDIO_LOGO_PNG = "/home_work_of_art_tattoo_piercing/work-of-art-logo.png"
STUDIO_LOGO_WEBP = "/home_work_of_art_tattoo_piercing/work-of-art-logo.webp"
CLIENT_INTERVIEW_PERMALINK = "https://www.instagram.com/p/DTZRprYgQ3G/"
HERO_INTERVIEW_STILL_PNG = (
    "/home_work_of_art_tattoo_piercing/joshua-cole-studio-interview-las-vegas.png"
)
HERO_INTERVIEW_STILL_WEBP = (
    "/home_work_of_art_tattoo_piercing/joshua-cole-studio-interview-las-vegas.webp"
)
KATELYN_STILL_JPG = (
    "/artists/katelyn-cole/"
    "katelyn-cole-professional-piercer-ear-curation-no-duplicates-las-vegas.jpg"
)

# Instagram /embed iframes render blank on static hosting — use poster + permalink cards.
VIDEO_CARD_POSTERS: dict[str, tuple[str, str]] = {
    "DDiX988y0tR": (HERO_INTERVIEW_STILL_PNG, "cover"),
    "DTZRprYgQ3G": (STUDIO_LOGO_PNG, "contain"),
    "C8vPwacP1du": (STUDIO_LOGO_PNG, "contain"),
    "Cpp18lXgU3P": (HERO_INTERVIEW_STILL_PNG, "cover"),
    "Cs1_Oc4gEx1": (KATELYN_STILL_JPG, "cover"),
    "C78fY1quCVF": (KATELYN_STILL_JPG, "cover"),
    "C0nNwUkRHz6": (KATELYN_STILL_JPG, "cover"),
    "C4fOsY7OSTq": (KATELYN_STILL_JPG, "cover"),
    "C3GjVCdLUQ9": (KATELYN_STILL_JPG, "cover"),
}

# Only allowlisted clips appear in embeds, /studio_videos/, and guide spotlights.
# Re-run refresh_videos_catalog.py after edits. See VIDEOS_CURATED.md for rationale.
SITE_VIDEO_ALLOWLIST: frozenset[str] = frozenset(
    {
        "DDiX988y0tR",  # Joshua — professional studio interview (hero)
        "DTZRprYgQ3G",  # Client interview
        "C8vPwacP1du",  # Joshua painting in studio
        "Cpp18lXgU3P",  # Joshua — seminars / advanced training
        "C78fY1quCVF",  # Katelyn — piercing in studio
        "C0nNwUkRHz6",  # Jewelry & anatomical placement
        "C4fOsY7OSTq",  # Ear curation
        "C3GjVCdLUQ9",  # Piercing session
        "Cs1_Oc4gEx1",  # Minor ear piercing (dedicated minors block)
    }
)

# Guide-page spotlights rotate within this subset (polished only).
SPOTLIGHT_VIDEO_IDS: tuple[str, ...] = (
    "C8vPwacP1du",
    "Cpp18lXgU3P",
    "C78fY1quCVF",
    "C0nNwUkRHz6",
    "C4fOsY7OSTq",
    "C3GjVCdLUQ9",
)


def is_site_video_allowed(media_id: str) -> bool:
    return bool(media_id) and media_id in SITE_VIDEO_ALLOWLIST


def filter_allowed_dicts(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [r for r in rows if is_site_video_allowed(r.get("media_id", ""))]

MARKER_START = "<!-- WOA_CLIENT_VIDEOS_START -->"
MARKER_END = "<!-- WOA_CLIENT_VIDEOS_END -->"
FEATURED_MARKER_START = "<!-- WOA_FEATURED_VIDEO_START -->"
FEATURED_MARKER_END = "<!-- WOA_FEATURED_VIDEO_END -->"
HERO_LEAD_MARKER_START = "<!-- WOA_HERO_LEAD_START -->"
HERO_LEAD_MARKER_END = "<!-- WOA_HERO_LEAD_END -->"
KATELYN_MARKER_START = "<!-- WOA_KATELYN_VIDEOS_START -->"
KATELYN_MARKER_END = "<!-- WOA_KATELYN_VIDEOS_END -->"
KATELYN_MINORS_MARKER_START = "<!-- WOA_KATELYN_MINORS_START -->"
KATELYN_MINORS_MARKER_END = "<!-- WOA_KATELYN_MINORS_END -->"
HOME_VIDEO_GRID_MARKER_START = "<!-- WOA_HOME_VIDEO_GRID_START -->"
HOME_VIDEO_GRID_MARKER_END = "<!-- WOA_HOME_VIDEO_GRID_END -->"
PIERCING_VIDEO_MARKER_START = "<!-- WOA_PIERCING_VIDEO_START -->"
PIERCING_VIDEO_MARKER_END = "<!-- WOA_PIERCING_VIDEO_END -->"
VIDEO_REPO_MARKER_START = "<!-- WOA_VIDEO_REPO_START -->"
VIDEO_REPO_MARKER_END = "<!-- WOA_VIDEO_REPO_END -->"
PAGE_SPOTLIGHT_MARKER_START = "<!-- WOA_PAGE_SPOTLIGHT_VIDEO_START -->"
PAGE_SPOTLIGHT_MARKER_END = "<!-- WOA_PAGE_SPOTLIGHT_VIDEO_END -->"

# Featured on Piercing Minors section (not duplicated in the reel grid)
KATELYN_MINORS_REEL_ID = "Cs1_Oc4gEx1"

# Joshua Cole artist page — continuing education (/artists/joshua-cole/)
JOSHUA_EDUCATION_MARKER_START = "<!-- WOA_JOSHUA_EDUCATION_START -->"
JOSHUA_EDUCATION_MARKER_END = "<!-- WOA_JOSHUA_EDUCATION_END -->"
JOSHUA_EDUCATION_REEL_ID = "Cpp18lXgU3P"

# Katelyn Cole artist page only (/artists/katelyn-cole/) — curated best four.
KATELYN_VIDEOS: list[dict[str, str]] = [
    {
        "kind": "reel",
        "media_id": "C78fY1quCVF",
        "title": "Katelyn Cole — piercing in the studio",
        "blurb": "Watch Katelyn at Work of Art — calm ear curation and piercing placement in Las Vegas.",
    },
    {
        "kind": "reel",
        "media_id": "C0nNwUkRHz6",
        "title": "Jewelry & placement — studio reel",
        "blurb": "Jewelry fit and anatomical placement.",
    },
    {
        "kind": "reel",
        "media_id": "C4fOsY7OSTq",
        "title": "Ear curation — studio reel",
        "blurb": "Katelyn Cole at Work of Art — Las Vegas piercing.",
    },
    {
        "kind": "reel",
        "media_id": "C3GjVCdLUQ9",
        "title": "Piercing session — studio reel",
        "blurb": "In-studio with professional piercer Katelyn Cole.",
    },
]

# Homepage hero — Joshua professional studio interview (Instagram reel)
FEATURED_HOME: dict[str, str] = {
    "kind": "reel",
    "media_id": "DDiX988y0tR",
    "title": "Joshua Cole — professional studio interview",
    "blurb": "The full Work of Art story — consult-first custom tattoos and piercings in Las Vegas, told straight from the studio chair.",
    "poster_png": HERO_INTERVIEW_STILL_PNG,
    "poster_webp": HERO_INTERVIEW_STILL_WEBP,
    "poster_fit": "cover",
}

# Homepage: hero preview + full interview section at #studio-interview.
HOME_VIDEO_GRID: list[dict[str, str]] = []

# Homepage piercing block: static image only (no Instagram embed on landing).
PIERCING_SECTION_VIDEO: dict[str, str] = {}

# Grid videos — curated tattoo clips (portfolio / client-stories sections).
CLIENT_VIDEOS: list[dict[str, str]] = [
    {
        "kind": "reel",
        "media_id": "DDiX988y0tR",
        "title": "Joshua Cole — professional studio interview",
        "blurb": "The full Work of Art story — consult-first studio in Las Vegas.",
    },
    {
        "kind": "post",
        "media_id": "DTZRprYgQ3G",
        "title": "Client interview — Las Vegas studio",
        "blurb": "Real collectors, unfiltered — filmed in-studio at Work of Art.",
        "poster_png": STUDIO_LOGO_PNG,
        "poster_webp": STUDIO_LOGO_WEBP,
        "poster_fit": "contain",
    },
    {
        "kind": "reel",
        "media_id": "C8vPwacP1du",
        "title": "Joshua Cole — painting in the studio",
        "blurb": "Joshua at the easel — fine art and tattoo craft under one roof at Work of Art Las Vegas.",
    },
    {
        "kind": "reel",
        "media_id": "Cpp18lXgU3P",
        "title": "Joshua Cole — seminars & advanced training",
        "blurb": "Continuing education and advanced training from Joshua Cole.",
    },
]


@dataclass(frozen=True)
class ClientVideo:
    kind: str  # "post" | "reel"
    media_id: str
    title: str
    blurb: str
    poster_png: str = ""
    poster_webp: str = ""
    poster_fit: str = "cover"  # "contain" for logo placeholder tiles

    @property
    def permalink(self) -> str:
        if self.kind == "reel":
            return f"https://www.instagram.com/reel/{self.media_id}/"
        return f"https://www.instagram.com/p/{self.media_id}/"

    @property
    def embed_url(self) -> str:
        if self.kind == "reel":
            return f"https://www.instagram.com/reel/{self.media_id}/embed"
        return f"https://www.instagram.com/p/{self.media_id}/embed"


@dataclass(frozen=True)
class PortfolioShowcase:
    """Static portfolio tile in the homepage studio band (replaces weak reel embeds)."""

    title: str
    blurb: str
    poster_png: str
    poster_webp: str
    href: str = "/#gallery-expanded"
    poster_fit: str = "cover"
    link_label: str = "View portfolio"


HomeGridItem = Union[ClientVideo, PortfolioShowcase]


def _parse_entry(raw: dict[str, str]) -> ClientVideo:
    png = raw.get("poster_png", "")
    webp = raw.get("poster_webp", png.replace(".png", ".webp") if png else "")
    return ClientVideo(
        kind=raw.get("kind", "post"),
        media_id=raw["media_id"] if "media_id" in raw else raw.get("post_id", ""),
        title=raw.get("title", "Client story"),
        blurb=raw.get("blurb", ""),
        poster_png=png,
        poster_webp=webp,
        poster_fit=raw.get("poster_fit", "cover"),
    )


def load_featured() -> ClientVideo | None:
    if not FEATURED_HOME.get("media_id"):
        return None
    return _parse_entry(FEATURED_HOME)


def load_katelyn_videos() -> list[ClientVideo]:
    return [
        _parse_entry(raw)
        for raw in KATELYN_VIDEOS
        if is_site_video_allowed(raw.get("media_id", ""))
    ]


def load_videos(*, exclude_featured: bool = False) -> list[ClientVideo]:
    featured_id = FEATURED_HOME.get("media_id") if exclude_featured else None
    out: list[ClientVideo] = []
    for raw in CLIENT_VIDEOS:
        v = _parse_entry(raw)
        if not is_site_video_allowed(v.media_id):
            continue
        if featured_id and v.media_id == featured_id:
            continue
        out.append(v)
    return out


def _parse_home_grid_entry(raw: dict[str, str]) -> HomeGridItem:
    if raw.get("kind") == "showcase":
        png = raw["poster_png"]
        webp = raw.get("poster_webp", png.replace(".png", ".webp"))
        return PortfolioShowcase(
            title=raw.get("title", "Portfolio highlight"),
            blurb=raw.get("blurb", ""),
            poster_png=png,
            poster_webp=webp,
            href=raw.get("href", "/#gallery-expanded"),
            poster_fit=raw.get("poster_fit", "cover"),
            link_label=raw.get("link_label", "View portfolio"),
        )
    return _parse_entry(raw)


def load_home_video_grid() -> list[HomeGridItem]:
    return [_parse_home_grid_entry(raw) for raw in HOME_VIDEO_GRID]


def load_piercing_section_video() -> ClientVideo:
    return _parse_entry(PIERCING_SECTION_VIDEO)


def _fallback_catalog_entries() -> list[dict[str, str]]:
    """Used when videos_catalog_merged.json is missing."""
    import re

    seen: set[str] = set()
    rows: list[dict[str, str]] = []

    def append(raw: dict[str, str]) -> None:
        v = _parse_entry(raw)
        if v.media_id in seen:
            return
        seen.add(v.media_id)
        rows.append(
            {
                "kind": v.kind,
                "media_id": v.media_id,
                "title": raw.get("title", v.title),
                "blurb": raw.get("blurb", ""),
            }
        )

    append(FEATURED_HOME)
    for raw in CLIENT_VIDEOS:
        append(raw)
    append(
        {
            "kind": "reel",
            "media_id": JOSHUA_EDUCATION_REEL_ID,
            "title": "Joshua Cole — seminars & advanced training",
            "blurb": "",
        }
    )
    append(
        {
            "kind": "reel",
            "media_id": KATELYN_MINORS_REEL_ID,
            "title": "Minor ear piercing — how Katelyn does it",
            "blurb": "",
        }
    )
    for raw in KATELYN_VIDEOS:
        append(raw)

    IG_RE = re.compile(
        r"https://www\.instagram\.com/(?:reel|p|tv)/([A-Za-z0-9_-]+)/?",
        re.IGNORECASE,
    )

    def kind_from_url(url: str) -> str:
        return "post" if "/p/" in url.lower() else "reel"

    for path in sorted(REPO_ROOT.rglob("*.html")):
        if any(x in path.parts for x in (".git", "skipped_upload_build", "node_modules")):
            continue
        try:
            blob = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in IG_RE.finditer(blob):
            mid = m.group(1)
            if mid in seen:
                continue
            seen.add(mid)
            rows.append(
                {
                    "kind": kind_from_url(m.group(0)),
                    "media_id": mid,
                    "title": "Work of Art — Instagram clip",
                    "blurb": "",
                }
            )

    return filter_allowed_dicts(rows)


def load_merged_catalog_dicts() -> list[dict[str, str]]:
    if not MERGED_CATALOG_JSON.is_file():
        return _fallback_catalog_entries()
    try:
        data = json.loads(MERGED_CATALOG_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _fallback_catalog_entries()
    if not isinstance(data, list):
        return _fallback_catalog_entries()
    out: list[dict[str, str]] = []
    for row in data:
        if isinstance(row, dict) and row.get("media_id"):
            out.append(
                {
                    "kind": str(row.get("kind", "reel")),
                    "media_id": str(row["media_id"]),
                    "title": str(row.get("title", "Instagram clip")),
                    "blurb": str(row.get("blurb", "")),
                }
            )
    return filter_allowed_dicts(out if out else _fallback_catalog_entries())


def load_all_catalog_videos() -> list[ClientVideo]:
    """Full catalog for /studio_videos/ — curated allowlist only."""
    return [
        _parse_entry(raw)
        for raw in load_merged_catalog_dicts()
        if is_site_video_allowed(raw.get("media_id", ""))
    ]


def load_spotlight_pool() -> list[ClientVideo]:
    """One embed per secondary page — polished clips only."""
    by_id = {v.media_id: v for v in load_all_catalog_videos()}
    pool = [by_id[mid] for mid in SPOTLIGHT_VIDEO_IDS if mid in by_id]
    return pool if pool else load_all_catalog_videos()


def export_videos_catalog(path: Path) -> None:
    import json

    rows = []
    for v in load_all_catalog_videos():
        rows.append(
            {
                "kind": v.kind,
                "media_id": v.media_id,
                "title": v.title,
                "blurb": v.blurb,
                "permalink": v.permalink,
                "embed_url": v.embed_url,
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def _css_block() -> str:
    return """<style data-woa-client-videos-css="1">
[data-woa-client-videos] .woa-ig-grid,
[data-woa-joshua-education] .woa-featured-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  align-items: center;
}
@media (min-width: 1024px) {
  [data-woa-joshua-education] .woa-featured-layout {
    grid-template-columns: 1fr minmax(320px, 420px);
    gap: 3rem;
  }
}
[data-woa-katelyn-videos] .woa-ig-grid { display: grid; grid-template-columns: 1fr; gap: 1.25rem; max-width: 420px; margin: 0 auto; }
[data-woa-client-videos].woa-client-videos--multi .woa-ig-grid,
[data-woa-katelyn-videos].woa-client-videos--multi .woa-ig-grid,
[data-woa-video-repo] .woa-video-grid {
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  max-width: 1200px;
  margin: 0 auto;
}
[data-woa-client-videos] .woa-video-card,
[data-woa-katelyn-videos] .woa-video-card {
  max-width: 420px;
  margin-left: auto;
  margin-right: auto;
}
[data-woa-client-videos] .woa-ig-cell,
[data-woa-featured-video] .woa-ig-cell,
[data-woa-joshua-education] .woa-ig-cell,
[data-woa-katelyn-videos] .woa-ig-cell,
[data-woa-home-video-grid] .woa-ig-cell,
[data-woa-video-repo] .woa-ig-cell {
  border: 1px solid rgba(68, 71, 72, 0.5);
  background: #131313;
  overflow: hidden;
  border-radius: 2px;
}
[data-woa-client-videos] .woa-ig-cell iframe,
[data-woa-featured-video] .woa-ig-cell iframe,
[data-woa-joshua-education] .woa-ig-cell iframe,
[data-woa-katelyn-videos] .woa-ig-cell iframe,
[data-woa-home-video-grid] .woa-ig-cell iframe,
[data-woa-video-repo] .woa-ig-cell iframe {
  width: 100%;
  aspect-ratio: 9 / 16;
  min-height: 320px;
  max-height: min(85vh, 680px);
  height: auto;
  border: 0;
  display: block;
  background: #0d0d0d;
}
[data-woa-featured-video] .woa-ig-cell iframe { min-height: 580px; }
[data-woa-client-videos] .woa-ig-caption,
[data-woa-featured-video] .woa-ig-caption,
[data-woa-joshua-education] .woa-ig-caption,
[data-woa-katelyn-videos] .woa-ig-caption {
  padding: 0.85rem 1rem 1rem;
  border-top: 1px solid rgba(68, 71, 72, 0.35);
}
[data-woa-client-videos] .woa-ig-caption h3,
[data-woa-featured-video] .woa-ig-caption h3,
[data-woa-joshua-education] .woa-ig-caption h3,
[data-woa-katelyn-videos] .woa-ig-caption h3 {
  margin: 0 0 0.35rem;
  font-size: 0.875rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #e9c349;
}
[data-woa-client-videos] .woa-ig-caption p,
[data-woa-featured-video] .woa-ig-caption p,
[data-woa-joshua-education] .woa-ig-caption p,
[data-woa-katelyn-videos] .woa-ig-caption p {
  margin: 0;
  font-size: 0.8125rem;
  color: #c4c7c7;
  line-height: 1.45;
}
[data-woa-client-videos] .woa-ig-caption a,
[data-woa-featured-video] .woa-ig-caption a,
[data-woa-joshua-education] .woa-ig-caption a,
[data-woa-katelyn-videos] .woa-ig-caption a {
  color: #e9c349;
  text-decoration: underline;
}
[data-woa-featured-video] .woa-featured-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  align-items: center;
}
@media (min-width: 1024px) {
  [data-woa-featured-video] .woa-featured-layout {
    grid-template-columns: 1fr minmax(320px, 420px);
    gap: 3rem;
  }
}
[data-woa-hero-lead] .woa-hero-lead-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  align-items: center;
  max-width: 1440px;
  margin: 0 auto;
}
@media (min-width: 1024px) {
  [data-woa-hero-lead] .woa-hero-lead-layout {
    grid-template-columns: minmax(340px, 1.15fr) 1fr;
    gap: 2.5rem;
  }
}
[data-woa-hero-lead] .woa-hero-lead-video {
  border: 2px solid rgba(233, 195, 73, 0.4);
  background: #0d0d0d;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.45);
}
[data-woa-hero-lead] .woa-hero-lead-video iframe {
  width: 100%;
  min-height: clamp(340px, 68vh, 820px);
  border: 0;
  display: block;
}
[data-woa-hero-lead] .woa-hero-lead-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem;
  border: 1px solid rgba(233, 195, 73, 0.5);
  color: #e9c349;
  font-size: 0.6875rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}
[data-woa-home-video-grid] .woa-ig-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
  max-width: 1200px;
  margin: 0 auto;
}
[data-woa-home-video-grid] .woa-ig-cell {
  max-width: 420px;
  margin-left: auto;
  margin-right: auto;
}
[data-woa-home-video-grid] .woa-ig-cell--showcase .woa-ig-showcase-link {
  display: block;
  background: #0d0d0d;
}
[data-woa-home-video-grid] .woa-ig-cell--showcase img {
  width: 100%;
  aspect-ratio: 3 / 4;
  min-height: 320px;
  max-height: min(85vh, 680px);
  object-fit: cover;
  object-position: center;
  display: block;
}
[data-woa-home-video-grid] .woa-ig-showcase-link--logo {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 3 / 4;
  min-height: 320px;
  max-height: min(85vh, 680px);
  padding: 2rem;
  background: #0d0d0d;
}
[data-woa-home-video-grid] .woa-ig-showcase-link--logo img {
  width: auto;
  max-width: 88%;
  max-height: 52%;
  min-height: 0;
  aspect-ratio: auto;
  object-fit: contain;
}
[data-woa-home-video-grid] .woa-ig-play-badge {
  position: absolute;
  bottom: 1.25rem;
  left: 50%;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 0.85rem;
  background: rgba(233, 195, 73, 0.92);
  color: #1c1b1b;
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  border-radius: 2px;
  pointer-events: none;
}
[data-woa-client-videos] .woa-ig-showcase-link--logo,
[data-woa-home-video-grid] .woa-ig-showcase-link--logo {
  position: relative;
}
[data-woa-client-videos] .woa-ig-showcase-link--logo img,
[data-woa-client-videos] .woa-ig-cell--showcase:not(.woa-ig-showcase-link--logo) img {
  width: 100%;
  aspect-ratio: 9 / 16;
  min-height: 320px;
  max-height: min(85vh, 680px);
  object-fit: cover;
  display: block;
}
[data-woa-client-videos] .woa-ig-showcase-link--logo {
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 9 / 16;
  min-height: 320px;
  padding: 2rem;
  background: #0d0d0d;
}
[data-woa-client-videos] .woa-ig-showcase-link--logo img {
  width: auto;
  max-width: 88%;
  max-height: 52%;
  aspect-ratio: auto;
  object-fit: contain;
}
[data-woa-home-video-grid] .woa-ig-caption {
  padding: 0.85rem 1rem 1rem;
  border-top: 1px solid rgba(68, 71, 72, 0.35);
}
[data-woa-home-video-grid] .woa-ig-caption h3 {
  margin: 0 0 0.35rem;
  font-size: 0.875rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #e9c349;
}
[data-woa-home-video-grid] .woa-ig-caption p {
  margin: 0;
  font-size: 0.8125rem;
  color: #c4c7c7;
  line-height: 1.45;
}
[data-woa-home-video-grid] .woa-ig-caption a { color: #e9c349; }
[data-woa-piercing-video] .woa-ig-cell iframe {
  width: 100%;
  min-height: clamp(360px, 52vh, 640px);
  border: 0;
  display: block;
  background: #0d0d0d;
}
[data-woa-video-repo] .woa-video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}
[data-woa-video-repo] .video-card,
[data-woa-client-videos] .video-card,
[data-woa-katelyn-videos] .video-card,
[data-woa-joshua-education] .video-card,
[data-woa-page-spotlight] .video-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid rgba(68, 71, 72, 0.5);
  background: #131313;
  border-radius: 2px;
  overflow: hidden;
  color: inherit;
  text-decoration: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
[data-woa-video-repo] .video-card:hover,
[data-woa-client-videos] .video-card:hover,
[data-woa-katelyn-videos] .video-card:hover,
[data-woa-joshua-education] .video-card:hover,
[data-woa-page-spotlight] .video-card:hover {
  border-color: rgba(233, 195, 73, 0.55);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
}
.video-thumb {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 9 / 16;
  min-height: clamp(280px, 50vw, 460px);
  max-height: min(72vh, 540px);
  background: #050505;
  background-size: cover;
  background-position: center 20%;
  overflow: hidden;
}
.video-thumb--brand {
  background: radial-gradient(circle at 50% 42%, rgba(233, 195, 73, 0.12) 0%, transparent 55%),
    linear-gradient(160deg, #141414 0%, #0d0d0d 100%);
}
.video-thumb-play {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 3.25rem;
  height: 3.25rem;
  border-radius: 999px;
  background: rgba(233, 195, 73, 0.94);
  color: #1c1b1b;
  font-size: 1.15rem;
  line-height: 1;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
}
.video-card h3 {
  margin: 0;
  padding: 0.85rem 1rem 0.35rem;
  font-size: 0.875rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #e9c349;
}
.video-card p {
  margin: 0;
  padding: 0 1rem;
  flex: 1;
  font-size: 0.8125rem;
  color: #c4c7c7;
  line-height: 1.45;
}
.video-card-cta {
  display: block;
  padding: 0.85rem 1rem 1rem;
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #e9c349;
}
/* Stylized double-exposure interview poster (#studio-interview) */
.woa-interview-thumb-art {
  position: relative;
  overflow: hidden;
  background: #050505;
  isolation: isolate;
}
.woa-interview-thumb-art .woa-interview-layer {
  position: absolute;
  inset: -10%;
  background-size: cover;
  background-position: center 24%;
  background-repeat: no-repeat;
  pointer-events: none;
}
.woa-interview-thumb-art .woa-interview-layer--base {
  filter: contrast(1.15) saturate(0.78) grayscale(0.15);
  opacity: 0.94;
  z-index: 1;
}
.woa-interview-thumb-art .woa-interview-layer--invert {
  filter: invert(1) hue-rotate(188deg) contrast(1.25) brightness(1.05);
  opacity: 0.42;
  transform: translateX(7%) scale(1.05);
  mix-blend-mode: difference;
  z-index: 2;
  animation: woa-interview-ghost-drift 9s ease-in-out infinite alternate;
}
.woa-interview-thumb-art .woa-interview-layer--flare {
  inset: 0;
  background:
    radial-gradient(ellipse at 28% 78%, rgba(233, 195, 73, 0.22), transparent 48%),
    radial-gradient(ellipse at 72% 22%, rgba(255, 90, 20, 0.12), transparent 42%),
    linear-gradient(165deg, transparent 35%, rgba(0, 0, 0, 0.55) 100%);
  mix-blend-mode: soft-light;
  z-index: 3;
  animation: woa-interview-fire-crawl 5.5s linear infinite;
}
.woa-interview-thumb-art .woa-interview-scanline {
  inset: 0;
  background: repeating-linear-gradient(
    180deg,
    transparent 0,
    transparent 3px,
    rgba(233, 195, 73, 0.04) 3px,
    rgba(233, 195, 73, 0.04) 4px
  );
  z-index: 4;
  opacity: 0.65;
  mix-blend-mode: overlay;
}
.woa-interview-thumb-art .video-thumb-play {
  z-index: 6;
  position: relative;
}
@keyframes woa-interview-ghost-drift {
  0% {
    transform: translateX(8%) translateY(1%) scale(1.04) rotate(0.6deg);
  }
  100% {
    transform: translateX(-6%) translateY(-2%) scale(1.07) rotate(-0.8deg);
  }
}
@keyframes woa-interview-fire-crawl {
  0% {
    filter: hue-rotate(0deg);
    opacity: 0.85;
  }
  50% {
    filter: hue-rotate(18deg);
    opacity: 1;
  }
  100% {
    filter: hue-rotate(-12deg);
    opacity: 0.88;
  }
}
</style>"""


def _is_interview_poster(png: str) -> bool:
    return "joshua-cole-studio-interview" in png


def _interview_stylized_thumb(png: str) -> str:
    src = escape(png)
    return f"""<div class="video-thumb woa-interview-thumb-art" aria-hidden="true">
<div class="woa-interview-layer woa-interview-layer--base" style="background-image:url('{src}');"></div>
<div class="woa-interview-layer woa-interview-layer--invert" style="background-image:url('{src}');"></div>
<div class="woa-interview-layer woa-interview-layer--flare"></div>
<div class="woa-interview-layer woa-interview-scanline"></div>
<span class="video-thumb-play">▶</span>
</div>"""


def _hero_lead_media(video: ClientVideo) -> str:
    title = escape(video.title)
    poster_png = video.poster_png or HERO_INTERVIEW_STILL_PNG
    poster_webp = video.poster_webp or HERO_INTERVIEW_STILL_WEBP
    ig = escape(video.permalink)
    return f"""<a class="block group" href="{ig}" rel="noopener noreferrer" target="_blank" aria-label="Watch studio interview on Instagram">
<picture>
<source srcset="{escape(poster_webp)}" type="image/webp"/>
<img alt="{title} — studio interview preview — Work of Art Tattoo Las Vegas" class="w-full h-full object-cover object-center" decoding="async" fetchpriority="high" loading="eager" src="{escape(poster_png)}" width="518" height="696"/>
</picture>
<div class="absolute inset-0 bg-gradient-to-t from-black/65 via-transparent to-transparent pointer-events-none"></div>
<span class="absolute bottom-4 left-4 bg-secondary text-on-secondary px-3 py-1 text-[10px] uppercase tracking-[0.14em] font-semibold pointer-events-none">Watch on Instagram</span>
</a>"""


def render_hero_lead_embed() -> str:
    video = load_featured()
    if not video:
        return ""
    title = escape(video.title)
    link = escape(video.permalink)
    media = _hero_lead_media(video)
    return f"""{HERO_LEAD_MARKER_START}
<div class="woa-hero-lead-video h-full flex flex-col" data-woa-hero-lead="1" id="hero-interview-preview">
<span class="woa-hero-lead-badge mx-4 mt-3 shrink-0">Studio interview</span>
<article class="woa-ig-cell flex-1 border-0 rounded-none shadow-none mx-0 relative">
{media}
</article>
<p class="px-4 pb-3 text-[11px] text-on-surface-variant leading-snug shrink-0"><span class="text-secondary font-semibold uppercase tracking-wider">{title}</span> — <a class="text-secondary underline hover:no-underline" href="{link}" rel="noopener noreferrer" target="_blank">Open on Instagram</a></p>
</div>
{HERO_LEAD_MARKER_END}"""


def _poster_for_video(video: ClientVideo) -> tuple[str, str, str]:
    if video.poster_png:
        png = video.poster_png
        fit = video.poster_fit or "cover"
    elif video.media_id in VIDEO_CARD_POSTERS:
        png, fit = VIDEO_CARD_POSTERS[video.media_id]
    else:
        png, fit = STUDIO_LOGO_PNG, "contain"
    webp = video.poster_webp or png.replace(".png", ".webp")
    return png, webp, fit


def _video_card_cell(video: ClientVideo) -> str:
    title = escape(video.title)
    blurb = escape(video.blurb) if video.blurb else "Open on Instagram to watch."
    link = escape(video.permalink)
    png, _webp, fit = _poster_for_video(video)
    if _is_interview_poster(png):
        thumb_inner = _interview_stylized_thumb(png)
    else:
        thumb_classes = "video-thumb"
        thumb_style = ""
        if fit == "contain" or png == STUDIO_LOGO_PNG:
            thumb_classes += " video-thumb--brand"
        else:
            thumb_style = f' style="background-image:url(\'{escape(png)}\');"'
        thumb_inner = (
            f'<div class="{thumb_classes}"{thumb_style} aria-hidden="true">'
            f'<span class="video-thumb-play">▶</span></div>'
        )
    return f"""<article class="woa-video-card">
<a class="video-card" href="{link}" rel="noopener noreferrer" target="_blank">
{thumb_inner}
<h3>{title}</h3>
<p>{blurb}</p>
<span class="video-card-cta">Watch on Instagram</span>
</a>
</article>"""


def _video_cell(video: ClientVideo) -> str:
    return _video_card_cell(video)


def _showcase_cell(showcase: PortfolioShowcase) -> str:
    title = escape(showcase.title)
    blurb = escape(showcase.blurb) if showcase.blurb else ""
    href = escape(showcase.href)
    png = escape(showcase.poster_png)
    webp = escape(showcase.poster_webp)
    link_label = escape(showcase.link_label)
    is_external = href.startswith("http")
    link_attrs = ' rel="noopener noreferrer" target="_blank"' if is_external else ""
    logo_class = " woa-ig-showcase-link--logo" if showcase.poster_fit == "contain" else ""
    play_badge = (
        '<span class="woa-ig-play-badge" aria-hidden="true">▶ Watch</span>'
        if is_external and "instagram.com" in href
        else ""
    )
    blurb_html = (
        f'<p>{blurb} <a href="{href}"{link_attrs}>{link_label}</a></p>'
        if blurb
        else f'<p><a href="{href}"{link_attrs}>{link_label}</a></p>'
    )
    return f"""<article class="woa-ig-cell woa-ig-cell--showcase">
<a class="woa-ig-showcase-link{logo_class}" href="{href}"{link_attrs}>
<picture><source srcset="{webp}" type="image/webp"/><img alt="{title} — Work of Art Tattoo Las Vegas" decoding="async" height="1600" loading="lazy" src="{png}" width="1200"/></picture>
{play_badge}
</a>
<div class="woa-ig-caption">
<h3>{title}</h3>
{blurb_html}
</div>
</article>"""


def _home_grid_cell(item: HomeGridItem) -> str:
    if isinstance(item, PortfolioShowcase):
        return _showcase_cell(item)
    return _video_cell(item)


_SPOTLIGHT_CSS = """<style data-woa-page-spotlight-css="1">
[data-woa-page-spotlight] .woa-video-card {
  margin: 0 auto;
  max-width: 420px;
}
[data-woa-page-spotlight] .video-thumb {
  min-height: 360px;
}
</style>"""


def render_page_spotlight_strip(video: ClientVideo) -> str:
    cell = _video_cell(video)
    return f"""{PAGE_SPOTLIGHT_MARKER_START}
{_SPOTLIGHT_CSS}
<section class="py-10 px-margin-mobile md:px-margin-desktop border-t border-outline-variant/15 bg-surface-container/40" data-woa-page-spotlight="1">
<div class="max-w-xl mx-auto space-y-4 text-center">
<span class="font-label-caps text-[10px] text-secondary uppercase tracking-[0.22em]">Studio clip</span>
{cell}
<p class="font-body-md text-[13px] text-on-surface-variant">
<a class="text-secondary underline hover:no-underline" href="/studio_videos/">Video library</a>
 · 
<a class="text-secondary underline hover:no-underline" href="https://www.instagram.com/workofarttattoo/" rel="noopener noreferrer" target="_blank">Instagram</a>
</p>
</div>
</section>
{PAGE_SPOTLIGHT_MARKER_END}"""


def render_featured_section() -> str:
    """Homepage studio interview — poster card opens Instagram (embed.js fails on static host)."""
    video = load_featured()
    if not video:
        return ""

    title = escape(video.title)
    link = escape(video.permalink)
    blurb = escape(video.blurb) if video.blurb else ""
    card = _video_cell(video)

    return f"""{FEATURED_MARKER_START}
<section class="py-12 md:py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-high border-y border-outline-variant/10" data-woa-featured-video="1" id="studio-interview">
<div class="max-w-3xl mx-auto space-y-8">
<div class="text-center space-y-4 max-w-2xl mx-auto">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Featured interview</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">{title}</h2>
<p class="font-body-lg text-on-surface-variant leading-relaxed">{blurb} Tap the gold play button — the full interview opens on Instagram in a new tab.</p>
</div>
<div class="woa-interview-player max-w-[420px] mx-auto w-full">
{card}
</div>
<p class="text-center flex flex-wrap gap-3 justify-center pt-2">
<a class="inline-flex items-center justify-center gap-2 bg-secondary text-on-secondary px-8 py-4 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest border-2 border-secondary gold-glow" href="/appointments/">Book consultation</a>
<a class="inline-flex items-center justify-center gap-2 border border-outline-variant text-on-surface px-8 py-4 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary transition-colors" href="{link}" rel="noopener noreferrer" target="_blank">Watch on Instagram</a>
<a class="inline-flex items-center justify-center gap-2 border border-outline-variant text-on-surface px-8 py-4 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary transition-colors" href="/studio_videos/">More studio videos</a>
</p>
</div>
</section>
<script data-woa-studio-interview="1" type="text/javascript">
(function () {{
  "use strict";
  function highlightInterview() {{
    var el = document.getElementById("studio-interview");
    if (!el) return;
    el.classList.add("woa-interview-highlight");
    window.setTimeout(function () {{
      el.classList.remove("woa-interview-highlight");
    }}, 2400);
    el.scrollIntoView({{ behavior: "smooth", block: "start" }});
  }}
  if (window.location.hash === "#studio-interview") {{
    window.setTimeout(highlightInterview, 120);
  }}
  window.addEventListener("hashchange", function () {{
    if (window.location.hash === "#studio-interview") highlightInterview();
  }});
  document.querySelectorAll('a[href="#studio-interview"]').forEach(function (link) {{
    link.addEventListener("click", function () {{
      window.setTimeout(highlightInterview, 120);
    }});
  }});
}})();
</script>
{FEATURED_MARKER_END}"""


def render_section(*, compact: bool = False, exclude_featured: bool = False) -> str:
    videos = load_videos(exclude_featured=exclude_featured)
    if not videos:
        return ""

    multi = len(videos) > 1
    multi_cls = " woa-client-videos--multi" if multi else ""
    py = "py-12 md:py-16" if compact else "py-16 md:py-section-gap"
    cells = "\n".join(_video_cell(v) for v in videos)

    intro = (
        '<p class="font-body-md text-on-surface-variant max-w-2xl mx-auto text-center">Phone-filmed interviews and in-studio reels with real clients — hear what the experience is like before you book.</p>'
        if not compact
        else '<p class="font-body-md text-on-surface-variant max-w-xl mx-auto text-center text-sm">In-studio client stories from our Las Vegas portfolio.</p>'
    )

    cta = """<p class="text-center pt-8">
<a class="inline-flex items-center justify-center gap-2 border border-secondary text-secondary px-8 py-3 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest hover:bg-secondary/10 transition-colors" href="https://www.instagram.com/workofarttattoo/" rel="noopener noreferrer" target="_blank">More on @workofarttattoo</a>
</p>"""

    return f"""{MARKER_START}
{_css_block()}
<section class="{py} px-margin-mobile md:px-margin-desktop bg-surface-container border-y border-outline-variant/10{multi_cls}" data-woa-client-videos="1" id="client-stories">
<div class="max-w-6xl mx-auto space-y-8">
<div class="text-center space-y-3 max-w-3xl mx-auto">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Client stories</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Hear From Our Collectors</h2>
{intro}
</div>
<div class="woa-ig-grid">
{cells}
</div>
{cta}
</div>
</section>
{MARKER_END}"""


def render_home_video_grid() -> str:
    items = load_home_video_grid()
    if not items:
        return ""

    cells = "\n".join(_home_grid_cell(item) for item in items)
    return f"""{HOME_VIDEO_GRID_MARKER_START}
{_css_block()}
<section class="py-12 md:py-16 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/10 woa-client-videos--multi" data-woa-home-video-grid="1" id="studio-videos">
<div class="max-w-6xl mx-auto space-y-8">
<div class="text-center space-y-3 max-w-3xl mx-auto">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Studio reels</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Watch Tattoo Sessions &amp; Client Stories</h2>
<p class="font-body-md text-on-surface-variant">Client interviews, healed portfolio highlights, and in-studio footage from Work of Art Las Vegas — lion thigh realism, portrait work, macro eye detail, and Joshua Cole at the easel.</p>
</div>
<div class="woa-ig-grid">
{cells}
</div>
<p class="text-center pt-4 flex flex-wrap gap-3 justify-center">
<a class="inline-flex items-center justify-center gap-2 border border-secondary text-secondary px-8 py-3 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest hover:bg-secondary/10 transition-colors" href="/studio_videos/">Full video library</a>
<a class="inline-flex items-center justify-center gap-2 border border-outline-variant text-on-surface px-8 py-3 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary transition-colors" href="https://www.instagram.com/workofarttattoo/" rel="noopener noreferrer" target="_blank">More on Instagram</a>
</p>
</div>
</section>
{HOME_VIDEO_GRID_MARKER_END}"""


PIERCING_SECTION_STATIC_IMAGE = """<div class="relative group">
<picture><source srcset="/artists/katelyn-cole/katelyn-cole-professional-piercer-ear-curation-no-duplicates-las-vegas.webp" type="image/webp"/><img alt="Katelyn Cole professional piercer — curated ear piercing at Work of Art Tattoo Las Vegas" class="w-full aspect-[4/5] object-cover object-center grayscale hover:grayscale-0 transition-all duration-1000" height="1600" loading="lazy" src="/artists/katelyn-cole/katelyn-cole-professional-piercer-ear-curation-no-duplicates-las-vegas.jpg" width="800"/></picture>
<div class="absolute -bottom-8 -right-8 w-48 h-48 bg-secondary flex items-center justify-center p-8 hidden md:flex pointer-events-none">
<span class="font-headline-md text-headline-md text-on-secondary text-center leading-tight">Professional Piercing</span>
</div>
</div>"""


def render_piercing_section_video() -> str:
    if not PIERCING_SECTION_VIDEO.get("media_id"):
        return ""
    video = load_piercing_section_video()
    title = escape(video.title)
    blurb = escape(video.blurb)
    link = escape(video.permalink)
    return f"""{PIERCING_VIDEO_MARKER_START}
<div class="relative group" data-woa-piercing-video="1">
<article class="woa-ig-cell border border-outline-variant/30">
<iframe allowfullscreen="true" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{escape(video.embed_url)}" title="{title} — Work of Art Tattoo Las Vegas"></iframe>
<div class="woa-ig-caption">
<h3>{title}</h3>
<p>{blurb} <a href="{link}" rel="noopener noreferrer" target="_blank">Watch on Instagram</a></p>
</div>
</article>
<div class="absolute -bottom-8 -right-8 w-48 h-48 bg-secondary flex items-center justify-center p-8 hidden md:flex pointer-events-none">
<span class="font-headline-md text-headline-md text-on-secondary text-center leading-tight">Professional Piercing</span>
</div>
</div>
{PIERCING_VIDEO_MARKER_END}"""


def render_video_repo_page() -> str:
    videos = load_all_catalog_videos()
    if not videos:
        return ""

    cells = "\n".join(_video_cell(v) for v in videos)
    return f"""{VIDEO_REPO_MARKER_START}
{_css_block()}
<section class="py-16 md:py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container border-b border-outline-variant/10 woa-client-videos--multi" data-woa-video-repo="1" id="video-library">
<div class="max-w-6xl mx-auto space-y-10">
<div class="text-center space-y-4 max-w-3xl mx-auto">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Video library</span>
<h1 class="font-headline-lg text-headline-lg text-on-surface">Studio Videos — Tattoos &amp; Client Stories</h1>
<p class="font-body-lg text-on-surface-variant">Tap any card — gold play button opens the full reel or interview on Instagram. Nine curated clips only (no random archive reels).</p>
</div>
<div class="woa-video-grid">
{cells}
</div>
<p class="text-center pt-6 flex flex-wrap gap-3 justify-center">
<a class="inline-flex items-center justify-center gap-2 bg-secondary text-on-secondary px-8 py-4 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest border-2 border-secondary gold-glow" href="/appointments/">Book consultation</a>
<a class="inline-flex items-center justify-center gap-2 border border-secondary text-secondary px-8 py-4 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest hover:bg-secondary/10 transition-colors" href="https://www.instagram.com/workofarttattoo/" rel="noopener noreferrer" target="_blank">Follow @workofarttattoo</a>
<a class="inline-flex items-center justify-center gap-2 border border-outline-variant text-on-surface px-8 py-4 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary transition-colors" href="/">Back to homepage</a>
</p>
</div>
</section>
{VIDEO_REPO_MARKER_END}"""


def render_katelyn_section() -> str:
    videos = load_katelyn_videos()
    if not videos:
        return ""

    multi = len(videos) > 1
    multi_cls = " woa-client-videos--multi" if multi else ""
    cells = "\n".join(_video_cell(v) for v in videos)

    return f"""{KATELYN_MARKER_START}
{_css_block()}
<section class="py-12 md:py-16 px-margin-desktop bg-surface-container border-b border-outline-variant/10{multi_cls}" data-woa-katelyn-videos="1" id="katelyn-reels">
<div class="max-w-6xl mx-auto space-y-8">
<div class="text-center space-y-3 max-w-3xl mx-auto">
<span class="text-label-caps font-label-caps text-secondary uppercase tracking-[0.2em]">In the studio</span>
<h2 class="text-headline-lg font-headline-lg text-on-surface">Watch Katelyn Cole</h2>
<p class="text-body-lg font-body-lg text-on-surface-variant">Real piercing sessions and studio moments from our professional piercer — @stabislifee on Instagram.</p>
</div>
<div class="woa-ig-grid">
{cells}
</div>
<p class="text-center pt-6">
<a class="inline-flex items-center justify-center gap-2 border border-secondary text-secondary px-8 py-3 min-h-[48px] text-label-caps font-label-caps uppercase tracking-widest hover:bg-secondary/10 transition-colors" href="https://www.instagram.com/stabislifee/" rel="noopener noreferrer" target="_blank">Follow @stabislifee</a>
</p>
</div>
</section>
{KATELYN_MARKER_END}"""


def _video_cell_for_media_id(media_id: str) -> str:
    for video in load_all_catalog_videos():
        if video.media_id == media_id:
            return _video_cell(video)
    return ""


def render_katelyn_minors_section() -> str:
    reel_id = KATELYN_MINORS_REEL_ID
    minors_card = _video_cell_for_media_id(reel_id)

    return f"""{KATELYN_MINORS_MARKER_START}
<section class="py-section-gap px-margin-desktop bg-surface border-y border-outline-variant/10" id="piercing-minors">
<div class="max-w-6xl mx-auto space-y-10">
<div class="max-w-3xl mx-auto text-center space-y-4">
<span class="text-label-caps font-label-caps text-secondary uppercase tracking-[0.2em]">Families welcome</span>
<h2 class="text-headline-lg font-headline-lg text-on-surface">Piercing Minors — Rules &amp; What to Bring</h2>
<p class="text-body-lg font-body-lg text-on-surface-variant">Katelyn Cole specializes in calm ear piercing for younger clients. Sessions are unhurried, explained step-by-step, and designed so kids and guardians feel confident — most families tell us how smoothly everything goes.</p>
</div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">
<div class="space-y-8">
<div class="p-8 border border-outline-variant/20 bg-surface-container/40">
<h3 class="text-headline-md font-headline-md text-secondary mb-4 uppercase tracking-tight">Who we can pierce</h3>
<ul class="text-body-md font-body-md text-on-surface-variant space-y-3 list-disc pl-5">
<li><strong class="text-on-surface">Ages 14 and up</strong> for ear piercing with a parent or legal guardian present the entire appointment.</li>
<li>The accompanying adult must be the <strong class="text-on-surface">legal guardian</strong> — we work with you when you are the guardian on record, not only a family friend or relative unless they are the documented guardian.</li>
<li>Ear piercing focus for minors; other placements are evaluated case-by-case at consultation.</li>
</ul>
</div>
<div class="p-8 border border-secondary/30 bg-secondary/5">
<h3 class="text-headline-md font-headline-md text-on-surface mb-4">What to bring</h3>
<ul class="text-body-md font-body-md text-on-surface-variant space-y-3 list-disc pl-5">
<li><strong class="text-on-surface">Minor&apos;s government-issued ID</strong> (or school ID with photo where applicable).</li>
<li><strong class="text-on-surface">Guardian&apos;s government-issued photo ID</strong>.</li>
<li><strong class="text-on-surface">Minor&apos;s birth certificate</strong> linking the guardian to the client.</li>
<li>Both minor and guardian must be present for the full service — no drop-offs.</li>
</ul>
</div>
<div class="p-6 border border-outline-variant/20 bg-background/40">
<p class="text-body-md text-on-surface-variant"><strong class="text-on-surface">Questions before you drive over?</strong> Call ahead at <a class="text-secondary underline hover:no-underline" href="tel:+17252241240">(725) 224-1240</a> or <a class="text-secondary underline hover:no-underline" href="mailto:thewhiteknight702@gmail.com">Email us!</a> — we will clarify paperwork, placement, and jewelry so your appointment is seamless.</p>
</div>
<div class="flex flex-wrap gap-3">
<a class="bg-secondary text-on-secondary px-8 py-4 text-label-caps font-label-caps uppercase gold-glow inline-block min-h-[48px]" href="/appointments/">Book piercing appointment</a>
<a class="border border-outline-variant text-on-surface px-8 py-4 text-label-caps font-label-caps uppercase hover:border-secondary transition-colors inline-block min-h-[48px]" href="tel:+17252241240">Call to confirm paperwork</a>
</div>
</div>
<div class="max-w-[420px] w-full mx-auto lg:mx-0 lg:ml-auto">
{minors_card}
</div>
</div>
</div>
</section>
{KATELYN_MINORS_MARKER_END}"""


def render_joshua_education_section() -> str:
    reel_id = JOSHUA_EDUCATION_REEL_ID
    permalink = f"https://www.instagram.com/reel/{reel_id}/"
    seminar_card = _video_cell_for_media_id(reel_id)

    return f"""{JOSHUA_EDUCATION_MARKER_START}
{_css_block()}
<section class="px-margin-mobile md:px-margin-desktop py-24 bg-surface-container relative z-10 border-y border-outline-variant/10" data-woa-joshua-education="1" id="continuing-education">
<div class="max-w-6xl mx-auto">
<div class="woa-featured-layout">
<div class="space-y-6 order-2 lg:order-1">
<span class="text-label-caps font-label-caps text-secondary uppercase tracking-[0.2em]">Never standing still</span>
<h2 class="text-headline-lg font-headline-lg text-on-surface">Advancing the Craft — Seminars &amp; Mastery</h2>
<p class="text-body-lg font-body-lg text-on-surface-variant leading-relaxed">Joshua Cole does not coast on reputation. He attended art school, oil painting school, and illustration school, and he regularly attends and <strong class="text-on-surface">pays out of pocket</strong> for advanced art and tattoo seminars, workshops, and industry intensives — investing in drawing, realism, color theory, and technical innovation so every collector at Work of Art gets current-world skill, not yesterday&apos;s tricks.</p>
<p class="text-body-md text-on-surface-variant leading-relaxed">That fine-art background also shows up beyond the tattoo chair: Joshua designs Work of Art merchandise, T-shirts, and advertising, keeping the studio&apos;s visual identity in the hands of an artist who works with the brand every day.</p>
<p class="text-body-md text-on-surface-variant leading-relaxed">That commitment is why Joshua trains artists in-studio, pushes large-scale realism further each year, and treats every session like a masterclass. When you book Joshua, you are booking an artist who is still in the room learning — on purpose.</p>
<ul class="text-body-md text-on-surface-variant space-y-2 list-disc pl-5">
<li>Ongoing tattoo and fine-art education beyond the chair</li>
<li>Art school, oil painting school, and illustration school foundation</li>
<li>Seminars focused on realism, composition, and advanced technique</li>
<li>Studio merchandise, T-shirt, and advertising design by Joshua</li>
<li>Skills brought straight back to Las Vegas for your custom work</li>
</ul>
<a class="inline-flex items-center gap-2 text-secondary font-label-caps text-label-caps uppercase tracking-widest underline hover:no-underline mt-4 min-h-[48px]" href="{permalink}" rel="noopener noreferrer" target="_blank">See seminar reel on Instagram</a>
</div>
<div class="order-1 lg:order-2 max-w-[420px] w-full mx-auto lg:mx-0 lg:ml-auto">
{seminar_card}
</div>
</div>
</div>
</section>
{JOSHUA_EDUCATION_MARKER_END}"""
