from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from analytics.models import AnalyticsEvent, Metric, Report
from analytics.services import analytics_service

User = get_user_model()


class AnalyticsServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="an-svc@example.com", password="pw-12345-test", name="Owner")
        self.metric = Metric.objects.create(user=self.user, key="mrr", name="MRR", unit="USD")
        now = timezone.now()
        for days, value in ((3, 100), (2, 150), (1, 200)):
            analytics_service.record_snapshot(self.metric, value, now - timedelta(days=days))

    def test_metric_summary(self):
        summary = analytics_service.metric_summary(self.metric)
        self.assertEqual(summary["count"], 3)
        self.assertEqual((summary["min"], summary["max"], summary["latest"]), (100.0, 200.0, 200.0))
        self.assertEqual(summary["average"], 150.0)
        self.assertEqual(summary["change"], 100.0)
        self.assertEqual(summary["change_percent"], 100.0)

    def test_summary_respects_period(self):
        today = timezone.localdate()
        summary = analytics_service.metric_summary(self.metric, today - timedelta(days=2), today)
        self.assertEqual(summary["count"], 2)

    def test_empty_metric_summary(self):
        empty = Metric.objects.create(user=self.user, key="none", name="None")
        summary = analytics_service.metric_summary(empty)
        self.assertEqual(summary["count"], 0)
        self.assertIsNone(summary["latest"])
        self.assertIsNone(summary["change"])

    def test_event_counts(self):
        for name in ("signup", "signup", "purchase"):
            AnalyticsEvent.objects.create(user=self.user, name=name)
        other = User.objects.create_user(email="an-svc2@example.com", password="pw-12345-test", name="Other")
        AnalyticsEvent.objects.create(user=other, name="signup")
        result = analytics_service.event_counts(self.user)
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["events"][0], {"name": "signup", "count": 2})

    def test_generate_summary_report(self):
        report = Report.objects.create(user=self.user, title="Weekly")
        analytics_service.generate_report(report)
        report.refresh_from_db()
        self.assertIsNotNone(report.generated_at)
        self.assertEqual(report.content["metrics"][0]["key"], "mrr")

    def test_generate_trend_report_requires_own_metric(self):
        other = User.objects.create_user(email="an-svc3@example.com", password="pw-12345-test", name="Other")
        foreign = Metric.objects.create(user=other, key="x", name="X")
        report = Report.objects.create(user=self.user, title="T", report_type="metric_trend", parameters={"metric": foreign.pk})
        self.assertIn("error", analytics_service.generate_report(report).content)
        report.parameters = {"metric": self.metric.pk}
        content = analytics_service.generate_report(report).content
        self.assertEqual([p["value"] for p in content["points"]], [100.0, 150.0, 200.0])
