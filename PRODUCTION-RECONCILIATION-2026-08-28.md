# Production Reconciliation — 2026-08-28

## Hosting model

Production is **GitHub Pages only**:

- Site content lives in this repo and publishes through `gh-pages`
- Custom domain is `www.workofarttattoo.com`
- Bluehost is not part of the live hosting/FTP path anymore

## Status after deploy-proof branch

This branch makes `main` deployable to GitHub Pages again and restores the broken production routes that navigation already advertised.

## Confirmed before this fix

- Live custom domain was serving `gh-pages`, but deploy-from-`main` was failing repeatedly.
- Failure cause: workflow required `cover-up-tattoos-las-vegas/index.html`, which existed neither on `main` nor on current `gh-pages`.
- Live `/merchandise/` was 404 while nav linked to it.
- Live `/privacy-policy/` was 404 while footer linked to it.
- Live cover-up URL in active nav/sitemap was the underscore route and returned 200.
- Open PRs `#7` and `#8` are **not** clean cherry-picks onto current `main` (many conflicts). Do not merge wholesale.
- `seo/master-authority-rebuild` is substantially ahead/behind and must be mined for specific pages only.

## What this branch restores under source control

- Clean cover-up route: `cover-up-tattoos-las-vegas/` (from reviewed SEO rebuild content)
- Merchandise route with **local** catalog images (not dead `/wp-content/` URLs)
- Teralyn artist page + build output
- Privacy policy page
- Deploy workflow that preserves live-only Pages content, overlays reviewed source, and verifies critical routes including Merchandise, Privacy, Cover-Up, and Teralyn

## Divergent branch policy (unchanged)

Do **not** merge old divergent branches wholesale.

- `jules-5081671558969232321-bdcd14dd` / PR `#8`: conflict-heavy; sleeve/Katelyn work already largely harvested.
- `optimize-conversion-and-trust-v2-...` / PR `#7`: stale and conflict-heavy.
- `seo/master-authority-rebuild`: salvage pages/assets only after review.
- `gh-pages`: deployment output, not source of truth.

## Release rule

Deploy is successful only when:

1. GitHub Actions publish to `gh-pages` succeeds
2. `DEPLOYED_MAIN_SHA` on the custom domain matches the merged `main` commit
3. Critical routes return 200 with expected content markers
