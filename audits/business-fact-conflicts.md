# Business Fact Conflicts

Generated: 2026-08-21T14:22:33

## Verified Source Of Truth

- Business: Work of Art Tattoo & Piercing
- Address: 2375 E. Tropicana Ave, Suite 3, Las Vegas, NV 89119
- Phone: (725) 224-1240
- Email: booking@workofarttattoo.com
- Google rating/reviews: 5.0 stars, hundreds of Google reviews
- Resident artist count: 3

## Business Fact Mismatches

- `business fact mismatch` in `fix_artist_roster_copy.py:125`: "Every tattoo at Work of Art is a collaboration with one of our two in-studio tattoo artists — Joshua Cole or Jay Jay — backed by a professional piercer, Katelyn Cole.",
- `business fact mismatch` in `remove_jay_jay_from_site.py:97`: ("one of our two in-studio tattoo artists — Joshua Cole or Jay Jay", "one of our two in-studio tattoo artists — Joshua Cole or Teralyn"),
- `business fact mismatch` in `fix_studio_nap.py:76`: "2375 E. Tropicana Ave, Suite 3<br/>Las Vegas, NV 89119",
- `business fact mismatch` in `fix_studio_nap.py:115`: ('"postalCode": "89119"', f'"postalCode": "{STUDIO_POSTAL_CODE}"'),
- `business fact mismatch` in `fix_studio_nap.py:195`: if "postalCode" in obj and obj["postalCode"] in ("89101", "89104"):

## Opening-Hours Statements For Manual Review

The brief did not provide a newly verified hours value, so these are inventoried instead of overwritten.

- `opening hours statement` in `woa_geo_pages.py:47`: "Daily 12 PM–12 AM hours align with evening consults around show schedules.",
- `opening hours statement` in `woa_geo_pages.py:80`: "Daily 12 PM–12 AM hours work for evening consults without late-night Strip booth pressure.",
- `opening hours statement` in `woa_geo_pages.py:145`: "Evening show + morning consult: our Mon–Thu hours start at 3 PM; book afternoon slots before doors.",
- `opening hours statement` in `fix_gsc_search_console_signals.py:54`: <h2 class="font-headline-md text-on-surface text-2xl">Piercing shop hours in Las Vegas: 12pm - 12am daily</h2>
- `opening hours statement` in `woa_nav_config.py:84`: STUDIO_HOURS_SUMMARY = "Daily 12 PM - 12 AM"
- `opening hours statement` in `woa_nav_config.py:87`: '<p class="text-on-surface-variant">DAILY</p><p>12:00 PM - 12:00 AM</p>'
- `opening hours statement` in `fix_site_footer.py:57`: <li>Daily: 12pm - 12am</li>
- `opening hours statement` in `inject_availability_urgency.py:20`: <p class="font-body-md text-on-surface m-0"><strong class="text-secondary">Availability:</strong> Katelyn — piercing during regular shop hours · Joshua — tattoo availability by request</p>
- `opening hours statement` in `woa_ai_crawl.py:263`: - Daily: 12:00 PM – 12:00 AM
- `opening hours statement` in `code.html:1652`: </div><div class="space-y-4"><h5 class="font-label-caps text-on-surface uppercase tracking-widest text-[11px]">Hours</h5><ul class="space-y-2 text-on-surface-variant text-[13px] font-body-md"><li class="">Daily: 12pm - 12am</li></ul></div>
- `opening hours statement` in `fix_studio_nap.py:120`: "<p>12:00 PM - 10:00 PM</p>\n"
- `opening hours statement` in `fix_studio_nap.py:122`: "<p>12:00 PM - 08:00 PM</p>\n"
- `opening hours statement` in `tattoo_shop_green_valley_henderson/code.html:506`: <p class="font-body-md text-on-surface-variant">Daily 12pm - 12am</p>
- `opening hours statement` in `tattoo_shop_near_allegiant_stadium_las_vegas/code.html:497`: <ul class="space-y-2 list-disc pl-5 marker:text-secondary"><li class="font-body-md text-on-surface-variant">Daily 12 PM–12 AM hours work for evening consults without late-night Strip booth pressure.</li><li class="font-body-md text-on-surface-variant">Piercing
- `opening hours statement` in `tattoo_shop_near_mgm_grand_las_vegas/code.html:497`: <ul class="space-y-2 list-disc pl-5 marker:text-secondary"><li class="font-body-md text-on-surface-variant">Strip walk-ins optimize turnover — we book consults and show healed portfolio photos before you commit.</li><li class="font-body-md text-on-surface-vari
- `opening hours statement` in `tattoo_shop_near_the_sphere_las_vegas/code.html:493`: <ul class="space-y-2 list-disc pl-5 marker:text-secondary"><li class="font-body-md text-on-surface-variant">Sphere parking is expensive and time-limited — park at our lot for consults instead.</li><li class="font-body-md text-on-surface-variant">Evening show +
- `opening hours statement` in `geo_hub_ai_source_of_truth_work_of_art/code.html:2258`: <span class="font-body-md text-body-md text-on-surface">12:00 PM - 12:00 AM</span>
- `opening hours statement` in `official_location_hours_contact/code.html:1896`: "text": "Daily 12pm - 12am. We are open seven days a week."
- `opening hours statement` in `official_location_hours_contact/code.html:2360`: <div class="grid grid-cols-2 gap-4"><p class="text-on-surface-variant">DAILY</p><p>12:00 PM - 12:00 AM</p></div>
- `opening hours statement` in `official_location_hours_contact/code.html:2430`: <p class="font-body-md text-on-surface-variant mt-4">Daily 12pm - 12am. We are open seven days a week.</p>
