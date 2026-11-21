from django.conf import settings
from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexConversation(models.Model):
    project = models.ForeignKey(
        ProjectRegistry,
        on_delete=models.CASCADE,
        related_name="codex_conversations",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=240, blank=True)
    provider = models.CharField(
        max_length=40,
        default="local",
        choices=[
            ("local", "Local"),
            ("openai", "OpenAI"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
