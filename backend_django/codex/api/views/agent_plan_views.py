from codex.services.intelligence import agent_plan
from codex.models import CodexAgentRun
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class AgentPlanView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        result = agent_plan(project, request.data.get(
            'request', ''), request.user)
        run = CodexAgentRun.objects.create(
            project=project, user=request.user, request=request.data.get('request', ''), plan=result)
        result['run_id'] = run.id
        return Response(result, status=201)
