#!/usr/bin/env python3
"""Priority commercial guides expose licensed image metadata without schema spam."""

from __future__ import annotations

import unittest
from pathlib import Path

from woa_entity_schema import ID_JOSHUA, priority_guide_image_objects

ROOT = Path(__file__).resolve().parents[1]


class MultimodalSchemaTests(unittest.TestCase):
    def test_priority_guides_have_small_visible_image_sets(self) -> None:
        for slug in (
            "cover-up-tattoos-las-vegas",
            "realism_tattoos_las_vegas_master_authority_guide",
            "fine_line_tattoos_las_vegas_master_authority_guide",
        ):
            nodes = priority_guide_image_objects(slug, ROOT, creator_id=ID_JOSHUA)
            self.assertGreaterEqual(len(nodes), 3, slug)
            self.assertLessEqual(len(nodes), 4, slug)
            urls = [node["contentUrl"] for node in nodes]
            self.assertEqual(len(urls), len(set(urls)), slug)
            for node in nodes:
                self.assertEqual(node.get("@type"), "ImageObject")
                self.assertTrue(node.get("description"))
                self.assertTrue(node.get("license"))
                self.assertTrue(node.get("creditText"))
                self.assertTrue(node.get("copyrightNotice"))
                self.assertTrue(node.get("contentUrl", "").startswith("https://www.workofarttattoo.com/"))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
