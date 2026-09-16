#!/usr/bin/env python3
"""Canonical URL helpers — https://www.workofarttattoo.com/ with trailing slashes."""

from __future__ import annotations

from woa_nav_config import SITE_CANONICAL_HOST

CANONICAL_ORIGIN = SITE_CANONICAL_HOST.rstrip("/")
if not CANONICAL_ORIGIN.startswith("https://www."):
    # Enforce www + https even if siteData drifts during local edits.
    CANONICAL_ORIGIN = "https://www.workofarttattoo.com"


def normalize_path(path: str) -> str:
    """Root-relative path with leading and trailing slash (home is /)."""
    path = (path or "/").strip()
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and not path.endswith("/"):
        path = path + "/"
    return path


def canonical_url(path: str = "/") -> str:
    """Absolute canonical URL for a site path."""
    path = normalize_path(path)
    if path == "/":
        return f"{CANONICAL_ORIGIN}/"
    return f"{CANONICAL_ORIGIN}{path}"


def is_asset_path(path: str) -> bool:
    """Paths that should not receive forced trailing-slash redirects."""
    lower = path.lower().split("?", 1)[0]
    if lower.endswith(
        (
            ".xml",
            ".txt",
            ".json",
            ".webp",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".svg",
            ".css",
            ".js",
            ".ico",
            ".pdf",
            ".md",
        )
    ):
        return True
    return False
