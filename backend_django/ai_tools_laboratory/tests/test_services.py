from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from rest_framework.test import APIClient

from ai_tools_laboratory.models import Tool, ToolConfiguration, ToolExecution
from ai_tools_laboratory.services import tool_service

User = get_user_model()


class ToolServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="lab-svc@example.com", password="pw-12345-test", name="Owner")

    def test_summary_counts_and_rates(self):
        a = Tool.objects.create(user=self.user, name="A", status="adopted", rating=4)
        Tool.objects.create(user=self.user, name="B", rating=2)
        ToolExecution.objects.create(user=self.user, tool=a, status="succeeded")
        ToolExecution.objects.create(user=self.user, tool=a, status="succeeded")
        ToolExecution.objects.create(user=self.user, tool=a, status="failed")
        ToolExecution.objects.create(user=self.user, tool=a, status="pending")
        summary = tool_service.laboratory_summary(self.user)
        self.assertEqual(summary["tools_total"], 2)
        self.assertEqual(summary["tools_by_status"], {"adopted": 1, "evaluating": 1})
        self.assertEqual(summary["average_rating"], 3.0)
        self.assertEqual(summary["success_rate"], round(2 / 3, 4))

    def test_summary_is_empty_for_new_user(self):
        summary = tool_service.laboratory_summary(self.user)
        self.assertEqual(summary["tools_total"], 0)
        self.assertIsNone(summary["average_rating"])
        self.assertIsNone(summary["success_rate"])

    def test_only_one_default_configuration_per_tool(self):
        client = APIClient()
        client.force_authenticate(self.user)
        tool = Tool.objects.create(user=self.user, name="A")
        first = client.post("/api/ai-tools/configurations/", {"tool": tool.pk, "name": "one", "is_default": True}, format="json")
        second = client.post("/api/ai-tools/configurations/", {"tool": tool.pk, "name": "two", "is_default": True}, format="json")
        self.assertEqual((first.status_code, second.status_code), (201, 201))
        defaults = ToolConfiguration.objects.filter(tool=tool, is_default=True)
        self.assertEqual([c.name for c in defaults], ["two"])
