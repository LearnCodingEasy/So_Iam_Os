from codex.services.execution import apply_changes
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class ApplyChangesView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        try:
            return Response(apply_changes(request.user, project, request.data.get('title', 'Codex change'), request.data.get('objective', ''), request.data.get('changes', []), request.data.get('confirm') is True), status=201)
        except PermissionError as exc:
            return Response({'detail': str(exc)}, status=403)
        except Exception as exc:
            return Response({'detail': str(exc)}, status=400)
