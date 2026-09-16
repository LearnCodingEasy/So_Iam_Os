from django.conf import settings
from django.db import models


class AIConversation(models.Model):
    """
    Represents one AI conversation/session.
    """

    PROVIDER_OLLAMA = "ollama"
    PROVIDER_OPENROUTER = "openrouter"

    PROVIDER_CHOICES = [
        (PROVIDER_OLLAMA, "Ollama"),
        (PROVIDER_OPENROUTER, "OpenRouter"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_conversations",
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    provider = models.CharField(
        max_length=50,
        choices=PROVIDER_CHOICES,
        default=PROVIDER_OLLAMA,
    )

    model = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    is_active = models.BooleanField(
        default=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["user", "-updated_at"]),
            models.Index(fields=["user", "is_active"]),
        ]

    def __str__(self):
        return self.title or f"AI Conversation #{self.pk}"


class AIMessage(models.Model):
    """
    A single message inside an AI conversation.
    """

    ROLE_SYSTEM = "system"
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"

    ROLE_CHOICES = [
        (ROLE_SYSTEM, "System"),
        (ROLE_USER, "User"),
        (ROLE_ASSISTANT, "Assistant"),
    ]

    conversation = models.ForeignKey(
        AIConversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )

    content = models.TextField()

    provider = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )

    model = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["conversation", "created_at"]),
        ]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
