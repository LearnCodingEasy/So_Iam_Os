from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class AgentExecution(models.Model):
    """A recorded step of an AgentRun. Written by the execution service only."""

    STATUS_CHOICES = [('pending', 'Pending'), ('running', 'Running'), ('succeeded', 'Succeeded'), ('failed', 'Failed'), ('skipped', 'Skipped')]
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_SUCCEEDED = 'succeeded'
    STATUS_FAILED = 'failed'
    STATUS_SKIPPED = 'skipped'

    run = models.ForeignKey('agents.AgentRun', on_delete=models.CASCADE, related_name='executions')
    step_index = models.PositiveIntegerField(default=0)
    action = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    input_data = models.JSONField(default=dict, blank=True)
    output_data = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)
    duration_ms = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['step_index', 'id']

    def __str__(self):
        return str('%s#%s' % (self.run_id, self.step_index))
