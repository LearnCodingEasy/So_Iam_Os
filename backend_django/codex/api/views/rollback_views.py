from codex.services.execution import rollback_changes
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class RollbackView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request, changeset_id):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        try:
            return Response(rollback_changes(request.user, project, changeset_id, request.data.get('confirm') is True))
        except PermissionError as exc:
            return Response({'detail': str(exc)}, status=403)
        except Exception as exc:
            return Response({'detail': str(exc)}, status=400)
