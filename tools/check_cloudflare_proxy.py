#!/usr/bin/env python3
"""Check whether production traffic hits Cloudflare (required for Bulk Redirects)."""

from __future__ import annotations

import socket
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from woa_canonical import CANONICAL_ORIGIN

HOST = CANONICAL_ORIGIN.replace("https://", "").replace("http://", "")
APEX = "workofarttattoo.com"
GITHUB_PAGES_HINTS = ("185.199.", "185.199")


def resolve(name: str) -> list[str]:
    try:
        infos = socket.getaddrinfo(name, 443, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        return [f"lookup failed: {exc}"]
    addrs = sorted({item[4][0] for item in infos})
    return addrs


def probe(url: str) -> dict[str, str]:
    req = urllib.request.Request(url, method="HEAD")
    req.add_header("User-Agent", "WOA-Cloudflare-Check/1.0")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return {
                "status": str(resp.status),
                "server": headers.get("server", ""),
                "cf_ray": headers.get("cf-ray", ""),
                "location": headers.get("location", ""),
            }
    except Exception as exc:
        return {"error": str(exc)}


def main() -> int:
    print("Cloudflare Bulk Redirects only run when DNS is proxied (orange cloud).\n")

    www_addrs = resolve(f"www.{APEX}")
    apex_addrs = resolve(APEX)

    print(f"DNS www.{APEX} -> {', '.join(www_addrs)}")
    print(f"DNS {APEX} -> {', '.join(apex_addrs)}")

    github_direct = any(
        addr.startswith(GITHUB_PAGES_HINTS) for addr in www_addrs + apex_addrs if addr[0].isdigit()
    )
    if github_direct:
        print(
            "\n[FAIL] DNS resolves to GitHub Pages IPs, not Cloudflare.\n"
            "       Bulk Redirect CSV uploads will NOT affect live traffic.\n"
            "       Fix: Cloudflare Dashboard -> DNS -> set www and @ records to Proxied (orange cloud)."
        )
    else:
        print("\n[OK] DNS does not look like direct GitHub Pages A records.")

    sample = f"{CANONICAL_ORIGIN}/realism_tattoos_las_vegas_master_authority_guide/"
    result = probe(sample)
    print(f"\nHEAD {sample}")
    if "error" in result:
        print(f"  error: {result['error']}")
    else:
        print(f"  status: {result['status']}")
        print(f"  server: {result['server']}")
        print(f"  cf-ray: {result['cf_ray'] or '(missing)'}")
        print(f"  location: {result['location'] or '(none)'}")

    if not result.get("cf-ray"):
        print(
            "\n[FAIL] No cf-ray header — request did not pass Cloudflare edge.\n"
            "       After enabling proxy, also verify:\n"
            "       1. Rules -> Bulk Redirects -> Redirect Lists (CSV imported)\n"
            "       2. Rules -> Bulk Redirects -> Redirect Rules (rule enabled, list attached)"
        )
        return 1

    if result.get("status") not in {"301", "308"}:
        print(
            "\n[WARN] Cloudflare is proxying, but the sample obsolete URL is not redirecting yet.\n"
            "       Confirm the Bulk Redirect Rule is enabled and uses the imported list."
        )
        return 1

    print("\n[OK] Cloudflare proxy and sample redirect look healthy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
