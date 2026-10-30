"""Regression tests for RSS 2.0 and Atom job-feed parsing."""
from django.test import SimpleTestCase

from .tasks import _rss_items, _safe_job_url, _json_path


class RSSParserTests(SimpleTestCase):
    def test_job_url_validator_rejects_unsafe_schemes_and_credentials(self):
        self.assertEqual(_safe_job_url("javascript:alert(1)"), "")
        self.assertEqual(_safe_job_url("https://user:pass@jobs.example/1"), "")
        self.assertEqual(_safe_job_url("http://127.0.0.1/internal"), "")
        self.assertEqual(_safe_job_url("https://jobs.example/1"), "https://jobs.example/1")

    def test_json_path_reads_nested_items(self):
        self.assertEqual(_json_path({"data": {"jobs": [{"title": "Django"}]}}, "data.jobs")[0]["title"], "Django")
        self.assertIsNone(_json_path({"data": {}}, "data.missing"))

    def test_rss_item_reads_leaf_elements(self):
        xml = b"""<?xml version="1.0"?>
        <rss version="2.0"><channel><item>
          <guid>job-123</guid><title>Python Developer</title>
          <description>Build APIs</description><link>https://jobs.example/jobs/123</link>
          <company>Example Ltd</company><location>Remote</location>
        </item></channel></rss>"""
        result = _rss_items(xml)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "job-123")
        self.assertEqual(result[0]["title"], "Python Developer")
        self.assertEqual(result[0]["url"], "https://jobs.example/jobs/123")
        self.assertEqual(result[0]["company"], "Example Ltd")
        self.assertEqual(result[0]["location"], "Remote")

    def test_atom_entry_reads_alternate_href(self):
        xml = b"""<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
          <entry><id>urn:job:456</id><title>Backend Engineer</title>
            <summary>Build backend services</summary>
            <link rel="self" href="https://jobs.example/api/456"/>
            <link rel="alternate" href="https://jobs.example/jobs/456"/>
          </entry>
        </feed>"""
        result = _rss_items(xml)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "urn:job:456")
        self.assertEqual(result[0]["title"], "Backend Engineer")
        self.assertEqual(result[0]["description"], "Build backend services")
        self.assertEqual(result[0]["url"], "https://jobs.example/jobs/456")

    def test_invalid_xml_raises_actionable_error_for_string_input(self):
        with self.assertRaisesRegex(ValueError, "RSS/Atom feed is not valid XML"):
            _rss_items("<rss><item>")
