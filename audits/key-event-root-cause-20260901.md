# Key Event Root Cause — 2026-09-01

## Summary

**99.41% session key-event rate** is caused by (1) GA4 Admin marking low-intent funnel/engagement events as key events, and (2) GTM Google Ads conversion `ads_conversion_Submit_lead_form_1` firing on pre-success triggers (~219 events vs ~847 sessions).

Site code did **not** emit `ads_conversion_Submit_lead_form_1` — that name is GTM/Google Ads imported.

## Event analysis

| Event | Current trigger | Why it fires | Should be key event? | Recommended action |
|-------|-----------------|--------------|----------------------|--------------------|
| `page_view` | gtag/GTM page load | Every page | No | Unmark in GA4 Admin |
| `session_start` | GA4 automatic | Every session | No | Unmark in GA4 Admin |
| `user_engagement` | GA4 automatic | Engaged sessions | No | Unmark in GA4 Admin |
| `scroll` / `scroll_depth` | Scroll listener + enhanced measurement | Most scrolling users | No | Unmark; keep diagnostic only |
| `booking_view` | `/appointments/` first view per session | Booking page visit | **No** | Unmark; viewing ≠ lead |
| `booking_start` | Book CTA click or first form field | Intent only | **No** | Unmark |
| `book_click` | Link to `/appointments/` | Navigation | No | Unmark |
| `form_start` | First form interaction | Form open | No | Unmark |
| `booking_submit_attempt` | Form submit before response | Attempt ≠ success | **No** | Unmark |
| `booking_submit` | Verified success only (after fix) | True lead | **Yes** | Keep ON |
| `generate_lead` | Verified success only (after fix) | GA4 recommended lead | Optional Yes | Keep ON if used |
| `ads_conversion_Submit_lead_form_1` | **GTM** (likely booking_view/start) | Pre-success trigger | **No until fixed** | Remap GTM to `woa_verified_lead` |

## Code fixes applied

1. `booking_submit` + `generate_lead` fire **only** in `recordFormSubmitSuccess` (deduped).
2. `booking_view` deduped once per session (`woa_booking_view_session`).
3. Init guard prevents duplicate listeners.
4. `woa_verified_lead` dataLayer event for GTM Ads mapping.
5. Automated traffic suppression.
