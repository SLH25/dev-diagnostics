import unittest

from dev_diagnostics.checks import (
    check_developer_tools,
    check_disk,
    check_environment,
    check_python,
)


class TestChecks(unittest.TestCase):

    def test_python(self):
        result = check_python()

        self.assertIn("version", result)
        self.assertIn("status", result)
        self.assertEqual(result["name"], "Python")

    def test_disk(self):
        result = check_disk()

        self.assertIn("total_gb", result)
        self.assertIn("free_gb", result)
        self.assertIn("status", result)

        self.assertGreater(result["total_gb"], 0)
        self.assertGreaterEqual(result["free_gb"], 0)

    def test_environment(self):
        result = check_environment()

        self.assertIn("variables", result)
        self.assertIn("PATH", result["variables"])
        self.assertIn("status", result)

    def test_developer_tools(self):
        result = check_developer_tools()

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        for tool in result:
            self.assertIn("name", tool)
            self.assertIn("installed", tool)
            self.assertIn("status", tool)


if __name__ == "__main__":
    unittest.main()