from datetime import date

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from revenue.models import RecurringRevenue, RevenueRecord, RevenueSource, RevenueStream
from sales.models import Sale

User = get_user_model()


class RevenueModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="rev-models@example.com", password="pw-12345-test", name="Owner")
        self.source = RevenueSource.objects.create(user=self.user, name="Mentoring")
        self.stream = RevenueStream.objects.create(user=self.user, source=self.source, name="1:1")

    def test_defaults(self):
        self.assertEqual(self.source.source_type, "service")
        self.assertEqual(self.stream.status, "active")
        item = RecurringRevenue.objects.create(user=self.user, stream=self.stream, amount=10, start_date=date(2026, 1, 1))
        self.assertEqual((item.interval, item.status, item.currency), ("monthly", "active", "USD"))

    def test_one_record_per_sale(self):
        sale = Sale.objects.create(user=self.user, amount=100)
        RevenueRecord.objects.create(user=self.user, sale=sale, amount=100, received_on=date(2026, 1, 1))
        with self.assertRaises(IntegrityError), transaction.atomic():
            RevenueRecord.objects.create(user=self.user, sale=sale, amount=100, received_on=date(2026, 1, 2))

    def test_many_records_without_sale_are_allowed(self):
        for day in (1, 2):
            RevenueRecord.objects.create(user=self.user, amount=5, received_on=date(2026, 1, day))
        self.assertEqual(RevenueRecord.objects.count(), 2)

    def test_deleting_a_sale_keeps_the_revenue_record(self):
        sale = Sale.objects.create(user=self.user, amount=100)
        record = RevenueRecord.objects.create(user=self.user, sale=sale, amount=100, received_on=date(2026, 1, 1))
        sale.delete()
        record.refresh_from_db()
        self.assertIsNone(record.sale)
