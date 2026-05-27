#!/usr/bin/env python3
"""Shared gold cursor + sparkle trail for static WOA pages."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SPARKLE_CSS_HREF = "/home_work_of_art_tattoo_piercing/woa-sparkle.css"

SPARKLE_LINK = f'<link href="{SPARKLE_CSS_HREF}" rel="stylesheet"/>\n'

SPARKLE_MARKUP = '<div id="sparkle-cursor" aria-hidden="true"></div>\n'

SPARKLE_SCRIPT = """<script data-woa-sparkle-cursor="1" type="text/javascript">
(function () {
  "use strict";
  var dot = document.getElementById("sparkle-cursor");
  if (!dot) return;

  function enabled() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return false;
    if (!window.matchMedia("(hover: hover)").matches) return false;
    if (!window.matchMedia("(pointer: fine)").matches) return false;
    return true;
  }

  if (!enabled()) {
    dot.style.display = "none";
    document.documentElement.classList.remove("woa-sparkle-on");
    return;
  }

  document.documentElement.classList.add("woa-sparkle-on");
  var throttle = 0;

  document.addEventListener(
    "mousemove",
    function (e) {
      dot.style.left = e.clientX - 11 + "px";
      dot.style.top = e.clientY - 11 + "px";

      var now = performance.now();
      if (now - throttle < 45) return;
      throttle = now;
      if (Math.random() > 0.42) return;

      var spark = document.createElement("span");
      spark.className = "sparkle";
      var size = 4 + Math.random() * 6;
      spark.style.width = size + "px";
      spark.style.height = size + "px";
      spark.style.left = e.clientX + "px";
      spark.style.top = e.clientY + "px";

      var ang = Math.random() * Math.PI * 2;
      var dist = 20 + Math.random() * 38;
      spark.style.setProperty("--x", Math.cos(ang) * dist + "px");
      spark.style.setProperty("--y", Math.sin(ang) * dist + "px");

      document.body.appendChild(spark);
      window.setTimeout(function () {
        spark.remove();
      }, 1450);
    },
    { passive: true }
  );
})();
</script>
"""

SPARKLE_MARKER = "<!-- WOA_SPARKLE_CURSOR -->"

OLD_SPARKLE_SCRIPT_RE = re.compile(
    r'<script[^>]*>\s*\(function\s*\(\)\s*\{\s*"use strict";\s*var dot = document\.getElementById\("sparkle-cursor"\);[\s\S]*?\}\)\(\);\s*</script>',
    re.MULTILINE,
)
LEGACY_CONTAINER_RE = re.compile(
    r'<div id="sparkle-container"></div>\s*',
    re.IGNORECASE,
)


def sparkle_head_link() -> str:
    return SPARKLE_LINK


def sparkle_body_open() -> str:
    return SPARKLE_MARKUP


def sparkle_footer_script() -> str:
    return SPARKLE_SCRIPT


def sparkle_bundle_after_body() -> str:
    return SPARKLE_MARKUP


def inject_sparkle_into_html(html: str) -> tuple[str, bool]:
    """Ensure sparkle CSS, cursor node, and script are present."""
    changed = False
    out = html

    if SPARKLE_CSS_HREF not in out:
        head_close = out.find("</head>")
        if head_close >= 0:
            out = out[:head_close] + SPARKLE_LINK + out[head_close:]
            changed = True

    out, n = LEGACY_CONTAINER_RE.subn(
        '<div id="sparkle-cursor" aria-hidden="true"></div>\n', out, count=1
    )
    changed = changed or n > 0

    if 'id="sparkle-cursor"' not in out:
        body_gt = out.find("<body")
        if body_gt >= 0:
            insert_at = out.find(">", body_gt) + 1
            out = out[:insert_at] + "\n" + SPARKLE_MARKUP + out[insert_at:]
            changed = True

    if 'data-woa-sparkle-cursor="1"' not in out:
        out2, n = OLD_SPARKLE_SCRIPT_RE.subn("", out, count=1)
        if n:
            out = out2
            changed = True
        body_close = out.rfind("</body>")
        if body_close >= 0:
            out = out[:body_close] + SPARKLE_SCRIPT + "\n" + out[body_close:]
            changed = True

    return out, changed
