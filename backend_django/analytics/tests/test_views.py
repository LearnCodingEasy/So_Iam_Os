from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from analytics.models import Metric

User = get_user_model()


class AnalyticsApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="an-api@example.com", password="pw-12345-test", name="Owner")
        self.other = User.objects.create_user(email="an-api2@example.com", password="pw-12345-test", name="Other")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def _metric(self, key="mrr"):
        return self.client.post("/api/analytics/metrics/", {"key": key, "name": key.upper(), "unit": "USD"}, format="json")

    def test_authentication_required(self):
        self.assertEqual(APIClient().get("/api/analytics/metrics/").status_code, 401)

    def test_duplicate_metric_key_is_a_400_not_a_500(self):
        self.assertEqual(self._metric().status_code, 201)
        self.assertEqual(self._metric().status_code, 400)

    def test_metrics_are_isolated(self):
        Metric.objects.create(user=self.other, key="secret", name="S")
        self._metric()
        self.assertEqual([m["key"] for m in self.client.get("/api/analytics/metrics/").json()], ["mrr"])

    def test_snapshot_for_foreign_metric_rejected(self):
        foreign = Metric.objects.create(user=self.other, key="secret", name="S")
        response = self.client.post("/api/analytics/snapshots/", {"metric": foreign.pk, "value": "1"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_snapshot_and_summary_flow(self):
        metric_id = self._metric().json()["id"]
        for value in ("10", "30"):
            r = self.client.post("/api/analytics/snapshots/", {"metric": metric_id, "value": value}, format="json")
            self.assertEqual(r.status_code, 201)
        summary = self.client.get("/api/analytics/metrics/%s/summary/" % metric_id).json()
        self.assertEqual(summary["count"], 2)
        self.assertEqual(summary["average"], 20.0)
        bad = self.client.get("/api/analytics/metrics/%s/summary/?start=nope" % metric_id)
        self.assertEqual(bad.status_code, 400)

    def test_event_counts_endpoint(self):
        for _ in range(2):
            self.client.post("/api/analytics/events/", {"name": "lesson_done", "properties": {"id": 1}}, format="json")
        data = self.client.get("/api/analytics/events/counts/").json()
        self.assertEqual(data["events"], [{"name": "lesson_done", "count": 2}])
        self.assertEqual(self.client.post("/api/analytics/events/", {"name": "x", "properties": [1]}, format="json").status_code, 400)

    def test_report_generation_and_period_validation(self):
        self._metric()
        created = self.client.post("/api/analytics/reports/", {"title": "Weekly"}, format="json").json()
        self.assertIsNone(created["generated_at"])
        generated = self.client.post("/api/analytics/reports/%s/generate/" % created["id"]).json()
        self.assertIsNotNone(generated["generated_at"])
        bad = self.client.post("/api/analytics/reports/", {"title": "x", "period_start": "2026-02-01", "period_end": "2026-01-01"}, format="json")
        self.assertEqual(bad.status_code, 400)
        self.assertEqual(self.client.patch("/api/analytics/reports/%s/" % created["id"], {"content": {"forged": 1}}, format="json").json()["content"].get("forged"), None)
