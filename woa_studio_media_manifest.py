#!/usr/bin/env python3
"""Catalog of studio media — Joshua tattoos/art, Katelyn piercing, studio life."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MediaCategory(str, Enum):
    JOSHUA_TATTOO = "joshua-tattoos"
    JOSHUA_TATTOOING = "joshua-tattooing"
    JOSHUA_ART = "joshua-original-art"
    JOSHUA_DESIGNS = "joshua-designs"
    KATELYN_PIERCING = "katelyn-piercing"
    STUDIO_LIFE = "studio-life"
    SKIP = "skip"


@dataclass(frozen=True)
class MediaItem:
    uuid_prefix: str
    stem: str
    category: MediaCategory
    title: str
    alt: str


# UUID prefix (first segment before _) -> metadata
# Flash sheets already live on /flash_art_deals_under_100/ — skip duplicates here.
FLASH_UUIDS = frozenset(
    {
        "659AB1DF", "E67DDAA9", "2081DC55", "6857A6B0", "7945073D", "95AEFAA3",
        "350E170E", "61D5E754", "927E2780", "17BEF5D1", "34626C14", "AF683B2E",
        "87FA191F", "C759FE19", "5E180922", "CC347721",
    }
)

SKIP_UUIDS = frozenset(
    {
        "94DD3E00",  # provocative graphic — not for public studio site
        "972A652D",  # phone lock-screen screenshot with UI overlays
        "CBD56334",  # iPhone contact screenshot — not gallery content
        "5FCDC216",  # client lifestyle Instagram grid — not Joshua tattooing
        "6B3D996F",  # Joshua at art car — not tattooing
        "19458891",  # tattoo montage collage — not a clean at-work shot
        "FCEB1FDB",  # Joshua standing in studio — portrait, not tattooing
        "BD93670A",  # Joshua portrait in tank — not tattooing
    }
)

HEALING_UUIDS = frozenset({"7168E5BE", "187BEB35"})  # on healing before/after page

KNOWN: dict[str, tuple[MediaCategory, str, str]] = {
    # Joshua · tattoos
    "B9702CF5": (MediaCategory.JOSHUA_TATTOO, "Fantasy portrait with lightning", "Black and grey fantasy portrait tattoo with orange energy — Joshua Cole, Work of Art Las Vegas"),
    "13AFB944": (MediaCategory.JOSHUA_TATTOO, "Memorial eagle script", "Healed black and grey memorial eagle tattoo — Joshua Cole, Work of Art Las Vegas"),
    "B66555E2": (MediaCategory.JOSHUA_TATTOO, "Roaring lion with crown of thorns", "Black and grey roaring lion tattoo with thorn crown — Joshua Cole, Work of Art Las Vegas"),
    "A1111068": (MediaCategory.JOSHUA_TATTOO, "Icarus falling angel", "Black and grey Icarus falling angel tattoo — Joshua Cole, Work of Art Las Vegas"),
    "5A41DF51": (MediaCategory.JOSHUA_TATTOO, "Dove in flight", "Black and grey dove realism tattoo on shoulder — Joshua Cole, Work of Art Las Vegas"),
    "4107AB02": (MediaCategory.JOSHUA_TATTOO, "Medusa portrait fresh", "Fresh black and grey Medusa realism forearm tattoo — Joshua Cole, Work of Art Las Vegas"),
    "F28E160A": (MediaCategory.KATELYN_PIERCING, "Triple flat conch lobe ear setup", "Blonde client ear with three flat helix studs, conch barbell and dangling lobe crystal — Joshua Cole, Work of Art Las Vegas"),
    "DD626B1D": (MediaCategory.KATELYN_PIERCING, "Nostril stud on smiling client", "Smiling woman in camo cadet hat with small silver nostril stud and hoop earrings — Joshua Cole, Work of Art Las Vegas"),
    "2455FD61": (MediaCategory.KATELYN_PIERCING, "Matching bilateral earlobe piercings", "Fresh silver ball studs in both earlobes on bearded man, shown in paired profile shots — Joshua Cole, Work of Art Las Vegas"),
    "C6159742": (MediaCategory.KATELYN_PIERCING, "Labret and eyebrow piercing closeup", "Close three-quarter portrait showing silver labret below lip and matching eyebrow stud — Joshua Cole, Work of Art Las Vegas"),
    "C317138A": (MediaCategory.KATELYN_PIERCING, "Flat and conch cartilage studs", "Side profile of smiling woman with new flat helix and conch crystal studs in studio — Joshua Cole, Work of Art Las Vegas"),
    "F1DA8B6F": (MediaCategory.KATELYN_PIERCING, "Conch and lobe piercing smile", "Smiling client showing fresh conch and lobe studs beside colorful butterfly shoulder tattoos — Joshua Cole, Work of Art Las Vegas"),
    # Joshua · original art
    "25BD710F": (MediaCategory.JOSHUA_ART, "Psychedelic chameleon painting", "Original chameleon painting — Joshua Cole fine art, Work of Art Las Vegas"),
    "7E01A1B0": (MediaCategory.JOSHUA_ART, "Grim reaper with violin", "Original grim reaper violin painting on canvas — Joshua Cole, Work of Art Las Vegas"),
    "0E0344C2": (MediaCategory.JOSHUA_TATTOO, "Artist preparing gloves in studio", "Heavily tattooed artist donning pink gloves inside Work of Art flash-lined studio — Joshua Cole, Work of Art Las Vegas"),
    "20D31CAD": (MediaCategory.JOSHUA_TATTOO, "Veiled crowned woman realism tattoo", "Black-grey veiled woman with ornate crown and clasped praying hands on forearm — Joshua Cole, Work of Art Las Vegas"),
    "2EA11860": (MediaCategory.JOSHUA_ART, "Pennywise clown horror illustration", "Color Pennywise portrait with cracked forehead, ruffled collar and Losers Club below — Joshua Cole, Work of Art Las Vegas"),
    "E010665E": (MediaCategory.JOSHUA_TATTOO, "All-seeing eye triangle tattoo", "Realistic eye inside a triangle with swirling smoke ribbons, black-grey forearm piece — Joshua Cole, Work of Art Las Vegas"),
    "BD93670A": (MediaCategory.JOSHUA_TATTOO, "Joshua Cole Work of Art portrait", "Joshua Cole in branded tank top showing neck tattoos and full black-grey arm sleeve — Joshua Cole, Work of Art Las Vegas"),
    # Katelyn · piercing
    "DA19EEC5": (MediaCategory.KATELYN_PIERCING, "Ear lobe piercing session", "Katelyn Cole ear piercing session — Work of Art Las Vegas"),
    "6AB88A11": (MediaCategory.KATELYN_PIERCING, "Piercing setup in studio", "Katelyn Cole preparing sterile piercing setup — Work of Art Las Vegas"),
    "EB7D2939": (MediaCategory.KATELYN_PIERCING, "Ear curation work", "Katelyn Cole ear curation piercing — Work of Art Las Vegas"),
    "C65AAED1": (MediaCategory.KATELYN_PIERCING, "Facial piercing work", "Katelyn Cole facial piercing — Work of Art Las Vegas"),
    "C611F77C": (MediaCategory.KATELYN_PIERCING, "Body piercing work", "Katelyn Cole body piercing — Work of Art Las Vegas"),
    "0F5998BE": (MediaCategory.KATELYN_PIERCING, "Ear piercing healed result", "Healed ear piercing by Katelyn Cole — Work of Art Las Vegas"),
    "86D3F26F": (MediaCategory.KATELYN_PIERCING, "Jewelry upgrade", "Implant-grade jewelry piercing by Katelyn Cole — Work of Art Las Vegas"),
    "B525678D": (MediaCategory.KATELYN_PIERCING, "Piercing session prep", "Katelyn Cole preparing piercing jewelry — Work of Art Las Vegas"),
    "69C261AF": (MediaCategory.KATELYN_PIERCING, "Ear piercing in studio", "Katelyn Cole ear piercing session — Work of Art Las Vegas"),
    # Studio life
    "70837687": (MediaCategory.JOSHUA_TATTOOING, "Tattoo session in progress", "Joshua Cole tattooing at Work of Art Las Vegas studio"),
    "88475D3E": (MediaCategory.KATELYN_PIERCING, "Curated helix tragus lobe piercings", "Ear curated with twin helix crystals, gold tragus hoop and square-cut lobe stud in studio — Joshua Cole, Work of Art Las Vegas"),
    "A704B2D4": (MediaCategory.KATELYN_PIERCING, "Industrial bar and decorative hoop", "Blonde freckled client with silver industrial barbell and decorative lobe hoop earring — Joshua Cole, Work of Art Las Vegas"),
    "FCEB1FDB": (MediaCategory.STUDIO_LIFE, "Joshua Cole in studio", "Joshua Cole — tattoo artist at Work of Art Las Vegas"),
    "1659A367": (MediaCategory.STUDIO_LIFE, "Work of Art studio", "Inside Work of Art Tattoo & Piercing Las Vegas"),
    "DC47F9F3": (MediaCategory.STUDIO_LIFE, "Studio storefront", "Work of Art Tattoo studio — sign up for classes"),
    "3A77750E": (MediaCategory.STUDIO_LIFE, "Studio interior", "Work of Art Tattoo & Piercing studio Las Vegas"),
    "EF852DBB": (MediaCategory.JOSHUA_TATTOO, "Falling winged angel realism tattoo", "Black-grey Icarus-style falling angel with spread feathered wings on leg, fine-line shading — Joshua Cole, Work of Art Las Vegas"),
    "D21A69FF": (MediaCategory.STUDIO_LIFE, "Storefront window and class signup", "Glass storefront cursive of Art lettering looking out to parking lot, sign up for classes — Joshua Cole, Work of Art Las Vegas"),
    # Joshua · completed tattoos (batch 2)
    "618E0BC3": (MediaCategory.JOSHUA_TATTOO, "Norse Odin half sleeve", "Norse Odin half sleeve with orange lightning — black and grey realism by Joshua Cole, Work of Art Las Vegas"),
    "BB2920B5": (MediaCategory.JOSHUA_TATTOO, "All-seeing eye triangle", "Black and grey all-seeing eye in triangle with smoke ribbons — Joshua Cole, Work of Art Las Vegas"),
    "220154A4": (MediaCategory.JOSHUA_TATTOO, "Roaring lion thigh portrait", "Black and grey roaring lion thigh tattoo — Joshua Cole, Work of Art Las Vegas"),
    "1BC3CC09": (MediaCategory.JOSHUA_TATTOO, "Norse full sleeve narrative", "Full Norse sleeve — Odin portrait, longship, and runes with orange highlights — Joshua Cole, Work of Art Las Vegas"),
    # Joshua · designs & concepts available to book
    "07F7A393": (MediaCategory.JOSHUA_DESIGNS, "Grim reaper with lantern", "Grim reaper with purple cloak and glowing lantern — custom design by Joshua Cole, available to book"),
    "40306E95": (MediaCategory.JOSHUA_DESIGNS, "Gothic skull & portrait", "Gothic skull and feminine portrait in ornate frame — Joshua Cole custom design, available to book"),
    "86C8EB99": (MediaCategory.JOSHUA_DESIGNS, "Skull with lens flare", "High-contrast skull illustration with graphic lens flare — Joshua Cole custom design, available to book"),
    "261CC990": (MediaCategory.JOSHUA_DESIGNS, "Reaper chess battlefield", "Grim reaper over chessboard and war scene — inspired custom concept Joshua Cole can tattoo"),
    "5C84D45C": (MediaCategory.JOSHUA_DESIGNS, "Horror rabbit concept", "Dark illustrative horror rabbit — inspired custom concept Joshua Cole can adapt for your placement"),
    "FC0D74FD": (MediaCategory.JOSHUA_DESIGNS, "Illustrative character concept", "High-contrast illustrative character design — inspired custom concept Joshua Cole can adapt"),
    "C6B7E1DE": (MediaCategory.JOSHUA_DESIGNS, "Gothic portrait with skull", "Gothic portrait holding skull in cathedral frame — inspired custom concept Joshua Cole can adapt"),
    # Joshua · completed tattoos (batch 3)
    "5BAED596": (MediaCategory.JOSHUA_TATTOO, "Realistic lipstick kiss mark", "Color realism lipstick kiss mark tattoo — Joshua Cole, Work of Art Las Vegas"),
    "0E676D8C": (MediaCategory.JOSHUA_TATTOO, "Lipstick kiss mark session", "Fresh lipstick kiss mark tattoo in studio — Joshua Cole, Work of Art Las Vegas"),
    "7AE96710": (MediaCategory.JOSHUA_TATTOO, "The Crow portrait tattoo", "Eric Draven Crow tattoo with gothic quote — black and grey illustrative work by Joshua Cole, Work of Art Las Vegas"),
    "20765B48": (MediaCategory.JOSHUA_TATTOO, "The Crow stained-glass frame", "The Crow Eric Draven in circular rain frame — Joshua Cole, Work of Art Las Vegas"),
    "FD5B8CD8": (MediaCategory.JOSHUA_TATTOO, "Three-eyed demon forearm", "Illustrative three-eyed demon with lyric text — black, grey, and red by Joshua Cole, Work of Art Las Vegas"),
    "C0D80F61": (MediaCategory.JOSHUA_TATTOO, "Demon piece in progress", "Illustrative demon tattoo session detail — Joshua Cole, Work of Art Las Vegas"),
    "C19414BD": (MediaCategory.JOSHUA_TATTOO, "Demon tattoo white highlights", "White ink detailing on illustrative demon tattoo — Joshua Cole, Work of Art Las Vegas"),
    "67F63F8A": (MediaCategory.JOSHUA_TATTOOING, "Joshua tattooing lyric piece", "Joshua Cole tattooing illustrative demon and text piece — Work of Art Las Vegas studio"),
    "F39790C4": (MediaCategory.JOSHUA_TATTOOING, "Studio session in progress", "Joshua Cole at work on custom illustrative tattoo — Work of Art Las Vegas"),
    "07AAD378": (MediaCategory.KATELYN_PIERCING, "Septum piercing session in studio", "Curly-haired client smiling after septum ring as piercer needles the columella below — Joshua Cole, Work of Art Las Vegas"),

    "12A42385": (MediaCategory.STUDIO_LIFE, "Guest viewing studio portrait gallery", "Guest admiring framed portrait art in the Work of Art studio gallery. — Joshua Cole, Work of Art Las Vegas"),

    "13B96E0D": (MediaCategory.JOSHUA_TATTOO, "Mushroom ghost blossom foot tattoos", "Whimsical mushroom, ghost, and cherry blossom fine-line foot tattoos. — Joshua Cole, Work of Art Las Vegas"),

    "1416BC55": (MediaCategory.JOSHUA_TATTOO, "Fuck luck all-seeing bicep", "Realistic all-seeing eye with FUCK LUCK banner on outer bicep. — Joshua Cole, Work of Art Las Vegas"),

    "1473AB08": (MediaCategory.JOSHUA_TATTOO, "Ornate cross realistic eye forearm", "Beveled ornate cross above a realistic eye on outer forearm. — Joshua Cole, Work of Art Las Vegas"),

    "19458891": (MediaCategory.STUDIO_LIFE, "Tattoo montage spider script pieces", "Collage of script, spider, ant, geometric and thorn tattoos plus Joshua tattooing a client — Joshua Cole, Work of Art Las Vegas"),

    "195A396A": (MediaCategory.JOSHUA_TATTOO, "Beauty script roses inner forearm", "Cursive Beauty script with crossed rose stems on inner forearm. — Joshua Cole, Work of Art Las Vegas"),

    "29096302": (MediaCategory.JOSHUA_TATTOO, "Norse Odin Viking ship sleeve", "Norse Odin portrait sleeve with Viking ship and red lightning bolts. — Joshua Cole, Work of Art Las Vegas"),

    "2C77C6C3": (MediaCategory.JOSHUA_TATTOO, "Black grey bondage portrait tattoo", "Realistic blindfolded woman with collar, chain and wrist shackles in black-grey ink — Joshua Cole, Work of Art Las Vegas"),

    "2E41FC98": (MediaCategory.KATELYN_PIERCING, "Fresh upper cartilage industrial bar", "Silver industrial barbell through upper helix cartilage on short-haired client ear — Joshua Cole, Work of Art Las Vegas"),

    "31AE60E1": (MediaCategory.JOSHUA_TATTOO, "Archangel wings shoulder blade tattoo", "Detailed black and grey armored archangel with feathered wings on shoulder blade. — Joshua Cole, Work of Art Las Vegas"),

    "34A5278A": (MediaCategory.KATELYN_PIERCING, "Color Superman temple with smoke", "Color Superman S shield with smoke accents on left temple near eyebrow. — Joshua Cole, Work of Art Las Vegas"),

    "3D49B9F9": (MediaCategory.JOSHUA_TATTOO, "Egyptian goddess neck portrait tattoo", "Black-grey Egyptian woman with scarab headdress and Eye of Horus mark on neck — Joshua Cole, Work of Art Las Vegas"),

    "3D695F6F": (MediaCategory.JOSHUA_ART, "Framed dreadlocked singer portrait art", "Framed color drawing of blonde dreadlocked singer screaming into a mic with smoke swirl — Joshua Cole, Work of Art Las Vegas"),

    "3F1329CC": (MediaCategory.KATELYN_PIERCING, "Client portrait with septum piercings", "Smiling client with magenta curls, septum ring, nostril stud and cheek piercings — Joshua Cole, Work of Art Las Vegas"),

    "4052A62B": (MediaCategory.JOSHUA_TATTOO, "Odin mechanical eye lightning tattoo", "Odin portrait with gem helmet, gear monocle and lightning bolts wrapping shoulder and arm — Joshua Cole, Work of Art Las Vegas"),

    "41F7CFA2": (MediaCategory.STUDIO_LIFE, "Studio group celebration with clients", "Collage of smiling women posing before flash-covered walls holding small blue gift bags — Joshua Cole, Work of Art Las Vegas"),

    "422C6A76": (MediaCategory.JOSHUA_TATTOO, "Hourglass luck gun arm sleeve", "Hourglass with money bags, eye, and smoking pistol sleeve on upper arm. — Joshua Cole, Work of Art Las Vegas"),

    "51D91C9F": (MediaCategory.JOSHUA_TATTOO, "Veiled crowned woman shoulder tattoo", "Black-grey veiled woman with ornate crown clutching fabric on upper arm, halo backdrop — Joshua Cole, Work of Art Las Vegas"),

    "55A4538D": (MediaCategory.JOSHUA_TATTOOING, "Joshua Cole fine-line ankle work", "Joshua Cole applying a fine-line ankle tattoo with a rotary machine. — Joshua Cole, Work of Art Las Vegas"),

    "5BC3D948": (MediaCategory.JOSHUA_TATTOO, "Cross eye skull forearm stack", "Ornate cross, realistic eye, and skull stacked down outer forearm. — Joshua Cole, Work of Art Las Vegas"),

    "5FCDC216": (MediaCategory.STUDIO_LIFE, "Client tattoo lifestyle Instagram grid", "Fifteen-panel grid of tattooed model at clubs, beach, studio and Vegas neon signs — Joshua Cole, Work of Art Las Vegas"),

    "609EC82D": (MediaCategory.JOSHUA_TATTOO, "Color realism gold grillz portrait", "Color realism portrait of face-tattooed man revealing gold grillz artwork. — Joshua Cole, Work of Art Las Vegas"),

    "6416E41F": (MediaCategory.STUDIO_LIFE, "Studio tattoo style grid collage", "Studio grid collage showing color, blackwork, and realism tattoo samples. — Joshua Cole, Work of Art Las Vegas"),

    "6AD610B8": (MediaCategory.JOSHUA_TATTOO, "Cross eye skull brown skin", "Black and grey cross, eye, and skull forearm tattoo on brown skin. — Joshua Cole, Work of Art Las Vegas"),

    "6B3D996F": (MediaCategory.STUDIO_LIFE, "Joshua Cole at Vegas art installation", "Joshua Cole at a fire-breathing octopus art car with Vegas skyline behind — Joshua Cole, Work of Art Las Vegas"),

    "76A60A87": (MediaCategory.JOSHUA_TATTOO, "Cross eye skull forearm piece", "Vertical forearm piece with ornate cross, detailed eye, and skull below. — Joshua Cole, Work of Art Las Vegas"),

    "7AC4181A": (MediaCategory.JOSHUA_TATTOOING, "Joshua Cole tattooing client forearm", "Joshua Cole tattooing a client's forearm with focused detail in the studio. — Joshua Cole, Work of Art Las Vegas"),

    "7D759759": (MediaCategory.KATELYN_PIERCING, "Curated facial piercing jewelry display", "Bridge, septum, nostril, philtrum and cheek piercings with silver jewelry — Joshua Cole, Work of Art Las Vegas"),

    "7EA2AF20": (MediaCategory.JOSHUA_TATTOO, "Fine-line howling werewolf ankle", "Fine-line howling werewolf outline tattooed above the ankle on lower leg. — Joshua Cole, Work of Art Las Vegas"),

    "83BE4284": (MediaCategory.JOSHUA_TATTOOING, "Joshua Cole geometric forearm stencil", "Joshua Cole inking a geometric star stencil on a client's forearm. — Joshua Cole, Work of Art Las Vegas"),

    "8EE69C62": (MediaCategory.JOSHUA_TATTOO, "Red rose Alexis name tattoo", "Color realism red rose with soft green halo and cursive Alexis script on inner forearm — Joshua Cole, Work of Art Las Vegas"),

    "90BCE5F7": (MediaCategory.JOSHUA_TATTOO, "All-seeing eye luck forearm", "Black and grey all-seeing eye with FUCK LUCK banner and money bags on forearm. — Joshua Cole, Work of Art Las Vegas"),

    "98200338": (MediaCategory.JOSHUA_TATTOO, "Smoky eye and skull forearm", "Smoky black and grey eye above skull realism on outer forearm. — Joshua Cole, Work of Art Las Vegas"),

    "A1784097": (MediaCategory.JOSHUA_ART, "Black and grey rose tattoo design", "Detailed stipple-shaded blooming rose with thorned stem, black-grey tattoo flash — Joshua Cole, Work of Art Las Vegas"),

    "AEEFD89F": (MediaCategory.JOSHUA_TATTOO, "Shaded skull forearm close-up", "Three-quarter black and grey skull with smoky shading on forearm. — Joshua Cole, Work of Art Las Vegas"),

    "B09080B0": (MediaCategory.KATELYN_PIERCING, "Spiked septum and chest ornament", "Spiked septum horseshoe with nose chain and symmetrical black chest filigree tattoo — Joshua Cole, Work of Art Las Vegas"),

    "BAB7C7FA": (MediaCategory.JOSHUA_TATTOO, "Small temple and cheek tattoos", "Side profile showing small fine-line temple and cheek tattoos on a man's face. — Joshua Cole, Work of Art Las Vegas"),

    "BD7EB0D3": (MediaCategory.JOSHUA_TATTOO, "Superman shield left temple tattoo", "Red and black Superman S shield tattoo on a man's left temple. — Joshua Cole, Work of Art Las Vegas"),

    "BF61B780": (MediaCategory.JOSHUA_TATTOO, "Armored archangel wings sword back", "Black and grey armored archangel with wings and sword on upper back. — Joshua Cole, Work of Art Las Vegas"),

    "C7F1842E": (MediaCategory.JOSHUA_TATTOO, "Skull and eye forearm realism", "Black and grey realistic skull stacked beneath a detailed eye on the forearm. — Joshua Cole, Work of Art Las Vegas"),

    "CBD56334": (MediaCategory.STUDIO_LIFE, "Studio contact phone number screenshot", "iPhone contact screen listing studio line +1 (725) 246-5283 under unknown caller — Joshua Cole, Work of Art Las Vegas"),

    "D4475940": (MediaCategory.JOSHUA_TATTOO, "Realistic eye skull forearm", "Realistic human eye above a shaded skull on medium-tone forearm. — Joshua Cole, Work of Art Las Vegas"),

    "E483138E": (MediaCategory.JOSHUA_TATTOO, "Black grey temple rose tattoo", "Soft-shaded black-grey rose tattoo on temple beside a small outline heart on cheek — Joshua Cole, Work of Art Las Vegas"),

    "ED94E39A": (MediaCategory.JOSHUA_TATTOO, "Cross eye skull darker skin", "Full forearm cross, eye, and skull sleeve on darker skin tone. — Joshua Cole, Work of Art Las Vegas"),

    "EE57F2A6": (MediaCategory.JOSHUA_TATTOO, "Fine-line ankle tattoos trio", "Three clients display fine-line ankle tattoos of a figure, pin, and star. — Joshua Cole, Work of Art Las Vegas"),

    "F002F0C4": (MediaCategory.KATELYN_PIERCING, "Helix and starburst lobe piercings", "Fresh helix stud and gold starburst lobe earring shown on two separate client ears — Joshua Cole, Work of Art Las Vegas"),

    "F4DDBBB2": (MediaCategory.JOSHUA_TATTOO, "Valkyrie winged helmet upper arm", "Profile Valkyrie in winged helmet with cheek runes on upper arm. — Joshua Cole, Work of Art Las Vegas"),

    "F76AEEF5": (MediaCategory.JOSHUA_TATTOOING, "Joshua Cole head tattoo session", "Joshua Cole carefully tattooing a client's temple during a head tattoo session. — Joshua Cole, Work of Art Las Vegas"),

    "FE20F013": (MediaCategory.JOSHUA_TATTOO, "Black and grey rapper calf portraits", "Matching black-grey calf portraits of Lil Peep and a tongue-out rock singer with neck rose — Joshua Cole, Work of Art Las Vegas"),

}


def slugify(text: str) -> str:
    keep = "".join(c if c.isalnum() else "-" for c in text.lower())
    while "--" in keep:
        keep = keep.replace("--", "-")
    return keep.strip("-")[:60] or "studio-photo"


def classify(uuid_prefix: str, index: int) -> MediaItem:
    if uuid_prefix in SKIP_UUIDS or uuid_prefix in FLASH_UUIDS or uuid_prefix in HEALING_UUIDS:
        cat = MediaCategory.SKIP
        title = "skipped"
        alt = ""
    elif uuid_prefix in KNOWN:
        cat, title, alt = KNOWN[uuid_prefix]
    else:
        raise ValueError(
            f"Missing alt catalog entry for {uuid_prefix} — run catalog_media_alts.py / apply_media_alt_catalog.py"
        )
    stem = f"{slugify(title)}-{uuid_prefix[:8].lower()}"
    return MediaItem(uuid_prefix=uuid_prefix, stem=stem, category=cat, title=title, alt=alt)


def all_user_uuid_prefixes() -> list[str]:
    """91 UUID prefixes from the user's uploaded batch."""
    return [
        "BF61B780", "BAB7C7FA", "90BCE5F7", "C7F1842E", "422C6A76", "7AC4181A", "7EA2AF20",
        "31AE60E1", "195A396A", "5BC3D948", "F76AEEF5", "BD7EB0D3", "1416BC55", "EE57F2A6",
        "76A60A87", "6AD610B8", "34A5278A", "D4475940", "55A4538D", "AEEFD89F", "ED94E39A",
        "1473AB08", "83BE4284", "98200338", "13B96E0D", "69C261AF", "12A42385", "29096302",
        "6416E41F", "609EC82D", "F4DDBBB2", "7D759759", "6B3D996F", "FE20F013", "3F1329CC",
        "CBD56334", "3D49B9F9", "A1784097", "BD93670A", "972A652D", "7168E5BE", "0E0344C2",
        "20D31CAD", "187BEB35", "2EA11860", "E010665E", "2C77C6C3", "8EE69C62", "E483138E",
        "F002F0C4", "19458891", "07AAD378", "B09080B0", "3D695F6F", "2E41FC98", "41F7CFA2",
        "5FCDC216", "F1DA8B6F", "C317138A", "C6159742", "DD626B1D", "2455FD61", "F28E160A",
        "A704B2D4", "88475D3E", "7E01A1B0", "FCEB1FDB", "1659A367", "EB7D2939", "6AB88A11",
        "C65AAED1", "C611F77C", "0F5998BE", "86D3F26F", "51D91C9F", "4052A62B", "DC47F9F3",
        "3A77750E", "EF852DBB", "D21A69FF", "94DD3E00", "B525678D", "4107AB02", "70837687",
        "25BD710F",         "B9702CF5", "13AFB944", "B66555E2", "A1111068", "5A41DF51", "DA19EEC5",
    ]


