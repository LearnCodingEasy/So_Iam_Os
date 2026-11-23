from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from revenue.models import RevenueRecord, RevenueSource, RevenueStream
from sales.models import Sale

User = get_user_model()


class RevenueApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="rev-api@example.com", password="pw-12345-test", name="Owner")
        self.other = User.objects.create_user(email="rev-api2@example.com", password="pw-12345-test", name="Other")
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.source = RevenueSource.objects.create(user=self.user, name="Mentoring")
        self.stream = RevenueStream.objects.create(user=self.user, source=self.source, name="1:1")

    def _record(self, **extra):
        payload = {"amount": "100.00", "received_on": "2026-03-01"}
        payload.update(extra)
        return self.client.post("/api/revenue/records/", payload, format="json")

    def test_authentication_required(self):
        self.assertEqual(APIClient().get("/api/revenue/records/").status_code, 401)

    def test_records_are_isolated(self):
        RevenueRecord.objects.create(user=self.other, amount=1, received_on=date(2026, 1, 1))
        self.assertEqual(self._record().status_code, 201)
        self.assertEqual(len(self.client.get("/api/revenue/records/").json()), 1)

    def test_validation(self):
        self.assertEqual(self._record(amount="0").status_code, 400)
        self.assertEqual(self._record(currency="dollars").status_code, 400)
        self.assertEqual(self._record(received_on="not-a-date").status_code, 400)

    def test_foreign_stream_or_sale_rejected(self):
        theirs_source = RevenueSource.objects.create(user=self.other, name="X")
        theirs_stream = RevenueStream.objects.create(user=self.other, source=theirs_source, name="X")
        theirs_sale = Sale.objects.create(user=self.other, amount=10)
        self.assertEqual(self._record(stream=theirs_stream.pk).status_code, 400)
        self.assertEqual(self._record(sale=theirs_sale.pk).status_code, 400)
        self.assertEqual(self.client.post("/api/revenue/streams/", {"source": theirs_source.pk, "name": "n"}, format="json").status_code, 400)

    def test_sale_attribution_rules(self):
        sale = Sale.objects.create(user=self.user, amount="100.00", currency="USD")
        mismatch = self._record(sale=sale.pk, currency="EUR")
        self.assertEqual(mismatch.status_code, 400)
        ok = self._record(sale=sale.pk, stream=self.stream.pk)
        self.assertEqual(ok.status_code, 201)
        duplicate = self._record(sale=sale.pk)
        self.assertEqual(duplicate.status_code, 400)
        refunded = Sale.objects.create(user=self.user, amount=5, status="refunded")
        self.assertEqual(self._record(sale=refunded.pk).status_code, 400)

    def test_sale_with_revenue_is_locked_in_sales_api(self):
        sale = Sale.objects.create(user=self.user, amount="100.00")
        self._record(sale=sale.pk)
        response = self.client.patch("/api/sales/sales/%s/" % sale.pk, {"amount": "1.00"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_from_sale_endpoint(self):
        sale = Sale.objects.create(user=self.user, amount="80.00")
        first = self.client.post("/api/revenue/records/from-sale/", {"sale": sale.pk}, format="json")
        second = self.client.post("/api/revenue/records/from-sale/", {"sale": sale.pk}, format="json")
        self.assertEqual((first.status_code, second.status_code), (201, 200))
        self.assertEqual(first.json()["id"], second.json()["id"])
        theirs = Sale.objects.create(user=self.other, amount=1)
        self.assertEqual(self.client.post("/api/revenue/records/from-sale/", {"sale": theirs.pk}, format="json").status_code, 400)
        self.assertEqual(self.client.post("/api/revenue/records/from-sale/", {}, format="json").status_code, 400)

    def test_summary_endpoint_and_bad_dates(self):
        self._record()
        data = self.client.get("/api/revenue/records/summary/?start=2026-01-01&end=2026-12-31").json()
        self.assertEqual(data["totals"], {"USD": "100.00"})
        self.assertEqual(self.client.get("/api/revenue/records/summary/?start=bad").status_code, 400)
        self.assertEqual(self.client.get("/api/revenue/records/summary/?start=2026-02-01&end=2026-01-01").status_code, 400)

    def test_recurring_and_mrr(self):
        payload = {"stream": self.stream.pk, "amount": "1200.00", "interval": "yearly", "start_date": "2026-01-01"}
        self.assertEqual(self.client.post("/api/revenue/recurring/", payload, format="json").status_code, 201)
        bad = dict(payload, end_date="2025-01-01")
        self.assertEqual(self.client.post("/api/revenue/recurring/", bad, format="json").status_code, 400)
        data = self.client.get("/api/revenue/recurring/mrr/").json()
        self.assertEqual(data["mrr"], {"USD": "100.00"})
