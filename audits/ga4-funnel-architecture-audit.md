# GA4 Funnel Architecture Audit

Date: 2026-08-24  
Branch: `seo/master-authority-rebuild`

## Current Lead Event Audit

The event/conversion named `ads_conversion_Submit_lead_form_1` is not emitted by repository source code. A repo-wide search found no source reference to that exact event name. The site does inject Google Analytics (`G-XLXNGGW7SX`) and Google Tag Manager (`GTM-TZTQSQBB`), so the current count of 210 is most likely coming from GA4/GTM/Admin or a Google Ads imported conversion, not a first-party static-site event.

Because the GTM container and GA4 Admin configuration are outside this repository, this repo can verify site-side trigger code, but it cannot prove whether the Ads conversion is mapped to a page view, form submit attempt, click, imported GA4 event, or GTM trigger without account access.

## Existing Site-Side Behavior Before This Sprint

- Appointment pages used native form submissions to FormSubmit with `?sent=tattoo` or `?sent=piercing` success URLs.
- `appointments/woa-booking.js` supported AJAX/PHP submission paths, but did not dispatch a success analytics event after the send completed.
- `woa_ga4_conversions.py` fired `booking_form_submit` on form submit attempt.
- `woa_ga4_conversions.py` fired `piercing_booking_submit` on piercing form submit attempt, before any confirmed send.
- `/appointments/?sent=tattoo|piercing` fired `booking_complete`, deduped by session storage.
- Piercing promotion events used `piercing_deal_view` and `piercing_deal_click`.
- The Start Here hub had visible choices, but no specific `start_here_selection` event.
- Custom `scroll_depth` existed alongside likely GA4 enhanced-measurement `scroll`, creating an analytics duplication risk if both are reported as engagement.

## Risks Found

- `booking_form_submit` and the previous piercing submit event could inflate lead/conversion reporting because they fired on submit attempt, not confirmed delivery.
- AJAX/PHP successful sends were not guaranteed to map to the same conversion event as FormSubmit redirects.
- Source/landing-page context was not preserved as a clean first-party attribution object.
- Internal campaign attribution should not be implemented with UTMs because that can pollute acquisition source/medium.
- Promotion event naming used "deal" language while reporting requirements now use "special."

## Required Repo-Side Model

- `booking_view`: appointment interface is available.
- `booking_start`: client begins a form or chooses a booking service path.
- `booking_submit_attempt`: client attempts to submit a form. This is diagnostic only and should not be marked as a key event.
- `booking_submit`: one true booking completion event, fired only after a success redirect or successful AJAX/PHP response.
- `piercing_booking_submit`: piercing-specific completion, fired only after confirmed piercing submission.
- Piercing commercial events should describe real client actions: CTA, booking start, booking submit, call, text, directions, Katelyn profile, special view/click, jewelry click.
- Attribution should be stored in session storage/local storage with safe page and selection values only. No PII, free-text request descriptions, phone, email, names, medical details, or reference links should be sent to analytics.

## GA Admin / Google Ads Follow-Up

Recommended Admin cleanup after deploy:

- Mark `booking_submit` as the primary key event/conversion.
- Do not mark `booking_submit_attempt`, `booking_start`, or `form_start` as conversions.
- Review and either retire or document `ads_conversion_Submit_lead_form_1`.
- If `ads_conversion_Submit_lead_form_1` is imported from Google Ads or created by GTM, remap it to the `booking_submit` event only.
- Keep `scroll` and `scroll_depth` as engagement diagnostics, not lead quality metrics.
