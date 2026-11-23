from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from sales.models import Deal, Offer, Sale
from sales.services import sales_service

User = get_user_model()


class SalesServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="sales-svc@example.com", password="pw-12345-test", name="Owner")
        self.offer = Offer.objects.create(user=self.user, name="Mentoring", price=500)

    def _deal(self, **extra):
        data = {"user": self.user, "title": "Deal", "value": Decimal("500"), "offer": self.offer}
        data.update(extra)
        return Deal.objects.create(**data)

    def test_open_stage_moves(self):
        deal = sales_service.set_stage(self._deal(), "qualified")
        self.assertEqual(deal.stage, "qualified")
        self.assertIsNone(deal.closed_at)

    def test_unknown_stage_rejected(self):
        with self.assertRaises(sales_service.SalesError):
            sales_service.set_stage(self._deal(), "banana")

    def test_winning_creates_exactly_one_sale(self):
        deal = sales_service.set_stage(self._deal(), "won")
        sale = Sale.objects.get(deal=deal)
        self.assertEqual((sale.amount, sale.currency, sale.offer, sale.user), (Decimal("500"), "USD", self.offer, self.user))
        self.assertIsNotNone(deal.closed_at)
        with self.assertRaises(sales_service.SalesError):
            sales_service.set_stage(deal, "negotiation")
        self.assertEqual(Sale.objects.filter(deal=deal).count(), 1)

    def test_cannot_win_a_zero_value_deal(self):
        with self.assertRaises(sales_service.SalesError):
            sales_service.set_stage(self._deal(value=0), "won")
        self.assertEqual(Sale.objects.count(), 0)

    def test_losing_requires_reason(self):
        deal = self._deal()
        with self.assertRaises(sales_service.SalesError):
            sales_service.set_stage(deal, "lost", "  ")
        lost = sales_service.set_stage(deal, "lost", "Budget")
        self.assertEqual((lost.stage, lost.lost_reason), ("lost", "Budget"))

    def test_refund_only_once(self):
        sale = Sale.objects.create(user=self.user, amount=10)
        self.assertEqual(sales_service.refund_sale(sale).status, "refunded")
        with self.assertRaises(sales_service.SalesError):
            sales_service.refund_sale(sale)

    def test_pipeline_summary(self):
        sales_service.set_stage(self._deal(), "won")
        sales_service.set_stage(self._deal(), "lost", "No budget")
        self._deal(value=100)
        summary = sales_service.pipeline_summary(self.user)
        self.assertEqual(summary["stages"]["won"], {"count": 1, "value": {"USD": 500.0}})
        self.assertEqual(summary["open_count"], 1)
        self.assertEqual(summary["win_rate"], 0.5)

    def test_win_rate_none_without_closed_deals(self):
        self.assertIsNone(sales_service.pipeline_summary(self.user)["win_rate"])
