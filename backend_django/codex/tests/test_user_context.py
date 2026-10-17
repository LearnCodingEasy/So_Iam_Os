from django.test import TestCase
from users_accounts.models import User
from goals.models import Goal
from tasks.models import Task
from knowledge.models import KnowledgeItem
from learning.models import LearningGoal, LearningPath, LearningTopic
from codex.services.user_context import build_user_context


class UserContextExportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="context-owner@example.test", password="not-a-real-secret", name="Owner")
        self.other = User.objects.create_user(email="other-owner@example.test", password="not-a-real-secret", name="Other")

    def test_export_is_scoped_to_authenticated_user(self):
        Goal.objects.create(user=self.user, title="Owner goal")
        Goal.objects.create(user=self.other, title="Other goal")
        Task.objects.create(user=self.user, title="Owner task")
        Task.objects.create(user=self.other, title="Other task")
        KnowledgeItem.objects.create(user=self.user, title="Owner note", content="private body")
        KnowledgeItem.objects.create(user=self.other, title="Other note", content="other body")
        LearningGoal.objects.create(user=self.user, title="Owner learning goal")
        LearningGoal.objects.create(user=self.other, title="Other learning goal")

        payload = build_user_context(self.user)

        self.assertEqual([item["title"] for item in payload["goals"]], ["Owner goal"])
        self.assertEqual([item["title"] for item in payload["tasks"]], ["Owner task"])
        self.assertEqual([item["title"] for item in payload["knowledge"]], ["Owner note"])
        self.assertEqual([item["title"] for item in payload["learning_goals"]], ["Owner learning goal"])
        self.assertNotIn("content", payload["knowledge"][0])

    def test_content_is_opt_in_and_bounded(self):
        KnowledgeItem.objects.create(user=self.user, title="Private note", content="secret context")
        payload = build_user_context(self.user, include_content=True, limit=500)
        self.assertEqual(payload["limits"]["per_collection"], 100)
        self.assertEqual(payload["knowledge"][0]["content"], "secret context")
        self.assertFalse(payload["knowledge"][0]["content_truncated"])
