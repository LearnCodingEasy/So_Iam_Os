
from django.conf import settings
from django.db import models


class AIPromptProfile(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_prompt_profiles"
    )

    name = models.CharField(max_length=120)

    system_prompt = models.TextField(
        blank=True,
        default=""
    )

    context_instructions = models.TextField(
        blank=True,
        default=""
    )

    temperature = models.FloatField(
        null=True,
        blank=True
    )

    max_tokens = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_user_ai_prompt_profile_name"
            )
        ]

    def __str__(self):
        return self.name
