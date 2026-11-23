from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from sales.models import Deal, Offer, Sale, SalesActivity

User = get_user_model()


class SalesModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="sales-models@example.com", password="pw-12345-test", name="Owner")

    def test_defaults(self):
        deal = Deal.objects.create(user=self.user, title="Course")
        self.assertEqual(deal.stage, "prospecting")
        self.assertEqual(deal.value, Decimal("0"))
        self.assertEqual(deal.currency, "USD")
        self.assertEqual(Offer.objects.create(user=self.user, name="Mentoring").status, "draft")
        self.assertEqual(Sale.objects.create(user=self.user, amount=10).status, "completed")

    def test_open_stages(self):
        self.assertEqual(set(Deal.OPEN_STAGES), {"prospecting", "qualified", "proposal", "negotiation"})

    def test_deleting_offer_keeps_deal_and_sale(self):
        offer = Offer.objects.create(user=self.user, name="X")
        deal = Deal.objects.create(user=self.user, title="D", offer=offer)
        offer.delete()
        deal.refresh_from_db()
        self.assertIsNone(deal.offer)
        SalesActivity.objects.create(user=self.user, deal=deal)
        deal.delete()
        self.assertEqual(SalesActivity.objects.count(), 0)
