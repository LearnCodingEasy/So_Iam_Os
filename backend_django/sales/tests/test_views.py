from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from crm.models import Contact
from sales.models import Deal, Offer, Sale

User = get_user_model()


class SalesApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="sales-api@example.com", password="pw-12345-test", name="Owner")
        self.other = User.objects.create_user(email="sales-api2@example.com", password="pw-12345-test", name="Other")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def _deal(self, **extra):
        payload = {"title": "Course", "value": "300.00"}
        payload.update(extra)
        return self.client.post("/api/sales/deals/", payload, format="json")

    def test_authentication_required(self):
        self.assertEqual(APIClient().get("/api/sales/deals/").status_code, 401)

    def test_deals_are_isolated(self):
        theirs = Deal.objects.create(user=self.other, title="Theirs")
        self._deal()
        self.assertEqual([d["title"] for d in self.client.get("/api/sales/deals/").json()], ["Course"])
        self.assertEqual(self.client.post("/api/sales/deals/%s/set-stage/" % theirs.pk, {"stage": "won"}, format="json").status_code, 404)

    def test_stage_cannot_be_set_directly(self):
        created = self._deal(stage="won").json()
        self.assertEqual(created["stage"], "prospecting")
        patched = self.client.patch("/api/sales/deals/%s/" % created["id"], {"stage": "won"}, format="json").json()
        self.assertEqual(patched["stage"], "prospecting")

    def test_negative_value_and_bad_currency_rejected(self):
        self.assertEqual(self._deal(value="-1").status_code, 400)
        self.assertEqual(self._deal(currency="usd").status_code, 400)

    def test_foreign_contact_or_offer_rejected(self):
        contact = Contact.objects.create(user=self.other, first_name="X")
        offer = Offer.objects.create(user=self.other, name="O")
        self.assertEqual(self._deal(contact=contact.pk).status_code, 400)
        self.assertEqual(self._deal(offer=offer.pk).status_code, 400)

    def test_win_flow_creates_sale_and_locks_deal(self):
        deal = self._deal().json()
        won = self.client.post("/api/sales/deals/%s/set-stage/" % deal["id"], {"stage": "won"}, format="json")
        self.assertEqual(won.status_code, 200)
        self.assertEqual(won.json()["stage"], "won")
        sales = self.client.get("/api/sales/sales/").json()
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0]["amount"], "300.00")
        again = self.client.post("/api/sales/deals/%s/set-stage/" % deal["id"], {"stage": "lost", "lost_reason": "x"}, format="json")
        self.assertEqual(again.status_code, 409)
        locked = self.client.patch("/api/sales/deals/%s/" % deal["id"], {"value": "1.00"}, format="json")
        self.assertEqual(locked.status_code, 400)

    def test_lost_needs_reason(self):
        deal = self._deal().json()
        url = "/api/sales/deals/%s/set-stage/" % deal["id"]
        self.assertEqual(self.client.post(url, {"stage": "lost"}, format="json").status_code, 409)
        self.assertEqual(self.client.post(url, {"stage": "lost", "lost_reason": "Price"}, format="json").status_code, 200)

    def test_pipeline_endpoint(self):
        self._deal()
        data = self.client.get("/api/sales/deals/pipeline/").json()
        self.assertEqual(data["open_count"], 1)
        self.assertEqual(data["stages"]["prospecting"]["value"], {"USD": 300.0})

    def test_sale_rules_and_refund(self):
        self.assertEqual(self.client.post("/api/sales/sales/", {"amount": "0"}, format="json").status_code, 400)
        sale = self.client.post("/api/sales/sales/", {"amount": "50.00", "status": "refunded"}, format="json").json()
        self.assertEqual(sale["status"], "completed")
        refunded = self.client.post("/api/sales/sales/%s/refund/" % sale["id"])
        self.assertEqual(refunded.json()["status"], "refunded")
        self.assertEqual(self.client.post("/api/sales/sales/%s/refund/" % sale["id"]).status_code, 409)

    def test_activity_requires_owned_deal(self):
        theirs = Deal.objects.create(user=self.other, title="Theirs")
        bad = self.client.post("/api/sales/activities/", {"deal": theirs.pk, "activity_type": "call"}, format="json")
        self.assertEqual(bad.status_code, 400)
        mine = self._deal().json()["id"]
        ok = self.client.post("/api/sales/activities/", {"deal": mine, "activity_type": "call"}, format="json")
        self.assertEqual(ok.status_code, 201)
