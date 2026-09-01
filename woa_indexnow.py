#!/usr/bin/env python3
"""
IndexNow URL submission for www.workofarttattoo.com.

Validates canonical HTTPS URLs, maps git-changed sources to public URLs,
and POSTs to https://api.indexnow.org/IndexNow.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from woa_ai_crawl import SITE_ORIGIN
from woa_page_consolidation import RETIRE_OVERLAP_SLUGS
from woa_url_aliases import URL_ALIASES

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config" / "indexnow.json"
INDEXNOW_API = "https://api.indexnow.org/IndexNow"

ASSET_SUFFIXES = frozenset(
    {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".gif",
        ".svg",
        ".ico",
        ".css",
        ".js",
        ".mjs",
        ".map",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
        ".pdf",
        ".xml",
        ".txt",
        ".json",
        ".md",
    }
)

SOURCE_SLUG_TO_SHORT: dict[str, str] = {a.source_slug: a.short_slug for a in URL_ALIASES}

INITIAL_SUBMISSION_URLS: tuple[str, ...] = (
    f"{SITE_ORIGIN}/",
    f"{SITE_ORIGIN}/fine_line_tattoos_las_vegas_master_authority_guide/",
    f"{SITE_ORIGIN}/tattoo_shop_near_the_strip_nap_corrected/",
    f"{SITE_ORIGIN}/walk-in-tattoos-las-vegas/",
    f"{SITE_ORIGIN}/cover-up-tattoos-las-vegas/",
    f"{SITE_ORIGIN}/realism-tattoos-las-vegas/",
    f"{SITE_ORIGIN}/artists/joshua-cole/",
    f"{SITE_ORIGIN}/artists/katelyn-cole/",
    f"{SITE_ORIGIN}/piercing-guide-las-vegas/",
    f"{SITE_ORIGIN}/start_here/",
    f"{SITE_ORIGIN}/skin_science_tattoo_dermatology_authority_guide/",
    f"{SITE_ORIGIN}/dermis_skin_science_las_vegas_authority_guide/",
)


def load_config() -> dict[str, str]:
    if not CONFIG_PATH.is_file():
        raise FileNotFoundError(f"Missing IndexNow config: {CONFIG_PATH}")
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    host = (cfg.get("host") or "").strip()
    key = (cfg.get("key") or "").strip()
    if not host or not key:
        raise ValueError("config/indexnow.json requires host and key")
    return {"host": host, "key": key}


def key_location(host: str, key: str) -> str:
    return f"https://{host}/{key}.txt"


def normalize_public_url(url: str) -> str | None:
    raw = (url or "").strip()
    if not raw:
        return None
    if raw.startswith("/"):
        raw = f"{SITE_ORIGIN}{raw}"
    parts = urlsplit(raw)
    if parts.scheme != "https":
        return None
    if parts.netloc != "www.workofarttattoo.com":
        return None
    if parts.query or parts.fragment:
        return None
    path = parts.path or "/"
    if not path.endswith("/"):
        if "." in path.rsplit("/", 1)[-1]:
            return None
        path = path + "/"
    return urlunsplit(("https", "www.workofarttattoo.com", path, "", ""))


def is_noindex_html(path: Path) -> bool:
    if not path.is_file():
        return True
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    if 'name="robots"' in text and "noindex" in text:
        return True
    if "http-equiv=\"refresh\"" in text and "noindex" in text:
        return True
    return False


def canonical_from_html(path: Path) -> str | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        text,
        re.I,
    )
    if not match:
        match = re.search(
            r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
            text,
            re.I,
        )
    if match:
        return normalize_public_url(match.group(1))
    return None


def slug_folder_to_url(slug: str) -> str:
    short = SOURCE_SLUG_TO_SHORT.get(slug)
    if short:
        return f"{SITE_ORIGIN}/{short}/"
    return f"{SITE_ORIGIN}/{slug}/"


def source_path_to_public_url(rel_path: str, repo_root: Path = ROOT) -> str | None:
    p = Path(rel_path)
    if p.suffix.lower() in ASSET_SUFFIXES and p.name != "code.html":
        return None
    parts = p.parts
    if "skipped_upload_build" in parts or ".git" in parts or ".github" in parts:
        return None
    if p.name == "code.html":
        slug = p.parent.name if p.parent != Path(".") else ""
        if slug in RETIRE_OVERLAP_SLUGS:
            return None
        html_path = repo_root / p
        if is_noindex_html(html_path):
            return None
        canonical = canonical_from_html(html_path)
        if canonical:
            return canonical
        if not slug or slug == "code.html":
            return f"{SITE_ORIGIN}/"
        if slug == "home_work_of_art_tattoo_piercing":
            return f"{SITE_ORIGIN}/"
        return slug_folder_to_url(slug)
    if p.parent.name == "artists_build" and p.suffix.lower() == ".html":
        slug = p.stem
        artist_html = repo_root / "artists" / slug / "code.html"
        if artist_html.is_file() and is_noindex_html(artist_html):
            return None
        return f"{SITE_ORIGIN}/artists/{slug}/"
    return None


def filter_submittable_urls(urls: list[str], repo_root: Path = ROOT) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for url in urls:
        normalized = normalize_public_url(url)
        if not normalized or normalized in seen:
            continue
        path = urlsplit(normalized).path.strip("/")
        slug = path.split("/")[0] if path else ""
        if slug in RETIRE_OVERLAP_SLUGS:
            continue
        slug_dir = repo_root / slug
        code_html = slug_dir / "code.html"
        if slug and code_html.is_file() and is_noindex_html(code_html):
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def build_payload(urls: list[str], cfg: dict[str, str] | None = None) -> dict[str, object]:
    cfg = cfg or load_config()
    clean = filter_submittable_urls(urls)
    return {
        "host": cfg["host"],
        "key": cfg["key"],
        "keyLocation": key_location(cfg["host"], cfg["key"]),
        "urlList": clean,
    }


def submit_indexnow(urls: list[str], *, dry_run: bool = False) -> tuple[int, dict[str, object]]:
    payload = build_payload(urls)
    url_list = payload["urlList"]
    log: dict[str, object] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "submitted_count": len(url_list),
        "urls": url_list,
        "keyLocation": payload["keyLocation"],
    }
    if not url_list:
        log["status"] = "skipped"
        log["http_status"] = None
        log["success"] = True
        log["message"] = "No URLs to submit"
        return 0, log
    body = json.dumps(payload).encode("utf-8")
    if dry_run:
        log["status"] = "dry_run"
        log["http_status"] = None
        log["success"] = True
        return 0, log
    req = urllib.request.Request(
        INDEXNOW_API,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            log["http_status"] = status
            log["success"] = status in (200, 202)
            log["status"] = "accepted" if log["success"] else "rejected"
    except urllib.error.HTTPError as exc:
        log["http_status"] = exc.code
        log["success"] = exc.code in (200, 202)
        log["status"] = "accepted" if log["success"] else "http_error"
        log["message"] = exc.reason
    except urllib.error.URLError as exc:
        log["http_status"] = None
        log["success"] = False
        log["status"] = "network_error"
        log["message"] = str(exc.reason)
    return (0 if log.get("success") else 1), log


def git_changed_source_paths(base_ref: str, head_ref: str = "HEAD") -> list[str]:
    cmd = ["git", "diff", "--name-only", base_ref, head_ref, "--"]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def urls_from_git_diff(base_ref: str, head_ref: str = "HEAD") -> list[str]:
    urls: list[str] = []
    for rel in git_changed_source_paths(base_ref, head_ref):
        mapped = source_path_to_public_url(rel)
        if mapped:
            urls.append(mapped)
    return filter_submittable_urls(urls)


def read_previous_deploy_sha() -> str | None:
    marker = ROOT / "DEPLOYED_MAIN_SHA"
    if marker.is_file():
        sha = marker.read_text(encoding="utf-8").strip()
        return sha or None
    proc = subprocess.run(
        ["git", "rev-parse", "origin/gh-pages"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    gh_ref = proc.stdout.strip()
    proc2 = subprocess.run(
        ["git", "show", f"{gh_ref}:DEPLOYED_MAIN_SHA"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc2.returncode != 0:
        return None
    return proc2.stdout.strip() or None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Submit canonical URLs to IndexNow")
    parser.add_argument("--urls", nargs="*", help="Explicit URLs to submit")
    parser.add_argument("--initial", action="store_true", help="Submit initial curated URL set")
    parser.add_argument(
        "--from-deploy",
        action="store_true",
        help="Submit URLs changed since previous production deploy",
    )
    parser.add_argument("--base-ref", help="Git ref for changed-URL detection")
    parser.add_argument("--head-ref", default="HEAD", help="Git head ref (default HEAD)")
    parser.add_argument("--dry-run", action="store_true", help="Validate payload only")
    args = parser.parse_args(argv)

    urls: list[str] = []
    if args.initial:
        urls.extend(INITIAL_SUBMISSION_URLS)
    if args.urls:
        urls.extend(args.urls)
    if args.from_deploy:
        base = args.base_ref or read_previous_deploy_sha()
        if not base:
            print("No previous deploy SHA found; skipping changed-URL submission.", file=sys.stderr)
        else:
            urls.extend(urls_from_git_diff(base, args.head_ref))
            print(f"Changed URLs since {base[:7]}: {len(urls)}")

    urls = filter_submittable_urls(urls)
    code, log = submit_indexnow(urls, dry_run=args.dry_run)
    print(json.dumps(log, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
