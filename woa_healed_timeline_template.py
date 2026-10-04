#!/usr/bin/env python3
"""One healed-photo timeline: Fresh, about 4 weeks, 3+ months.

A stage gets an image only when that file is on disk. Missing stages are
labeled as not on file. They are not empty frames and they are not "coming soon."
"""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHONE_DISPLAY = "(725) 224-1240"
TEL = "tel:+17252241240"
SMS = "sms:+17252241240"
APPOINTMENTS = "/appointments/"

STAGE_ORDER = ("fresh", "four_weeks", "settled")
STAGE_HEADINGS = {
    "fresh": "Fresh",
    "four_weeks": "About 4 weeks",
    "settled": "3+ months",
}


def classify_stage(stage: str, stem: str) -> str:
    """Map an existing caption or filename onto the three supported stages."""
    label = (stage or "").lower()
    name = (stem or "").lower()
    if "4 week" in label or "four week" in label or "week 4" in label:
        return "four_weeks"
    if "vs healed" in label or "fresh vs healed" in label:
        return "settled"
    if (
        label.startswith("fresh")
        or "day 0" in label
        or "bandage" in label
        or "in-studio" in label
        or "in progress" in label
        or name.startswith("fresh-")
    ):
        return "fresh"
    return "settled"


def file_exists(folder: str, stem: str) -> tuple[bool, bool]:
    base = ROOT / folder / stem
    return base.with_suffix(".webp").is_file(), base.with_suffix(".png").is_file()


def picture_html(folder: str, stem: str, alt: str, *, eager: bool = False) -> str:
    webp_ok, png_ok = file_exists(folder, stem)
    if not webp_ok and not png_ok:
        return ""
    webp = f"/{folder}/{stem}.webp"
    png = f"/{folder}/{stem}.png"
    src = png if png_ok else webp
    loading = "eager" if eager else "lazy"
    source = f'<source srcset="{webp}" type="image/webp"/>' if webp_ok else ""
    return (
        f"<picture>{source}"
        f'<img alt="{html.escape(alt)}" class="w-full h-auto object-cover" decoding="async" '
        f'height="800" loading="{loading}" src="{src}" width="800"/></picture>'
    )


def request_healed_aside(*, has_healed: bool, source_path: str) -> str:
    if has_healed:
        title = "Send a later healed photo"
        lead = (
            "A healed photo is already on this page. If you have a later photo of the same piece, "
            "text or email the studio. There is no upload form — send the image by text or email."
        )
    else:
        title = "Request a healed photo"
        lead = (
            "This piece does not have a healed photo on the site. Text the studio or use the "
            "appointments form and we can follow up after your visit. We will not publish a stand-in image."
        )
    return f"""<aside class="mt-6 border border-outline-variant/40 bg-surface-container-low p-6 space-y-3" data-woa-request-healed="1">
<h3 class="font-headline-md text-on-surface text-xl">{html.escape(title)}</h3>
<p class="font-body-md text-on-surface-variant">{html.escape(lead)}</p>
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline hover:no-underline" href="{SMS}">Text {PHONE_DISPLAY}</a> · <a class="text-secondary underline hover:no-underline" href="{TEL}">Call {PHONE_DISPLAY}</a> · <a class="text-secondary underline hover:no-underline" href="#" data-woa-email-us="1">Email us now</a> · <a class="text-secondary underline hover:no-underline" href="{APPOINTMENTS}">Appointments form</a></p>
</aside>"""


def timeline_html(
    photos: list[tuple[str, str, str, str, str]],
    *,
    has_healed: bool,
    source_path: str,
    eager: bool = False,
) -> str:
    """photos: (bucket, folder, stem, stage_label, alt) for files that exist."""
    grouped: dict[str, list[tuple[str, str, str, str]]] = {key: [] for key in STAGE_ORDER}
    seen: set[str] = set()
    for bucket, folder, stem, stage_label, alt in photos:
        if bucket not in grouped or stem in seen:
            continue
        webp_ok, png_ok = file_exists(folder, stem)
        if not webp_ok and not png_ok:
            continue
        seen.add(stem)
        grouped[bucket].append((folder, stem, stage_label, alt))

    rows = []
    first_image = True
    for bucket in STAGE_ORDER:
        items = grouped[bucket]
        heading = STAGE_HEADINGS[bucket]
        if not items:
            rows.append(
                f"""<li class="border border-outline-variant/30 p-4 bg-surface">
<p class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-2">{heading}</p>
<p class="font-body-md text-on-surface-variant">No studio photo on file for this stage.</p>
</li>"""
            )
            continue
        figures = []
        for folder, stem, stage_label, alt in items:
            use_eager = eager and first_image
            first_image = False
            figures.append(
                f"""<figure class="border border-outline-variant/30 bg-surface overflow-hidden">
{picture_html(folder, stem, alt, eager=use_eager)}
<figcaption class="p-3 font-label-caps text-[10px] uppercase tracking-widest text-secondary">{html.escape(stage_label)}</figcaption>
</figure>"""
            )
        grid = "grid-cols-1" if len(figures) == 1 else "grid-cols-1 sm:grid-cols-2"
        rows.append(
            f"""<li class="border border-outline-variant/30 p-4 bg-surface space-y-3">
<p class="font-label-caps text-secondary uppercase tracking-widest text-[10px]">{heading}</p>
<div class="grid {grid} gap-3">{"".join(figures)}</div>
</li>"""
        )

    return f"""<div class="mt-6" data-woa-heal-stages="1">
<p class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-2">Documented stages</p>
<p class="font-body-md text-on-surface-variant mb-4">Fresh, about 4 weeks, and 3+ months. A photo appears only when that file is on disk.</p>
<ol class="space-y-4 list-none pl-0">{"".join(rows)}</ol>
{request_healed_aside(has_healed=has_healed, source_path=source_path)}
</div>"""
