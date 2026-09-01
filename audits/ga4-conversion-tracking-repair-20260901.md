# GA4 Conversion Tracking Repair — 2026-09-01

**Branch:** `fix/ga4-conversion-tracking-repair-20260901`  
**Base main SHA:** `9f78c3cc71caacbe498f4116013a99a4bfa9ebee`

## Analytics architecture

| Layer | ID / file | Role |
|-------|-----------|------|
| GA4 (direct gtag) | `G-XLXNGGW7SX` | `inject_google_tag.py` |
| GTM | `GTM-TZTQSQBB` | `inject_google_tag_manager.py` |
| Site events | `woa_ga4_conversions.py` | `inject_ga4_conversions.py` |
| Booking bridge | `appointments/woa-booking.js` | AJAX success → `woa_booking_submit_success` |
| Mixpanel | `db89dd14246e223536112f4ba3d5cbc0` | Separate product analytics |
| Google Ads | GTM-managed | `ads_conversion_Submit_lead_form_1` — **not in repo** |

**Architecture type:** **C — both GTM and direct gtag** on most pages. Homepage was missing direct gtag until this repair added `inject_google_tag.py` to deploy pipeline.

## Tracking inventory table

| File | Tracking type | ID | Events sent | Trigger | Destination |
|------|---------------|-----|-------------|---------|-------------|
| `inject_google_tag.py` | gtag config | G-XLXNGGW7SX | page_view (auto) | Page load | GA4 |
| `inject_google_tag_manager.py` | GTM bootstrap | GTM-TZTQSQBB | Container-defined | Page load | GTM → GA4/Ads |
| `woa_ga4_conversions.py` | Custom events | via gtag + dataLayer | booking funnel, CTAs, scroll_depth | User actions | GA4 + GTM dataLayer |
| `appointments/woa-booking.js` | DOM bridge | — | woa_booking_submit_success | AJAX/PHP success | → woa_ga4_conversions |
| `inject_mixpanel.py` | Mixpanel | db89dd… | autocapture | Page load | Mixpanel |

## Root cause (99.41% key events)

See `audits/key-event-root-cause-20260901.md`. Primary: GA4 Admin + GTM marking funnel/engagement events as key events/conversions.

## Files changed (code)

- `woa_ga4_conversions.py` — funnel semantics, dedupe, generate_lead, instagram_click, automated traffic guard
- `prepare_site_deploy.py` — add `inject_google_tag.py`; verify GA4 on homepage
- `tools/seo_qa.py` — analytics validation expanded
- `tests/test_analytics_semantics.py` — new test suite
- `docs/analytics-event-contract.md` — event contract
- `audits/*.md` — audit artifacts
- All `*/code.html` — regenerated conversion script block via `inject_ga4_conversions.py`
- Homepage sources — gtag added via `inject_google_tag.py`

## QA results

See final report section M (run after tests complete).

## SEO content

No intentional changes to titles, metas, H1s, body copy, canonicals, sitemap, or robots.
