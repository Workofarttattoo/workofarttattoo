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

The restored page uses the legacy Work of Art art-catalog images and routes inquiries to the studio booking email. The existing production build step will convert `merchandise/code.html` to `merchandise/index.html` when this branch is merged to `main` and deployed.

## Divergent branch policy

Do **not** merge old divergent branches wholesale.

- `seo/master-authority-rebuild` is 37 commits ahead but also far behind current `main`; it contains useful pages/tools mixed with stale rendered HTML and older factual claims.
- `jules-5081671558969232321-bdcd14dd` contains historical sleeve/Katelyn cleanup that has already been substantially harvested into later work; individual live/source checks are required before copying anything.
- `gh-pages` is deployment output, not source-of-truth code.
- old conversion/sync branches are not candidates for wholesale merge.

## Deployment guardrails

Before production publish:

1. Preserve existing production-only routes and assets.
2. Overlay reviewed current source onto that tree.
3. Generate `index.html` from reviewed `code.html` sources.
4. Require critical routes to exist before publish.
5. Audit root-relative internal links and block repeated broken targets.
6. Write `DEPLOYED_MAIN_SHA` and verify the exact main commit from the active website after propagation.
7. Do not mark reconciliation complete until the active site is checked, not merely GitHub Actions.

## Remaining reconciliation queue

- Bring the clean cover-up route back under source control without replacing the superior live version.
- Inventory live-only pages/assets from the SEO rebuild and classify each as: already live, source missing, obsolete, or safe to salvage.
- Reconcile Teralyn/Jay Jay artist route naming and current roster references.
- Reconcile the piercing authority/placement-guide cluster against the live site and remove mismatched tattoo-proof modules.
- Reconcile skin-science pages and flag unsupported quantitative/mechanistic claims for citation review.
- Reconcile legacy indexed routes (`/appointments/`, old cover-up URL, retired geo aliases) and redirects/canonicals.
- Run a production broken-link crawl after deployment and fix all internal 4xx links.
