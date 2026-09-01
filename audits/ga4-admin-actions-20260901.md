# GA4 / GTM Admin Actions Required — 2026-09-01

1. **GA4 key events:** Turn OFF funnel/engagement events; turn ON only `booking_submit` (+ optional `generate_lead`, `phone_click`, `email_click`).
2. **GTM (`GTM-TZTQSQBB`):** Remap `ads_conversion_Submit_lead_form_1` trigger to `woa_verified_lead` or `booking_submit` only.
3. **Google Ads:** Verify conversion import matches verified submission events.
4. **Data filters:** Add internal/developer traffic filters in GA4 Admin (not in repo).
5. **DebugView validation:** Homepage load → no lead events; appointments → one `booking_view`; successful submit → one `booking_submit`.

See `docs/analytics-event-contract.md` for full event semantics.
