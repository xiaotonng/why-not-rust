import json
import sys
import unittest
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parents[1] / "skills" / "why-not-rust" / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

from report_safety import html_text, json_for_html, safe_href  # noqa: E402


class ReportSafetyTests(unittest.TestCase):
    def test_visible_text_is_escaped(self) -> None:
        payload = '<img src=x onerror="alert(1)"> & "quoted"'
        escaped = html_text(payload)
        self.assertNotIn("<img", escaped)
        self.assertIn("&lt;img", escaped)
        self.assertIn("&amp;", escaped)
        self.assertIn("&quot;", escaped)

    def test_only_absolute_http_links_are_allowed(self) -> None:
        self.assertEqual(safe_href("https://example.com/a?b=1&c=2"), "https://example.com/a?b=1&amp;c=2")
        for value in ["javascript:alert(1)", "data:text/html,x", "/local/path", "example.com"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_href(value)

    def test_embedded_json_cannot_close_its_script_block(self) -> None:
        payload = {"repo": "</ScRiPt><script>alert(1)</script>", "line": "a\u2028b\u2029c", "amp": "a&b"}
        rendered = json_for_html(payload)
        self.assertNotIn("<", rendered)
        self.assertNotIn(">", rendered)
        self.assertNotIn("&", rendered)
        self.assertEqual(json.loads(rendered), payload)


if __name__ == "__main__":
    unittest.main()
