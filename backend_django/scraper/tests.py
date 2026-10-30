from django.test import SimpleTestCase
from types import SimpleNamespace
from .services import normalize_item, parse_source, validate_public_url


class ScraperSafetyTests(SimpleTestCase):
    def test_rejects_localhost(self):
        with self.assertRaises(ValueError):
            validate_public_url("http://localhost:8000/api/")

    def test_rejects_non_http_scheme(self):
        with self.assertRaises(ValueError):
            validate_public_url("file:///etc/passwd")

    def test_normalize_json_job(self):
        result = normalize_item({"id": "abc", "title": "Python Engineer", "company": "Example", "url": "https://example.com/jobs/1"})
        self.assertEqual(result["title"], "Python Engineer")
        self.assertEqual(result["external_id"], "abc")
        self.assertEqual(result["url"], "https://example.com/jobs/1")

    def test_normalize_greenhouse_style_job(self):
        result = normalize_item({
            "id": "gh-123", "title": "Django Engineer",
            "company_name": "Example Co", "absolute_url": "https://jobs.example/123",
            "content": "<p>Build APIs</p>", "location": {"name": "Remote"},
        })
        self.assertEqual(result["external_id"], "gh-123")
        self.assertEqual(result["url"], "https://jobs.example/123")
        self.assertEqual(result["company"], "Example Co")
        self.assertEqual(result["description"], "Build APIs")
        self.assertEqual(result["location"], "Remote")

    def test_normalize_does_not_treat_id_as_a_url(self):
        result = normalize_item({"id": "job-42", "title": "Backend Engineer"})
        self.assertEqual(result["external_id"], "job-42")
        self.assertEqual(result["url"], "")

    def test_parse_json_items_path(self):
        website = SimpleNamespace(source_type="json", config={"items_path": "data.results"})
        rows = parse_source(website, b'{"data":{"results":[{"title":"A"}]}}', "application/json")
        self.assertEqual(rows, [{"title": "A"}])

    def test_html_requires_explicit_selector(self):
        website = SimpleNamespace(source_type="html", config={})
        with self.assertRaises(ValueError):
            parse_source(website, b"<html><body><h1>jobs</h1></body></html>", "text/html")
