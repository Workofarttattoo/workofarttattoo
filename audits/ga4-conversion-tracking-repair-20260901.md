# GA4 Conversion Tracking Repair — 2026-09-01

**Branch:** `fix/ga4-conversion-tracking-repair-20260901`  
**Base main SHA:** `9f78c3cc71caacbe498f4116013a99a4bfa9ebee`

## Architecture

- **GA4:** `G-XLXNGGW7SX` via `inject_google_tag.py`
- **GTM:** `GTM-TZTQSQBB` via `inject_google_tag_manager.py`
- **Events:** `woa_ga4_conversions.py` → `inject_ga4_conversions.py`
- **Type:** C — both GTM and direct gtag (mixed; homepage gtag added in this repair)

## Root cause

GA4 Admin + GTM key-event/conversion misconfiguration. See `audits/key-event-root-cause-20260901.md`.

## QA

- Analytics unit tests: 11/11 PASS
- `validate_analytics_source`: PASS
- SEO titles on key pages: unchanged vs origin/main
