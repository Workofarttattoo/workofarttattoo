#!/usr/bin/env python3
"""Homepage availability urgency — text-first conversion prompt."""

from __future__ import annotations

from pathlib import Path

from woa_nav_config import STUDIO_PHONE_PARENS, STUDIO_PHONE_TEL

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
ROOT_HOME = ROOT / "code.html"

START = "<!-- WOA_AVAILABILITY_URGENCY_START -->"
END = "<!-- WOA_AVAILABILITY_URGENCY_END -->"

BLOCK = f"""{START}
<section aria-label="Today's availability" class="woa-availability-urgency px-margin-mobile md:px-margin-desktop py-4 bg-surface-container border-b border-outline-variant/30" data-woa-availability="1">
<div class="max-w-3xl mx-auto flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
<p class="font-body-md text-on-surface m-0"><strong class="text-secondary">Availability:</strong> Katelyn — piercing daily 3 PM–9 PM · Joshua — tattoo availability by request</p>
<a class="inline-flex shrink-0 bg-secondary text-on-secondary px-6 py-2.5 font-label-caps text-[11px] tracking-widest uppercase hover:bg-secondary-fixed transition-colors" href="{STUDIO_PHONE_TEL}">Text for availability · {STUDIO_PHONE_PARENS}</a>
</div>
</section>
{END}
"""


def inject(html: str) -> tuple[str, bool]:
    if START in html:
        import re

        new = re.sub(rf"{re.escape(START)}[\s\S]*?{re.escape(END)}", BLOCK, html, count=1)
        return new, new != html
    anchor = "<!-- WOA_HOME_WELCOME_END -->"
    if anchor not in html:
        return html, False
    return html.replace(anchor, anchor + "\n" + BLOCK, 1), True


def main() -> int:
    n = 0
    for path in (HOME, ROOT_HOME):
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated, ok = inject(raw)
        if ok:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {path.relative_to(ROOT)}")
            n += 1
    print(f"done — updated {n} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
