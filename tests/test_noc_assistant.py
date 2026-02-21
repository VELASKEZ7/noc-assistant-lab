import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from noc_assistant import build_markdown_report, build_report, triage_alert  # noqa: E402


class NocAssistantTests(unittest.TestCase):
    def test_triage_alert_priority(self):
        now = datetime(2026, 2, 21, 4, 0, tzinfo=UTC)
        alert = {"severity": "critical", "message": "Main DB down", "timestamp": "2026-02-21T03:55:00Z"}
        triaged = triage_alert(alert, now)
        self.assertEqual(triaged["priority"], "P1")
        self.assertEqual(triaged["eta_minutes"], 5)
        self.assertFalse(triaged["risk_sla_breach"])

    def test_build_report_summary(self):
        alerts = [
            {"severity": "critical", "service": "db", "timestamp": "2026-02-21T03:30:00Z"},
            {"severity": "high", "service": "api", "timestamp": "2026-02-21T03:50:00Z"},
            {"severity": "low", "service": "api", "timestamp": "2026-02-21T03:40:00Z"},
        ]
        report = build_report(alerts, now_utc=datetime(2026, 2, 21, 4, 0, tzinfo=UTC))
        self.assertEqual(report["summary"]["total_alerts"], 3)
        self.assertEqual(report["summary"]["severity_counts"]["critical"], 1)
        self.assertGreater(report["summary"]["high_priority_ratio_percent"], 60)
        markdown = build_markdown_report(report)
        self.assertIn("Top services", markdown)


if __name__ == "__main__":
    unittest.main()
