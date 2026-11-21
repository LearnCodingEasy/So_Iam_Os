from codex.services.intelligence import security_scan
from codex.models import CodexFinding
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class SecurityScanView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'findings': security_scan(project, request.user)})

    def get(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'findings': list(CodexFinding.objects.filter(project=project, category='security', resolved=False).values())})
