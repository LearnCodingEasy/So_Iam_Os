
# learning/models.py

import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone


SCORE_VALIDATORS = [
    MinValueValidator(0),
    MaxValueValidator(100),
]

PERCENT_VALIDATORS = [
    MinValueValidator(0),
    MaxValueValidator(100),
]

MINUTES_VALIDATORS = [MinValueValidator(0)]


class Skill(models.Model):
    class Level(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"
        EXPERT = "expert", "Expert"

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["category", "is_active"]),
        ]

    def __str__(self):
        return self.name


class LearningGoal(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        PAUSED = "paused", "Paused"
        ARCHIVED = "archived", "Archived"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_goals",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="learning_goals",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    reason = models.TextField(blank=True)

    current_level = models.CharField(
        max_length=20,
        choices=Skill.Level.choices,
        blank=True,
    )
    target_level = models.CharField(
        max_length=20,
        choices=Skill.Level.choices,
        default=Skill.Level.INTERMEDIATE,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    target_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "target_date"]),
        ]

    def __str__(self):
        return self.title


class LearningPath(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        PAUSED = "paused", "Paused"
        ARCHIVED = "archived", "Archived"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_paths",
    )
    goal = models.ForeignKey(
        LearningGoal,
        on_delete=models.CASCADE,
        related_name="paths",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["goal", "status"]),
        ]

    def clean(self):
        super().clean()
        if self.goal_id and self.user_id:
            if self.goal.user_id != self.user_id:
                raise ValidationError(
                    {"goal": "Goal must belong to the same user."}
                )

    def __str__(self):
        return self.title


class LearningTopic(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        SKIPPED = "skipped", "Skipped"

    class Difficulty(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    path = models.ForeignKey(
        LearningPath,
        on_delete=models.CASCADE,
        related_name="topics",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="learning_topics",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        blank=True,
    )
    estimated_minutes = models.PositiveIntegerField(
        default=0,
        validators=MINUTES_VALIDATORS,
    )

    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="unlocked_topics",
    )

    knowledge_item = models.ForeignKey(
        "knowledge.KnowledgeItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="learning_topics",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]
        indexes = [
            models.Index(fields=["path", "order"]),
            models.Index(fields=["path", "status"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["path", "order"],
                name="learning_topic_unique_path_order",
            ),
        ]

    def clean(self):
        super().clean()
        if self.pk and self.prerequisites.filter(pk=self.pk).exists():
            raise ValidationError(
                {"prerequisites": "A topic cannot depend on itself."}
            )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    class ContentFormat(models.TextChoices):
        TEXT = "text", "Plain text"
        MARKDOWN = "markdown", "Markdown"
        STRUCTURED = "structured", "Structured JSON"

    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    content_format = models.CharField(
        max_length=20,
        choices=ContentFormat.choices,
        default=ContentFormat.MARKDOWN,
    )

    order = models.PositiveIntegerField(default=0)
    estimated_minutes = models.PositiveIntegerField(
        default=0,
        validators=MINUTES_VALIDATORS,
    )

    learning_objectives = models.JSONField(default=list, blank=True)
    key_concepts = models.JSONField(default=list, blank=True)
    examples = models.JSONField(default=list, blank=True)
    practical_instructions = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]
        indexes = [
            models.Index(fields=["topic", "order"]),
        ]

    def clean(self):
        super().clean()
        for field in (
            "learning_objectives",
            "key_concepts",
            "examples",
            "practical_instructions",
        ):
            value = getattr(self, field)
            if not isinstance(value, list):
                raise ValidationError({field: "Must be a JSON list."})

    def __str__(self):
        return self.title


class LearningResource(models.Model):
    class ResourceType(models.TextChoices):
        WEBSITE = "website", "Website"
        DOCUMENTATION = "documentation", "Documentation"
        ARTICLE = "article", "Article"
        BOOK = "book", "Book"
        VIDEO = "video", "Video"
        FILE = "file", "File"
        IMAGE = "image", "Image"
        NOTE = "note", "Personal note"
        CODE = "code", "Code example"
        OTHER = "other", "Other"

    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="resources",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resources",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    reference_type = models.CharField(
        max_length=30,
        choices=ResourceType.choices,
        default=ResourceType.WEBSITE,
    )

    url = models.URLField(blank=True)
    file = models.FileField(
        upload_to="learning/resources/%Y/%m/",
        null=True,
        blank=True,
    )
    content = models.TextField(blank=True)
    caption = models.CharField(max_length=255, blank=True)

    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]
        indexes = [
            models.Index(fields=["topic", "order"]),
        ]

    def clean(self):
        super().clean()

        if self.lesson_id and self.topic_id:
            if self.lesson.topic_id != self.topic_id:
                raise ValidationError(
                    {"lesson": "Lesson must belong to this topic."}
                )

        if self.reference_type == self.ResourceType.FILE and not self.file:
            raise ValidationError(
                {"file": "A file is required for file resources."}
            )

        if self.reference_type in {
            self.ResourceType.WEBSITE,
            self.ResourceType.DOCUMENTATION,
            self.ResourceType.ARTICLE,
            self.ResourceType.VIDEO,
        } and not self.url:
            raise ValidationError(
                {"url": "A URL is required for this resource type."}
            )

    def __str__(self):
        return self.title


