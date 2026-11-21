from codex.services.intelligence import ensure_tools
from codex.models import CodexTool
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class ToolsView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        ensure_tools(project)
        return Response(list(CodexTool.objects.filter(project=project).values()))
