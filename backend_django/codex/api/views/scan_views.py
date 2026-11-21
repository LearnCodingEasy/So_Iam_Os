from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.services.project_scanner import ProjectScanner


class ScanView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        return Response(ProjectScanner().run())
