#!/usr/bin/env python3
"""Print rsync --exclude patterns for slugs that must not ship on GitHub Pages."""

from __future__ import annotations

from deploy_stitch_site_root import SKIP_DEPLOY_SLUGS
from woa_url_aliases import ALIASES_BY_SOURCE, MUST_PUBLISH_ALIAS_SOURCES


def gh_pages_exclude_slugs() -> frozenset[str]:
    """Legacy redirect stubs and alias source folders — canonical short URLs only.

    MUST_PUBLISH_ALIAS_SOURCES stay on GitHub Pages. Those URLs are the AI
    source of truth in robots.txt, llms.txt, and ai.txt, and Pages cannot 301.
    """
    return (
        frozenset(SKIP_DEPLOY_SLUGS) | frozenset(ALIASES_BY_SOURCE.keys())
    ) - MUST_PUBLISH_ALIAS_SOURCES


def main() -> int:
    for slug in sorted(gh_pages_exclude_slugs()):
        print(f"--exclude={slug}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
