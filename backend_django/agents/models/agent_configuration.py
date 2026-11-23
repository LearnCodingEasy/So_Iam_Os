from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class AgentConfiguration(models.Model):
    """A numbered, versioned configuration of an agent. Only one version is active."""

    agent = models.ForeignKey('agents.Agent', on_delete=models.CASCADE, related_name='configurations')
    version = models.PositiveIntegerField(default=1)
    temperature = models.FloatField(default=0.2)
    max_steps = models.PositiveIntegerField(default=10)
    tools = models.JSONField(default=list, blank=True)
    parameters = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version']
        constraints = [
            models.UniqueConstraint(fields=['agent', 'version'], name='agent_configuration_version_unique'),
        ]

    def __str__(self):
        return str('%s v%s' % (self.agent_id, self.version))
