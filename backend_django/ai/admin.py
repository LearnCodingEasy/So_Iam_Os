from django.contrib import admin

from .models import (
    AIConversation,
    AIMessage,
)


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "provider",
        "model",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "provider",
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(AIMessage)
class AIMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "role",
        "provider",
        "model",
        "created_at",
    )

    list_filter = (
        "role",
        "provider",
        "created_at",
    )

    search_fields = (
        "content",
    )

    readonly_fields = (
        "created_at",
    )
