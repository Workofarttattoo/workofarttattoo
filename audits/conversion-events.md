# Conversion Events

Existing analytics detected:

- Google Tag Manager: `GTM-TZTQSQBB`
- Google Analytics / gtag: `G-XLXNGGW7SX`

## Recommended Event Names

Use these consistently in GTM/gtag if not already configured:

| Event | Trigger | Priority |
|---|---|---|
| `phone_click` | `tel:` click | P0 |
| `booking_click` | appointment/booking CTA click | P0 |
| `email_click` | `mailto:` click | P1 |
| `directions_click` | map/directions link click | P0 |
| `artist_profile_view` | artist profile pageview | P1 |
| `gallery_view` | gallery/healed work view | P1 |
| `consultation_start` | consult form or booking flow start | P0 |
| `instagram_click` | artist/studio Instagram outbound click | P2 |

Do not invent analytics IDs. Wire these through the existing GTM/gtag infrastructure and test in GA debug/realtime before treating them as production KPIs.

