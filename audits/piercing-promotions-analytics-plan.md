# Piercing Promotions Analytics Plan

Last updated: 2026-08-25

## Current Repo-Controlled Tracking

The static site already injects GA4/GTM-side engagement tracking through `woa_ga4_conversions.py` and `inject_ga4_conversions.py`.

Existing site-side events include:

- `call_click`
- `email_click`
- `book_click`
- `directions_click`
- `form_start`
- `booking_form_submit`
- `booking_page_view`
- `booking_complete`
- `booking_iframe_loaded`
- `scroll_depth`

No connected GA4 property access was available in this repo pass, so the reported August 20 traffic anomaly should not be treated as human conversion activity without GA4 source/medium, event, bot, and key-event validation.

## New Piercing Promotion Events

Added to the existing GA4 listener:

- `piercing_deal_view`
- `piercing_deal_click`
- `piercing_booking_start`
- `piercing_booking_submit`
- `piercing_call_click`
- `piercing_text_click`
- `piercing_directions_click`
- `piercing_katelyn_profile_click`
- `piercing_jewelry_click`

Promotion attribution is stored in session storage only after a user clicks from a piercing promotion or piercing booking CTA. No internal UTM parameters were added to internal links.

## Weekly Report Spec

Recommended weekly piercing report columns:

- Week start date
- Promotion ID
- Promotion status
- Promo views
- Promo clicks
- Booking starts from promo
- Piercing booking submits
- Call clicks
- Text clicks
- Directions clicks
- Katelyn profile clicks
- Jewelry guide clicks
- Top source / medium
- Top landing page
- New users
- Returning users
- Notes from front desk or Katelyn

## Data Quality Checks

Before calling a promo successful, compare:

- Promo clicks to booking starts
- Booking starts to actual appointment requests
- Text/call clicks to real phone volume if available
- Source/medium quality to screen out spam/bot traffic
- Location pages that assisted conversion without becoming doorway pages

## Promotion Source of Truth

The editable promotion config is:

`siteData/piercing_promotions.json`

Do not create weekly URLs. Update the active promotion data and regenerate the site.
