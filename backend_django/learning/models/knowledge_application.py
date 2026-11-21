from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from learning.models.learning_topic import LearningTopic
from learning.models.lesson import Lesson


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
