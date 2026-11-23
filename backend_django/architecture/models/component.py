from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Component(models.Model):
    """A building block of an architecture (service, database, queue, ...)."""

    TYPE_CHOICES = [('service', 'Service'), ('database', 'Database'), ('queue', 'Queue'), ('frontend', 'Frontend'), ('library', 'Library'), ('external', 'External'), ('other', 'Other')]
    TYPE_SERVICE = 'service'
    TYPE_DATABASE = 'database'
    TYPE_QUEUE = 'queue'
    TYPE_FRONTEND = 'frontend'
    TYPE_LIBRARY = 'library'
    TYPE_EXTERNAL = 'external'
    TYPE_OTHER = 'other'

    architecture = models.ForeignKey('architecture.Architecture', on_delete=models.CASCADE, related_name='components')
    name = models.CharField(max_length=160)
    component_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='service')
    description = models.TextField(blank=True)
    technology = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['architecture', 'name'], name='architecture_component_name_unique'),
        ]

    def __str__(self):
        return str(self.name)
