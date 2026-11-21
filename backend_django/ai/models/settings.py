from django.conf import settings
from django.db import models

from ..security import decrypt_secret, encrypt_secret

class AISettings(models.Model):
    class Provider(models.TextChoices):
        OLLAMA = "ollama", "Ollama"
        OPENAI = "openai", "OpenAI"
        OPENROUTER = "openrouter", "OpenRouter"
        GEMINI = "gemini", "Google Gemini"
        DEEPSEEK = "deepseek", "DeepSeek"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_settings",
    )
    preferred_provider = models.CharField(
        max_length=50,
        choices=Provider.choices,
        default=Provider.OLLAMA,
    )
    preferred_model = models.CharField(max_length=255, blank=True, default="")
    default_prompt_profile = models.ForeignKey(
        "ai.AIPromptProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_for_settings",
    )
    context_enabled = models.BooleanField(default=True)
    streaming_enabled = models.BooleanField(default=True)
    temperature = models.FloatField(default=0.7)
    timeout_seconds = models.PositiveIntegerField(default=35)
    fallback_enabled = models.BooleanField(default=True)
    max_context_tokens = models.PositiveIntegerField(default=6000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AI Settings — {self.user}"



