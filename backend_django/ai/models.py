from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models

from .security import decrypt_secret, encrypt_secret


class AISettings(models.Model):
    class Provider(models.TextChoices):
        OLLAMA = "ollama", "Ollama"
        OPENAI = "openai", "OpenAI"
        OPENROUTER = "openrouter", "OpenRouter"

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
    max_context_tokens = models.PositiveIntegerField(default=6000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AI Settings — {self.user}"


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


class AIPromptProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_prompt_profiles",
    )
    name = models.CharField(max_length=120)
    system_prompt = models.TextField(blank=True)
    context_instructions = models.TextField(blank=True)
    temperature = models.FloatField(null=True, blank=True)
    max_tokens = models.PositiveIntegerField(null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_user_ai_prompt_profile_name"),
        ]

    def __str__(self):
        return self.name


class AIConversation(models.Model):
    PROVIDER_OLLAMA = "ollama"
    PROVIDER_OPENAI = "openai"
    PROVIDER_OPENROUTER = "openrouter"

    PROVIDER_CHOICES = [
        (PROVIDER_OLLAMA, "Ollama"),
        (PROVIDER_OPENAI, "OpenAI"),
        (PROVIDER_OPENROUTER, "OpenRouter"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_conversations")
    title = models.CharField(max_length=255, blank=True, default="")
    provider = models.CharField(
        max_length=50, choices=PROVIDER_CHOICES, default=PROVIDER_OLLAMA)
    model = models.CharField(max_length=255, blank=True, default="")
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [models.Index(fields=["user", "-updated_at"]),
                   models.Index(fields=["user", "is_active"])]

    def __str__(self):
        return self.title or f"AI Conversation #{self.pk}"


class AIMessage(models.Model):
    ROLE_SYSTEM = "system"
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_CHOICES = [(ROLE_SYSTEM, "System"), (ROLE_USER,
                                              "User"), (ROLE_ASSISTANT, "Assistant")]

    conversation = models.ForeignKey(
        AIConversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    provider = models.CharField(max_length=50, blank=True, default="")
    model = models.CharField(max_length=255, blank=True, default="")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["conversation", "created_at"])]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"


# backend_django/ai/models.py


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
        fernet = Fernet(settings.ENCRYPTION_KEY.encode() if hasattr(
            settings, 'ENCRYPTION_KEY') else Fernet.generate_key())
        self.api_key_encrypted = fernet.encrypt(raw_key.encode()).decode()

    def get_api_key(self):
        if not self.api_key_encrypted:
            return None
        fernet = Fernet(settings.ENCRYPTION_KEY.encode())
        return fernet.decrypt(self.api_key_encrypted.encode()).decode()

    @property
    def api_key(self):
        return self.get_api_key()

    def __str__(self):
        return f"{self.name} ({self.provider_type})"
