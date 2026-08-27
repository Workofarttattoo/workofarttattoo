#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "artists_build" / "katelyn-cole.html",
    ROOT / "artists_raw" / "katelyn-cole.html",
]

REPL = {
    '"jobTitle": "Master Body Piercer"': '"jobTitle": "Professional Piercer"',
    '"jobTitle":"Master Body Piercer"': '"jobTitle":"Professional Piercer"',
    '"email": "booking@workofarttattoo.com"': '"email": "kmorgen14@gmail.com"',
    '"email":"booking@workofarttattoo.com"': '"email":"kmorgen14@gmail.com"',
    'Master Body Piercer': 'Professional Piercer',
    'Master Piercer': 'Professional Piercer',
    'Master Piercing': 'Professional Piercing',
}

for path in PATHS:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    old = text
    for a, b in REPL.items():
        text = text.replace(a, b)
    # Katelyn-specific direct email; preserve generic shop email elsewhere.
    text = text.replace('mailto:booking@workofarttattoo.com', 'mailto:kmorgen14@gmail.com')
    if text != old:
        path.write_text(text, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
