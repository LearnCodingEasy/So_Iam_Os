"""CRM -> Sales -> Revenue -> AI insight. Real ORM rows in the test DB; only the
provider call is patched (isolated automated test, not runtime evidence)."""
from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from ai.models import AIExecution
from crm.models import Contact, CustomerRelationship
from revenue.models import RevenueRecord
from sales.models import Deal, Sale

User = get_user_model()
URL = "/api/ai/insights/business/"


class BusinessInsightTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="bi@example.com", password="test-password-123")
        self.other = User.objects.create_user(email="bi2@example.com", password="test-password-123")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def _seed(self, user):
        contact = Contact.objects.create(user=user, first_name="Ada")
        CustomerRelationship.objects.create(user=user, contact=contact, stage="customer", health_score=80)
        deal = Deal.objects.create(user=user, contact=contact, title="D1", value=Decimal("1000"), stage="won")
        Deal.objects.create(user=user, contact=contact, title="D2", value=Decimal("500"), stage="proposal")
        sale = Sale.objects.create(user=user, deal=deal, contact=contact, amount=Decimal("1000"))
        RevenueRecord.objects.create(user=user, sale=sale, amount=Decimal("1000"), received_on=date.today())

    def test_snapshot_comes_from_database_and_is_user_scoped(self):
        self._seed(self.user)
        self._seed(self.other)
        data = self.client.get(URL).data
        self.assertTrue(data["has_data"])
        snap = data["snapshot"]
        self.assertEqual(snap["crm"]["contacts"], 1)
        self.assertEqual(snap["sales"]["completed_sales_amount"], 1000.0)
        self.assertEqual(snap["sales"]["open_pipeline_value"], 500.0)
        self.assertEqual(snap["revenue"]["attributed_to_sales"], 1)

    def test_no_data_refuses_without_calling_ai(self):
        with patch("ai.services.core.AIFallbackChainService.generate_completion") as gen:
            r = self.client.post(URL, {}, format="json")
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.data["error_code"], "no_business_data")
        gen.assert_not_called()

    def test_invalid_timeout_rejected(self):
        self._seed(self.user)
        r = self.client.post(URL, {"timeout": 100000}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_ai_called_with_snapshot_task_type_and_timeout(self):
        self._seed(self.user)
        fake = {"content": "Summary...", "provider": "ollama", "model": "m", "execution_id": 7}
        with patch("ai.services.core.AIFallbackChainService.generate_completion", return_value=fake) as gen:
            r = self.client.post(URL, {"provider": "ollama", "timeout": 180}, format="json")
        self.assertEqual(r.status_code, 200, r.content)
        kwargs = gen.call_args.kwargs
        self.assertEqual(kwargs["task_type"], "business_insight")
        self.assertEqual(kwargs["timeout_seconds"], 180)
        self.assertIn('"contacts": 1', kwargs["messages"][1]["content"])
        self.assertEqual(r.data["insight"], "Summary...")
