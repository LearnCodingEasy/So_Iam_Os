
from django.contrib import admin

from .models import (
    Skill,
    LearningGoal,
    LearningPath,
    LearningTopic,
    Lesson,
    LearningResource,
    LearningNote,
    LearningProgress,
    LearningSession,
    Assessment,
    AssessmentQuestion,
    AssessmentChoice,
    AssessmentAttempt,
    AssessmentResponse,
    KnowledgeApplication,
    ApplicationSubmission,
    ApplicationReview,
    LearningRevision,
)


# =========================================================
# SKILLS
# =========================================================

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
        "slug",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# LEARNING GOALS
# =========================================================

@admin.register(LearningGoal)
class LearningGoalAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "skill",
        "current_level",
        "target_level",
        "status",
        "target_date",
        "completed_at",
    )

    list_filter = (
        "status",
        "current_level",
        "target_level",
        "skill",
    )

    search_fields = (
        "title",
        "description",
        "reason",
        "user__username",
        "user__email",
    )

    autocomplete_fields = (
        "user",
        "skill",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# LEARNING PATHS
# =========================================================

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "goal",
        "status",
        "started_at",
        "completed_at",
        "created_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "title",
        "description",
        "user__username",
        "goal__title",
    )

    autocomplete_fields = (
        "user",
        "goal",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# LEARNING TOPICS
# =========================================================

@admin.register(LearningTopic)
class LearningTopicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "path",
        "skill",
        "order",
        "difficulty",
        "status",
        "estimated_minutes",
    )

    list_filter = (
        "status",
        "difficulty",
        "skill",
    )

    search_fields = (
        "title",
        "description",
        "path__title",
    )

    autocomplete_fields = (
        "path",
        "skill",
        "knowledge_item",
    )

    filter_horizontal = (
        "prerequisites",
    )

    ordering = (
        "path",
        "order",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# LESSONS
# =========================================================

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "order",
        "content_format",
        "estimated_minutes",
        "is_active",
    )

    list_filter = (
        "content_format",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
        "topic__title",
    )

    autocomplete_fields = (
        "topic",
    )

    ordering = (
        "topic",
        "order",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# LEARNING RESOURCES
# =========================================================

@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "lesson",
        "reference_type",
        "order",
        "created_at",
    )

    list_filter = (
        "reference_type",
    )

    search_fields = (
        "title",
        "description",
        "url",
        "topic__title",
    )

    autocomplete_fields = (
        "topic",
        "lesson",
    )

    ordering = (
        "topic",
        "order",
    )

    readonly_fields = (
        "created_at",
    )


# =========================================================
# PERSONAL LEARNING NOTES
# =========================================================

@admin.register(LearningNote)
class LearningNoteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "topic",
        "lesson",
        "note_type",
        "updated_at",
    )

    list_filter = (
        "note_type",
    )

    search_fields = (
        "title",
        "content",
        "user__username",
        "topic__title",
    )

    autocomplete_fields = (
        "user",
        "topic",
        "lesson",
        "knowledge_item",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# LEARNING PROGRESS
# =========================================================

@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "topic",
        "progress_percent",
        "mastery_level",
        "practice_completed",
        "needs_review",
        "last_activity_at",
        "updated_at",
    )

    list_filter = (
        "mastery_level",
        "practice_completed",
        "needs_review",
        "lesson_completed",
        "quick_check_completed",
        "assessment_completed",
    )

    search_fields = (
        "user__username",
        "topic__title",
        "notes",
    )

    autocomplete_fields = (
        "user",
        "topic",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# LEARNING SESSIONS
# =========================================================

@admin.register(LearningSession)
class LearningSessionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "topic",
        "lesson",
        "activity_type",
        "started_at",
        "ended_at",
        "duration_seconds",
        "completed",
    )

    list_filter = (
        "activity_type",
        "completed",
    )

    search_fields = (
        "user__username",
        "topic__title",
        "lesson__title",
    )

    autocomplete_fields = (
        "user",
        "topic",
        "lesson",
    )

    readonly_fields = (
        "started_at",
    )


