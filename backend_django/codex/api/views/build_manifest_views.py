from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class BuildManifestView(APIView):
    """Generate the versioned build manifest on explicit POST only."""
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        from codex.services.build_workspace import export_manifest
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"}
        )[0]
        return Response(export_manifest(project))
