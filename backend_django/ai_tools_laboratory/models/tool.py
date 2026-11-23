from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Tool(models.Model):
    """An AI tool being evaluated, adopted or rejected by the user."""

    STATUS_CHOICES = [('evaluating', 'Evaluating'), ('adopted', 'Adopted'), ('rejected', 'Rejected'), ('archived', 'Archived')]
    STATUS_EVALUATING = 'evaluating'
    STATUS_ADOPTED = 'adopted'
    STATUS_REJECTED = 'rejected'
    STATUS_ARCHIVED = 'archived'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_tools')
    category = models.ForeignKey('ai_tools_laboratory.ToolCategory', null=True, blank=True, on_delete=models.SET_NULL, related_name='tools')
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    vendor = models.CharField(max_length=160, blank=True)
    website_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='evaluating')
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    pricing_model = models.CharField(max_length=80, blank=True)
    tags = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.name)
