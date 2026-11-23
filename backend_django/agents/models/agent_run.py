from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class AgentRun(models.Model):
    """One orchestrated attempt of an agent to reach a goal."""

    STATUS_CHOICES = [('pending', 'Pending'), ('awaiting_approval', 'Awaiting approval'), ('running', 'Running'), ('succeeded', 'Succeeded'), ('failed', 'Failed'), ('cancelled', 'Cancelled')]
    STATUS_PENDING = 'pending'
    STATUS_AWAITING_APPROVAL = 'awaiting_approval'
    STATUS_RUNNING = 'running'
    STATUS_SUCCEEDED = 'succeeded'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'
    TERMINAL_STATUSES = ('succeeded', 'failed', 'cancelled')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_runs')
    agent = models.ForeignKey('agents.Agent', on_delete=models.CASCADE, related_name='runs')
    configuration = models.ForeignKey('agents.AgentConfiguration', null=True, blank=True, on_delete=models.SET_NULL, related_name='runs')
    goal = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    input_data = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str('%s:%s' % (self.agent_id, self.status))
