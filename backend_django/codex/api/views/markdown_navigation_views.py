from codex.services.extensions import markdown_index
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class MarkdownNavigationView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        try:
            return Response(markdown_index(project, request.data.get("path", "")))
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
