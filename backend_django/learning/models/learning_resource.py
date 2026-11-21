from django.core.exceptions import ValidationError
from django.db import models
from learning.models.learning_topic import LearningTopic
from learning.models.lesson import Lesson


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
