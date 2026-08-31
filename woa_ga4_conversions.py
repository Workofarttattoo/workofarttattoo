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
  var PIERCING_ROUTE_RE = /(piercing|katelyn|helix|conch|tragus|daith|rook|septum|nostril|labret|philtrum|navel|nipple|industrial)/i;

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

  function storageSetOnce(key, value) {{
    if (!storageGet(key)) storageSet(key, value);
  }}

  function safeSlug(value) {{
    return String(value || "")
      .toLowerCase()
      .replace(/&/g, " and ")
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_+|_+$/g, "")
      .slice(0, 80);
  }}

  storageSetOnce("woa_first_landing_page", location.pathname || "/");

  function firstLandingPage() {{
    return storageGet("woa_first_landing_page") || location.pathname || "/";
  }}

  function bookingOriginPage() {{
    return storageGet("woa_booking_origin_page") || location.pathname || "/";
  }}

  function serviceInterestFromPath(path) {{
    var value = String(path || location.pathname || "");
    if (PIERCING_ROUTE_RE.test(value)) return "piercing";
    if (/(fine[-_]?line|script|floral|small[-_]?tattoo|teralyn)/i.test(value)) return "fine_line_tattoo";
    if (/(realism|portrait|black[-_]?grey|blackwork|joshua)/i.test(value)) return "tattoo";
    if (/(cover[-_]?up|flash|walk[-_]?in|tattoo)/i.test(value)) return "tattoo";
    return "unknown";
  }}

  function attributionParams(params) {{
    return assign(
      {{
        landing_page: firstLandingPage(),
        origin_page: bookingOriginPage(),
        service_interest: serviceInterestFromPath(bookingOriginPage()),
      }},
      params || {{}}
    );
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

  function formValue(form, names) {{
    for (var i = 0; i < names.length; i += 1) {{
      var field = form.querySelector('[name="' + names[i] + '"]');
      if (field && field.value) return field.value;
    }}
    return "";
  }}

  function serviceTypeFromForm(form, id) {{
    var service = serviceFromFormId(id);
    if (service === "piercing") return safeSlug(formValue(form, ["piercing_type"]) || "piercing");
    return safeSlug(formValue(form, ["tattoo_request_type"]) || "tattoo");
  }}

  function artistFromForm(form, id) {{
    var raw = formValue(form, serviceFromFormId(id) === "piercing" ? ["preferred_piercer"] : ["preferred_artist"]);
    var slug = safeSlug(raw);
    if (!slug || slug === "no_preference") return "no_preference";
    if (slug.indexOf("joshua") >= 0) return "joshua";
    if (slug.indexOf("katelyn") >= 0 || slug.indexOf("katie") >= 0) return "katelyn";
    if (slug.indexOf("teralyn") >= 0) return "teralyn";
    return slug;
  }}

  function bookingParamsFromForm(form, id, extras) {{
    var service = serviceFromFormId(id);
    return attributionParams(assign(
      {{
        form_id: id,
        form_destination: "formsubmit",
        service_category: service,
        service_type: serviceTypeFromForm(form, id),
        artist: artistFromForm(form, id),
      }},
      extras || {{}}
    ));
  }}

  function closestPromo(el) {{
    return el && el.closest ? el.closest("[data-woa-piercing-special]") : null;
  }}

  function promoParams(link, action) {{
    var promo = closestPromo(link);
    var params = {{
      link_url: link ? link.getAttribute("href") || "" : "",
      click_text: linkText(link),
      click_location: clickLocation(link),
      service_type: "piercing",
      promo_action: action || (link ? link.getAttribute("data-woa-promo-click") || "" : ""),
      promo_context: link ? link.getAttribute("data-woa-promo-context") || "" : "",
      promotion_id: "",
    }};
    if (promo) {{
      params.promo_id = promo.getAttribute("data-woa-promo-id") || "";
      params.promotion_id = params.promo_id;
      params.promo_campaign = promo.getAttribute("data-woa-promo-campaign") || "";
      params.promo_variant = promo.getAttribute("data-woa-promo-variant") || "";
    }}
    return attributionParams(params);
  }}

  function persistPiercingAttribution(link) {{
    var params = promoParams(link, "booking_start");
    storageSet("woa_booking_origin_page", location.pathname || "/");
    storageSet("woa_piercing_attribution", JSON.stringify({{
      promo_id: params.promo_id || "",
      promotion_id: params.promotion_id || params.promo_id || "",
      promo_campaign: params.promo_campaign || "",
      promo_context: params.promo_context || "",
      page_path: location.pathname,
      landing_page: firstLandingPage(),
      origin_page: location.pathname || "/",
    }}));
    return params;
  }}

  function storedPiercingAttribution() {{
    try {{
      var raw = storageGet("woa_piercing_attribution");
      return raw ? JSON.parse(raw) : {{}};
    }} catch (e) {{
      return {{}};
    }}
  }}

  function observePiercingDeals() {{
    var blocks = Array.prototype.slice.call(document.querySelectorAll("[data-woa-piercing-special]"));
    if (!blocks.length) return;
    var seen = {{}};
    function view(block) {{
      var id = block.getAttribute("data-woa-promo-id") || "";
      if (!id || seen[id + location.pathname]) return;
      seen[id + location.pathname] = true;
      var params = attributionParams({{
        service_type: "piercing",
        promo_id: id,
        promotion_id: id,
        promo_campaign: block.getAttribute("data-woa-promo-campaign") || "",
        promo_variant: block.getAttribute("data-woa-promo-variant") || "",
      }});
      send("piercing_special_view", params);
      send("piercing_deal_view", assign({{ legacy_event: true }}, params));
    }}
    if (!("IntersectionObserver" in window)) {{
      blocks.forEach(view);
      return;
    }}
    var observer = new IntersectionObserver(function (entries) {{
      entries.forEach(function (entry) {{
        if (entry.isIntersecting) {{
          view(entry.target);
          observer.unobserve(entry.target);
        }}
      }});
    }}, {{ threshold: 0.35 }});
    blocks.forEach(function (block) {{ observer.observe(block); }});
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
      if (h.indexOf("/appointments") >= 0) {{
        storageSet("woa_booking_origin_page", location.pathname || "/");
      }}

      if (link.hasAttribute("data-woa-promo-click")) {{
        var specialParams = promoParams(link);
        send("piercing_special_click", specialParams);
        send("piercing_deal_click", assign({{ legacy_event: true }}, specialParams));
      }}
      if (link.hasAttribute("data-woa-piercing-booking-start") || (h.indexOf("/appointments") >= 0 && closestPromo(link))) {{
        send("piercing_booking_start", persistPiercingAttribution(link));
      }}
      if (link.hasAttribute("data-woa-katelyn-profile-click")) {{
        send("piercing_katelyn_click", attributionParams(assign({{ service_type: "piercing" }}, base)));
        send("piercing_katelyn_profile_click", attributionParams(assign({{ service_type: "piercing", legacy_event: true }}, base)));
      }}
      if (link.hasAttribute("data-woa-piercing-jewelry-click")) {{
        send("piercing_jewelry_click", attributionParams(assign({{ service_type: "piercing" }}, base)));
      }}
      if (link.hasAttribute("data-woa-piercing-directions-click")) {{
        send("piercing_directions_click", attributionParams(assign({{ service_type: "piercing" }}, base)));
      }}
      if (link.hasAttribute("data-woa-start-here-selection")) {{
        send("start_here_selection", attributionParams(assign({{
          selection: link.getAttribute("data-woa-start-here-selection") || "",
          selection_link_type: link.getAttribute("data-woa-start-here-link-type") || "content",
        }}, base)));
      }}

      if (h.indexOf("tel:") === 0) {{
        if (PIERCING_ROUTE_RE.test(location.pathname) || closestPromo(link)) {{
          send("piercing_call_click", attributionParams(assign({{ service_type: "piercing" }}, base)));
          send("piercing_cta_click", attributionParams(assign({{ service_type: "piercing", cta_type: "call" }}, base)));
        }}
        send("call_click", base);
        return;
      }}
      if (h.indexOf("sms:") === 0 || link.hasAttribute("data-woa-piercing-text-click")) {{
        send("piercing_text_click", attributionParams(assign({{ service_type: "piercing" }}, base)));
        send("piercing_cta_click", attributionParams(assign({{ service_type: "piercing", cta_type: "text" }}, base)));
        return;
      }}
      if (h.indexOf("mailto:") === 0) {{
        send("email_click", base);
        return;
      }}
      if (h.indexOf("/appointments") >= 0) {{
        if (PIERCING_ROUTE_RE.test(location.pathname) || closestPromo(link) || link.hasAttribute("data-woa-piercing-booking-start")) {{
          send("piercing_cta_click", attributionParams(assign({{ service_type: "piercing", cta_type: "book" }}, base)));
        }}
        send("booking_start", attributionParams(assign({{
          service_category: serviceInterestFromPath(location.pathname) === "piercing" ? "piercing" : "unknown",
          service_type: serviceInterestFromPath(location.pathname),
          source_action: "appointment_link_click",
        }}, base)));
        send("book_click", base);
        return;
      }}
      if (
        h.indexOf("google.com/maps") >= 0 ||
        h.indexOf("maps.app.goo.gl") >= 0 ||
        h.indexOf("g.page") >= 0 ||
        h.indexOf("maps.google.com") >= 0
      ) {{
        if (PIERCING_ROUTE_RE.test(location.pathname) || closestPromo(link)) {{
          send("piercing_directions_click", attributionParams(assign({{ service_type: "piercing" }}, base)));
          send("piercing_cta_click", attributionParams(assign({{ service_type: "piercing", cta_type: "directions" }}, base)));
        }}
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
      var params = bookingParamsFromForm(form, id);
      send("booking_start", params);
      send("form_start", assign({{ legacy_event: true }}, params));
      if (params.service_category === "piercing") send("piercing_booking_start", assign(storedPiercingAttribution(), params));
    }}
    ["focusin", "input", "change"].forEach(function (eventName) {{
      form.addEventListener(eventName, markStarted, true);
    }});
    form.addEventListener("submit", function () {{
      send("booking_submit_attempt", bookingParamsFromForm(form, id, {{ conversion_origin: "submit_attempt" }}));
    }});
  }});

  observePiercingDeals();

  if (/^\\/appointments\\/?$/.test(location.pathname)) {{
    send("booking_view", attributionParams({{ interface_present: !!document.getElementById("woa-booking-app") }}), {{ allowRepeat: true }});
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
      var submitParams = attributionParams(assign(storedPiercingAttribution(), {{
        conversion_origin: "formsubmit_redirect",
        service_category: sent,
        service_type: sent,
        form_destination: "formsubmit",
      }}));
      send("booking_submit", submitParams);
      send("booking_complete", assign({{ legacy_event: true }}, submitParams));
      if (sent === "piercing") send("piercing_booking_submit", submitParams);
    }}
  }}

  document.addEventListener("woa_booking_submit_success", function (e) {{
    var detail = (e && e.detail) || {{}};
    var service = detail.service_category === "piercing" ? "piercing" : detail.service_category === "tattoo" ? "tattoo" : "unknown";
    var successParams = attributionParams(assign(storedPiercingAttribution(), {{
      conversion_origin: detail.conversion_origin || "ajax_success",
      form_id: detail.form_id || "",
      form_destination: detail.form_destination || "",
      service_category: service,
      service_type: safeSlug(detail.service_type || service),
      artist: safeSlug(detail.artist || "no_preference"),
    }}));
    send("booking_submit", successParams);
    if (service === "piercing") send("piercing_booking_submit", successParams);
  }});

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
