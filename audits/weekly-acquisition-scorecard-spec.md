# Weekly Acquisition Scorecard Spec

Date: 2026-08-24  
Scope: Work of Art GA4 / Google Ads / Search Console weekly piercing and booking review.

## Primary Funnel

| Metric | Formula | Notes |
| --- | --- | --- |
| Booking views | Count of `booking_view` | Appointment interface reached. |
| Booking starts | Count of `booking_start` | First meaningful form interaction or appointment-path click. |
| Booking submissions | Count of `booking_submit` | True completion only. Primary key event candidate. |
| Booking start rate | `booking_start / booking_view` | Diagnose page friction. |
| Booking completion rate | `booking_submit / booking_start` | Diagnose form friction or delivery issues. |
| Piercing submissions | Count of `piercing_booking_submit` | Piercing-specific confirmed leads. |
| Piercing CTA rate | `piercing_cta_click / piercing page sessions` | CTA quality on piercing pages. |

## Piercing Commercial Events

| Event | Use |
| --- | --- |
| `piercing_special_view` | Measures exposure to the permanent specials module. |
| `piercing_special_click` | Measures interest in current piercing specials. |
| `piercing_booking_start` | Measures piercing-intent booking starts. |
| `piercing_booking_submit` | Measures confirmed piercing booking submissions. |
| `piercing_call_click` | Measures high-intent phone taps. |
| `piercing_text_click` | Measures high-intent SMS taps. |
| `piercing_directions_click` | Measures local/travel intent. |
| `piercing_katelyn_click` | Measures Katelyn trust/profile engagement. |
| `piercing_jewelry_click` | Measures jewelry education interest. |

## Attribution Dimensions

Use event parameters instead of internal UTMs:

- `landing_page`
- `origin_page`
- `service_interest`
- `service_category`
- `service_type`
- `artist`
- `promotion_id`
- `promo_campaign`
- `promo_context`
- `click_location`

Do not send names, email addresses, phone numbers, medical history, reference links, tattoo descriptions, or piercing notes.

## Weekly Review Questions

- Which landing pages drive the most `booking_submit` events?
- Which piercing pages drive `piercing_booking_start` but not `piercing_booking_submit`?
- Do specials views become specials clicks?
- Do Katelyn profile clicks improve piercing booking completion?
- Are calls/texts rising on mobile while form completions stay flat?
- Are Google Ads conversions counting the same event as GA4 `booking_submit`?

## Recommended GA Admin Setup

- Mark `booking_submit` as the main key event.
- Keep `piercing_booking_submit` as a secondary piercing-segment key event if useful.
- Do not mark `booking_start`, `booking_submit_attempt`, `form_start`, `scroll`, or `scroll_depth` as lead conversions.
- Retire or remap `ads_conversion_Submit_lead_form_1` once GA/GTM confirms its trigger.
