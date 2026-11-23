from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class ToolExecution(models.Model):
    """A manual log entry of one trial run of a tool (the laboratory does not run tools itself)."""

    STATUS_CHOICES = [('pending', 'Pending'), ('succeeded', 'Succeeded'), ('failed', 'Failed')]
    STATUS_PENDING = 'pending'
    STATUS_SUCCEEDED = 'succeeded'
    STATUS_FAILED = 'failed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_tool_executions')
    tool = models.ForeignKey('ai_tools_laboratory.Tool', on_delete=models.CASCADE, related_name='executions')
    configuration = models.ForeignKey('ai_tools_laboratory.ToolConfiguration', null=True, blank=True, on_delete=models.SET_NULL, related_name='executions')
    input_text = models.TextField(blank=True)
    output_text = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    duration_ms = models.PositiveIntegerField(null=True, blank=True)
    executed_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-executed_at']

    def __str__(self):
        return str('%s:%s' % (self.tool_id, self.status))
