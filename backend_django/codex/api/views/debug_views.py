from codex.services.intelligence import debug_error
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class DebugView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        return Response(debug_error(project, request.data.get('error', ''), request.user))
