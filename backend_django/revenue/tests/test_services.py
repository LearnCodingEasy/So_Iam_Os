from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from revenue.models import RecurringRevenue, RevenueRecord, RevenueSource, RevenueStream
from revenue.services import revenue_service
from sales.models import Sale

User = get_user_model()


class RevenueServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="rev-svc@example.com", password="pw-12345-test", name="Owner")
        self.source = RevenueSource.objects.create(user=self.user, name="Mentoring")
        self.stream = RevenueStream.objects.create(user=self.user, source=self.source, name="1:1")

    def test_record_from_sale_is_idempotent(self):
        sale = Sale.objects.create(user=self.user, amount=Decimal("250.00"), currency="EUR", reference="INV-1")
        record, created = revenue_service.record_from_sale(self.user, sale)
        again, created_again = revenue_service.record_from_sale(self.user, sale)
        self.assertTrue(created)
        self.assertFalse(created_again)
        self.assertEqual(record.pk, again.pk)
        self.assertEqual((record.amount, record.currency, record.reference), (Decimal("250.00"), "EUR", "INV-1"))
        self.assertEqual(RevenueRecord.objects.count(), 1)

    def test_refunded_or_foreign_sales_cannot_be_recognised(self):
        refunded = Sale.objects.create(user=self.user, amount=10, status="refunded")
        with self.assertRaises(revenue_service.RevenueError):
            revenue_service.record_from_sale(self.user, refunded)
        other = User.objects.create_user(email="rev-svc2@example.com", password="pw-12345-test", name="Other")
        theirs = Sale.objects.create(user=other, amount=10)
        with self.assertRaises(revenue_service.RevenueError):
            revenue_service.record_from_sale(self.user, theirs)

    def test_summary_groups_by_currency_month_and_source(self):
        RevenueRecord.objects.create(user=self.user, stream=self.stream, amount=Decimal("100.10"), received_on=date(2026, 1, 5))
        RevenueRecord.objects.create(user=self.user, stream=self.stream, amount=Decimal("50.05"), received_on=date(2026, 2, 1))
        RevenueRecord.objects.create(user=self.user, amount=Decimal("10"), currency="EUR", received_on=date(2026, 2, 2))
        result = revenue_service.summary(self.user)
        self.assertEqual(result["totals"], {"EUR": "10.00", "USD": "150.15"})
        self.assertEqual(result["by_month"]["USD"], {"2026-01": "100.10", "2026-02": "50.05"})
        self.assertEqual(result["by_source"]["USD"], {"Mentoring": "150.15"})
        self.assertEqual(result["by_source"]["EUR"], {"Unattributed": "10.00"})

    def test_summary_period_and_isolation(self):
        other = User.objects.create_user(email="rev-svc3@example.com", password="pw-12345-test", name="Other")
        RevenueRecord.objects.create(user=other, amount=999, received_on=date(2026, 1, 5))
        RevenueRecord.objects.create(user=self.user, amount=5, received_on=date(2026, 1, 5))
        RevenueRecord.objects.create(user=self.user, amount=7, received_on=date(2026, 3, 5))
        result = revenue_service.summary(self.user, start=date(2026, 3, 1), end=date(2026, 3, 31))
        self.assertEqual(result["totals"], {"USD": "7.00"})
        self.assertEqual(revenue_service.summary(self.user)["count"], 2)

    def test_mrr_normalises_intervals_and_skips_inactive(self):
        def add(amount, interval, **extra):
            return RecurringRevenue.objects.create(
                user=self.user, stream=self.stream, amount=amount, interval=interval,
                start_date=date(2026, 1, 1), **extra)
        add(100, "monthly")
        add(300, "quarterly")
        add(1200, "yearly")
        add(500, "monthly", status="paused")
        add(500, "monthly", end_date=date(2026, 2, 1))
        result = revenue_service.monthly_recurring_revenue(self.user, on=date(2026, 6, 1))
        self.assertEqual(result["active_items"], 3)
        self.assertEqual(result["mrr"], {"USD": "300.00"})
        self.assertEqual(result["arr"], {"USD": "3600.00"})
