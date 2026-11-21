from django.db import models
from codex.models.architecture_node import ArchitectureNode
from codex.models.project_registry import ProjectRegistry


class ArchitectureEdge(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='architecture_edges')
    source = models.ForeignKey(
        ArchitectureNode, on_delete=models.CASCADE, related_name='out_edges')
    target = models.ForeignKey(
        ArchitectureNode, on_delete=models.CASCADE, related_name='in_edges')
    relation = models.CharField(max_length=120)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['project', 'source', 'target', 'relation'], name='codex_arch_edge_unique')]
