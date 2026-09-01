# GA4 / GTM Admin Actions Required — 2026-09-01

These steps **cannot** be done in the repository. Owner must perform after deploy.

## 1. Key events (GA4 Admin → Events)

**Turn OFF** as key events:
- `page_view`, `session_start`, `user_engagement`, `scroll`, `scroll_depth`
- `booking_view`, `booking_page_view`, `booking_start`, `book_click`, `form_start`
- `booking_submit_attempt`, `booking_complete`, `form_submit_success`
- `piercing_booking_start`, `piercing_deal_view`, `piercing_deal_click`
- Any event with >50% session rate that is not a verified submission

**Turn ON** as key events:
- `booking_submit` (primary)
- `generate_lead` (optional co-primary)

**Optional ON:** `phone_click`, `email_click`

## 2. Google Tag Manager (`GTM-TZTQSQBB`)

1. Tags → find `Submit_lead_form` / `ads_conversion_Submit_lead_form_1`
2. **Change trigger** to Custom Event: `woa_verified_lead` OR GA4 event `booking_submit`
3. Remove triggers on: `booking_view`, `booking_start`, `page_view`, All Pages, DOM Ready
4. Publish container
5. Tag Assistant: complete test booking → exactly **one** Ads conversion

## 3. Google Ads

1. Tools → Conversions → verify import source is `booking_submit` or fixed GTM tag
2. Disable duplicate conversion actions if multiple count the same action

## 4. Data filters (GA4 Admin)

- Create **Internal traffic** rule (IP or debug param) if staff traffic is significant
- Create **Developer traffic** filter for `debug_analytics=1` sessions
- Do not hard-code personal IPs in repo

## 5. Unassigned traffic (~31.5%)

- Review Acquisition → Traffic acquisition → Session source
- Unassigned often = missing referrer + no UTM + direct app/webview
- **Do not** add UTMs to internal links (already prevented in `woa_external_attribution.py`)
- AI assistant attribution (ChatGPT, Perplexity) appears to work — do not override with custom JS

## 6. Bot / data-center traffic

- Use GA4 Admin **Bot filtering** (if available on property)
- Consider segment excluding Singapore/data-center spikes for business reporting
- Do not geo-block at website level

## 7. Validate in DebugView

1. Load homepage → no `booking_submit`, no `generate_lead`
2. Load `/appointments/` → one `booking_view`, no submit
3. Click book CTA from another page → `booking_start`, no submit
4. Submit form successfully → one `booking_submit`, one `generate_lead`, one `woa_verified_lead`
