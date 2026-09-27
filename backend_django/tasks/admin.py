from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "scheduled_date",
                    "status", "priority", "goal")
    list_filter = ("status", "priority", "scheduled_date")
    search_fields = ("title", "description", "user__email")
    ordering = ("scheduled_date", "sort_order")
