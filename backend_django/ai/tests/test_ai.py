from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from ai.models import AIConversation, AIMessage, AIProviderCredential, AIBudgetPolicy, AIWorkflowDefinition
from ai.services import AIService


User = get_user_model()


class AIServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="ai_test@example.com",
            password="test-password-123",
        )

    @patch("ai.providers.get_ai_provider")
    def test_create_conversation(self, mock_provider):
        service = AIService(
            user=self.user
        )

        conversation = service.create_conversation(
            title="Test Conversation"
        )

        self.assertEqual(
            conversation.user,
            self.user,
        )

        self.assertEqual(
            conversation.title,
            "Test Conversation",
        )

    @patch("ai.providers.get_ai_provider")
    def test_chat_creates_messages(
        self,
        mock_provider,
    ):
        mock_provider.return_value.generate.return_value = {
            "content": "Hello from AI",
            "provider": "ollama",
            "model": "llama3.2",
            "raw": {},
        }

        service = AIService(
            user=self.user
        )

        result = service.chat(
            message="Hello",
        )

        conversation = result[
            "conversation"
        ]

        self.assertEqual(
            AIMessage.objects.filter(
                conversation=conversation
            ).count(),
            2,
        )

        self.assertEqual(
            result[
                "assistant_message"
            ].content,
            "Hello from AI",
        )


class AIAPITests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="api_test@example.com",
            password="test-password-123",
        )

        self.client = APIClient()

        self.client.force_authenticate(
            user=self.user
        )

    @patch("ai.api.views.ai_views.AIService.chat")
    def test_chat_endpoint(
        self,
        mock_chat,
    ):
        conversation = AIConversation.objects.create(
            user=self.user,
            provider="ollama",
            model="llama3.2",
        )

        assistant_message = AIMessage.objects.create(
            conversation=conversation,
            role="assistant",
            content="Test AI response",
            provider="ollama",
            model="llama3.2",
        )

        mock_chat.return_value = {
            "conversation": conversation,
            "user_message": AIMessage.objects.create(
                conversation=conversation,
                role="user",
                content="Hello",
            ),
            "assistant_message": assistant_message,
            "provider": "ollama",
            "model": "llama3.2",
        }

        response = self.client.post(
            "/api/ai/chat/",
            {
                "message": "Hello",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["message"]["content"],
            "Test AI response",
        )


class AIFeedbackAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="feedback_owner@example.com", password="test-password-123"
        )
        self.other_user = User.objects.create_user(
            email="feedback_other@example.com", password="test-password-123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.conversation = AIConversation.objects.create(user=self.user)
        self.message = AIMessage.objects.create(
            conversation=self.conversation, role="assistant", content="A response"
        )

    def test_feedback_is_saved_and_updated_for_owned_assistant_message(self):
        payload = {"message_id": self.message.pk, "sentiment": "like", "comment": "Useful"}
        first = self.client.post("/api/ai/feedback/", payload, format="json")
        second = self.client.post(
            "/api/ai/feedback/",
            {**payload, "sentiment": "dislike", "comment": "Needs work"},
            format="json",
        )
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(second.data["sentiment"], "dislike")
        from ai.models import AIFeedback
        self.assertEqual(AIFeedback.objects.filter(user=self.user, message=self.message).count(), 1)

    def test_feedback_cannot_reference_another_users_message(self):
        foreign_conversation = AIConversation.objects.create(user=self.other_user)
        foreign_message = AIMessage.objects.create(
            conversation=foreign_conversation, role="assistant", content="Private"
        )
        response = self.client.post(
            "/api/ai/feedback/",
            {"message_id": foreign_message.pk, "sentiment": "like"},
            format="json",
        )
        self.assertEqual(response.status_code, 404)


class AIPlatformIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="ai_platform_test@example.com",
            password="test-password-123",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_credential_delete_is_idempotent(self):
        AIProviderCredential.objects.create(user=self.user, provider="gemini")
        first = self.client.delete("/api/ai/credentials/gemini/")
        second = self.client.delete("/api/ai/credentials/gemini/")
        self.assertEqual(first.status_code, 204)
        self.assertEqual(second.status_code, 204)

    def test_workflow_definition_is_user_scoped_and_persisted(self):
        payload = {
            "name": "Test workflow",
            "graph": {"nodes": [{"id": "start"}], "edges": []},
        }
        created = self.client.post("/api/ai/workflows/", payload, format="json")
        self.assertEqual(created.status_code, 201)
        self.assertTrue(AIWorkflowDefinition.objects.filter(user=self.user, name="Test workflow").exists())
        listed = self.client.get("/api/ai/workflows/")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(len(listed.data), 1)
        second = self.client.post("/api/ai/workflows/", payload, format="json")
        self.assertEqual(second.status_code, 201)
        self.assertEqual(second.data["version"], 2)

    def test_invalid_workflow_graph_is_rejected(self):
        response = self.client.post(
            "/api/ai/workflows/",
            {"name": "Invalid", "graph": {"nodes": [{"id": "a"}], "edges": [{"source": "a", "target": "missing"}]}},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_budget_detail_cannot_modify_another_users_policy(self):
        other = User.objects.create_user(email="other_ai@example.com", password="test-password-123")
        policy = AIBudgetPolicy.objects.create(user=other, scope="user")
        response = self.client.patch(
            f"/api/ai/budgets/{policy.pk}/",
            {"enabled": False},
            format="json",
        )
        self.assertEqual(response.status_code, 404)

class AIProviderConnectivityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="provider_test@example.com",
            password="test-password-123",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch("ai.api.views.ai_views.get_ai_provider")
    def test_provider_test_executes_generation_with_selected_model(self, mock_get_provider):
        mock_get_provider.return_value.generate.return_value = {
            "content": "OK",
            "provider": "openai",
            "model": "gpt-4o-mini",
        }
        response = self.client.post(
            "/api/ai/providers/openai/test/",
            {"model": "gpt-4o-mini"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["connected"])
        self.assertTrue(response.data["generation_verified"])
        self.assertEqual(response.data["model"], "gpt-4o-mini")
        mock_get_provider.return_value.generate.assert_called_once()
        self.assertEqual(
            mock_get_provider.return_value.generate.call_args.kwargs["model"],
            "gpt-4o-mini",
        )

    @patch("ai.api.views.ai_views.get_ai_provider")
    def test_provider_test_rejects_empty_generation(self, mock_get_provider):
        mock_get_provider.return_value.generate.return_value = {
            "content": "   ",
            "provider": "gemini",
            "model": "gemini-2.5-flash",
        }
        response = self.client.post(
            "/api/ai/providers/gemini/test/",
            {"model": "gemini-2.5-flash"},
            format="json",
        )
        self.assertEqual(response.status_code, 502)
        self.assertFalse(response.data["generation_verified"])

    def test_provider_test_validates_model_length(self):
        response = self.client.post(
            "/api/ai/providers/openai/test/",
            {"model": "x" * 256},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
