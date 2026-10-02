from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    class Type(models.TextChoices):
        SYSTEM = "system", "System"
        TASK = "task", "Task"
        GOAL = "goal", "Goal"
        LEARNING = "learning", "Learning"
        KNOWLEDGE = "knowledge", "Knowledge"
        JOB = "job", "Job"
        AI = "ai", "AI"
        SOCIAL = "social", "Social"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=30, choices=Type.choices, default=Type.SYSTEM)
    title = models.CharField(max_length=255)
    message = models.TextField()
    action_url = models.CharField(max_length=500, blank=True)
    priority = models.PositiveSmallIntegerField(default=50)
    read_at = models.DateTimeField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.CharField(max_length=255, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "read_at", "created_at"]),
            models.Index(fields=["user", "type", "created_at"]),
        ]

    @property
    def is_read(self):
        return self.read_at is not None

    def mark_read(self):
        if not self.read_at:
            self.read_at = timezone.now()
            self.save(update_fields=["read_at"])


class NotificationService:
    @staticmethod
    def create(user, *, type=Notification.Type.SYSTEM, title, message, action_url="", priority=50, obj=None, metadata=None):
        kwargs = dict(user=user, type=type, title=title, message=message, action_url=action_url, priority=priority, metadata=metadata or {})
        if obj is not None:
            kwargs["content_type"] = ContentType.objects.get_for_model(obj.__class__)
            kwargs["object_id"] = str(obj.pk)
        return Notification.objects.create(**kwargs)
