#!/usr/bin/env python3
"""Build the small guide PDFs offered on the lead-capture pages."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "downloads"

STUDIO = [
    "Work of Art Tattoo & Piercing",
    "2375 E. Tropicana Ave, Suite 3, Las Vegas, NV 89119",
    "Daily 12 PM-12 AM",
    "725-224-1240",
    "Email us from https://www.workofarttattoo.com/appointments/",
]


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap(text: str, width: int = 88) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if len(trial) <= width:
            current = trial
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines or [""]


def build_pdf_bytes(title: str, blocks: list[str]) -> bytes:
    lines: list[tuple[str, int, bool]] = [(title, 18, True)]
    lines.append(("", 8, False))
    for block in blocks:
        if block == "":
            lines.append(("", 8, False))
            continue
        heading = block.startswith("# ")
        text = block[2:] if heading else block
        size = 13 if heading else 11
        for index, line in enumerate(_wrap(text, 78 if heading else 92)):
            lines.append((line, size if index == 0 or heading else 11, heading or (index == 0 and False)))

    pages: list[list[tuple[str, int, bool]]] = []
    current: list[tuple[str, int, bool]] = []
    y = 740
    for item in lines:
        step = item[1] + 5
        if y - step < 54 and current:
            pages.append(current)
            current = []
            y = 740
        current.append(item)
        y -= step
    if current:
        pages.append(current)

    objects: list[bytes] = [b""]  # 1-indexed

    def add(payload: bytes) -> int:
        objects.append(payload)
        return len(objects) - 1

    font_id = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    bold_id = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    content_ids: list[int] = []
    for page_lines in pages:
        commands: list[str] = ["BT"]
        y = 740
        for line, size, heading in page_lines:
            font = "F2" if heading or size >= 16 else "F1"
            commands.append(f"/{font} {size} Tf")
            commands.append(f"1 0 0 1 54 {y} Tm ({_escape(line)}) Tj")
            y -= size + 5
        commands.append("ET")
        stream = "\n".join(commands).encode("latin-1", errors="replace")
        content_ids.append(add(f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1") + stream + b"\nendstream"))

    page_ids: list[int] = []
    for content_id in content_ids:
        page_ids.append(
            add(
                (
                    f"<< /Type /Page /Parent PAGES 0 R /MediaBox [0 0 612 792] "
                    f"/Contents {content_id} 0 R /Resources << /Font << "
                    f"/F1 {font_id} 0 R /F2 {bold_id} 0 R >> >> >>"
                ).encode("latin-1")
            )
        )
    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    pages_id = add(f"<< /Type /Pages /Count {len(page_ids)} /Kids [{kids}] >>".encode("latin-1"))
    for page_id in page_ids:
        objects[page_id] = objects[page_id].replace(b"Parent PAGES 0 R", f"Parent {pages_id} 0 R".encode("latin-1"))
    catalog_id = add(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("latin-1"))

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, payload in enumerate(objects[1:], start=1):
        offsets.append(len(out))
        out.extend(f"{index} 0 obj\n".encode("latin-1"))
        out.extend(payload)
        out.extend(b"\nendobj\n")
    xref = len(out)
    out.extend(f"xref\n0 {len(objects)}\n".encode("latin-1"))
    out.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        out.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    out.extend(
        f"trailer << /Size {len(objects)} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("latin-1")
    )
    return bytes(out)


AFTERCARE = [
    "# What this is",
    "Studio aftercare notes for healing a tattoo in dry Las Vegas conditions. Follow the instructions your artist gives you for your piece. This checklist repeats the desert aftercare guide on workofarttattoo.com.",
    "",
    "# Do this",
    "Wash with clean hands, then pat dry. Gentle washing is enough.",
    "Low humidity can make a fresh tattoo feel tight. Use a thin layer of product. More product is not always safer. Over-moisturizing can trap moisture and soften scabs.",
    "Do not pick flakes. Let them release on their own.",
    "Wear loose clothing. Keep tight straps and waistbands off fresh work.",
    "Do not swim while the tattoo is open or peeling. Wait until the skin is fully closed and your artist clears soaking.",
    "Do not put sunscreen on open healing skin. Keep it covered from the sun. Use SPF after it has healed.",
    "Schedule the tattoo after pool-heavy plans, not before them. Pools, hot tubs, lake days, and long walks in direct sun are the Las Vegas issues most likely to disrupt healing.",
    "Sweat, hotel sheets, and travel friction can irritate fresh skin.",
    "",
    "# Ask the artist when",
    "Second skin lifts, leaks, or traps fluid.",
    "The tattoo is rubbed raw by clothing or travel.",
    "You are unsure whether dryness is normal.",
    "You want a healed check before a touch-up.",
    "",
    "# When to contact a clinician",
    "Contact a health care professional if redness spreads instead of improving, pain or swelling gets worse after the first few days, drainage becomes thick or foul-smelling, red streaks appear, or you develop fever or chills. Tattoo artists do not diagnose infections or skin disease.",
    "",
    "# Studio",
    *STUDIO,
    "Guide: https://www.workofarttattoo.com/tattoo-aftercare-desert-climate/",
]

PORTFOLIO = [
    "# What to look at",
    "The photographs stay on the studio site so you can see them large. This sheet is the map to the healed realism portfolio.",
    "Fresh and healed documentation is grouped by style: black and grey, fine line, color, cover-ups, sleeves, and portraits.",
    "Start with healed photos in the style you want, not only fresh shots.",
    "",
    "# Who does this work",
    "Joshua Cole is the studio lead and black-and-grey realism tattoo artist. His work includes portraits, large-scale sleeves, and cover-up and rework projects.",
    "Teralyn is the studio fine-line tattoo artist: floral, script, and small detailed tattoos.",
    "Katelyn Cole is the studio piercer: ear curation and anatomy-first placement.",
    "",
    "# Cover-ups",
    "A cover-up consult looks at the old tattoo and at healed cover-ups in a similar size. The new piece has to be planned around what is already in the skin.",
    "",
    "# Open the portfolio",
    "Healed gallery: https://www.workofarttattoo.com/healed_tattoo_gallery_las_vegas/",
    "Realism guide: https://www.workofarttattoo.com/realism-tattoos-las-vegas/",
    "Cover-ups: https://www.workofarttattoo.com/cover-up-tattoos-las-vegas/",
    "",
    "# Studio",
    *STUDIO,
]

DECISION = [
    "# Before you book",
    "Start with healed photos in your style. Ask how the consult works, whether the artist is licensed, and how they plan for Las Vegas sun on your placement.",
    "Eat a meal, hydrate, sleep, and wear comfortable clothing. Avoid alcohol for 24 hours before. Bring ID. Nevada requires valid ID proving you are 18 or older.",
    "",
    "# Match the work to the artist",
    "Joshua Cole: black and grey realism, portraits, sleeves, and cover-up or rework projects.",
    "Teralyn: fine line, floral, script, and small detailed tattoos.",
    "Katelyn Cole: piercing, ear curation, and jewelry fit.",
    "",
    "# Price and the quote",
    "The studio quotes by project after a consult: size, detail, placement, and how many sessions the piece needs. Ask for a quote instead of expecting one flat menu.",
    "Small pieces have a studio minimum that covers setup, sterile supplies, and artist time.",
    "",
    "# If you are visiting Las Vegas",
    "Read the desert aftercare guide before a trip tattoo. Sun, pools, sweat, and dry air change the heal. The studio is open daily from 12 PM to 12 AM.",
    "Desert aftercare: https://www.workofarttattoo.com/tattoo-aftercare-desert-climate/",
    "How to choose an artist: https://www.workofarttattoo.com/how-to-choose-a-tattoo-artist/",
    "Pricing guide: https://www.workofarttattoo.com/how_much_do_tattoos_cost_in_las_vegas_authority_guide/",
    "Book a consult: https://www.workofarttattoo.com/appointments/",
    "",
    "# Studio",
    *STUDIO,
]


def main() -> int:
    OUT.mkdir(exist_ok=True)
    files = {
        "vegas-desert-aftercare-checklist.pdf": ("Vegas Desert Aftercare Checklist", AFTERCARE),
        "healed-realism-portfolio.pdf": ("Healed Realism Portfolio", PORTFOLIO),
        "first-tattoo-decision-guide.pdf": ("First Tattoo Decision Guide", DECISION),
    }
    for name, (title, blocks) in files.items():
        payload = build_pdf_bytes(title, blocks)
        path = OUT / name
        path.write_bytes(payload)
        if not payload.startswith(b"%PDF-1.4") or b"%%EOF" not in payload:
            raise SystemExit(f"invalid pdf: {name}")
        print(f"[ok] {path.relative_to(ROOT)} ({len(payload)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
