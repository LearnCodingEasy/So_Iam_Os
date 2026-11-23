from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Company(models.Model):
    """An organization the user does business with."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crm_companies')
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=120, blank=True)
    website = models.URLField(blank=True)
    size = models.CharField(max_length=60, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
