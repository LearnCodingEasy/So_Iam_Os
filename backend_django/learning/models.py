from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Skill(models.Model):
    """
    Skill represents a capability that the user wants to learn,
    improve, measure, or master.
    """

    LEVEL_BEGINNER = "beginner"
    LEVEL_INTERMEDIATE = "intermediate"
    LEVEL_ADVANCED = "advanced"
    LEVEL_EXPERT = "expert"

    LEVEL_CHOICES = [
        (LEVEL_BEGINNER, "Beginner"),
        (LEVEL_INTERMEDIATE, "Intermediate"),
        (LEVEL_ADVANCED, "Advanced"),
        (LEVEL_EXPERT, "Expert"),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)

    description = models.TextField(blank=True)

    category = models.CharField(
        max_length=100,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class LearningGoal(models.Model):
    """
    Represents a learning objective owned by a user.
    """

    STATUS_ACTIVE = "active"
    STATUS_COMPLETED = "completed"
    STATUS_PAUSED = "paused"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_PAUSED, "Paused"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_goals",
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    skill = models.ForeignKey(
        Skill,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="learning_goals",
    )

    reason = models.TextField(
        blank=True,
        help_text="Why does the user want to achieve this goal?",
    )

    target_level = models.CharField(
        max_length=30,
        choices=Skill.LEVEL_CHOICES,
        default=Skill.LEVEL_INTERMEDIATE,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )

    target_date = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class LearningPath(models.Model):
    """
    Structured learning journey for a user.
    """

    STATUS_ACTIVE = "active"
    STATUS_COMPLETED = "completed"
    STATUS_PAUSED = "paused"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_PAUSED, "Paused"),
        (STATUS_ARCHIVED, "Archived"),
    ]

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
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class LearningTopic(models.Model):
    """
    A topic inside a learning path.
    """

    STATUS_PENDING = "pending"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_SKIPPED = "skipped"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_SKIPPED, "Skipped"),
    ]

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
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    estimated_minutes = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return self.title


class Assessment(models.Model):
    """
    Assessment used to evaluate whether the user can actually
    apply what was learned.
    """

    TYPE_QUIZ = "quiz"
    TYPE_PRACTICAL = "practical"
    TYPE_PROJECT = "project"

    TYPE_CHOICES = [
        (TYPE_QUIZ, "Quiz"),
        (TYPE_PRACTICAL, "Practical"),
        (TYPE_PROJECT, "Project"),
    ]

    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="assessments",
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    assessment_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_QUIZ,
    )

    passing_score = models.PositiveIntegerField(
        default=70,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class AssessmentAttempt(models.Model):
    """
    A user's attempt at an assessment.
    """

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

    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    passed = models.BooleanField(default=False)

    feedback = models.TextField(blank=True)

    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-attempted_at"]

    def __str__(self):
        return f"{self.user} - {self.assessment} - {self.score}%"


# ============================================================
# LEARNING PROGRESS
# ============================================================

class LearningProgress(models.Model):
    topic = models.ForeignKey(
        "learning.LearningTopic",
        on_delete=models.CASCADE,
        related_name="progress_records",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_progress",
    )

    progress_percent = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    practice_completed = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    # New
    mastery_level = models.CharField(
        max_length=20,
        choices=[
            ("not_started", "Not Started"),
            ("beginner", "Beginner"),
            ("developing", "Developing"),
            ("competent", "Competent"),
            ("advanced", "Advanced"),
            ("mastered", "Mastered"),
        ],
        default="not_started",
    )

    last_ai_score = models.FloatField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    needs_review = models.BooleanField(default=False)

    last_activity_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["topic", "user"],
                name="unique_learning_progress_per_user_topic",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.topic} - {self.progress_percent}%"


class KnowledgeApplication(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("reviewed", "Reviewed"),
    ]

    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="knowledge_applications",
    )

    knowledge_item = models.ForeignKey(
        "knowledge.KnowledgeItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
    )

    title = models.CharField(
        max_length=255,
    )

    content = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user}"


class ApplicationReview(models.Model):

    application = models.OneToOneField(
        KnowledgeApplication,
        on_delete=models.CASCADE,
        related_name="review",
    )

    # Overall result
    score = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    mastery_level = models.CharField(
        max_length=30,
        default="developing",
    )

    # What the system understood
    understood = models.JSONField(
        default=list,
        blank=True,
    )

    # What user actually applied
    applied = models.JSONField(
        default=list,
        blank=True,
    )

    # Strengths
    strengths = models.JSONField(
        default=list,
        blank=True,
    )

    # Weaknesses
    weaknesses = models.JSONField(
        default=list,
        blank=True,
    )

    # Errors
    errors = models.JSONField(
        default=list,
        blank=True,
    )

    # Things to review
    needs_review = models.JSONField(
        default=list,
        blank=True,
    )

    # AI explanation
    feedback = models.TextField(
        blank=True,
    )

    # Raw AI response if needed later
    ai_metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    reviewed_by = models.CharField(
        max_length=30,
        default="ai",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Review: {self.application.title}"
