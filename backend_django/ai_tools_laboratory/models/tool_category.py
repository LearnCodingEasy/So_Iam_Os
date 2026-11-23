from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class ToolCategory(models.Model):
    """A user-defined grouping for tools in the laboratory."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_tool_categories')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='ai_tool_category_user_name_unique'),
        ]

    def __str__(self):
        return str(self.name)
