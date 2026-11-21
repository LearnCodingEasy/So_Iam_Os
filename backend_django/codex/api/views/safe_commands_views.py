from codex.services.execution import ALLOWED, run_safe
from codex.services.intelligence import ensure_policy
from codex.models import CodexAuditEvent
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class SafeCommandsView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        policy = ensure_policy(project, request.user)
        return Response({'commands': [{'key': k, 'command': v, 'policy': policy.permissions.get('RUN_COMMANDS', 'DENY')} for k, v in ALLOWED.items()]})

    def post(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        key = request.data.get('key', '')
        if request.data.get('confirm') is not True:
            return Response({'detail': 'Explicit confirmation is required.', 'key': key}, status=400)
        try:
            result = run_safe(request.user, project, key)
        except PermissionError as exc:
            CodexAuditEvent.objects.create(project=project, user=request.user, event_type='command',
                                           action=key, status='denied', payload={'reason': str(exc)})
            return Response({'detail': str(exc)}, status=403)
        except Exception as exc:
            return Response({'detail': str(exc)}, status=400)
        return Response(result)
