#!/usr/bin/env python3
"""Print rsync --exclude patterns for slugs that must not ship on GitHub Pages."""

from __future__ import annotations

from deploy_stitch_site_root import SKIP_DEPLOY_SLUGS
from woa_url_aliases import ALIASES_BY_SOURCE


def gh_pages_exclude_slugs() -> frozenset[str]:
    """Legacy redirect stubs and alias source folders — canonical short URLs only."""
    return frozenset(SKIP_DEPLOY_SLUGS) | frozenset(ALIASES_BY_SOURCE.keys())


def main() -> int:
    for slug in sorted(gh_pages_exclude_slugs()):
        print(f"--exclude={slug}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
