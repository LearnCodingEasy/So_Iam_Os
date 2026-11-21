from codex.services.intelligence import test_plan
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class TestPlanView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        return Response(test_plan(project, request.data.get('target', ''), request.user))
