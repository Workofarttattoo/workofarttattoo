# Video catalog pipeline

Instagram blocks anonymous bulk scraping of reel feeds. This repo merges **every clip already linked or embedded in site HTML**, optional **manual reels**, and optionally **Instagram Graph** `me/media` when a token is provided.

## 1. Refresh `videos_catalog_merged.json`

```bash
python3 refresh_videos_catalog.py
```

**Reels not referenced in HTML yet:** copy `instagram_reels_inventory.example.json` to `instagram_reels_inventory.json` in the same folder and add `items` with `kind`, `media_id` (shortcode), `title`, `blurb`.

**Optional API:** token must be allowed to call `graph.instagram.com/me/media`.

```bash
export INSTAGRAM_ACCESS_TOKEN='YOUR_TOKEN'
python3 refresh_videos_catalog.py --fetch-api
```

## 2. Regenerate pages

```bash
python3 build_studio_videos_page.py
python3 inject_client_videos.py
python3 inject_page_spotlights.py
```

- `/studio_videos/` lists the full merged catalog.
- `inject_page_spotlights.py` places one deterministic “studio clip” block before `<footer` on guides, appointments, etc. Home, hub pages with dense embeds, and `studio_videos` are skipped.
