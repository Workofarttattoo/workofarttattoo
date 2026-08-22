#!/usr/bin/env python3
"""GA4 conversion + engagement events for Work of Art static pages."""

from __future__ import annotations

import re

MARKER = 'data-woa-ga4-conversions="1"'

GA4_CONVERSION_SCRIPT = f"""<script {MARKER} type="text/javascript">
(function () {{
  "use strict";
  var EVENT_SOURCE = "woa_site";
  var DEDUPE_MS = 1200;
  var sentRecently = {{}};

  function assign(target, source) {{
    Object.keys(source || {{}}).forEach(function (key) {{
      target[key] = source[key];
    }});
    return target;
  }}

  function now() {{
    return Date.now ? Date.now() : new Date().getTime();
  }}

  function debugMode() {{
    return (location.search || "").indexOf("debug_analytics=1") >= 0;
  }}

  function storageGet(key) {{
    try {{
      return window.sessionStorage ? window.sessionStorage.getItem(key) : null;
    }} catch (e) {{
      return null;
    }}
  }}

  function storageSet(key, value) {{
    try {{
      if (window.sessionStorage) window.sessionStorage.setItem(key, value);
    }} catch (e) {{}}
  }}

  function baseParams(params) {{
    var out = {{
      event_source: EVENT_SOURCE,
      page_path: location.pathname,
      page_location: location.href.split("#")[0],
      page_title: document.title,
    }};
    if (debugMode()) out.debug_mode = true;
    return assign(out, params || {{}});
  }}

  function eventKey(name, params) {{
    return [
      name,
      params.page_path || "",
      params.link_url || "",
      params.form_id || "",
      params.service_type || "",
      params.percent || "",
    ].join("|");
  }}

  function pushDataLayer(name, params) {{
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(assign({{ event: "woa_" + name }}, params || {{}}));
  }}

  function send(name, params, options) {{
    var payload = baseParams(params);
    var key = eventKey(name, payload);
    var t = now();

    if (!(options && options.allowRepeat)) {{
      if (sentRecently[key] && t - sentRecently[key] < DEDUPE_MS) return;
      sentRecently[key] = t;
    }}

    if (typeof window.gtag === "function") {{
      window.gtag("event", name, payload);
    }}
    pushDataLayer(name, payload);
  }}

  function linkFromClick(target) {{
    var el = target && target.closest ? target.closest("a") : null;
    return el;
  }}

  function linkText(el) {{
    return ((el && el.textContent) || "").replace(/\\s+/g, " ").trim().slice(0, 80);
  }}

  function clickLocation(el) {{
    if (!el || !el.closest) return "content";
    if (el.closest("[data-woa-sticky-book]")) return "sticky_book";
    if (el.closest("[data-woa-mobile-panel]")) return "mobile_nav";
    if (el.closest("[data-woa-top-shell]")) return "header";
    if (el.closest("footer")) return "footer";
    if (el.closest(".woa-hero, .hero, #hero, [data-woa-hero]")) return "hero";
    return "content";
  }}

  function serviceFromFormId(id) {{
    return id && id.indexOf("piercing") >= 0 ? "piercing" : "tattoo";
  }}

  document.addEventListener(
    "click",
    function (e) {{
      var link = linkFromClick(e.target);
      var href = link ? link.getAttribute("href") || "" : "";
      if (!href) return;
      var h = href.toLowerCase();
      var base = {{
        link_url: href,
        click_text: linkText(link),
        click_location: clickLocation(link),
      }};

      if (h.indexOf("tel:") === 0) {{
        send("call_click", base);
        return;
      }}
      if (h.indexOf("mailto:") === 0) {{
        send("email_click", base);
        return;
      }}
      if (h.indexOf("/appointments") >= 0) {{
        send("book_click", base);
        return;
      }}
      if (
        h.indexOf("google.com/maps") >= 0 ||
        h.indexOf("maps.app.goo.gl") >= 0 ||
        h.indexOf("g.page") >= 0 ||
        h.indexOf("maps.google.com") >= 0
      ) {{
        send("directions_click", base);
        return;
      }}
      if (
        h.indexOf("review") >= 0 &&
        (h.indexOf("google") >= 0 || h.indexOf("g.page") >= 0)
      ) {{
        send("review_click", base);
      }}
    }},
    true
  );

  ["woa-form-tattoo", "woa-form-piercing"].forEach(function (id) {{
    var form = document.getElementById(id);
    if (!form) return;
    var started = false;
    function markStarted() {{
      if (started) return;
      started = true;
      send("form_start", {{
        form_id: id,
        service_type: serviceFromFormId(id),
      }});
    }}
    ["focusin", "input", "change"].forEach(function (eventName) {{
      form.addEventListener(eventName, markStarted, true);
    }});
    form.addEventListener("submit", function () {{
      send("booking_form_submit", {{
        form_id: id,
        form_destination: "formsubmit",
        service_type: serviceFromFormId(id),
      }});
    }});
  }});

  if (/^\\/appointments\\/?$/.test(location.pathname)) {{
    send("booking_page_view", {{}}, {{ allowRepeat: true }});
  }}

  var sent = "";
  try {{
    sent = new URLSearchParams(location.search || "").get("sent") || "";
  }} catch (e) {{
    var q = location.search || "";
    sent = q.indexOf("sent=piercing") >= 0 ? "piercing" : q.indexOf("sent=tattoo") >= 0 ? "tattoo" : "";
  }}
  if (sent === "tattoo" || sent === "piercing") {{
    var completeKey = "woa_booking_complete_" + sent + "_" + location.pathname;
    if (!storageGet(completeKey)) {{
      storageSet(completeKey, "1");
      send("booking_complete", {{
        conversion_origin: "formsubmit_redirect",
        service_type: sent,
      }});
    }}
  }}

  Array.prototype.forEach.call(document.querySelectorAll("iframe[src]"), function (iframe) {{
    var src = iframe.getAttribute("src") || "";
    if (!/(booking|appointment|formsubmit|calendly|fresha|squareup)/i.test(src)) return;
    iframe.addEventListener(
      "load",
      function () {{
        send("booking_iframe_loaded", {{ iframe_src: src }});
      }},
      {{ once: true }}
    );
  }});

  var depths = [25, 50, 75, 90];
  var fired = {{}};
  window.addEventListener(
    "scroll",
    function () {{
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      if (max <= 0) return;
      var pct = Math.round((window.scrollY / max) * 100);
      depths.forEach(function (d) {{
        if (pct >= d && !fired[d]) {{
          fired[d] = true;
          send("scroll_depth", {{ percent: d, page_path: location.pathname }});
        }}
      }});
    }},
    {{ passive: true }}
  );
}})();
</script>"""

BLOCK_RE = re.compile(
    rf"<script[^>]*{re.escape(MARKER)}[\s\S]*?</script>\s*",
    re.MULTILINE,
)


def inject_ga4_conversions(html: str) -> tuple[str, bool]:
    """Insert conversion listener after gtag is present."""
    has_google_tag = (
        "googletagmanager.com/gtag/js" in html
        or "googletagmanager.com/gtm.js" in html
        or "function gtag" in html
        or "dataLayer" in html
    )
    if not has_google_tag:
        return html, False

    block = GA4_CONVERSION_SCRIPT + "\n"
    if MARKER in html:
        updated = BLOCK_RE.sub(lambda _match: block, html, count=1)
        return updated, updated != html

    body_close = html.rfind("</body>")
    if body_close >= 0:
        return html[:body_close] + block + html[body_close:], True
    return html, False
