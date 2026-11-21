import sys
import unittest
from pathlib import Path

PROJECT = Path("/content/drive/MyDrive/Cehpoint_Hermes_AI_SOC")
sys.path.insert(0, str(PROJECT / "src"))

from soc.investigation.engine import assess_severity, build_timeline


def make_event(event_id, event_type, timestamp):
    return {
        "event_id": event_id,
        "event_type": event_type,
        "timestamp": timestamp,
        "account": "analyst.user",
        "source_ip": "198.51.100.42",
        "asset": "WORKSTATION-042",
        "_source_line": 1
    }


class InvestigationTests(unittest.TestCase):

    def test_suspicious_sequence_with_host_event(self):
        events = (
            [make_event(f"F{i}", "failed_login", "2026-11-21T09:00:00Z")
             for i in range(50)]
            + [make_event("S1", "successful_login", "2026-11-21T09:26:00Z")]
            + [make_event("H1", "host_login_observed", "2026-11-21T09:27:00Z")]
        )
        result = assess_severity(events, {})
        self.assertEqual(result["severity"], "High")
        self.assertEqual(result["confidence"], "High")

    def test_no_events(self):
        result = assess_severity([], {})
        self.assertEqual(result["severity"], "Low")
        self.assertEqual(result["confidence"], "Low")

    def test_failed_logins_without_success(self):
        events = [
            make_event(f"F{i}", "failed_login", "2026-11-21T09:00:00Z")
            for i in range(10)
        ]
        result = assess_severity(events, {})
        self.assertEqual(result["severity"], "Medium")
        self.assertEqual(result["confidence"], "Low")

    def test_missing_host_corroboration(self):
        events = (
            [make_event(f"F{i}", "failed_login", "2026-11-21T09:00:00Z")
             for i in range(50)]
            + [make_event("S1", "successful_login", "2026-11-21T09:26:00Z")]
        )
        result = assess_severity(events, {})
        self.assertEqual(result["severity"], "High")
        self.assertEqual(result["confidence"], "Medium")

    def test_below_50_failures_with_success(self):
        events = (
            [make_event(f"F{i}", "failed_login", "2026-11-21T09:00:00Z")
             for i in range(5)]
            + [make_event("S1", "successful_login", "2026-11-21T09:26:00Z")]
        )
        result = assess_severity(events, {})
        self.assertEqual(result["severity"], "Medium")

    def test_timeline_is_sorted(self):
        events = [
            make_event("LATE", "successful_login", "2026-11-21T09:26:00Z"),
            make_event("EARLY", "failed_login", "2026-11-21T09:00:00Z")
        ]
        timeline = build_timeline(events)
        self.assertEqual(timeline[0]["event_id"], "EARLY")
        self.assertEqual(timeline[1]["event_id"], "LATE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
