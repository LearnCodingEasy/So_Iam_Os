from django.core.exceptions import ValidationError
from django.db import models
from learning.models.common import MINUTES_VALIDATORS
from learning.models.learning_path import LearningPath
from learning.models.skill import Skill


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
