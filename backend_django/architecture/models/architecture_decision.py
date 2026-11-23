from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class ArchitectureDecision(models.Model):
    """An architecture decision record (ADR)."""

    STATUS_CHOICES = [('proposed', 'Proposed'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('deprecated', 'Deprecated'), ('superseded', 'Superseded')]
    STATUS_PROPOSED = 'proposed'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_DEPRECATED = 'deprecated'
    STATUS_SUPERSEDED = 'superseded'

    architecture = models.ForeignKey('architecture.Architecture', on_delete=models.CASCADE, related_name='decisions')
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='proposed')
    context = models.TextField(blank=True)
    decision = models.TextField(blank=True)
    consequences = models.TextField(blank=True)
    superseded_by = models.ForeignKey('architecture.ArchitectureDecision', null=True, blank=True, on_delete=models.SET_NULL, related_name='supersedes')
    decided_on = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)
