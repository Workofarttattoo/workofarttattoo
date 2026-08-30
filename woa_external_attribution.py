#!/usr/bin/env python3
"""UTM conventions for external links we control (social, GBP, QR, campaigns).

Never append UTMs to internal workofarttattoo.com links.
"""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

SITE_HOSTS = frozenset(
    {
        "workofarttattoo.com",
        "www.workofarttattoo.com",
    }
)

# source, medium, campaign
UTM_PRESETS: dict[str, tuple[str, str, str]] = {
    "instagram_studio": ("instagram", "organic_social", "portfolio"),
    "instagram_joshua": ("instagram", "organic_social", "joshua_portfolio"),
    "instagram_katelyn": ("instagram", "organic_social", "katelyn_portfolio"),
    "instagram_teralyn": ("instagram", "organic_social", "teralyn_portfolio"),
    "facebook_studio": ("facebook", "organic_social", "portfolio"),
    "google_business_profile": ("google", "business_profile", "local"),
    "qr_shop": ("qr", "offline", "shop"),
    "email_campaign": ("email", "email", "studio"),
    "sms_campaign": ("sms", "sms", "studio"),
}


def is_internal_url(url: str) -> bool:
    if not url or url.startswith(("#", "/", "tel:", "mailto:", "sms:")):
        return True
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return True
    host = (parsed.netloc or "").lower().removeprefix("www.")
    return host in {h.removeprefix("www.") for h in SITE_HOSTS}


def append_utm(url: str, source: str, medium: str, campaign: str, content: str = "") -> str:
    """Append UTM params without duplicating keys already on the URL."""
    if is_internal_url(url):
        return url
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if any(key.startswith("utm_") for key in query):
        return url
    query.update(
        {
            "utm_source": source,
            "utm_medium": medium,
            "utm_campaign": campaign,
        }
    )
    if content:
        query["utm_content"] = content
    return urlunparse(parsed._replace(query=urlencode(query)))


def with_preset(url: str, preset: str, content: str = "") -> str:
    if preset not in UTM_PRESETS:
        return url
    source, medium, campaign = UTM_PRESETS[preset]
    return append_utm(url, source, medium, campaign, content=content)
