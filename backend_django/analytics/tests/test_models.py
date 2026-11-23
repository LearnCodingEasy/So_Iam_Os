from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from analytics.models import AnalyticsEvent, Metric, MetricSnapshot, Report

User = get_user_model()


class AnalyticsModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="an-models@example.com", password="pw-12345-test", name="Owner")

    def test_metric_key_unique_per_user(self):
        Metric.objects.create(user=self.user, key="mrr", name="MRR")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Metric.objects.create(user=self.user, key="mrr", name="Other")

    def test_other_user_can_reuse_key(self):
        other = User.objects.create_user(email="an-models2@example.com", password="pw-12345-test", name="Other")
        Metric.objects.create(user=self.user, key="mrr", name="MRR")
        Metric.objects.create(user=other, key="mrr", name="MRR")

    def test_defaults(self):
        metric = Metric.objects.create(user=self.user, key="k", name="K")
        self.assertEqual(metric.kind, "gauge")
        self.assertTrue(metric.is_active)
        self.assertEqual(Report.objects.create(user=self.user, title="R").report_type, "summary")
        self.assertEqual(AnalyticsEvent.objects.create(user=self.user, name="e").properties, {})
        self.assertEqual(str(MetricSnapshot.objects.create(metric=metric, value=3)), "%s=3" % metric.pk)
