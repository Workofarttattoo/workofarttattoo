(function () {
  "use strict";

  var BOOKING_EMAIL = "thewhiteknight702@gmail.com";
  var PHP_ENDPOINT = "/appointments/booking-mail.php";
  var FORMSUBMIT_ENDPOINT = "https://formsubmit.co/ajax/" + encodeURIComponent(BOOKING_EMAIL);

  var root = document.getElementById("woa-booking-app");
  if (!root) return;

  var tabs = root.querySelectorAll("[data-woa-service-tab]");
  var panels = root.querySelectorAll("[data-woa-service-panel]");
  var statusEl = root.querySelector("#woa-booking-status");
  var tattooForm = root.querySelector("#woa-form-tattoo");
  var piercingForm = root.querySelector("#woa-form-piercing");
  var activeService = "tattoo";

  function setStatus(kind, text) {
    if (!statusEl) return;
    statusEl.hidden = false;
    statusEl.className =
      "rounded-sm border px-4 py-3 text-sm " +
      (kind === "ok"
        ? "border-secondary/40 bg-secondary/10 text-on-surface"
        : kind === "err"
          ? "border-error/50 bg-error-container/30 text-on-error-container"
          : "border-outline-variant bg-surface-container-high text-on-surface-variant");
    statusEl.textContent = text;
  }

  function clearStatus() {
    if (statusEl) {
      statusEl.hidden = true;
      statusEl.textContent = "";
    }
  }

  function showService(service) {
    activeService = service;
    tabs.forEach(function (btn) {
      var on = btn.getAttribute("data-woa-service-tab") === service;
      btn.setAttribute("aria-selected", on ? "true" : "false");
      btn.classList.toggle("bg-secondary", on);
      btn.classList.toggle("text-on-secondary", on);
      btn.classList.toggle("border-secondary", on);
      btn.classList.toggle("text-on-surface-variant", !on);
      btn.classList.toggle("border-outline-variant", !on);
    });
    panels.forEach(function (panel) {
      var on = panel.getAttribute("data-woa-service-panel") === service;
      panel.hidden = !on;
      panel.classList.toggle("hidden", !on);
    });
  }

  tabs.forEach(function (btn) {
    btn.addEventListener("click", function () {
      showService(btn.getAttribute("data-woa-service-tab"));
      clearStatus();
    });
  });

  function formToObject(form) {
    var data = {};
    new FormData(form).forEach(function (value, key) {
      if (data[key] !== undefined) {
        if (!Array.isArray(data[key])) data[key] = [data[key]];
        data[key].push(value);
      } else {
        data[key] = value;
      }
    });
    data.service_type = form.id === "woa-form-piercing" ? "piercing" : "tattoo";
    return data;
  }

  function safeSlug(value) {
    return String(value || "")
      .toLowerCase()
      .replace(/&/g, " and ")
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_+|_+$/g, "")
      .slice(0, 80);
  }

  function safeArtist(value) {
    var slug = safeSlug(value);
    if (!slug || slug === "no_preference") return "no_preference";
    if (slug.indexOf("joshua") >= 0) return "joshua";
    if (slug.indexOf("katelyn") >= 0 || slug.indexOf("katie") >= 0) return "katelyn";
    if (slug.indexOf("teralyn") >= 0) return "teralyn";
    return slug;
  }

  function dispatchBookingSuccess(form, data, origin) {
    var isPiercing = form.id === "woa-form-piercing";
    var detail = {
      conversion_origin: origin,
      form_id: form.id,
      form_destination: origin === "php_success" ? "php_mailer" : "formsubmit_ajax",
      service_category: isPiercing ? "piercing" : "tattoo",
      service_type: isPiercing
        ? safeSlug(data.piercing_type || "piercing")
        : safeSlug(data.tattoo_request_type || "tattoo"),
      artist: safeArtist(isPiercing ? data.preferred_piercer : data.preferred_artist),
    };
    try {
      document.dispatchEvent(new CustomEvent("woa_booking_submit_success", { detail: detail }));
    } catch (e) {
      var event = document.createEvent("CustomEvent");
      event.initCustomEvent("woa_booking_submit_success", true, true, detail);
      document.dispatchEvent(event);
    }
  }

  function buildFormSubmitBody(data) {
    var subject =
      data.service_type === "piercing"
        ? "[Piercing] Appointment request — " + (data.full_name || "Client")
        : "[Tattoo] Appointment request — " + (data.full_name || "Client");
    var body = Object.keys(data)
      .filter(function (k) {
        return k.indexOf("_") !== 0 && data[k];
      })
      .map(function (k) {
        return k + ": " + data[k];
      })
      .join("\n");
    return {
      _subject: subject,
      _template: "box",
      _captcha: "false",
      message: body,
      name: data.full_name,
      email: data.email,
      phone: data.phone,
    };
  }

  function submitFormSubmit(data) {
    return fetch(FORMSUBMIT_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(buildFormSubmitBody(data)),
    }).then(function (res) {
      if (!res.ok) throw new Error("FormSubmit failed");
      return res.json();
    });
  }

  function submitPhp(form) {
    return fetch(PHP_ENDPOINT, {
      method: "POST",
      body: new FormData(form),
    }).then(function (res) {
      return res.json().then(function (json) {
        if (!res.ok || !json.ok) {
          var err = new Error(json.error || "Send failed");
          err.fallback = !!json.fallback;
          throw err;
        }
        return json;
      });
    });
  }

  function onSubmit(form, e) {
    e.preventDefault();
    clearStatus();
    var btn = form.querySelector("[type=submit]");
    if (btn) {
      btn.disabled = true;
      btn.setAttribute("aria-busy", "true");
    }
    setStatus("info", "Sending your request…");

    var data = formToObject(form);

    submitPhp(form)
      .then(function (json) {
        setStatus("ok", json.message);
        dispatchBookingSuccess(form, data, "php_success");
        form.reset();
        showService(activeService);
      })
      .catch(function (err) {
        return submitFormSubmit(data)
          .then(function () {
            setStatus(
              "ok",
              "Thank you — your request was sent. Our team will reply to " +
                data.email +
                " shortly."
            );
            dispatchBookingSuccess(form, data, "formsubmit_ajax_success");
            form.reset();
          })
          .catch(function () {
            setStatus(
              "err",
              err.message ||
                "Could not send online. Please call (725) 224-1240 or email " +
                  BOOKING_EMAIL +
                  "."
            );
          });
      })
      .finally(function () {
        if (btn) {
          btn.disabled = false;
          btn.removeAttribute("aria-busy");
        }
      });
  }

  if (tattooForm) tattooForm.addEventListener("submit", onSubmit.bind(null, tattooForm));
  if (piercingForm) piercingForm.addEventListener("submit", onSubmit.bind(null, piercingForm));

  showService("tattoo");
})();
