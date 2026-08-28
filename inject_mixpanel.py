#!/usr/bin/env python3
"""Inject Mixpanel analytics snippet into all public HTML exports."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_PARTS = frozenset({"skipped_upload_build", "artists_raw", ".git"})

MIXPANEL_SNIPPET = """<script type="text/javascript">
  (function(e,c){if(!c.__SV){var l,h;window.mixpanel=c;c._i=[];c.init=function(q,r,f){function t(d,a){var g=a.split(".");2==g.length&&(d=d[g[0]],a=g[1]);d[a]=function(){d.push([a].concat(Array.prototype.slice.call(arguments,0)))}}var b=c;"undefined"!==typeof f?b=c[f]=[]:f="mixpanel";b.people=b.people||[];b.toString=function(d){var a="mixpanel";"mixpanel"!==f&&(a+="."+f);d||(a+=" (stub)");return a};b.people.toString=function(){return b.toString(1)+".people (stub)"};l="disable time_event track track_pageview track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking start_batch_senders start_session_recording stop_session_recording people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split(" ");
  for(h=0;h<l.length;h++)t(b,l[h]);var n="set set_once union unset remove delete".split(" ");b.get_group=function(){function d(p){a[p]=function(){b.push([g,[p].concat(Array.prototype.slice.call(arguments,0))])}}for(var a={},g=["get_group"].concat(Array.prototype.slice.call(arguments,0)),m=0;m<n.length;m++)d(n[m]);return a};c._i.push([q,r,f])};c.__SV=1.2;var k=e.createElement("script");k.type="text/javascript";k.async=!0;k.src="undefined"!==typeof MIXPANEL_CUSTOM_LIB_URL?MIXPANEL_CUSTOM_LIB_URL:"file:"===
  e.location.protocol&&"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js".match(/^\\//)?"https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js":"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";e=e.getElementsByTagName("script")[0];e.parentNode.insertBefore(k,e)}})(document,window.mixpanel||[])

  mixpanel.init('db89dd14246e223536112f4ba3d5cbc0', {
    autocapture: true,
    record_sessions_percent: 100,
  })

</script>"""

MIXPANEL_MARKER = "mixpanel.init('db89dd14246e223536112f4ba3d5cbc0'"
MIXPANEL_BLOCK_RE = re.compile(
    r'<script type="text/javascript">\s*\(function\(e,c\).*?mixpanel\.init\([^)]+\)[^<]*</script>\s*',
    re.DOTALL,
)


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    seen: set[str] = set()

    def add(p: Path) -> None:
        if not p.is_file():
            return
        if any(part in SKIP_PARTS for part in p.parts):
            return
        key = str(p.resolve())
        if key in seen:
            return
        seen.add(key)
        out.append(p)

    for p in sorted(ROOT.glob("*/code.html")):
        if not p.parent.name.startswith("."):
            add(p)
    add(ROOT / "code.html")
    for p in sorted((ROOT / "artists_build").glob("*.html")):
        add(p)
    add(ROOT / "artists" / "code.html")
    add(ROOT / "appointments" / "code.html")
    add(ROOT / "appointments" / "woa-booking-forms.html")
    return out


def inject_mixpanel(html: str) -> str:
    if MIXPANEL_MARKER in html:
        return html
    if "</head>" not in html:
        return html
    return html.replace("</head>", f"{MIXPANEL_SNIPPET}\n</head>", 1)


def normalize_mixpanel(html: str) -> str:
    """Replace stale Mixpanel blocks with the canonical snippet."""
    if MIXPANEL_MARKER not in html:
        return inject_mixpanel(html)
    cleaned = MIXPANEL_BLOCK_RE.sub("", html, count=1)
    if MIXPANEL_MARKER in cleaned:
        return cleaned
    return inject_mixpanel(cleaned)


def main() -> int:
    changed = 0
    for path in iter_html_files():
        raw = path.read_text(encoding="utf-8", errors="replace")
        updated = normalize_mixpanel(raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ok] {path.relative_to(ROOT)}")
    print(f"Done: {changed} file(s) with Mixpanel")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