# =========================================================
# ASSESSMENTS
# =========================================================

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "assessment_type",
        "passing_score",
        "estimated_minutes",
        "order",
        "is_active",
    )

    list_filter = (
        "assessment_type",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
        "topic__title",
    )

    autocomplete_fields = (
        "topic",
    )

    ordering = (
        "topic",
        "order",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# ASSESSMENT QUESTIONS
# =========================================================

@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "assessment",
        "question_type",
        "order",
        "points",
        "is_required",
    )

    list_filter = (
        "question_type",
        "is_required",
    )

    search_fields = (
        "prompt",
        "assessment__title",
    )

    autocomplete_fields = (
        "assessment",
    )

    ordering = (
        "assessment",
        "order",
    )


# =========================================================
# ASSESSMENT CHOICES
# =========================================================

@admin.register(AssessmentChoice)
class AssessmentChoiceAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "text",
        "order",
        "is_correct",
    )

    list_filter = (
        "is_correct",
    )

    search_fields = (
        "text",
        "question__prompt",
    )

    autocomplete_fields = (
        "question",
    )

    ordering = (
        "question",
        "order",
    )


# =========================================================
# ASSESSMENT ATTEMPTS
# =========================================================

@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "assessment",
        "attempt_number",
        "score",
        "passed",
        "started_at",
        "completed_at",
    )

    list_filter = (
        "passed",
        "assessment__assessment_type",
    )

    search_fields = (
        "user__username",
        "assessment__title",
        "feedback",
    )

    autocomplete_fields = (
        "user",
        "assessment",
    )

    readonly_fields = (
        "started_at",
    )


# =========================================================
# ASSESSMENT RESPONSES
# =========================================================

@admin.register(AssessmentResponse)
class AssessmentResponseAdmin(admin.ModelAdmin):
    list_display = (
        "attempt",
        "question",
        "is_correct",
        "points_awarded",
    )

    list_filter = (
        "is_correct",
    )

    search_fields = (
        "question__prompt",
        "text_answer",
    )

    autocomplete_fields = (
        "attempt",
        "question",
    )


# =========================================================
# KNOWLEDGE APPLICATIONS
# =========================================================

@admin.register(KnowledgeApplication)
class KnowledgeApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "topic",
        "application_type",
        "status",
        "submitted_at",
        "reviewed_at",
    )

    list_filter = (
        "status",
        "application_type",
    )

    search_fields = (
        "title",
        "content",
        "user__username",
        "topic__title",
    )

    autocomplete_fields = (
        "user",
        "topic",
        "lesson",
        "knowledge_item",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# =========================================================
# APPLICATION SUBMISSIONS
# =========================================================

@admin.register(ApplicationSubmission)
class ApplicationSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "version",
        "submitted_at",
    )

    search_fields = (
        "application__title",
        "title",
        "content",
    )

    autocomplete_fields = (
        "application",
    )

    readonly_fields = (
        "submitted_at",
    )


# =========================================================
# AI APPLICATION REVIEWS
# =========================================================

@admin.register(ApplicationReview)
class ApplicationReviewAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "submission",
        "score",
        "mastery_level",
        "reviewed_by",
        "reviewed_at",
    )

    list_filter = (
        "mastery_level",
        "reviewed_by",
    )

    search_fields = (
        "application__title",
        "feedback",
    )

    autocomplete_fields = (
        "application",
        "submission",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "reviewed_at",
    )


# =========================================================
# LEARNING REVISIONS
# =========================================================

@admin.register(LearningRevision)
class LearningRevisionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "topic",
        "status",
        "scheduled_for",
        "started_at",
        "completed_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "user__username",
        "topic__title",
        "recommendation",
    )

    autocomplete_fields = (
        "user",
        "topic",
        "source_review",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
