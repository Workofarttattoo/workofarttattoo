# Production Reconciliation — 2026-08-30

Three-way comparison of **main** (editable source), **gh-pages** (generated deploy output), and **live** (`https://www.workofarttattoo.com/`).

Evidence rule: **live HTML is treated as production truth** when branches disagree. Newer `main` commits are not assumed correct.

## Hosting model

| Layer | Role |
|-------|------|
| `main` | Authoritative editable source (`code.html` + committed `index.html` where generated) |
| `gh-pages` | Generated deployment output only — never edit directly |
| Live | Serves `gh-pages` via GitHub Pages custom domain `www.workofarttattoo.com` |

Live deploy marker at audit time: `94e0aaf` (Aug 28, 2026). Current `main` HEAD is ahead; no deploy has run since marker.

## Sitewide NAP / SEO notes (all priority routes)

| Signal | Production (live) | main | Notes |
|--------|---------------------|------|-------|
| Phone | `(725) 224-1240` / `725-224-1240` | Same on matched routes | Consistent |
| Footer email | `booking@workofarttattoo.com` | Same on most pages | Schema on some pages still references `thewhiteknight702@gmail.com` |
| Canonical host | Mixed: bare `workofarttattoo.com` on core pages; `www.` on newer hyphen routes | Same split | Not a content fork; normalize in a future SEO pass |
| Hours | Not surfaced as a structured block on priority routes | Same | Hours live in schema/footer on select pages only |
| Knowledge vault | `#knowledge-base` + `woa-kb-card` grid on `/` | Same | Class `woa-kb-group` not present; module is present under different markup |

---

## Reconciliation table

| ROUTE | MAIN | GH-PAGES | LIVE | STATUS | ACTION |
|-------|------|----------|------|--------|--------|
| `/` | ✅ index.html — title/canonical/phone/hero imgs/CTAs match | ✅ identical bytes | ✅ HTTP 200, identical | **MATCH** | None. Optional: add visible H1; align roster copy to 3-person `STUDIO_ROSTER_BLURB` (currently says "Two resident specialists"). |
| `/artists/` | ✅ index.html | ✅ identical | ✅ HTTP 200 | **MATCH** | None |
| `/artists/joshua-cole/` | ✅ index.html | ✅ identical | ✅ HTTP 200 | **MATCH** | None |
| `/artists/katelyn-cole/` | ✅ index.html | ✅ identical | ✅ HTTP 200 | **MATCH** | None |
| `/artists/teralyn/` | ⚠️ `code.html` only (17 KB source) | ✅ built `index.html` (37 KB) | ✅ HTTP 200 | **MATCH** | Keep `artists/teralyn/code.html` as source; deploy builds via `artists_build/teralyn.html` → `index.html`. Do not edit gh-pages. |
| `/appointments/` | ✅ index.html | ✅ identical | ✅ HTTP 200 | **MATCH** | None |
| `/merchandise/` | ⚠️ `code.html` only | ✅ `index.html` | ✅ HTTP 200 | **MATCH** | Source = `merchandise/code.html`; deploy copies to `index.html`. Local images (not `/wp-content/`). |
| `/cover-up-tattoos-las-vegas/` | ⚠️ `code.html` only | ✅ `index.html` | ✅ HTTP 200 | **MATCH** | Source = `cover-up-tattoos-las-vegas/code.html`. **DUPLICATE** route also exists at `/cover_up_tattoos_las_vegas_master_authority_guide/` (200 live) — see preserved routes below. |
| `/best_piercing_shop_las_vegas_updated_jewelry_standards/` | ✅ index.html | ✅ identical | ✅ HTTP 200 | **MATCH** | None |
| `/fine_line_tattoos_las_vegas_master_authority_guide/` | ✅ index.html | ✅ identical | ✅ HTTP 200 | **MATCH** | None |
| `/best_tattoo_styles_for_sleeves_large_scale_project_hub/` | ❌ had unreconciled 97 KB rewrite in `code.html` | ✅ 32 KB hub (live version) | ✅ HTTP 200 | **LIVE AHEAD** → fixed | Restored `code.html` + `index.html` from gh-pages/live. Retired draft rewrite preserved only in git history. |
| `/walk_in_tattoos_las_vegas_authority_guide/` | ❌ `index.html` contained **Jay Jay** artist page (wrong canonical) | ✅ walk-in authority guide | ✅ HTTP 200 | **BROKEN** → fixed | Restored from gh-pages/live. Jay Jay content removed per entity-conflict policy. |
| `/tattoo_shop_near_the_strip_geo_seo_optimized/` | ✅ index.html | ✅ identical | ✅ HTTP 200 | **MATCH** | None |
| `/dermis_skin_science_las_vegas_authority_guide/` | ⚠️ `code.html` only (complete page) | ❌ missing | ❌ HTTP 404 | **BROKEN** | Add to deploy build + sitemap; publish on next deploy. Do not delete source. |

---

## Field-level summary (priority routes)

