# UTM Attribution Guide — Work of Art Tattoo

Use UTMs on **external links we control** only. **Never** add UTMs to internal `workofarttattoo.com` links.

## Conventions (implemented in `woa_external_attribution.py`)

| Channel | utm_source | utm_medium | utm_campaign |
|---------|------------|------------|--------------|
| Instagram (studio) | `instagram` | `organic_social` | `portfolio` |
| Instagram (Joshua) | `instagram` | `organic_social` | `joshua_portfolio` |
| Instagram (Katelyn) | `instagram` | `organic_social` | `katelyn_portfolio` |
| Instagram (Teralyn) | `instagram` | `organic_social` | `teralyn_portfolio` |
| Facebook | `facebook` | `organic_social` | `portfolio` |
| Google Business Profile | `google` | `business_profile` | `local` |
| QR codes (shop) | `qr` | `offline` | `shop` |
| Email campaigns | `email` | `email` | `studio` |
| SMS campaigns | `sms` | `sms` | `studio` |

## Sitewide automation

`fix_social_links.py` applies Instagram/Facebook UTMs to footer and artist-page social links during build.

## Manual links (owner applies)

### Google Business Profile

Website button and posts should use:

```
https://www.workofarttattoo.com/?utm_source=google&utm_medium=business_profile&utm_campaign=local
```

Or deep-link to a page:

```
https://www.workofarttattoo.com/appointments/?utm_source=google&utm_medium=business_profile&utm_campaign=local
```

### QR codes (print, signage, business cards)

```
https://www.workofarttattoo.com/start_here/?utm_source=qr&utm_medium=offline&utm_campaign=shop
```

### Email / SMS blasts

```
https://www.workofarttattoo.com/appointments/?utm_source=email&utm_medium=email&utm_campaign=studio
```

Use `utm_content` for A/B variants (e.g. `utm_content=piercing_special_march`).

## Reducing Direct / Unassigned traffic

1. Add UTMs to **all** bio links (Instagram, Facebook, TikTok if used).
2. Use tagged short links on GBP posts and review responses.
3. Tag QR landing URLs on physical materials.
4. Do **not** tag internal navigation — that pollutes session attribution.

## GA4 reporting

Create explorations filtered by `session source / medium` for:

- `instagram / organic_social`
- `google / business_profile`
- `qr / offline`

Compare month-over-month against total Direct and Unassigned.
