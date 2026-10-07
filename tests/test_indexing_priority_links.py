#!/usr/bin/env python3
"""Guard the surgical Indexing Priority 30 internal-link pass."""

from __future__ import annotations

import unittest
from pathlib import Path

from inject_indexing_priority_links import PRIORITY_30, SECTIONS

ROOT = Path(__file__).resolve().parents[1]


class IndexingPriorityLinksTests(unittest.TestCase):
    def test_exactly_30_unique_priority_urls(self) -> None:
        self.assertEqual(len(PRIORITY_30), 30)
        self.assertEqual(len(set(PRIORITY_30)), 30)

    def test_parent_pages_exist(self) -> None:
        for rel in SECTIONS:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_targets_are_internal_and_have_human_labels(self) -> None:
        for section in SECTIONS.values():
            for href, label in section["links"]:
                self.assertTrue(href.startswith("/") and href.endswith("/"), href)
                self.assertNotIn("http", href)
                self.assertGreaterEqual(len(label.strip()), 8, label)

    def test_no_parent_gets_link_dump(self) -> None:
        for rel, section in SECTIONS.items():
            self.assertLessEqual(len(section["links"]), 8, rel)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
