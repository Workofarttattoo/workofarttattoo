#!/usr/bin/env python3
"""Add the guide email/SMS capture block to the published code.html sources."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARKER = 'data-woa-guide-lead="1"'
SECTION_RE = re.compile(
    r'<section\s+data-woa-guide-lead="1"[\s\S]*?</section>\s*',
    re.IGNORECASE,
)
# The published pricing form puts class before the marker, so SECTION_RE misses
# it and a later inject appends a second First Tattoo Decision Guide form.
ANY_LEAD_SECTION_RE = re.compile(
    r'<section\b[^>]*\bdata-woa-guide-lead="1"[\s\S]*?</section>\s*',
    re.IGNORECASE,
)
PRICING_FOLDER = "how_much_do_tattoos_cost_in_las_vegas_authority_guide"

# Public folder, offer id. Alias folders are listed with their source so both HTML copies carry the form.
PAGES: dict[str, str] = {
    "tattoo-aftercare-desert-climate": "desert-aftercare",
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": "desert-aftercare",
    "knowledge/vegas-tattoo-aftercare-desert-climate": "desert-aftercare",
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide": "first-tattoo",
    "how-to-choose-a-tattoo-artist": "first-tattoo",
    "how_to_choose_a_tattoo_artist_master_selection_guide_2": "first-tattoo",
    "start_here": "first-tattoo",
    "healed_tattoo_gallery_las_vegas": "healed-realism",
    "realism-tattoos-las-vegas": "healed-realism",
    "realism_tattoos_las_vegas_master_authority_guide": "healed-realism",
    "cover-up-tattoos-las-vegas": "healed-realism",
}

OFFERS: dict[str, dict[str, str]] = {
    "desert-aftercare": {
        "name": "Vegas Desert Aftercare Checklist",
        "file": "/downloads/vegas-desert-aftercare-checklist.pdf",
        "intro": (
            "Email the studio and unlock the Vegas desert aftercare checklist on this page. "
            "Add a mobile number if you want a text back. The request includes the page you sent it from."
        ),
    },
    "healed-realism": {
        "name": "Healed Realism Portfolio",
        "file": "/downloads/healed-realism-portfolio.pdf",
        "intro": (
            "Email the studio and unlock the healed realism portfolio sheet on this page. "
            "Add a mobile number if you want a text back. The request includes the page you sent it from."
        ),
    },
    "first-tattoo": {
        "name": "First Tattoo Decision Guide",
        "file": "/downloads/first-tattoo-decision-guide.pdf",
        "intro": (
            "Email the studio and unlock the first tattoo decision guide on this page. "
            "Add a mobile number if you want a text back. The request includes the page you sent it from."
        ),
    },
}

SCRIPT = r"""<script data-woa-guide-lead-script="1">
(function () {
  var section = document.currentScript && document.currentScript.closest("[data-woa-guide-lead]");
  if (!section || section.getAttribute("data-woa-guide-ready") === "1") return;
  section.setAttribute("data-woa-guide-ready", "1");
  var form = section.querySelector("form");
  var thanks = section.querySelector("[data-woa-guide-lead-thanks]");
  var offer = section.getAttribute("data-woa-guide-offer") || "";
  var fileUrl = section.getAttribute("data-woa-guide-file") || "";
  var guideName = section.getAttribute("data-woa-guide-name") || offer;
  var sentThisView = false;

  function trackAllowed() {
    var query = location.search || "";
    if (query.indexOf("debug_analytics=1") >= 0) return true;
    if (navigator.webdriver) return false;
    var ua = navigator.userAgent || "";
    if (/HeadlessChrome|Lighthouse|PageSpeed|WOA-Deploy-Verifier|Google-InspectionTool/i.test(ua)) return false;
    try {
      if (window.sessionStorage && window.sessionStorage.getItem("woa_analytics_opt_out") === "1") return false;
    } catch (e) {}
    return true;
  }

  function send(name, params) {
    if (!trackAllowed()) return;
    var payload = {
      event_source: "woa_site",
      page_path: location.pathname || "/",
      page_location: (location.href || "").split("#")[0],
      page_title: document.title,
      guide_offer: offer,
      guide_name: guideName,
      source_page: location.pathname || "/"
    };
    Object.keys(params || {}).forEach(function (key) { payload[key] = params[key]; });
    if (typeof window.gtag === "function") window.gtag("event", name, payload);
    window.dataLayer = window.dataLayer || [];
    var layerEvent = { event: "woa_" + name };
    Object.keys(payload).forEach(function (key) { layerEvent[key] = payload[key]; });
    window.dataLayer.push(layerEvent);
  }

  send("guide_view", { guide_file: fileUrl });

  function reveal() {
    if (form) {
      form.classList.add("hidden");
      form.setAttribute("hidden", "");
    }
    if (thanks) {
      thanks.hidden = false;
      thanks.classList.remove("hidden");
    }
  }

  try {
    var params = new URLSearchParams(location.search || "");
    if (params.get("guide_lead") === "1") {
      reveal();
      params.delete("guide_lead");
      var rest = params.toString();
      history.replaceState(null, "", location.pathname + (rest ? "?" + rest : "") + location.hash);
    }
  } catch (e) {}

  if (!form) return;
  var source = form.querySelector('[name="source_page"]');
  var subject = form.querySelector('[name="_subject"]');
  var nextField = form.querySelector('[name="_next"]');
  var path = location.pathname || "/";
  if (source) source.value = path;
  if (subject) subject.value = "[Guide] " + guideName + " — " + path;
  if (nextField) nextField.value = "https://www.workofarttattoo.com" + path + "?guide_lead=1";

  form.addEventListener("submit", function (event) {
    if (typeof form.checkValidity === "function" && !form.checkValidity()) return;
    event.preventDefault();
    var honey = form.querySelector('[name="_woa_hp"]');
    if (honey && honey.value) return;
    if (form.getAttribute("data-woa-lead-pending") === "1" || sentThisView) return;
    form.setAttribute("data-woa-lead-pending", "1");

    function succeed() {
      if (sentThisView) return;
      sentThisView = true;
      form.setAttribute("data-woa-lead-pending", "0");
      reveal();
      send("guide_lead_submit", {
        form_id: "woa-guide-lead",
        form_destination: "formsubmit",
        source_page: (source && source.value) || path
      });
    }

    function fail() {
      form.setAttribute("data-woa-lead-pending", "0");
      var status = section.querySelector("[data-woa-guide-lead-status]");
      if (!status) return;
      status.hidden = false;
      status.classList.remove("hidden");
      status.textContent = "We could not send that just now. Call or text the studio at 725-224-1240.";
    }

    var host = location.hostname;
    if (host === "localhost" || host === "127.0.0.1" || location.protocol === "file:") {
      succeed();
      return;
    }

    fetch("https://formsubmit.co/ajax/thewhiteknight702@gmail.com", {
      method: "POST",
      headers: { Accept: "application/json" },
      body: new FormData(form)
    }).then(function (res) {
      if (!res.ok) throw new Error("formsubmit");
      return res.json();
    }).then(function () {
      succeed();
    }).catch(function () {
      fail();
    });
  });
})();
</script>
"""


def lead_section(offer_id: str) -> str:
    offer = OFFERS[offer_id]
    name = offer["name"]
    return f"""<section class="my-12 mx-auto max-w-3xl border border-outline-variant/40 bg-surface-container-high p-6 md:p-8" {MARKER} data-woa-guide-offer="{offer_id}" data-woa-guide-file="{offer["file"]}" data-woa-guide-name="{name}">
