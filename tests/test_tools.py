import sys
import unittest
from pathlib import Path

PROJECT = Path("/content/drive/MyDrive/Cehpoint_Hermes_AI_SOC")
sys.path.insert(0, str(PROJECT / "src"))

from soc.tools.registry import execute_tool


class ToolTests(unittest.TestCase):

    def test_search_logs_returns_matching_events(self):
        result = execute_tool(
            "search_logs",
            {"account": "analyst.user"}
        )
        self.assertTrue(result["success"])
        self.assertGreater(result["count"], 0)

    def test_search_logs_empty_result(self):
        result = execute_tool(
            "search_logs",
            {"account": "account_that_does_not_exist"}
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["count"], 0)

    def test_lookup_ip_rejects_invalid_ip(self):
        result = execute_tool(
            "lookup_ip",
            {"ip": "999.999.999.999"}
        )
        self.assertFalse(result["success"])

    def test_lookup_ip_handles_unknown_address(self):
        result = execute_tool(
            "lookup_ip",
            {"ip": "203.0.113.20"}
        )
        self.assertTrue(result["success"])
        self.assertFalse(result["found"])

    def test_search_cve_handles_unknown_product(self):
        result = execute_tool(
            "search_cve",
            {"product": "UnknownProductForTest"}
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["count"], 0)

    def test_unapproved_tool_is_rejected(self):
        result = execute_tool(
            "disable_account",
            {"account": "analyst.user"}
        )
        self.assertFalse(result["success"])

    def test_missing_tool_argument_is_rejected(self):
        result = execute_tool("lookup_ip", {})
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
