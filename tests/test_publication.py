"""Publication checks detect private content without echoing matched values."""

import io
import sys
import unittest
from pathlib import Path

from PIL import Image, PngImagePlugin

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from audit_publication import inspect  # noqa: E402


class PublicationTests(unittest.TestCase):
    def test_documented_home_placeholders_are_allowed(self):
        data = b'%USERPROFILE%/.codex/pets and $CODEX_HOME/pets; D:/My Codex Home'
        self.assertEqual(inspect("example.md", data), [])

    def test_private_values_are_detected_without_echoing_them(self):
        cases = [
            ("C:" + "/Users/" + "example-user" + "/private", "personal-home-path"),
            ("sample" + "@" + "example.com", "email-address"),
            ("gh" + "p_" + "a" * 30, "credential"),
        ]
        for value, category in cases:
            findings = inspect("example.txt", value.encode())
            self.assertTrue(any(category in finding for finding in findings))
            self.assertNotIn(value, " ".join(findings))

    def test_png_text_metadata_is_detected(self):
        info = PngImagePlugin.PngInfo()
        info.add_text("Comment", "private value")
        output = io.BytesIO()
        Image.new("RGB", (2, 2)).save(output, format="PNG", pnginfo=info)
        findings = inspect("image.png", output.getvalue())
        self.assertTrue(findings)
        self.assertNotIn("private value", " ".join(findings))

    def test_clean_png_is_allowed(self):
        output = io.BytesIO()
        Image.new("RGB", (2, 2)).save(output, format="PNG")
        self.assertEqual(inspect("image.png", output.getvalue()), [])


if __name__ == "__main__":
    unittest.main()
