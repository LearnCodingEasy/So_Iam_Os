from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry
from codex.services.context_builder import ContextBuilder


class ContextView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get(key="so_iam_os")
        return Response(ContextBuilder.build(project))