<p class="font-label-caps text-secondary uppercase tracking-widest text-xs mb-2">Free studio guide</p>
<h2 class="font-headline-md text-on-surface text-2xl md:text-3xl mb-3">{name}</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed mb-6">{offer["intro"]}</p>
<form action="https://formsubmit.co/thewhiteknight702@gmail.com" class="space-y-4" id="woa-guide-lead" method="POST">
<input name="_captcha" type="hidden" value="false"/>
<input name="_template" type="hidden" value="table"/>
<input name="_subject" type="hidden" value="[Guide] {name}"/>
<input name="_next" type="hidden" value=""/>
<input name="offer" type="hidden" value="{name}"/>
<input name="source_page" type="hidden" value=""/>
<input autocomplete="off" class="hidden" name="_woa_hp" tabindex="-1" type="text"/>
<label class="block space-y-2"><span class="font-label-caps text-[11px] uppercase tracking-widest text-on-surface-variant">Email *</span><input class="w-full bg-background border border-outline-variant px-4 py-3 text-on-surface rounded-sm focus:border-secondary outline-none" name="email" required="" type="email"/></label>
<label class="block space-y-2"><span class="font-label-caps text-[11px] uppercase tracking-widest text-on-surface-variant">Mobile for a text back (optional)</span><input class="w-full bg-background border border-outline-variant px-4 py-3 text-on-surface rounded-sm focus:border-secondary outline-none" name="phone" type="tel"/></label>
<button class="bg-secondary text-on-secondary px-8 py-3 font-label-caps text-label-caps uppercase tracking-widest" type="submit">Send me the guide</button>
</form>
<p class="hidden mt-4 text-sm text-on-surface-variant" data-woa-guide-lead-status hidden=""></p>
<div class="hidden mt-4" data-woa-guide-lead-thanks hidden="">
<p class="font-body-md text-on-surface mb-4">Thanks. Your guide is ready.</p>
<a class="inline-flex bg-secondary text-on-secondary px-8 py-3 font-label-caps text-label-caps uppercase tracking-widest" download="" href="{offer["file"]}">Download {name}</a>
</div>
{SCRIPT}
</section>
"""


def ensure_single_pricing_lead(html: str, offer_id: str) -> str:
    """Keep exactly one guide form on the tattoo pricing page."""
    matches = list(ANY_LEAD_SECTION_RE.finditer(html))
    if not matches:
        return inject_html(html, offer_id)
    if len(matches) == 1:
        return html
    first_end = matches[0].end()
    return html[:first_end] + ANY_LEAD_SECTION_RE.sub("", html[first_end:])


def inject_html(html: str, offer_id: str) -> str:
    block = lead_section(offer_id) + "\n"
    cleaned = SECTION_RE.sub("", html)
    if "</main>" in cleaned:
        return cleaned.replace("</main>", block + "</main>", 1)
    body = cleaned.rfind("</body>")
    if body >= 0:
        return cleaned[:body] + block + cleaned[body:]
    return cleaned + block


def target_files() -> list[tuple[Path, str]]:
    found: list[tuple[Path, str]] = []
    for folder, offer_id in PAGES.items():
        directory = ROOT / folder
        for name in ("code.html", "index.html"):
            path = directory / name
            if path.is_file():
                found.append((path, offer_id))
    return found


def main() -> int:
    changed = 0
    missing = 0
    for folder in PAGES:
        if not (ROOT / folder).is_dir():
            missing += 1
            print(f"[missing] {folder}")
    for path, offer_id in target_files():
        raw = path.read_text(encoding="utf-8")
        if PRICING_FOLDER in path.parts:
            updated = ensure_single_pricing_lead(raw, offer_id)
        else:
            updated = inject_html(raw, offer_id)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ok] {path.relative_to(ROOT)} ({offer_id})")
    print(f"Done: {changed} file(s), {missing} missing folder(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
