from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


# ---------------------------------------------------------------------------
# Codex Capability Registry — 300 Features / 300 Tools / 300 Agents
# ---------------------------------------------------------------------------


class CapabilityRegistryMixin:
    permission_classes = [CodexAuthenticated]

    def project(self, *, create=False):
        if create:
            return ProjectRegistry.objects.get_or_create(key='so_iam_os', defaults={'name': 'SO_IAM_OS'})[0]
        return ProjectRegistry.objects.filter(key='so_iam_os').first()

    def require_project(self):
        project = self.project()
        if project is None:
            from rest_framework.exceptions import NotFound
            raise NotFound(
                'Codex project registry has not been bootstrapped yet.')
        return project
