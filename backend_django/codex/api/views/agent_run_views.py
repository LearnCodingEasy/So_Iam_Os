from codex.models import CodexAgentRun
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class AgentRunView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        return Response(list(CodexAgentRun.objects.filter(project=project).order_by('-created_at')[:100].values()))
