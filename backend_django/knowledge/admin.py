from django.contrib import admin

from .models import KnowledgeFile, KnowledgeItem


@admin.register(KnowledgeItem)
class KnowledgeItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "knowledge_type",
        "user",
        "visibility",
        "is_archived",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "knowledge_type",
        "visibility",
        "is_archived",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "content",
        "source_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )


@admin.register(KnowledgeFile)
class KnowledgeFileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "original_name",
        "knowledge",
        "file_type",
        "mime_type",
        "file_size",
        "created_at",
    )

    list_filter = (
        "file_type",
        "created_at",
    )

    search_fields = (
        "original_name",
        "description",
        "knowledge__title",
    )

    readonly_fields = (
        "original_name",
        "file_type",
        "mime_type",
        "file_size",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )
