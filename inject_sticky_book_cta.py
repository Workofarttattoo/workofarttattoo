#!/usr/bin/env python3
"""Sticky booking + free consultation CTA on every public page."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARKER = 'data-woa-sticky-book="1"'
BOOKING_HREF = "/appointments/"


def sticky_cta_for_path(path: Path | None) -> tuple[str, str]:
    """Return (href, visible label) matched to page intent."""
    if path is None:
        return BOOKING_HREF, "Book a Consultation"

    rel = str(path.relative_to(ROOT)).replace("\\", "/").lower()
    slug = path.parent.name if path.name == "code.html" else path.stem

    if "joshua-cole" in rel:
        return BOOKING_HREF, "Book With Joshua"
    if "katelyn-cole" in rel:
        return BOOKING_HREF, "Book a Piercing"
    if "cover-up-tattoos-las-vegas" in rel or "cover_up_tattoos" in rel:
        return BOOKING_HREF, "Ask About a Cover-Up"
    if slug == "appointments":
        return BOOKING_HREF, "Continue Booking"
    if any(
        token in rel
        for token in (
            "piercing",
            "ear_piercing",
            "helix",
            "nostril",
            "septum",
            "conch",
            "tragus",
            "daith",
            "rook",
            "labret",
            "best_piercing",
        )
    ):
        return BOOKING_HREF, "Book Your Piercing"
    if rel.startswith("tattoo_shop_") or "tattoo_shop_near" in rel or "/geo_" in rel:
        return BOOKING_HREF, "Check Availability"
    if "realism" in rel:
        return BOOKING_HREF, "Book a Tattoo Consultation"
    return BOOKING_HREF, "Book a Consultation"


def sticky_link_for_path(path: Path | None) -> str:
    href, label = sticky_cta_for_path(path)
    esc_label = label.replace("&", "&amp;")
    return (
        f'<a data-woa-sticky-book="1" href="{href}" '
        f'aria-label="{esc_label}">'
        '<span aria-hidden="true" class="woa-sticky-book-icon material-symbols-outlined">'
        "calendar_month</span>"
        f'<span class="woa-sticky-book-text">{esc_label}</span>'
        "</a>"
    )


STICKY_CSS = """
<style data-woa-sticky-book-css="1">
[data-woa-sticky-book] {
  position: fixed;
  right: max(0.85rem, env(safe-area-inset-right, 0px));
  bottom: max(0.85rem, env(safe-area-inset-bottom, 0px));
  left: auto;
  z-index: 880;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  max-width: min(16rem, calc(100vw - 1.75rem));
  padding: 0.65rem 0.9rem;
  background: rgba(12, 12, 12, 0.92);
  color: #ffe088;
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  line-height: 1.35;
  text-decoration: none;
  border: 1px solid rgba(233, 195, 73, 0.55);
  border-radius: 2px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  opacity: 0.93;
  transition: opacity 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}
.woa-sticky-book-icon {
  font-family: "Material Symbols Outlined";
  font-size: 1.15rem;
  line-height: 1;
  color: #e9c349;
  flex-shrink: 0;
  font-variation-settings: "FILL" 0, "wght" 500, "GRAD" 0, "opsz" 24;
}
.woa-sticky-book-text {
  text-align: left;
}
@media (min-width: 768px) {
  [data-woa-sticky-book] {
    right: max(1.25rem, env(safe-area-inset-right, 0px));
    bottom: max(1.25rem, env(safe-area-inset-bottom, 0px));
    max-width: 14rem;
    padding: 0.75rem 1rem;
    font-size: 0.6875rem;
  }
}
[data-woa-sticky-book]:hover,
[data-woa-sticky-book]:focus-visible {
  opacity: 1;
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(233, 195, 73, 0.22);
  outline: 2px solid rgba(233, 195, 73, 0.45);
  outline-offset: 2px;
}
@media (prefers-reduced-motion: reduce) {
  [data-woa-sticky-book] {
    transition: none;
  }
  [data-woa-sticky-book]:hover,
  [data-woa-sticky-book]:focus-visible {
    transform: none;
  }
}
</style>
"""

STICKY_CSS_RE = re.compile(
    r"<style data-woa-sticky-book-css=\"1\">.*?</style>\s*",
    re.DOTALL,
)
STICKY_LINK_RE = re.compile(
    r'<a\b(?=[^>]*\bdata-woa-sticky-book="1")[^>]*>.*?</a>\s*',
    re.DOTALL,
)
LEGACY_MOBILE_BAR_RE = re.compile(
    r"<!-- Sticky Booking Bar \(Mobile Only\) -->\s*"
    r'<div class="md:hidden fixed bottom-0[\s\S]*?</div>\s*',
    re.MULTILINE,
)


def strip_legacy_mobile_bar(html: str) -> str:
    return LEGACY_MOBILE_BAR_RE.sub("", html)


def inject(html: str, path: Path | None = None) -> str:
    html = strip_legacy_mobile_bar(html)
    html = STICKY_CSS_RE.sub("", html)
    html = STICKY_LINK_RE.sub("", html)
    sticky_link = sticky_link_for_path(path)
    if "</head>" in html:
        html = html.replace("</head>", STICKY_CSS + "\n</head>", 1)
    html = html.replace("</body>", sticky_link + "\n</body>", 1)
    return html


def iter_targets() -> list[Path]:
    targets: list[Path] = []
    for path in ROOT.rglob("code.html"):
        if "skipped" in path.parts:
            continue
        targets.append(path)
    for path in (ROOT / "artists_build").glob("*.html"):
        targets.append(path)
    extra = ROOT / "artists" / "code.html"
    if extra.is_file():
        targets.append(extra)
    root_home = ROOT / "code.html"
    if root_home.is_file():
        targets.append(root_home)
    return sorted(set(targets))


def main() -> int:
    changed = 0
    for path in iter_targets():
        raw = path.read_text(encoding="utf-8")
        updated = inject(raw, path)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Done: sticky booking CTA on {changed} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