class LearningNote(models.Model):
    class NoteType(models.TextChoices):
        GENERAL = "general", "General"
        SUMMARY = "summary", "Summary"
        QUESTION = "question", "Question"
        INSIGHT = "insight", "Insight"
        EXAMPLE = "example", "Example"
        CONFUSION = "confusion", "Confusion"
        REVISION = "revision", "Revision"
        REFLECTION = "reflection", "Reflection"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_notes",
    )
    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notes",
    )
    knowledge_item = models.ForeignKey(
        "knowledge.KnowledgeItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="learning_notes",
    )

    note_type = models.CharField(
        max_length=20,
        choices=NoteType.choices,
        default=NoteType.GENERAL,
    )
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["user", "topic"]),
            models.Index(fields=["user", "note_type"]),
        ]

    def clean(self):
        super().clean()
        if self.lesson_id and self.topic_id:
            if self.lesson.topic_id != self.topic_id:
                raise ValidationError(
                    {"lesson": "Lesson must belong to this topic."}
                )

    def __str__(self):
        return self.title or f"Note: {self.topic}"


class LearningProgress(models.Model):
    class Mastery(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        BEGINNER = "beginner", "Beginner"
        DEVELOPING = "developing", "Developing"
        COMPETENT = "competent", "Competent"
        ADVANCED = "advanced", "Advanced"
        MASTERED = "mastered", "Mastered"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_progress",
    )
    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="progress_records",
    )

    progress_percent = models.PositiveSmallIntegerField(
        default=0,
        validators=PERCENT_VALIDATORS,
    )
    practice_completed = models.BooleanField(default=False)

    # Legacy field retained during migration.
    notes = models.TextField(blank=True)

    mastery_level = models.CharField(
        max_length=20,
        choices=Mastery.choices,
        default=Mastery.NOT_STARTED,
    )
    last_ai_score = models.FloatField(
        null=True,
        blank=True,
        validators=SCORE_VALIDATORS,
    )
    needs_review = models.BooleanField(default=False)

    lesson_completed = models.BooleanField(default=False)
    quick_check_completed = models.BooleanField(default=False)
    assessment_completed = models.BooleanField(default=False)

    last_activity_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["topic", "user"],
                name="unique_learning_progress_per_user_topic",
            ),
            models.CheckConstraint(
                condition=Q(progress_percent__gte=0)
                & Q(progress_percent__lte=100),
                name="learning_progress_percent_0_100",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "needs_review"]),
            models.Index(fields=["user", "last_activity_at"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.topic} - {self.progress_percent}%"


class LearningSession(models.Model):
    class ActivityType(models.TextChoices):
        LESSON = "lesson", "Lesson"
        PRACTICE = "practice", "Practice"
        ASSESSMENT = "assessment", "Assessment"
        REVIEW = "review", "Review"
        READING = "reading", "Reading"
        OTHER = "other", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_sessions",
    )
    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sessions",
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        default=ActivityType.LESSON,
    )
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(
        default=0,
        validators=MINUTES_VALIDATORS,
    )
    completed = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["user", "started_at"]),
            models.Index(fields=["topic", "started_at"]),
        ]

    def clean(self):
        super().clean()
        if self.ended_at and self.ended_at < self.started_at:
            raise ValidationError(
                {"ended_at": "End time cannot precede start time."}
            )
        if self.lesson_id and self.topic_id:
            if self.lesson.topic_id != self.topic_id:
                raise ValidationError(
                    {"lesson": "Lesson must belong to this topic."}
                )

    def __str__(self):
        return f"{self.user} - {self.topic} - {self.started_at}"


