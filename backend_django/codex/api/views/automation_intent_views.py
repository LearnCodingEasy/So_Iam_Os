from codex.services.intelligence import ensure_policy
from codex.models import CodexAuditEvent
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class AutomationIntentView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        policy = ensure_policy(project, request.user)
        intent = request.data.get('intent', '').strip()
        if not intent:
            return Response({'detail': 'intent is required'}, status=400)
        allowed = policy.permissions.get('AUTOMATION', 'DENY')
        plan = {'intent': intent, 'status': 'planned', 'requires_approval': allowed != 'ALLOW', 'policy': allowed,
                'actions': [{'action': 'analyze_intent'}, {'action': 'resolve_automation_tool'}, {'action': 'request_approval' if allowed != 'ALLOW' else 'execute'}],
                'guardrails': ['Codex never executes arbitrary automation from natural language', 'Destructive actions require approval', 'All actions are audited']}
        CodexAuditEvent.objects.create(project=project, user=request.user,
                                       event_type='automation', action='automation.plan', payload=plan)
        return Response(plan, status=201)
