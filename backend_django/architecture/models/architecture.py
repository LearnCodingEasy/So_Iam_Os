from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Architecture(models.Model):
    """A system architecture the user is designing or documenting."""

    STATUS_CHOICES = [('draft', 'Draft'), ('active', 'Active'), ('deprecated', 'Deprecated')]
    STATUS_DRAFT = 'draft'
    STATUS_ACTIVE = 'active'
    STATUS_DEPRECATED = 'deprecated'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='architectures')
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    version = models.CharField(max_length=40, default='1.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.name)
