# GSC Wizard ↔ GA4 setup — Work of Art Tattoo

GSC Wizard is **read-only reporting**. It does not install tags. Your site already sends events via `G-XLXNGGW7SX` (gtag) and `GTM-TZTQSQBB`. This guide connects that data to Search Console inside GSC Wizard and Cursor.

## 1. GA4 Admin — mark key events (required)

In [GA4 Admin](https://analytics.google.com/) → **Data display** → **Events**, toggle **Mark as key event** only for:

| Event | Role in GSC Wizard |
|-------|-------------------|
| `booking_submit` | **Primary conversion** — use in `get_ga4_key_events` |
| `generate_lead` | Optional duplicate of verified lead (GA4 recommended) |
| `phone_click` | Call intent |
| `text_click` | SMS intent |
| `email_click` | Email intent |
| `directions_click` | Maps / visit intent |
| `appointment_cta_click` | Book CTA clicks |

**Leave OFF as key events:** `page_view`, `session_start`, `scroll_depth`, `booking_view`, `booking_start`, `booking_submit_attempt`, `book_click`, `form_start`, `call_click`, `ads_conversion_Submit_lead_form_1` (fix GTM first).

Source of truth: `docs/analytics-event-contract.md` and `siteData/analytics.json`.

### Verify tags fire once

1. Open `https://www.workofarttattoo.com/appointments/?debug_analytics=1`
2. GA4 **DebugView** → confirm one `booking_view` per session, one `booking_submit` only after real success
3. Click phone link on homepage → one `phone_click` (not double `call_click` + `phone_click` counted as two key events — only mark `phone_click`)

## 2. GSC Wizard web app — link Search Console + GA4

1. Sign in at [gscwizard.com](https://www.gscwizard.com/)
2. Add / confirm property: **`https://www.workofarttattoo.com/`** (www + trailing slash matches canonical)
3. **Connect Google Analytics** → grant `analytics.readonly` (read-only)
4. **Couple GA4 property** → pick the property that receives measurement ID **`G-XLXNGGW7SX`**
5. Open **GA4 reports** tab — confirm sessions, key events, and event breakdown appear
6. Use **Blended landing pages** (or MCP `get_blended_landing_pages`) to join GSC clicks with GA4 sessions/conversions

If key events show **0**, return to step 1 — GSC Wizard reads GA4 **key events**, not custom event names unless marked.

## 3. Cursor MCP — Search Console + GA4 in chat

1. In GSC Wizard: **Settings → API keys** → create key (scope: read)
2. Copy `.cursor/mcp.json.example` → `.cursor/mcp.json` (project root, **gitignored**)
3. Replace `REPLACE_WITH_GSCW_API_KEY` with your `gscw_live_…` key
4. Restart Cursor → **Settings → MCP** → enable **gsc-wizard**

Example questions once connected:

- “Blended report: which landing pages have high GSC clicks but low `booking_submit`?”
- “Key events for `booking_submit` by channel last 28 days”
- “Compare organic clicks vs GA4 sessions for `/piercing-guide-las-vegas/`”

MCP endpoint: `https://mcp.gscwizard.com/mcp`

## 4. GTM — align Ads tag with site events (optional but recommended)

Container **`GTM-TZTQSQBB`**:

- Map Google Ads conversion to **`booking_submit`** or dataLayer **`woa_verified_lead`**
- Do **not** map to `booking_view`, `booking_start`, or `ads_conversion_Submit_lead_form_1` until remapped

## 5. Event ↔ tag map (site implementation)

| User action | GA4 event | GTM / gtag |
|-----------|-----------|------------|
| Successful booking form | `booking_submit`, `generate_lead` | gtag via `woa_ga4_conversions.py` |
| Book link click | `booking_start`, `appointment_cta_click`, `book_click` | same |
| Phone tap | `phone_click` (+ legacy `call_click`) | same |
| SMS tap | `text_click` | same |
| Email tap | `email_click` | same |
| Maps tap | `directions_click` | same |
| Appointments page (1/session) | `booking_view` | same — **not** a key event |

Implementation: `inject_ga4_conversions.py` → every public `code.html`.

## 6. Troubleshooting

| Symptom | Fix |
|---------|-----|
| GSC Wizard shows GA4 but key events = 0 | Mark `booking_submit` as key event in GA4 Admin |
| Blended pages mismatch | Use `https://www.workofarttattoo.com/` property; paths must match canonical trailing-slash URLs |
| MCP “not configured” | Couple GA4 property to site in GSC Wizard app first |
| Double conversions | Turn off duplicate key events; dedupe already in site code for `booking_submit` |
| AI traffic empty | Normal if referrers are google/organic; AI Overviews have no distinct referrer |

Run locally: `python3 tools/print_gsc_wizard_event_map.py`
