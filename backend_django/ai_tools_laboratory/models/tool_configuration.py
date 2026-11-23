from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class ToolConfiguration(models.Model):
    """A named set of non-secret settings for a tool. Credentials are never stored here."""

    tool = models.ForeignKey('ai_tools_laboratory.Tool', on_delete=models.CASCADE, related_name='configurations')
    name = models.CharField(max_length=120)
    settings = models.JSONField(default=dict, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', 'name']

    def __str__(self):
        return str(self.name)