| Route | Title (live) | Canonical (live) | H1 (live) | Key images (live) | Primary CTAs (live) |
|-------|--------------|------------------|-----------|-------------------|---------------------|
| `/` | Tattoo and Piercing Shop Near Me \| Las Vegas \| Work of Art | `https://workofarttattoo.com/` | *(no H1)* | `las-vegas-tattoo-hero-background.webp`, studio banner | `/appointments/`, `mailto:booking@workofarttattoo.com` |
| `/artists/` | Artists \| Work of Art Tattoo & Piercing Las Vegas | `…/artists/` | Artists at Work of Art | `joshua-cole-portrait-las-vegas.webp` + gallery | `/appointments/` |
| `/artists/joshua-cole/` | Joshua Cole \| Realism Tattoo Artist Las Vegas \| Work of Art | `…/artists/joshua-cole/` | Joshua Cole — Realism Tattoo Artist Las Vegas | `joshua-cole-portrait-las-vegas.webp`, gallery webps | `/appointments/`, `#booking-vault` |
| `/artists/katelyn-cole/` | Ear Piercing Las Vegas \| Katelyn Cole \| Work of Art | `…/artists/katelyn-cole/` | Katelyn Cole — Ear Piercing in Las Vegas | Katelyn piercing webps | `/appointments/` |
| `/artists/teralyn/` | Teralyn \| Tattoo Artist & Piercer Las Vegas \| Work of Art | `https://www.workofarttattoo.com/artists/teralyn/` | Teralyn | `teralyn-fine-line-tattoo-artist-las-vegas.webp` | `/appointments/` |
| `/appointments/` | Book an Appointment \| Work of Art Tattoo & Piercing Las Vegas | `…/appointments/` | Book your appointment | studio/gallery imgs | Fresha + `/appointments/` |
| `/merchandise/` | Merchandise & Original Art \| Work of Art Tattoo Las Vegas | `https://www.workofarttattoo.com/merchandise/` | Merchandise & one-of-a-kind pieces | local framed-art webps/pngs | `/appointments/` |
| `/cover-up-tattoos-las-vegas/` | Tattoo Cover-Ups — Joshua Cole \| Work of Art Las Vegas | `https://www.workofarttattoo.com/cover-up-tattoos-las-vegas/` | Cover Up Tattoos Las Vegas | cover-up before/after imgs | `/appointments/` |
| `/best_piercing_shop…/` | Body Piercing Store Near Me Las Vegas \| Helix \| Work of Art | `…/best_piercing_shop_las_vegas_updated_jewelry_standards/` | Body Piercing Store Near Me — Las Vegas | piercing + tattoo imgs | `/appointments/` |
| `/fine_line_tattoos…/` | Fine Line Tattoos Las Vegas \| Single Needle Guide \| WOA | `…/fine_line_tattoos_las_vegas_master_authority_guide/` | Mastering the Micro: The Physics & Art of Fine Line | interview + fine-line webps | `/appointments/` |
| `/best_tattoo_styles…/` | Best Tattoo Styles For Sleeves \| Work of Art Tattoo Las Vegas | *(none in live head)* | Best Tattoo Styles For Sleeves: Planning & Composition | sleeve gallery pngs | `/appointments/` |
| `/walk_in_tattoos…/` | Walk-In Tattoos Las Vegas \| Tattoo and Piercing Shop Near Me \| Work of Art | `https://workofarttattoo.com/walk_in_tattoos_las_vegas_authority_guide/` | Instant Art. Zero Compromise. | studio hero + gallery | `/appointments/`, `mailto:booking@workofarttattoo.com` |
| `/tattoo_shop_near_the_strip…/` | Tattoo and Piercing Shops Near Me Las Vegas \| Strip Area \| Work of Art | `…/tattoo_shop_near_the_strip_geo_seo_optimized/` | Vegas Artistry, No Ego Culture. | geo hero png + gallery | `/appointments/` |
| `/dermis_skin_science…/` | — | — | — | — | — |

---

## Intentionally preserved production-only / duplicate routes

These remain live on gh-pages and should stay until redirects are wired in `main`:

| Live URL | Relationship | Policy |
|----------|--------------|--------|
| `/cover_up_tattoos_las_vegas_master_authority_guide/` | Underscore legacy cover-up hub (200) | **DUPLICATE** of `/cover-up-tattoos-las-vegas/`. Nav prefers hyphen route. Keep live until 301 added in source. |
| `/walk-in-tattoos-las-vegas/` | Hyphen alias referenced in some `code.html` canonicals | **404 live**. Authority URL is `/walk_in_tattoos_las_vegas_authority_guide/`. |
| Jay Jay artist URLs | Removed from roster | **Do not restore**. `walk_in` index had been contaminated with Jay Jay export — fixed in this reconciliation. |

---

## Source-of-truth policy (post-reconciliation)

1. **Edit only on `main`**: `code.html` for page bodies; run `prepare_site_deploy.py` before push; CI copies `code.html` → `index.html` and publishes to `gh-pages`.
2. **Never treat `gh-pages` as source**: it is rsync output + `DEPLOYED_MAIN_SHA`.
3. **Live wins on conflict**: when `main` diverges from live, either restore from gh-pages/live (this pass) or get explicit owner approval before deploy.
4. **Deploy blockers on `main` at audit time**:
   - Unresolved merge conflict markers in `.github/workflows/deploy-production.yml` — must be resolved before next production deploy.
   - `/dermis_skin_science_las_vegas_authority_guide/` ready in source but not in gh-pages/sitemap — add to deploy verification list.

## Fixes applied on `main` in this reconciliation

- Restored `/walk_in_tattoos_las_vegas_authority_guide/` from live/gh-pages (removed Jay Jay contamination).
- Restored `/best_tattoo_styles_for_sleeves_large_scale_project_hub/` from live/gh-pages (retired unreconciled rewrite in `code.html`).
- Added `three_way_reconciliation.py` + `audits/three-way-reconciliation-2026-08-30.csv` for repeatable audits.

## Next deploy checklist

1. Resolve deploy workflow conflict markers (keep HEAD deploy verifier with critical route list).
2. Add `/dermis_skin_science_las_vegas_authority_guide/` to sitemap + deploy critical routes.
3. Push `main` → verify `DEPLOYED_MAIN_SHA` on live matches new commit.
4. Re-run: `python3 three_way_reconciliation.py`