class Assessment(models.Model):
    class Type(models.TextChoices):
        QUIZ = "quiz", "Quiz"
        QUICK_CHECK = "quick_check", "Quick Check"
        PRACTICAL = "practical", "Practical"
        PROJECT = "project", "Project"

    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="assessments",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    assessment_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.QUIZ,
    )
    passing_score = models.PositiveSmallIntegerField(
        default=70,
        validators=SCORE_VALIDATORS,
    )
    estimated_minutes = models.PositiveIntegerField(
        default=0,
        validators=MINUTES_VALIDATORS,
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]
        indexes = [
            models.Index(fields=["topic", "assessment_type", "is_active"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(passing_score__gte=0)
                & Q(passing_score__lte=100),
                name="assessment_passing_score_0_100",
            ),
        ]

    def __str__(self):
        return self.title


class AssessmentQuestion(models.Model):
    class Type(models.TextChoices):
        SINGLE_CHOICE = "single_choice", "Single choice"
        MULTIPLE_SELECT = "multiple_select", "Multiple select"
        TRUE_FALSE = "true_false", "True / False"
        SHORT_ANSWER = "short_answer", "Short answer"
        PRACTICAL = "practical", "Practical task"

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_type = models.CharField(
        max_length=30,
        choices=Type.choices,
    )
    prompt = models.TextField()
    explanation = models.TextField(blank=True)
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    is_required = models.BooleanField(default=True)

    # Private grading data; exclude from learner serializers.
    grading_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["order", "id"]
        indexes = [
            models.Index(fields=["assessment", "order"]),
        ]

    def __str__(self):
        return f"{self.assessment}: Q{self.order}"


class AssessmentChoice(models.Model):
    question = models.ForeignKey(
        AssessmentQuestion,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    # Never expose this field in learner-facing serializers.
    is_correct = models.BooleanField(default=False)

    feedback = models.TextField(blank=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text[:100]


class AssessmentAttempt(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assessment_attempts",
    )

    score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=SCORE_VALIDATORS,
    )
    passed = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)

    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    attempt_number = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-started_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["assessment", "user", "attempt_number"],
                name="unique_assessment_attempt_number",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "assessment", "started_at"]),
        ]

    def clean(self):
        super().clean()
        if self.completed_at and self.completed_at < self.started_at:
            raise ValidationError(
                {"completed_at": "Cannot precede start time."}
            )

    def __str__(self):
        return f"{self.user} - {self.assessment} - {self.score}"


class AssessmentResponse(models.Model):
    attempt = models.ForeignKey(
        AssessmentAttempt,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    question = models.ForeignKey(
        AssessmentQuestion,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    selected_choices = models.ManyToManyField(
        AssessmentChoice,
        blank=True,
        related_name="responses",
    )
    text_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(null=True, blank=True)
    points_awarded = models.FloatField(default=0)
    feedback = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["attempt", "question"],
                name="unique_response_per_attempt_question",
            ),
        ]

    def clean(self):
        super().clean()
        if self.attempt_id and self.question_id:
            if self.attempt.assessment_id != self.question.assessment_id:
                raise ValidationError(
                    "Question must belong to the attempt's assessment."
                )

    def __str__(self):
        return f"Response: {self.question_id}"


