from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Dependency(models.Model):
    """A directed dependency: ``source`` depends on ``target`` (same architecture, acyclic)."""

    TYPE_CHOICES = [('depends_on', 'Depends on'), ('calls', 'Calls'), ('reads', 'Reads from'), ('writes', 'Writes to')]
    TYPE_DEPENDS_ON = 'depends_on'
    TYPE_CALLS = 'calls'
    TYPE_READS = 'reads'
    TYPE_WRITES = 'writes'

    source = models.ForeignKey('architecture.Component', on_delete=models.CASCADE, related_name='outgoing_dependencies')
    target = models.ForeignKey('architecture.Component', on_delete=models.CASCADE, related_name='incoming_dependencies')
    dependency_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='depends_on')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['source', 'target', 'dependency_type'], name='architecture_dependency_unique'),
        ]

    def __str__(self):
        return str('%s -> %s' % (self.source_id, self.target_id))
