from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from ai_tools_laboratory.models import Tool, ToolCategory, ToolExecution

User = get_user_model()


class ToolModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="lab-models@example.com", password="pw-12345-test", name="Owner")

    def test_tool_defaults(self):
        tool = Tool.objects.create(user=self.user, name="Cursor")
        self.assertEqual(tool.status, Tool.STATUS_EVALUATING)
        self.assertEqual(tool.tags, [])
        self.assertEqual(str(tool), "Cursor")

    def test_category_name_unique_per_user(self):
        ToolCategory.objects.create(user=self.user, name="Coding")
        with self.assertRaises(IntegrityError), transaction.atomic():
            ToolCategory.objects.create(user=self.user, name="Coding")

    def test_execution_defaults_to_pending(self):
        tool = Tool.objects.create(user=self.user, name="Cursor")
        self.assertEqual(ToolExecution.objects.create(user=self.user, tool=tool).status, "pending")
