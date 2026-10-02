# codex/services/project_context.py
from django.db.models import Q

from ..models import (
    ProjectRegistry,
    Feature,
    FileRegistry,
    APIEndpoint,
    ProtectedFeature,
    ArchitectureNode,
    ArchitectureEdge,
    CodexPolicy,
    CodexTool,
    CodexFinding,
)


class ProjectContextService:

    def __init__(self, project=None):
        self.project = project or ProjectRegistry.objects.get(
            key="so_iam_os"
        )

    def build_context(self, query: str):

        query = (query or "").strip()

        features = self._features(query)
        files = self._files(query)
        apis = self._apis(query)

        frontend_files = [
            item
            for item in files
            if (
                item["kind"] == "vue"
                or "frontend" in item["path"].lower()
            )
        ]

        backend_files = [
            item
            for item in files
            if (
                item["kind"] == "python"
                or "backend" in item["path"].lower()
            )
        ]

        protected = list(
            ProtectedFeature.objects.filter(
                project=self.project,
                enabled=True,
            ).values(
                "key",
                "reason",
                "paths",
                "rules",
            )
        )

        return {
            "project": {
                "key": self.project.key,
                "name": self.project.name,
                "root_path": self.project.root_path,
                "scanned_at": (
                    self.project.scanned_at.isoformat()
                    if self.project.scanned_at
                    else None
                ),
            },
            "query": query,
            "features": features,
            "files": files,
            "frontend_files": frontend_files,
            "backend_files": backend_files,
            "apis": apis,
            "protected": protected,
            "architecture": {
                "nodes": ArchitectureNode.objects.filter(project=self.project).count(),
                "edges": ArchitectureEdge.objects.filter(project=self.project).count(),
            },
            "tools": list(CodexTool.objects.filter(project=self.project, enabled=True).values("key", "name", "capability")),
            "security_findings": list(CodexFinding.objects.filter(project=self.project, resolved=False).values("category", "severity", "title", "path", "line", "message")[:100]),
        }

    def _features(self, query):
        qs = Feature.objects.filter(
            project=self.project
        )

        if query:
            qs = qs.filter(
                Q(key__icontains=query)
                | Q(name__icontains=query)
                | Q(app_label__icontains=query)
                | Q(description__icontains=query)
            )

        return list(
            qs.values(
                "id",
                "key",
                "name",
                "app_label",
                "description",
                "status",
                "protected",
            )[:100]
        )

    def _files(self, query):
        qs = FileRegistry.objects.filter(
            project=self.project
        )

        if query:
            qs = qs.filter(
                Q(path__icontains=query)
                | Q(kind__icontains=query)
                | Q(app_label__icontains=query)
            )

        return list(
            qs.values(
                "id",
                "path",
                "kind",
                "app_label",
                "sha256",
                "size",
                "protected",
            )[:200]
        )

    def _apis(self, query):
        qs = APIEndpoint.objects.filter(
            project=self.project
        )

        if query:
            qs = qs.filter(
                Q(path__icontains=query)
                | Q(name__icontains=query)
                | Q(app_label__icontains=query)
                | Q(frontend_service__icontains=query)
            )

        return list(
            qs.values(
                "id",
                "method",
                "path",
                "name",
                "source",
                "app_label",
                "frontend_route",
                "frontend_section",
                "frontend_service",
                "coverage_status",
                "protected",
            )[:200]
        )
