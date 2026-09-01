#!/usr/bin/env python3
"""Analytics event semantics — guard against lead/conversion inflation."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GA_PATH = ROOT / "woa_ga4_conversions.py"
BOOKING_PATH = ROOT / "appointments" / "woa-booking.js"


def ga_source() -> str:
    return GA_PATH.read_text(encoding="utf-8")


def record_success_block(source: str) -> str:
    match = re.search(r"function recordFormSubmitSuccess[\s\S]*?^  \}", source, re.MULTILINE)
    if not match:
        raise AssertionError("recordFormSubmitSuccess block not found")
    return match.group(0)


class AnalyticsSemanticsTests(unittest.TestCase):
    def test_case_1_homepage_load_no_lead_events(self) -> None:
        source = ga_source()
        top_level = source.split("function recordFormSubmitSuccess")[0]
        for event in ("booking_submit", "generate_lead"):
            self.assertNotIn(f'send("{event}"', top_level, f"{event} must not fire outside success handler")

    def test_case_2_appointments_booking_view_once_no_submit(self) -> None:
        source = ga_source()
        self.assertIn("woa_booking_view_session", source)
        top_level = source.split("function recordFormSubmitSuccess")[0]
        self.assertNotIn('send("booking_submit"', top_level)

    def test_case_3_book_cta_booking_start_not_submit(self) -> None:
        source = ga_source()
        click_block = re.search(r'document\.addEventListener\(\s*"click"[\s\S]*?true\s*\);', source)
        self.assertIsNotNone(click_block)
        block = click_block.group(0)
        self.assertIn('send("booking_start"', block)
        self.assertNotIn('send("booking_submit"', block)

    def test_case_4_submit_attempt_not_success(self) -> None:
        source = ga_source()
        submit_block = re.search(r'form\.addEventListener\("submit"[\s\S]*?\n  \}\}\);', source)
        self.assertIsNotNone(submit_block)
        block = submit_block.group(0)
        self.assertIn('send("booking_submit_attempt"', block)
        self.assertNotIn('send("booking_submit"', block)
        self.assertNotIn('send("generate_lead"', block)

    def test_case_5_success_handler_fires_booking_submit_once(self) -> None:
        block = record_success_block(ga_source())
        self.assertEqual(block.count('send("booking_submit"'), 1)
        self.assertIn('send("generate_lead"', block)
        self.assertIn("dedupeKey", block)
        self.assertNotIn("allowRepeat: true", block)

    def test_case_6_phone_click_once_pattern(self) -> None:
        source = ga_source()
        self.assertIn('send("phone_click"', source)
        self.assertIn('h.indexOf("tel:") === 0', source)

    def test_case_7_email_click_once_pattern(self) -> None:
        source = ga_source()
        self.assertIn('send("email_click"', source)
        self.assertIn('h.indexOf("mailto:") === 0', source)

    def test_case_8_reload_listener_guard(self) -> None:
        source = ga_source()
        self.assertIn("__woaGa4ConversionsInit", source)

    def test_case_9_automated_traffic_suppressed(self) -> None:
        source = ga_source()
        self.assertIn("isAutomatedTraffic", source)
        send_block = re.search(r"function send\(name, params, options\)[\s\S]*?^  \}", source, re.MULTILINE)
        self.assertIsNotNone(send_block)
        self.assertIn("isAutomatedTraffic()", send_block.group(0))

    def test_booking_js_dispatches_success_bridge(self) -> None:
        booking = BOOKING_PATH.read_text(encoding="utf-8")
        self.assertIn("woa_booking_submit_success", booking)
        self.assertIn("dispatchBookingSuccess", booking)

    def test_no_pii_in_analytics_payloads(self) -> None:
        source = ga_source()
        forbidden = ("full_name", "data.email", "data.phone", "tattoo_description", "piercing_notes")
        for phrase in forbidden:
            self.assertNotIn(phrase, source, f"possible PII reference: {phrase}")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
