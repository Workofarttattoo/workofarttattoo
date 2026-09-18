#!/usr/bin/env python3
"""Test domain-protocol canonicalization: single-hop 301/308 to https://www."""

from __future__ import annotations

import argparse
import sys
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("Install requests: pip install requests", file=sys.stderr)
    raise SystemExit(2)

CANONICAL_ORIGIN = "https://www.workofarttattoo.com"

DEFAULT_URLS = [
    "http://workofarttattoo.com/",
    "http://www.workofarttattoo.com/",
    "https://workofarttattoo.com/",
    "http://workofarttattoo.com/piercing-guide-las-vegas/",
    "https://workofarttattoo.com/cover-up-tattoos-las-vegas/?utm=test",
    "http://www.workofarttattoo.com/how-to-choose-a-tattoo-artist/",
    "https://workofarttattoo.com/sitemap-static-pages.xml",
    "http://workofarttattoo.com/knowledge/tattoo-on-ribs-recovery/",
]


def trace_redirects(url: str, timeout: float = 15.0) -> dict:
    hops: list[dict] = []
    session = requests.Session()
    current = url
    for _ in range(10):
        resp = session.get(current, allow_redirects=False, timeout=timeout)
        hop = {
            "url": current,
            "status": resp.status_code,
            "location": resp.headers.get("Location", ""),
        }
        hops.append(hop)
        if resp.status_code not in (301, 302, 303, 307, 308):
            break
        location = hop["location"]
        if not location:
            break
        if location.startswith("/"):
            parsed = urlparse(current)
            current = f"{parsed.scheme}://{parsed.netloc}{location}"
        else:
            current = location
    final = hops[-1]
    expected = url.replace("http://workofarttattoo.com", CANONICAL_ORIGIN)
    expected = expected.replace("http://www.workofarttattoo.com", CANONICAL_ORIGIN)
    expected = expected.replace("https://workofarttattoo.com", CANONICAL_ORIGIN)
    ok = (
        len(hops) <= 2
        and final["status"] == 200
        and hops[0]["url"] != hops[-1]["url"]
        and current.startswith(CANONICAL_ORIGIN)
    )
    if url.startswith(CANONICAL_ORIGIN):
        ok = len(hops) == 1 and final["status"] == 200
    return {
        "requested": url,
        "hops": len(hops) - 1 if final["status"] == 200 else len(hops),
        "chain": hops,
        "final_url": current if final["status"] == 200 else hops[-1]["url"],
        "final_status": final["status"],
        "ok": ok,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Test canonical redirect hops")
    parser.add_argument("--url", action="append", dest="urls", help="URL to test (repeatable)")
    parser.add_argument("--live", action="store_true", help="Required flag for production tests")
    args = parser.parse_args()
    if not args.live:
        print("Pass --live to run against production.", file=sys.stderr)
        return 1
    urls = args.urls or DEFAULT_URLS
    failures = 0
    print(f"{'Requested URL':<70} {'Status':>6} {'Hops':>4} {'Final URL'}")
    print("-" * 120)
    for url in urls:
        result = trace_redirects(url)
        first_loc = result["chain"][0]["location"] if len(result["chain"]) > 1 else ""
        status = result["chain"][0]["status"]
        print(
            f"{result['requested']:<70} {status:>6} {result['hops']:>4} "
            f"{result['final_url'][:60]}"
        )
        if first_loc:
            print(f"  Location: {first_loc}")
        if not result["ok"]:
            failures += 1
            print("  FAIL")
    print(f"\n{len(urls) - failures}/{len(urls)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
