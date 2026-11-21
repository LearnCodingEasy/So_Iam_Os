from codex.services.intelligence import build_graph, security_scan, ensure_policy, ensure_tools
from codex.models import CodexTool
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


# ---------------------------------------------------------------------------
# Codex V2 — project brain / safe agent / developer tools
# ---------------------------------------------------------------------------


class IntelligenceBootstrapView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key='so_iam_os', defaults={'name': 'SO_IAM_OS'})[0]
        ensure_tools(project)
        ensure_policy(project, request.user)
        graph = build_graph(project)
        findings = security_scan(project, request.user)
        return Response({'graph': graph, 'security_findings': len(findings), 'tools': CodexTool.objects.filter(project=project, enabled=True).count()})
