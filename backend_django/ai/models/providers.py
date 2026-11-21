from django.conf import settings
from django.db import models
from .settings import AISettings

from ..security import decrypt_secret, encrypt_secret

class AIProviderCredential(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_provider_credentials",
    )
    provider = models.CharField(
        max_length=50, choices=AISettings.Provider.choices)
    encrypted_api_key = models.TextField(blank=True, default="")
    metadata = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=[
        ("valid", "Valid"), ("invalid", "Invalid"), ("needs_review", "Needs Review")
    ], default="needs_review")
    last_used_at = models.DateTimeField(null=True, blank=True)
    last_validated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "provider"], name="unique_user_ai_provider_credential"),
        ]
        indexes = [models.Index(fields=["user", "provider"])]

    def set_api_key(self, value):
        self.encrypted_api_key = encrypt_secret(value)

    def get_api_key(self):
        return decrypt_secret(self.encrypted_api_key)

    @property
    def has_api_key(self):
        return bool(self.encrypted_api_key)




class AIProviderConfig(models.Model):
    PROVIDER_TYPES = [
        ('ollama', 'Ollama (Local)'),
        ('openai', 'OpenAI'),
        ('gemini', 'Google Gemini'),
        ('deepseek', 'DeepSeek'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPES)
    api_key_encrypted = models.TextField(blank=True, null=True)
    api_base_url = models.URLField(blank=True, null=True)
    model_name = models.CharField(max_length=100, default="default")
    priority = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def set_api_key(self, raw_key):
        self.api_key_encrypted = encrypt_secret(raw_key)

    def get_api_key(self):
        if not self.api_key_encrypted:
            return None
        return decrypt_secret(self.api_key_encrypted)

    @property
    def api_key(self):
        # Compatibility accessor; callers must never serialize this property.
        return self.get_api_key()

    def __str__(self):
        return f"{self.name} ({self.provider_type})"



