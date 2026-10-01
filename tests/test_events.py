import unittest

from dev_diagnostics.events import analyze_events


class TestEvents(unittest.TestCase):

    def test_event_analysis(self):
        events = [
            {
                "timestamp": "2026-08-01T09:00:00Z",
                "service": "billing-api",
                "level": "INFO",
                "latency_ms": 148,
                "status_code": 200,
            },
            {
                "timestamp": "2026-08-01T09:01:00Z",
                "service": "billing-api",
                "level": "WARN",
                "latency_ms": 920,
                "status_code": 200,
            },
            {
                "timestamp": "2026-08-01T09:02:00Z",
                "service": "profile-api",
                "level": "ERROR",
                "latency_ms": 1210,
                "status_code": 503,
            },
        ]

        result = analyze_events(events)

        self.assertEqual(result["total_events"], 3)
        self.assertEqual(result["info"], 1)
        self.assertEqual(result["warnings"], 1)
        self.assertEqual(result["errors"], 1)
        self.assertEqual(result["status"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()