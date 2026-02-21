import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from noc_assistant import build_report, triage_alert  # noqa: E402


class NocAssistantTests(unittest.TestCase):
    def test_triage_alert_priority(self):
        alert = {"severity": "critical", "message": "Main DB down"}
        triaged = triage_alert(alert)
        self.assertEqual(triaged["priority"], "P1")
        self.assertEqual(triaged["eta_minutes"], 5)

    def test_build_report_summary(self):
        alerts = [
            {"severity": "critical"},
            {"severity": "high"},
            {"severity": "low"},
        ]
        report = build_report(alerts)
        self.assertEqual(report["summary"]["total_alerts"], 3)
        self.assertEqual(report["summary"]["severity_counts"]["critical"], 1)
        self.assertGreater(report["summary"]["high_priority_ratio_percent"], 60)


if __name__ == "__main__":
    unittest.main()
