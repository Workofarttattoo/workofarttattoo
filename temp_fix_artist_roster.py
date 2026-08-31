import re
from pathlib import Path

file_path = Path("fix_artist_roster_copy.py")
content = file_path.read_text(encoding="utf-8")

# Define the new, corrected REPLACEMENTS block
new_replacements_block = r"""REPLACEMENTS: list[tuple[str, str]] = [
    (
        "<h4 class=\"text-secondary font-headline-md\">15+</h4>\n"
        "<p class=\"text-on-surface-variant font-label-caps text-[10px] uppercase tracking-widest\">Master Artists</p>",
        "<h4 class=\"text-secondary font-headline-md\">3</h4>\n"
        "<p class=\"text-on-surface-variant font-label-caps text-[10px] uppercase tracking-widest\">Resident Artists</p>",
    ),
    (
        "<h4 class=\"text-secondary font-headline-md\">50k+</h4>\n"
        "<p class=\"text-on-surface-variant font-label-caps text-[10px] uppercase tracking-widest\">Hours Inked</p>",
        "<h4 class=\"text-secondary font-headline-md\">7+</h4>\n"
        "<p class=\"text-on-surface-variant font-label-caps text-[10px] uppercase tracking-widest\">Artists Mentored</p>",
    ),
    (
        "Joshua Cole is widely recognized as the premier black and grey realism master in the valley, specializing in hyper-realistic portraits and intricate custom sleeves at our studio.",
        "Joshua Cole specializes in black and grey realism in Las Vegas — portraits, sleeves, and cover-ups. See healed portfolio photos before you book, not just fresh session shots.",
    ),
    (
        "Hospital-grade sterilization and single-use equipment are our baseline. We maintain the cleanest environment in Las Vegas.",
        "Hospital-grade sterilization and single-use equipment are our baseline. We document our cleaning routine every session — ask us to walk you through it when you visit.",
    ),
    (
        "<h4 class=\"font-headline-md text-headline-md text-on-surface\">15+ Years Experience</h4>",
        "<h4 class=\"font-headline-md text-headline-md text-on-surface\">20+ Years Experience</h4>",
    ),
    ("<p class=\"font-body-md\">4 Artists Available</p>", "<p class=\"font-body-md\">3 In-Studio Artists</p>"),
    ("<p class=\"font-body-md\">2 Tattoo · 1 Piercing</p>", "<p class=\"font-body-md\">3 In-Studio Artists</p>"),
    (
        "AWARD-WINNING RESIDENT ARTISTS",
        "THREE RESIDENT ARTISTS",
    ),
    (
        "A professional studio is a collective of resident artists with decades of combined experience. These are professionals who have spent years mastering specific styles—Realism, Traditional, Neo-Traditional, or Fine Line.",
        "A professional studio keeps a focused resident roster — not a rotating wall of names. Work of Art has three in-studio artists: Joshua Cole (tattoo & piercing; studio lead who trains the team), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer).",
    ),
    (
        "A professional studio keeps a focused resident roster — not a rotating wall of names. Work of Art has three in-studio artists: two tattoo artists (Joshua Cole and Teralyn) and professional piercer Katelyn Cole, each with a clear specialty.",
        "A professional studio keeps a focused resident roster — not a rotating wall of names. Work of Art has three in-studio artists: Joshua Cole (tattoo & piercing; studio lead who trains the team), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer).",
    ),
    (
        "At Work of Art, our collective is comprised of classically trained painters and illustrators. We believe that the ability to create original work on a canvas is the ultimate prerequisite for creating a masterpiece on the skin.",
        "At Work of Art, our small resident team is built on fine-art discipline and specialization, not volume. Joshua Cole offers tattoo and piercing and trains resident artists and alumni; Katelyn Cole leads piercing. Seven alumni trained here now run their own shops or travel as guest artists.",
    ),
    ("See the fine art roots of our master artists.", "Meet our three resident artists and their specialties."),
    ("Consult with our award-winning artists today", "Consult with our resident artists today"),
    ("Mark Thorne", "Joshua Cole"),
    ("Lead Artist &amp; Founder", "Lead Tattoo Artist — Black &amp; Grey Realism"),
    ("Followed Mark's desert healing guide", "Followed Work of Art's desert healing guide"),
    ("Artist: Thorne", "Artist: Joshua Cole"),
    ("Artist: Elara", "Artist: Teralyn"),
    ("Piercing &amp; Fine Line", "Professional Piercer"),
    ("Piercing & Fine Line", "Professional Piercer"),
    ("Katelyn Cole — Piercing &amp; Fine Line", "Katelyn Cole — Professional Piercer"),
    ("Katelyn Cole — Piercing & Fine Line", "Katelyn Cole — Professional Piercer"),
    (
        "Joshua Cole, Katelyn Cole, and Jay Jay — the resident masters behind every piece at Work of Art Tattoo &amp; Piercing.",
        f"{{STUDIO_ROSTER_BLURB}} {{STUDIO_ROSTER_LEGACY}}",
    ),
    (
        "Joshua Cole and Jay Jay tattoo in-studio; Katelyn Cole is our professional piercer. Seven artists trained at Work of Art now own shops or travel as guest artists — we're proud of that legacy without pretending we have a dozen chairs filled today.",
        f"{{STUDIO_ROSTER_BLURB}} {{STUDIO_ROSTER_LEGACY}}",
    ),
    ("New Artist Coming Soon", ""),
    ("NEW ARTIST COMING SOON", ""),
    ("New artist coming soon", ""),
    (
        "Joshua Cole, Katelyn Cole, and Jay Jay — the resident masters at Work of Art Tattoo &amp; Piercing, Las Vegas.",
        f"{{STUDIO_ROSTER_BLURB}} {{STUDIO_ROSTER_LEGACY}}",
    ),
    (
        "Joshua Cole and Jay Jay (tattoo) and Katelyn Cole (piercing) — our three in-studio residents. Seven alumni trained here now lead their own studios or travel as guest artists.",
        f"{{STUDIO_ROSTER_BLURB}} {{STUDIO_ROSTER_LEGACY}}",
    ),
    (
        "two tattooists (Joshua Cole and Jay Jay) and professional piercer Katelyn Cole",
        "two tattoo artists (Joshua Cole and Teralyn) and professional piercer Katelyn Cole",
    ),
    (
        "Joshua Cole and Jay Jay lead tattoo work; Katelyn Cole leads piercing.",
        "Joshua Cole offers tattoo and piercing and trains the team; Katelyn Cole leads piercing.",
    ),
    (
        "Joshua Cole and Jay Jay tattoo in-studio; Katelyn Cole is our professional piercer.",
        "Joshua Cole (tattoo & piercing; studio lead), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer).",
    ),
    (
        "2 tattoo artists and 1 professional piercer",
        "Joshua Cole (tattoo & piercing; trains the team), Katelyn Cole (piercing), and Teralyn (tattoo artist and piercer)",
    ),
    (
        "Tattoo services only — piercing is handled by Katelyn Cole.",
        "Master tattoo & piercing artist; studio founder who trains resident artists and alumni across Las Vegas.",
    ),
    (
        "Lead Tattoo Artist",
        "Master Artist — Tattoo &amp; Piercing",
    ),
    (
        "Lead Tattoo Artist — Black &amp; Grey Realism",
        "Master Artist — Tattoo, Piercing &amp; Training",
    ),
    (
        "Tattoo work at the studio is handled by Joshua Cole and Jay Jay.",
        "Tattoo work with Joshua Cole and Teralyn; Joshua trained the in-studio team in piercing fundamentals.",
    ),
    (
        "Every tattoo at Work of Art is a collaboration with one of our two in-studio tattoo artists — Joshua Cole or Jay Jay — backed by a professional piercer, Katelyn Cole.",
        "Work of Art is led by Joshua Cole (tattoo, piercing, and artist training), Katelyn Cole as professional piercer, and Teralyn for fineline floral, script, custom drawings by commission, and high-detail small tattoos. Three residents today; seven alumni we trained now run their own shops or travel as guests.",
    ),
    (
        "Three in-studio residents — Joshua Cole and Jay Jay (tattoo), Katelyn Cole (piercing)",
        "Three in-studio residents — Joshua Cole (tattoo and piercing, studio lead), Katelyn Cole (piercing), and Teralyn (tattoo artist and piercer; fineline floral, script, commissioned custom drawings)",
    ),
]"""

# Find the start and end of the REPLACEMENTS list
# I'll use regex to be more robust against minor formatting differences
replacements_start_re = re.compile(r"REPLACEMENTS: list\[tuple\[str, str\]\] = \[.*?\[", re.DOTALL)
replacements_end_re = re.compile(r"\]\n\nMARCUS_SIDEBAR = re.compile\(", re.DOTALL)

start_match = replacements_start_re.search(content)
end_match = replacements_end_re.search(content)

if start_match and end_match:
    # Extract the content before and after the REPLACEMENTS block
    before_replacements = content[:start_match.start()]
    after_replacements = content[end_match.start():]

    # Reconstruct the file content with the new_replacements_block
    new_content = before_replacements + new_replacements_block + after_replacements
    file_path.write_text(new_content, encoding="utf-8")
    print("Successfully updated fix_artist_roster_copy.py")
else:
    print("Could not find REPLACEMENTS block in fix_artist_roster_copy.py")