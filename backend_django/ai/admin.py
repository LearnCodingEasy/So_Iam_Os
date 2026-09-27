from django.contrib import admin

from .models import AIConversation, AIMessage, AISettings, AIProviderCredential, AIPromptProfile


@admin.register(AISettings)
class AISettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "preferred_provider",
                    "preferred_model", "context_enabled", "updated_at")
    search_fields = ("user__email", "preferred_model")


@admin.register(AIProviderCredential)
class AIProviderCredentialAdmin(admin.ModelAdmin):
    list_display = ("user", "provider", "has_api_key", "updated_at")
    search_fields = ("user__email", "provider")

    @admin.display(boolean=True)
    def has_api_key(self, obj):
        return obj.has_api_key


@admin.register(AIPromptProfile)
class AIPromptProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_default", "updated_at")
    list_filter = ("is_default",)
    search_fields = ("name", "user__email")


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "provider",
                    "model", "is_active", "updated_at")
    list_filter = ("provider", "is_active")
    search_fields = ("title", "user__email")


@admin.register(AIMessage)
class AIMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "role",
                    "provider", "model", "created_at")
    list_filter = ("role", "provider")
    search_fields = ("content",)
