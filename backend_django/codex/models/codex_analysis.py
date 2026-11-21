from django.db import models
from codex.models.codex_conversation import CodexConversation


class CodexAnalysis(models.Model):
    conversation = models.ForeignKey(
        CodexConversation,
        on_delete=models.CASCADE,
        related_name="analyses",
    )

    request = models.TextField()

    provider = models.CharField(
        max_length=40,
        default="local",
    )

    result = models.JSONField(
        default=dict,
        blank=True,
    )

    context = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
