from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Agent(models.Model):
    """An AI agent definition owned by one user."""

    STATUS_CHOICES = [('draft', 'Draft'), ('active', 'Active'), ('paused', 'Paused'), ('archived', 'Archived')]
    STATUS_DRAFT = 'draft'
    STATUS_ACTIVE = 'active'
    STATUS_PAUSED = 'paused'
    STATUS_ARCHIVED = 'archived'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agents')
    name = models.CharField(max_length=160)
    role = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    model_name = models.CharField(max_length=120, blank=True)
    system_prompt = models.TextField(blank=True)
    requires_approval = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.name)
