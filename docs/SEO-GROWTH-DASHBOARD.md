# SEO Growth Dashboard — Work of Art Tattoo

Track these metrics **monthly** in GA4 (and Google Search Console for organic). Export on the 1st of each month for trend comparison.

## Traffic health

| Metric | GA4 path | Notes |
|--------|----------|-------|
| Active users | Reports → Acquisition overview | Total site |
| New users | Same | Growth vs returning |
| Organic Search users | Acquisition → Traffic acquisition → `Organic Search` | Primary SEO KPI |
| Organic Search sessions | Same | Session volume |
| AI Assistant sessions | Explore → filter `session source` contains `chatgpt`, `perplexity`, `copilot`, `gemini`, `claude` | Adjust as new referrers appear |
| Google / organic sessions | `google / organic` | Classic search |
| Direct sessions | `direct / (none)` | Watch for inflation when UTMs missing |
| Unassigned sessions | `(not set)` | Should decrease as UTMs improve |

## Landing pages

| Metric | Source |
|--------|--------|
| Top landing pages | GA4 → Engagement → Landing page |
| Organic landing pages | GSC → Performance → Pages + filter Queries |

**Protected winners to watch individually:**

- `/appointments/`
- `/start_here/`
- `/piercing-guide-las-vegas/`
- `/artists/katelyn-cole/`
- `/cover-up-tattoos-las-vegas/`
- `/artists/joshua-cole/`
- `/best_piercing_shop_las_vegas_updated_jewelry_standards/`
- `/ear_piercing_guide_las_vegas/`
- `/skin_science_tattoo_dermatology_authority_guide/`

## Conversion funnel (custom events)

| Event | Meaning |
|-------|---------|
| `book_click` | Clicked link to `/appointments/` |
| `booking_page_view` | Loaded appointments page |
| `form_start` | Started tattoo or piercing form |
| `form_submit_success` | **Completed** submission (one per success) |
| `phone_click` | Clicked `tel:` link |
| `directions_click` | Clicked maps/directions link |
| `email_click` | Clicked `mailto:` link |

## Conversion rates

Calculate in GA4 Explore (Funnel or calculated metrics):

| Rate | Formula |
|------|---------|
| Visitor → book click | `book_click` users ÷ Active users |
| Book click → form start | `form_start` users ÷ `book_click` users |
| Form start → submission | `form_submit_success` users ÷ `form_start` users |
| Full funnel | `form_submit_success` ÷ Active users |

## Monthly checklist

- [ ] Export traffic by channel (CSV)
- [ ] Compare Direct + Unassigned % to prior month
- [ ] Review top 20 landing pages for position/clicks (GSC)
- [ ] Verify `form_submit_success` count ≈ actual FormSubmit emails received
- [ ] Check protected URLs — no ranking drops >15% WoW
- [ ] Note any new AI referrer strings for filter updates

## Baseline context (owner-reported)

| Month | Approx. visitors |
|-------|------------------|
| Recent trend | ~150 → ~250 → ~300 → **~880** (current) |

Use this dashboard to confirm growth continues while conversion and attribution improve.

## Related docs

- `docs/analytics-tracking-audit.md` — event implementation details
- `docs/utm-attribution-guide.md` — UTM conventions for off-site links