def batch2_uuid_prefixes() -> list[str]:
    """Completed tattoos + design concepts (second user upload)."""
    return [
        "618E0BC3",
        "BB2920B5",
        "220154A4",
        "1BC3CC09",
        "07F7A393",
        "261CC990",
        "5C84D45C",
        "40306E95",
        "FC0D74FD",
        "C6B7E1DE",
        "86C8EB99",
    ]


def batch3_uuid_prefixes() -> list[str]:
    """Completed tattoos (third user upload)."""
    return [
        "5BAED596",
        "7AE96710",
        "0E676D8C",
        "FD5B8CD8",
        "C0D80F61",
        "20765B48",
        "67F63F8A",
        "F39790C4",
        "C19414BD",
    ]


def all_manifest_uuid_prefixes() -> list[str]:
    return all_user_uuid_prefixes() + batch2_uuid_prefixes() + batch3_uuid_prefixes()


def manifest_items() -> list[MediaItem]:
    seen: set[str] = set()
    out: list[MediaItem] = []
    for i, prefix in enumerate(all_manifest_uuid_prefixes(), 1):
        if prefix in seen:
            continue
        seen.add(prefix)
        item = classify(prefix, i)
        if item.category != MediaCategory.SKIP:
            out.append(item)
    return out


def items_by_category() -> dict[MediaCategory, list[MediaItem]]:
    buckets: dict[MediaCategory, list[MediaItem]] = {c: [] for c in MediaCategory if c != MediaCategory.SKIP}
    for item in manifest_items():
        buckets[item.category].append(item)
    return buckets
