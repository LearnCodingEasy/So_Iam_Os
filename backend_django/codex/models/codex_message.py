from django.db import models
from codex.models.codex_conversation import CodexConversation


class CodexMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    ]

    conversation = models.ForeignKey(
        CodexConversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )
    content = models.TextField()
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
