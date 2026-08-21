#!/usr/bin/env python3
"""Apply canonical homepage title and meta description."""

from __future__ import annotations

import re
from pathlib import Path

from woa_nav_config import HOME_META_DESCRIPTION, HOME_SLUG, HOME_TITLE, ROOT_A

ROOT = ROOT_A


def fix(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    updated = raw
    updated = re.sub(
        r"<title>[^<]*</title>",
        f"<title>{HOME_TITLE.replace('&', '&amp;')}</title>",
        updated,
        count=1,
    )
    updated = re.sub(
        r'(<meta content=")[^"]*(" name="description"/>)',
        rf"\1{HOME_META_DESCRIPTION}\2",
        updated,
        count=1,
    )
    if updated == raw:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    home = ROOT / HOME_SLUG / "code.html"
    if not home.is_file():
        print(f"[skip] missing {home}")
        return 1
    if fix(home):
        print(f"[ok] {home.relative_to(ROOT)}")
    else:
        print("[skip] homepage already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
