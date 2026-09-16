from django.contrib import admin

from .models import (
    Skill,
    LearningGoal,
    LearningPath,
    LearningTopic,
    LearningProgress,
    Assessment,
    AssessmentAttempt,
)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(LearningGoal)
class LearningGoalAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "skill",
        "target_level",
        "status",
        "target_date",
        "created_at",
    )

    list_filter = (
        "status",
        "target_level",
    )

    search_fields = (
        "title",
        "description",
        "reason",
    )


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "goal",
        "status",
        "created_at",
    )

    list_filter = ("status",)

    search_fields = (
        "title",
        "description",
    )


@admin.register(LearningTopic)
class LearningTopicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "path",
        "skill",
        "order",
        "status",
    )

    list_filter = ("status",)

    search_fields = (
        "title",
        "description",
    )

    ordering = (
        "path",
        "order",
    )


@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "topic",
        "progress_percent",
        "practice_completed",
        "last_activity_at",
        "updated_at",
    )

    list_filter = (
        "practice_completed",
    )

    search_fields = (
        "notes",
    )


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "assessment_type",
        "passing_score",
        "is_active",
    )

    list_filter = (
        "assessment_type",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "assessment",
        "score",
        "passed",
        "attempted_at",
    )

    list_filter = (
        "passed",
    )

    search_fields = (
        "feedback",
    )
