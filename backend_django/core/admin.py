from django.contrib import admin
from .models import UserLearningSettings

@admin.register(UserLearningSettings)
class UserLearningSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "daily_learning_tasks", "current_learning_goal", "task_generation_enabled", "preferred_learning_time", "updated_at")
    list_filter = ("task_generation_enabled",)
    search_fields = ("user__email", "user__name", "current_learning_goal__title")
