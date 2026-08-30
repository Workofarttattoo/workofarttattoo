# Analytics & Tracking Audit — Work of Art Tattoo

**Date:** August 2026  
**Container:** GTM `GTM-TZTQSQBB` (sitewide via `inject_google_tag_manager.py`)  
**Site events:** `woa_ga4_conversions.py` → injected by `inject_ga4_conversions.py`

## Executive summary

| Event | Status | Notes |
|-------|--------|-------|
| `book_click` | ✅ Sitewide | Fires on `/appointments/` link clicks |
| `booking_page_view` | ✅ Fixed | Canonical name; `booking_view` kept as legacy alias |
| `form_start` | ✅ Sitewide | First interaction on tattoo/piercing forms |
| `form_submit_success` | ✅ **New** | **One event per successful submission** (deduped) |
| `phone_click` | ✅ Fixed | Alias of `call_click` |
| `directions_click` | ✅ Sitewide | Google Maps / g.page links |
| `email_click` | ✅ Sitewide | `mailto:` links |
| `ads_conversion_Submit_lead_form_1` | ⚠️ **Not in repo** | Configured in GTM/Google Ads — verify in GTM UI |

## `ads_conversion_Submit_lead_form_1`

**Not found in this repository.** It is almost certainly a **Google Tag Manager conversion tag** or **Google Ads conversion linker** separate from `woa_ga4_conversions.py`.

### How to verify in GTM (owner action)

1. Open GTM container `GTM-TZTQSQBB` → Tags → search `Submit_lead_form` or `ads_conversion`.
2. Check **trigger**: should fire on `form_submit_success` or FormSubmit redirect — **not** on page load or button click alone.
3. In GA4 DebugView / Tag Assistant, complete a test form and confirm:
   - Exactly **one** conversion per submission
   - No duplicate fire from both redirect + AJAX paths
4. If the Ads tag still listens to deprecated `booking_submit` + `booking_complete`, update it to `form_submit_success`.

## Duplicate firing issues (fixed)

| Issue | Before | After |
|-------|--------|-------|
| Success events | `booking_submit` + `booking_complete` both on redirect | Single `form_submit_success`; legacy events gated behind same dedupe |
| AJAX + redirect | Could double-count if both paths ran | `sessionStorage` key `woa_form_submit_success_{service}` blocks repeats |
| Booking page name | Only `booking_view` | `booking_page_view` primary; `booking_view` legacy |
| Phone | Only `call_click` | `phone_click` added as alias |

## Event flow (booking funnel)

```
Discovery page
  → book_click (appointment link)
  → booking_page_view (appointments page load)
  → form_start (first field interaction)
  → form_submit_success (redirect ?sent=tattoo|piercing OR ajax woa_booking_submit_success)
```

## Piercing attribution

Promo blocks (`data-woa-piercing-special`) persist `woa_piercing_attribution` in sessionStorage and attach to success events.

## Debug mode

Append `?debug_analytics=1` to any URL — events include `debug_mode: true` for GA4 DebugView.

## Files

| File | Role |
|------|------|
| `woa_ga4_conversions.py` | Event definitions (source of truth for site JS) |
| `inject_ga4_conversions.py` | Injects script into all HTML pages |
| `appointments/woa-booking.js` | Dispatches `woa_booking_submit_success` on AJAX success |

## Appointments page note

`appointments/code.html` may contain an inline copy of the GA4 block from an earlier build. The deploy pipeline re-injects via `inject_ga4_conversions.py` (runs twice in `prepare_site_deploy.py`). No functional duplicate listeners if only one `data-woa-ga4-conversions` block exists after build.
