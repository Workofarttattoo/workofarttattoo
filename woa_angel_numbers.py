#!/usr/bin/env python3
"""Stable angel-number assignment for every public HTML page.

Numbers cycle 222 → 777 → 333 across public paths sorted lexicographically.
Existing assignments are kept so a rebuild of the same page set does not
reshuffle them. New paths take the next numbers in that cycle.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from generate_gh_pages_excludes import gh_pages_exclude_slugs
from woa_nav_config import HOME_SLUG
from woa_page_consolidation import (
    CONSOLIDATION_REDIRECTS,
    GSC_OBSOLETE_PATH_REDIRECTS,
    gsc_obsolete_slug_redirects,
)
from woa_url_aliases import ALIASES_BY_SOURCE, MUST_PUBLISH_ALIAS_SOURCES

ROOT = Path(__file__).resolve().parent
MAPPING_PATH = ROOT / "config" / "angel-numbers.json"
CYCLE = ("222", "777", "333")

SKIP_PARTS = frozenset(
    {
        ".git",
        ".github",
        "tools",
        "audits",
        "skipped_upload_build",
        "artists_raw",
        "node_modules",
        "__pycache__",
        ".snapshots",
        "piercing_asset_chunks",
        "content-needed",
        "artists_build",
    }
)

META_TAG_RE = re.compile(r"<meta\b[^>]*>", re.I)
ATTR_RE = re.compile(r"([:\w-]+)\s*=\s*([\"'])(.*?)\2", re.I | re.S)
CONTENT_ATTR_RE = re.compile(r"(\bcontent\s*=\s*)([\"'])(.*?)\2", re.I | re.S)
ANGEL_SUFFIX_RE = re.compile(r"(?<!\d)(?:222|777|333)\s*$")
ANGEL_BLOCK_RE = re.compile(
    r"\n?<p\b[^>]*\bdata-woa-angel-number=\"(?:222|777|333)\"[^>]*>\s*(?:222|777|333)\s*</p>\n?",
    re.I,
)
REFRESH_RE = re.compile(r"http-equiv\s*=\s*[\"']refresh[\"']", re.I)
ESSENTIAL_RE = re.compile(
    r"\b(?:las vegas|vegas|tattoo|tattoos|piercing|pierce|book|booking|"
    r"appointment|appointments|tropicana|walk-?ins?|hours|consult|cover-?ups?|"
    r"studio|aftercare|healing|realism|sleeve|call|text|service)\b|\b725\b",
    re.I,
)
DESCRIPTION_KEYS = {"description", "og:description", "twitter:description"}

# Append without trimming unless the plain description is already very long.
# Service, location, and booking facts are never removed to make room.
LONG_DESCRIPTION = 220


def obsolete_redirect_paths() -> set[str]:
    """Public paths that 301 (or are the duplicate homepage folder)."""
    paths = {f"/{HOME_SLUG}/"}
    for slug, _dest in CONSOLIDATION_REDIRECTS:
        paths.add(f"/{slug}/")
    for slug in gsc_obsolete_slug_redirects():
        paths.add(f"/{slug}/")
    for src, _dest in GSC_OBSOLETE_PATH_REDIRECTS:
        path = src if src.startswith("/") else f"/{src}"
        if not path.endswith("/"):
            path += "/"
        paths.add(path)
    for slug in ALIASES_BY_SOURCE:
        if slug not in MUST_PUBLISH_ALIAS_SOURCES:
            paths.add(f"/{slug}/")
    return paths


def is_redirect_html(text: str) -> bool:
    return bool(REFRESH_RE.search(text[:20_000]))


def discover_public_paths(root: Path | None = None) -> list[str]:
    """Sorted public paths that production publishes as HTML 200s."""
    root = (root or ROOT).resolve()
    excludes = gh_pages_exclude_slugs()
    obsolete = obsolete_redirect_paths()
    paths: set[str] = set()

    def consider(public_path: str, sample: Path) -> None:
        if not public_path.startswith("/") or "?" in public_path:
            return
        if public_path in obsolete:
            return
        if not sample.is_file():
            return
        text = sample.read_text(encoding="utf-8", errors="replace")
        if is_redirect_html(text):
            return
        if "<html" not in text[:12_000].lower():
            return
        paths.add(public_path if public_path == "/" else public_path.rstrip("/") + "/")

    home = root / HOME_SLUG / "code.html"
    consider("/", home if home.is_file() else root / "code.html")

    for code in root.rglob("code.html"):
        if any(part in SKIP_PARTS for part in code.parts):
            continue
        rel = code.relative_to(root)
        if rel == Path("code.html"):
            continue
        top = rel.parts[0]
        if top in excludes or top == HOME_SLUG or top.startswith("home_work_of_art"):
            continue
        consider("/" + rel.parent.as_posix() + "/", code)

    artists_build = root / "artists_build"
    if artists_build.is_dir():
        for page in sorted(artists_build.glob("*.html")):
            consider(f"/artists/{page.stem}/", page)

    return sorted(paths)


def load_mapping(path: Path | None = None) -> dict[str, str]:
    path = path or MAPPING_PATH
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    pages = data.get("pages") if isinstance(data, dict) else None
    if not isinstance(pages, dict):
        return {}
    kept: dict[str, str] = {}
    for key, value in pages.items():
        if isinstance(key, str) and value in CYCLE:
            kept[key] = value
    return kept


def assign_numbers(paths: list[str], stored: dict[str, str]) -> dict[str, str]:
    """Keep stored numbers. First-seen sets follow sorted index order."""
    current = {path: stored[path] for path in paths if stored.get(path) in CYCLE}
    missing = [path for path in paths if path not in current]
    if not current:
        for index, path in enumerate(paths):
            current[path] = CYCLE[index % 3]
        return current
    start = len(current)
    for offset, path in enumerate(missing):
        current[path] = CYCLE[(start + offset) % 3]
    return current


def save_mapping(assigned: dict[str, str], stored: dict[str, str], path: Path | None = None) -> None:
    path = path or MAPPING_PATH
    pages = {key: value for key, value in stored.items() if value in CYCLE}
    pages.update(assigned)
    payload = {
        "cycle": list(CYCLE),
        "pages": {key: pages[key] for key in sorted(pages)},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def source_files(root: Path, public_path: str) -> list[Path]:
    """HTML sources that deploy publishes for this public path."""
    if public_path == "/":
        candidates = [
            root / HOME_SLUG / "code.html",
            root / "code.html",
            root / "index.html",
        ]
    else:
        folder = root / public_path.strip("/")
        candidates = [folder / "code.html", folder / "index.html"]
        parts = [part for part in public_path.strip("/").split("/") if part]
        if len(parts) == 2 and parts[0] == "artists":
            candidates.append(root / "artists_build" / f"{parts[1]}.html")
    files: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if not candidate.is_file():
            continue
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        text = candidate.read_text(encoding="utf-8", errors="replace")
        if is_redirect_html(text):
            continue
        seen.add(resolved)
        files.append(candidate)
    return files


def _tag_attrs(tag: str) -> dict[str, str]:
    return {match.group(1).lower(): match.group(3) for match in ATTR_RE.finditer(tag)}


def _meta_key(attrs: dict[str, str]) -> str:
    return (attrs.get("name") or attrs.get("property") or "").lower()


def _strip_suffix(text: str) -> str:
    return ANGEL_SUFFIX_RE.sub("", text).rstrip()


def _trim_nonessential(plain: str, number: str) -> str:
    if len(plain) + 1 + len(number) <= LONG_DESCRIPTION:
        return plain
    limit = 160 - (1 + len(number))
    words = plain.split()
    while len(words) > 8 and len(" ".join(words)) > limit:
        if ESSENTIAL_RE.search(" ".join(words[-8:])):
            break
        words.pop()
    return " ".join(words).rstrip(" ,;:-—")


def description_with_number(raw: str, number: str) -> str:
    raw_base = _strip_suffix(raw).rstrip()
    plain = _trim_nonessential(html.unescape(raw_base), number)
    if plain == html.unescape(raw_base):
        return f"{raw_base} {number}"
    return html.escape(f"{plain} {number}", quote=False)


def _replace_content(tag: str, content: str) -> str:
    def repl(match: re.Match[str]) -> str:
        quote = match.group(2)
        safe = content.replace(quote, "&quot;" if quote == '"' else "&#39;")
        return f"{match.group(1)}{quote}{safe}{quote}"

    updated, count = CONTENT_ATTR_RE.subn(repl, tag, count=1)
    return updated if count else tag


def apply_descriptions(html_text: str, number: str) -> str:
    tags = list(META_TAG_RE.finditer(html_text))
    description_raw = None
    for match in tags:
        attrs = _tag_attrs(match.group(0))
        if _meta_key(attrs) == "description" and "content" in attrs:
            description_raw = attrs["content"]
            break
    if description_raw is None:
        return html_text
    updated_description = description_with_number(description_raw, number)
    old_norm = re.sub(r"\s+", " ", _strip_suffix(html.unescape(description_raw))).strip()

    pieces: list[str] = []
    cursor = 0
    for match in tags:
        tag = match.group(0)
        attrs = _tag_attrs(tag)
        key = _meta_key(attrs)
        content = attrs.get("content")
        replacement = tag
        if key == "description" and content is not None:
            replacement = _replace_content(tag, description_with_number(content, number))
        elif key in DESCRIPTION_KEYS and content is not None:
            current_norm = re.sub(r"\s+", " ", _strip_suffix(html.unescape(content))).strip()
            if current_norm == old_norm:
                replacement = _replace_content(tag, updated_description)
        if replacement != tag:
            pieces.append(html_text[cursor:match.start()])
            pieces.append(replacement)
            cursor = match.end()
    pieces.append(html_text[cursor:])
    return "".join(pieces)


def visible_markup(number: str) -> str:
    return (
        f'<p data-woa-angel-number="{number}" '
        'style="display:block;visibility:visible;opacity:1;margin:1.5rem auto 5rem;'
        "padding:0.75rem 1rem;max-width:36rem;text-align:center;color:#f4efe4;"
        "background:#1a1a1a;border-top:1px solid #e9c349;font-size:1rem;line-height:1.5;"
        f'letter-spacing:0.18em;">{number}</p>'
    )


def apply_visible_number(html_text: str, number: str) -> str:
    html_text = ANGEL_BLOCK_RE.sub("\n", html_text)
    block = visible_markup(number)
    body_match = re.search(r"<body\b", html_text, re.I)
    start = body_match.start() if body_match else 0
    region = html_text[start:]
    footer = re.search(r"<footer\b", region, re.I)
    if footer:
        at = start + footer.start()
        return html_text[:at] + block + "\n" + html_text[at:]
    main_end = re.search(r"</main>", region, re.I)
    if main_end:
        at = start + main_end.start()
        return html_text[:at] + block + "\n" + html_text[at:]
    body_end = re.search(r"</body>", region, re.I)
    if body_end:
        at = start + body_end.start()
        return html_text[:at] + block + "\n" + html_text[at:]
    raise ValueError("no visible insertion point before footer, main, or body")


def apply_page(html_text: str, number: str) -> str:
    return apply_visible_number(apply_descriptions(html_text, number), number)


def hidden_markup(tag: str) -> bool:
    style = ""
    attrs = _tag_attrs(tag)
    style = attrs.get("style", "").lower().replace(" ", "")
    if "aria-hidden" in tag.lower():
        return True
    banned = (
        "display:none",
        "visibility:hidden",
        "opacity:0",
        "font-size:0",
        "text-indent:-",
    )
    return any(token in style for token in banned)
