from django.core.exceptions import ValidationError
from django.db import models
from learning.models.common import MINUTES_VALIDATORS
from learning.models.learning_topic import LearningTopic


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
