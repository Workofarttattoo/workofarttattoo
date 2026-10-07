#!/usr/bin/env python3
"""Booking form semantics for accessibility and browser agents."""

from __future__ import annotations

import unittest
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ROOT / "appointments" / "code.html",
    ROOT / "appointments" / "woa-booking-forms.html",
)
FORM_IDS = ("woa-form-tattoo", "woa-form-piercing")


class BookingAccessibilityTests(unittest.TestCase):
    def test_visible_controls_have_explicit_labels_and_unique_ids(self) -> None:
        for path in FILES:
            soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
            ids: list[str] = []
            for form_id in FORM_IDS:
                form = soup.find("form", id=form_id)
                self.assertIsNotNone(form, f"{path}: missing {form_id}")
                for control in form.find_all(["input", "select", "textarea"]):
                    if control.name == "input" and control.get("type", "").lower() == "hidden":
                        continue
                    if control.get("name") == "_woa_hp":
                        continue
                    control_id = control.get("id")
                    self.assertTrue(control_id, f"{path}: {form_id} {control.get('name')} missing id")
                    label = form.find("label", attrs={"for": control_id})
                    self.assertIsNotNone(
                        label,
                        f"{path}: {form_id} {control.get('name')} missing explicit label[for]",
                    )
                    ids.append(control_id)
            self.assertEqual(len(ids), len(set(ids)), f"{path}: duplicate form control ids")

    def test_booking_destinations_are_unchanged(self) -> None:
        for path in FILES:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(
                text.count('action="https://formsubmit.co/thewhiteknight702@gmail.com"'),
                2,
                f"{path}: booking destination changed",
            )


if __name__ == "__main__":
    raise SystemExit(unittest.main())
