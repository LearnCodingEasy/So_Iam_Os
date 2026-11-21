from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry
from codex.api.serializers import ProjectSerializer


class OverviewView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        return Response({"project": ProjectSerializer(project).data, "counts": {"features": project.features.count(), "files": project.files.count(), "apis": project.apis.count(), "protected": project.protected_features.filter(enabled=True).count(), "changes": project.changesets.count(), "snapshots": project.snapshots.count()}, "guarantee": "Every discovered backend API is represented in the frontend Codex API Registry at /codex."})
