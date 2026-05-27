# Curated studio videos

Only clips in `SITE_VIDEO_ALLOWLIST` (`client_videos.py`) are embedded on the site, listed on `/studio_videos/`, or used as guide-page spotlights.

## Kept (9 clips)

| ID | Use |
|----|-----|
| `DDiX988y0tR` | Joshua professional interview (hero) |
| `DTZRprYgQ3G` | Client interview (logo poster → Instagram) |
| `C8vPwacP1du` | Joshua painting in studio |
| `Cpp18lXgU3P` | Joshua seminars / advanced training |
| `C78fY1quCVF` | Katelyn piercing in studio (homepage piercing block) |
| `C0nNwUkRHz6` | Jewelry & placement |
| `C4fOsY7OSTq` | Ear curation |
| `C3GjVCdLUQ9` | Piercing session |
| `Cs1_Oc4gEx1` | Minor ear piercing (minors section) |

Homepage **Studio reels** band uses portfolio stills for tattoo highlights plus `C8vPwacP1du` (Joshua painting reel).

## Removed from site (not polished / wrong thumbnails)

| ID | Reason |
|----|--------|
| `DXfX3r-DQSP` | Weak embed / off-brand preview |
| `DEgSKaryfPz` | Weak embed / off-brand preview |
| `DB1scTAy9Zz` | Weak embed / off-brand preview |
| `DXSZTKZyt2l` | Generic studio reel — not in curated set |
| `DQ1Sv4oEfLG` | Phone-filmed, less polished |
| 12× older Katelyn reels | Redundant with the four kept piercing clips |

## Add a new approved reel

1. Add the shortcode to `SITE_VIDEO_ALLOWLIST` in `client_videos.py`.
2. Add metadata to `CLIENT_VIDEOS`, `KATELYN_VIDEOS`, or `instagram_reels_inventory.json` as needed.
3. Run:

```bash
python3 refresh_videos_catalog.py
python3 build_studio_videos_page.py
python3 inject_client_videos.py
python3 inject_page_spotlights.py
```
