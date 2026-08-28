# Production Reconciliation — 2026-08-28

Branch: `reconcile-production-20260828`

## Goal

Make GitHub source, `gh-pages`, and the active Work of Art website agree without destroying valid live-only work.

## Confirmed live and must be preserved

- `/cover-up-tattoos-las-vegas/` — clean-route cover-up page is live and contains the newer Joshua Cole cover-up/rework content.
- `/artists/katelyn-cole/` — live Katelyn page uses `Professional Piercer` and the current portfolio structure.
- `/dermis_skin_science_las_vegas_authority_guide/` — live skin-science route exists even though this content originated in the divergent SEO rebuild work.

## Confirmed source/deployment mismatch

- `main` does not currently contain `cover-up-tattoos-las-vegas/code.html` even though the clean route is live.
- The older underscore route `cover_up_tattoos_las_vegas_master_authority_guide/` still exists and should not be allowed to replace the clean route.
- `gh-pages` contains generated `index.html` files and production-only material that is not represented one-for-one on `main`.
- Therefore production deployment must remain an overlay/preserve operation, not a destructive mirror of `main`.

## Merchandise repair

The active navigation links to `/merchandise/`, but that route is broken on production.

Reconciliation branch now restores:

- `merchandise/code.html`
- `woa_merchandise_manifest.py`

The restored page uses the legacy Work of Art art-catalog images and routes inquiries to the studio booking email. The production build will convert `merchandise/code.html` to `merchandise/index.html`.

The GitHub Pages deployment workflow has also been corrected: it no longer strips Merchandise links. Instead, it requires `merchandise/index.html`, checks for expected merchandise/original-art content, verifies the route on `gh-pages`, and verifies `/merchandise/` on the active custom domain after Pages propagation.

## Current deployment guardrails

The reviewed workflow on this reconciliation branch now:

1. Builds `index.html` from source `code.html` pages.
2. Uses reviewed Joshua and Katelyn artist build outputs.
3. Preserves production-only files from the existing `gh-pages` tree and overlays reviewed source without `--delete`.
4. Requires homepage, appointments, Joshua, Katelyn, clean cover-up, Merchandise, fine-line, sleeve, sitemap, robots, CNAME, and deploy-marker files before publishing.
5. Audits root-relative internal links and blocks repeated broken targets.
6. Writes `DEPLOYED_MAIN_SHA` and verifies that exact source commit on `gh-pages`.
7. Waits for the active custom domain to serve the same SHA and verifies all critical routes there before reporting success.

## Divergent branch policy

Do **not** merge old divergent branches wholesale.

- `seo/master-authority-rebuild` is substantially ahead and behind current `main`; it contains useful pages/tools mixed with stale rendered HTML and older factual claims.
- `jules-5081671558969232321-bdcd14dd` contains historical sleeve/Katelyn cleanup that has already been substantially harvested into later work; individual live/source checks are required before copying anything.
- `gh-pages` is deployment output, not source-of-truth code.
- old conversion/sync branches are not candidates for wholesale merge.

## Live content findings that require reconciliation

- Live navigation currently identifies Joshua Cole, Katelyn Cole, and Teralyn, while shared source configuration still contains Jay Jay in the resident roster/navigation.
- Shared source hours still contain an older split-hours schedule and need reconciliation against the active published hours before source regeneration.
- The live clean cover-up page is superior to the old underscore source and must not be overwritten while its source is being recovered.
- The live cover-up page also contains testimonial-style copy and some trust/credential wording that requires factual review rather than blind preservation.

## Remaining reconciliation queue

- Bring the clean cover-up route back under source control without replacing the superior live version.
- Inventory live-only pages/assets from the SEO rebuild and classify each as: already live, source missing, obsolete, or safe to salvage.
- Reconcile Teralyn/Jay Jay artist route naming and current roster references.
- Reconcile shared studio hours and navigation facts.
- Reconcile the piercing authority/placement-guide cluster against the live site and remove mismatched tattoo-proof modules.
- Reconcile skin-science pages and flag unsupported quantitative/mechanistic claims for citation review.
- Reconcile legacy indexed routes (`/appointments/`, old cover-up URL, retired geo aliases) and redirects/canonicals.
- Run a production broken-link crawl after deployment and fix all internal 4xx links.

## Release rule

Do not merge this reconciliation branch to `main` or publish it until the source/live differences above are reviewed. A green GitHub Actions run alone is not sufficient; the active website must serve the exact `DEPLOYED_MAIN_SHA` and the critical-route checks must pass.
