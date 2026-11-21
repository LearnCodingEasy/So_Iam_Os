from django.db import models
from codex.models.project_registry import ProjectRegistry


class ArchitectureNode(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='architecture_nodes')
    key = models.CharField(max_length=500)
    kind = models.CharField(max_length=80)
    label = models.CharField(max_length=300)
    path = models.CharField(max_length=700, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['project', 'key'], name='codex_arch_node_unique')]
