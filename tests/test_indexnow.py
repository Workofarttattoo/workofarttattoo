"""Tests for IndexNow URL validation and payload construction."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from woa_indexnow import (
    INITIAL_SUBMISSION_URLS,
    build_payload,
    filter_submittable_urls,
    key_location,
    load_config,
    normalize_public_url,
    source_path_to_public_url,
    urls_from_git_diff,
)


class IndexNowValidationTests(unittest.TestCase):
    def test_normalize_requires_www_https(self) -> None:
        self.assertEqual(
            normalize_public_url("https://www.workofarttattoo.com/start_here/"),
            "https://www.workofarttattoo.com/start_here/",
        )
        self.assertIsNone(normalize_public_url("http://www.workofarttattoo.com/"))
        self.assertIsNone(normalize_public_url("https://workofarttattoo.com/"))
        self.assertIsNone(normalize_public_url("https://example.com/"))

    def test_reject_query_and_fragment(self) -> None:
        self.assertIsNone(
            normalize_public_url("https://www.workofarttattoo.com/start_here/?x=1")
        )
        self.assertIsNone(
            normalize_public_url("https://www.workofarttattoo.com/start_here/#section")
        )

    def test_deduplicate_urls(self) -> None:
        urls = filter_submittable_urls(
            [
                "https://www.workofarttattoo.com/start_here/",
                "https://www.workofarttattoo.com/start_here/",
                "/start_here/",
            ]
        )
        self.assertEqual(urls, ["https://www.workofarttattoo.com/start_here/"])

    def test_reject_external_urls(self) -> None:
        urls = filter_submittable_urls(
            [
                "https://www.workofarttattoo.com/",
                "https://www.google.com/",
            ]
        )
        self.assertEqual(urls, ["https://www.workofarttattoo.com/"])

    def test_retired_slug_excluded(self) -> None:
        mapped = source_path_to_public_url(
            "tattoo_shop_near_the_strip_geo_seo_optimized/code.html"
        )
        self.assertIsNone(mapped)

    def test_noindex_stub_not_submitted(self) -> None:
        mapped = source_path_to_public_url(
            "cover_up_tattoos_las_vegas_master_authority_guide/code.html"
        )
        self.assertIsNone(mapped)

    def test_canonical_cover_up_folder(self) -> None:
        mapped = source_path_to_public_url("cover-up-tattoos-las-vegas/code.html")
        self.assertEqual(mapped, "https://www.workofarttattoo.com/cover-up-tattoos-las-vegas/")

    def test_key_location_format(self) -> None:
        cfg = load_config()
        loc = key_location(cfg["host"], cfg["key"])
        self.assertTrue(loc.startswith("https://www.workofarttattoo.com/"))
        self.assertTrue(loc.endswith(".txt"))

    def test_payload_structure(self) -> None:
        payload = build_payload(["https://www.workofarttattoo.com/start_here/"])
        self.assertEqual(payload["host"], "www.workofarttattoo.com")
        self.assertIn("key", payload)
        self.assertIn("keyLocation", payload)
        self.assertEqual(
            payload["urlList"],
            ["https://www.workofarttattoo.com/start_here/"],
        )

    def test_initial_urls_are_canonical(self) -> None:
        for url in INITIAL_SUBMISSION_URLS:
            self.assertIsNotNone(normalize_public_url(url))
            self.assertNotIn("geo_seo_optimized", url)

    def test_key_file_matches_config(self) -> None:
        cfg = load_config()
        key_file = ROOT / f"{cfg['key']}.txt"
        self.assertTrue(key_file.is_file())
        self.assertEqual(key_file.read_text(encoding="utf-8").strip(), cfg["key"])

    def test_changed_url_selection_from_git(self) -> None:
        urls = urls_from_git_diff("HEAD~1", "HEAD")
        self.assertIsInstance(urls, list)
        for url in urls:
            self.assertTrue(url.startswith("https://www.workofarttattoo.com/"))


if __name__ == "__main__":
    unittest.main()
