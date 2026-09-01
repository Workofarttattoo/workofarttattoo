# GA4 Key Event Recommendations — 2026-09-01

## Primary key events (ON)

| Event | Rationale |
|-------|-----------|
| `booking_submit` | Verified successful booking/contact submission |
| `generate_lead` | GA4 recommended; fires with same dedupe as booking_submit |

## Optional primary (owner decision)

| Event | Rationale |
|-------|-----------|
| `phone_click` | Count phone calls as leads if desired |
| `email_click` | Count email clicks as leads if desired |

## Optional secondary

| Event | Rationale |
|-------|-----------|
| `directions_click` | Visit intent; not a booking lead |

## Must be OFF (not key events)

- `page_view`
- `session_start`
- `user_engagement`
- `scroll` / `scroll_depth`
- `booking_view` / `booking_page_view`
- `booking_start` / `book_click` / `form_start`
- `booking_submit_attempt`
- `booking_complete` (legacy alias)
- `form_submit_success` (legacy alias)
- `piercing_booking_start`
- `piercing_special_view` / `piercing_special_click`
- `ads_conversion_Submit_lead_form_1` until GTM trigger is fixed

## Generate Leads report

Use `generate_lead` and/or `booking_submit` as the qualified lead signal. Do not mark funnel steps as lead equivalents.
