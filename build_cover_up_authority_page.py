#!/usr/bin/env python3
"""Cover-up authority now lives at /cover-up-tattoos-las-vegas/.

Running this script writes the GitHub Pages retirement stub for the
legacy underscore URL instead of regenerating a competing page.
"""

from __future__ import annotations

from build_retired_cover_up_redirect import main


if __name__ == "__main__":
    raise SystemExit(main())
