from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import (
    AIConversation,
    AIMessage,
)
from .services import AIService


User = get_user_model()


class AIServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="ai_test@example.com",
            password="test-password-123",
        )

    @patch("ai.services.get_ai_provider")
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

    @patch("ai.services.get_ai_provider")
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

    @patch("ai.views.AIService.chat")
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