class KnowledgeApplication(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        REVIEWED = "reviewed", "Reviewed"

    class ApplicationType(models.TextChoices):
        CODE = "code", "Code"
        PROJECT = "project", "Project"
        EXPLANATION = "explanation", "Explanation"
        WORKFLOW = "workflow", "Workflow"
        EXPERIMENT = "experiment", "Experiment"
        OTHER = "other", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="knowledge_applications",
    )
    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
    )
    knowledge_item = models.ForeignKey(
        "knowledge.KnowledgeItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="learning_applications",
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    application_type = models.CharField(
        max_length=20,
        choices=ApplicationType.choices,
        default=ApplicationType.OTHER,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["user", "topic", "status"]),
        ]

    def clean(self):
        super().clean()
        if self.lesson_id and self.topic_id:
            if self.lesson.topic_id != self.topic_id:
                raise ValidationError(
                    {"lesson": "Lesson must belong to this topic."}
                )

    def __str__(self):
        return f"{self.title} - {self.user}"


class ApplicationSubmission(models.Model):
    """Immutable snapshot of an application submitted for review."""

    application = models.ForeignKey(
        KnowledgeApplication,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    version = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-version"]
        constraints = [
            models.UniqueConstraint(
                fields=["application", "version"],
                name="unique_application_submission_version",
            ),
        ]

    def __str__(self):
        return f"{self.application} v{self.version}"


class ApplicationReview(models.Model):
    class Mastery(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        DEVELOPING = "developing", "Developing"
        COMPETENT = "competent", "Competent"
        ADVANCED = "advanced", "Advanced"
        MASTERED = "mastered", "Mastered"

    submission = models.ForeignKey(
        ApplicationSubmission,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    # Compatibility link to the parent application.
    application = models.ForeignKey(
        KnowledgeApplication,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    score = models.FloatField(validators=SCORE_VALIDATORS)
    mastery_level = models.CharField(
        max_length=20,
        choices=Mastery.choices,
        default=Mastery.DEVELOPING,
    )

    understood = models.JSONField(default=list, blank=True)
    applied = models.JSONField(default=list, blank=True)
    strengths = models.JSONField(default=list, blank=True)
    weaknesses = models.JSONField(default=list, blank=True)
    errors = models.JSONField(default=list, blank=True)
    needs_review = models.JSONField(default=list, blank=True)
    knowledge_gaps = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)

    feedback = models.TextField(blank=True)
    ai_metadata = models.JSONField(default=dict, blank=True)
    reviewed_by = models.CharField(max_length=100, default="ai")
    reviewed_at = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-reviewed_at"]
        indexes = [
            models.Index(fields=["application", "reviewed_at"]),
        ]

    def clean(self):
        super().clean()
        if self.submission_id and self.application_id:
            if self.submission.application_id != self.application_id:
                raise ValidationError(
                    "Submission must belong to this application."
                )

    def __str__(self):
        return f"Review: {self.application.title}"


class LearningRevision(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        SKIPPED = "skipped", "Skipped"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_revisions",
    )
    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="revisions",
    )
    source_review = models.ForeignKey(
        ApplicationReview,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revision_sessions",
    )

    concepts = models.JSONField(default=list, blank=True)
    recommendation = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
    )
    scheduled_for = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    outcome = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_for", "-created_at"]
        indexes = [
            models.Index(fields=["user", "status", "scheduled_for"]),
        ]

    def clean(self):
        super().clean()
        if self.completed_at and self.started_at:
            if self.completed_at < self.started_at:
                raise ValidationError(
                    {"completed_at": "Cannot precede start time."}
                )

    def __str__(self):
        return f"Revision: {self.topic} - {self.user}"
