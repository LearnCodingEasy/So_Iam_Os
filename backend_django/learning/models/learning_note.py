from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from learning.models.learning_topic import LearningTopic
from learning.models.lesson import Lesson


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
