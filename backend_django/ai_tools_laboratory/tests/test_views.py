from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from ai_tools_laboratory.models import Tool, ToolCategory

User = get_user_model()


class ToolApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="lab-api@example.com", password="pw-12345-test", name="Owner")
        self.other = User.objects.create_user(email="lab-api2@example.com", password="pw-12345-test", name="Other")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_authentication_required(self):
        self.assertEqual(APIClient().get("/api/ai-tools/tools/").status_code, 401)

    def test_tools_are_isolated(self):
        Tool.objects.create(user=self.other, name="Secret")
        mine = self.client.post("/api/ai-tools/tools/", {"name": "Mine"}, format="json")
        self.assertEqual(mine.status_code, 201)
        self.assertEqual([t["name"] for t in self.client.get("/api/ai-tools/tools/").json()], ["Mine"])
        foreign = Tool.objects.get(name="Secret")
        self.assertEqual(self.client.patch("/api/ai-tools/tools/%s/" % foreign.pk, {"name": "x"}, format="json").status_code, 404)
        self.assertEqual(self.client.delete("/api/ai-tools/tools/%s/" % foreign.pk).status_code, 404)

    def test_rating_range_and_filters(self):
        self.assertEqual(self.client.post("/api/ai-tools/tools/", {"name": "A", "rating": 6}, format="json").status_code, 400)
        self.client.post("/api/ai-tools/tools/", {"name": "A", "rating": 5, "status": "adopted"}, format="json")
        self.client.post("/api/ai-tools/tools/", {"name": "B"}, format="json")
        rows = self.client.get("/api/ai-tools/tools/?status=adopted").json()
        self.assertEqual([r["name"] for r in rows], ["A"])
        self.assertEqual(self.client.get("/api/ai-tools/tools/?status=adopted&category=abc").json(), [])

    def test_cannot_attach_foreign_category(self):
        foreign = ToolCategory.objects.create(user=self.other, name="Theirs")
        response = self.client.post("/api/ai-tools/tools/", {"name": "A", "category": foreign.pk}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_duplicate_category_name_rejected(self):
        self.assertEqual(self.client.post("/api/ai-tools/categories/", {"name": "Coding"}, format="json").status_code, 201)
        self.assertEqual(self.client.post("/api/ai-tools/categories/", {"name": "coding"}, format="json").status_code, 400)

    def test_configuration_rejects_credentials(self):
        tool = Tool.objects.create(user=self.user, name="A")
        bad = self.client.post("/api/ai-tools/configurations/", {"tool": tool.pk, "name": "c", "settings": {"api_key": "sk-123"}}, format="json")
        self.assertEqual(bad.status_code, 400)
        ok = self.client.post("/api/ai-tools/configurations/", {"tool": tool.pk, "name": "c", "settings": {"temperature": 0.2}}, format="json")
        self.assertEqual(ok.status_code, 201)

    def test_execution_configuration_must_match_tool(self):
        a = Tool.objects.create(user=self.user, name="A")
        b = Tool.objects.create(user=self.user, name="B")
        config = self.client.post("/api/ai-tools/configurations/", {"tool": a.pk, "name": "c"}, format="json").json()
        response = self.client.post("/api/ai-tools/executions/", {"tool": b.pk, "configuration": config["id"]}, format="json")
        self.assertEqual(response.status_code, 400)
        good = self.client.post("/api/ai-tools/executions/", {"tool": a.pk, "configuration": config["id"], "status": "succeeded"}, format="json")
        self.assertEqual(good.status_code, 201)

    def test_summary_endpoint(self):
        self.client.post("/api/ai-tools/tools/", {"name": "A", "rating": 4}, format="json")
        data = self.client.get("/api/ai-tools/tools/summary/").json()
        self.assertEqual(data["tools_total"], 1)
        self.assertEqual(data["average_rating"], 4.0)
