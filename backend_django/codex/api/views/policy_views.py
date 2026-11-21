from codex.services.intelligence import ensure_policy
from codex.models import CodexAuditEvent
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class PolicyView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'permissions': ensure_policy(project, request.user).permissions})

    def patch(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        policy = ensure_policy(project, request.user)
        permissions = dict(policy.permissions)
        permissions.update(request.data.get('permissions', {}))
        policy.permissions = permissions
        policy.save(update_fields=['permissions', 'updated_at'])
        CodexAuditEvent.objects.create(project=project, user=request.user, event_type='policy',
                                       action='policy.update', payload={'permissions': permissions})
        return Response({'permissions': permissions})
