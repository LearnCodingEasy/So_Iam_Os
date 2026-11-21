from codex.services.extensions import local_file_link
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class LocalFileOpenView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        try:
            return Response(local_file_link(project, request.data.get("path", "")))
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
