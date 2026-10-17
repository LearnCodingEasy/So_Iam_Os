"""Unit tests for deterministic knowledge metadata extraction."""
import unittest

from .metadata import extract_metadata


class MetadataExtractionTests(unittest.TestCase):
    def test_extracts_headings_summary_and_technology_tags(self):
        result = extract_metadata(
            title="Django API",
            content="# API Overview\n\nThis guide explains Django REST API design.\n\n## Authentication\nUse token authentication.",
        )
        self.assertEqual(result["headings"], ["API Overview", "Authentication"])
        self.assertIn("django", result["technology_tags"])
        self.assertIn("api", result["keywords"])
        self.assertTrue(result["summary"].startswith("This guide"))

    def test_arabic_language_hint(self):
        self.assertEqual(extract_metadata(content="مقدمة عن البرمجة")["language_hint"], "ar")

    def test_empty_content_is_safe(self):
        result = extract_metadata()
        self.assertEqual(result["word_count"], 0)
        self.assertEqual(result["headings"], [])


if __name__ == "__main__":
    unittest.main()
