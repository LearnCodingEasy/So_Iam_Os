from django.contrib import admin

from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "priority",
                    "progress_percent", "target_date")
    list_filter = ("status", "priority")
    search_fields = ("title", "description", "user__email")
    filter_horizontal = ("skills", "learning_goals")
