# Analytics Event Contract — Work of Art Tattoo

Source of truth for client-side GA4/GTM events. Implementation: `woa_ga4_conversions.py` (injected by `inject_ga4_conversions.py`).

## IDs

| System | ID |
|--------|-----|
| GA4 | `G-XLXNGGW7SX` |
| GTM | `GTM-TZTQSQBB` |
| Google Ads conversion | **GTM-managed** — remap to `woa_verified_lead` / `booking_submit` |

## Event contract

| Event | When it fires | When it must NOT fire | Key event? | Purpose |
|-------|---------------|------------------------|------------|---------|
| `page_view` | GA4 automatic / gtag config | — | No | Page traffic |
| `scroll_depth` | User scrolls past 25/50/75/90% | Page load | No | Engagement diagnostic |
| `booking_view` | First `/appointments/` view per browser session | Repeat reloads same session; non-booking pages | No | Booking funnel top |
| `booking_start` | Book CTA click or first form field interaction | Page load; iframe load | No | Intent to book |
| `booking_submit_attempt` | Native form submit event (before server response) | Page load; CTA click alone | No | Diagnostic / drop-off |
| `booking_submit` | Verified successful submission only | Page load; view; start; failed validation; attempt | **Yes (primary)** | True completed lead |
| `generate_lead` | Same trigger as `booking_submit` | Any pre-success action | Optional primary | GA4 recommended lead event |
| `phone_click` | `tel:` link click | — | Optional primary | Call intent |
| `email_click` | `mailto:` link click | — | Optional primary | Email intent |
| `directions_click` | Google Maps / g.page link click | — | Optional secondary | Visit intent |
| `instagram_click` | Instagram profile/post link click | — | No | Social outbound |
| `woa_verified_lead` (dataLayer) | Successful submission | All other triggers | GTM → Ads only | Google Ads conversion hook |

## Google Ads relationship

- `ads_conversion_Submit_lead_form_1` is **not** emitted by site code.
- GTM must fire Google Ads conversion **only** on `woa_verified_lead` or `booking_submit` / `generate_lead`.
- Do **not** map Ads conversion to `booking_view`, `booking_start`, `book_click`, `scroll_depth`, or `page_view`.

## Success verification paths

1. AJAX/PHP success → `woa_booking_submit_success` custom event → `recordFormSubmitSuccess`
2. FormSubmit redirect → `/appointments/?sent=tattoo|piercing` → `recordFormSubmitSuccess`

Deduped per service via `sessionStorage` key `woa_form_submit_success_{service}`.

## Debug

Append `?debug_analytics=1` to any URL for GA4 DebugView (`debug_mode: true` on events only). Never enable globally in production gtag config.

## Automated traffic

Events suppressed for headless QA, Lighthouse, `navigator.webdriver`, `?woa_qa=1`, and `sessionStorage.woa_analytics_opt_out=1`.

## Privacy

Never send customer name, email, phone, form free text, medical info, or tattoo/piercing descriptions in analytics payloads.
